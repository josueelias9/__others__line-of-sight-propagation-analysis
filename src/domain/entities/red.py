from typing import List


class Red:
    """
    Entidad que representa una red de radio-enlaces.

    Pertenece a la capa de Dominio.
    """

    def __init__(
        self,
        conectado: bool = False,
        lista_de_relaciones: List = None,
        lista_de_nodos: List = None,
        key: int = 0,
    ) -> None:
        self.conectado = conectado
        self.lista_de_relaciones: List = (
            lista_de_relaciones if lista_de_relaciones is not None else []
        )
        self.lista_de_nodos: List = (
            lista_de_nodos if lista_de_nodos is not None else []
        )
        self.key = key

    def __str__(self) -> str:
        return f"Red(conectado={self.conectado}, key={self.key})"
