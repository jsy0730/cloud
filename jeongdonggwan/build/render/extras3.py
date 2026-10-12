import json, sys, random
sys.path.insert(0, '..')
from geo import POLY_M
from shapely.geometry import Polygon, Point, box
d = json.load(open('design.json'))
random.seed(7)
roof = Polygon(d['roof'][0]); rz = d['roofz']
trees = []
for x in range(3, 44, 6):
    for y in range(5, 40, 7):
        if roof.buffer(-2.2).contains(Point(x, y)) and (x * 7 + y) % 3: trees.append([x, y, rz, 0.75])
for y in range(-2, 130, 11): trees.append([-4.5, y, 0, 1.1])
for x in range(-4, 44, 11): trees.append([x, 131.0, 0, 1.0])
for x in range(-4, 44, 11): trees.append([x, -4.0, 0, 0.95])
d['trees'] = trees
R = Polygon(POLY_M['R'])
lane_pts = []
for y in (20, 45, 75, 105):
    s = R.intersection(box(-10, y - 0.3, 80, y + 0.3)).centroid
    lane_pts.append([round(s.x, 2), round(s.y, 2)])
d["cars"] = [[-13, 62, 1.5708], [-16, 100, 1.5708], [-20, 150, 1.5708],
             [10, 136, 0], [30, 140, 0], [-5, 140, 0], [20, -8, 0], [36, -11, 0]] + [[p[0], p[1], 1.25] for p in lane_pts[:3]]
ppl = []
def scatter(cx, cy, n, r, z=0):
    for _ in range(n): ppl.append([round(cx + random.uniform(-r, r), 2), round(cy + random.uniform(-r, r), 2), z])
scatter(-3.0, 70, 8, 6); scatter(-3, 30, 6, 5); scatter(8, 128.5, 6, 6); scatter(30, 128.5, 4, 4); scatter(20, -1.5, 5, 6)
scatter(15, 20, 14, 9, rz); scatter(30, 30, 8, 6, rz)
d['people'] = [p for p in ppl if not Polygon(d['parts'][0]['pts']).contains(Point(p[0], p[1])) or p[2] > 0]
d['lights'] = [[3, 45, 4, 380], [5, 75, 6, 300], [20, 20, 23, 260], [30, 30, 23, 260], [38, 105, 6, 300], [-2, 110, 6, 250], [12, 10, 6, 300]]
json.dump(d, open('design.json', 'w'))
print(len(trees), len(d['people']))
# --- realism extras: lamps, lane lamps, more people near entrances
d = json.load(open('design.json'))
d['lamps'] = [[-5.5, y] for y in range(10, 130, 22)] + [[x, -5.0] for x in (6, 28)] + [[x, 133.5] for x in (6, 28)]
ll = []
for y in range(2, 120, 9):
    c = R.intersection(box(-10, y - 0.3, 80, y + 0.3)).centroid
    ll.append([round(c.x, 2), round(c.y, 2), 6.85])
d['laneLamps'] = ll
more = []
for (cx, cy, n, r, z) in ((-3.5, 100, 6, 5, 0), (-3.5, 20, 5, 5, 0), (20, 140, 4, 5, 0), (4, 12, 3, 2, 0), (30, 6, 5, 4, 21.6), (12, 20, 8, 7, 21.6)):
    for _ in range(n): more.append([round(cx + random.uniform(-r, r), 2), round(cy + random.uniform(-r, r), 2), z])
d['people'] = d.get('people', []) + more
json.dump(d, open('design.json', 'w'))
lane = {}
for y in (4, 8, 30, 60, 90, 120):
    c = R.intersection(box(-10, y - 0.3, 80, y + 0.3)).centroid
    lane[y] = [round(c.x, 2), round(c.y, 2)]
json.dump(lane, open('lane_pts.json', 'w'))
print('lane', lane)

d = json.load(open('design.json'))
H = 127.4
d['walks'] = [[[-6.5, -6], [-0.3, -6], [-0.3, H + 6], [-6.5, H + 6]]]
json.dump(d, open('design.json', 'w'))

d = json.load(open('design.json'))
roof = Polygon(d['roof'][0]); rz = d['roofz']
from shapely.affinity import scale as sscale
lawns = []
for (cx, cy, rx, ry) in ((10, 12, 6.5, 4.0), (30, 16, 5.5, 3.5), (18, 31, 7.0, 3.0), (34, 33, 4.0, 2.4)):
    e = sscale(Point(cx, cy).buffer(1.0), rx, ry)
    e = e.intersection(roof.buffer(-1.5))
    if not e.is_empty and e.geom_type == 'Polygon': lawns.append([[round(x, 2), round(y, 2)] for x, y in e.exterior.coords][:-1])
d['lawns'] = lawns
d['benches'] = [[10, 20, 0], [24, 22, 0], [28, 8, 1.57], [16, 6, 0], [34, 24, 0.3], [6, 28, 1.57]]
d['shrubs'] = [[4, 8, 0.8], [5, 10, 0.7], [38, 10, 0.8], [38, 28, 0.9], [20, 35, 0.8], [30, 35, 0.8], [8, 35, 0.7], [14, 14, 0.6], [28, 20, 0.6]]
sl = []
import math
for i in range(24):
    t = i / 23; sl.append([round(4 + t * 36, 2), round(5 + 1.8 * math.sin(t * 6.28), 2), rz + 3.2 - 0.6 * math.sin(t * 3.14)])
d['stringLights'] = sl
json.dump(d, open('design.json', 'w'))
