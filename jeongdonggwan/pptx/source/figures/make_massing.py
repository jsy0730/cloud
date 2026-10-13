# alternative building forms (massing studies) -> JSON consumed by build_scene.py via JD_MASSING
import sys, json, math, os
sys.path.insert(0, '.')
from env_common import *          # D (design3 module), polys, shapely names
import shapely
from shapely.geometry import box as sbox, LineString, Polygon, MultiPolygon
from shapely.ops import unary_union

BASE = json.load(open(os.environ['TEMP'].replace(chr(92), '/') + '/cloud_repo/jeongdonggwan/build/render/design.json', encoding='utf8'))
OUT = os.environ['TEMP'].replace(chr(92), '/') + '/bl/'
BF = D.BF; H = BF.bounds[3]
FL = 3.3; SL = 0.35
ground = [p for p in BASE['parts'] if abs(p['z0']) < 1e-6]        # keep the 1F as designed


def pieces(g, amin=3.0):
    return [q for q in polys(g) if q.area >= amin]


def pts(q):
    return [[round(x, 2), round(y, 2)] for x, y in list(q.exterior.coords)[:-1]]


def add(parts, g, z0, h, mat, inner=False):
    for q in pieces(g):
        d = {'pts': pts(q), 'z0': round(z0, 2), 'h': round(h, 2), 'mat': mat}
        if inner:
            ib = q.buffer(-1.1, join_style=2)
            if not ib.is_empty:
                ib = ib if ib.geom_type == 'Polygon' else max(ib.geoms, key=lambda t: t.area)
                d['inner'] = pts(ib)
        parts.append(d)


def trees_on(g, z, n, seed, s=0.8):
    import random
    r = random.Random(seed); out = []
    minx, miny, maxx, maxy = g.bounds
    tries = 0
    while len(out) < n and tries < 400:
        tries += 1
        x, y = r.uniform(minx, maxx), r.uniform(miny, maxy)
        if g.buffer(-2.0).contains(shapely.geometry.Point(x, y)):
            out.append([round(x, 1), round(y, 1), z, s])
    return out


# ---------------------------------------------------------------- A: stepped terraces (north high, south low)
def massing_A():
    parts = list(ground); lawns = []; trees = []
    zones = [(3, 34, 1), (34, 62, 2), (62, 92, 4), (92, H - 3, 6)]       # (y0, y1, floors above 1F)
    z_base = 8.65
    for k, (y0, y1, n) in enumerate(zones):
        zone = BF.intersection(sbox(-10, y0, 80, y1))
        for i in range(n):
            z = z_base + FL * i
            if k == len(zones) - 1 and i == n - 1:
                add(parts, zone, z, SL, 'slab'); add(parts, zone, z + SL, FL * 1.45, 'fin')     # hall
                add(parts, zone, z + SL + FL * 1.45, 0.5, 'roof')
            else:
                add(parts, zone, z, SL, 'slab'); add(parts, zone, z + SL, FL - SL, 'screen', inner=True)
        ztop = z_base + FL * n
        if k < len(zones) - 1:
            add(parts, zone, ztop, 0.35, 'slab')
            ter = zone.buffer(-3.0, join_style=2)
            if not ter.is_empty:
                add(parts, ter, ztop + 0.35, 0.1, 'roofdeck')
                for q in pieces(ter.buffer(-1.0)):
                    lawns.append([pts(q), round(ztop + 0.45, 2)])
                trees += trees_on(ter, ztop + 0.45, 6, 10 + k, 0.8)
    return dict(parts=parts, lawns_z=lawns, trees=trees, drop=['solar', 'lawns', 'benches', 'parapets', 'roof'], stairs=[])


# ---------------------------------------------------------------- B: shifted plates with varied floor heights
def massing_B():
    parts = list(ground)
    spec = [  # (x0, x1, y0, y1, floor height)
        (0, 42.6, 3, H - 3, 3.3), (6, 42.6, 3, 104, 3.3), (0, 36, 18, H - 3, 4.9), (8, 42.6, 3, 112, 3.3),
        (0, 28, 8, H - 3, 3.3), (10, 42.6, 36, H - 3, 4.2)]
    z = 8.65
    for i, (x0, x1, y0, y1, hh) in enumerate(spec):
        g = BF.intersection(sbox(x0, y0, x1, y1))
        add(parts, g, z, SL + 0.15, 'slab')
        if i == len(spec) - 1:
            add(parts, g, z + SL + 0.15, hh - SL - 0.15, 'fin')
        z += hh
    g = BF.intersection(sbox(10, 36, 42.6, H - 3))
    add(parts, g, z, 0.5, 'roof')
    roofz = z + 0.5
    return dict(parts=parts, lawns_z=[], trees=trees_on(BF.intersection(sbox(0, 8, 28, H - 3)), 8.65 + 3.3 * 4 + 0.4 + 6.6 * 0 + 3.3 + 0.5 * 0, 5, 3, 0.8) if False else [],
                drop=['solar', 'lawns', 'benches', 'parapets', 'roof'], stairs=[])


# ---------------------------------------------------------------- C: diagonal canyon slot, bridged by the hall
def massing_C():
    parts = list(ground); lawns = []; trees = []
    slot = LineString([(-14, 30), (58, 80)]).buffer(4.6, cap_style='flat')
    z_base = 8.65
    for i in range(4):
        z = z_base + FL * i
        g = BF.difference(slot)
        add(parts, g, z, SL, 'slab'); add(parts, g, z + SL, FL - SL, 'screen', inner=True)
    zt = z_base + FL * 4
    zh = zt
    south = BF.intersection(sbox(-10, 3, 80, 38.5)).difference(slot)
    north = BF.intersection(sbox(-10, 38.5, 80, H - 3)).difference(slot)
    add(parts, BF.difference(slot), zh, SL, 'slab')
    add(parts, north, zh + SL, 8.0 - SL, 'fin')
    add(parts, north, zh + 8.0, 0.6, 'roof')
    ter = south.buffer(-2.5, join_style=2)
    for q in pieces(ter):
        add(parts, q, zh + SL, 0.1, 'roofdeck'); lawns.append([pts(q.buffer(-1.0)), round(zh + SL + 0.1, 2)])
    trees += trees_on(ter, zh + SL + 0.1, 8, 5, 0.8)
    # glass bridges across the canyon (links the two wings)
    mid = LineString([(-14, 30), (58, 80)]).interpolate(0.52, normalized=True)
    dx, dy = 72.0, 50.0; L_ = math.hypot(dx, dy); ux, uy = dx / L_, dy / L_
    for off, zz in ((0.0, z_base + FL * 2), (12.0, z_base + FL * 3)):
        cx, cy = mid.x + ux * off, mid.y + uy * off
        perp = LineString([(cx - uy * 9, cy + ux * 9), (cx + uy * 9, cy - ux * 9)]).buffer(2.0, cap_style='flat')
        add(parts, perp, zz, SL, 'slab'); add(parts, perp, zz + SL, FL - SL, 'glass')
    # canyon floor planting + long black stair up the slot centre line
    cl = LineString([(-6, 33.5), (52, 76.5)])
    stairs = [[-5.0, 33.0, 0.2, 51.0, 75.5, zh, 2.6]]
    for t in (0.18, 0.32, 0.48, 0.62):
        p = cl.interpolate(t, normalized=True)
        trees.append([round(p.x + 3.4, 1), round(p.y - 2.8, 1), 0.0, 1.0])
    return dict(parts=parts, lawns_z=lawns, trees=trees, drop=['solar', 'lawns', 'benches', 'parapets', 'roof'], stairs=stairs)


for name, fn in (('A', massing_A), ('B', massing_B), ('C', massing_C)):
    d = fn()
    json.dump(d, open(OUT + f'massing_{name}.json', 'w'))
    print(name, 'parts', len(d['parts']), 'lawns', len(d['lawns_z']), 'trees', len(d['trees']))
