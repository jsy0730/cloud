import sys
sys.path.insert(0, '/tmp/claude-0/-home-user-cloud/76ed2005-4113-58c6-b90f-f280afa8844d/scratchpad/build')
from numbers_base import *
H = B.bounds[3]; s = 4.6; ox, oy = 90, 60
def X(x): return ox + x * s
def Yp(y): return oy + (H - y) * s
def pts(g): return [' '.join(f'{X(x):.1f},{Yp(y):.1f}' for x, y in p.exterior.coords) for p in polys(g)]
o = []; T = []
def poly(g, f, st='#000', sw=1.5):
    for p in pts(g): o.append(f'<polygon points="{p}" fill="{f}" stroke="{st}" stroke-width="{sw}"/>')
def t(x, y, s_, size=22, a='middle', w=400, fill='#000'): T.append(f'<text x="{x:.0f}" y="{y:.0f}" font-size="{size}" text-anchor="{a}" font-weight="{w}" fill="{fill}">{s_}</text>')
poly(W1, '#fbf3a4'); poly(E1, '#f4d3b0'); poly(L1, '#8c8c8c'); poly(tE.intersection(SB), '#ec8080', '#c00000', 2.2); poly(tW, '#ec8080', '#c00000', 2.2)
poly(B.difference(SB), '#fff3e3', '#c8a27a', 1)
# cut A (stepped)
A = []
for yy in range(3, int(H) - 1, 4):
    c = R.intersection(box(-10, yy - 0.3, 80, yy + 0.3))
    if not c.is_empty: A.append((c.centroid.x + 0.6, yy))
A = [(A[0][0], 0)] + A + [(A[-1][0], H)]
o.append('<polyline points="' + ' '.join(f'{X(x):.1f},{Yp(y):.1f}' for x, y in A) + '" fill="none" stroke="#1f1f1f" stroke-width="4" stroke-dasharray="14 6 3 6"/>')
t(X(A[0][0]) - 6, Yp(0) + 34, 'A', 28, w=700); t(X(A[-1][0]) + 4, Yp(H) - 16, "A'", 28, w=700)
# cut B
o.append(f'<line x1="{X(-6)}" y1="{Yp(70)}" x2="{X(47)}" y2="{Yp(70)}" stroke="#1f1f1f" stroke-width="4" stroke-dasharray="14 6 3 6"/>')
t(X(-6) - 20, Yp(70) + 10, 'B', 28, w=700); t(X(47) + 24, Yp(70) + 10, "B'", 28, w=700)
o.append(f'<polygon points="{X(Wd := 40.7) + 70},{oy + 20} {X(40.7) + 82},{oy - 10} {X(40.7) + 94},{oy + 20}" fill="#000"/>'); t(X(40.7) + 82, oy + 46, 'N', 20, w=700)
t(X(20), Yp(0) + 66, '키 플랜 (1층)', 22, w=700); t(X(20), Yp(0) + 92, 'A는 소로를 따라 펼친 선', 18, fill='#595959')
t(X(30) + 40, Yp(100), '끝 코어①', 18, 'start', 700, '#8b0000'); t(X(0) - 8, Yp(42), '끝 코어②', 18, 'end', 700, '#8b0000')
svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="420" height="{int(oy + H * s + 110)}" font-family="Pretendard, sans-serif"><rect width="100%" height="100%" fill="#fff"/>' + ''.join(o) + ''.join(T) + '</svg>'
open('keyplan.html', 'w').write('<html><head><link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.css"></head><body style="margin:0">' + svg + '</body></html>')
print(420, int(oy + H * s + 110))
