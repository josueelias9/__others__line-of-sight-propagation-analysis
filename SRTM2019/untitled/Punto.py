'''
crear clase punto mas general y que tenga menos atributos
class Punto(self,longitud,latitud):
    self.latitud = latitud              #coordenadas
    self.longitud = longitud            #coordenadas
'''

class Punto:#class PuntoRadionelace(Punto):

    def __init__(self, nombre:str, ubigeo:int, longitud:float, latitud:float, alturaAntena:float, tipo:str, metrosSobreElNivelDelMar:float):
        self.nombre = nombre
        self.ubigeo = ubigeo                #numero ID
        self.longitud = longitud            #coordenadas
        self.latitud = latitud              #coordenadas
        self.alturaAntena = alturaAntena    #metros
        self.tipo = tipo
        self.metrosSobreElNivelDelMar = metrosSobreElNivelDelMar #metros
        self.greenAsociado = ''

    def __str__(self):
        return 'MsgPunto: alturaAntena:{4}\tmsnm:{6}\tlongitud:{2}\tlatitud:{3}\tnombre:{0}'.format(self.nombre,self.ubigeo,self.longitud,self.latitud,self.alturaAntena,self.tipo,self.metrosSobreElNivelDelMar)


if __name__=="__main__":
    punto=Punto('nombre',4,-76.134,-8.6424,20,'tipo',2341)
    print(punto)