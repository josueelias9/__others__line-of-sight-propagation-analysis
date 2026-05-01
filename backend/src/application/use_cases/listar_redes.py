from dataclasses import dataclass
from typing import List

from application.interface.db.red import RedGateway
from domain.entities.red import Red


@dataclass
class ListarRedesRequest:
    pass


class ListarRedesUseCase:
    """
    Caso de uso: listar todas las redes persistidas con su geojson.

    Pertenece a la capa de Aplicación.
    """

    def __init__(self, red_repo: RedGateway) -> None:
        self._red_repo = red_repo

    def ejecutar(self) -> List[Red]:
        return self._red_repo.listar_redes()
