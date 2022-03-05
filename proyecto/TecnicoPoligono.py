from Poligonito import Poligonito
from Estructura import Estructura
from Poligonos import Poligonos
from Internet import Internet
from shapely.geometry.polygon import Polygon

class TecnicoPoligono:
    # for i in range(a0,a1) = a1-a0 veces, de a0 a a1-1
    def __str__(self):
        return 'Josue Huaman'

    def __init__(self,miEstructura:Estructura,muestras):
        self.inter=Internet(muestras)
        self.myEstructura=miEstructura
        self.noHagasDobleTrabajoI=0
        self.noHagasDobleTrabajoJ=-1
 
    # ===================================================================== CALCULOS
    # ======================= PARTE LINEA DE VISTA
    def llenaEstructuraMatricial(self):
        for i in range(0, self.myEstructura.n):#n veces, de 0 a n-1 (7 veces, de 0 a 6)
            #print('MsgTecnicoPoligono: iteracion {}'.format(i))
            lista, b = self.inter.traerInfoDeAlturas(self.myEstructura.puntoCero, self.myEstructura.estructuraLineaDeVista[i][self.myEstructura.m - 1])
                
            #print(0'MsgTecnicoPoligono:{}-{}'.format(i,j))
            for j in range(0, self.myEstructura.m):#m veces, de 0 a m-1 (4 veces, de 0 a 3)
                y_0 = lista[0] + self.myEstructura.puntoCero.alturaAntena
                x_0 = 0
                y_f = lista[j] + self.myEstructura.alturaTorreFantasma
                x_f = j
                for k in range(0,j):#j veces, de 0 a j-1
                    x_i = k
                    y_i = ((y_f - y_0) / (x_f - x_0)) * (x_i - x_0) + y_0
                    if y_i < lista[k]:
                        self.myEstructura.estructuraMatricial[i][j]=0
                        break
        #2 AUMENTE ESTO
        for i in range(0,len(self.myEstructura.estructuraMatricial)):
            self.myEstructura.estructuraMatricial[i][0]=0
        #2
    # ======================= PARTE LINEA HAS POLIGONO UNICO
    '''
    funcionDetectaUnos  ------->    cierraPoligono
                        <-------
    funcionDetectaUnos  ------->    hayProblemaDiagonal
                        <-------
    '''
    def funcionDetectaUnos(self,i,j):
        '''
        Busca en la matriz "estructuraMatricial" todos los "1s" que
        pueden pertenecer a un poligono (que no viole las premisas de
        poligonos que establecimos)
        :param i:
        :param j:
        :return:
        '''
        #CREANDO LISTAS
        lista2 = []
        lista1a2 = []
        listaAux = []
        if self.myEstructura.estructuraMatricial[i][j] == 1:
            lista2.append([i,j])
            self.myEstructura.estructuraMatricial[i][j] = 2
            listaAux.append([i, j])
        while not len(lista2)==0:
            for k in range(0,len(lista2)):
                a0=lista2[k][0]
                a1=lista2[k][1]
                ################## POR SI SE SALE DE LOS LIMITES DE LA MATRIZ
                if a0+1==self.myEstructura.n:
                    arriba=0
                else:
                    arriba = self.myEstructura.estructuraMatricial[a0 + 1][a1]
                if a1+1==self.myEstructura.m:
                    derecha=0
                else:
                    derecha = self.myEstructura.estructuraMatricial[a0][a1 + 1]
                if a0-1==-1:
                    abajo=0
                else:
                    abajo = self.myEstructura.estructuraMatricial[a0 - 1][a1]
                if a1-1==-1:
                    izquierda=0
                else:
                    izquierda = self.myEstructura.estructuraMatricial[a0][a1 - 1]
                ##################
                if arriba==1 or abajo==1 or derecha==1 or izquierda==1:
                    if arriba == 1 and self.cierraPoligono(a0+1,a1)==False and self.hayProblemaDiagonal(a0+1,a1)==False:
                        self.myEstructura.estructuraMatricial[a0+1][a1]=2
                        lista1a2.append([a0+1,a1])
                        listaAux.append([a0+1,a1])
                    if abajo == 1 and self.cierraPoligono(a0-1, a1) == False and self.hayProblemaDiagonal(a0-1,a1)==False:
                        self.myEstructura.estructuraMatricial[a0 - 1][a1] = 2
                        lista1a2.append([a0-1,a1])
                        listaAux.append([a0-1,a1])
                    if derecha == 1 and self.cierraPoligono(a0, a1+1) == False and self.hayProblemaDiagonal(a0,a1+1)==False:
                        self.myEstructura.estructuraMatricial[a0][a1+1] = 2
                        lista1a2.append([a0,a1+1])
                        listaAux.append([a0,a1+1])
                    if izquierda == 1 and self.cierraPoligono(a0, a1-1) == False and self.hayProblemaDiagonal(a0,a1-1)==False:
                        self.myEstructura.estructuraMatricial[a0][a1-1] = 2
                        lista1a2.append([a0,a1-1])
                        listaAux.append([a0,a1-1])
                    self.myEstructura.estructuraMatricial[a0][a1]=3
                else:
                    self.myEstructura.estructuraMatricial[a0][a1]=3
            ##################
            lista2=lista1a2
            lista1a2=[]
        return listaAux

    def robot(self,i,j):
        #CREANDO LISTAS
        lista4 = []
        lista0a4 = []
        listaAux=[]
        if i==self.myEstructura.n:
            return True
        if j==self.myEstructura.m:
            return True
        if self.myEstructura.estructuraMatricial[i][j] == 0:
            lista4.append([i,j])
            self.myEstructura.estructuraMatricial[i][j] = 4
            listaAux.append([i,j])
        while not len(lista4)==0:
            for k in range(0,len(lista4)):
                a0=lista4[k][0]
                a1=lista4[k][1]
                ################## POR SI SE SALE DE LOS LIMITES DE LA MATRIZ
                if a0+1==self.myEstructura.n:
                    self.limpiador(listaAux,0)
                    return True
                else:
                    arriba = self.myEstructura.estructuraMatricial[a0 + 1][a1]
                if a1+1==self.myEstructura.m:
                    self.limpiador(listaAux, 0)
                    return True
                else:
                    derecha = self.myEstructura.estructuraMatricial[a0][a1 + 1]
                if a0-1==-1:
                    self.limpiador(listaAux, 0)
                    return True
                else:
                    abajo = self.myEstructura.estructuraMatricial[a0 - 1][a1]
                if a1-1==-1:
                    self.limpiador(listaAux, 0)
                    return True
                else:
                    izquierda = self.myEstructura.estructuraMatricial[a0][a1 - 1]
                ##################
                if arriba==0 or abajo==0 or derecha==0 or izquierda==0:
                    if arriba == 0:
                        self.myEstructura.estructuraMatricial[a0+1][a1]=4
                        lista0a4.append([a0+1,a1])
                        listaAux.append([a0+1,a1])
                    if abajo == 0:
                        self.myEstructura.estructuraMatricial[a0 - 1][a1] = 4
                        lista0a4.append([a0-1,a1])
                        listaAux.append([a0-1,a1])
                    if derecha == 0:
                        self.myEstructura.estructuraMatricial[a0][a1+1] = 4
                        lista0a4.append([a0,a1+1])
                        listaAux.append([a0,a1+1])
                    if izquierda == 0:
                        self.myEstructura.estructuraMatricial[a0][a1-1] = 4
                        lista0a4.append([a0,a1-1])
                        listaAux.append([a0,a1-1])
                    self.myEstructura.estructuraMatricial[a0][a1]=5
                else:
                    self.myEstructura.estructuraMatricial[a0][a1]=5
            ##################
            lista4=lista0a4
            lista0a4=[]
        self.limpiador(listaAux, 0)
        return False

    def maquinaDeEstadosUnosEvolucion3(self):#MAQUINA MEALY
        poligonito=Poligonito()
        ESTADO_INICIAL=0
        ESTADO_IZQUIERDA=1
        ESTADO_DERECHA=2
        ESTADO_ARRIBA=3
        ESTADO_ABAJO=4
        ESTADO_BUSCAR=5
        ESTADO_SUBE=6
        ESTADO_ACTUAL=0
        ESTADO_FINAL=7
        listaBorrarq=[]
        while True:
            # ESTADOS
            ####################################################
            if ESTADO_ACTUAL == ESTADO_INICIAL:
                ###################ACCION DEL ESTADO
                i =  self.noHagasDobleTrabajoI
                j =  self.noHagasDobleTrabajoJ
                ###################CAMBIO DE ESTADO
                ESTADO_ACTUAL = ESTADO_BUSCAR
            ####################################################
            elif ESTADO_ACTUAL == ESTADO_BUSCAR:
                ###################ACCION DEL ESTADO
                j = j + 1
                ###################CAMBIO DE ESTADO
                if j + 1 == self.myEstructura.m:
                    ESTADO_ACTUAL = ESTADO_SUBE
                elif self.myEstructura.estructuraMatricial[i][j + 1] == 0:
                    ESTADO_ACTUAL = ESTADO_BUSCAR
                elif self.myEstructura.estructuraMatricial[i][j + 1] == 1:
                    poligonito.verticeInicial=[i,j]
                    self.noHagasDobleTrabajoI=i
                    self.noHagasDobleTrabajoJ=j
                    listaBorrarq = self.funcionDetectaUnos(i, j + 1)
                    #========================
                    '''
                    #CODIGO INEFICIENTE
                    if self.pregunta_elPoligonoDaLaVuelta():
                        for p in range(0,len(listaBorrarq)):
                            if listaBorrarq[p][0]>int(self.myEstructura.n/2)-1:
                                self.myEstructura.estructuraMatricial[listaBorrarq[p][0]][listaBorrarq[p][1]]=1
                        a=len(listaBorrarq)
                        while 0<a:
                            for k in range(0, len(listaBorrarq)):
                                if listaBorrarq[k][0] > int(self.myEstructura.n/2)-1:
                                    del listaBorrarq[k]
                                    break
                            a=a-1
                    '''       
                         
                    #========================
                    #CODIGO EFICIENTE
                    if self.pregunta_elPoligonoDaLaVuelta():
                        for p in range(0,len(listaBorrarq)):
                            if listaBorrarq[p][0]>int(self.myEstructura.n/2)-1:
                                self.myEstructura.estructuraMatricial[listaBorrarq[p][0]][listaBorrarq[p][1]]=1
                        aux=[]
                        for q in range(0,len(listaBorrarq)):
                            if listaBorrarq[q][0] > int(self.myEstructura.n / 2) - 1:
                                aux.append(q)
                        for k in range(0,len(aux)):
                            del listaBorrarq[aux[len(aux)-1-k]]
                    
                    #========================
                    #GUIA
                    #self.ploteadorDeMatriz(self.estructuraMatricial)
                    ESTADO_ACTUAL = ESTADO_DERECHA
            ####################################################
            elif ESTADO_ACTUAL == ESTADO_SUBE:
                ###################ACCION DEL ESTADO
                i = i + 1
                j = -1
                if i == self.myEstructura.n:
                    return poligonito
                ###################CAMBIO DE ESTADO
                ESTADO_ACTUAL = ESTADO_BUSCAR
            ####################################################
            elif ESTADO_ACTUAL == ESTADO_DERECHA:
                ###################ACCION DEL ESTADO
                j = j + 1
                ###################CALCULANDO CONDICIONANTES
                up = i + 1
                down = i - 1
                right = j + 1
                left = j - 1
                if up == self.myEstructura.n:
                    AR = 0
                else:
                    AR = self.myEstructura.estructuraMatricial[up][j]
                if down == -1:
                    AB = 0
                else:
                    AB = self.myEstructura.estructuraMatricial[down][j]
                if right == self.myEstructura.m:
                    DE = 0
                else:
                    DE = self.myEstructura.estructuraMatricial[i][right]
                if left == -1:
                    IZ = 0
                else:
                    IZ = self.myEstructura.estructuraMatricial[i][left]
                ###################CAMBIO DE ESTADO
                if poligonito.finDelPoligono:
                    ESTADO_ACTUAL = ESTADO_FINAL
                elif AR != 3 and AB != 3 and DE != 3 and IZ != 3:
                    if up == self.myEstructura.n:
                        poligonito.verSiSeLlegoAlFinalDelPoligonito([[i, left], [i, j], [0, j], [0, left], [i, left]])
                    else:
                        poligonito.verSiSeLlegoAlFinalDelPoligonito([[i, left], [i, j], [up, j], [up, left], [i, left]])
                    ESTADO_ACTUAL = ESTADO_FINAL
                elif DE == 3 and AB != 3:
                    poligonito.verSiSeLlegoAlFinalDelPoligonito([[i, left]])
                    ESTADO_ACTUAL = ESTADO_DERECHA
                elif AR != 3 and AB != 3 and DE != 3:
                    if up == self.myEstructura.n:
                        poligonito.verSiSeLlegoAlFinalDelPoligonito([[i, left], [i, j], [0, j]])
                    else:
                        poligonito.verSiSeLlegoAlFinalDelPoligonito([[i, left], [i, j], [up, j]])
                    ESTADO_ACTUAL = ESTADO_IZQUIERDA
                elif DE != 3 and AB != 3:
                    poligonito.verSiSeLlegoAlFinalDelPoligonito([[i, left], [i, j]])
                    ESTADO_ACTUAL = ESTADO_ARRIBA
                elif AB == 3:
                    ESTADO_ACTUAL = ESTADO_ABAJO
            ####################################################
            elif ESTADO_ACTUAL == ESTADO_ABAJO:
                ###################ACCION DE ESTADO
                i = i - 1
                ###################CALCULANDO CONDICIONANTES
                up = i + 1
                down = i - 1
                right = j + 1
                left = j - 1
                if up == self.myEstructura.n:
                    AR = 0
                else:
                    AR = self.myEstructura.estructuraMatricial[up][j]
                if down == -1:
                    AB = 0
                else:
                    AB = self.myEstructura.estructuraMatricial[down][j]
                if right == self.myEstructura.m:
                    DE = 0
                else:
                    DE = self.myEstructura.estructuraMatricial[i][right]
                if left == -1:
                    IZ = 0
                else:
                    IZ = self.myEstructura.estructuraMatricial[i][left]
                ###################
                if poligonito.finDelPoligono:
                    ESTADO_ACTUAL = ESTADO_FINAL
                elif AB == 3 and IZ != 3:
                    poligonito.verSiSeLlegoAlFinalDelPoligonito([[up, left]])
                    ESTADO_ACTUAL = ESTADO_ABAJO
                elif AB != 3 and DE != 3 and IZ != 3:
                    poligonito.verSiSeLlegoAlFinalDelPoligonito([[up, left], [i, left], [i, j]])
                    ESTADO_ACTUAL = ESTADO_ARRIBA
                elif AB != 3 and IZ != 3:
                    poligonito.verSiSeLlegoAlFinalDelPoligonito([[up, left], [i, left]])
                    ESTADO_ACTUAL = ESTADO_DERECHA
                elif IZ == 3:
                    ESTADO_ACTUAL = ESTADO_IZQUIERDA
            ####################################################
            elif ESTADO_ACTUAL == ESTADO_IZQUIERDA:
                ###################ACCION DE ESTADO
                j = j - 1
                ###################CALCULANDO CONDICIONANTES
                up = i + 1
                down = i - 1
                right = j + 1
                left = j - 1
                if up == self.myEstructura.n:
                    AR = 0
                else:
                    AR = self.myEstructura.estructuraMatricial[up][j]
                if down == -1:
                    AB = 0
                else:
                    AB = self.myEstructura.estructuraMatricial[down][j]
                if right == self.myEstructura.m:
                    DE = 0
                else:
                    DE = self.myEstructura.estructuraMatricial[i][right]
                if left == -1:
                    IZ = 0
                else:
                    IZ = self.myEstructura.estructuraMatricial[i][left]
                ###################CAMBIO DE ESTADO
                if poligonito.finDelPoligono:
                    ESTADO_ACTUAL = ESTADO_FINAL
                elif IZ == 3 and AR != 3:
                    if up == self.myEstructura.n:
                        poligonito.verSiSeLlegoAlFinalDelPoligonito([[0, j]])
                    else:
                        poligonito.verSiSeLlegoAlFinalDelPoligonito([[up, j]])
                    ESTADO_ACTUAL = ESTADO_IZQUIERDA
                elif IZ != 3 and AB != 3 and AR != 3:
                    if up == self.myEstructura.n:
                        poligonito.verSiSeLlegoAlFinalDelPoligonito([[0, j], [0, left], [i, left]])
                    else:
                        poligonito.verSiSeLlegoAlFinalDelPoligonito([[up, j], [up, left], [i, left]])
                    ESTADO_ACTUAL = ESTADO_DERECHA
                elif IZ != 3 and AR != 3:
                    if up == self.myEstructura.n:
                        poligonito.verSiSeLlegoAlFinalDelPoligonito([[0, j], [0, left]])
                    else:
                        poligonito.verSiSeLlegoAlFinalDelPoligonito([[up, j], [up, left]])
                    ESTADO_ACTUAL = ESTADO_ABAJO
                elif AR == 3:
                    ESTADO_ACTUAL = ESTADO_ARRIBA
            ####################################################
            elif ESTADO_ACTUAL == ESTADO_ARRIBA:
                ###################ACCION DEL ESTADO
                i = i + 1
                ###################CALCULANDO CONDICIONANTES
                up = i + 1
                down = i - 1
                right = j + 1
                left = j - 1
                if up == self.myEstructura.n:
                    AR = 0
                else:
                    AR = self.myEstructura.estructuraMatricial[up][j]
                if down == -1:
                    AB = 0
                else:
                    AB = self.myEstructura.estructuraMatricial[down][j]
                if right == self.myEstructura.m:
                    DE = 0
                else:
                    DE = self.myEstructura.estructuraMatricial[i][right]
                if left == -1:
                    IZ = 0
                else:
                    IZ = self.myEstructura.estructuraMatricial[i][left]
                ###################CAMBIO DE ESTADO
                if poligonito.finDelPoligono:
                    ESTADO_ACTUAL = ESTADO_FINAL
                elif AR == 3 and DE != 3:
                    poligonito.verSiSeLlegoAlFinalDelPoligonito([[i, j]])
                    ESTADO_ACTUAL = ESTADO_ARRIBA
                elif AR != 3 and DE != 3 and IZ != 3:
                    if up == self.myEstructura.n:
                        poligonito.verSiSeLlegoAlFinalDelPoligonito([[i, j], [0, j], [0, left]])
                    else:
                        poligonito.verSiSeLlegoAlFinalDelPoligonito([[i, j], [up, j], [up, left]])
                    ESTADO_ACTUAL = ESTADO_ABAJO
                elif AR != 3 and DE != 3:
                    if up == self.myEstructura.n:
                        poligonito.verSiSeLlegoAlFinalDelPoligonito([[i, j], [0, j]])
                    else:
                        poligonito.verSiSeLlegoAlFinalDelPoligonito([[i, j], [up, j]])
                    ESTADO_ACTUAL = ESTADO_IZQUIERDA
                elif DE == 3:
                    ESTADO_ACTUAL = ESTADO_DERECHA
            ####################################################
            elif ESTADO_ACTUAL == ESTADO_FINAL:
                break
        self.limpiador(listaBorrarq,0)
        return poligonito


    def limpiador(self,lista,valor):
        for i in range(0, len(lista)):
            self.myEstructura.estructuraMatricial[lista[i][0]][lista[i][1]] = valor

    def cierraPoligono(self,i,j):
        if i+1==self.myEstructura.n:
            arriba=0
        else:
            arriba=self.myEstructura.estructuraMatricial[i+1][j]
        if i-1==-1:
            abajo=0
        else:
            abajo=self.myEstructura.estructuraMatricial[i-1][j]
        if j+1==self.myEstructura.m:
            derecha=0
        else:
            derecha=self.myEstructura.estructuraMatricial[i][j+1]
        if j-1==-1:
            izquierda=0
        else:
            izquierda=self.myEstructura.estructuraMatricial[i][j-1]

        if (arriba==2 or arriba==3) and (abajo==2 or abajo==3) and (derecha==0 or derecha==1) and (izquierda==0 or izquierda==1):
            if self.robot(i,j+1)==False:
                return True
            if self.robot(i,j-1)==False:
                return True
        elif (arriba==0 or arriba==1) and (abajo==0 or abajo==1) and (derecha==2 or derecha==3) and (izquierda==2 or izquierda==3):
            if self.robot(i+1,j)==False:
                return True
            if self.robot(i-1,j)==False:
                return True
        return False

    def hayProblemaDiagonal(self,i,j):
        if i+1==self.myEstructura.n:
            arrib=0
        else:
            arrib=self.myEstructura.estructuraMatricial[i+1][j]
        if i-1==-1:
            abajo=0
        else:
            abajo=self.myEstructura.estructuraMatricial[i-1][j]
        if j+1==self.myEstructura.m:
            derec=0
        else:
            derec=self.myEstructura.estructuraMatricial[i][j+1]
        if j-1==-1:
            izqui=0
        else:
            izqui=self.myEstructura.estructuraMatricial[i][j-1]
        if i+1==self.myEstructura.n or j+1==self.myEstructura.m:
            arrDe=0
        else:
            arrDe=self.myEstructura.estructuraMatricial[i+1][j+1]
        if i+1==self.myEstructura.n or j-1==-1:
            arrIz=0
        else:
            arrIz=self.myEstructura.estructuraMatricial[i+1][j-1]
        if i-1==-1 or j+1==self.myEstructura.m:
            abaDe=0
        else:
            abaDe=self.myEstructura.estructuraMatricial[i-1][j+1]
        if i-1==-1 or j-1==-1:
            abaIz=0
        else:
            abaIz=self.myEstructura.estructuraMatricial[i-1][j-1]

        if abaIz==3 or abaIz==2:
            if not(abajo==3 or abajo==2 or izqui==3 or izqui==2):
                return True
        if arrDe == 3 or arrDe == 2:
            if not(arrib == 3 or arrib== 2 or derec== 3 or derec== 2):
                return True
        if arrIz ==3 or arrIz==2:
            if not(arrib==3 or arrib==2 or izqui==3 or izqui==2):
                return True
        if abaDe==3 or abaDe==2:
            if not(abajo==3 or abajo==2 or derec==3 or derec==2):
                return True
        return False


    def pregunta_elPoligonoDaLaVuelta(self):
        llegaHastaAbajo=False
        llegaHastaArrib=False
        for i in range(0,self.myEstructura.m):
            if self.myEstructura.estructuraMatricial[0][i]==3:
                llegaHastaAbajo=True
            if self.myEstructura.estructuraMatricial[-1][i]==3:
                llegaHastaArrib=True

            if llegaHastaAbajo and llegaHastaArrib:
                #print('si da la vuelta')
                return True
        #print('no da la vuelta')
        return False
    

    # ===================================================================== MACROS pasarlo a __main__
    def funcionMacroSinInternet(self):
        listaTotal=[]
        while True:
            poligono = self.maquinaDeEstadosUnosEvolucion3()
            if len(poligono.listaDePuntosDelGranPoligono)==0:
                break
            listaTotal.append(poligono)
        poligonos=Poligonos()
        poligonos.listaDePoligonitos=listaTotal
        return poligonos
    
    def funcionMacroConInternet(self):
        self.llenaEstructuraMatricial()
        listaTotal=[]
        while True:
            poligono = self.maquinaDeEstadosUnosEvolucion3()
            if len(poligono.listaDePuntosDelGranPoligono)==0:
                break
            listaTotal.append(poligono)
        poligonos=Poligonos()
        poligonos.listaDePoligonitos=listaTotal
        holu=self.paraPoligonos(poligonos)
        return holu
    #===============================================================================
    #===============================================================================
    #===============================================================================
    #===============================================================================
    def paraPoligonos(self,poligonos:Poligonos):
        '''
        return un objeto de la clase Polygon
        '''
        b=Polygon()
        for i in range(0,len(poligonos.listaDePoligonitos)):
            a=self.paraPoligono(poligonos.listaDePoligonitos[i])
            b=b.union(a)
        return b

    def paraPoligono(self,poligono:Poligonito):
        '''
        esta funcion recibe un Poligono y devuele un Polygon
        '''
        tupla=()
        for i in range (0,len(poligono.listaDePuntosDelGranPoligono)):
            a0=poligono.listaDePuntosDelGranPoligono[i][0]
            a1=poligono.listaDePuntosDelGranPoligono[i][1]
            long=self.myEstructura.estructuraFigurasGeome[a0][a1].longitud
            lati=self.myEstructura.estructuraFigurasGeome[a0][a1].latitud
            c=((long,lati),)
            tupla=tupla+c
        return Polygon(tupla)


if __name__=="__main__":
    import Factor
    from Punto import Punto
    from Impresora import Impresora
    
    lados=100
    muestras=100
    distanciaEnGrados=Factor.deKilometrosAGrados(20)
    punto=Punto('',25,-72.918626,-15.656727,20.0,'',3341.13110351562)
    alturaTorreFantasma=30
    
    est=Estructura(lados,muestras,distanciaEnGrados,punto,alturaTorreFantasma)
    imp=Impresora(Factor.lugarDeTrabajo)
    
    tec=TecnicoPoligono(est,muestras)
    tec.llenaEstructuraMatricial()
    imp.hacerMallaSegunEstructuraMatricial('out/TecnicoPoligono_malla',est)
    imp.graficaPuntosEstructura(est.estructuraLineaDeVista,'out/TecnicoPoligono_puntos_1','arrow')
    imp.graficaPuntosEstructura(est.estructuraFigurasGeome,'out/TecnicoPoligono_puntos_2','square')