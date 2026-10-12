# extract OSM context (buildings w/ heights, roads) around the block into local metres
import sys, json, math
sys.path.insert(0, '..'); sys.path.insert(0, '.')
from geo import ll2m, POLY_M
from shapely.geometry import Polygon, LineString
import xml.etree.ElementTree as ET
S = '/tmp/claude-0/-home-user-cloud/76ed2005-4113-58c6-b90f-f280afa8844d/scratchpad'
t = ET.parse(S + '/osm/map.osm').getroot()
nodes = {n.get('id'): ll2m(float(n.get('lat')), float(n.get('lon'))) for n in t.findall('node')}
block = Polygon(POLY_M['W']).union(Polygon(POLY_M['R'])).union(Polygon(POLY_M['E']))
cx, cy = block.centroid.x, block.centroid.y
R = 420
blds, roads = [], []
W = {'trunk': 22, 'primary': 30, 'secondary': 24, 'tertiary': 12, 'residential': 7, 'unclassified': 6,
     'service': 4, 'living_street': 5, 'secondary_link': 7, 'trunk_link': 7, 'pedestrian': 5, 'footway': 2.5}
for w in t.findall('way'):
    tg = {x.get('k'): x.get('v') for x in w.findall('tag')}
    pts = [nodes[nd.get('ref')] for nd in w.findall('nd') if nd.get('ref') in nodes]
    if len(pts) < 2: continue
    if 'building' in tg and len(pts) >= 4:
        p = Polygon(pts).buffer(0)
        if p.is_empty or p.area < 15: continue
        if math.hypot(p.centroid.x - cx, p.centroid.y - cy) > R: continue
        if p.intersection(block.buffer(-1)).area > 0.3 * p.area: continue  # drop existing buildings on our site
        if 'height' in tg:
            try: h = float(tg['height'].replace('m', ''))
            except: h = None
        else: h = None
        if h is None:
            lv = tg.get('building:levels')
            try: h = float(lv) * 3.3 + 1
            except: h = 3 * 3.2 + 1 if p.area < 400 else 5 * 3.3
        if p.geom_type != 'Polygon': p = max(p.geoms, key=lambda g: g.area)
        blds.append({'pts': [list(map(lambda v: round(v, 2), c)) for c in p.exterior.coords][:-1], 'h': round(h, 1)})
    elif 'highway' in tg and tg['highway'] in W:
        ls = LineString(pts)
        if ls.distance(block.centroid) > R + 100: continue
        width = W[tg['highway']]
        if tg.get('lanes'):
            try: width = max(width, int(tg['lanes']) * 3.3)
            except: pass
        roads.append({'pts': [[round(x, 2), round(y, 2)] for x, y in pts], 'w': width, 'name': tg.get('name', ''), 'hw': tg['highway']})
json.dump({'buildings': blds, 'roads': roads, 'center': [cx, cy]}, open(S + '/build/render/context.json', 'w'))
print(len(blds), len(roads), round(cx, 1), round(cy, 1))
import collections
print(sorted([b['h'] for b in blds])[-15:])
