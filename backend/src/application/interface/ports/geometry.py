from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple

from domain.entities.estructura import Estructura
from domain.entities.poligonos import Poligonos
from domain.entities.relacion import Relacion


@dataclass
class AreaGeometrica:
    """
    DTO que representa un área geométrica resultado de operaciones sobre coberturas.

    Cada elemento de `anillos` es un polígono compuesto por:
      - anillos[i][0] → coordenadas del contorno exterior
      - anillos[i][1:] → coordenadas de agujeros interiores (si los hay)

    Pertenece a la capa de Aplicación.
    """

    anillos: List[List[List[Tuple[float, float]]]] = field(default_factory=list)

    @property
    def vacia(self) -> bool:
        return not self.anillos


class GeometryGateway(ABC):
    """
    Puerto para operaciones geométricas sobre polígonos de cobertura.

    Pertenece a la capa de Aplicación.
    La implementación concreta reside en la capa de Infraestructura.
    """

    @abstractmethod
    def estructura_a_area(self, estructura: Estructura) -> AreaGeometrica:
        """Une las celdas con LOS=1 en un AreaGeometrica (unary_union)."""

    @abstractmethod
    def estructura_a_geojson(self, estructura: Estructura) -> dict:
        """Une las celdas con LOS=1 y devuelve un Feature GeoJSON (EPSG:4326)."""

    @abstractmethod
    def estructura_a_malla_geojson(self, estructura: Estructura) -> dict:
        """Devuelve un FeatureCollection GeoJSON con cada celda visible (LOS=1) como Feature."""

    @abstractmethod
    def intersectar(
        self,
        a1: AreaGeometrica,
        a2: AreaGeometrica,
    ) -> AreaGeometrica:
        """Intersecta dos áreas geométricas. Devuelve AreaGeometrica vacía si no se superponen."""

    @abstractmethod
    def relaciones_a_geojson(self, relaciones: List[Relacion]) -> Dict[str, Any]:
        """"""
