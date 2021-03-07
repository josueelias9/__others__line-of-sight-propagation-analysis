from Punto import Punto
import math

class Relacion:
    
    def __init__(self, puntoInicial:Punto, puntoFinal:Punto):
        self.puntoInicial = puntoInicial
        self.puntoFinal = puntoFinal
        self.ditancia=0 #en kilometros
        self.distanciaEntrePuntos()

    def __str__(self):
        relacion = '{}\t{}\t{}'.format(self.puntoInicial.nombre,self.puntoFinal.nombre,self.distancia)
        return relacion
    
    def distanciaEntrePuntos(self):
        '''
        devuelve la distancia en kilometros
        '''
        y_0 = self.puntoInicial.longitud * 111.11 
        x_0 = self.puntoInicial.latitud * 111.11
        h_0 = self.puntoInicial.alturaAntena + self.puntoInicial.metrosSobreElNivelDelMar
        y_f = self.puntoFinal.longitud * 111.11
        x_f = self.puntoFinal.latitud * 111.11
        h_f = self.puntoFinal.alturaAntena + self.puntoFinal.metrosSobreElNivelDelMar
        self.distancia = math.sqrt((y_f - y_0) ** 2 + (x_f - x_0) ** 2) #OJO! ... la distancia esta en kilometros
