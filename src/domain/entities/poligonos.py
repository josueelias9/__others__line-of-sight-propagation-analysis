from typing import List

from domain.entities.poligonito import Poligonito


class Poligonos:
    """
    Entidad que agrupa una colección de Poligonitos formando el área de cobertura.

    Pertenece a la capa de Dominio.
    """

    def __init__(self) -> None:
        self.lista_de_poligonitos: List[Poligonito] = []
