from typing import Callable, List, Set, Tuple

from domain.entities.punto import Punto
from domain.entities.red import Red
from domain.entities.relacion import Relacion


class NetworkAnalysisService:
    """
    Servicio de dominio para análisis de redes de radio-enlace.

    Todos los métodos son stateless. Cuando se necesita verificar LOS,
    recibe la función verificadora como parámetro para no depender de
    ningún repositorio externo.

    Pertenece a la capa de Dominio.
    """

    @staticmethod
    def encontrar_relaciones_por_distancia(
        lista: List[Punto],
        distancia_maxima: float,
    ) -> List[Relacion]:
        """
        Devuelve todas las relaciones posibles entre los puntos de `lista`
        cuya distancia sea menor que `distancia_maxima`.
        """
        relaciones: List[Relacion] = []
        for i in range(len(lista)):
            for j in range(i + 1, len(lista)):
                re = Relacion(lista[i], lista[j])
                if re.distancia < distancia_maxima:
                    relaciones.append(re)
        return relaciones

    @staticmethod
    def encontrar_relaciones_dos_listas_por_distancia(
        lista1: List[Punto],
        lista2: List[Punto],
        distancia_maxima: float,
    ) -> Tuple[List[Relacion], List[Punto], List[Punto]]:
        """
        Relaciona puntos de lista1 con lista2 que estén a menos de
        distancia_maxima. Devuelve (relaciones, conectados_lista1, conectados_lista2).
        """
        relaciones: List[Relacion] = []
        conectados1: Set[Punto] = set()
        conectados2: Set[Punto] = set()

        for p1 in lista1:
            for p2 in lista2:
                re = Relacion(p1, p2)
                if re.distancia < distancia_maxima:
                    relaciones.append(re)
                    conectados1.add(p1)
                    conectados2.add(p2)

        return relaciones, list(conectados1), list(conectados2)

    @staticmethod
    def encontrar_menor_relacion(
        lista1: List[Punto],
        lista2: List[Punto],
        distancia_maxima: float,
        verifica_los: Callable[[Punto, Punto], bool],
    ) -> Tuple[List[Relacion], List]:
        """
        Para cada punto de lista2 busca el punto de lista1 más cercano
        con LOS. Si no hay candidato el punto queda sin conectar.

        Devuelve (relaciones_encontradas, errores).
        """
        resultados: List[Relacion] = []
        sin_conexion: List[Punto] = []
        sin_conectar = list(lista2)
        ya_conectados: List[Punto] = list(lista1)

        while True:
            nuevos_conectados: List[Punto] = []
            pendientes: List[Punto] = []

            for punto in sin_conectar:
                candidatos: List[Relacion] = []
                for base in ya_conectados:
                    re = Relacion(base, punto)
                    if re.distancia < distancia_maxima and verifica_los(base, punto):
                        candidatos.append(re)

                if candidatos:
                    mejor = min(candidatos, key=lambda r: r.distancia)
                    resultados.append(mejor)
                    nuevos_conectados.append(punto)
                else:
                    pendientes.append(punto)

            if not nuevos_conectados:
                sin_conexion.extend(pendientes)
                break

            ya_conectados.extend(nuevos_conectados)
            sin_conectar = pendientes

        return resultados, sin_conexion

    @staticmethod
    def clusterizar(
        lista: List[Punto],
        verifica_los: Callable[[Punto, Punto], bool],
        distancia_maxima: float,
    ) -> Tuple[List[Red], List[Relacion]]:
        """
        Agrupa los puntos de `lista` en subredes (clusters) conectadas según
        criterio de distancia y LOS.

        Devuelve (lista_de_redes, lista_de_relaciones).
        """
        relaciones: List[Relacion] = []
        redes: List[Red] = []
        no_conectados = list(lista)
        key = 0

        while no_conectados:
            conectados: List[Punto] = []
            ultimos = [no_conectados.pop(0)]

            while ultimos:
                conectados.extend(ultimos)
                nuevos: List[Punto] = []
                siguientes_no_conectados: List[Punto] = []

                for nc in no_conectados:
                    encontrado = False
                    for uc in ultimos:
                        re = Relacion(uc, nc)
                        if (
                            re.distancia < distancia_maxima
                            and verifica_los(nc, uc)
                        ):
                            relaciones.append(re)
                            nuevos.append(nc)
                            encontrado = True
                            break
                    if not encontrado:
                        siguientes_no_conectados.append(nc)

                ultimos = nuevos
                no_conectados = siguientes_no_conectados

            redes.append(Red(lista_de_nodos=conectados, key=key))
            key += 1

        return redes, relaciones
