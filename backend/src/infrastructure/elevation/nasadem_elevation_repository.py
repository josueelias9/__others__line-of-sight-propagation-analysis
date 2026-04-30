import logging
import math
from functools import lru_cache
from typing import List, Tuple

import numpy as np
from NASADEM import NASADEMConnection
from rasters import MultiPoint, Point

from domain.entities.punto import Punto
from application.interface.ports.elevation import ElevationGateway

logger = logging.getLogger(__name__)

# Instancia global de la conexión (se crea una sola vez al importar el módulo).
# Los tiles descargados se persisten en download_directory, por lo que solo
# se descargan una vez por tile (cache en disco gestionado por la librería).
_connection = NASADEMConnection()


@lru_cache(maxsize=8192)
def _get_elevation(lat: float, lon: float) -> float:
    """Obtiene la elevación en metros para un punto lat/lon. Devuelve 0.0 si no hay dato.
    Usa lru_cache para evitar re-consultas de coordenadas ya procesadas."""
    try:
        value = _connection.elevation_m(Point(lon, lat))
        if value is None or (isinstance(value, float) and math.isnan(value)):
            return 0.0
        return float(value)
    except Exception as exc:
        logger.warning("No se pudo obtener elevación para (%.6f, %.6f): %s", lat, lon, exc)
        return 0.0


def _get_elevations_batch(lats: List[float], lons: List[float]) -> List[float]:
    """Consulta elevaciones para múltiples coordenadas en una sola llamada.
    La librería agrupa los puntos por tile y carga cada tile una sola vez,
    evitando abrir el mismo archivo zip repetidamente.
    Recae en _get_elevation individual si el batch falla."""
    try:
        multi = MultiPoint(x=lons, y=lats)
        raw = _connection.elevation_m(multi)
        results: List[float] = []
        for v in raw:
            if v is None or (isinstance(v, float) and math.isnan(float(v))):
                results.append(0.0)
            else:
                results.append(float(v))
        return results
    except Exception as exc:
        logger.warning("Error en consulta batch de elevaciones (%s). Usando consulta individual.", exc)
        return [_get_elevation(lat, lon) for lat, lon in zip(lats, lons)]


class NasademElevationRepository(ElevationGateway):
    """
    Adaptador de infraestructura que implementa ElevationGateway
    usando la librería NASADEM (NASA DEM) para obtener datos de elevación del terreno.

    Pertenece a la capa de Infraestructura.
    """

    def __init__(self, muestras: int) -> None:
        self._muestras = muestras

    # ------------------------------------------------------------------ ElevationGateway

    def obtener_perfil_de_puntos(
        self,
        punto_inicial: Punto,
        punto_final: Punto,
        muestras: int,
    ) -> Tuple[List[Punto], str]:
        """Interpola `muestras` puntos entre punto_inicial y punto_final.
        Genera todas las coordenadas primero y consulta las elevaciones en lote
        para que la librería cargue cada tile una sola vez."""
        lat_0, lon_0 = punto_inicial.latitud, punto_inicial.longitud
        lat_f, lon_f = punto_final.latitud, punto_final.longitud
        delta_lon = lon_f - lon_0
        delta_lat = lat_f - lat_0

        lats: List[float] = []
        lons: List[float] = []

        if delta_lon == 0:
            factor = delta_lat / (muestras - 1)
            pendiente = delta_lon / delta_lat if delta_lat != 0 else 0
            for i in range(muestras):
                lat_i = factor * i + lat_0
                lon_i = pendiente * (lat_i - lat_0) + lon_0
                lats.append(lat_i)
                lons.append(lon_i)
        else:
            factor = delta_lon / (muestras - 1)
            pendiente = delta_lat / delta_lon
            for i in range(muestras):
                lon_i = factor * i + lon_0
                lat_i = pendiente * (lon_i - lon_0) + lat_0
                lats.append(lat_i)
                lons.append(lon_i)

        alturas = _get_elevations_batch(lats, lons)

        puntos: List[Punto] = []
        altura_aux = 0.0
        for lat_i, lon_i, altura in zip(lats, lons, alturas):
            if altura == 0.0:
                altura = altura_aux
            else:
                altura_aux = altura
            puntos.append(Punto("", 0, lon_i, lat_i, 0, "", float(altura)))

        return puntos, "puntos"

    def obtener_perfil_de_alturas(
        self,
        punto_inicial: Punto,
        punto_final: Punto,
        muestras: int,
    ) -> Tuple[List[float], str]:
        """Interpola `muestras` alturas entre punto_inicial y punto_final.
        Usa consulta batch para cargar cada tile una sola vez."""
        lat_0, lon_0 = punto_inicial.latitud, punto_inicial.longitud
        lat_f, lon_f = punto_final.latitud, punto_final.longitud
        delta_lon = lon_f - lon_0
        delta_lat = lat_f - lat_0

        lats: List[float] = []
        lons: List[float] = []

        if delta_lon == 0:
            factor = delta_lat / (muestras - 1)
            pendiente = delta_lon / delta_lat if delta_lat != 0 else 0
            for i in range(muestras):
                lat_i = factor * i + lat_0
                lon_i = pendiente * (lat_i - lat_0) + lon_0
                lats.append(lat_i)
                lons.append(lon_i)
        else:
            factor = delta_lon / (muestras - 1)
            pendiente = delta_lat / delta_lon
            for i in range(muestras):
                lon_i = factor * i + lon_0
                lat_i = pendiente * (lon_i - lon_0) + lat_0
                lats.append(lat_i)
                lons.append(lon_i)

        raw_alturas = _get_elevations_batch(lats, lons)

        alturas: List[float] = []
        altura_aux = 0.0
        for altura in raw_alturas:
            if altura == 0.0:
                altura = altura_aux
            else:
                altura_aux = altura
            alturas.append(float(altura))

        return alturas, "alturas"

    def obtener_elevacion_punto(self, punto: Punto) -> None:
        """Asigna la elevación NASADEM al atributo metros_sobre_nivel_mar del punto."""
        altura = _get_elevation(punto.latitud, punto.longitud)
        if altura == 0.0:
            punto.metros_sobre_nivel_mar = 0.0
            logger.warning("altura 0 para '%s', se asigna 0.", punto.nombre)
        else:
            punto.metros_sobre_nivel_mar = float(altura)
