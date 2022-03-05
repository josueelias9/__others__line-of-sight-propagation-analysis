# -*- coding: utf-8 -*-
"""
Created on Thu May 24 03:35:26 2018

@author: Josue
"""

class Poligonito:
    def __init__(self):
        self.verticeInicial=[]
        self.finDelPoligono=False
        self.listaDePuntosDelGranPoligono=[]
        self.aux=0
        
    def __str__(self):
        return 'esto es una prueba'
        
    def verSiSeLlegoAlFinalDelPoligonito(self,lista:list):
        for i in range (0,len(lista)):
            self.listaDePuntosDelGranPoligono.append(lista[i])
            if lista[i][0]==self.verticeInicial[0] and lista[i][1]==self.verticeInicial[1]:
                self.aux = self.aux + 1
                if self.aux == 2:
                    self.finDelPoligono=True
                    return
        return