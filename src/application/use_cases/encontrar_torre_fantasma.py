from itertools import combinations
from typing import List, Optional, Tuple

from shapely.geometry import mapping
from shapely.geometry.polygon import Polygon

from application.ports.output_port import KmlOutputPort, TxtOutputPort
from application.use_cases.generar_poligono_cobertura import (
    GenerarPoligonoCoberturaUseCase,
)
from domain.entities.punto import Punto
from domain.entities.relacion import Relacion
from domain.repositories.punto_repository import PuntoRepository


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
        punto_repo: PuntoRepository,
        cobertura_uc: GenerarPoligonoCoberturaUseCase,
        kml_output: KmlOutputPort,
        txt_output: TxtOutputPort,
        distancia_maxima: float,
    ) -> None:
        self._punto_repo = punto_repo
        self._cobertura_uc = cobertura_uc
        self._kml_output = kml_output
        self._txt_output = txt_output
        self._distancia_maxima = distancia_maxima

    # ------------------------------------------------------------------ API pública

    def ejecutar(
        self,
        nombre_archivo: str,
        nombre_salida: str,
        reduccion_maxima: int = 3,
    ) -> bool:
        """
        Lee los puntos de `nombre_archivo` y busca la intersección de sus
        polígonos de cobertura.

        `reduccion_maxima` indica cuántos puntos se pueden eliminar de la
        lista antes de abandonar la búsqueda.

        Devuelve True si se encontró una zona de intersección.
        """
        puntos = self._punto_repo.leer_puntos(nombre_archivo)
        print(f"EncontrarTorreFantasmaUseCase: {len(puntos)} puntos cargados.")

        for eliminados in range(reduccion_maxima):
            longitud_subconjunto = len(puntos) - eliminados
            for tupla in combinations(puntos, longitud_subconjunto):
                if not self._todos_a_distancia_razonable(list(tupla)):
                    continue

                area, poligono = self._intersectar_coberturas(list(tupla))
                if area:
                    self._kml_output.escribir_wkt(mapping(poligono), nombre_salida)
                    self._txt_output.escribir_puntos(list(tupla), nombre_salida + "_puntos")
                    print("EncontrarTorreFantasmaUseCase: ¡área encontrada!")
                    return True

        print("EncontrarTorreFantasmaUseCase: no se encontró área de intersección.")
        return False

    def ejecutar_dos_archivos(
        self,
        nombre_no_conectados: str,
        nombre_conectados: str,
        nombre_salida_prefijo: str,
    ) -> None:
        """
        Para cada punto no conectado busca la intersección de su cobertura
        con la cobertura de los puntos conectados más cercanos.
        """
        no_conectados = self._punto_repo.leer_puntos(nombre_no_conectados)
        conectados = self._punto_repo.leer_puntos(nombre_conectados)

        for i, nc in enumerate(no_conectados):
            print(f"  Nodo no conectado {i}: {nc.nombre}")
            cobertura_nc = self._cobertura_uc.ejecutar(nc)
            cobertura_actual = cobertura_nc

            candidatos = sorted(
                [Relacion(nc, c) for c in conectados if Relacion(nc, c).distancia < self._distancia_maxima * 2],
                key=lambda r: r.distancia,
            )

            for j, rel in enumerate(candidatos):
                cobertura_c = self._cobertura_uc.ejecutar(rel.punto_final)
                interseccion = cobertura_actual.intersection(cobertura_c)
                if interseccion.wkt != "GEOMETRYCOLLECTION EMPTY":
                    nombre = f"{nc.nombre}-{rel.punto_final.nombre}"
                    self._kml_output.escribir_wkt(
                        mapping(interseccion), nombre_salida_prefijo + nombre
                    )
                    print(f"    → intersección encontrada con {rel.punto_final.nombre}")
                    break
                else:
                    cobertura_actual = cobertura_nc
            print()

    # ------------------------------------------------------------------ helpers privados

    def _todos_a_distancia_razonable(self, puntos: List[Punto]) -> bool:
        for i in range(len(puntos)):
            for j in range(i + 1, len(puntos)):
                if Relacion(puntos[i], puntos[j]).distancia > self._distancia_maxima * 2:
                    return False
        return True

    def _intersectar_coberturas(
        self, puntos: List[Punto]
    ) -> Tuple[bool, Optional[Polygon]]:
        if not puntos:
            return False, None

        resultado = self._cobertura_uc.ejecutar(puntos[0])
        for pt in puntos[1:]:
            cobertura = self._cobertura_uc.ejecutar(pt)
            resultado = resultado.intersection(cobertura)
            if resultado.wkt == "GEOMETRYCOLLECTION EMPTY":
                return False, None

        return True, resultado
