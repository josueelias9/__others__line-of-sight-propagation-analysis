import logging
from dataclasses import dataclass, field
from itertools import combinations
from typing import List, Optional, Tuple

from application.interface.ports.geometry import AreaGeometrica, GeometryGateway
from application.interface.ports.output import KmlOutputPort, TxtOutputPort
from application.use_cases.generar_poligono_cobertura import (
    GenerarPoligonoCoberturaRequest,
    GenerarPoligonoCoberturaUseCase,
)
from domain.entities.punto import Punto
from domain.entities.relacion import Relacion
from application.interface.db.punto import PuntoGateway

logger = logging.getLogger(__name__)


@dataclass
class EncontrarTorreFantasmaRequest:
    nombre_salida: str
    reduccion_maxima: int = 3
    ubigeos: Optional[List[int]] = None


@dataclass
class EncontrarTorreFantasmaResponse:
    encontrado: bool


@dataclass
class EncontrarTorreFantasmaDosArchivosRequest:
    nombre_no_conectados: str
    nombre_conectados: str
    nombre_salida_prefijo: str


@dataclass
class EncontrarTorreFantasmaDosArchivosResponse:
    pass


class EncontrarTorreFantasmaUseCase:
    """
    Caso de uso: encontrar la ubicación óptima para una torre repetidora
    (torre fantasma) que conecte puntos sin servicio.

    Estrategia: intersectar los polígonos de cobertura de todos los puntos
    de una lista buscando un área común que cubra a todos. Si no existe,
    se prueba con subconjuntos de tamaño decreciente.

    Pertenece a la capa de Aplicación.
    """

    def __init__(
        self,
        punto_repo: PuntoGateway,
        cobertura_uc: GenerarPoligonoCoberturaUseCase,
        geometry_gw: GeometryGateway,
        kml_output: KmlOutputPort,
        txt_output: TxtOutputPort,
        distancia_maxima: float,
    ) -> None:
        self._punto_repo = punto_repo
        self._cobertura_uc = cobertura_uc
        self._geometry_gw = geometry_gw
        self._kml_output = kml_output
        self._txt_output = txt_output
        self._distancia_maxima = distancia_maxima

    # ------------------------------------------------------------------ API pública

    def ejecutar(
        self,
        request: EncontrarTorreFantasmaRequest,
    ) -> EncontrarTorreFantasmaResponse:
        """
        Lee los puntos de `punto.csv` y busca la intersección
        de sus polígonos de cobertura.

        `request.reduccion_maxima` indica cuántos puntos se pueden eliminar
        de la lista antes de abandonar la búsqueda.
        """
        logger.info("🟢")
        puntos = self._punto_repo.leer_puntos()
        if request.ubigeos:
            puntos = [p for p in puntos if p.ubigeo in request.ubigeos]
        logger.info("%d puntos cargados.", len(puntos))

        for eliminados in range(request.reduccion_maxima):
            longitud_subconjunto = len(puntos) - eliminados
            for tupla in combinations(puntos, longitud_subconjunto):
                if not self._todos_a_distancia_razonable(list(tupla)):
                    continue

                area, poligono = self._intersectar_coberturas(list(tupla))
                if area:
                    self._kml_output.escribir_area(poligono, request.nombre_salida)
                    self._txt_output.escribir_puntos(
                        list(tupla), request.nombre_salida + "_puntos"
                    )
                    logger.info("¡área encontrada!")
                    return EncontrarTorreFantasmaResponse(encontrado=True)

        logger.info("no se encontró área de intersección.")
        logger.info("🔴")
        return EncontrarTorreFantasmaResponse(encontrado=False)

    def ejecutar_dos_archivos(
        self,
        request: EncontrarTorreFantasmaDosArchivosRequest,
    ) -> EncontrarTorreFantasmaDosArchivosResponse:
        """
        Para cada punto no conectado busca la intersección de su cobertura
        con la cobertura de los puntos conectados más cercanos.
        """
        no_conectados = self._punto_repo.leer_puntos(request.nombre_no_conectados)
        conectados = self._punto_repo.leer_puntos(request.nombre_conectados)

        for i, nc in enumerate(no_conectados):
            logger.debug("Nodo no conectado %d: %s", i, nc.nombre)
            resp_nc = self._cobertura_uc.ejecutar(
                GenerarPoligonoCoberturaRequest(punto=nc)
            )
            area_nc = self._geometry_gw.estructura_a_area(resp_nc.estructura)
            area_actual = area_nc

            candidatos = sorted(
                [
                    Relacion(nc, c)
                    for c in conectados
                    if Relacion(nc, c).distancia < self._distancia_maxima * 2
                ],
                key=lambda r: r.distancia,
            )

            for j, rel in enumerate(candidatos):
                resp_c = self._cobertura_uc.ejecutar(
                    GenerarPoligonoCoberturaRequest(punto=rel.punto_final)
                )
                area_c = self._geometry_gw.estructura_a_area(resp_c.estructura)
                interseccion = self._geometry_gw.intersectar(area_actual, area_c)
                if not interseccion.vacia:
                    nombre = f"{nc.nombre}-{rel.punto_final.nombre}"
                    self._kml_output.escribir_area(
                        interseccion, request.nombre_salida_prefijo + nombre
                    )
                    logger.info(
                        "→ intersección encontrada con %s", rel.punto_final.nombre
                    )
                    break
                else:
                    area_actual = area_nc

        return EncontrarTorreFantasmaDosArchivosResponse()

    # ------------------------------------------------------------------ helpers privados

    def _todos_a_distancia_razonable(self, puntos: List[Punto]) -> bool:
        for i in range(len(puntos)):
            for j in range(i + 1, len(puntos)):
                if (
                    Relacion(puntos[i], puntos[j]).distancia
                    > self._distancia_maxima * 2
                ):
                    return False
        return True

    def _intersectar_coberturas(
        self, puntos: List[Punto]
    ) -> Tuple[bool, Optional[AreaGeometrica]]:
        if not puntos:
            return False, None

        resp = self._cobertura_uc.ejecutar(
            GenerarPoligonoCoberturaRequest(punto=puntos[0])
        )
        resultado = self._geometry_gw.estructura_a_area(resp.estructura)
        for pt in puntos[1:]:
            logger.debug(
                "intersectando con cobertura de %s con id %s", pt.nombre, pt.ubigeo
            )
            resp = self._cobertura_uc.ejecutar(
                GenerarPoligonoCoberturaRequest(punto=pt)
            )
            cobertura = self._geometry_gw.estructura_a_area(resp.estructura)
            resultado = self._geometry_gw.intersectar(resultado, cobertura)
            if resultado.vacia:
                return False, None

        return True, resultado
