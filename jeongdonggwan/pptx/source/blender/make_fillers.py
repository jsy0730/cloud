# low-rise filler massing for blocks where OSM has no buildings (visual context only)
import json, math, os, random
from shapely.geometry import Polygon, LineString, Point, box
from shapely.ops import unary_union
from shapely import affinity
ROOT = os.path.join(os.environ['TEMP'], 'cloud_repo', 'jeongdonggwan', 'build', 'render')
C = json.load(open(os.path.join(ROOT, 'context.json'), encoding='utf8'))
D = json.load(open(os.path.join(ROOT, 'design.json'), encoding='utf8'))
random.seed(5)
cx, cy = C['center']
R = 330
road_polys = []
for r in C['roads']:
    if len(r['pts']) < 2: continue
    road_polys.append(LineString(r['pts']).buffer(r['w'] / 2 + 3.2, cap_style=2))
roads = unary_union(road_polys)
exist = unary_union([Polygon(b['pts']).buffer(2.0) for b in C['buildings']])
site = unary_union([Polygon(p) for p in D['block']]).buffer(3.5)
free = Point(cx, cy).buffer(R).difference(roads).difference(exist).difference(site)
parts = list(free.geoms) if free.geom_type == 'MultiPolygon' else [free]
out = []
for P in parts:
    if P.area < 140: continue
    mrr = P.minimum_rotated_rectangle
    xs, ys = mrr.exterior.coords.xy
    ang = math.atan2(ys[1] - ys[0], xs[1] - xs[0])
    Pr = affinity.rotate(P, -math.degrees(ang), origin=(cx, cy))
    minx, miny, maxx, maxy = Pr.bounds
    y = miny
    while y < maxy:
        h_strip = random.uniform(11, 17)
        x = minx
        while x < maxx:
            w = random.uniform(9, 18)
            cell = box(x, y, x + w, y + h_strip).buffer(-0.9)
            piece = Pr.intersection(cell)
            geoms = list(piece.geoms) if piece.geom_type in ('MultiPolygon', 'GeometryCollection') else [piece]
            for g in geoms:
                if g.geom_type != 'Polygon' or g.area < 70: continue
                g2 = g.simplify(0.3)
                if g2.minimum_rotated_rectangle.length < 1: continue
                w_, h_ = g2.bounds[2] - g2.bounds[0], g2.bounds[3] - g2.bounds[1]
                if min(w_, h_) < 5.0: continue
                g3 = affinity.rotate(g2, math.degrees(ang), origin=(cx, cy))
                d = g3.centroid.distance(Point(cx, cy))
                hs = random.choices([6.6, 9.9, 13.2, 16.5, 19.8], weights=[1, 4, 4, 3, 1 if d < 150 else 2])[0]
                out.append({'pts': [[round(a, 2), round(b, 2)] for a, b in list(g3.exterior.coords)[:-1]], 'h': hs})
            x += w + random.uniform(0.0, 1.5)
        y += h_strip + random.uniform(0.0, 1.2)
json.dump(out, open(os.path.join(os.environ['TEMP'], 'bl', 'fillers.json'), 'w'))
print('fillers', len(out))
