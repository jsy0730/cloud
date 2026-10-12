# 볼륨 도출 5단계 axonometric (SVG)
import sys, math
sys.path.insert(0, '/tmp/claude-0/-home-user-cloud/76ed2005-4113-58c6-b90f-f280afa8844d/scratchpad/build')
from numbers_base import *
from shapely.geometry import box
from shapely.ops import unary_union
H = B.bounds[3]
Rw = R.intersection(W.buffer(3.0, join_style=2)); Re = R.difference(Rw)
PW = BF.intersection(unary_union([W, Rw]).buffer(0.01)); PE = BF.intersection(unary_union([E, Re]).buffer(0.01))
def cut_y(g, y0, y1): return g.intersection(box(-50, y0, 120, y1))
sc = 2.15
def iso(x, y, z, ox, oy):
    a = math.radians(30)
    return (ox + (x + y * 0.55) * math.cos(a) * sc * 1.0 - y * 0.0, oy - (y * 0.62 + z * 1.0 - x * 0.18) * sc)
COL = dict(site='#e9e6df', W='#fbf3a4', E='#f4d3b0', lane='#9a9a9a', park='#d9b48f', park2='#c79f78', cult='#9dc3e6', biz='#fbf3a4', core='#d2432a', roof='#a9d18e', off='#d9cbe9')
def shade(c, f):
    c = c.lstrip('#'); r, g, b = (int(c[i:i + 2], 16) for i in (0, 2, 4)); return '#%02x%02x%02x' % tuple(int(v * f) for v in (r, g, b))
def prisms(items, ox, oy):
    # items: (geom, z0, h, color) ; painter by (z0, -centroid y)
    polys = []
    for g, z0, h, c in items:
        for p in polys_of(g): polys.append((p, z0, h, c))
    polys.sort(key=lambda t: (t[1], -(t[0].centroid.y) + t[0].centroid.x * 0.3))
    out = []
    for p, z0, h, c in polys:
        pts = list(p.exterior.coords)[:-1]
        if not p.exterior.is_ccw: pts = pts[::-1]
        faces = []
        for i in range(len(pts)):
            (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % len(pts)]
            nx, ny = (y2 - y1), -(x2 - x1)
            L = math.hypot(nx, ny) or 1
            vis = (-ny * 0.62 + nx * 0.18) / L  # facing viewer (south / west-ish)
            if vis > -0.05 and h > 0.01: faces.append(((x1, y1), (x2, y2), nx / L, ny / L))
        faces.sort(key=lambda f: -(f[0][1] + f[1][1]))
        for (x1, y1), (x2, y2), nx, ny in faces:
            f = 0.78 if abs(nx) > abs(ny) else 0.66
            q = [iso(x1, y1, z0, ox, oy), iso(x2, y2, z0, ox, oy), iso(x2, y2, z0 + h, ox, oy), iso(x1, y1, z0 + h, ox, oy)]
            out.append('<polygon points="%s" fill="%s" stroke="#2b2b2b" stroke-width="0.8"/>' % (' '.join('%.1f,%.1f' % v for v in q), shade(c, f)))
        top = [iso(x, y, z0 + h, ox, oy) for x, y in pts]
        out.append('<polygon points="%s" fill="%s" stroke="#2b2b2b" stroke-width="0.8"/>' % (' '.join('%.1f,%.1f' % v for v in top), c))
    return out
def polys_of(g):
    if g.is_empty: return []
    if g.geom_type == 'Polygon': return [g] if g.area > 1 else []
    return [p for p in getattr(g, 'geoms', []) if p.geom_type == 'Polygon' and p.area > 1]
steps = []
# 1 merge
steps.append(('① 53필지 합필', '서측+소로+동측 4,964.5㎡', [(W, 0, 0.6, COL['W']), (R, 0, 0.3, COL['lane']), (E, 0, 0.6, COL['E'])]))
# 2 lane kept as car lane, 1F 7m pilotis
steps.append(('② 소로 = 차량 전용 차로', '1층 층고 7m, 차로 위는 비움', [(B, -0.01, 0.01, COL['site']), (W1, 0, 7, COL['W']), (E1, 0, 7, COL['E']), (R, 0, 0.2, COL['lane'])]))
# 3 one slab from 2F + 3m setback
steps.append(('③ 2층부터 한 판 + 3m 이격', '소로 위로 이은 바닥 · 북남 3m', [(B, -0.01, 0.01, COL['site']), (W.intersection(SB), 0, 7, COL['W']), (E.intersection(SB), 0, 7, COL['E']), (R, 0, 0.2, COL['lane']), (B.intersection(SB), 7, 14.1, COL['park'])]))
# 4 tips removed -> open stair cores
steps.append(('④ 두 끝을 비워 코어', '순환 계단 + 승강기 · 건폐율 87.1%', [(B, -0.01, 0.01, COL['site']), (W1, 0, 7, COL['W']), (E1, 0, 7, COL['E']), (R, 0, 0.2, COL['lane']), (BF, 7, 14.1, COL['park']), (tE.intersection(SB), 0, 29.8, COL['core']), (tW, 0, 21.6, COL['core'])]))
# 5 skip floors + hall + terrace (+ theatre underground mark)
y6 = 36.8
items5 = [(B, -0.01, 0.01, COL['site']), (W1, 0, 7, COL['W']), (E1, 0, 8.65, COL['E']), (R, 0, 0.2, COL['lane'])]
for i, z in enumerate((7.0, 10.3, 13.6)): items5.append((PW, z, 3.3, COL['park'] if i % 2 == 0 else COL['park2']))
for i, (z, h) in enumerate(((8.65, 3.3), (11.95, 3.3), (15.25, 1.65))): items5.append((PE, z, h, COL['park2'] if i % 2 == 0 else COL['park']))
items5 += [(cut_y(BF, -5, 63), 16.9, 4.2, COL['park']), (cut_y(BF, 63, 200), 16.9, 4.2, COL['off']), (cut_y(BF, y6, 200), 21.1, 8.0, COL['cult']), (cut_y(BF, -5, y6), 21.1, 0.5, COL['roof']),
           (tE.intersection(SB), 0, 29.8, COL['core']), (tW, 0, 21.6, COL['core'])]
steps.append(('⑤ 스킵플로어 · 홀 · 광장', '소로를 이음매로 반 층 · 6F 가변홀 · 옥상 광장', items5))
Wd, Hd = 1920, 560
svg = []
pw = Wd / 5
for i, (t1, t2, items) in enumerate(steps):
    ox = i * pw + 70; oy = 430
    svg += prisms(items, ox, oy)
    svg.append(f'<text x="{i * pw + pw / 2:.0f}" y="490" font-size="27" font-weight="700" text-anchor="middle">{t1}</text>')
    svg.append(f'<text x="{i * pw + pw / 2:.0f}" y="526" font-size="21" text-anchor="middle" fill="#595959">{t2}</text>')
    if i: svg.append(f'<text x="{i * pw + 6:.0f}" y="300" font-size="40" fill="#a0a2a5">›</text>')
html = f'<html><head><link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.css"></head><body style="margin:0"><svg xmlns="http://www.w3.org/2000/svg" width="{Wd}" height="{Hd}" font-family="Pretendard, sans-serif"><rect width="100%" height="100%" fill="#fff"/>' + ''.join(svg) + '</svg></body></html>'
open('/tmp/claude-0/-home-user-cloud/76ed2005-4113-58c6-b90f-f280afa8844d/scratchpad/build/diag/volume.html', 'w').write(html)
print('ok')
