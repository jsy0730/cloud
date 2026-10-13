import json, os
from shapely.geometry import Polygon
ROOT = os.path.join(os.environ['TEMP'], 'cloud_repo', 'jeongdonggwan', 'build', 'render')
D = json.load(open(os.path.join(ROOT, 'design.json'), encoding='utf8'))
out = []
for i, p in enumerate(D['parts']):
    if p['mat'] not in ('glass', 'fin'): continue
    g = Polygon(p['pts']).buffer(-0.45, join_style=2)
    if g.is_empty: continue
    if g.geom_type == 'MultiPolygon': g = max(g.geoms, key=lambda q: q.area)
    out.append({'i': i, 'pts': [[round(a, 2), round(b, 2)] for a, b in list(g.exterior.coords)[:-1]]})
json.dump(out, open(os.path.join(os.environ['TEMP'], 'bl', 'rooms.json'), 'w'))
print('rooms', len(out))
