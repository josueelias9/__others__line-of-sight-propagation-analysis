from typing import Any, Callable, Dict, List, Optional, Set, Tuple


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
        nombre: str = "",
        id: Optional[int] = None,
        geojson: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.conectado = conectado
        self.lista_de_relaciones: List = (
            lista_de_relaciones if lista_de_relaciones is not None else []
        )
        self.lista_de_nodos: List = lista_de_nodos if lista_de_nodos is not None else []
        self.key = key
        self.nombre = nombre
        self.id: Optional[int] = id
        self.geojson: Optional[Dict[str, Any]] = geojson

    # ------------------------------------------------------------------ análisis de red

    @staticmethod
    def encontrar_relaciones_por_distancia(
        lista: List, distancia_maxima: float
    ) -> List:
        """
        Devuelve todas las relaciones posibles entre los puntos de `lista`
        cuya distancia sea menor que `distancia_maxima`.
        """
        from domain.entities.relacion import Relacion

        relaciones: List = []
        for i in range(len(lista)):
            for j in range(i + 1, len(lista)):
                re = Relacion(lista[i], lista[j])
                if re.distancia < distancia_maxima:
                    relaciones.append(re)
        return relaciones

    @staticmethod
    def encontrar_relaciones_dos_listas_por_distancia(
        lista1: List,
        lista2: List,
        distancia_maxima: float,
    ) -> Tuple[List, List, List]:
        """
        Relaciona puntos de lista1 con lista2 que estén a menos de
        distancia_maxima. Devuelve (relaciones, conectados_lista1, conectados_lista2).
        """
        from domain.entities.relacion import Relacion

        relaciones: List = []
        conectados1: Set = set()
        conectados2: Set = set()

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
        lista1: List,
        lista2: List,
        distancia_maxima: float,
        verifica_los: Callable,
    ) -> Tuple[List, List]:
        """
        Para cada punto de lista2 busca el punto de lista1 más cercano
        con LOS. Si no hay candidato el punto queda sin conectar.

        Devuelve (relaciones_encontradas, errores).
        """
        from domain.entities.relacion import Relacion

        resultados: List = []
        sin_conexion: List = []
        sin_conectar = list(lista2)
        ya_conectados: List = list(lista1)

        while True:
            nuevos_conectados: List = []
            pendientes: List = []

            for punto in sin_conectar:
                candidatos: List = []
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
        lista: List,
        verifica_los: Callable,
        distancia_maxima: float,
    ) -> Tuple[List, List]:
        """
        Agrupa los puntos de `lista` en subredes (clusters) conectadas según
        criterio de distancia y LOS.

        Devuelve (lista_de_redes, lista_de_relaciones).
        """
        from domain.entities.relacion import Relacion

        relaciones: List = []
        redes: List = []
        no_conectados = list(lista)
        key = 0

        while no_conectados:
            conectados: List = []
            ultimos = [no_conectados.pop(0)]

            while ultimos:
                conectados.extend(ultimos)
                nuevos: List = []
                siguientes_no_conectados: List = []

                for nc in no_conectados:
                    encontrado = False
                    for uc in ultimos:
                        re = Relacion(uc, nc)
                        if re.distancia < distancia_maxima and verifica_los(nc, uc):
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

    # ------------------------------------------------------------------ repr

    def __str__(self) -> str:
        return f"Red(conectado={self.conectado}, key={self.key})"
