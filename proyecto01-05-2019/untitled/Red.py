# -*- coding: utf-8 -*-
"""
Created on Mon May 28 12:25:56 2018

@author: Josue
"""
from Punto import Punto

class Red:
    
    def __init__(self,conectado=False,listaDeRelaciones=[],listaDeNodos=[],key=0):
        if key!=int(key):
            key=0
        if conectado!=bool(conectado):
            conectado=False
        if listaDeRelaciones!=list(listaDeRelaciones):
            listaDeRelaciones=[]
        self.conectado=conectado
        self.listaDeRelaciones=listaDeRelaciones
        self.listaDeNodos=listaDeNodos
        self.key=key
        '''
        esta clase representa una red
        
        id: id de mi red
        nodos: lista de nodos conectados
        radioenlaces: lista de relaciones de radioenlaces
        distanciaMax: distancia maxima de radioenlace en kilomentros
        infoAdicional: informacion adicional de la red
        listaDeSubredes: lista de subredes
        '''
    
    def __str__(self):
        texto = '''
        conectado = {}
        id = {}'''.format(self.conectado,self.key)
        return texto
        
if __name__=="__main__":
    red=Red()
    print(red)