from typing import Any, Dict, List

from shapely.geometry import LineString, MultiLineString, mapping


def relaciones_a_geojson(relaciones: List) -> Dict[str, Any]:
    """
    Convierte una lista de Relacion en un GeoJSON MultiLineString.

    Pertenece a la capa de Infraestructura.
    """
    lines = [
        LineString([
            (r.punto_inicial.longitud, r.punto_inicial.latitud),
            (r.punto_final.longitud, r.punto_final.latitud),
        ])
        for r in relaciones
    ]
    if lines:
        return dict(mapping(MultiLineString(lines)))
    return {"type": "MultiLineString", "coordinates": []}
