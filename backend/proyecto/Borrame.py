# -*- coding: utf-8 -*-
"""
Created on Tue May 29 12:55:57 2018

@author: Josue
"""
'''
lista1=['1','w','q','aa','www']

tam=len(lista1)
print(tam)
veces=0
for i in range(0,tam):
    for j in range(i+1,tam):
        print(str(i)+'-'+str(j))
        veces=veces+1
print(veces)

''' 
'''
from itertools import combinations
lista=[90,2,3,4,5]
for j in range(0,len(lista)):
    comb=combinations(lista,len(lista)-j)
    for tupla in list(comb):
        print(tupla)
'''
'''
for j in range(0,len(lista)):
    comb=combinations(lista,len(lista)-j)
    for tupla in list(comb):
        print(tupla)
        print('·······················')
        flag=True
        comb2=combinations(tupla,2)
        for tupla2 in list(comb2):
            print(tupla2)
        print('·······················')
'''
'''
lista=[90,2,3,4,5]
aux=1      
for i in range(1,len(lista)):
    print(lista[i])

#for i in range(0,len(lista))
'''

'''
ALGORITMO PARA HACER EL SPANNING TREE
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree
X = csr_matrix([[0, 8, 0, 3],
                [0, 0, 2, 5],
                [0, 0, 0, 6],
                [0, 0, 0, 0]])
Tcsr = minimum_spanning_tree(X)
print(Tcsr.toarray().astype(int))
'''
'''
import Factor
from shapely.geometry import Polygon, Point
p = Point(2,2)
P=Polygon([(0,0), (0,5), (5,0), (5,5)])
print (P.contains(p))
'''

'''
from fastkml import kml
f=open('C:/Users/Josue/Desktop/gabo/macro.kml','r')
doc = f.read()
k = kml.KML()
k.from_string(doc)
len(k._features)
'''

'''
# Import the library
from fastkml import kml
from shapely.geometry import Point, LineString, Polygon

# Create the root KML object
k = kml.KML()
ns = '{http://www.opengis.net/kml/2.2}'

# Create a KML Document and add it to the KML root object
d = kml.Document(ns, 'docid', 'doc name', 'doc description')
k.append(d)

# Create a KML Folder and add it to the Document
f = kml.Folder(ns, 'fid', 'f name', 'f description')
d.append(f)

# Create a KML Folder and nest it in the first Folder
nf = kml.Folder(ns, 'nested-fid', 'nested f name', 'nested f description')
f.append(nf)

# Create a second KML Folder within the Document
f2 = kml.Folder(ns, 'id2', 'name2', 'description2')
d.append(f2)

# Create a Placemark with a simple polygon geometry and add it to the
# second folder of the Document
p = kml.Placemark(ns, 'id', 'name', 'description')
p.geometry =  Polygon([(0, 0, 0), (1, 1, 0), (1, 0, 1)])
f2.append(p)

# Print out the KML Object as a string
print(k.to_string(prettyprint=True))
'''




from fastkml import kml

doc='''
    <?xml version="1.0" encoding="UTF-8"?>
    <kml xmlns="http://www.opengis.net/kml/2.2">
    	<Document>
    		<name>Document.kml</name>
    		<open>1</open>
    	<Style id="exampleStyleDocument">
    		<LabelStyle>
    			<color>ff0000cc</color>
    		</LabelStyle>
    	</Style>
    		<Placemark>
    	<name>Document Feature 1</name>
    	<styleUrl>#exampleStyleDocument</styleUrl>
    	<Point>
    	<coordinates>-122.371,37.816,0</coordinates>
    	</Point>
    </Placemark>
    		<Placemark>
    			<name>Document Feature 2</name>
    			<styleUrl>#exampleStyleDocument</styleUrl>
    			<Point>
    									<coordinates>-122.370,37.817,0</coordinates>
    			</Point>
    		</Placemark>
    	</Document>
    </kml>
    '''
k = kml.KML()
k.from_string(doc)
# Create the KML object to store the parsed result
#k = kml.KML()

# Read in the KML string
#k.from_string(doc)

# Next we perform some simple sanity checks

# Check that the number of features is correct
# This corresponds to the single ``Document``
