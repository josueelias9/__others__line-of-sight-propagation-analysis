import logging
from dataclasses import dataclass
from typing import List

from domain.entities.punto import Punto
from application.gateways.elevation_gateway import ElevationGateway
from application.gateways.punto_gateway import PuntoGateway

logger = logging.getLogger(__name__)




@dataclass
class AsignarAlturasResponse:
    puntos: List[Punto]


class AsignarAlturasUseCase:
    """
    Caso de uso: asignar la altura sobre el nivel del mar a una lista de puntos.

    1. Lee los puntos desde el gateway.
    2. Para cada punto consulta la elevación al gateway de elevación.
    3. Sobreescribe el mismo archivo de entrada con los datos actualizados.

    Pertenece a la capa de Aplicación.
    """

    def __init__(
        self,
        punto_repo: PuntoGateway,
        elevation_repo: ElevationGateway,
    ) -> None:
        self._punto_repo = punto_repo
        self._elevation_repo = elevation_repo

    def ejecutar(self) -> AsignarAlturasResponse:
        """
        Lee los puntos de `punto.csv`, asigna alturas y
        sobreescribe el mismo archivo de entrada con los valores actualizados.
        """
        logger.info("🟢")
        puntos = self._punto_repo.leer_puntos()
        for i, punto in enumerate(puntos):
            self._elevation_repo.obtener_elevacion_punto(punto)
            logger.debug("punto %d actualizado → %s", i, punto)

        self._punto_repo.guardar_puntos(puntos)
        logger.info("🔴")
        return AsignarAlturasResponse(puntos=puntos)
