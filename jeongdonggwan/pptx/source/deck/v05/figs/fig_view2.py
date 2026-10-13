from fig_ds import *
import shapely, math
from geo import ll2m
from matplotlib.patches import Patch, Polygon as MP, FancyArrowPatch
XL = (-120, 200); YL = (-85, 215)

# ================= view profile =================
LM = {'황령산 정상': ((35.1573354, 129.0819088), 427.0), 'BIFC': ((35.14641389, 129.06485), 289.0)}
GZ = 8.0
tc = TERR.centroid
eyes = {'1층 가로': (Point(-14, 60), 1.6), '옥상 광장': (Point(tc.x, tc.y), 21.1 + 1.6)}
az = np.arange(0, 360, 0.5)
obst = [(Polygon(b['pts']).buffer(0), b['h']) for b in CTX['buildings']] + [(q, h) for g, h in PARTS for q in polys(g)]
def skyline(eye, eh):
    rays = np.array([LineString([(eye.x, eye.y), (eye.x + 500 * math.sin(math.radians(a)), eye.y + 500 * math.cos(math.radians(a)))]) for a in az], dtype=object)
    best = np.full(len(az), -90.0)
    for poly, h in obst:
        if h <= eh: continue
        inter = shapely.intersection(rays, poly)
        ok = ~shapely.is_empty(inter)
        if not ok.any(): continue
        d = np.maximum(shapely.distance(inter[ok], eye), 1.0)
        ang = np.degrees(np.arctan2(h - eh, d)); idx = np.where(ok)[0]
        best[idx] = np.maximum(best[idx], ang)
    return best
res = {n: skyline(e, h) for n, (e, h) in eyes.items()}
fig, ax = plt.subplots(figsize=(12.2, 1.72))
ax.set_facecolor(PANEL)
ax.fill_between(az, -6, np.maximum(res['옥상 광장'], -6), color=D1, step='mid', zorder=3, label='옥상 광장(+21.1m)에서 본 스카이라인')
ax.fill_between(az, -6, np.minimum(np.maximum(res['1층 가로'], -6), 40), color='#bdbdbd', alpha=0.55, step='mid', zorder=2, label='1층 가로에서 본 스카이라인')
ax.axhline(0, color=INK, lw=1, zorder=5)
for k, ((la, lo), h) in LM.items():
    x, y = ll2m(la, lo)
    eye, eh = eyes['옥상 광장']
    dx, dy = x - eye.x, y - eye.y; d = math.hypot(dx, dy); a = (math.degrees(math.atan2(dx, dy)) + 360) % 360
    top = math.degrees(math.atan2(h - GZ - eh, d))
    ax.plot([a, a], [-6, top], color=PIN, lw=3.2, zorder=6, solid_capstyle='butt')
    ax.plot([a], [top], marker='v', color=PIN, ms=9, zorder=7)
    pos = (a - 78, 31.0) if k == '황령산 정상' else (a + 14, 28.0)
    ax.annotate(f'{k}  {h:.0f}m\n방위 {a:.0f}° · {d/1000:.2f}km · 앙각 {top:.1f}°', xy=(a, top), xytext=pos, fontsize=10, fontweight='bold', color=PIN,
                va='center', ha='left', arrowprops=dict(arrowstyle='-', color=PIN, lw=1.1), zorder=8, bbox=dict(fc='white', ec=PIN, lw=0.8, pad=3))
ax.set_xlim(0, 360); ax.set_ylim(-6, 38)
ax.set_xticks([0, 45, 90, 135, 180, 225, 270, 315, 360])
ax.set_xticklabels(['북 0°', '북동 45°', '동 90°', '남동 135°', '남 180°', '남서 225°', '서 270°', '북서 315°', '북 360°'], fontsize=10)
ax.set_yticks([0, 10, 20, 30]); ax.set_yticklabels(['0°', '10°', '20°', '30°'], fontsize=9.5, color=MUTED)
ax.grid(axis='both', color='white', lw=1.0, zorder=0)
for s in ax.spines.values(): s.set_visible(False)
ax.tick_params(length=0)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=2, frameon=False, fontsize=10)
save(fig, 'view_profile')
print('ok')
