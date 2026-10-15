from fig_ds import *
import shapely, math
from geo import ll2m
from matplotlib.patches import Patch, Polygon as MP, FancyArrowPatch
XL = (-120, 200); YL = (-85, 215)

# ================= noise map =================
REF = {'secondary': 70, 'primary': 72, 'trunk': 72, 'tertiary': 63, 'residential': 58, 'unclassified': 58, 'service': 52,
       'living_street': 50, 'secondary_link': 64, 'trunk_link': 66, 'pedestrian': 40, 'footway': 35}
lines = []
for r in CTX['roads']:
    if len(r['pts']) < 2: continue
    ls = LineString(r['pts'])
    if ls.distance(Point(21, 63)) > 450: continue
    lines.append((ls, REF.get(r['hw'], 55)))
SRC = []
for ls, L0 in lines:
    n = max(1, int(ls.length / 5)); dl = ls.length / n
    for i in range(n):
        p = ls.interpolate((i + 0.5) * dl)
        SRC.append((p.x, p.y, 10 ** (L0 / 10) * 10.0 * dl / math.pi))
SRC = np.array(SRC)
def levels(X, Y):
    I = np.zeros_like(X, dtype=float)
    for sx, sy, e in SRC:
        I += e / ((X - sx) ** 2 + (Y - sy) ** 2 + 9.0)
    return 10 * np.log10(I)
xs = np.arange(XL[0], XL[1], 2.5); ys = np.arange(YL[0], YL[1], 2.5); X, Y = np.meshgrid(xs, ys)
Z = levels(X, Y)
fig, ax = plt.subplots(figsize=(5.6, 5.5))
base_map(ax, XL, YL)
lv = [0, 62, 65, 68, 71, 120]
cols = [D5, D4, D3, D2, D1]
ax.contourf(X, Y, Z, levels=lv, colors=cols, alpha=0.80, zorder=3)
cs = ax.contour(X, Y, Z, levels=[65, 70], colors=[NAVY], linewidths=[0.8, 1.3], zorder=4)
ax.clabel(cs, fmt=lambda v: f'{v:.0f}', fontsize=8, inline=True)
mass(ax); site_outline(ax)
ax.plot([XE + 45, XE + 45], [YL[0], YL[1]], color='#222', lw=1.1, ls=(0, (5, 4)), zorder=8)
pts = {'서': (-2, 60), '북': (21, 131), '남': (20, -4), '동': (XE + 4, 60), '주거\n경계': (XE + 45, 60)}
for k, (x, y) in pts.items():
    ax.plot([x], [y], 'o', ms=6.5, mfc='white', mec=INK, mew=1.4, zorder=12)
    dx = {'서': -16, '북': 0, '남': 0, '동': 15, '주거\n경계': 14}[k]; dy = {'서': 0, '북': 11, '남': -12, '동': 0, '주거\n경계': 0}[k]
    ax.text(x + dx, y + dy, k, fontsize=9.5, fontweight='bold', ha='center', va='center', zorder=13,
            bbox=dict(fc='white', ec='none', pad=1.2, alpha=0.9))
north(ax, XL[0] + 14, YL[0] + 8); scale_bar(ax, XL[1] - 48, YL[0] + 8, 40)
lab = ['62 미만', '62~65', '65~68', '68~71', '71 이상']
ax.legend(handles=[Patch(fc=c, label=l) for c, l in zip(cols, lab)], loc='upper center', bbox_to_anchor=(0.5, 0.0), ncol=5,
          frameon=False, fontsize=9, handlelength=1.2, columnspacing=1.0, borderaxespad=0.4, title='주간 Leq 추정 dB(A) · 가정 교통량 · 건물 차폐 미반영', title_fontsize=9)
save(fig, 'noise_map')
for k, (x, y) in pts.items():
    print(k.replace('\n', ''), round(float(levels(np.array([x]), np.array([y]))[0]), 1))

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
fig, ax = plt.subplots(figsize=(12.2, 2.35))
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
    pos = (a - 78, 28.5) if k == '황령산 정상' else (a + 14, 25)
    ax.annotate(f'{k}  {h:.0f}m\n방위 {a:.0f}° · {d/1000:.2f}km · 앙각 {top:.1f}°', xy=(a, top), xytext=pos, fontsize=10, fontweight='bold', color=PIN,
                va='center', ha='left', arrowprops=dict(arrowstyle='-', color=PIN, lw=1.1), zorder=8, bbox=dict(fc='white', ec=PIN, lw=0.8, pad=3))
ax.set_xlim(0, 360); ax.set_ylim(-6, 36)
ax.set_xticks([0, 45, 90, 135, 180, 225, 270, 315, 360])
ax.set_xticklabels(['북 0°', '북동 45°', '동 90°', '남동 135°', '남 180°', '남서 225°', '서 270°', '북서 315°', '북 360°'], fontsize=10)
ax.set_yticks([0, 10, 20, 30]); ax.set_yticklabels(['0°', '10°', '20°', '30°'], fontsize=9.5, color=MUTED)
ax.grid(axis='both', color='white', lw=1.0, zorder=0)
for s in ax.spines.values(): s.set_visible(False)
ax.tick_params(length=0)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.12), ncol=2, frameon=False, fontsize=10)
save(fig, 'view_profile')

# ================= case diagrams =================
def dim_v(ax, x, y0, y1, txt, col=MUTED, side='r'):
    ax.annotate('', xy=(x, y1), xytext=(x, y0), arrowprops=dict(arrowstyle='<->', color=col, lw=1.1))
    ax.text(x + (0.25 if side == 'r' else -0.25), (y0 + y1) / 2, txt, va='center', ha='left' if side == 'r' else 'right', fontsize=10, color=INK, linespacing=1.25)
# --- 1111 Lincoln Road: open slab section, floor height varies
fig, ax = plt.subplots(figsize=(6.4, 4.2))
hs = [4.4, 2.1, 2.1, 2.1, 3.2, 2.1, 7.4]
cols_ = [FENTRY, PARK, PARK, PARK, FCULT, PARK, FFLEX]
names = ['상업·카페', '주차', '주차', '주차', '전환 층', '주차', '행사·문화']
y = 0; ys_ = []
for h, c, n in zip(hs, cols_, names):
    ax.add_patch(Rectangle((0.6, y), 10.8, h, fc=c, ec='none', alpha=0.55, zorder=1))
    ax.add_patch(Rectangle((0, y - 0.22), 12, 0.22, fc=CHAR, ec='none', zorder=3))
    ys_.append((y, h, n)); y += h + 0.22
ax.add_patch(Rectangle((0, y - 0.22), 12, 0.22, fc=CHAR, ec='none', zorder=3))
for x in (1.2, 4.4, 7.6, 10.8):
    ax.add_patch(MP([[x, 0], [x + 0.42, 0], [x + 0.78, y], [x + 0.36, y]], closed=True, fc='#9aa3b2', ec='none', zorder=2))
for (y0, h, n) in ys_:
    ax.text(6.0, y0 + h / 2, n, ha='center', va='center', fontsize=10, color=INK, zorder=4, fontweight='medium')
dim_v(ax, 12.5, ys_[1][0], ys_[1][0] + ys_[1][1], '약 2.1m\n(주차층 7ft)')
dim_v(ax, 12.5, ys_[6][0], ys_[6][0] + ys_[6][1], '최대 약 10.4m\n(34ft)')
ax.text(6, -1.1, '외벽 없이 슬래브 · 기둥 · 램프로만 구성', ha='center', va='top', fontsize=10.5, color=NAVY, fontweight='bold')
ax.set_xlim(-0.4, 17.5); ax.set_ylim(-2.4, y + 0.6); ax.axis('off')
save(fig, 'diag_lincoln')
# --- skip floor concept
fig, ax = plt.subplots(figsize=(6.4, 4.2))
H = 3.0
for i in range(4):
    y0 = i * 2 * H
    ax.add_patch(Rectangle((0.4, y0), 5.4, 0.3, fc=NAVY, ec='none'))
    ax.add_patch(Rectangle((7.0, y0 + H), 5.4, 0.3, fc=D2, ec='none'))
    ax.add_patch(MP([[5.8, y0], [7.0, y0 + H], [7.0, y0 + H + 0.3], [5.8, y0 + 0.3]], closed=True, fc=DRIVE, ec='none'))
    if i < 3:
        ax.add_patch(MP([[7.0, y0 + H], [5.8, y0 + 2 * H], [5.8, y0 + 2 * H + 0.3], [7.0, y0 + H + 0.3]], closed=True, fc=DRIVE, ec='none'))
dim_v(ax, 12.9, 0, H, '반 층')
ax.text(3.1, -1.2, 'A판', ha='center', va='top', fontsize=11, fontweight='bold', color=NAVY)
ax.text(9.7, -1.2, 'B판 (반 층 엇갈림)', ha='center', va='top', fontsize=11, fontweight='bold', color=D2)
ax.text(6.4, 4 * 2 * H + 0.4, '램프가 반 층 높이만 오르내려 길이와 면적이 줄어듦', ha='center', va='bottom', fontsize=10.5, color=NAVY, fontweight='bold')
ax.set_xlim(-0.2, 16.5); ax.set_ylim(-2.4, 4 * 2 * H + 1.6); ax.axis('off')
save(fig, 'diag_skip')
print('ok')
