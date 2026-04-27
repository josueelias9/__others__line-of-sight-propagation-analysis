from shapely.geometry import mapping
from shapely.geometry.polygon import Polygon

from application.gateways.geometry_gateway import AreaGeometrica, GeometryGateway
from domain.entities.estructura import Estructura
from domain.entities.poligonos import Poligonos


class ShapelyGeometryRepository(GeometryGateway):
    """
    Implementación de GeometryGateway usando la librería Shapely.

    Pertenece a la capa de Infraestructura.
    """

    def poligonos_a_area(
        self,
        poligonos: Poligonos,
        estructura: Estructura,
    ) -> AreaGeometrica:
        resultado = Polygon()
        for poligonito in poligonos.lista_de_poligonitos:
            coords = estructura.coordenadas_poligonito(poligonito)
            resultado = resultado.union(Polygon(coords))
        return self._shapely_a_area(resultado)

    def intersectar(
        self,
        a1: AreaGeometrica,
        a2: AreaGeometrica,
    ) -> AreaGeometrica:
        s1 = self._area_a_shapely(a1)
        s2 = self._area_a_shapely(a2)
        return self._shapely_a_area(s1.intersection(s2))

    # ------------------------------------------------------------------ helpers

    @staticmethod
    def _area_a_shapely(area: AreaGeometrica) -> Polygon:
        if area.vacia:
            return Polygon()
        # Toma el primer polígono (anillo exterior + agujeros)
        if len(area.anillos) == 1:
            outer = area.anillos[0][0]
            holes = area.anillos[0][1:]
            return Polygon(outer, holes)
        # Multi-polígono: unión de todos
        resultado = Polygon()
        for poligono in area.anillos:
            outer = poligono[0]
            holes = poligono[1:]
            resultado = resultado.union(Polygon(outer, holes))
        return resultado

    @staticmethod
    def _shapely_a_area(geom) -> AreaGeometrica:
        if geom is None or geom.is_empty:
            return AreaGeometrica()
        wkt_dict = mapping(geom)
        tipo = wkt_dict.get("type", "")
        coords = wkt_dict.get("coordinates", [])

        if tipo == "Polygon":
            anillos = [[[tuple(p) for p in ring] for ring in coords]]
            return AreaGeometrica(anillos=anillos)
        if tipo == "MultiPolygon":
            anillos = [[[tuple(p) for p in ring] for ring in poly] for poly in coords]
            return AreaGeometrica(anillos=anillos)
        return AreaGeometrica()
