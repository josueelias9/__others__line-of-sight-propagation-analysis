import math
from typing import List

from domain.entities.punto import Punto


class Relacion:
    """
    Entidad que representa un radio-enlace entre dos puntos geográficos.

    Calcula automáticamente la distancia en kilómetros al ser creada.
    Pertenece a la capa de Dominio. No depende de ninguna capa exterior.
    """

    def __init__(self, punto_inicial: Punto, punto_final: Punto) -> None:
        self.punto_inicial = punto_inicial
        self.punto_final = punto_final
        self.distancia: float = self._calcular_distancia()

    def _calcular_distancia(self) -> float:
        """Calcula la distancia en kilómetros entre los dos puntos (proyección plana)."""
        y_0 = self.punto_inicial.longitud * 111.11
        x_0 = self.punto_inicial.latitud * 111.11
        y_f = self.punto_final.longitud * 111.11
        x_f = self.punto_final.latitud * 111.11
        return math.sqrt((y_f - y_0) ** 2 + (x_f - x_0) ** 2)

    # ------------------------------------------------------------------ LOS

    def calcular_fresnel(self, punto_intermedio: Punto) -> float:
        """
        Calcula el radio de la primera zona de Fresnel en el punto intermedio.
        Devuelve el radio en metros.
        """
        d1 = Relacion(self.punto_inicial, punto_intermedio).distancia * 1000
        d2 = Relacion(punto_intermedio, self.punto_final).distancia * 1000
        lambd = 3e8 / 3e9  # velocidad de la luz / frecuencia (3 GHz)
        return math.sqrt((lambd * d1 * d2) / (d1 + d2))

    def verificar_linea_de_vista(self, puntos_elevacion: List[Punto]) -> bool:
        """
        Verifica si existe línea de vista considerando el 60 % de la primera
        zona de Fresnel como margen.

        puntos_elevacion debe ser la lista de puntos interpolados con sus
        alturas ya asignadas en metros_sobre_nivel_mar.
        """
        if len(puntos_elevacion) < 2:
            return True

        y_0 = (
            self.punto_inicial.metros_sobre_nivel_mar + self.punto_inicial.altura_antena
        )
        x_0 = 0.0
        y_f = self.punto_final.metros_sobre_nivel_mar + self.punto_final.altura_antena
        x_f = float(len(puntos_elevacion) - 1)

        for i in range(1, len(puntos_elevacion) - 1):
            x_i = float(i)
            y_linea = ((y_f - y_0) / (x_f - x_0)) * (x_i - x_0) + y_0
            radio_fresnel = self.calcular_fresnel(puntos_elevacion[i])
            if (
                y_linea - 0.6 * radio_fresnel
                <= puntos_elevacion[i].metros_sobre_nivel_mar
            ):
                return False
        return True

    def generar_linea_recta(self, puntos_elevacion: List[Punto]) -> "List[Relacion]":
        """
        Genera la línea recta de vista como lista de Relaciones,
        sobreescribiendo la elevación de los puntos intermedios con
        la altura interpolada de la línea.
        """
        if not puntos_elevacion:
            return []

        y_0 = (
            self.punto_inicial.metros_sobre_nivel_mar + self.punto_inicial.altura_antena
        )
        y_f = self.punto_final.metros_sobre_nivel_mar + self.punto_final.altura_antena
        x_f = float(len(puntos_elevacion) - 1)

        for i, pt in enumerate(puntos_elevacion):
            pt.metros_sobre_nivel_mar = (y_f - y_0) / x_f * i + y_0

        return [
            Relacion(puntos_elevacion[i - 1], puntos_elevacion[i])
            for i in range(1, len(puntos_elevacion))
        ]

    def generar_perfil_fresnel(self, puntos_elevacion: List[Punto]) -> "List[Relacion]":
        """
        Genera el perfil de la zona de Fresnel como lista de Relaciones,
        sobreescribiendo la elevación de los puntos intermedios con
        (altura_linea - radio_fresnel).
        """
        if not puntos_elevacion:
            return []

        y_0 = (
            self.punto_inicial.metros_sobre_nivel_mar + self.punto_inicial.altura_antena
        )
        y_f = self.punto_final.metros_sobre_nivel_mar + self.punto_final.altura_antena
        x_f = float(len(puntos_elevacion) - 1)

        for i, pt in enumerate(puntos_elevacion):
            y_linea = (y_f - y_0) / x_f * i + y_0
            radio = self.calcular_fresnel(pt)
            pt.metros_sobre_nivel_mar = y_linea - radio

        return [
            Relacion(puntos_elevacion[i - 1], puntos_elevacion[i])
            for i in range(1, len(puntos_elevacion))
        ]

    @staticmethod
    def encontrar_menor_distancia(relaciones: "List[Relacion]") -> "Relacion":
        """Devuelve la Relacion con menor distancia de la lista."""
        return min(relaciones, key=lambda r: r.distancia)

    # ------------------------------------------------------------------ repr

    def __str__(self) -> str:
        return (
            f"{self.punto_inicial.nombre}\t"
            f"{self.punto_final.nombre}\t"
            f"{self.distancia}"
        )
