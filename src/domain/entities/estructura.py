import math
from typing import List

from domain.entities.punto import Punto


class Estructura:
    """
    Entidad que representa la grilla polar usada para el análisis de cobertura.

    Almacena tres matrices paralelas de igual tamaño (n × m):
      - estructura_linea_de_vista : puntos sobre los que se evalúa LOS.
      - estructura_figuras_geome  : vértices de los polígonos generados.
      - estructura_matricial      : matriz de enteros que codifica el estado LOS:
            0 = sin línea de vista
            1 = con línea de vista
            2 = primera detección de grupo de 1s
            3 = segunda detección (contorno trazado)
            4 = primera detección de 0s (robot)
            5 = segunda detección de 0s

    Pertenece a la capa de Dominio.
    """

    def __init__(
        self,
        n: int,
        m: int,
        r: float,
        punto_cero: Punto,
        altura_torre_fantasma: float,
    ) -> None:
        self.n = n                          # número de direcciones (lados)
        self.m = m                          # número de muestras por dirección
        self.r = r                          # radio en grados
        self.punto_cero = punto_cero
        self.altura_torre_fantasma = altura_torre_fantasma

        self.a = r / (self.m - 1)
        self.alfa = math.pi * 2 / self.n
        self.teta = self.alfa / 2
        self.b = self.a * (1 / math.cos(self.teta))

        self.estructura_linea_de_vista: List[List[Punto]] = []
        self.estructura_figuras_geome: List[List[Punto]] = []
        self.estructura_matricial: List[List[int]] = []

        self._inicializa_puntos_linea_de_vista()
        self._inicializa_puntos_poligonos()
        self._inicializa_matriz()

    # ------------------------------------------------------------------ init

    def _inicializa_matriz(self) -> None:
        for _ in range(self.n):
            self.estructura_matricial.append([1] * self.m)

    def _inicializa_puntos_linea_de_vista(self) -> None:
        angulo = 0.0
        for _ in range(self.n):
            fila: List[Punto] = []
            for j in range(self.m):
                x = self.punto_cero.longitud + math.cos(angulo) * self.a * j
                y = self.punto_cero.latitud + math.sin(angulo) * self.a * j
                fila.append(Punto("", 0, x, y, 0, "", 0))
            self.estructura_linea_de_vista.append(fila)
            angulo += self.alfa

    def _inicializa_puntos_poligonos(self) -> None:
        angulo = -self.teta
        for _ in range(self.n):
            fila: List[Punto] = []
            for j in range(self.m):
                x = self.punto_cero.longitud + math.cos(angulo) * self.b * (j + 0.5)
                y = self.punto_cero.latitud + math.sin(angulo) * self.b * (j + 0.5)
                fila.append(Punto("", 0, x, y, 0, "", 0))
            self.estructura_figuras_geome.append(fila)
            angulo += self.alfa
