# -*- coding: utf-8 -*-
"""
Created on Tue May 29 00:49:48 2018

@author: Josue
"""
from timeit import default_timer as timer
import math
import Factor
from Punto import Punto
from Impresora import Impresora
from Secretaria import Secretaria
from Relacion import Relacion
from TecnicoRed import TecnicoRed
from itertools import combinations
from TecnicoPoligono import TecnicoPoligono
from Estructura import Estructura
from shapely.geometry import mapping
#from shapely.geometry.polygon import LinearRing, Polygon
#import shapely.geometry as sg
#import shapely.ops as so
class Jefe:
    '''
    Esta clase se comunica con el usuario
    '''
    # =================================================================================================
    # =================================================================================================
    # =================================================================================================
    def __init__(self,numeroDeLDV,muestras,distancia,alturaTorreFantasma,lugarConectado,lugarNoConectado):
        self.listaTra = []
        self.listaAcc = []
        self.tecnico = TecnicoRed(muestras)
        self.impresora = Impresora(Factor.lugarDeTrabajo)
        self.secretaria = Secretaria(Factor.lugarDeTrabajo)
        self.numeroDeLDV=numeroDeLDV
        self.muestras=muestras
        self.distancia=distancia
        self.alturaTorreFantasma=alturaTorreFantasma
        self.lugarConectado=lugarConectado
        self.lugarNoConectado=lugarNoConectado
    # =================================================================================================
    # =================================================================================================
    # =================================================================================================
    def todasLasRelacionesPosibles(self):
        self.listaAcc = self.secretaria.ordenameInput2('unSoloTrasporte')
        lista = self.tecnico.encontrarTodasLasRelacionesPosibles(self.listaAcc, 30, 300)
        self.impresora.generarTxtDeRelaciones(lista,self.listaAcc[0].nombre)
        self.impresora.generaKmlRutas(lista,self.listaAcc[0].nombre)


    def funcionFinal0(self,nombre):
        '''
        grafica puntos
        :return:
        '''
        lista1=self.secretaria.ordenameInput2(nombre)
        self.impresora.generaKmlPuntos(lista1,nombre)

    def funcionFinal1(self,nombre):
        '''
        pone altura a puntos
        :return:
        '''
        lista1 = self.secretaria.ordenameInput2(nombre)
        self.tecnico.ponleAlturas(lista1)
        self.impresora.generarTxtDePuntos(lista1, nombre)
        
    def funcionFinal2(self):
        '''
        genera el arbol, genera kml y txt de relaciones
        :param nombre1: nodos conectados
        :param nombre2: nodos no conectados
        :param distancia:
        :param muestras:
        :param nombre3: nombre de archivo salida
        :param nombre3: nombre de archivo errores
        :return:
        '''
        lista1 = self.secretaria.ordenameInput2(self.lugarConectado)
        lista2 = self.secretaria.ordenameInput2(self.lugarNoConectado)
        uno, dos = self.tecnico.encuentraRelacionesPosibles(lista1, lista2, self.distancia)
        self.impresora.generaKmlRutas(uno, 'red','absolute')
        self.impresora.generaKmlRutas(dos, 'errores','absolute')
        self.impresora.generarTxtDeRelaciones(uno, 'red')
        self.impresora.generarTxtDeRelaciones(dos, 'errores')


    def funcionFinal3(self,nombreDeArchivoALeer:str):
        '''
        2 km
        :return:
        '''
        #DEFINIENDO
        lista=self.secretaria.ordenameInput2(nombreDeArchivoALeer)
        lista2=self.tecnico.encontrarTodasLasRelacionesPosibles1LDVDist(lista,2,300)
        #SALIDA
        self.impresora.generaKmlRutas(lista2,'rutas')
        self.impresora.generarTxtDeRelaciones(lista2,'texto')

    def funcionFinal4(self,nombre1:str):
        '''
        grafica relaciones
        :param nombre1: nombre de archivo de lectura txt
        :param nombre2: nombre de archivo de escritura kml
        :return:
        '''
        #LEE...
        lista=self.secretaria.leeListaDeRutas(nombre1)
        #IMPRIME
        self.impresora.generaKmlRutas(lista,nombre1,'absolute')

    def emergencia(self,nombre1,nombre2):
        '''
        -> este programa relaciona los elementos de la lista nombre1 con los elementos
        de la lista nombre2 de acuerdo a la distancia "self.distancia"
        Pseudocodigo:
        para cada uno de los elementos de la lista noTiene
            primero, establece un valor inicial de una distancia muy grande.
            para cada uno de los elementos de la lista siTiene
                si la distancia entre el elemento de noTiene y siTiene
                es menor a un valor de referencia entonces
                    guara la relacion y guarda la distancia
            despues que acabaste de iterar un elemento de la lista noTiene
            con todos los elementod de la lista siTiene te estas quedando con
            la menor relacion'''
        self.funcionFinal1(nombre1)
        self.funcionFinal1(nombre2)
        siTiene=self.secretaria.ordenameInput2(nombre1)
        noTiene=self.secretaria.ordenameInput2(nombre2)
        print('si tiene 3G: '+str(len(siTiene)))
        print('no tiene 3G: '+str(len(noTiene)))
        lista=[]
        contador=0
        for j in range(0,len(noTiene)):
            relacionAux=0
            #print('MsgJefe: estas en "{}" {}'.format(nombre2,j))
            aux = self.distancia
            print('MsgJefe: Valor de {}'.format(aux))
            for i in range(0,len(siTiene)):                
                contador=contador+1
                distancia=Relacion(siTiene[i],noTiene[j]).distancia
                if aux >= distancia:
                    #print('MsgJefe: superaste el filtro de distancia. La distancia es {}'.format(distancia))
                    if True:#self.tecnico.lineaDeVista(siTiene[i],noTiene[j]):
                        print('MsgJefe: superaste el filtro de linea de vista')
                        aux = distancia
                        relacionAux = Relacion(siTiene[i],noTiene[j])
                        relacionAux.distancia=distancia
                        noTiene[j].greenAsociado=siTiene[i].tipo
            if relacionAux!=0:
                lista.append(relacionAux)
        self.impresora.generaKmlPuntos(siTiene,nombre1)
        self.impresora.generaKmlPuntos(noTiene,nombre2)
        self.impresora.generarTxtDeRelaciones(lista,'bitel')
        self.impresora.generaKmlRutas(lista,'bitel','absolute')
        self.impresora.generarTxtDePuntos(siTiene,nombre1+'2')
        self.impresora.generarTxtDePuntos(noTiene,nombre2+'2')
        print(contador)

    def gabriel(self,nombre1,nombre2):
        '''
        encuentra puntos que alrededor de otros a una distancia determinada
        :param nombre1: puntos fijos
        :param nombre2: ver si estos puntos estan alrededor de los puntos fijos y mostrarlos
        :return:
        '''
        lista1 = self.secretaria.ordenameInput2(nombre1)
        lista2 = self.secretaria.ordenameInput2(nombre2)
        nada,dentro,fuera=self.tecnico.encontrarTodasLasRelacionesPosibles2Dist(lista1,lista2,5)
        self.impresora.generaKmlPuntos(dentro,'puntos alrededor')
        self.impresora.generarTxtDePuntos(dentro,'puntos alrededor')
    
    def funciona(self):
        '''
        genera clusteres a partir de una lista
        '''
        lista = self.secretaria.ordenameInput2('fuera')
        uno = self.tecnico.unePuntosQueSeQuedaronFuera(lista,self.distancia)
        self.impresora.generaKmlRutas(uno, 'clusteres','absolute')
        self.impresora.generarTxtDeRelaciones(uno, 'clusteres')

    # =================================================================================================
    # =================================================================================================
    # =================================================================================================
    
    def hasTodoSinInternet(self):
        listaDePuntos = self.sec.ordenameInput2('nodo')
        for i in range(0,len(listaDePuntos)):
            matrixAux = [
                [0, 1, 1, 1, 0],
                [0, 1, 1, 1, 0],
                [0, 1, 0, 1, 0],
                [0, 1, 0, 1, 0],
                [0, 1, 1, 1, 0],
                [0, 1, 1, 1, 0]]
            est = Estructura(len(matrixAux), len(matrixAux[0]), .01, listaDePuntos[i])
            est.estructuraMatricial = matrixAux
            listaTotal=est.funcionMacroSinInternet()
            # tarea de impresora
            self.im.ploteadorDeMatriz(est.estructuraMatricial)
            self.im.hacerMallaSegunEstructuraMatricial(est.puntoCero.nombre + '_partido', est.estructuraMatricial,est.estructuraFigurasGeome, est.n, est.m)
            self.im.graficaPuntosEstructura(est.estructuraLineaDeVista,est.puntoCero.nombre + '_puntos_linea_de_vista', 'arrow')
            self.im.graficaPuntosEstructura(est.estructuraFigurasGeome, est.puntoCero.nombre + '_puntos_geometria','square')
            self.im.funcion(listaTotal, est.puntoCero.nombre + '_completo')
    
    def dePuntoAPoligono(self,punto:Punto):
        estructura=Estructura(self.numeroDeLDV,self.muestras,Factor.deKilometrosAGrados(self.distancia),punto,self.alturaTorreFantasma)
        tecnicoPoligono = TecnicoPoligono(estructura,self.muestras)        
        return tecnicoPoligono.funcionMacroConInternet()
    '''
    hayInterseccionEnTupla-------->   dePuntoAPoligono
                    
    ''' 
    
    def ultimaEsperanza(self,nombreee,nombreee2):
        def hayInterseccionEnTupla(tupla):
            '''intersecta todos los elementos de la tupla, y si no no hay interseccion 
            entre todos los elementos retorna falso en la variable "flag. La variable c 
            contiene el poligono. Ademas esta retornando otro valor pero no se que es. Averiguar.'''
            flag=True
            c=self.dePuntoAPoligono(tupla[0])
            for i in range(1,len(tupla)):
                b=self.dePuntoAPoligono(tupla[i])
                c=c.intersection(b)
                if c.wkt=='GEOMETRYCOLLECTION EMPTY':
                    flag=False
                    return flag,c
            return flag,c
              
        def funcion(lista):    
            '''ve si en la lista hay algun relacion de puntos que este a una distancia
            mayor a dos veces la distancia max definida de radioenlace'''
            aux=1      
            for i in range(0,len(lista)):
                for j in range(aux,len(lista)):
                    if Relacion(lista[i],lista[j]).distancia>self.distancia*2:
                        return False
                aux=aux+1
            return True

        '''encuentra la primera interseccion de varios puntos y la plotea.
        La estoy usando para el proyecto de la banda 2.6GHz'''
        
        jefe.funcionFinal0(nombreee)#grafica
        jefe.funcionFinal1(nombreee)#pone alturas
        lista = jefe.secretaria.ordenameInput2(nombreee)
        
        print('MsgJefe: el tamaño de lista es {}'.format(len(lista)))
        for j in range(len(lista)-3,len(lista)):
            #print('MsgJefe: para j, de {} a {}'.format(len(lista)-6,len(lista)))
            comb=combinations(lista,len(lista)-j)
            for tupla in list(comb):
                print('MsgJefe: comb contiene varias tuplas. Una de ellas contiene los siguientes puntos:')
                for i in range(0,len(tupla)):
                    print('elemento {}'.format(tupla[i]))
                if funcion(tupla):
                    print('MsgJefe: Todos los puntos estan a menos de {}'.format(self.distancia*2))
                    a,b=hayInterseccionEnTupla(tupla)
                    if a==True:
                        self.impresora.deWktAKml(nombreee2+" mancha",mapping(b))                                                    
                        self.impresora.generarTxtDePuntos(tupla,nombreee2)
                        self.impresora.generaKmlPuntos(tupla,nombreee2)
                        print('MsgJefe: Se encontro area!')
                        return True
                else:
                    print('MsgJefe: Se salio porque hay un par de puntos que esta a mas de {}'.format(self.distancia*2))
        return False
                
    
    def hasTodoConInternet(self):
        nodosNoConectados = self.secretaria.ordenameInput2(self.lugarConectado)
        nodosConectados = self.secretaria.ordenameInput2(self.lugarNoConectado)       
        for i in range(0,len(nodosNoConectados)):
            print('Nodo no conectado '+str(i)+'. Analizando...')
            c=self.dePuntoAPoligono(nodosNoConectados[i])
            cAux=c   
            listaAux=[]
            ###################SAQUE ESTE...
            for k in range (0,len(nodosConectados)):
                re=Relacion(nodosNoConectados[i],nodosConectados[k])
                if re.distancia<self.distancia*2:
                    listaAux.append(re)
            print('hay '+str(len(listaAux))+' puntos a menos de 40 km')
            listaAux.sort(key=lambda x: x.distancia,reverse=False)
            ###################...POR ESTE
            #Factor.alfa([nodosNoConectados[i]],nodosConectados)
            ###################
            for j in range(0,len(listaAux)):
                b=self.dePuntoAPoligono(listaAux[j].puntoFinal)
                c=c.intersection(b)
                if c.wkt != 'GEOMETRYCOLLECTION EMPTY':
                    x=mapping(c)
                    self.impresora.deWktAKml(listaAux[j].puntoInicial.nombre+'-'+listaAux[j].puntoFinal.nombre,x)
                    print(str(i)+'-'+str(j)+' se encontro un area donde se puede poner un repetidor.')           
                    break
                else:
                    c=cAux
                    print('{}-{} estan a menos de {} km pero no se intersectan, prueba de nuevo...'.format(i,j,self.distancia*2))
            print('Siguiente nodo no conectado.')
            print()
            
            

    def interface(self):
        nodosNoConectados = self.secretaria.ordenameInput2(self.lugarConectado)
        nodosConectados = self.secretaria.ordenameInput2(self.lugarNoConectado)
        b=0
        while b<6:
            b=b+1
            a=input('OPCIONES\n1 {}\n2 {}\n: '.format(self.lugarConectado,self.lugarNoConectado))
            if a=='1':
                a=input('{} ubigeo?: '.format(self.lugarConectado))
                try:
                    c = next(filter(lambda x: x.ubigeo == int(a),nodosNoConectados))
                    c=self.dePuntoAPoligono(c)
                    x=mapping(c)
                    self.impresora.deWktAKml('ver',x)
                except:
                    print('ingresaste mal.')
            elif a=='2':
                a=input('{} ubigeo?: '.format(self.lugarNoConectado))
                try:
                    c = next(filter(lambda x: x.ubigeo == int(a),nodosConectados))
                    c=self.dePuntoAPoligono(c)
                    x=mapping(c)
                    self.impresora.deWktAKml('ver',x)
                except:
                    print('ingresaste mal.')
            else:
                print('intenta de nuevo')
                
    # =================================================================================================
    
    
if __name__=="__main__":
    Factor.generaBases()
    #GRAFICA PUNTOS
    '''
    jefe=Jefe(numeroDeLDV=300,muestras=300,distancia=4,alturaTorreFantasma=30,lugarConectado=Factor.archivo_trans,lugarNoConectado=Factor.archivo_acces)
    jefe.funcionFinal0(Factor.archivo_trans)
    jefe.funcionFinal0(Factor.archivo_acces)
    '''
    #ACCESO MAS CERCANO A TRANSPORTE EN UN RADIO
    '''
    jefe=Jefe(numeroDeLDV=300,muestras=300,distancia=4,alturaTorreFantasma=30,lugarConectado=Factor.archivo_trans,lugarNoConectado=Factor.archivo_acces)
    jefe.emergencia(Factor.archivo_trans,Factor.archivo_acces)
    '''
    #MANCHA DE DOS EN DOS
    jefe=Jefe(numeroDeLDV=40,muestras=200,distancia=4,alturaTorreFantasma=30,lugarConectado=Factor.archivo_trans,lugarNoConectado=Factor.archivo_acces)
    jefe.hasTodoConInternet()



'''
#jefe.emergencia('transporte','acceso')
print(jefe.ultimaEsperanza('green','resultado'))

'''




'''
sx=Secretaria(Factor.lugarDeTrabajo)
lista=sx.ordenameInput2('aaaa')
dd=Impresora()
internet=Internet()
tec=TecnicoRed()
listaAux=[]
#internet=Internet()
aux=1   

for i in range(0,len(lista)):
    for j in range(aux,len(lista)):
        if lista[i].tipo==lista[j].tipo:
            if(Relacion(lista[i],lista[j]).distancia<3):
                if lista[i].metrosSobreElNivelDelMar <1 or lista[j].metrosSobreElNivelDelMar<1:
                    if (abs(lista[i].metrosSobreElNivelDelMar-lista[j].metrosSobreElNivelDelMar)>4):
                        try:
                            puntosDeElevacion, estado = internet.traerInfoDeAlturas(lista[i], lista[j])
                            if tec.lineaDeVistaConsiderandoFresnel(puntosDeElevacion, lista[i], lista[j]):
                                listaAux.append(Relacion(lista[i],lista[j]))
                        except:
                            print('error')
               
    aux=aux+1

dd.generaKmlRutas(listaAux,'holsss','absolute')   
dd.generaKmlPuntos(lista,'puntos')
'''
'''
herberth pidio analisis de trafico

este programa coge los puntos
analiza trafico. hace comparaciones

condiciones:
celdas del mismo tipo
distancia entre antenas menor a 3 kilometros
diferencia entre celdas mayor a 4 terabits
'''


