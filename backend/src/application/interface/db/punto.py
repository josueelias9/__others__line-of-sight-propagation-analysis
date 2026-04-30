from abc import ABC, abstractmethod
from typing import List, Optional

from domain.entities.punto import Punto
from domain.entities.relacion import Relacion


class PuntoGateway(ABC):
    """
    Gateway para la lectura y escritura de puntos y relaciones persistidos.

    Pertenece a la capa de Aplicación. La implementación concreta (archivos .txt)
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
        """Persiste la lista de Punto en punto.csv (sobreescribe)."""

    @abstractmethod
    def leer_relaciones(self) -> List[Relacion]:
        """Lee y devuelve una lista de Relacion desde la fuente de datos."""

    @abstractmethod
    def guardar_relaciones(self, relaciones: List[Relacion]) -> None:
        """Persiste la lista de Relacion en relacion.csv (sobreescribe)."""
        """Persiste la lista de Relacion en la fuente de datos (sobreescribe)."""

    @abstractmethod
    def actualizar_conectado(self, puntos: List[Punto]) -> None:
        """Actualiza únicamente el campo `conectado` de los Punto indicados en punto.csv,
        sin modificar los demás campos ni los puntos no presentes en la lista."""

    @abstractmethod
    def agregar_punto(self, punto: Punto) -> Punto:
        """Persiste un nuevo Punto asignándole un ubigeo único y lo devuelve con ese valor."""
