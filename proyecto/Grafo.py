# -*- coding: utf-8 -*-
"""
Created on Tue May 29 00:28:21 2018

@author: Josue
"""

class GrafoDirigido:
    grafo={}
    def __str__(self):
        pass
    def agregarVertices(self, num):
        for i in range(0, num):
            self.grafo[str(i)] = []

    def agregarAdyacencia(self, v0: int, v1: int, w: float):
        self.grafo[str(v0)].append((str(v1), w))

class GrafoNoDirigido:
    grafo={}

    def agregarVertices(self, num):
        for i in range(0, num):
            self.grafo[str(i)] = []

    def agregarAdyacencia(self, v0: int, v1: int, w: float):
        '''
        Se crea asiciacion de v0 a v1 y de v1 a v0.
        :param v0: Vertice 0
        :param v1: Vertice 1
        :param w: Peso
        :return:
        '''
        self.grafo[str(v0)].append((str(v1), w))
        self.grafo[str(v1)].append((str(v0), w))

    def minimumSpanningTree(self,a):
        grafo = self.grafo
        listaVisitados = []
        grafoResultante = {}
        listaOrdenada = []

        origen=str(a)
        listaVisitados.append(origen)
        for destino, peso in grafo[origen]:
            listaOrdenada.append((origen, destino, peso))
        pos = 0
        act = 0
        listAux = []
        for i in range(len(listaOrdenada)):
            listAux = listaOrdenada[i]
            act = listaOrdenada[i][2]
            pos = i
            while pos > 0 and listaOrdenada[pos - 1][2] > act:
                listaOrdenada[pos] = listaOrdenada[pos - 1]
                pos = pos - 1
            listaOrdenada[pos] = listAux
        while listaOrdenada:
            vertice = listaOrdenada.pop(0)
            d = vertice[1]
            if d not in listaVisitados:
                listaVisitados.append(d)
                for key, lista in grafo[d]:
                    if key not in listaVisitados:
                        listaOrdenada.append((d, key, lista))
                listaOrdenada = [(c, a, b) for a, b, c in listaOrdenada]
                listaOrdenada.sort()
                listaOrdenada = [(a, b, c) for c, a, b in listaOrdenada]
                origen = vertice[0]
                destino = vertice[1]
                peso = vertice[2]
                if origen in grafoResultante:
                    if destino in grafoResultante:
                        lista = grafoResultante[origen]
                        grafoResultante[origen] = lista + [(destino, peso)]
                        lista = grafoResultante[destino]
                        lista.append((origen, peso))
                        grafoResultante[destino] = lista
                    else:
                        grafoResultante[destino] = [(origen, peso)]
                        lista = grafoResultante[origen]
                        lista.append((destino, peso))
                        grafoResultante[origen] = lista
                elif destino in grafoResultante:
                    grafoResultante[origen] = [(destino, peso)]
                    lista = grafoResultante[destino]
                    lista.append((origen, peso))
                    grafoResultante[destino] = lista
                else:
                    grafoResultante[destino] = [(origen, peso)]
                    grafoResultante[origen] = [(destino, peso)]

        print("\n\nGrafo resultante:\n")
        for key, lista in grafoResultante.items():
            print(key)
            print(lista)

if __name__=="__main__":
    '''importando todo lo que necesitamos'''
    import Factor      
    from Relacion import Relacion
    from Secretaria import Secretaria
    from Impresora import Impresora
    from scipy.sparse import csr_matrix
    from scipy.sparse.csgraph import minimum_spanning_tree
    '''====================================
    ===================================='''
    Factor.generaBases()
    secretaria = Secretaria(Factor.lugarDeTrabajo)
    impresora = Impresora(Factor.lugarDeTrabajo)
    listaAcces = secretaria.ordenameInput2(Factor.nombreArchivoAcces)
    impresora.generaKmlPuntos(listaAcces,Factor.nombreArchivoAcces)
    
    '''====================================
    generando matriz triangular superior con las todas las distancias 
    https://es.wikipedia.org/wiki/Matriz_triangular
    ===================================='''
    b=[]
    for i in range(0,len(listaAcces)):
        a=[]
        aux=i
        for j in range(0,len(listaAcces)):
            re=Relacion(listaAcces[aux],listaAcces[j])
            re.distanciaEntrePuntos
            if aux < j:
                a.append(re.distancia)
            else:
                a.append(0)
        b.append(a)
    for a in range(0,len(b)):
        print(b[a])
    #print(nodosNoConectados)
    '''====================================
    algoritmo para poder hacer el calculo de minimun spaning tree
    https://docs.scipy.org/doc/scipy-0.15.1/reference/generated/scipy.sparse.csgraph.minimum_spanning_tree.html
    ===================================='''
    X = csr_matrix(b)
    Tcsr = minimum_spanning_tree(X)
    print(type(Tcsr))
    '''====================================
    convertir la sparse matrix en una lista [] para poder tener acceso a los elementos
    https://stackoverflow.com/questions/15115765/how-to-access-sparse-matrix-elements
    ===================================='''
    temp_list = []
    for i in Tcsr:
        temp_list.append(list(i.A[0]))
    '''====================================
    imprime lista recien formada
    ===================================='''
    print(temp_list)