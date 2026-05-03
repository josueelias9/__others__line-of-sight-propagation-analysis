from shapely.geometry import LineString, MultiLineString, mapping, MultiPolygon
from shapely.geometry.polygon import Polygon
from shapely.ops import unary_union

from application.interface.ports.geometry import AreaGeometrica, GeometryGateway
from domain.entities.estructura import Estructura
from domain.entities.relacion import Relacion

from typing import Any


class ShapelyGeometryRepository(GeometryGateway):
    """
    Implementación de GeometryGateway usando la librería Shapely.

    Pertenece a la capa de Infraestructura.
    """

    def estructura_a_area(self, estructura: Estructura) -> AreaGeometrica:
        return self._shapely_a_area(self._estructura_a_shapely(estructura))

    def estructura_a_geojson(self, estructura: Estructura) -> dict[str, Any]:
        geom = self._estructura_a_shapely(estructura)
        if geom.is_empty:
            return {"type": "Feature", "geometry": None, "properties": {}}
        epsilon = estructura.r / estructura.m
        geom = geom.buffer(-epsilon, resolution=32).buffer(epsilon, resolution=32)
        return {"type": "Feature", "geometry": mapping(geom), "properties": {}}

    def estructura_a_malla_geojson(self, estructura: Estructura) -> dict[str, Any]:
        polygons = self._lista_de_poligonos(estructura)
        if not polygons:
            return {"type": "Feature", "geometry": None, "properties": {}}
        multipoly = MultiPolygon(polygons)
        return {"type": "Feature", "geometry": mapping(multipoly), "properties": {}}

    def intersectar(
        self,
        a1: AreaGeometrica,
        a2: AreaGeometrica,
    ) -> AreaGeometrica:
        s1 = self._area_a_shapely(a1)
        s2 = self._area_a_shapely(a2)
        return self._shapely_a_area(s1.intersection(s2))

    def relaciones_a_geojson(self, relaciones: list[Relacion]) -> dict[str, Any]:
        """
        Convierte una lista de Relacion en un GeoJSON MultiLineString con altitudes.

        Cada coordenada incluye la altura absoluta (msnm + altura_antena) como
        tercer componente: [longitud, latitud, altitud_m].

        Pertenece a la capa de Infraestructura.
        """
        lines = [
            LineString(
                [
                    (
                        r.punto_inicial.longitud,
                        r.punto_inicial.latitud,
                        r.punto_inicial.metros_sobre_nivel_mar
                        + r.punto_inicial.altura_antena,
                    ),
                    (
                        r.punto_final.longitud,
                        r.punto_final.latitud,
                        r.punto_final.metros_sobre_nivel_mar
                        + r.punto_final.altura_antena,
                    ),
                ]
            )
            for r in relaciones
        ]
        if lines:
            return dict(mapping(MultiLineString(lines)))
        return {"type": "MultiLineString", "coordinates": []}

    # ------------------------------------------------------------------ helpers

    @staticmethod
    def _lista_de_poligonos(estructura: Estructura) -> list[Polygon]:
        """
        Convierte una Estructura en una lista de objetos Polygon de Shapely.

        Pertenece a la capa de Infraestructura.
        """
        fg = estructura.estructura_figuras_geome
        ultimo_i = len(fg) - 1
        polygons = []
        for i in range(estructura.n):
            for j in range(1, estructura.m):
                if estructura.estructura_matricial[i][j] != 1:
                    continue
                next_i = 0 if i == ultimo_i else i + 1
                p00, p0m = fg[i][j], fg[i][j - 1]
                ppm, pp0 = fg[next_i][j - 1], fg[next_i][j]
                polygons.append(
                    Polygon(
                        [
                            (p00.longitud, p00.latitud),
                            (p0m.longitud, p0m.latitud),
                            (ppm.longitud, ppm.latitud),
                            (pp0.longitud, pp0.latitud),
                        ]
                    )
                )
        return polygons

    @staticmethod
    def _estructura_a_shapely(estructura: Estructura) -> Polygon:
        polygons = ShapelyGeometryRepository._lista_de_poligonos(estructura)
        if not polygons:
            return Polygon()
        return unary_union(polygons).buffer(0)

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
