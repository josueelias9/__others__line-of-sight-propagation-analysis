import math
from Punto import Punto
from Relacion import Relacion
#from Red import Red
from Internet import Internet


class TecnicoRed:
    '''
    Esta clase hace calculos con la informacion

    28-12-2018
    Dividir esta clase en dos clases:
    - una que trabaje con una archivo de entrada
    - otra que trabaje con dos archivos de entrada
    '''

    def __init__(self):
        self.internet = Internet()

    def __str__(self):
        texto='El tecnico usara "{}" muestras'.format(self.internet.samples)
        return texto

    '''
    input de metodos
    - Relaciones
    '''
    def calculaMenorDistanciaEnLista(self, listaDeRelaciones:list)-> Relacion:
        aux = 9000000
        #relacionAux = Relacion(None, None)
        for i in range(0, len(listaDeRelaciones)):
            distancia = listaDeRelaciones[i].distancia
            if aux >= distancia:
                aux = distancia
                relacionAux = listaDeRelaciones[i]
        return relacionAux

    '''
    input de metodos
    - Punto 
    - Puntos
    '''
    def lineaDeVistaConsiderandoFresnel(self, listaDePuntos:list, puntoInicial:Punto, puntoFinal:Punto)-> bool:
        y_0 = puntoInicial.metrosSobreElNivelDelMar + puntoInicial.alturaAntena
        x_0 = 0
        y_f = puntoFinal.metrosSobreElNivelDelMar + puntoFinal.alturaAntena
        x_f = len(listaDePuntos) - 1
        for i in range(1, len(listaDePuntos) - 1):
            x_i = i
            y_i = ((y_f - y_0) / (x_f - x_0)) * (x_i - x_0) + y_0
            if y_i - 0.6*self.fresnel(puntoInicial, puntoFinal, listaDePuntos[i]) <= listaDePuntos[i].metrosSobreElNivelDelMar:
                return False
        return True

    '''
    input de metodos
    - Punto
    '''
    def fresnel(self, puntoInicial:Punto, puntoFinal:Punto, puntoI:Punto)->float:
        '''funcion matematica
        :param puntoInicial:
        :param puntoFinal:
        :param puntoI:
        :return:
        '''
        distancia1 = Relacion(puntoInicial, puntoI).distancia*1000#en metros
        distancia2 = Relacion(puntoI, puntoFinal).distancia*1000 #en metros
        c = 3*pow(10, 8)
        f = 3*pow(10, 9)
        lambd = c/f
        return math.sqrt((lambd*distancia1*distancia2)/(distancia1+distancia2))

    def generaFresnel(self,puntoInicial:Punto, puntoFinal:Punto)->list:
        fresnel = []
        listaDePuntos, estado = self.internet.traerInfoDePuntos(puntoInicial, puntoFinal)
        y_0 = puntoInicial.metrosSobreElNivelDelMar + puntoInicial.alturaAntena
        x_0 = 0
        y_f = puntoFinal.metrosSobreElNivelDelMar + puntoFinal.alturaAntena
        x_f = len(listaDePuntos) - 1
        for i in range(0, len(listaDePuntos)):
            x_i = i
            a0 = ((y_f - y_0) / (x_f - x_0)) * (x_i - x_0) + y_0
            a1 = self.fresnel(puntoInicial, puntoFinal, listaDePuntos[i])
            listaDePuntos[i].metrosSobreElNivelDelMar = a0 - a1
            fresnel.append(Relacion(listaDePuntos[i - 1], listaDePuntos[i]))
        return fresnel

    def generaLineaDeVista(self,puntoInicial:Punto, puntoFinal:Punto)->list:
        fresnel = []
        listaDePuntos, estado = self.internet.traerInfoDePuntos(puntoInicial, puntoFinal)
        y_0 = puntoInicial.metrosSobreElNivelDelMar + puntoInicial.alturaAntena
        x_0 = 0
        y_f = puntoFinal.metrosSobreElNivelDelMar + puntoFinal.alturaAntena
        x_f = len(listaDePuntos) - 1
        for i in range(0, len(listaDePuntos)):
            x_i = i
            listaDePuntos[i].metrosSobreElNivelDelMar = ((y_f - y_0) / (x_f - x_0)) * (x_i - x_0) + y_0
            fresnel.append(Relacion(listaDePuntos[i - 1], listaDePuntos[i]))
        return fresnel

    def lineaDeVista(self, punto1, punto2):
        try:
            (puntosDeElevacion, estado) = self.internet.traerInfoDePuntos(punto1, punto2)
            a = self.lineaDeVistaConsiderandoFresnel(puntosDeElevacion, punto1, punto2)
        except:
            a = False
            print('MsgTecnicoRed: Estoy devolviendo "{}", pero hubo un error al usar los puntos "{}" y "{}"'.format(a,
                                                                                                                    punto1.nombre,
                                                                                                                    punto2.nombre))
        return a

    '''
    input de metodos
    - Puntos
    - int
    '''
    def ponleAlturas(self, listaDePuntos: list):
        for i in range(0, len(listaDePuntos)):
            self.internet.consigueDatoDeAlturaDeUnSoloPunto(listaDePuntos[i])
            print('MsgTecnicoRed: se puso...{}'.format(i))

    def encuentraRelacionesPosibles(self, lista1:list, lista2:list, distancia:int)-> (list, list):
        '''Esta funcion lo que hace es coger cada uno de los elementos de la lista2 y los compara con cada uno de los elementos de la lista 1.
        En caso a un elemento de la lista2 le corresponda 2 o mas elementos de la lista1 se quedara con aquel con la cual tenga la menor distancia.
        Esto se repetira hasta la cantidad de puntos relacionados por cada ciclo sea igual a 0, es decir, hasta que ya no se puedan asociar mas.
        :param lista1:
        :param lista2:
        :param distancia:
        :param muestras:
        :return:
        '''
        resultadoFinal = []
        listaNodosLibres = []
        listaNodosConectados = []
        listaRelacionesAux = []
        listaRelacionesErrores = []
        while True:
            for j in range(0, len(lista2)):
                for i in range(0, len(lista1)):
                    #print(Relacion(lista1[i], lista2[j]))
                    if distancia > Relacion(lista1[i], lista2[j]).distancia:
                        if self.lineaDeVista(lista1[i], lista2[j]):
                            listaRelacionesAux.append(Relacion(lista1[i], lista2[j]))
                if len(listaRelacionesAux) == 0:
                    listaNodosLibres.append(lista2[j])
                else:
                    listaNodosConectados.append(lista2[j])
                    menorRelacion = self.calculaMenorDistanciaEnLista(listaRelacionesAux)
                    resultadoFinal.append(menorRelacion)
                    listaRelacionesAux = []
            if len(listaNodosConectados) == 0:
                break
            else:
                print(len(listaNodosConectados))
                lista2 = listaNodosLibres
                lista1 = listaNodosConectados
                listaNodosLibres = []
                listaNodosConectados = []
        return resultadoFinal, listaRelacionesErrores

    def encontrarTodasLasRelacionesPosibles1Dist(self, listaDePuntos:list, distanciaMaxima:int)->list:
        '''
        :param listaDePuntos:
        :param distanciaMaxima: Distancia maxima de radio enlace
        :param muestras: Numero de muestras
        :return: list of Relaciones
        '''
        listaDeRelacionesPosibles = []
        aux = 1
        for i in range(0, len(listaDePuntos)):
            for j in range(aux, len(listaDePuntos)):
                print(str(i)+'-'+str(j))
                re = Relacion(listaDePuntos[i], listaDePuntos[j])
                if distanciaMaxima > re.distancia:
                    listaDeRelacionesPosibles.append(re)
            aux = aux+1
        return listaDeRelacionesPosibles

    def encontrarTodasLasRelacionesPosibles1LDVDist(self, listaDePuntos:list, distanciaMaxima:int)->list:
        '''
        :param listaDePuntos:
        :param distanciaMaxima: Distancia maxima de radio enlace
        :param muestras: Numero de muestras
        :return: list of Relaciones
        '''
        listaDeRelacionesPosibles = []
        aux = 1
        for i in range(0, len(listaDePuntos)):
            for j in range(aux, len(listaDePuntos)):
                print(str(i)+'-'+str(j))
                re = Relacion(listaDePuntos[i], listaDePuntos[j])
                if distanciaMaxima > re.distancia:
                    if self.lineaDeVista(listaDePuntos[i], listaDePuntos[j]):
                        listaDeRelacionesPosibles.append(re)
            aux = aux+1
        return listaDeRelacionesPosibles

    def encontrarTodasLasRelacionesPosibles2Dist(self, lista1: list, lista2: list, distanciaMaxima: int)->list:
        '''
        :param lista1:
        :param distanciaMaxima: Distancia maxima de radio enlace
        :param muestras: Numero de muestras
        :return: list of Relaciones
        '''
        listaDeRelacionesPosibles = []
        listaConectadosLista1 = set()
        listaConectadosLista2 = set()
        for i in range(0, len(lista1)):
            for j in range(0, len(lista2)):
                #print(str(i)+'-'+str(j))
                re = Relacion(lista1[i], lista2[j])
                if distanciaMaxima > re.distancia:
                    print(re.distancia)
                    listaDeRelacionesPosibles.append(re)
                    listaConectadosLista1.add(lista1[i])
                    listaConectadosLista2.add(lista2[j])
        return [listaDeRelacionesPosibles, list(listaConectadosLista1), list(listaConectadosLista2)]

    def encontrarTodasLasRelacionesPosibles2LDV(self, lista1:list,lista2:list)->list:
        '''
        :param lista1:
        :param distanciaMaxima: Distancia maxima de radio enlace
        :param muestras: Numero de muestras
        :return: list of Relaciones
        '''
        listaDeRelacionesPosibles = []
        listaConectadosLista1 = set()
        listaConectadosLista2 = set()
        for i in range(0, len(lista1)):
            for j in range(0, len(lista2)):
                print(str(i)+'-'+str(j))
                re = Relacion(lista1[i], lista2[j])
                if self.lineaDeVista(lista1[i], lista2[j]):
                    listaDeRelacionesPosibles.append(re)
                    listaConectadosLista1.add(lista1[i])
                    listaConectadosLista2.add(lista2[j])
        return [listaDeRelacionesPosibles, list(listaConectadosLista1), list(listaConectadosLista2)]

    def encontrarTodasLasRelacionesPosibles2LDVDist(self, lista1:list, lista2:list, distanciaMaxima:int)->list:
        '''
        :param listaDePuntos:
        :param distanciaMaxima: Distancia maxima de radio enlace
        :param muestras: Numero de muestras
        :return: list of Relaciones
        '''
        listaDeRelacionesPosibles = []
        listaConectadosLista1 = set()
        listaConectadosLista2 = set()        
        for i in range(0, len(lista1)):
            for j in range(0, len(lista2)):
                print(str(i)+'-'+str(j))
                re = Relacion(lista1[i], lista2[j])
                if distanciaMaxima > re.distancia:
                    if self.lineaDeVista(lista1[i], lista2[j]):
                        listaDeRelacionesPosibles.append(re)
                        listaConectadosLista1.add(lista1[i])
                        listaConectadosLista2.add(lista2[j])
        return [listaDeRelacionesPosibles, list(listaConectadosLista1), list(listaConectadosLista2)]

    def unePuntosQueSeQuedaronFuera(self,lista,distancia):
        def tareaRepetitiva():
            '''
            FUNCION 2
            para cada uno de los lementos de lista no conectados (j)
                para cada uno de los elementos de lista ultimos conectados (i)    
                    si i y j cumple con la condicion de distancia y linea de vista
                        agrega j a lista auxiliar ultimos conectados
                        salir (i)
                si se itero con todos los i y ninguno cumplio la condicion
                    agrega j a lista auxiliar no conectados
            retorna lista auxiliar ultimos conectados, lista auxiliar no conectados
            '''
            listaAuxiliarNoConectados = []
            listaAuxiliarUltimosConectados = []
            for j in range(0,len(listaNoConectados)):
                aux=True
                for i in range(0,len(listaUltimosConectados)):             
                    re=Relacion(listaUltimosConectados[i],listaNoConectados[j])
                    if re.distancia<distancia and self.lineaDeVista(listaNoConectados[j],listaUltimosConectados[i]):    
                        listaRelaciones.append(re)
                        listaAuxiliarUltimosConectados.append(listaNoConectados[j])
                        aux=False
                        break
                if aux:
                    listaAuxiliarNoConectados.append(listaNoConectados[j])
            #print('tamaño: {} {}'.format(len(listaAuxiliarUltimosConectados),len(listaAuxiliarNoConectados)))
            return listaAuxiliarUltimosConectados,listaAuxiliarNoConectados
        '''
        FUNCION 1
        lista conectados (vacio)
        lista ultimos conectados (solo el primero)
        lista no conectados (todos menos el primero)

        mientras que el tamaño de la lista ultimos conectados no sea 0
            lista ultimos conectados,lista no conectados = funcion(lista ultimos conectados, lista no conectados)
            lista conectados = lista conectados + lista ultimos conectados            
        crea red, asignale un identificador unico y que tenga la lista de conectados        
        '''
        listaRelaciones = []
        listaDeRedes = []
        listaNoConectados = lista
        aux=0
        while len(listaNoConectados) != 0:
            listaConectados = []
            listaUltimosConectados = [listaNoConectados[0]]
            del listaNoConectados[0]
            while len(listaUltimosConectados) != 0:
                print('tamaño de listas: {}\t{}'.format(len(listaUltimosConectados), len(listaNoConectados)))
                listaConectados=listaConectados+listaUltimosConectados    
                listaUltimosConectados,listaNoConectados=tareaRepetitiva()
            red = Red(listaDeNodos=listaConectados, key=aux)
            listaDeRedes.append(red)
            #print(red)
            aux = aux+1
        return listaDeRedes, listaRelaciones


if __name__=="__main__":
    print("casa")
    from Interface import InterfaceSalida
    from Interface import InterfaceEntrada
    hola = InterfaceEntrada()
    wwww = InterfaceSalida()
    eeee = TecnicoRed()
    r = hola.ordenameInput2()
    eeee.ponleAlturas(r)
    wwww.generarTxtDePuntos(r)