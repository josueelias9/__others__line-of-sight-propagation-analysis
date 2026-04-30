import logging
from dataclasses import dataclass
from typing import List, Tuple

from application.interface.ports.output import KmlOutputPort, TxtOutputPort
from domain.entities.punto import Punto
from domain.entities.red import Red
from domain.entities.relacion import Relacion
from application.interface.ports.elevation import ElevationGateway
from application.interface.db.punto import PuntoGateway

logger = logging.getLogger(__name__)


@dataclass
class EncontrarRelacionesUnArchivoRequest:
    distancia_maxima: float


@dataclass
class EncontrarRelacionesUnArchivoResponse:
    relaciones: List[Relacion]


@dataclass
class EncontrarRelacionesArbolRequest:
    tipo_conectados: str
    tipo_no_conectados: str
    distancia_maxima: float


@dataclass
class EncontrarRelacionesArbolResponse:
    relaciones_exitosas: List[Relacion]
    puntos_sin_conexion: List[Punto]


@dataclass
class EncontrarRelacionesClusterizarRequest:
    nombre_archivo: str
    distancia_maxima: float


@dataclass
class EncontrarRelacionesClusterizarResponse:
    redes: List[Red]
    relaciones: List[Relacion]


class EncontrarRelacionesUseCase:
    """
    Caso de uso: encontrar todas las relaciones posibles entre puntos
    con línea de vista y dentro de una distancia máxima.

    Pertenece a la capa de Aplicación.
    """
    # TODO punto_repo tiene que cambiarse a data_repo o store_repo porque ahora se guardaran relaciones y no solo puntos.
    def __init__(
        self,
        punto_repo: PuntoGateway,
        elevation_repo: ElevationGateway,
        kml_output: KmlOutputPort,
        muestras: int,
    ) -> None:
        self._punto_repo = punto_repo
        self._elevation_repo = elevation_repo
        self._kml_output = kml_output
        self._muestras = muestras

    # ------------------------------------------------------------------ verificador LOS

    def _verificar_los(self, p1: Punto, p2: Punto) -> bool:
        try:
            puntos_elev, _ = self._elevation_repo.obtener_perfil_de_puntos(
                p1, p2, self._muestras
            )
            return Relacion(p1, p2).verificar_linea_de_vista(puntos_elev)
        except Exception as exc:
            logger.warning(
                "error al verificar LOS entre '%s' y '%s': %s",
                p1.nombre, p2.nombre, exc,
            )
            return False

    # ------------------------------------------------------------------ casos de uso

    def ejecutar_un_archivo(
        self,
        request: EncontrarRelacionesUnArchivoRequest,
    ) -> EncontrarRelacionesUnArchivoResponse:
        """
        Lee un solo archivo de puntos y encuentra todas las relaciones
        posibles con LOS dentro de la distancia máxima.
        """
        logger.info("🟢")
        puntos = self._punto_repo.leer_puntos()
        relaciones = []
        for i in range(len(puntos)):
            for j in range(i + 1, len(puntos)):
                re = Relacion(puntos[i], puntos[j])
                if re.distancia < request.distancia_maxima:
                    if self._verificar_los(puntos[i], puntos[j]):
                        relaciones.append(re)
                logger.debug("par %d-%d evaluado", i, j)

        self._kml_output.escribir_rutas(relaciones, "relaciones_un_archivo", altitud_absoluta=True)
        self._punto_repo.guardar_relaciones(relaciones)
        logger.info("🔴")
        return EncontrarRelacionesUnArchivoResponse(relaciones=relaciones)

    def ejecutar_dos_archivos_arbol(
        self,
        request: EncontrarRelacionesArbolRequest,
    ) -> EncontrarRelacionesArbolResponse:
        """
        Lee los puntos de `punto.csv` filtrando por tipo y construye
        el árbol de conexión mínimo.
        """
        logger.info("🟢")
        conectados = self._punto_repo.leer_puntos(request.tipo_conectados)
        no_conectados = self._punto_repo.leer_puntos(request.tipo_no_conectados)

        for p in conectados:
            p.conectado = True

        for p in no_conectados:
            p.conectado = False

        exitosas, sin_conexion = Red.encontrar_menor_relacion(
            lista1=conectados,
            lista2=no_conectados,
            distancia_maxima=request.distancia_maxima,
            verifica_los=self._verificar_los,
        )

        for rel in exitosas:
            rel.punto_final.conectado = True

        self._kml_output.escribir_rutas(exitosas, f"{request.tipo_conectados}_arbol", altitud_absoluta=True)
        self._punto_repo.guardar_relaciones(exitosas)
        self._punto_repo.actualizar_conectado(conectados + no_conectados)
        logger.info("🔴")
        return EncontrarRelacionesArbolResponse(
            relaciones_exitosas=exitosas,
            puntos_sin_conexion=sin_conexion,
        )

    def ejecutar_clusterizar(
        self,
        request: EncontrarRelacionesClusterizarRequest,
    ) -> EncontrarRelacionesClusterizarResponse:
        """
        Agrupa los puntos en clusters conectados por LOS y distancia.
        """
        logger.info("🟢")
        puntos = self._punto_repo.leer_puntos(request.nombre_archivo)
        redes, relaciones = Red.clusterizar(
            lista=puntos,
            verifica_los=self._verificar_los,
            distancia_maxima=request.distancia_maxima,
        )
        self._kml_output.escribir_rutas(relaciones, request.nombre_archivo + "_rutas", altitud_absoluta=True)
        self._punto_repo.guardar_relaciones(relaciones)
        logger.info("🔴")
        return EncontrarRelacionesClusterizarResponse(redes=redes, relaciones=relaciones)
