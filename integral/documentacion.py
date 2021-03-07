# 1 datos
'''
·····················
estructura antigua
·····················

|------------|
|jefe        |
|------------|

--------------------------------------------------------------

|------------|  |------------|  |------------|  |------------|
tecnicored       tecnicopoligono  impresora        secretaria
|------------|  |------------|  |------------|  |------------|

--------------------------------------------------------------

|------------|  |------------|  |------------|  |------------|
poligono             estructura	  relacion       internet
|------------|  |------------|  |------------|  |------------|

--------------------------------------------------------------

|------------|
|punto       |
|------------|

··········································
estructura general del programa
··········································
pero en si, lo que yo le ingreso al programa es:
- archivos txt, eso es todo. -> se convierte en listapunto y lista relacion (lo que alimentara el programa)




|INTERFACE---|------------|ENTRADA-----|------------|CLASES------|------------|SALIDA------|

                         TecnicoPoligono, TecnicoRed [integradores]

|------------|------------|------------|------------|------------|------------|------------|

|------------|------------|------------|------------|------------|------------|------------|
 IntefaceEntrada  ------>  Puntos                    Internet                  InterfaceSalidaText
|------------|-------|----|------------|------------|------------|------------|------------|
                     |-->  Relaciones                                          InterfaceSalidaKML
|------------|------------|------------|------------|------------|------------|------------|

         punto (mas basico), relacion, estructura, poligono, poligonito [unidades]


- metodos que requieren dos archivos de entrada
- metodos que requieren un archivo de entrada



tareas:
listaA    listaB
|-|       |-|
a0        b0
a1        b1
a3        b3
a4        b4
a5        b5

relaciona los elementos de la lista A con los elementos de la lista B


las interfaces no se comunican entre ellas


··········································
clasificacion de las clases
··········································
unidades basicas, no tienen metodos
- Relacion
- Punto
- estructura
- Poligono
- Poligonito
implementan metodos
    complejos
    - TecnicoRed
    - TecnicoPoligono
    interface
    - InterfaceEntrada
    - InterfaceSalida
    integradores
    - Integral

'''

# 2 clases y librerias

    # 2.1 MACRO
'''
··········································
factor
··········································
No es una clase en si. Tiene informacion de:
- altura de antena
- altura de repetidor
- cantidad de angulos
- cantidad de muestreos
- distancia maxima (radio)
- ruda donde se realizara los trabajo
- texto de entrada 1
- texto de entrada 2
- texto de salida 1
- texto de salida 2
- kml de salida 1
- kml de salida 2
- kml de salida 3
Esta informacion debe estar completa antes de realizar algun trabajo
'''

    # 2.2 COMPLEJOS
'''
··········································
InterfaceEntrada (Secretaria)
··········································
1) atributos definidos en el el __init__:
- ruta
- listaAcc     / tipo lista (eliminar)
- listaAccCone / tipo lista 
- listaFinal   / tipo lista
- listaFuera   / tipo lista 

2) metodos:
- ordenameInput2
se encarga de coger el TXT de entrada y convertirlo en 
objeto LISTA_DE_PUNTOS (o LISTA_DE_RELACIONES)

··········································
InterfaceSalida (Impresora)
··········································
1) atributos definidos en el el __init__:
ruta

saca: kml y txt

2) metodos:
- generaKmlRutas (lista de relaciones, nombre del kml, tipo de kml)(genera archivo kml)
- generarTxtDeRelaciones
- generaKmlPuntos
- generarTxtDePuntos
- graficaPuntosEstructura

··········································
TecnicoRed
··········································
atributos definidos en el el __init__:
internet / objeto creado por mi

metodos
con mayuscuta: mis clases
todo minuscula: objetos de Python

P) fresnel(Punto, Punto, Punto) -> float
encuentraRelacionesPosibles(Puntos, Puntos, int) -> Puntos, Puntos
lineaDeVistaConsiderandoFresnel(Puntos, Punto, Punto) -> bool
calculaMenorDistanciaEnLista(Relaciones) -> Relacion
P) generaFresnel(Punto, Punto) -> lista
P) generaLineaDeVista(Punto, Punto) -> lista
ponleAlturas(Puntos)
encontrarTodasLasRelacionesPosibles1Dist(Puntos, int) -> Relaciones
encontrarTodasLasRelacionesPosibles1LDVDist(Puntos, int) -> lista
encontrarTodasLasRelacionesPosibles2Dist(Puntos, Puntos, int) -> lista
P) encontrarTodasLasRelacionesPosibles2LDV(Puntos, Puntos) -> lista
encontrarTodasLasRelacionesPosibles2LDVDist(Puntos, Puntos, int) -> lista

%%%%%%%%%%%%%%%%%
clasificacion
%%%%%%%%%%%%%%%%%
funciones que 
- ingresa una txt
- ingresa dos txt
input
int, float / int, float
deGradosAKilometros()
deKilometrosAGrados()

miObjeto, int
buscaPuntosQueCumplanCondicion()

··········································
Internet
··········································
metodos
- traerInfoDeAlturas(list(listadealturas), Punto) -> Puntos, str
- traerInfoDePuntos(Punto, Punto) -> Puntos, str
- consigueDatoDeAlturaDeUnSoloPunto(Punto) -> str, str
'''

    # 2.3 BASICOS (no tienen metodos, solo atributos / si es que tiene tener en cuenta que se van a sacar)
'''
··········································
Punto
··········································
atributos definidos en el el __init__:
- nombre
- ubigeo                   #numero ID
- longitud                 #coordenadas
- latitud                  #coordenadas
- alturaAntena             #metros
- tipo
- metrosSobreElNivelDelMar #metros
- greenAsociado

··········································
Relacion
··········································
atributos definidos en el el __init__:
- puntoInicial
- puntoFinal
- distancia

'''

# 3 pseudocodigo
'''
··········································
Del programa poligono
··········································
Detecta uno
Nos dan un 1. Lo ponemos en lista2
Cambiar el 1 por el 2
Repetir hasta que lista2 este vacía
	Repite con todos los elementos de lista2
		Si arriba escapa de la matriz limpiar hacemos que arriba sea 0
		Si abajo escapa de la matriz limpiar hacemos que abajo sea 0
		Si derecha escapa de la matriz limpiar hacemos que derecha sea 0
		Si izquierda escapa de la matriz limpiar hacemos que izquierda sea 0
		Si hay uno alrededor de 2
			Si arriba de 2 es 1 y este 1 no cierra polígono (llamar función):
				Ponerlo en lista1->2
				Cambiar el 1 por el 2
Si abajo de 2 es 1 y este 1 no cierra polígono (llamar función):
				Ponerlo en lista1->2
				Cambiar el 1 por el 2
Si derecha de 2 es 1 y este 1 no cierra polígono (llamar función):
				Ponerlo en lista1->2
				Cambiar el 1 por el 2
Si izquierda de 2 es 1 y este 1 no cierra polígono (llamar función):
				Ponerlo en lista1->2
				Cambiar el 1 por el 2
Cambiar el 2 por el 3
		Si no hay uno alrededor de 2
			Cambiar el 2 por el 3

··········································
robot
··········································
el robot debe retornar verdadero si es que puede llegar a los limites de la matriz. En caso no pueda retornar falso

Nos dan un 0. Lo ponemos en lista4
Cambiar el 0 por el 4
Repetir hasta que lista4 este vacía
	Repite con todos los elementos de lista4
		Si arriba escapa de la matriz, llamar función limpiar (limpiar con ceros) y retornar verdadero
		Si abajo escapa de la matriz, llamar función limpiar (limpiar con ceros) y retornar verdadero
		Si derecha escapa de la matriz, llamar función limpiar (limpiar con ceros) y retornar verdadero
		Si izquierda escapa de la matriz, llamar función limpiar (limpiar con ceros) y retornar verdadero
		Si hay uno alrededor de 4
			Si arriba de 4 es 0
				Ponerlo en lista0->4
				Cambiar el 0 por el 4
Si abajo de 4 es 0
				Ponerlo en lista0->4
				Cambiar el 0 por el 4
Si derecha de 4 es 0
				Ponerlo en lista0->4
				Cambiar el 0 por el 4
Si izquierda de 4 es 0
				Ponerlo en lista0->4
				Cambiar el 0 por el 4
Cambiar el 4 por el 5
		Si no hay uno alrededor de 4
			Cambiar el 4 por el 5
Llamar función limpiar (limpiar con ceros) y retornar falso


··········································
borrador
··········································
recibimos la lista y el numero que tenemos que cambiar
La lista contiene los índices de la estructuraMatricial. De acuerdo al valor que nos dan ponemos este valor en los lugares que corresponde con los índices de la lista que nos dieron


··········································
Cierre polígono
··········································
Como input tiene recibe un índice
Retorna verdadero si el valor de entrada cierra el polígono. Retorna falso en caso contrario

Si arriba escapa de la matriz limpiar hacemos que arriba sea 0
Si abajo escapa de la matriz limpiar hacemos que abajo sea 0
Si derecha escapa de la matriz limpiar hacemos que derecha sea 0
Si izquierda escapa de la matriz limpiar hacemos que izquierda sea 0
si arriba es 0 y abajo es 0 y derecha es 2 (o 3) y izquierda es 2 (o 3)
	en arriba llamar a robot. Si retorna falso
		retornar verdadero
	en abajo llamar a robot. Si retorna falso
		retornar verdadero
retornar falso
en caso contrario, si arriba es 2 (o 3) y abajo es 2 (o 3) y derecha es y e izquierda es 0
	en derecha llamar a robot. Si retorna falso
		retornar verdadero
	en izquierda llamar a robot. Si retorna falso
		retornar verdadero
retornar falso




··········································
Del programa línea de vista
··········································
Unir puntos
une los puntos que se quedaron fuera entre ellos

la lista0 contiene todos los elementos que no fueron conectados
listaRelaciones contiene todas las relaciones formadas
repetir hasta que el tamaño de lista0 no sea 0
	crear listaPuntosConectados y que este vacía
crear listaPuntosNoConectados y que este vacía
Coger el primer elemento
Para cada uno de los elementos de la lista0, desde el segundo elemento:
Si LDV y distancia
			Poner elemento el listaPuntosConectados
Poner en listaRelaciones a este elemento y el primer elemento
		Else
			Poner elemento en listaPuntosNoConectados
	Si el tamaño de listaPuntosConectados no es 0
		Poner al primer elemento de lista0 en listaPuntosConectados
	Else
		Poner al primer elemento de lista0 en listaPuntosNoConectados
	lista0= listaPuntosNoConectados


'''


