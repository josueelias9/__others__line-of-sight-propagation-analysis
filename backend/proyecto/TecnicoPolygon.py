# -*- coding: utf-8 -*-
"""
Created on Tue May 29 04:32:14 2018

@author: Josue
"""
from Poligonos import Poligonos
from Poligonito import Poligonito
from Estructura import Estructura
from shapely.geometry.polygon import LinearRing, Polygon,Point
import shapely.geometry as sg
import shapely.ops as so

class TecnicoPolygon:
    '''
    especialista en trabajar con la clase polygon
    '''
    def omar(self):
        c=Polygon(((-84,-20),(-84,0),(-60,0),(-60,-84),(-84,-20)))
        c.contains(Point(0.5, 0.5))
        
    
    def funcion(self,listaDePoligonos:list,listaDeEstructuras:list):
        c=Polygon(((-84,-20),(-84,0),(-60,0),(-60,-84),(-84,-20)))
        cAux=c
        for i in range(0,len(listaDePoligonos)):
            b=self.tecnicoPolygon.paraPoligonos(listaDePoligonos[i],miEst)
            self.impresora.funcion(poligonos,est.myEstructura)
            c=c.intersection(b)
            if c.wkt=='GEOMETRYCOLLECTION EMPTY':
                print("no coincide prr "+listaDePuntos[i].nombre)
                c=cAux
            else:
                print("bien "+listaDePuntos[i].nombre)
                cAux=c                           
        self.impresora.generaTxtDeWkt(c.wkt,'pruebaaaaa')
        
        
        
    def funcion2(self,listaConectados,listaNoConectados):
        c=Polygon(((-84,-20),(-84,0),(-60,0),(-60,-84),(-84,-20)))
        cAux=c
        c=listaNoConectados[i]
        for i in range(0,len(listaNoConectados)):
            for j in range(0,len(listaConectados)):    
                c=c.intersection(listaConectados[j])
                if c.wkt != 'GEOMETRYCOLLECTION EMPTY':
                    break
            self.impresora.generaTxtDeWkt(c.wkt,str(i))
            
if __name__=="__main__":
    tec=TecnicoPolygon()
    tec.omar()
    print('modificar esto wuey')