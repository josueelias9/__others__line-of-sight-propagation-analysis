# -*- coding: utf-8 -*-
"""
Created on Thu May 24 11:54:21 2018

@author: Josue
"""
import math
from Punto import Punto

class Estructura:
    def __str__(self):
        return 'hola'

    def __init__(self,n,m,r,puntoCero:Punto,alturaTorreFantasma):
        self.n=n    #NUMERO DE LADOS
        self.m=m    #NUMERO DE MUESTRAS
        self.r=r    #RADIO
        self.puntoCero=puntoCero
        self.alturaTorreFantasma=alturaTorreFantasma
        self.a=r/(self.m-1)
        self.alfa = math.pi * 2 / self.n
        self.teta = self.alfa/2
        self.b=self.a*(1/math.cos(self.teta))
        self.auxAngulo = 0
        ########## matrices. Todas tienen el mismo tamaño        
        self.estructuraLineaDeVista = []
        self.estructuraFigurasGeome = []
        self.estructuraMatricial = []
        '''
        estructuraLineaDeVista = matriz de puntos que se asocia a la ubicacion de las torres fantasmas
        estructuraFigurasGeome = matriz de puntos que se asicia con los vertices de los poligonos generados
        estructuraMatricial    = matriz de int (0,1,2,3,4,5) que se asocia a la propiedad "linea de vista con esta torre fantasma"
            0 = no hay linea de vista
            1 = hay linea de vista
            2 = primera deteccion de 1
            3 = segunda deteccion de 1
            4 = primera deteccion de 0
            5 = segunda deteccion de 0
        '''
        ########## funciones de inicializacion
        self.puntosLineaDeVista()#inicializa estructuraLineaDeVista
        self.puntosPoligonos()#inicializa estructuraFigurasGeome
        self.inicializaMatrizEstructuraMatricial()#inicializa estructuraMatricial
        
    def inicializaMatrizEstructuraMatricial(self):
        for i in range(self.n):
            lista=[]
            for j in range(self.m):
                lista.append(1)
            self.estructuraMatricial.append(lista)
            
    def puntosLineaDeVista(self):
        self.auxAngulo = 0
        for i in range(0,self.n):#n veces, de 0 a n-1
            listaAux=[]
            for j in range(0,self.m):#m veces, de 0 a m-1
                xI = self.puntoCero.longitud + math.cos(self.auxAngulo)*self.a*j
                yI = self.puntoCero.latitud + math.sin(self.auxAngulo)*self.a*j
                listaAux.append(Punto('',0,xI,yI,0,'',0))
            self.estructuraLineaDeVista.append(listaAux)
            self.auxAngulo = self.auxAngulo + self.alfa

    def puntosPoligonos(self):
        self.auxAngulo = -self.teta
        for i in range(0,self.n):#n veces, de 0 a n-1
            listaAux=[]
            for j in range(0,self.m):#m veces, de 0 a m-1
                xI = self.puntoCero.longitud + math.cos(self.auxAngulo)*self.b*(j+1/2)
                yI = self.puntoCero.latitud + math.sin(self.auxAngulo)*self.b*(j+1/2)
                listaAux.append(Punto('',0,xI,yI,0,'',0))
            self.estructuraFigurasGeome.append(listaAux)
            self.auxAngulo = self.auxAngulo + self.alfa

        
if __name__=="__main__":
    from Impresora import Impresora
    import Factor
    lados = 20
    muestras = 20
    distanciaEnGrados = Factor.deKilometrosAGrados(10)
    punto = Punto('', 25, -71.318626, -16.556727, 20.0, '', 3341.13110351562)
    alturaTorreFantasma = 20
    
    est = Estructura(lados, muestras, distanciaEnGrados, punto, alturaTorreFantasma)
    imp = Impresora(Factor.lugarDeTrabajo)
    
    imp.hacerMallaSegunEstructuraMatricial('h222', est)
    imp.ploteadorDeMatriz(est.estructuraMatricial)