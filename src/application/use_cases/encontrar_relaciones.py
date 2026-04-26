from dataclasses import dataclass
from typing import List, Tuple

from application.ports.output_port import KmlOutputPort, TxtOutputPort
from domain.entities.punto import Punto
from domain.entities.red import Red
from domain.entities.relacion import Relacion
from application.gateways.elevation_gateway import ElevationGateway
from application.gateways.punto_gateway import PuntoGateway
from domain.services.line_of_sight_service import LineOfSightService
from domain.services.network_analysis_service import NetworkAnalysisService


@dataclass
class EncontrarRelacionesUnArchivoRequest:
    nombre_archivo: str
    distancia_maxima: float


@dataclass
class EncontrarRelacionesUnArchivoResponse:
    relaciones: List[Relacion]


@dataclass
class EncontrarRelacionesArbolRequest:
    nombre_conectados: str
    nombre_no_conectados: str
    distancia_maxima: float


@dataclass
class EncontrarRelacionesArbolResponse:
    relaciones_exitosas: List[Relacion]
    relaciones_con_error: List[Relacion]


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

    def __init__(
        self,
        punto_repo: PuntoGateway,
        elevation_repo: ElevationGateway,
        kml_output: KmlOutputPort,
        txt_output: TxtOutputPort,
        muestras: int,
    ) -> None:
        self._punto_repo = punto_repo
        self._elevation_repo = elevation_repo
        self._kml_output = kml_output
        self._txt_output = txt_output
        self._muestras = muestras

    # ------------------------------------------------------------------ verificador LOS

    def _verificar_los(self, p1: Punto, p2: Punto) -> bool:
        try:
            puntos_elev, _ = self._elevation_repo.obtener_perfil_de_puntos(
                p1, p2, self._muestras
            )
            return LineOfSightService.verificar_linea_de_vista(puntos_elev, p1, p2)
        except Exception as exc:
            print(
                f"EncontrarRelacionesUseCase: error al verificar LOS "
                f"entre '{p1.nombre}' y '{p2.nombre}': {exc}"
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
        puntos = self._punto_repo.leer_puntos(request.nombre_archivo)
        relaciones = []
        for i in range(len(puntos)):
            for j in range(i + 1, len(puntos)):
                re = Relacion(puntos[i], puntos[j])
                if re.distancia < request.distancia_maxima:
                    if self._verificar_los(puntos[i], puntos[j]):
                        relaciones.append(re)
                print(f"  par {i}-{j}")

        self._kml_output.escribir_rutas(relaciones, request.nombre_archivo, altitud_absoluta=True)
        self._punto_repo.guardar_relaciones(relaciones, "relacion")
        return EncontrarRelacionesUnArchivoResponse(relaciones=relaciones)

    def ejecutar_dos_archivos_arbol(
        self,
        request: EncontrarRelacionesArbolRequest,
    ) -> EncontrarRelacionesArbolResponse:
        """
        Lee dos archivos (puntos ya conectados y puntos sin conexión)
        y construye el árbol de conexión mínimo.
        """
        conectados = self._punto_repo.leer_puntos(request.nombre_conectados)
        no_conectados = self._punto_repo.leer_puntos(request.nombre_no_conectados)

        exitosas, errores = NetworkAnalysisService.encontrar_menor_relacion(
            lista1=conectados,
            lista2=no_conectados,
            distancia_maxima=request.distancia_maxima,
            verifica_los=self._verificar_los,
        )

        self._kml_output.escribir_rutas(exitosas, request.nombre_conectados, altitud_absoluta=True)
        self._kml_output.escribir_rutas(errores, request.nombre_conectados + "_errores", altitud_absoluta=True)
        self._punto_repo.guardar_relaciones(exitosas, "relacion")
        self._punto_repo.guardar_relaciones(errores, "relacion_errores")
        return EncontrarRelacionesArbolResponse(
            relaciones_exitosas=exitosas,
            relaciones_con_error=errores,
        )

    def ejecutar_clusterizar(
        self,
        request: EncontrarRelacionesClusterizarRequest,
    ) -> EncontrarRelacionesClusterizarResponse:
        """
        Agrupa los puntos en clusters conectados por LOS y distancia.
        """
        puntos = self._punto_repo.leer_puntos(request.nombre_archivo)
        redes, relaciones = NetworkAnalysisService.clusterizar(
            lista=puntos,
            verifica_los=self._verificar_los,
            distancia_maxima=request.distancia_maxima,
        )
        self._kml_output.escribir_rutas(relaciones, request.nombre_archivo + "_rutas", altitud_absoluta=True)
        self._punto_repo.guardar_relaciones(relaciones, "relacion")
        return EncontrarRelacionesClusterizarResponse(redes=redes, relaciones=relaciones)
