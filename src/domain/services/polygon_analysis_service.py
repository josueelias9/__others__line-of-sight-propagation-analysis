from typing import List

from shapely.geometry.polygon import Polygon

from domain.entities.estructura import Estructura
from domain.entities.poligonito import Poligonito
from domain.entities.poligonos import Poligonos


class PolygonAnalysisService:
    """
    Servicio de dominio para el análisis de polígonos de cobertura.

    Opera sobre una instancia de Estructura (que contiene la grilla polar
    y la matriz de estado LOS). Implementa el algoritmo BFS + máquina de
    estados que detecta y traza los polígonos de cobertura.

    Pertenece a la capa de Dominio.
    """

    def __init__(self, estructura: Estructura) -> None:
        self._est = estructura
        # Posición donde continúa la búsqueda entre llamadas a la máquina
        self._cursor_i: int = 0
        self._cursor_j: int = -1

    # ------------------------------------------------------------------ API pública

    def extraer_poligonos(self) -> Poligonos:
        """
        Ejecuta la máquina de estados hasta agotar todos los polígonos
        detectables en la estructura matricial.
        """
        lista: List[Poligonito] = []
        while True:
            poligonito = self._ejecutar_maquina_de_estados()
            if not poligonito.lista_de_puntos:
                break
            lista.append(poligonito)

        resultado = Poligonos()
        resultado.lista_de_poligonitos = lista
        return resultado

    def convertir_a_shapely(self, poligonos: Poligonos) -> Polygon:
        """
        Convierte el objeto Poligonos de dominio a un Polygon de Shapely
        (unión de todos los Poligonitos).
        """
        resultado = Polygon()
        for poligonito in poligonos.lista_de_poligonitos:
            parte = self._poligonito_a_shapely(poligonito)
            resultado = resultado.union(parte)
        return resultado

    # ------------------------------------------------------------------ BFS interno

    def _detectar_unos(self, i: int, j: int) -> List[List[int]]:
        """
        BFS que marca con 2/3 todos los celdas de valor 1 conectadas a (i,j),
        respetando las restricciones de cierre de polígono y diagonal.
        Devuelve la lista de coordenadas [i,j] del grupo encontrado.
        """
        mat = self._est.estructura_matricial
        if mat[i][j] != 1:
            return []

        cola = [[i, j]]
        mat[i][j] = 2
        grupo = [[i, j]]
        siguientes: List[List[int]] = []

        while cola:
            siguientes = []
            for celda in cola:
                a0, a1 = celda
                arr = self._valor(a0 + 1, a1)
                aba = self._valor(a0 - 1, a1)
                der = self._valor(a0, a1 + 1)
                izq = self._valor(a0, a1 - 1)

                vecinos_candidatos = [
                    (arr, a0 + 1, a1),
                    (aba, a0 - 1, a1),
                    (der, a0, a1 + 1),
                    (izq, a0, a1 - 1),
                ]
                tiene_vecino_1 = any(v[0] == 1 for v in vecinos_candidatos)

                for val, ni, nj in vecinos_candidatos:
                    if (
                        val == 1
                        and not self._cierra_poligono(ni, nj)
                        and not self._hay_problema_diagonal(ni, nj)
                    ):
                        mat[ni][nj] = 2
                        siguientes.append([ni, nj])
                        grupo.append([ni, nj])

                if tiene_vecino_1:
                    mat[a0][a1] = 3
                else:
                    mat[a0][a1] = 3
            cola = siguientes

        return grupo

    def _robot(self, i: int, j: int) -> bool:
        """
        BFS sobre celdas con valor 0. Devuelve True si el grupo llega al
        borde de la matriz (es exterior), False si está completamente encerrado.
        """
        mat = self._est.estructura_matricial
        if i == self._est.n or j == self._est.m:
            return True
        if i < 0 or j < 0:
            return True
        if mat[i][j] != 0:
            return False

        cola = [[i, j]]
        mat[i][j] = 4
        visitados = [[i, j]]

        while cola:
            siguientes: List[List[int]] = []
            for celda in cola:
                a0, a1 = celda
                for ni, nj in ((a0 + 1, a1), (a0 - 1, a1), (a0, a1 + 1), (a0, a1 - 1)):
                    if ni == self._est.n or nj == self._est.m or ni < 0 or nj < 0:
                        self._limpiar(visitados, 0)
                        return True
                    if mat[ni][nj] == 0:
                        mat[ni][nj] = 4
                        siguientes.append([ni, nj])
                        visitados.append([ni, nj])
                    mat[a0][a1] = 5
            cola = siguientes

        self._limpiar(visitados, 0)
        return False

    # ------------------------------------------------------------------ máquina de estados

    def _ejecutar_maquina_de_estados(self) -> Poligonito:
        """
        Máquina de estados de Mealy que traza el contorno de un polígono
        a partir de la posición del cursor interno.
        """
        (
            EST_INICIAL, EST_IZQ, EST_DER, EST_ARR, EST_ABA,
            EST_BUSCAR, EST_SUBE, EST_FINAL
        ) = range(8)

        mat = self._est.estructura_matricial
        poligonito = Poligonito()
        a_borrar: List[List[int]] = []
        estado = EST_INICIAL
        i = j = 0

        while True:
            # ── INICIAL ──────────────────────────────────────────────
            if estado == EST_INICIAL:
                i = self._cursor_i
                j = self._cursor_j
                estado = EST_BUSCAR

            # ── BUSCAR ───────────────────────────────────────────────
            elif estado == EST_BUSCAR:
                j += 1
                if j + 1 == self._est.m:
                    estado = EST_SUBE
                elif mat[i][j + 1] == 0:
                    estado = EST_BUSCAR
                elif mat[i][j + 1] == 1:
                    poligonito.vertice_inicial = [i, j]
                    self._cursor_i = i
                    self._cursor_j = j
                    a_borrar = self._detectar_unos(i, j + 1)
                    if self._da_la_vuelta():
                        # descartar la mitad superior del polígono circular
                        mitad = self._est.n // 2
                        a_borrar = [
                            c for c in a_borrar if c[0] <= mitad - 1
                        ]
                    estado = EST_DER

            # ── SUBE ─────────────────────────────────────────────────
            elif estado == EST_SUBE:
                i += 1
                j = -1
                if i == self._est.n:
                    return poligonito
                estado = EST_BUSCAR

            # ── DERECHA ──────────────────────────────────────────────
            elif estado == EST_DER:
                j += 1
                AR, AB, DE, IZ = self._vecinos(i, j)
                up = i + 1

                if poligonito.fin_del_poligono:
                    estado = EST_FINAL
                elif AR != 3 and AB != 3 and DE != 3 and IZ != 3:
                    tope = 0 if up == self._est.n else up
                    poligonito.ver_si_llego_al_final(
                        [[i, j - 1], [i, j], [tope, j], [tope, j - 1], [i, j - 1]]
                    )
                    estado = EST_FINAL
                elif DE == 3 and AB != 3:
                    poligonito.ver_si_llego_al_final([[i, j - 1]])
                    estado = EST_DER
                elif AR != 3 and AB != 3 and DE != 3:
                    tope = 0 if up == self._est.n else up
                    poligonito.ver_si_llego_al_final([[i, j - 1], [i, j], [tope, j]])
                    estado = EST_IZQ
                elif DE != 3 and AB != 3:
                    poligonito.ver_si_llego_al_final([[i, j - 1], [i, j]])
                    estado = EST_ARR
                elif AB == 3:
                    estado = EST_ABA

            # ── ABAJO ────────────────────────────────────────────────
            elif estado == EST_ABA:
                i -= 1
                AR, AB, DE, IZ = self._vecinos(i, j)
                up = i + 1

                if poligonito.fin_del_poligono:
                    estado = EST_FINAL
                elif AB == 3 and IZ != 3:
                    poligonito.ver_si_llego_al_final([[up, j - 1]])
                    estado = EST_ABA
                elif AB != 3 and DE != 3 and IZ != 3:
                    poligonito.ver_si_llego_al_final([[up, j - 1], [i, j - 1], [i, j]])
                    estado = EST_ARR
                elif AB != 3 and IZ != 3:
                    poligonito.ver_si_llego_al_final([[up, j - 1], [i, j - 1]])
                    estado = EST_DER
                elif IZ == 3:
                    estado = EST_IZQ

            # ── IZQUIERDA ────────────────────────────────────────────
            elif estado == EST_IZQ:
                j -= 1
                AR, AB, DE, IZ = self._vecinos(i, j)
                up = i + 1

                if poligonito.fin_del_poligono:
                    estado = EST_FINAL
                elif IZ == 3 and AR != 3:
                    tope = 0 if up == self._est.n else up
                    poligonito.ver_si_llego_al_final([[tope, j]])
                    estado = EST_IZQ
                elif IZ != 3 and AB != 3 and AR != 3:
                    tope = 0 if up == self._est.n else up
                    poligonito.ver_si_llego_al_final([[tope, j], [tope, j - 1], [i, j - 1]])
                    estado = EST_DER
                elif IZ != 3 and AR != 3:
                    tope = 0 if up == self._est.n else up
                    poligonito.ver_si_llego_al_final([[tope, j], [tope, j - 1]])
                    estado = EST_ABA
                elif AR == 3:
                    estado = EST_ARR

            # ── ARRIBA ───────────────────────────────────────────────
            elif estado == EST_ARR:
                i += 1
                AR, AB, DE, IZ = self._vecinos(i, j)
                up = i + 1

                if poligonito.fin_del_poligono:
                    estado = EST_FINAL
                elif AR == 3 and DE != 3:
                    poligonito.ver_si_llego_al_final([[i, j]])
                    estado = EST_ARR
                elif AR != 3 and DE != 3 and IZ != 3:
                    tope = 0 if up == self._est.n else up
                    poligonito.ver_si_llego_al_final([[i, j], [tope, j], [tope, j - 1]])
                    estado = EST_ABA
                elif AR != 3 and DE != 3:
                    tope = 0 if up == self._est.n else up
                    poligonito.ver_si_llego_al_final([[i, j], [tope, j]])
                    estado = EST_IZQ
                elif DE == 3:
                    estado = EST_DER

            # ── FINAL ────────────────────────────────────────────────
            elif estado == EST_FINAL:
                break

        self._limpiar(a_borrar, 0)
        return poligonito

    # ------------------------------------------------------------------ helpers privados

    def _valor(self, i: int, j: int) -> int:
        """Devuelve el valor en (i,j) o 0 si está fuera de los límites."""
        if i < 0 or i >= self._est.n or j < 0 or j >= self._est.m:
            return 0
        return self._est.estructura_matricial[i][j]

    def _vecinos(self, i: int, j: int):
        """Devuelve (arriba, abajo, derecha, izquierda) de la celda (i,j)."""
        return (
            self._valor(i + 1, j),
            self._valor(i - 1, j),
            self._valor(i, j + 1),
            self._valor(i, j - 1),
        )

    def _limpiar(self, lista: List[List[int]], valor: int) -> None:
        for celda in lista:
            self._est.estructura_matricial[celda[0]][celda[1]] = valor

    def _cierra_poligono(self, i: int, j: int) -> bool:
        arr = self._valor(i + 1, j)
        aba = self._valor(i - 1, j)
        der = self._valor(i, j + 1)
        izq = self._valor(i, j - 1)

        if (arr in (2, 3) and aba in (2, 3) and der in (0, 1) and izq in (0, 1)):
            if not self._robot(i, j + 1):
                return True
            if not self._robot(i, j - 1):
                return True
        elif (arr in (0, 1) and aba in (0, 1) and der in (2, 3) and izq in (2, 3)):
            if not self._robot(i + 1, j):
                return True
            if not self._robot(i - 1, j):
                return True
        return False

    def _hay_problema_diagonal(self, i: int, j: int) -> bool:
        arr = self._valor(i + 1, j)
        aba = self._valor(i - 1, j)
        der = self._valor(i, j + 1)
        izq = self._valor(i, j - 1)
        arr_der = self._valor(i + 1, j + 1)
        arr_izq = self._valor(i + 1, j - 1)
        aba_der = self._valor(i - 1, j + 1)
        aba_izq = self._valor(i - 1, j - 1)

        if aba_izq in (2, 3) and not (aba in (2, 3) or izq in (2, 3)):
            return True
        if arr_der in (2, 3) and not (arr in (2, 3) or der in (2, 3)):
            return True
        if arr_izq in (2, 3) and not (arr in (2, 3) or izq in (2, 3)):
            return True
        if aba_der in (2, 3) and not (aba in (2, 3) or der in (2, 3)):
            return True
        return False

    def _da_la_vuelta(self) -> bool:
        """Comprueba si el polígono detectado rodea el punto central."""
        llega_abajo = any(
            self._est.estructura_matricial[0][j] == 3
            for j in range(self._est.m)
        )
        llega_arriba = any(
            self._est.estructura_matricial[-1][j] == 3
            for j in range(self._est.m)
        )
        return llega_abajo and llega_arriba

    def _poligonito_a_shapely(self, poligonito: Poligonito) -> Polygon:
        coords = []
        for idx in poligonito.lista_de_puntos:
            pt = self._est.estructura_figuras_geome[idx[0]][idx[1]]
            coords.append((pt.longitud, pt.latitud))
        return Polygon(coords)
