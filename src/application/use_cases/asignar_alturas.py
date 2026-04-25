from typing import List

from application.ports.output_port import TxtOutputPort
from domain.entities.punto import Punto
from domain.repositories.elevation_repository import ElevationRepository
from domain.repositories.punto_repository import PuntoRepository


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
        punto_repo: PuntoRepository,
        elevation_repo: ElevationRepository,
        txt_output: TxtOutputPort,
    ) -> None:
        self._punto_repo = punto_repo
        self._elevation_repo = elevation_repo
        self._txt_output = txt_output

    def ejecutar(self, nombre_archivo: str) -> List[Punto]:
        """
        Lee los puntos de `nombre_archivo`, asigna alturas y los guarda
        en el mismo nombre de archivo de salida.

        Devuelve la lista de puntos con las alturas asignadas.
        """
        puntos = self._punto_repo.leer_puntos(nombre_archivo)
        for i, punto in enumerate(puntos):
            self._elevation_repo.obtener_elevacion_punto(punto)
            print(f"AsignarAlturasUseCase: punto {i} actualizado → {punto}")

        self._txt_output.escribir_puntos(puntos, nombre_archivo)
        return puntos
