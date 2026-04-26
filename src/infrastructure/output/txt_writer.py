from typing import List

from domain.entities.punto import Punto
from domain.entities.relacion import Relacion
from application.ports.output_port import TxtOutputPort


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
    # TODO elmina esto, ya fue reemplazado
    def escribir_relaciones(self, relaciones: List[Relacion], nombre: str) -> None:
        ruta = self._directorio + nombre + ".txt"
        with open(ruta, "w", encoding="utf-8") as f:
            for r in relaciones:
                pi = r.punto_inicial
                pf = r.punto_final
                f.write(
                    f"{pi.nombre};{pi.ubigeo};{pi.longitud};{pi.latitud};"
                    f"{pi.altura_antena};{pi.tipo};{pi.metros_sobre_nivel_mar};"
                    f"{pf.nombre};{pf.ubigeo};{pf.longitud};{pf.latitud};"
                    f"{pf.altura_antena};{pf.tipo};{pf.metros_sobre_nivel_mar};"
                    f"{r.distancia}\n"
                )
