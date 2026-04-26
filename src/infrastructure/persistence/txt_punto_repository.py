from typing import List

from domain.entities.punto import Punto
from domain.entities.relacion import Relacion
from application.gateways.punto_gateway import PuntoGateway


class TxtPuntoRepository(PuntoGateway):
    """
    Adaptador de infraestructura que implementa PuntoGateway
    leyendo archivos de texto plano con campos separados por ';'.

    Formato de línea para puntos (7 campos):
        nombre;ubigeo;longitud;latitud;altura_antena;tipo;metros_sobre_nivel_mar

    Formato de línea para relaciones (14 campos + distancia):
        nombre1;ubi1;lon1;lat1;h1;tipo1;msnm1;
        nombre2;ubi2;lon2;lat2;h2;tipo2;msnm2;distancia

    Pertenece a la capa de Infraestructura.
    """

    def __init__(self, directorio: str) -> None:
        # directorio debe terminar con '/'
        self._directorio = directorio

    # ------------------------------------------------------------------ PuntoGateway

    def leer_puntos(self, nombre_archivo: str) -> List[Punto]:
        puntos: List[Punto] = []
        ruta = self._directorio + nombre_archivo + ".txt"
        with open(ruta, encoding="utf-8") as f:
            for numero_linea, linea in enumerate(f, start=1):
                linea = linea.strip()
                if not linea:
                    continue
                campos = linea.split(";")
                if len(campos) < 7:
                    print(
                        f"TxtPuntoRepository: línea {numero_linea} ignorada "
                        f"(solo {len(campos)} campos)."
                    )
                    continue
                puntos.append(
                    Punto(
                        nombre=campos[0],
                        ubigeo=int(campos[1]),
                        longitud=float(campos[2]),
                        latitud=float(campos[3]),
                        altura_antena=float(campos[4]),
                        tipo=campos[5],
                        metros_sobre_nivel_mar=float(campos[6]),
                    )
                )
        return puntos

    def leer_relaciones(self, nombre_archivo: str) -> List[Relacion]:
        relaciones: List[Relacion] = []
        ruta = self._directorio + nombre_archivo + ".txt"
        with open(ruta, encoding="utf-8") as f:
            for numero_linea, linea in enumerate(f, start=1):
                linea = linea.strip()
                if not linea:
                    continue
                c = linea.split(";")
                if len(c) < 14:
                    print(
                        f"TxtPuntoRepository: línea {numero_linea} ignorada "
                        f"(solo {len(c)} campos para relación)."
                    )
                    continue
                p1 = Punto(c[0], int(c[1]), float(c[2]), float(c[3]), float(c[4]), c[5], float(c[6]))
                p2 = Punto(c[7], int(c[8]), float(c[9]), float(c[10]), float(c[11]), c[12], float(c[13]))
                relaciones.append(Relacion(p1, p2))
        return relaciones
