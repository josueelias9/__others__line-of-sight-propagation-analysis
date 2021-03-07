from Relacion import Relacion
'''variables globales de esta libreria'''
lugarDeTrabajo = "C:/Users/DELLL/Desktop/borra/"
miBaseT = '''transporte1;1;-78.426652;-6.884226;15.0;transporte;0;
transporte2;2;-78.438926;-6.900705;15.0;transporte;0;
transporte3;3;-78.454004;-6.937299;15.0;transporte;0;'''
miBaseA = '''acceso1;1;-78.397267;-6.898882;15.0;acceso;0;
acceso2;2;-78.424352;-6.893104;15.0;acceso;0;
acceso3;3;-78.420674;-6.922061;15.0;acceso;0;
acceso4;4;-78.447779;-6.890579;15.0;acceso;0;
acceso5;5;-78.461209;-6.886364;15.0;acceso;0;
acceso6;6;-78.455400;-6.918098;15.0;acceso;0;
acceso7;7;-78.477435;-6.914850;15.0;acceso;0;
acceso8;8;-78.504492;-6.901809;15.0;acceso;0;
acceso9;9;-78.431883;-6.915703;15.0;acceso;0;
acceso10;10;-78.436611;-6.895702;15.0;acceso;0;'''
nombreArchivoTrans = 'uno' #nombre del archivo de entrada
nombreArchivoAcces = 'dos' #nombre del archivo de entrada
''''''

def generaBases():
    fT = open(lugarDeTrabajo + nombreArchivoTrans + '.txt', 'w')
    fA = open(lugarDeTrabajo + nombreArchivoAcces + '.txt', 'w')
    fT.write(miBaseT)
    fA.write(miBaseA)
    fT.close()
    fA.close()

def deGradosAKilometros(grados):
    return grados*111.11

def deKilometrosAGrados(kilometros):
    return kilometros/111.11

def buscaPuntosQueCumplanCondicion(lista1:list,distancia:int):
    '''
    esta funcion hace lo siguiente: regresa una lista con puntos que cumplen la condicion
    de estar a menos de "distancia" kilometros. Esta condicion se cumple entre todos los 
    puntos de la lista que se retorna.
    '''
    listaQueCumpleCondicion=[]
    listaQueCumpleCondicion.append(lista1[0])
    for i in range(1,len(lista1)):
        bandera=True
        for j in range(0,len(listaQueCumpleCondicion)):
            print(j)
            if Relacion(listaQueCumpleCondicion[j],lista1[i]).distancia > distancia:
                bandera=False
                break
        if bandera==True:
            listaQueCumpleCondicion.append(lista1[i])
    return listaQueCumpleCondicion

def alfa(nodosNoConectados,nodoConectados):
    '''
    esta funcion pone en una lista los puntos de nodosConectados que estan a menos
    de 40 km
    este metodo escoge de la lista de nodosConectados, los puntos que estan a menos de
    40 km 
    '''
    listaAux=[]
    for i in range(0,len(nodoConectados)):
        flag=True
        for j in range(0,len(nodosNoConectados)):
            if Relacion(nodosNoConectados[j],nodoConectados[i]).distancia>40:
                flag=False
                break
        if flag ==True:
            listaAux.append(nodoConectados)
    listaAux.sort(key=lambda x: x.distancia,reverse=False)
    return listaAux
            

