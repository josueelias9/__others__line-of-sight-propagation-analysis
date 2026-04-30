from abc import ABC, abstractmethod
from typing import List

from domain.entities.red import Red


class RedGateway(ABC):
    """
    Gateway para la persistencia de redes.

    Pertenece a la capa de Aplicación. La implementación concreta
    reside en la capa de Infraestructura.
    """

    @abstractmethod
    def guardar_red(self, red: Red) -> Red:
        """Persiste la Red junto con sus nodos en red_punto.
        Devuelve la misma instancia con el id asignado."""

    @abstractmethod
    def listar_redes(self) -> List[Red]:
        """Devuelve todas las redes con sus nodos (ubigeo + conectado)."""

    @abstractmethod
    def eliminar_red(self, red_id: int) -> None:
        """Elimina la red con el id dado y sus entradas en red_punto."""
