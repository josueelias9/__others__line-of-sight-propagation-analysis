import logging
import math
from typing import List

from domain.entities.poligonito import Poligonito
from domain.entities.poligonos import Poligonos
from domain.entities.punto import Punto

logger = logging.getLogger(__name__)


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

        # cursor para la máquina de estados de extracción de polígonos
        self._cursor_i: int = 0
        self._cursor_j: int = -1

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

    # ------------------------------------------------------------------ extracción de polígonos

    def extraer_poligonos(self) -> Poligonos:
        """
        Ejecuta la máquina de estados hasta agotar todos los polígonos
        detectables en la estructura matricial.
        """
        lista: List[Poligonito] = []
        counter = 0
        while True:
            poligonito = self._ejecutar_maquina_de_estados()
            if not poligonito.lista_de_puntos:
                break
            lista.append(poligonito)
            counter += 1
            logger.debug("polígono %d detectado con %d puntos.", counter, len(poligonito.lista_de_puntos))

        resultado = Poligonos()
        resultado.lista_de_poligonitos = lista
        return resultado

    def coordenadas_poligonito(self, poligonito: Poligonito) -> List:
        """
        Devuelve la lista de coordenadas (longitud, latitud) de un Poligonito
        mapeando sus índices matriciales a puntos geográficos reales.
        """
        coords = []
        for idx in poligonito.lista_de_puntos:
            pt = self.estructura_figuras_geome[idx[0]][idx[1]]
            coords.append((pt.longitud, pt.latitud))
        return coords

    # ------------------------------------------------------------------ BFS interno

    def _detectar_unos(self, i: int, j: int) -> List[List[int]]:
        """
        BFS que marca con 2/3 todos los celdas de valor 1 conectadas a (i,j),
        respetando las restricciones de cierre de polígono y diagonal.
        Devuelve la lista de coordenadas [i,j] del grupo encontrado.
        """
        mat = self.estructura_matricial
        if mat[i][j] != 1:
            return []

        cola = [[i, j]]
        mat[i][j] = 2
        grupo = [[i, j]]

        while cola:
            siguientes: List[List[int]] = []
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
        mat = self.estructura_matricial
        if i == self.n or j == self.m:
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
                    if ni == self.n or nj == self.m or ni < 0 or nj < 0:
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
    # TODO error aqui! revisar
    def _ejecutar_maquina_de_estados(self) -> Poligonito:
        """
        Máquina de estados de Mealy que traza el contorno de un polígono
        a partir de la posición del cursor interno.
        """
        (
            EST_INICIAL, EST_IZQ, EST_DER, EST_ARR, EST_ABA,
            EST_BUSCAR, EST_SUBE, EST_FINAL
        ) = range(8)

        mat = self.estructura_matricial
        poligonito = Poligonito()
        a_borrar: List[List[int]] = []
        estado = EST_INICIAL
        i = j = 0

        while True:
            # ── INICIAL ──────────────────────────────────────────────
            if estado == EST_INICIAL:
                logger.debug("estado INICIAL en (%d, %d)", i, j)
                i = self._cursor_i
                j = self._cursor_j
                estado = EST_BUSCAR

            # ── BUSCAR ───────────────────────────────────────────────
            elif estado == EST_BUSCAR:
                logger.debug("estado BUSCAR en (%d, %d)", i, j)
                j += 1
                if j + 1 == self.m:
                    estado = EST_SUBE
                elif mat[i][j + 1] == 0:
                    estado = EST_BUSCAR
                elif mat[i][j + 1] == 1:
                    poligonito.vertice_inicial = [i, j]
                    self._cursor_i = i
                    self._cursor_j = j
                    a_borrar = self._detectar_unos(i, j + 1)
                    if self._da_la_vuelta():
                        mitad = self.n // 2
                        a_borrar = [c for c in a_borrar if c[0] <= mitad - 1]
                    estado = EST_DER

            # ── SUBE ─────────────────────────────────────────────────
            elif estado == EST_SUBE:
                logger.debug("estado SUBE en (%d, %d)", i, j)
                i += 1
                j = -1
                if i == self.n:
                    return poligonito
                estado = EST_BUSCAR

            # ── DERECHA ──────────────────────────────────────────────
            elif estado == EST_DER:
                logger.debug("estado DER en (%d, %d)", i, j)
                j += 1
                AR, AB, DE, IZ = self._vecinos(i, j)
                up = i + 1

                if poligonito.fin_del_poligono:
                    estado = EST_FINAL
                elif AR != 3 and AB != 3 and DE != 3 and IZ != 3:
                    tope = 0 if up == self.n else up
                    poligonito.ver_si_llego_al_final(
                        [[i, j - 1], [i, j], [tope, j], [tope, j - 1], [i, j - 1]]
                    )
                    estado = EST_FINAL
                elif DE == 3 and AB != 3:
                    poligonito.ver_si_llego_al_final([[i, j - 1]])
                    estado = EST_DER
                elif AR != 3 and AB != 3 and DE != 3:
                    tope = 0 if up == self.n else up
                    poligonito.ver_si_llego_al_final([[i, j - 1], [i, j], [tope, j]])
                    estado = EST_IZQ
                elif DE != 3 and AB != 3:
                    poligonito.ver_si_llego_al_final([[i, j - 1], [i, j]])
                    estado = EST_ARR
                elif AB == 3:
                    estado = EST_ABA

            # ── ABAJO ────────────────────────────────────────────────
            elif estado == EST_ABA:
                logger.debug("estado ABA en (%d, %d)", i, j)
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
                logger.debug("estado IZQ en (%d, %d)", i, j)
                j -= 1
                AR, AB, DE, IZ = self._vecinos(i, j)
                up = i + 1

                if poligonito.fin_del_poligono:
                    estado = EST_FINAL
                elif IZ == 3 and AR != 3:
                    tope = 0 if up == self.n else up
                    poligonito.ver_si_llego_al_final([[tope, j]])
                    estado = EST_IZQ
                elif IZ != 3 and AB != 3 and AR != 3:
                    tope = 0 if up == self.n else up
                    poligonito.ver_si_llego_al_final([[tope, j], [tope, j - 1], [i, j - 1]])
                    estado = EST_DER
                elif IZ != 3 and AR != 3:
                    tope = 0 if up == self.n else up
                    poligonito.ver_si_llego_al_final([[tope, j], [tope, j - 1]])
                    estado = EST_ABA
                elif AR == 3:
                    estado = EST_ARR

            # ── ARRIBA ───────────────────────────────────────────────
            elif estado == EST_ARR:
                logger.debug("estado ARR en (%d, %d)", i, j)
                i += 1
                AR, AB, DE, IZ = self._vecinos(i, j)
                up = i + 1

                if poligonito.fin_del_poligono:
                    estado = EST_FINAL
                elif AR == 3 and DE != 3:
                    poligonito.ver_si_llego_al_final([[i, j]])
                    estado = EST_ARR
                elif AR != 3 and DE != 3 and IZ != 3:
                    tope = 0 if up == self.n else up
                    poligonito.ver_si_llego_al_final([[i, j], [tope, j], [tope, j - 1]])
                    estado = EST_ABA
                elif AR != 3 and DE != 3:
                    tope = 0 if up == self.n else up
                    poligonito.ver_si_llego_al_final([[i, j], [tope, j]])
                    estado = EST_IZQ
                elif DE == 3:
                    estado = EST_DER

            # ── FINAL ────────────────────────────────────────────────
            elif estado == EST_FINAL:
                logger.debug("estado FINAL en (%d, %d)", i, j)
                break

        self._limpiar(a_borrar, 0)
        return poligonito

    # ------------------------------------------------------------------ helpers privados

    def _valor(self, i: int, j: int) -> int:
        """Devuelve el valor en (i,j) o 0 si está fuera de los límites."""
        if i < 0 or i >= self.n or j < 0 or j >= self.m:
            return 0
        return self.estructura_matricial[i][j]

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
            self.estructura_matricial[celda[0]][celda[1]] = valor

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
            self.estructura_matricial[0][j] == 3
            for j in range(self.m)
        )
        llega_arriba = any(
            self.estructura_matricial[-1][j] == 3
            for j in range(self.m)
        )
        return llega_abajo and llega_arriba
