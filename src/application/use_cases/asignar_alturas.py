from dataclasses import dataclass
from typing import List

from application.ports.output_port import TxtOutputPort
from domain.entities.punto import Punto
from application.gateways.elevation_gateway import ElevationGateway
from application.gateways.punto_gateway import PuntoGateway


@dataclass
class AsignarAlturasRequest:
    nombre_archivo: str


@dataclass
class AsignarAlturasResponse:
    puntos: List[Punto]


class AsignarAlturasUseCase:
    """
    Caso de uso: asignar la altura sobre el nivel del mar a una lista de puntos.

    1. Lee los puntos desde el repositorio.
    2. Para cada punto consulta la elevación al repositorio de elevación.
    3. Persiste los puntos actualizados vía el puerto de salida.

    Pertenece a la capa de Aplicación.
    """

    def __init__(
        self,
        punto_repo: PuntoGateway,
        elevation_repo: ElevationGateway,
        txt_output: TxtOutputPort,
    ) -> None:
        self._punto_repo = punto_repo
        self._elevation_repo = elevation_repo
        self._txt_output = txt_output

    def ejecutar(self, request: AsignarAlturasRequest) -> AsignarAlturasResponse:
        """
        Lee los puntos de `request.nombre_archivo`, asigna alturas y los guarda
        en el mismo nombre de archivo de salida.
        """
        puntos = self._punto_repo.leer_puntos(request.nombre_archivo)
        for i, punto in enumerate(puntos):
            self._elevation_repo.obtener_elevacion_punto(punto)
            print(f"AsignarAlturasUseCase: punto {i} actualizado → {punto}")

        self._txt_output.escribir_puntos(puntos, request.nombre_archivo)
        return AsignarAlturasResponse(puntos=puntos)
