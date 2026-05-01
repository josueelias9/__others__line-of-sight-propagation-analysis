from abc import ABC, abstractmethod
from typing import List, Optional

from domain.entities.punto import Punto


class PuntoGateway(ABC):
    """
    Gateway para la lectura y escritura de puntos persistidos.

    Pertenece a la capa de Aplicación. La implementación concreta
    reside en la capa de Infraestructura.
    """

    @abstractmethod
    def leer_puntos(self, tipo: Optional[str] = None) -> List[Punto]:
        """Lee y devuelve una lista de Punto. Si se indica tipo, filtra por ese valor."""

    @abstractmethod
    def obtener_punto_por_ubigeo(self, ubigeo: int) -> Punto:
        """Devuelve el Punto cuyo ubigeo coincide; lanza ValueError si no existe."""

    @abstractmethod
    def guardar_puntos(self, puntos: List[Punto]) -> None:
        """Persiste la lista de Punto (sobreescribe)."""

    @abstractmethod
    def actualizar_conectado(self, puntos: List[Punto]) -> None:
        """Actualiza únicamente el campo `conectado` de los Punto indicados."""

    @abstractmethod
    def agregar_punto(self, punto: Punto) -> Punto:
        """Persiste un nuevo Punto asignándole un ubigeo único y lo devuelve con ese valor."""
