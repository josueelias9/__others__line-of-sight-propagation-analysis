from abc import ABC, abstractmethod
from typing import List

from domain.entities.punto import Punto
from domain.entities.relacion import Relacion


class PuntoGateway(ABC):
    """
    Gateway para la lectura de puntos y relaciones persistidos.

    Pertenece a la capa de Aplicación. La implementación concreta (archivos .txt)
    reside en la capa de Infraestructura.
    """

    @abstractmethod
    def leer_puntos(self, nombre_archivo: str) -> List[Punto]:
        """Lee y devuelve una lista de Punto desde la fuente de datos."""

    @abstractmethod
    def leer_relaciones(self, nombre_archivo: str) -> List[Relacion]:
        """Lee y devuelve una lista de Relacion desde la fuente de datos."""
