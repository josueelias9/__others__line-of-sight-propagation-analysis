from shapely.geometry import Point
from shapely.geometry import Polygon
from shapely.geometry import MultiPolygon

point = Point(0.0, 0.0)
q = Point((0.0, 0.0))
ext = [(0, 0), (0, 2), (2, 2), (2, 0), (0, 0)]
inte = [(1, 1), (1, 1.5), (1.5, 1.5), (1.5, 1)]
m = Polygon(ext,[inte])