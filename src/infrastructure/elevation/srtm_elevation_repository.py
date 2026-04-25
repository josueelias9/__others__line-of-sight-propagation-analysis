from typing import List, Tuple

import srtm

from domain.entities.punto import Punto
from domain.repositories.elevation_repository import ElevationRepository


# Cargado una sola vez al importar el módulo (costoso en tiempo/memoria)
_elevation_data = srtm.get_data()


class SrtmElevationRepository(ElevationRepository):
    """
    Adaptador de infraestructura que implementa ElevationRepository
    usando la librería SRTM para obtener datos de elevación del terreno.

    Pertenece a la capa de Infraestructura.
    """

    def __init__(self, muestras: int) -> None:
        self._muestras = muestras

    # ------------------------------------------------------------------ ElevationRepository

    def obtener_perfil_de_puntos(
        self,
        punto_inicial: Punto,
        punto_final: Punto,
        muestras: int,
    ) -> Tuple[List[Punto], str]:
        """Interpola `muestras` puntos entre punto_inicial y punto_final."""
        puntos: List[Punto] = []
        altura_aux = 0.0

        lat_0, lon_0 = punto_inicial.latitud, punto_inicial.longitud
        lat_f, lon_f = punto_final.latitud, punto_final.longitud
        delta_lon = lon_f - lon_0
        delta_lat = lat_f - lat_0

        if delta_lon == 0:
            factor = delta_lat / (muestras - 1)
            pendiente = delta_lon / delta_lat if delta_lat != 0 else 0
            for i in range(muestras):
                lat_i = factor * i + lat_0
                lon_i = pendiente * (lat_i - lat_0) + lon_0
                altura = _elevation_data.get_elevation(lat_i, lon_i)
                if altura is None:
                    altura = altura_aux
                else:
                    altura_aux = altura
                puntos.append(Punto("", 0, lon_i, lat_i, 0, "", float(altura)))
        else:
            factor = delta_lon / (muestras - 1)
            pendiente = delta_lat / delta_lon
            for i in range(muestras):
                lon_i = factor * i + lon_0
                lat_i = pendiente * (lon_i - lon_0) + lat_0
                altura = _elevation_data.get_elevation(lat_i, lon_i)
                if altura is None:
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
        """Interpola `muestras` alturas entre punto_inicial y punto_final."""
        alturas: List[float] = []
        altura_aux = 0.0

        lat_0, lon_0 = punto_inicial.latitud, punto_inicial.longitud
        lat_f, lon_f = punto_final.latitud, punto_final.longitud
        delta_lon = lon_f - lon_0
        delta_lat = lat_f - lat_0

        if delta_lon == 0:
            factor = delta_lat / (muestras - 1)
            pendiente = delta_lon / delta_lat if delta_lat != 0 else 0
            for i in range(muestras):
                lat_i = factor * i + lat_0
                lon_i = pendiente * (lat_i - lat_0) + lon_0
                altura = _elevation_data.get_elevation(lat_i, lon_i)
                if altura is None:
                    altura = altura_aux
                else:
                    altura_aux = altura
                alturas.append(float(altura))
        else:
            factor = delta_lon / (muestras - 1)
            pendiente = delta_lat / delta_lon
            for i in range(muestras):
                lon_i = factor * i + lon_0
                lat_i = pendiente * (lon_i - lon_0) + lat_0
                altura = _elevation_data.get_elevation(lat_i, lon_i)
                if altura is None:
                    altura = altura_aux
                else:
                    altura_aux = altura
                alturas.append(float(altura))

        return alturas, "alturas"

    def obtener_elevacion_punto(self, punto: Punto) -> None:
        """Asigna la elevación SRTM al atributo metros_sobre_nivel_mar del punto."""
        altura = _elevation_data.get_elevation(punto.latitud, punto.longitud)
        if altura is None:
            punto.metros_sobre_nivel_mar = 0.0
            print(
                f"SrtmElevationRepository: altura None para '{punto.nombre}', "
                "se asigna 0."
            )
        else:
            punto.metros_sobre_nivel_mar = float(altura)
