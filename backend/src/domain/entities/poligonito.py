from typing import List


class Poligonito:
    """
    Entidad que representa un fragmento de polígono de cobertura.

    Almacena los índices (fila, columna) de la matriz de la Estructura
    que componen el contorno del polígono.

    Pertenece a la capa de Dominio.
    """

    def __init__(self) -> None:
        self.vertice_inicial: List[int] = []
        self.fin_del_poligono: bool = False
        self.lista_de_puntos: List[List[int]] = []
        self._contador: int = 0

    def ver_si_llego_al_final(self, lista: List[List[int]]) -> None:
        """
        Agrega puntos a la lista y verifica si el polígono se cerró.
        El polígono se considera cerrado cuando el vértice inicial aparece
        por segunda vez.
        """
        for punto in lista:
            self.lista_de_puntos.append(punto)
            if (
                len(self.vertice_inicial) >= 2
                and punto[0] == self.vertice_inicial[0]
                and punto[1] == self.vertice_inicial[1]
            ):
                self._contador += 1
                if self._contador == 2:
                    self.fin_del_poligono = True
                    return
