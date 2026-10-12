# 정동관 v3 massing for render (traced coords registered to OSM; metres)
import sys, json, math
sys.path.insert(0, '..')
from geo import POLY_M
from shapely.geometry import Polygon, box, LineString, Point
from shapely.ops import unary_union
W, R, E = (Polygon(POLY_M[k]) for k in 'WRE')
B = unary_union([W, R, E]).buffer(0.01).buffer(-0.01)
k = 0.9568
H = B.bounds[3]
tE = E.intersection(box(-10, 85 / k, 80, 200)); tW = W.intersection(box(-10, -10, 80, 55 / k))
SB = box(-10, 3, 80, H - 3)
BF = B.intersection(SB).difference(tE).difference(tW)
Rw = R.intersection(W.buffer(3.2, join_style=2)); Re = R.difference(Rw)
PW = BF.intersection(unary_union([W, Rw]).buffer(0.01)); PE = BF.intersection(unary_union([E, Re]).buffer(0.01))
W1 = W.intersection(SB).difference(tW); E1 = E.intersection(SB).difference(tE)
def P(g):
    g = g.buffer(0)
    gs = [g] if g.geom_type == 'Polygon' else [q for q in getattr(g, 'geoms', []) if q.geom_type == 'Polygon']
    return [[[round(x, 2), round(y, 2)] for x, y in q.exterior.coords][:-1] for q in gs if q.area > 2]
parts = []
def add(g, z0, h, mat):
    for q in ([g] if g.geom_type == 'Polygon' else [x for x in getattr(g, 'geoms', []) if x.geom_type == 'Polygon']):
        if q.area < 2: continue
        d = {'pts': [[round(x, 2), round(y, 2)] for x, y in q.exterior.coords][:-1], 'z0': round(z0, 2), 'h': round(h, 2), 'mat': mat}
        if mat in ('screen', 'base'):
            ib = q.buffer(-1.1, join_style=2)
            if not ib.is_empty:
                ib = ib if ib.geom_type == 'Polygon' else max(ib.geoms, key=lambda t: t.area)
                d['inner'] = [[round(x, 2), round(y, 2)] for x, y in ib.exterior.coords][:-1]
        parts.append(d)
def cut_y(g, y0, y1): return g.intersection(box(-50, y0, 120, y1))
SL = 0.35
# 1F: west programme glass 0-7.0 ; east: south shops glass, rest base screen 0-8.65
add(W1, 0, 7.0, 'glass')
add(cut_y(E1, -5, 30), 0, 8.65, 'glass')
add(cut_y(E1, 30, 200), 0, 8.65, 'base')
# skip floors: west plate at 7.0/10.3/13.6, east plate at 8.65/11.95/15.25
for z in (7.0, 10.3, 13.6):
    add(PW, z, SL, 'slab'); add(PW, z + SL, 3.3 - SL, 'screen')
for z, h in ((8.65, 3.3), (11.95, 3.3), (15.25, 1.65)):
    add(PE, z, SL, 'slab'); add(PE, z + SL, h - SL, 'screen')
# 5F 16.9-21.1: offices north (glass), parking south (screen)
add(BF, 16.9, SL, 'slab')
add(cut_y(BF, 66, 200), 16.9 + SL, 4.2 - SL, 'glass')
add(cut_y(BF, -5, 66), 16.9 + SL, 4.2 - SL, 'screen')
# 6F hall north part, roof terrace south part
y6 = 38.5
hall = cut_y(BF, y6, 200); terrace = cut_y(BF, -5, y6)
add(hall, 21.1, 0.4, 'slab'); add(hall, 21.5, 7.6, 'fin'); add(hall, 29.1, 0.7, 'roof')
add(terrace, 21.1, 0.45, 'roofdeck')
# parapet on terrace edges (thin)
# tip cores: glass lift shafts + stair flights around triangular voids (Herma-like)
stairs = []; shafts = []
def tip_core(tip, levels, top):
    g = tip.buffer(-0.6, join_style=2)
    ring = list(g.exterior.coords)[:-1]
    # longest two edges
    edges = sorted([(LineString([ring[i], ring[(i + 1) % len(ring)]]).length, i) for i in range(len(ring))], reverse=True)
    e_ids = [edges[0][1], edges[1][1]]
    z = 0.0; f = 0
    while z < top - 0.1:
        i = e_ids[f % 2]; a = ring[i]; b = ring[(i + 1) % len(ring)]
        L = math.hypot(b[0] - a[0], b[1] - a[1]); run = min(L * 0.8, 9.0)
        ux, uy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
        # inward normal
        cx, cy = g.centroid.x, g.centroid.y
        nx, ny = -uy, ux
        if (cx - a[0]) * nx + (cy - a[1]) * ny < 0: nx, ny = -nx, -ny
        sx = a[0] + ux * (L - run) / 2 + nx * 0.9; sy = a[1] + uy * (L - run) / 2 + ny * 0.9
        dz = min(1.75, top - z)
        if f % 4 >= 2: sx, sy, ex, ey = sx + ux * run, sy + uy * run, sx, sy
        else: ex, ey = sx + ux * run, sy + uy * run
        stairs.append([round(sx, 2), round(sy, 2), round(z, 2), round(ex, 2), round(ey, 2), round(z + dz, 2), 1.6])
        z += dz; f += 1
    c = g.centroid
    shafts.append([round(c.x, 2), round(c.y, 2), top + 1.5])
tip_core(tE.intersection(SB), None, 29.8)
tip_core(tW, None, 21.6)
# sunken court under tip2 (dark pit) marker
pit = P(tW.buffer(-0.8, join_style=2))
out = {'parts': parts, 'lane': P(R), 'block': P(B), 'roof': P(terrace), 'roofz': 21.55, 'stairs': stairs, 'shafts': shafts, 'pit': pit,
       'tips': P(tE.intersection(SB)) + P(tW)}
json.dump(out, open('design.json', 'w'))
print('parts', len(parts), 'BF', round(BF.area * k * k, 1), 'hall', round(hall.area * k * k, 1), 'terrace', round(terrace.area * k * k, 1), 'stairs', len(stairs))
# posts/beams around tip voids, terrace parapets, solar on hall roof
posts = []; beams = []
for tip, top, lv in ((tE.intersection(SB), 29.8, (7.0, 10.3, 13.6, 16.9, 21.1, 29.1)), (tW, 21.6, (7.0, 10.3, 13.6, 16.9, 21.1))):
    ring = list(tip.buffer(-0.2, join_style=2).exterior.coords)[:-1]
    for x, y in ring: posts.append([round(x, 2), round(y, 2), top])
    for z in lv:
        for i in range(len(ring)):
            a, b = ring[i], ring[(i + 1) % len(ring)]
            beams.append([round(a[0], 2), round(a[1], 2), round(b[0], 2), round(b[1], 2), z])
par = []
tr = list(terrace.exterior.coords) if terrace.geom_type == 'Polygon' else list(max(terrace.geoms, key=lambda g: g.area).exterior.coords)
for i in range(len(tr) - 1):
    a, b = tr[i], tr[i + 1]
    if abs(a[1] - y6) < 0.01 and abs(b[1] - y6) < 0.01: continue
    par.append([round(a[0], 2), round(a[1], 2), round(b[0], 2), round(b[1], 2), 21.55])
solar = [{'pts': pts, 'z': 29.8} for pts in P(hall.buffer(-2.0, join_style=2))]
out.update({'posts': posts, 'beams': beams, 'parapets': par, 'solar': solar})
json.dump(out, open('design.json', 'w'))
print('posts', len(posts), 'beams', len(beams), 'parapets', len(par))
