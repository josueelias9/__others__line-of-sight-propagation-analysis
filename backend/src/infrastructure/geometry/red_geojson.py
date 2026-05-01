from typing import Any, Dict, List

from shapely.geometry import LineString, MultiLineString, mapping


def relaciones_a_geojson(relaciones: List) -> Dict[str, Any]:
    """
    Convierte una lista de Relacion en un GeoJSON MultiLineString con altitudes.

    Cada coordenada incluye la altura absoluta (msnm + altura_antena) como
    tercer componente: [longitud, latitud, altitud_m].

    Pertenece a la capa de Infraestructura.
    """
    lines = [
        LineString([
            (
                r.punto_inicial.longitud,
                r.punto_inicial.latitud,
                r.punto_inicial.metros_sobre_nivel_mar + r.punto_inicial.altura_antena,
            ),
            (
                r.punto_final.longitud,
                r.punto_final.latitud,
                r.punto_final.metros_sobre_nivel_mar + r.punto_final.altura_antena,
            ),
        ])
        for r in relaciones
    ]
    if lines:
        return dict(mapping(MultiLineString(lines)))
    return {"type": "MultiLineString", "coordinates": []}
