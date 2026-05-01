from Punto import Punto
from Relacion import Relacion

class Secretaria:
    '''
    es la que organiza la informacion de entrada
    '''
    def __init__(self,ruta):
        self.ruta=ruta
        self.listaAcc = []
        self.listaAccCone = []
        self.listaFinal = []
        self.listaFuera = []

    def encuentraPuntosFuera(self, listaDeConectados:list,listaDeTodos:list)->list:
        '''
        Segun decia en otro lado esta funcion no sirve.
        Ver si no sirve.
        :param listaDeConectados:
        :param listaDeTodos:
        :return:
        '''
        listaFuera = []
        for i in range(0, len(listaDeTodos)):
            flag = True
            for j in range(0, len(listaDeConectados)):
                if listaDeTodos[i].codigo == listaDeConectados[j].codigo and listaDeTodos[i].tipo == listaDeConectados[j].tipo:
                    flag = False
                    break
            if flag:
                listaFuera.append(listaDeTodos[i])
        return listaFuera

    def funcion(self,archivo1:str,archivo2:str):
        '''
        esta funcion sirve para comparar una lista con otra y
        da como resultado elementos NO repetidos
        '''
        f = open(self.ruta + archivo1+'.txt', 'r')
        for line in f:
            lista = line.split(';')
            lista[6] = lista[6].strip()
            self.listaAcc.append(Punto(lista[0], int(lista[1]), float(lista[2]), float(lista[3]), float(lista[4]), lista[5], float(lista[6])))

        f = open(self.ruta + archivo2+'.txt', 'r')
        for line in f:
            lista = line.split(';')
            lista[6] = lista[6].strip()
            self.listaAccCone.append(Punto(lista[0], int(lista[1]), float(lista[2]), float(lista[3]), float(lista[4]), lista[5], float(lista[6])))

        for i in range(0, len(self.listaAcc)):
            flag = True
            for j in range(0, len(self.listaAccCone)):
                if self.listaAcc[i].ubigeo == self.listaAccCone[j].ubigeo:
                    flag = False
            if flag:
                self.listaFuera.append(self.listaAcc[i])

        alfa = open(self.ruta + 'fuera.txt', 'w')
        for i in range(0, len(self.listaFuera)):
            alfa.write(self.listaFuera[i].nombre + ';' + str(self.listaFuera[i].ubigeo) + ';' + str(self.listaFuera[i].longitud) + ';' + str(self.listaFuera[i].latitud) + ';' + str(self.listaFuera[i].alturaAntena) + ';' + self.listaFuera[i].tipo + ';' + str(self.listaFuera[i].metrosSobreElNivelDelMar) + '\n')

    def ordenameInput2(self,nombreDelArchivoALeer:str)->(list):
        '''
        -esta funcion ordena datos de una grupo de puntos
        -lee archivo separado por comas
        -7 elementos
        -separa los siete elementos del archivo separado por comas y lo pone en una lista de objetos "Punto"
        :return:
        '''
        listaAcc=[]
        aux=0
        with open(self.ruta + nombreDelArchivoALeer+'.txt') as inputfile:
            for line in inputfile:
                #print(aux)
                aux=aux+1
                linea = line.split(';')
                linea[3] = linea[3].strip()
                listaAcc.append(Punto(linea[0], int(linea[1]), float(linea[2]), float(linea[3]), float(linea[4]), linea[5], float(linea[6])))
                print('MsgSecretaria: Interacion: {}'.format(aux))
        return listaAcc

    def leeListaDeRutas(self,nombreDelArchivoALeer:str)->(list):
        '''
        :return:
        '''
        listadeRelaciones=[]
        with open(self.ruta + nombreDelArchivoALeer+'.txt') as inputfile:
            for line in inputfile:
                linea = line.split(';')
                linea[3] = linea[3].strip()
                punto1=Punto(linea[0], int(linea[1]), float(linea[2]), float(linea[ 3]), float(linea[ 4]), linea[ 5], float(linea[ 6]))
                punto2=Punto(linea[7], int(linea[8]), float(linea[9]), float(linea[10]), float(linea[11]), linea[12], float(linea[13]))
                re=Relacion(punto1,punto2)
                listadeRelaciones.append(re)
        return listadeRelaciones