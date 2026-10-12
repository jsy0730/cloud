import json, sys
sys.path.insert(0, '..')
from geo import POLY_M
from shapely.geometry import Polygon, Point
d = json.load(open('design.json'))
roof = Polygon(d['roof'][0]); rz = d['roofz']
trees = []
import itertools
for x in range(4, 44, 7):
    for y in range(3, 45, 8):
        if roof.buffer(-2.5).contains(Point(x, y)) and (x + y) % 3: trees.append([x, y, rz, 0.8])
for y in range(-2, 130, 12): trees.append([-4.5, y, 0, 1.1])          # 전포대로 street trees (west sidewalk)
for x in range(-4, 44, 12): trees.append([x, 131.5, 0, 1.0])          # 서전로
d['trees'] = trees
d['cars'] = [[-12, 20, 1.5708], [-12, 55, 1.5708], [-16, 95, 1.5708], [-20, 40, 1.5708], [-20, 140, 1.5708],
             [10, 136, 0], [30, 140, 0], [-5, 140, 0], [18, 75, 1.2], [24, 104, 1.35]]
d['lights'] = [[5, 70, 6, 300], [10, 30, 6, 300], [24, 100, 6, 300], [20, 8, 6, 300], [-2, 110, 6, 250]]
json.dump(d, open('design.json', 'w'))
print(len(trees))
# external stair on south face (Park 'n' Play), flights alternating along x, inside the lot line
fl = []; z = 0.0; x0, x1 = 8.0, 36.0; i = 0
while z < rz - 0.1:
    dz = min(3.6, rz - z)
    a, b = (x0, x1) if i % 2 == 0 else (x1, x0)
    fl.append([a, 1.3, z, b, 1.3, z + dz, 2.2]); z += dz; i += 1
d['stairs'] = fl
json.dump(d, open('design.json', 'w'))
print('flights', len(fl))
