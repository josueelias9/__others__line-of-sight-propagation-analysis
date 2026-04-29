from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class CoberturaGuardada:
    """
    DTO que representa una cobertura persistida.

    Pertenece a la capa de Aplicación.
    """
    id: int
    punto_ubigeo: int
    punto_nombre: str
    geojson: Dict[str, Any]


class CoberturaGuardadaGateway(ABC):
    """
    Puerto para persistir y recuperar coberturas generadas.

    Pertenece a la capa de Aplicación.
    La implementación concreta reside en la capa de Infraestructura.
    """

    @abstractmethod
    def guardar(self, punto_ubigeo: int, geojson: Dict[str, Any]) -> int:
        """Persiste el geojson de cobertura y devuelve el id generado."""

    @abstractmethod
    def listar(self) -> List[CoberturaGuardada]:
        """Devuelve todas las coberturas guardadas."""

    @abstractmethod
    def eliminar(self, id: int) -> None:
        """Elimina una cobertura por id. Lanza ValueError si no existe."""
