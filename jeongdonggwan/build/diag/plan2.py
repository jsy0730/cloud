import sys
sys.path.insert(0, '/tmp/claude-0/-home-user-cloud/76ed2005-4113-58c6-b90f-f280afa8844d/scratchpad/build')
from numbers_base import *
from shapely.geometry import box, Point
H = B.bounds[3]; s = 6.4; ox, oy = 250, 70
def X(x): return ox + x * s
def Yp(y): return oy + (H - y) * s
def P(g):
    out = []
    for p in polys(g): out.append(' '.join(f'{X(x):.1f},{Yp(y):.1f}' for x, y in p.exterior.coords))
    return out
def cut_y(g, y0, y1): return g.intersection(box(-50, y0, 120, y1))
o = []; T = []
def poly(g, fill, stroke='#000', sw=1.5, extra=''):
    for pts in P(g): o.append(f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>')
def t(x, y, s_, size=19, anchor='middle', w=400, fill='#000', halo=False): size = round(size * 1.28); hs = ' stroke="#fff" stroke-width="5" paint-order="stroke" stroke-linejoin="round"' if halo else ''; T.append(f'<text{hs} x="{x:.0f}" y="{y:.0f}" font-size="{size}" text-anchor="{anchor}" font-weight="{w}" fill="{fill}">{s_}</text>')
Wd = 40.7
# roads
o.append(f'<rect x="{X(-22)}" y="{oy - 46}" width="{22 * s}" height="{H * s + 92}" fill="#d9d9d9"/>')
o.append(f'<rect x="{X(-22)}" y="{oy - 46}" width="{(Wd + 30) * s}" height="44" fill="#d9d9d9"/>')
o.append(f'<rect x="{X(-22)}" y="{Yp(0) + 2}" width="{(Wd + 30) * s}" height="44" fill="#d9d9d9"/>')
o.append(f'<rect x="{X(Wd) + 4}" y="{oy - 46}" width="{6 * s}" height="{H * s + 92}" fill="#e6e6e6"/>')
# setback strips (pedestrian)
poly(B.difference(SB), '#fff3e3', '#c8a27a', 1, 'stroke-dasharray="4 3"')
# programmes
poly(cut_y(W1, 80, 200), '#fbf3a4'); poly(cut_y(W1, 0, 80), '#fbf3a4')
poly(cut_y(E1, 0, 30), '#fbf3a4'); poly(cut_y(E1, 30, 200), '#f4d3b0')
poly(L1, '#8c8c8c'); poly(R.difference(SB), '#8c8c8c')
poly(tE.intersection(SB), '#ec8080', '#c00000', 2.5); poly(tW, '#ec8080', '#c00000', 2.5)
poly(tE.difference(SB), '#ec8080', '#c00000', 1)
# labels
c = cut_y(W1, 80, 200).centroid; t(X(c.x) - 6, Yp(c.y) - 10, '서점', 22, w=700); t(X(c.x) - 6, Yp(c.y) + 22, '400㎡', 17)
c = cut_y(W1, 62, 80).centroid; t(X(c.x) - 4, Yp(c.y) - 4, '카페', 18, w=700); t(X(c.x) - 4, Yp(c.y) + 24, '400㎡', 17)
c = cut_y(W1, 55, 62).centroid; t(X(c.x) - 2, Yp(c.y) + 8, '공연 로비', 16, w=700)
c = cut_y(E1, 0, 30).centroid; t(X(c.x) + 10, Yp(c.y) - 30, '근생 소점포', 20, w=700); t(X(c.x) + 10, Yp(c.y) + 2, '600㎡', 16); t(X(c.x) + 10, Yp(c.y) + 30, '10곳 안팎', 16)
c = cut_y(E1, 30, 62).centroid; t(X(c.x) + 14, Yp(c.y), '오르내림', 19, w=700); t(X(c.x) + 14, Yp(c.y) + 30, '램프', 19, w=700); t(X(c.x) + 14, Yp(c.y) + 62, '정산·관리', 16)
c = cut_y(E1, 70, 85).centroid; t(X(c.x) + 8, Yp(c.y) - 12, '이륜차·', 17, w=700); t(X(c.x) + 8, Yp(c.y) + 16, '자전거', 17, w=700); t(X(c.x) + 8, Yp(c.y) + 44, '하역', 15)
c = tE.intersection(SB).centroid; t(X(c.x), Yp(c.y) - 14, '끝 코어①', 14, w=700, fill='#8b0000'); t(X(c.x), Yp(c.y) + 18, '순환 계단', 13); t(X(c.x), Yp(c.y) + 42, '승강기', 13)
c = tW.centroid; t(X(c.x) + 2, Yp(c.y) - 12, '코어②', 14, w=700, fill='#8b0000'); t(X(c.x) + 2, Yp(c.y) + 16, '선큰', 13)
# aux stairs
for (x, y) in ((3.5, H - 6), (Wd - 4, 6)):
    o.append(f'<rect x="{X(x) - 12}" y="{Yp(y) - 12}" width="24" height="24" fill="#c00000"/>')
t(X(3.5) + 18, Yp(H - 6) + 8, '보조 계단', 14, anchor='start', fill='#8b0000'); t(X(Wd - 4) - 18, Yp(6) + 8, '보조 계단', 14, anchor='end', fill='#8b0000')
# lane arrows: entry south end (from 전포대로), exit north end (to 서전로)
south = R.intersection(box(-1, -10, 0.6, 200)).centroid
sx, sy = X(south.x), Yp(south.y)
o.append(f'<line x1="{sx - 120}" y1="{sy}" x2="{sx - 6}" y2="{sy}" stroke="#00b0ef" stroke-width="7"/><polygon points="{sx - 8},{sy - 13} {sx - 8},{sy + 13} {sx + 14},{sy}" fill="#00b0ef"/>')
t(sx - 128, sy - 14, '진입 (전포대로 → 소로 남단)', 14, anchor='start', w=700, fill='#0070c0', halo=True)
north = R.intersection(box(-10, H - 0.6, 80, H + 1)).centroid
nx_, ny_ = X(north.x), Yp(north.y)
o.append(f'<line x1="{nx_}" y1="{ny_ + 4}" x2="{nx_}" y2="{ny_ - 40}" stroke="#00b0ef" stroke-width="7"/><polygon points="{nx_ - 13},{ny_ - 38} {nx_ + 13},{ny_ - 38} {nx_},{ny_ - 60}" fill="#00b0ef"/>')
t(nx_ - 24, ny_ - 42, '진출 (소로 북단 → 서전로)', 14, anchor='end', w=700, fill='#0070c0', halo=True)
# flow arrows along lane
for yy in (25, 50, 75, 100):
    cc = R.intersection(box(-10, yy - 0.3, 80, yy + 0.3)).centroid
    o.append(f'<polygon points="{X(cc.x) - 7},{Yp(cc.y) + 6} {X(cc.x) + 7},{Yp(cc.y) + 6} {X(cc.x)},{Yp(cc.y) - 10}" fill="#ffffff"/>')
# crosswalk mid (between entry ramps and exit)
cy = 65
cw = R.intersection(box(-10, cy - 1.6, 80, cy + 1.6))
for pts in P(cw): o.append(f'<polygon points="{pts}" fill="url(#zebra)" stroke="#fff" stroke-width="1"/>')
c = cw.centroid; t(X(c.x) + 60, Yp(c.y) + 46, '횡단보도', 16, anchor='start', w=700, fill='#ed7d31', halo=True)
o.append(f'<line x1="{X(c.x) + 8}" y1="{Yp(c.y)}" x2="{X(c.x) + 56}" y2="{Yp(c.y) + 34}" stroke="#ed7d31" stroke-width="2"/>')
# pedestrian loop (orange dashed) around perimeter outside
loop = [(-2.2, -2.0), (-2.2, H + 1.8), (Wd + 2.0, H + 1.8), (Wd + 2.0, -2.0)]
o.append('<polygon points="' + ' '.join(f'{X(x):.1f},{Yp(y):.1f}' for x, y in loop) + '" fill="none" stroke="#ed7d31" stroke-width="4" stroke-dasharray="12 8"/>')
t(X(-11), Yp(H / 2), '전포대로 (광로)', 18, w=700)
T.append(f'<text x="{X(-11)}" y="{Yp(H / 2)}" font-size="0"/>')
t(X(-2), oy - 14, '서전로', 17, anchor='start', w=700); t(X(-2), Yp(0) + 38, '전포대로224번길', 17, anchor='start', w=700)
T.append(f'<text x="{X(Wd) + 4 + 3 * s}" y="{Yp(H / 2)}" font-size="20" text-anchor="middle" transform="rotate(90 {X(Wd) + 4 + 3 * s} {Yp(H / 2)})">동측 이면도로</text>')
# north arrow
o.append(f'<polygon points="{X(Wd) + 80},{oy + 40} {X(Wd) + 92},{oy + 10} {X(Wd) + 104},{oy + 40}" fill="#000"/>'); t(X(Wd) + 92, oy + 74, 'N', 16, w=700)
Wd_px, Hd_px = 660, int(oy + H * s + 80)
defs = '<defs><pattern id="zebra" width="10" height="10" patternUnits="userSpaceOnUse"><rect width="10" height="10" fill="#8c8c8c"/><rect width="5" height="10" fill="#ffffff"/></pattern></defs>'
svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{Wd_px}" height="{Hd_px}" font-family="Pretendard, sans-serif">{defs}<rect width="100%" height="100%" fill="#fff"/>' + ''.join(o) + ''.join(T) + '</svg>'
open('/tmp/claude-0/-home-user-cloud/76ed2005-4113-58c6-b90f-f280afa8844d/scratchpad/build/diag/plan2.html', 'w').write('<html><head><link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.css"></head><body style="margin:0">' + svg + '</body></html>')
print(Wd_px, Hd_px)
