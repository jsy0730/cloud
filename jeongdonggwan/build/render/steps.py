import sys, json
sys.path.insert(0, '..')
from geo import POLY_M
from shapely.geometry import Polygon, box
from shapely.ops import unary_union
W, R, E = (Polygon(POLY_M[k]) for k in 'WRE')
B = unary_union([W, R, E]).buffer(0.01).buffer(-0.01)
k = 0.9568; H = B.bounds[3]
tE = E.intersection(box(-10, 85 / k, 80, 200)); tW = W.intersection(box(-10, -10, 80, 55 / k))
SB = box(-10, 3, 80, H - 3)
BF = B.intersection(SB).difference(tE).difference(tW)
Rw = R.intersection(W.buffer(3.2, join_style=2)); Re = R.difference(Rw)
PW = BF.intersection(unary_union([W, Rw]).buffer(0.01)); PE = BF.intersection(unary_union([E, Re]).buffer(0.01))
W1 = W.intersection(SB).difference(tW); E1 = E.intersection(SB).difference(tE)
def cut_y(g, y0, y1): return g.intersection(box(-50, y0, 120, y1))
def P(g):
    g = g.buffer(0)
    gs = [g] if g.geom_type == 'Polygon' else [q for q in getattr(g, 'geoms', []) if q.geom_type == 'Polygon']
    return [[[round(x, 2), round(y, 2)] for x, y in q.exterior.coords][:-1] for q in gs if q.area > 2]
def mk(items):
    parts = []
    for g, z0, h, m in items:
        for pts in P(g): parts.append({'pts': pts, 'z0': z0, 'h': h, 'mat': m})
    return {'parts': parts}
y6 = 38.5
S = []
S.append(mk([(W, 0, 0.8, 'dW'), (R, 0, 0.3, 'dlane'), (E, 0, 0.8, 'dE')]))
S.append(mk([(W1, 0, 7, 'dW'), (E1, 0, 7, 'dE'), (R, 0, 0.2, 'dlane'), (tE, 0, 0.1, 'dsite'), (tW, 0, 0.1, 'dsite')]))
S.append(mk([(W.intersection(SB), 0, 7, 'dW'), (E.intersection(SB), 0, 7, 'dE'), (R, 0, 0.2, 'dlane'), (B.intersection(SB), 7, 14.2, 'dpark')]))
S.append(mk([(W1, 0, 7, 'dW'), (E1, 0, 7, 'dE'), (R, 0, 0.2, 'dlane'), (BF, 7, 14.2, 'dpark'), (tE.intersection(SB), 0, 29.8, 'dcore'), (tW, 0, 21.6, 'dcore')]))
it = [(W1, 0, 7, 'dW'), (E1, 0, 8.65, 'dE'), (R, 0, 0.2, 'dlane')]
for i, z in enumerate((7.0, 10.3, 13.6)): it.append((PW, z, 3.3, 'dpark' if i % 2 == 0 else 'dpark2'))
for i, (z, h) in enumerate(((8.65, 3.3), (11.95, 3.3), (15.25, 1.65))): it.append((PE, z, h, 'dpark2' if i % 2 == 0 else 'dpark'))
it += [(cut_y(BF, -5, 66), 16.9, 4.2, 'dpark'), (cut_y(BF, 66, 200), 16.9, 4.2, 'doff'), (cut_y(BF, y6, 200), 21.1, 8.0, 'dcult'), (cut_y(BF, -5, y6), 21.1, 0.5, 'droof'),
       (tE.intersection(SB), 0, 29.8, 'dcore'), (tW, 0, 21.6, 'dcore')]
S.append(mk(it))
for i, s in enumerate(S): json.dump(s, open(f'step{i + 1}.json', 'w'))
print('ok')
