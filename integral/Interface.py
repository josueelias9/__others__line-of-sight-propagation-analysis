import Factor
from Punto import Punto

class InterfaceEntrada:
    def ordenameInput2(self, entradaTexto) -> (list):
        '''
        convierte el archivo .txt en clases entendibles
        por las clases del proyecto
        -esta funcion ordena datos de una grupo de puntos
        -lee archivo separado por comas
        -7 elementos
        -separa los siete elementos del archivo separado por comas y lo pone en una lista de objetos "Punto"
        :return:
        '''
        listaAcc=[]
        aux=0
        with open(Factor.ruta + entradaTexto + '.txt') as inputfile:
            for line in inputfile:
                #print(aux)
                aux=aux+1
                linea = line.split(';')
                linea[3] = linea[3].strip()
                listaAcc.append(Punto(linea[0], int(linea[1]), float(linea[2]), float(linea[3]), float(linea[4]), linea[5], float(linea[6])))
                print('MsgSecretaria: Interacion: {}'.format(aux))
        return listaAcc

class InterfaceSalida:
    def generaKmlPuntos(self, lista: list, salidaKml):
        f = open(Factor.ruta + salidaKml + '.kml', 'w')
        print(Factor.ruta + salidaKml + '.kml')
        f.write(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">\n'
            '<Document>\n'
            '	<name>' + salidaKml + '.kml</name>\n'
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

    def generarTxtDePuntos(self, listaDePuntos: list, salidaTexto):
        f = open(Factor.ruta + salidaTexto + '.txt', 'w')
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

    def generaKmlRutas(self, relacionDeRutas: list, tipo: str, salidaKml):
        '''
        tipo str: si se pone un str vacio se obtendra relaciones que estaran pegadas al piso, pero
        si se esoge 'absolute' se obtendra relaciones rectas
        '''
        f = open(Factor.ruta + salidaKml + '.kml', 'w')
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



if __name__ == "__main__":
    imp = InterfaceSalida()
    sec = InterfaceEntrada()
    imp.generaKmlPuntos(sec.ordenameInput2())
    imp.generarTxtDePuntos(sec.ordenameInput2())