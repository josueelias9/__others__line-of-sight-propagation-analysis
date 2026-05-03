from typing import List

from domain.entities.punto import Punto
from domain.entities.relacion import Relacion
from application.interface.ports.output import TxtOutputPort


class TxtWriter(TxtOutputPort):
    """
    Adaptador de infraestructura para escritura de archivos de texto plano.

    Implementa TxtOutputPort.
    Pertenece a la capa de Infraestructura.
    """

    def __init__(self, directorio: str) -> None:
        self._directorio = directorio

    # ------------------------------------------------------------------ TxtOutputPort

    def escribir_puntos(self, puntos: List[Punto], nombre: str) -> None:
        ruta = self._directorio + nombre + ".txt"
        with open(ruta, "w", encoding="utf-8") as f:
            for p in puntos:
                f.write(
                    f"{p.nombre};{p.ubigeo};{p.longitud};{p.latitud};"
                    f"{p.altura_antena};{p.tipo};{p.metros_sobre_nivel_mar};"
                    f"{p.green_asociado}\n"
                )
