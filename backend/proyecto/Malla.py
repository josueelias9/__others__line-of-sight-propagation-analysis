from Punto import Punto
from Impresora import Impresora
from Relacion import Relacion
import Factor

class Malla:
    '''
    Esta clase la hice porque queria dejar la proyeccion polar e
    intentar un proyeccion cartesiana para asi tener figuar cuadradas 
    en vez de poligonos complejos.
    
    Se trata de una malla, como su mismo nombre infiere.
    '''
    def __init__(self,distanciaKilometrosX,distanciaKilometrosY,puntoInicial):
        self.numeroDeFilas=10
        self.numeroDeColumnas=10
        self.distanciaKilometrosX=distanciaKilometrosX
        self.distanciaKilometrosY=distanciaKilometrosY
        self.punto  =puntoInicial
        self.puntoX =Punto('', 0, self.punto.longitud+Factor.deKilometrosAGrados(self.distanciaKilometrosX), self.punto.latitud, 0, '', 0)
        self.puntoY =Punto('', 0, self.punto.longitud, self.punto.latitud+Factor.deKilometrosAGrados(self.distanciaKilometrosY), 0, '', 0)
        self.puntoXY=Punto('', 0, self.punto.longitud+Factor.deKilometrosAGrados(self.distanciaKilometrosX), self.punto.latitud+Factor.deKilometrosAGrados(self.distanciaKilometrosY), 0, '', 0)
        self.impresora=Impresora(Factor.lugarDeTrabajo)
        self.pasosEnX=self.distanciaKilometrosX/(self.numeroDeColumnas-1)
        self.pasosEnY=self.distanciaKilometrosY/(self.numeroDeFilas-1)
        self.matriz=[]


    def llenaMatriz(self):
        for j in range(0,self.numeroDeFilas):
            lista = []
            for i in range(0,self.numeroDeColumnas):
                punto = Punto('', 0, self.punto.longitud + Factor.deKilometrosAGrados(self.pasosEnX)*i, self.punto.latitud + Factor.deKilometrosAGrados(self.pasosEnY)*j, 0, '', 0)
                lista.append(punto)
            self.matriz.append(lista)
        print(self.matriz)

        lista2=[]
        for i in range(0,len(self.matriz)):
            for j in range(0,len(self.matriz[i])):
                lista2.append(self.matriz[i][j])
        self.impresora.generaKmlPuntos(lista2,'eeee')


    def imprimeVertices(self):
        lista = [self.punto, self.puntoX, self.puntoY, self.puntoXY]
        self.impresora.generaKmlPuntos(lista, 'hola')

    def macro(self):
        self.imprimeVertices()
        self.llenaMatriz()
        pass

if __name__=="__main__":
    punto  =Punto('', 0,-72.351042,-15.542516, 0, '', 0)
    malla=Malla(4,4,punto)
    malla.macro()