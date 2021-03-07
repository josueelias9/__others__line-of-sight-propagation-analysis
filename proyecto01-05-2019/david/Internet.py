import json
import urllib.request
from Punto import Punto
import math
from Relacion import Relacion
import Factor
#====================== solo para rtsm
import srtm
from geohelper import distance
elevation_data = srtm.get_data()
#======================

class Internet:

    def __init__(self,a):
        self.samples=a
    
    def traerInfoDeAlturas(self, puntoInicial:Punto, puntoFinal:Punto)->(list, str):
        alturas = []
        path_str = str(puntoInicial.latitud) + ',' + str(puntoInicial.longitud) + '|' + str(puntoFinal.latitud) + ',' + str(puntoFinal.longitud)
        url = 'https://maps.googleapis.com/maps/api/elevation/json?key=AIzaSyCmtdVdS71cvhCAMq4LM38fFqTLwq3zy9U&path=' + path_str + '&samples=' + str(self.samples)
        print(url)
        datos = urllib.request.urlopen(url)
        w = datos.read().decode("utf-8")
        q = json.loads(w)
        for k in range(0, len(q['results'])):
            alturas.append(q['results'][k]['elevation'])
        return alturas, q['status']

    def traerInfoDePuntos(self, puntoInicial:Punto, puntoFinal:Punto)->(list, str):
        puntos = []
        path_str = str(puntoInicial.latitud) + ',' + str(puntoInicial.longitud) + '|' + str(puntoFinal.latitud) + ',' + str(puntoFinal.longitud)
        url = 'https://maps.googleapis.com/maps/api/elevation/json?key=AIzaSyCmtdVdS71cvhCAMq4LM38fFqTLwq3zy9U&path=' + path_str + '&samples=' + str(self.samples)
        datos = urllib.request.urlopen(url)
        w = datos.read().decode("utf-8")
        q = json.loads(w)
        for k in range(0, len(q['results'])):
            punto = Punto('', 0, float(q['results'][k]['location']['lng']), float(q['results'][k]['location']['lat']),0,'', float(q['results'][k]['elevation']))
            puntos.append(punto)
        return puntos, q['status']
    
    def consigueDatoDeAlturaDeUnSoloPunto(self, punto:Punto)->(str, str):
        url = 'https://maps.googleapis.com/maps/api/elevation/json?key=AIzaSyCmtdVdS71cvhCAMq4LM38fFqTLwq3zy9U&locations='+str(punto.latitud) + ',' + str(punto.longitud)
        try:
            datos = urllib.request.urlopen(url)
            w = datos.read().decode("utf-8")

            q = json.loads(w)
            punto.metrosSobreElNivelDelMar = float(q['results'][0]['elevation'])
        except Exception as e:
            print(e)
    
            
            
    '''
    def consigueDatoDeAlturaDeUnSoloPunto(self, punto:Punto)->(str, str):
        x_i=punto.longitud
        y_i=punto.latitud
        altura = elevation_data.get_elevation(y_i, x_i)
        if altura ==None:
            punto.metrosSobreElNivelDelMar = float(0)
            print('MsgInternet:Como altura es None, le asignamos 0 metros')
        else:
            punto.metrosSobreElNivelDelMar = float(altura)
    


    
    def traerInfoDeAlturas(self,puntoInicial:Punto,puntoFinal:Punto):
        lista=[]
        alturaAux=0
        y_f=puntoFinal.latitud
        y_0=puntoInicial.latitud
        x_f=puntoFinal.longitud
        x_0=puntoInicial.longitud
        x_i=0
        y_i=0
        dividendo=y_f-y_0
        divisor=x_f-x_0
        factor=(x_f-x_0)/(self.samples-1)
        if divisor==0:
            #print('MsgInternet: Cuidado! division entre 0')
            factor=(y_f-y_0)/(self.samples-1)
            m=divisor/dividendo
            for i in range(0,self.samples):
                y_i=(factor*i)+y_0
                x_i=m*(y_i-y_0)+x_0
                #print('MsgInternet: este es x_i {} y este es y_i {}'.format(x_i,y_i)) 
                altura = elevation_data.get_elevation(y_i,x_i)
                if altura==None:
                    altura=alturaAux
                else:
                    alturaAux=altura
                lista.append(altura)
        else:
            factor=(x_f-x_0)/(self.samples-1)
            m=dividendo/divisor
            for i in range(0,self.samples):
                x_i=(factor*i)+x_0
                y_i=m*(x_i-x_0)+y_0
                #print(str(x_i)+'\t'+str(y_i)) 
                altura = elevation_data.get_elevation(y_i, x_i)
                if altura==None:
                    altura=alturaAux
                else:
                    alturaAux=altura
                lista.append(altura)
        #print(lista)
        return lista,'alturas'


    
    def traerInfoDePuntos(self,puntoInicial:Punto,puntoFinal:Punto):
        lista=[]
        alturaAux=0
        y_f=puntoFinal.latitud
        y_0=puntoInicial.latitud
        x_f=puntoFinal.longitud
        x_0=puntoInicial.longitud
        x_i=0
        y_i=0
        dividendo=y_f-y_0
        divisor=x_f-x_0
        factor=(x_f-x_0)/(self.samples-1)
        if divisor==0:
            #print('MsgInternet: Cuidado! division entre 0')
            factor=(y_f-y_0)/(self.samples-1)
            m=divisor/dividendo
            for i in range(0,self.samples):
                y_i=(factor*i)+y_0
                x_i=m*(y_i-y_0)+x_0
                #print('MsgInternet: este es x_i {} y este es y_i {}'.format(x_i,y_i)) 
                altura = elevation_data.get_elevation(y_i,x_i)
                if altura==None:
                    altura=alturaAux
                else:
                    alturaAux=altura
                punto=Punto('',0,x_i,y_i,0,'',altura)
                lista.append(punto)
        else:
            factor=(x_f-x_0)/(self.samples-1)
            m=dividendo/divisor
            for i in range(0,self.samples):
                x_i=(factor*i)+x_0
                y_i=m*(x_i-x_0)+y_0
                #print('MsgInternet: este es x_i {} y este es y_i {}'.format(x_i,y_i)) 
                altura = elevation_data.get_elevation(y_i, x_i)
                if altura==None:
                    altura=alturaAux
                else:
                    alturaAux=altura
                punto=Punto('',0,x_i,y_i,0,'',altura)
                lista.append(punto)
        return lista,'puntos'
    
    
    '''
    
if __name__=="__main__":
    from Punto import Punto
    from Secretaria import Secretaria
    from Impresora import Impresora

    sec=Secretaria(Factor.lugarDeTrabajo)
    imp=Impresora(Factor.lugarDeTrabajo)
    lonIn=0
    latIn=0
    punto1=Punto('',0,lonIn,latIn,20,'',0)
    punto2=Punto('',0,lonIn,latIn+.4,20,'',0)
    inter=Internet(5)
    
    (a,b)=inter.traerInfoDePuntos(punto1,punto2)
    for i in range(0,len(a)):
        print(a[i])
    
    imp.generaKmlPuntos(a,'borrmeRapido')

    