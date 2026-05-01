'''
DESCARGA DE WHELLS PARA ESTE PROYECTO:
como instalar Shapely en Pycharm
https://gis.stackexchange.com/questions/62925/why-is-shapely-not-installing-correctly
como instalar matplotlib
https://stackoverflow.com/questions/39067640/i-cant-install-matplotlib
request
https://pypi.org/project/requests/#files
geohelper
https://pypi.org/project/geohelper/#files

'''

print('wwwwww')
from shapely.geometry import box
from shapely.geometry import Polygon
import matplotlib.pyplot as plt
b = Polygon([[0, 0], [3, 0], [3, 1], [0, 1], [0, 0]])
c = Polygon([[1, 0], [2, 0], [2, 2], [1, 2], [1, 0]])
v = b.union(c)
xs, ys = v.exterior.xy
#plot it
fig, axs = plt.subplots()
axs.fill(xs, ys, alpha=0.5, fc='r')
plt.show() #if not interactive


'''
import shapely.geometry as sg
import shapely.ops as so
import matplotlib.pyplot as plt

#constructing the first rect as a polygon
r1 = sg.Polygon([(0,0),(0,1),(1,1),(1,0),(0,0)])

#a shortcut for constructing a rectangular polygon
r2 = sg.box(0.5,0.5,1.5,1.5)

#cascaded union can work on a list of shapes
new_shape = so.cascaded_union([r1,r2])

#exterior coordinates split into two arrays, xs and ys
# which is how matplotlib will need for plotting
xs, ys = new_shape.exterior.xy

#plot it
fig, axs = plt.subplots()
axs.fill(xs, ys, alpha=0.5, fc='r', ec='none')
plt.show() #if not interactive
'''