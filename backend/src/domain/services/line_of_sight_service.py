import math
from typing import List

from domain.entities.punto import Punto
from domain.entities.relacion import Relacion


class LineOfSightService:
    """
    Servicio de dominio para cálculos de Línea de Vista (LDV / LOS).

    Todos los métodos son stateless. Reciben los puntos de elevación ya
    obtenidos (sin depender de ningún repositorio externo).

    Pertenece a la capa de Dominio.
    """

    @staticmethod
    def calcular_fresnel(
        punto_inicial: Punto,
        punto_final: Punto,
        punto_intermedio: Punto,
    ) -> float:
        """
        Calcula el radio de la primera zona de Fresnel en el punto intermedio.
        Devuelve el radio en metros.
        """
        d1 = Relacion(punto_inicial, punto_intermedio).distancia * 1000  # m
        d2 = Relacion(punto_intermedio, punto_final).distancia * 1000    # m
        lambd = 3e8 / 3e9  # velocidad de la luz / frecuencia (3 GHz)
        return math.sqrt((lambd * d1 * d2) / (d1 + d2))

    @staticmethod
    def verificar_linea_de_vista(
        puntos_elevacion: List[Punto],
        punto_inicial: Punto,
        punto_final: Punto,
    ) -> bool:
        """
        Verifica si existe línea de vista entre punto_inicial y punto_final
        considerando el 60 % de la primera zona de Fresnel como margen.

        puntos_elevacion debe ser la lista de puntos interpolados con sus
        alturas ya asignadas en metros_sobre_nivel_mar.
        """
        if len(puntos_elevacion) < 2:
            return True

        y_0 = punto_inicial.metros_sobre_nivel_mar + punto_inicial.altura_antena
        x_0 = 0.0
        y_f = punto_final.metros_sobre_nivel_mar + punto_final.altura_antena
        x_f = float(len(puntos_elevacion) - 1)

        for i in range(1, len(puntos_elevacion) - 1):
            x_i = float(i)
            y_linea = ((y_f - y_0) / (x_f - x_0)) * (x_i - x_0) + y_0
            radio_fresnel = LineOfSightService.calcular_fresnel(
                punto_inicial, punto_final, puntos_elevacion[i]
            )
            if (
                y_linea - 0.6 * radio_fresnel
                <= puntos_elevacion[i].metros_sobre_nivel_mar
            ):
                return False
        return True

    @staticmethod
    def encontrar_menor_distancia(relaciones: List[Relacion]) -> Relacion:
        """Devuelve la Relacion con menor distancia de la lista."""
        return min(relaciones, key=lambda r: r.distancia)

    @staticmethod
    def generar_linea_recta(
        puntos_elevacion: List[Punto],
        punto_inicial: Punto,
        punto_final: Punto,
    ) -> List[Relacion]:
        """
        Genera la línea recta de vista como lista de Relaciones,
        sobreescribiendo la elevación de los puntos intermedios con
        la altura interpolada de la línea.
        """
        if not puntos_elevacion:
            return []

        y_0 = punto_inicial.metros_sobre_nivel_mar + punto_inicial.altura_antena
        y_f = punto_final.metros_sobre_nivel_mar + punto_final.altura_antena
        x_f = float(len(puntos_elevacion) - 1)

        for i, pt in enumerate(puntos_elevacion):
            pt.metros_sobre_nivel_mar = (y_f - y_0) / x_f * i + y_0

        return [
            Relacion(puntos_elevacion[i - 1], puntos_elevacion[i])
            for i in range(1, len(puntos_elevacion))
        ]

    @staticmethod
    def generar_perfil_fresnel(
        puntos_elevacion: List[Punto],
        punto_inicial: Punto,
        punto_final: Punto,
    ) -> List[Relacion]:
        """
        Genera el perfil de la zona de Fresnel como lista de Relaciones,
        sobreescribiendo la elevación de los puntos intermedios con
        (altura_linea - radio_fresnel).
        """
        if not puntos_elevacion:
            return []

        y_0 = punto_inicial.metros_sobre_nivel_mar + punto_inicial.altura_antena
        y_f = punto_final.metros_sobre_nivel_mar + punto_final.altura_antena
        x_f = float(len(puntos_elevacion) - 1)

        for i, pt in enumerate(puntos_elevacion):
            y_linea = (y_f - y_0) / x_f * i + y_0
            radio = LineOfSightService.calcular_fresnel(
                punto_inicial, punto_final, pt
            )
            pt.metros_sobre_nivel_mar = y_linea - radio

        return [
            Relacion(puntos_elevacion[i - 1], puntos_elevacion[i])
            for i in range(1, len(puntos_elevacion))
        ]
