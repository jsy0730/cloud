import sys, os, json, math, io, contextlib
T = os.environ['TEMP'].replace(chr(92), '/')
RB = T + '/cloud_repo/jeongdonggwan/build/'
_cwd = os.getcwd(); os.chdir(RB + 'render'); sys.path[:0] = [RB, RB + 'render', RB + 'env']
with contextlib.redirect_stdout(io.StringIO()):
    import design3 as D
os.chdir(_cwd)
from solar import sunpos
from shapely.geometry import Polygon, box, LineString, Point, MultiPolygon
from shapely.ops import unary_union
from shapely import affinity
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MPoly
from matplotlib import font_manager as fm
plt.rcParams['font.family'] = 'Malgun Gothic'; plt.rcParams['axes.unicode_minus'] = False
CTX = json.load(open(RB + 'render/context.json', encoding='utf8'))
NAVY = '#002060'; RED = '#C8102E'; BRICK = '#B5533C'; GOLD = '#FFC000'; GRAY = '#595959'; LG = '#D9DCE1'
# massing parts (frame units == metres in OSM frame), heights in metres
HALL = D.hall; TERR = D.terrace; BF = D.BF; TE = D.tE.intersection(D.SB); TW = D.tW
PARTS = [(BF.difference(HALL), 21.1), (HALL, 29.8), (TE, 29.8), (TW, 21.6)]
SITE = D.B
XE = max(x for x, y in D.POLY_M['E'])  # east edge of block
def polys(g):
    if g.is_empty: return []
    return [g] if g.geom_type == 'Polygon' else [q for q in g.geoms if q.geom_type == 'Polygon']
def shadow(poly, h, az, el):
    if el <= 0.5: return None
    L = h / math.tan(math.radians(el)); a = math.radians(az + 180)
    v = (math.sin(a) * L, math.cos(a) * L)
    import shapely
    out = [poly, affinity.translate(poly, *v)]
    c = list(poly.exterior.coords)
    for i in range(len(c) - 1):
        p, q = c[i], c[i + 1]
        if abs(p[0]-q[0]) + abs(p[1]-q[1]) < 1e-6: continue
        out.append(Polygon([p, q, (q[0] + v[0], q[1] + v[1]), (p[0] + v[0], p[1] + v[1])]))
    out = [shapely.make_valid(g).buffer(0.02) for g in out if not g.is_empty]
    return unary_union(out)
def site_shadow(az, el):
    sh = [shadow(q, h, az, el) for g, h in PARTS for q in polys(g)]
    sh = [s for s in sh if s is not None]
    return unary_union(sh) if sh else None
def draw_ctx(ax, xlim, ylim, tall=True):
    for r in CTX['roads']:
        xs = [p[0] for p in r['pts']]; ys = [p[1] for p in r['pts']]
        if max(xs) < xlim[0] - 50 or min(xs) > xlim[1] + 50 or max(ys) < ylim[0] - 50 or min(ys) > ylim[1] + 50: continue
        ax.plot(xs, ys, color='#EDEAE4', lw=max(1.2, r['w'] / 3.0), solid_capstyle='butt', zorder=1)
    for b in CTX['buildings']:
        xs = [p[0] for p in b['pts']]; ys = [p[1] for p in b['pts']]
        if max(xs) < xlim[0] - 30 or min(xs) > xlim[1] + 30 or max(ys) < ylim[0] - 30 or min(ys) > ylim[1] + 30: continue
        shade = max(0.0, min(1.0, b['h'] / 60.0))
        col = (0.86 - 0.28 * shade,) * 3
        ax.add_patch(MPoly(b['pts'], closed=True, fc=col, ec='white', lw=0.4, zorder=2))
def draw_site(ax, fc=NAVY, alpha=1.0, z=5):
    for q in polys(SITE): ax.add_patch(MPoly(list(q.exterior.coords), closed=True, fc=fc, ec='white', lw=0.6, alpha=alpha, zorder=z))
def north_arrow(ax, x, y, s=14):
    ax.annotate('', xy=(x, y + s), xytext=(x, y), arrowprops=dict(arrowstyle='-|>', color='black', lw=1.4), zorder=20)
    ax.text(x, y + s * 1.15, 'N', ha='center', va='bottom', fontsize=11, fontweight='bold', zorder=20)
