from abc import ABC, abstractmethod
from typing import List

from application.gateways.geometry_gateway import AreaGeometrica
from domain.entities.estructura import Estructura
from domain.entities.poligonos import Poligonos
from domain.entities.punto import Punto
from domain.entities.relacion import Relacion


class KmlOutputPort(ABC):
    """
    Puerto de salida para archivos KML.

    Pertenece a la capa de Aplicación. La implementación concreta
    reside en la capa de Infraestructura.
    """

    @abstractmethod
    def escribir_rutas(
        self,
        relaciones: List[Relacion],
        nombre: str,
        altitud_absoluta: bool = True,
    ) -> None:
        """Genera un KML con las rutas (radio-enlaces)."""

    @abstractmethod
    def escribir_puntos(self, puntos: List[Punto], nombre: str) -> None:
        """Genera un KML con los puntos (antenas)."""

    @abstractmethod
    def escribir_estructura_puntos(
        self,
        matriz_de_puntos: List[List[Punto]],
        nombre: str,
        forma: str = "arrow",
    ) -> None:
        """Genera un KML con los puntos de la grilla de la Estructura."""

    @abstractmethod
    def escribir_malla_cobertura(
        self,
        estructura: Estructura,
        nombre: str,
    ) -> None:
        """Genera un KML con la malla de cobertura de la Estructura."""

    @abstractmethod
    def escribir_poligonos(
        self,
        poligonos: Poligonos,
        estructura: Estructura,
        nombre: str,
    ) -> None:
        """Genera un KML con los polígonos de cobertura."""

    @abstractmethod
    def escribir_area(self, area: AreaGeometrica, nombre: str) -> None:
        """Genera un KML a partir de un AreaGeometrica."""


class TxtOutputPort(ABC):
    """
    Puerto de salida para archivos de texto plano.

    Pertenece a la capa de Aplicación.
    """

    @abstractmethod
    def escribir_puntos(self, puntos: List[Punto], nombre: str) -> None:
        """Persiste una lista de Punto en formato CSV con ';'."""

