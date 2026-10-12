# parametric massing of 정동관 -> design.json (local metres, x east, y north)
import sys, json
sys.path.insert(0, '..')
from geo import POLY_M
from shapely.geometry import Polygon, box
from shapely.ops import unary_union
S = '/tmp/claude-0/-home-user-cloud/76ed2005-4113-58c6-b90f-f280afa8844d/scratchpad/build/render/'
W, R, E = (Polygon(POLY_M[k]) for k in 'WRE')
BLOCK = unary_union([W, R, E]).buffer(0.01).buffer(-0.01)
CFG = json.load(open(S + 'cfg.json')) if len(sys.argv) < 2 else json.loads(sys.argv[1])
def cut_y(g, y0, y1): return g.intersection(box(-50, y0, 120, y1))
def P(g):
    g = g.buffer(0)
    gs = [g] if g.geom_type == 'Polygon' else [q for q in g.geoms if q.geom_type == 'Polygon']
    return [[[round(x, 2), round(y, 2)] for x, y in q.exterior.coords][:-1] for q in gs if q.area > 1]
parts = []
def add(g, z0, h, mat):
    for pts in P(g): parts.append({'pts': pts, 'z0': z0, 'h': h, 'mat': mat})
inset = CFG.get('upper_inset', 0.0)
UP = BLOCK.buffer(-inset, join_style=2) if inset else BLOCK
if CFG.get('void'):
    UP = UP.difference(Polygon(CFG['void']))
lane = R.buffer(CFG.get('lane_widen', 0.0) / 2, join_style=2)
W1 = W.difference(lane); E1 = E.difference(lane)
# 1F 7.0m: west programme (glass), east: south retail glass, rest parking base (screen)
add(W1, 0, 7.0, 'glass')
ysplit = CFG.get('east_retail_y', 16)
add(cut_y(E1, -5, ysplit), 0, 7.0, 'glass')
add(cut_y(E1, ysplit, 200), 0, 7.0, 'base')
z = 7.0
for i in range(3):
    add(UP, z, 0.35, 'slab'); add(UP, z + 0.35, 2.95, 'screen'); z += 3.3
y6 = CFG['y6']
add(UP, z, 0.35, 'slab')
add(cut_y(UP, -5, CFG.get('office_y', 70)), z + 0.35, 3.85, 'screen')
add(cut_y(UP, CFG.get('office_y', 70), 200), z + 0.35, 3.85, 'glass')
z += 4.2
hall = cut_y(UP, y6, 200)
add(hall, z, 0.4, 'slab'); add(hall, z + 0.4, 7.6, 'hall'); add(hall, z + 8.0, 0.6, 'roof')
roof = cut_y(UP, -5, y6)
add(roof, z, 0.5, 'roofdeck')
json.dump({'parts': parts, 'lane': P(lane), 'block': P(BLOCK), 'roof': P(roof), 'top': z + 8.6, 'roofz': z + 0.5,
           'W1': P(W1), 'E1': P(E1)}, open(S + 'design.json', 'w'))
print('parts', len(parts), 'UP area', round(UP.area, 1), 'block', round(BLOCK.area, 1), 'roof', round(roof.area, 1), 'hall', round(hall.area, 1))
