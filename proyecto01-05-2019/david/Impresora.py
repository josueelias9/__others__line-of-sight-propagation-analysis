import sys
from Poligonos import Poligonos
from Estructura import Estructura

class Impresora:
    def __init__(self,a):
        self.ruta=a
    
    def generaKmlRutas(self, relacionDeRutas: list, nombre: str,tipo:str):
        '''
        tipo str: si se pone un str vacio se obtendra relaciones que estaran pegadas al piso, pero
        si se esoge 'absolute' se obtendra relaciones rectas
        '''
        f = open(self.ruta + nombre + '.kml', 'w')
        f.write(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">\n'
            '<Document>\n'
            '	<name>rutas.kml</name>\n'
            '	<Style id="sh_ylw-pushpin">\n'
            '		<IconStyle>\n'
            '			<scale>1.3</scale>\n'
            '			<Icon>\n'
            '				<href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>\n'
            '			</Icon>\n'
            '			<hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>\n'
            '		</IconStyle>\n'
            '		<LineStyle>\n'
            '			<color>ff00ff00</color>\n'
            '		</LineStyle>\n'
            '	</Style>\n'
            '	<Style id="sn_ylw-pushpin">\n'
            '		<IconStyle>\n'
            '			<scale>1.1</scale>\n'
            '			<Icon>\n'
            '				<href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>\n'
            '			</Icon>\n'
            '			<hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>\n'
            '		</IconStyle>\n'
            '		<LineStyle>\n'
            '			<color>ff00ff00</color>\n'
            '		</LineStyle>\n'
            '	</Style>\n'
            '	<StyleMap id="msn_ylw-pushpin">\n'
            '		<Pair>\n'
            '			<key>normal</key>\n'
            '			<styleUrl>#sn_ylw-pushpin</styleUrl>\n'
            '		</Pair>\n'
            '		<Pair>\n'
            '			<key>highlight</key>\n'
            '			<styleUrl>#sh_ylw-pushpin</styleUrl>\n'
            '		</Pair>\n'
            '	</StyleMap>\n'
            '	<Folder>\n'
            '		<name>Mis sitios</name>\n'
            '		<open>1</open>\n'
            '		<Style>\n'
            '			<ListStyle>\n'
            '				<listItemType>check</listItemType>\n'
            '				<ItemIcon>\n'
            '					<state>open</state>\n'
            '					<href>:/mysavedplaces_open.png</href>\n'
            '				</ItemIcon>\n'
            '				<ItemIcon>\n'
            '					<state>closed</state>\n'
            '					<href>:/mysavedplaces_closed.png</href>\n'
            '				</ItemIcon>\n'
            '				<bgColor>00ffffff</bgColor>\n'
            '				<maxSnippetLines>2</maxSnippetLines>\n'
            '			</ListStyle>\n'
            '		</Style>\n')

        #################################################################################################################

        for i in range(0, len(relacionDeRutas)):
            a3 = relacionDeRutas[i].puntoInicial.nombre
            b3 = relacionDeRutas[i].puntoFinal.nombre
            a0 = str(relacionDeRutas[i].puntoInicial.longitud)
            a1 = str(relacionDeRutas[i].puntoInicial.latitud)
            a2 = str(relacionDeRutas[i].puntoInicial.metrosSobreElNivelDelMar + relacionDeRutas[i].puntoInicial.alturaAntena)
            b0 = str(relacionDeRutas[i].puntoFinal.longitud)
            b1 = str(relacionDeRutas[i].puntoFinal.latitud)
            b2 = str(relacionDeRutas[i].puntoFinal.metrosSobreElNivelDelMar + relacionDeRutas[i].puntoFinal.alturaAntena)
            c = str(relacionDeRutas[i].distancia)[:5]
            f.write(
                '<Placemark>\n'
                '	<name>'+relacionDeRutas[i].puntoInicial.nombre+'->'+relacionDeRutas[i].puntoFinal.nombre+'</name>\n'
                '<description>'
                'inicio:\t'+ a3 +'\n'
                'fin:\t'+ b3 +'\n'
                'distancia:\t'+ c +' km\n'
                '</description>\n'
                '	<styleUrl>#msn_ylw-pushpin</styleUrl>\n'
                '	<LineString>\n'
                '		<tessellate>1</tessellate>\n'
                '		<altitudeMode>'+tipo+'</altitudeMode>\n'
                '		<coordinates>\n' +
					a0 + ',' + a1 + ',' + a2 + ' ' + b0 + ',' + b1 + ',' + b2 +
                '		</coordinates>\n'
                '	</LineString>\n'
                '</Placemark>\n')
        #################################################################################################################
        f.write(
            '	</Folder>\n'
            '</Document>\n'
            '</kml>\n')

    def generarTxtDeRelaciones(self, listaDeRelaciones: list, nombre: str):
        f = open(self.ruta + nombre + '.txt', 'w')
        for i in range(0, len(listaDeRelaciones)):
            f.write(
                listaDeRelaciones[i].puntoInicial.nombre + ';' +
                str(listaDeRelaciones[i].puntoInicial.ubigeo) + ';' +
                str(listaDeRelaciones[i].puntoInicial.longitud) + ';' +
                str(listaDeRelaciones[i].puntoInicial.latitud) + ';' +
                str(listaDeRelaciones[i].puntoInicial.alturaAntena) + ';' +
                listaDeRelaciones[i].puntoInicial.tipo + ';' +
                str(listaDeRelaciones[i].puntoInicial.metrosSobreElNivelDelMar) + ';' +

                listaDeRelaciones[i].puntoFinal.nombre + ';' +
                str(listaDeRelaciones[i].puntoFinal.ubigeo) + ';' +
                str(listaDeRelaciones[i].puntoFinal.longitud) + ';' +
                str(listaDeRelaciones[i].puntoFinal.latitud) + ';' +
                str(listaDeRelaciones[i].puntoFinal.alturaAntena) + ';' +
                listaDeRelaciones[i].puntoFinal.tipo + ';' +
                str(listaDeRelaciones[i].puntoFinal.metrosSobreElNivelDelMar) + ';' +

                str(listaDeRelaciones[i].distancia) + '\n')
        f.close()
    # ==============================================
    def generaKmlPuntos(self, lista: list, nombre: str):
        f = open(self.ruta + nombre + '.kml', 'w')
        print(self.ruta)
        f.write(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">\n'
            '<Document>\n'
            '	<name>' + nombre + '.kml</name>\n'
            '	<Style id="s_ylw-pushpin">\n'
            '		<IconStyle>\n'
            '			<scale>1.1</scale>\n'
            '			<Icon>\n'
            '				<href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>\n'
            '			</Icon>\n'
            '			<hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>\n'
            '		</IconStyle>\n'
            '	</Style>\n'
            '	<Style id="s_ylw-pushpin_hl">\n'
            '		<IconStyle>\n'
            '			<scale>1.3</scale>\n'
            '			<Icon>\n'
            '				<href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>\n'
            '			</Icon>\n'
            '			<hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>\n'
            '		</IconStyle>\n'
            '	</Style>\n'
            '	<StyleMap id="m_ylw-pushpin">\n'
            '		<Pair>\n'
            '			<key>normal</key>\n'
            '			<styleUrl>#s_ylw-pushpin</styleUrl>\n'
            '		</Pair>\n'
            '		<Pair>\n'
            '			<key>highlight</key>\n'
            '			<styleUrl>#s_ylw-pushpin_hl</styleUrl>\n'
            '		</Pair>\n'
            '	</StyleMap>\n'
            '	<Folder>\n'
            '		<name>Mis sitios</name>\n'
            '		<open>1</open>\n'
            '		<Style>\n'
            '			<ListStyle>\n'
            '				<listItemType>check</listItemType>\n'
            '				<ItemIcon>\n'
            '					<state>open</state>\n'
            '					<href>:/mysavedplaces_open.png</href>\n'
            '				</ItemIcon>\n'
            '				<ItemIcon>\n'
            '					<state>closed</state>\n'
            '					<href>:/mysavedplaces_closed.png</href>\n'
            '				</ItemIcon>\n'
            '				<bgColor>00ffffff</bgColor>\n'
            '				<maxSnippetLines>2</maxSnippetLines>\n'
            '			</ListStyle>\n'
            '		</Style>\n')

        for i in range(0, len(lista)):
            a3 = lista[i].nombre 
            a0 = str(lista[i].longitud)
            a1 = str(lista[i].latitud)
            a2 = str(lista[i].alturaAntena)
            a4 = lista[i].tipo
            a5 = str(lista[i].ubigeo)
            f.write(
                '		<Placemark>\n'
                '			<name>' + a3 + '</name>\n'
                '       <description>' + 
                'altura:\t'+ a2 +'\n'
                'identificador:\t'+ a5 +'\n'
                'Tipo de antena:\t' + a4 +
                '       </description>\n'
                '			<LookAt>\n'
                '				<longitude>' + a0 + '</longitude>\n'
                '				<latitude>' + a1 + '</latitude>\n'
                '				<altitude>' + a2 + str(2000) + '</altitude>\n'
                '				<heading>-29.85409409104959</heading>\n'
                '				<tilt>47.39871002284249</tilt>\n'
                '				<range>2900762.623799278</range>\n'
                '				<gx:altitudeMode>relativeToSeaFloor</gx:altitudeMode>\n'
                '			</LookAt>\n'
                '			<styleUrl>#m_ylw-pushpin</styleUrl>\n'
                '			<Point>\n'
                '				<gx:drawOrder>1</gx:drawOrder>\n'
                '				<coordinates>' + a0 + ',' + a1 + ',' + a2 + '</coordinates>\n' 
                '			</Point>\n'
                '		</Placemark>\n')

        ####################################################################################################
        f.write(
            '	</Folder>\n'
            '</Document>\n'
            '</kml>\n')
        f.close()

    def generarTxtDePuntos(self, listaDePuntos: list, nombre: str):
        f = open(self.ruta + nombre + '.txt', 'w')
        for i in range(0, len(listaDePuntos)):
            f.write(
                listaDePuntos[i].nombre + ';' +
                str(listaDePuntos[i].ubigeo) + ';' +
                str(listaDePuntos[i].longitud) + ';' +
                str(listaDePuntos[i].latitud) + ';' +
                str(listaDePuntos[i].alturaAntena) + ';' +
                listaDePuntos[i].tipo + ';' +
                str(listaDePuntos[i].metrosSobreElNivelDelMar) + ';' +
                listaDePuntos[i].greenAsociado + '\n')
        f.close()
            
    # ==============================================
    def graficaPuntosEstructura(self,lista:list,nombre:str,forma:str):
        f = open(self.ruta + nombre + '.kml', 'w')
        f.write(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">\n'
            '<Document>\n'
            '	<name>estructuraLineaDeVista.kml</name>\n'
            '	<Style id="s_ylw-pushpin">\n'
            '		<IconStyle>\n'
            '			<scale>1.1</scale>\n'
            '			<Icon>\n'
            '               <href>http://maps.google.com/mapfiles/kml/shapes/' + forma + '.png</href>\n'
            '			</Icon>\n'
            '			<hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>\n'
            '		</IconStyle>\n'
            '	</Style>\n'
            '	<Style id="s_ylw-pushpin_hl">\n'
            '		<IconStyle>\n'
            '			<scale>1.3</scale>\n'
            '			<Icon>\n'
            '               <href>http://maps.google.com/mapfiles/kml/shapes/' + forma + '.png</href>\n'
            '			</Icon>\n'
            '			<hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>\n'
            '		</IconStyle>\n'
            '	</Style>\n'
            '	<StyleMap id="m_ylw-pushpin">\n'
            '		<Pair>\n'
            '			<key>normal</key>\n'
            '			<styleUrl>#s_ylw-pushpin</styleUrl>\n'
            '		</Pair>\n'
            '		<Pair>\n'
            '			<key>highlight</key>\n'
            '			<styleUrl>#s_ylw-pushpin_hl</styleUrl>\n'
            '		</Pair>\n'
            '	</StyleMap>\n'
            '	<Folder>\n'
            '		<name>Mis sitios</name>\n'
            '		<open>1</open>\n'
            '		<Style>\n'
            '			<ListStyle>\n'
            '				<listItemType>check</listItemType>\n'
            '				<ItemIcon>\n'
            '					<state>open</state>\n'
            '					<href>:/mysavedplaces_open.png</href>\n'
            '				</ItemIcon>\n'
            '				<ItemIcon>\n'
            '					<state>closed</state>\n'
            '					<href>:/mysavedplaces_closed.png</href>\n'
            '				</ItemIcon>\n'
            '				<bgColor>00ffffff</bgColor>\n'
            '				<maxSnippetLines>2</maxSnippetLines>\n'
            '			</ListStyle>\n'
            '		</Style>\n')
        for i in range(0, len(lista)):
            for j in range(0, len(lista[i])):
                a0 = str(lista[i][j].longitud)
                a1 = str(lista[i][j].latitud)
                a2 = str(lista[i][j].alturaAntena)
                f.write(
                    '		<Placemark>\n'
                    '			<name>' + str(i)+'-'+str(j) + '</name>\n'
                    '			<LookAt>\n'
                    '				<longitude>' + a0 + '</longitude>\n'
                    '				<latitude>' + a1 + '</latitude>\n'
                    '				<altitude>' + a2 + str(2000) + '</altitude>\n'
                    '				<heading>-29.85409409104959</heading>\n'
                    '				<tilt>47.39871002284249</tilt>\n'
                    '				<range>2900762.623799278</range>\n'
                    '				<gx:altitudeMode>relativeToSeaFloor</gx:altitudeMode>\n'
                    '			</LookAt>\n'
                    '			<styleUrl>#m_ylw-pushpin</styleUrl>\n'
                    '			<Point>\n'
                    '				<gx:drawOrder>1</gx:drawOrder>\n'
                    '				<coordinates>' + a0 + ',' + a1 + ',' + a2 + '</coordinates>\n' 
                    '			</Point>\n'
                    '		</Placemark>\n')
        f.write(
            '	</Folder>\n'
            '</Document>\n'
            '</kml>\n')
        f.close()

    def funcion(self,misPoligonos:Poligonos,myEstructura:Estructura):
        nombre=myEstructura.puntoCero.nombre
        '''
        grafica el poligono entero, haciendo sinergia entre los poligonos chiquitos
        :param lista:
        :param nombre:
        :return:
        '''
        f = open(self.ruta + nombre+'.kml', 'w')
        f.write(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">\n'
            '<Document>\n'
            '    <name>'+nombre+'.kml</name>\n'
            '    <Style id="s_ylw-pushpin">\n'
            '        <IconStyle>\n'
            '            <scale>1.1</scale>\n'
            '            <Icon>\n'
            '                <href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>\n'
            '            </Icon>\n'
            '            <hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>\n'
            '        </IconStyle>\n'
            '    </Style>\n'
            '    <StyleMap id="m_ylw-pushpin">\n'
            '        <Pair>\n'
            '            <key>normal</key>\n'
            '            <styleUrl>#s_ylw-pushpin</styleUrl>\n'
            '        </Pair>\n'
            '        <Pair>\n'
            '            <key>highlight</key>\n'
            '            <styleUrl>#s_ylw-pushpin_hl</styleUrl>\n'
            '        </Pair>\n'
            '    </StyleMap>\n'
            '    <Style id="s_ylw-pushpin_hl">\n'
            '        <IconStyle>\n'
            '            <scale>1.3</scale>\n'
            '            <Icon>\n'
            '                <href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>\n'
            '            </Icon>\n'
            '            <hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>\n'
            '        </IconStyle>\n'
            '    </Style>\n'
            '    <Folder>\n'
            '        <name>ww</name>\n'
            '        <open>1</open>\n')
        for i in range(0,len(misPoligonos.listaDePoligonitos)):
            f.write(
                '<Placemark>\n'
                '    <name>'+str(i)+'</name>\n'
                '    <styleUrl>#m_ylw-pushpin</styleUrl>\n'
                '    <Polygon>\n'
                '        <tessellate>1</tessellate>\n'
                '        <outerBoundaryIs>\n'
                '            <LinearRing>\n'
                '                <coordinates>\n')
            for j in range(0, len(misPoligonos.listaDePoligonitos[i].listaDePuntosDelGranPoligono)):
                a0=misPoligonos.listaDePoligonitos[i].listaDePuntosDelGranPoligono[j][0]
                a1=misPoligonos.listaDePoligonitos[i].listaDePuntosDelGranPoligono[j][1]
                long=myEstructura.estructuraFigurasGeome[a0][a1].longitud
                lati=myEstructura.estructuraFigurasGeome[a0][a1].latitud
                f.write(str(long) + ',' + str(lati) + ',0 ')
            f.write(
                '                </coordinates>\n'
                '            </LinearRing>\n'
                '        </outerBoundaryIs>\n'
                '    </Polygon>\n'
                '</Placemark>\n')
        f.write(
            '</Folder>\n'
            '</Document>\n'
            '</kml>\n')

    def hacerMallaSegunEstructuraMatricial(self,nombre,est:Estructura):
        f=open(self.ruta + nombre+'.kml', 'w')
        f.write(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">\n'
            '<Document>\n'
            '	<name>cuadrilateros.kml</name>\n'
            '	<Style id="sh_ylw-pushpin">\n'
            '		<IconStyle>\n'
            '			<scale>1.3</scale>\n'
            '			<Icon>\n'
            '				<href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>\n'
            '			</Icon>\n'
            '			<hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>\n'
            '		</IconStyle>\n'
            '		<PolyStyle>\n'
            '			<color>80ffffff</color>\n'
            '		</PolyStyle>\n'
            '	</Style>\n'
            '	<StyleMap id="msn_ylw-pushpin">\n'
            '		<Pair>\n'
            '			<key>normal</key>\n'
            '			<styleUrl>#sn_ylw-pushpin</styleUrl>\n'
            '		</Pair>\n'
            '		<Pair>\n'
            '			<key>highlight</key>\n'
            '			<styleUrl>#sh_ylw-pushpin</styleUrl>\n'
            '		</Pair>\n'
            '	</StyleMap>\n'
            '	<Style id="sn_ylw-pushpin">\n'
            '		<IconStyle>\n'
            '			<scale>1.1</scale>\n'
            '			<Icon>\n'
            '				<href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>\n'
            '			</Icon>\n'
            '			<hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>\n'
            '		</IconStyle>\n'
            '		<PolyStyle>\n'
            '			<color>80ffffff</color>\n'
            '		</PolyStyle>\n'
            '	</Style>\n'
            '	<Folder>\n'
            '		<name>Lugares temporales</name>\n'
            '		<open>1</open>\n')
        ##################################################################################################################################
        for i in range(0, est.n):
            for j in range(1, est.m):
                if(est.estructuraMatricial[i][j]==1):
                    f.write(
                        '		<Placemark>\n'
                        '			<name>poligono'+str(i) + '-' + str(j)+'</name>\n'
                        '			<styleUrl>#msn_ylw-pushpin</styleUrl>\n'
                        '			<Polygon>\n'
                        '				<tessellate>1</tessellate>\n'
                        '				<outerBoundaryIs>\n'
                        '					<LinearRing>\n'
                        '						<coordinates>\n')
                    if (i == len(est.estructuraFigurasGeome) - 1):
                        xi0j0 = est.estructuraFigurasGeome[i][j].longitud
                        yi0j0 = est.estructuraFigurasGeome[i][j].latitud
                        xi0jm = est.estructuraFigurasGeome[i][j - 1].longitud
                        yi0jm = est.estructuraFigurasGeome[i][j - 1].latitud
                        xipjm = est.estructuraFigurasGeome[0][j - 1].longitud
                        yipjm = est.estructuraFigurasGeome[0][j - 1].latitud
                        xipj0 = est.estructuraFigurasGeome[0][j].longitud
                        yipj0 = est.estructuraFigurasGeome[0][j].latitud
                    else:
                        xi0j0 = est.estructuraFigurasGeome[i][j].longitud
                        yi0j0 = est.estructuraFigurasGeome[i][j].latitud
                        xi0jm = est.estructuraFigurasGeome[i][j-1].longitud
                        yi0jm = est.estructuraFigurasGeome[i][j-1].latitud
                        xipjm = est.estructuraFigurasGeome[i+1][j-1].longitud
                        yipjm = est.estructuraFigurasGeome[i+1][j-1].latitud
                        xipj0 = est.estructuraFigurasGeome[i+1][j].longitud
                        yipj0 = est.estructuraFigurasGeome[i+1][j].latitud
                    f.write(str(xi0j0) + ',' + str(yi0j0) + ',0 ')
                    f.write(str(xi0jm) + ',' + str(yi0jm) + ',0 ')
                    f.write(str(xipjm) + ',' + str(yipjm) + ',0 ')
                    f.write(str(xipj0) + ',' + str(yipj0) + ',0 ')
                    f.write(str(xi0j0) + ',' + str(yi0j0) + ',0\n')
                    f.write(
                        '						</coordinates>\n'
                    '					</LinearRing>\n'
                    '				</outerBoundaryIs>\n'
                    '			</Polygon>\n'
                    '		</Placemark>\n')
        ##################################################################################################################################
        f.write(
            '	</Folder>\n'
            '</Document>\n'
            '</kml>\n')

    def ploteadorDeMatriz(self,matriz):
        '''
        el ploteo se hace en la linea de comandos
        nuestra matriz no es una matriz ordinaria.
        crece de abajo a arriba             v ^
        crece de izquierda a derecha        < >
        sus elementos son de la forma[a][b]
        a hace referencia a una fila        v ^
        b hace referencia a una columna     < >
        :param a0: numero de total de filas
        :param a1: numero de total de columnas
        :return:
        '''
        a0=len(matriz)
        a1=len(matriz[0])
        for i in range(0, a0):
            for j in range(0,a1):
                sys.stdout.write(str(matriz[a0-i-1][j])+' ')
            print()
    # ==============================================
       
    def deWktAKml(self,nombre:str,diccionario:dict):
        #['coordinates']       -lista- poligonos
        #['coordinates'][]     -tupla- poligono
        #['coordinates'][][]   -tupla- si 0 oubount del poligono, y lo que viene el inbound
        #['coordinates'][][][] -tupla- cordenada    
        f = open(self.ruta + nombre + '.kml', 'w')
        if diccionario['type']=='MultiPolygon':
            f.write(
                '<?xml version="1.0" encoding="UTF-8"?>\n'
                '<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">\n'
                '<Placemark>\n'
                '	<Style>\n'
                '		<LineStyle>\n'
                '			<color>ff0000ff</color>\n'
                '		</LineStyle>\n'
                '	</Style>\n'
                '	<MultiGeometry>\n')
            for i in range (0,len(diccionario['coordinates'])):
                f.write(
                    '		<Polygon>\n'
                    '			<outerBoundaryIs>\n'
                    '				<LinearRing>\n'
                    '					<coordinates>\n')
                for n in range(0,len(diccionario['coordinates'][i][0])):
                    f.write(str(diccionario['coordinates'][i][0][n][0])+','+str(diccionario['coordinates'][i][0][n][1])+' ')
                f.write(
                    '					</coordinates>\n'
                    '				</LinearRing>\n'
                    '			</outerBoundaryIs>\n')
                for j in range(1,len(diccionario['coordinates'][i])):
                    f.write(
                    '			<innerBoundaryIs>\n'
                    '				<LinearRing>\n'
                    '					<coordinates>\n')
                    for k in range(0,len(diccionario['coordinates'][i][j])):
                        f.write(str(diccionario['coordinates'][i][j][k][0])+','+str(diccionario['coordinates'][i][j][k][1])+' ')
                    f.write(    
                        '					</coordinates>\n'
                        '				</LinearRing>\n'
                        '			</innerBoundaryIs>\n')
                        
                f.write(
                    '		</Polygon>\n')
            
            f.write(
                '	</MultiGeometry>\n'
                '</Placemark>\n'
                '</kml>\n')           
            
            ###############################
        if diccionario['type']=='Polygon':
            f.write(
                '<?xml version="1.0" encoding="UTF-8"?>\n'
                '<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">\n'
                '<Placemark>\n'
                '	<Style>\n'
                '		<LineStyle>\n'
                '			<color>ff0000ff</color>\n'
                '		</LineStyle>\n'
                '	</Style>\n'    
                '		<Polygon>\n'
                '			<outerBoundaryIs>\n'
                '				<LinearRing>\n'
                '					<coordinates>\n')
            for n in range(0,len(diccionario['coordinates'][0])):
                f.write(str(diccionario['coordinates'][0][n][0])+','+str(diccionario['coordinates'][0][n][1])+' ')
            f.write(
                '					</coordinates>\n'
                '				</LinearRing>\n'
                '			</outerBoundaryIs>\n')
            for j in range(1,len(diccionario['coordinates'])):
                f.write(
                '			<innerBoundaryIs>\n'
                '				<LinearRing>\n'
                '					<coordinates>\n')
                for k in range(0,len(diccionario['coordinates'][j])):
                    f.write(str(diccionario['coordinates'][j][k][0])+','+str(diccionario['coordinates'][j][k][1])+' ')
                f.write(    
                    '					</coordinates>\n'
                    '				</LinearRing>\n'
                    '			</innerBoundaryIs>\n')             
            f.write(
                '		</Polygon>\n'
                '</Placemark>\n'
                '</kml>\n')           
        
        
        