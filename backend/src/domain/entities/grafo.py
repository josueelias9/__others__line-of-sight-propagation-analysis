from typing import Dict, List, Tuple


class GrafoDirigido:
    """Grafo dirigido con representación de lista de adyacencia."""

    def __init__(self) -> None:
        self.grafo: Dict[str, List[Tuple[str, float]]] = {}

    def agregar_vertices(self, num: int) -> None:
        for i in range(num):
            self.grafo[str(i)] = []

    def agregar_adyacencia(self, v0: int, v1: int, w: float) -> None:
        self.grafo[str(v0)].append((str(v1), w))


class GrafoNoDirigido:
    """
    Grafo no dirigido con representación de lista de adyacencia.
    Incluye cálculo de árbol de expansión mínima (Prim).

    Pertenece a la capa de Dominio.
    """

    def __init__(self) -> None:
        self.grafo: Dict[str, List[Tuple[str, float]]] = {}

    def agregar_vertices(self, num: int) -> None:
        for i in range(num):
            self.grafo[str(i)] = []

    def agregar_adyacencia(self, v0: int, v1: int, w: float) -> None:
        self.grafo[str(v0)].append((str(v1), w))
        self.grafo[str(v1)].append((str(v0), w))

    def minimum_spanning_tree(self, origen: int) -> Dict[str, List[Tuple[str, float]]]:
        """Calcula el árbol de expansión mínima usando el algoritmo de Prim."""
        lista_visitados: List[str] = []
        grafo_resultante: Dict[str, List[Tuple[str, float]]] = {}
        lista_ordenada: List[Tuple[str, str, float]] = []

        origen_str = str(origen)
        lista_visitados.append(origen_str)
        for destino, peso in self.grafo[origen_str]:
            lista_ordenada.append((origen_str, destino, peso))
        lista_ordenada.sort(key=lambda x: x[2])

        while lista_ordenada:
            vertice = lista_ordenada.pop(0)
            d = vertice[1]
            if d not in lista_visitados:
                lista_visitados.append(d)
                for key, lista in self.grafo[d]:
                    if key not in lista_visitados:
                        lista_ordenada.append((d, key, lista))
                lista_ordenada.sort(key=lambda x: x[2])

                o = vertice[0]
                dest = vertice[1]
                peso = vertice[2]
                grafo_resultante.setdefault(o, []).append((dest, peso))
                grafo_resultante.setdefault(dest, []).append((o, peso))

        return grafo_resultante
