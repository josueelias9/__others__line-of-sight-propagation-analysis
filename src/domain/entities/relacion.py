import math

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

    def __str__(self) -> str:
        return (
            f"{self.punto_inicial.nombre}\t"
            f"{self.punto_final.nombre}\t"
            f"{self.distancia}"
        )
