from abc import ABC, abstractmethod
from typing import List, Tuple

from domain.entities.punto import Punto


class ElevationRepository(ABC):
    """
    Puerto (interfaz) para la obtención de datos de elevación del terreno.

    Pertenece a la capa de Dominio. La implementación concreta (SRTM)
    reside en la capa de Infraestructura.
    """

    @abstractmethod
    def obtener_perfil_de_puntos(
        self,
        punto_inicial: Punto,
        punto_final: Punto,
        muestras: int,
    ) -> Tuple[List[Punto], str]:
        """
        Devuelve una lista de objetos Punto con sus elevaciones interpoladas
        entre punto_inicial y punto_final.
        """

    @abstractmethod
    def obtener_perfil_de_alturas(
        self,
        punto_inicial: Punto,
        punto_final: Punto,
        muestras: int,
    ) -> Tuple[List[float], str]:
        """
        Devuelve una lista de valores de altura (float) interpolados
        entre punto_inicial y punto_final.
        """

    @abstractmethod
    def obtener_elevacion_punto(self, punto: Punto) -> None:
        """
        Asigna in-place el valor de metros_sobre_nivel_mar del punto
        a partir de los datos de elevación.
        """
