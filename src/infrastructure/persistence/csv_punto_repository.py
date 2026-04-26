import csv
from typing import List

from domain.entities.punto import Punto
from domain.entities.relacion import Relacion
from application.gateways.punto_gateway import PuntoGateway


class CsvPuntoRepository(PuntoGateway):
    """
    Adaptador de infraestructura que implementa PuntoGateway
    leyendo archivos CSV con cabecera.

    Formato esperado (8 columnas):
        nombre,ubigeo,longitud,latitud,altura_antena,tipo,metros_sobre_nivel_mar,green_asociado

    Pertenece a la capa de Infraestructura.
    """

    def __init__(self, directorio: str) -> None:
        # directorio debe terminar con '/'
        self._directorio = directorio

    # ------------------------------------------------------------------ PuntoGateway

    def leer_puntos(self, nombre_archivo: str) -> List[Punto]:
        puntos: List[Punto] = []
        ruta = self._directorio + nombre_archivo + ".csv"
        with open(ruta, encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for numero_linea, fila in enumerate(reader, start=2):
                try:
                    punto = Punto(
                        nombre=fila["nombre"],
                        ubigeo=int(fila["ubigeo"]),
                        longitud=float(fila["longitud"]),
                        latitud=float(fila["latitud"]),
                        altura_antena=float(fila["altura_antena"]),
                        tipo=fila["tipo"],
                        metros_sobre_nivel_mar=float(fila["metros_sobre_nivel_mar"]),
                    )
                    punto.green_asociado = fila.get("green_asociado", "").strip()
                    puntos.append(punto)
                except (KeyError, ValueError) as exc:
                    print(
                        f"CsvPuntoRepository: línea {numero_linea} ignorada ({exc})."
                    )
        return puntos

    def leer_relaciones(self, nombre_archivo: str) -> List[Relacion]:
        raise NotImplementedError(
            "CsvPuntoRepository: leer_relaciones no está implementado para el formato CSV."
        )

    def guardar_puntos(self, puntos: List[Punto], nombre_archivo: str) -> None:
        ruta = self._directorio + nombre_archivo + ".csv"
        _CAMPOS = [
            "nombre", "ubigeo", "longitud", "latitud",
            "altura_antena", "tipo", "metros_sobre_nivel_mar", "green_asociado",
        ]
        with open(ruta, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=_CAMPOS)
            writer.writeheader()
            for p in puntos:
                writer.writerow({
                    "nombre": p.nombre,
                    "ubigeo": p.ubigeo,
                    "longitud": p.longitud,
                    "latitud": p.latitud,
                    "altura_antena": p.altura_antena,
                    "tipo": p.tipo,
                    "metros_sobre_nivel_mar": p.metros_sobre_nivel_mar,
                    "green_asociado": p.green_asociado,
                })
