# Gongseolgi v1.2 styled figures (flat plan-diagram language)
import sys; sys.path.insert(0, '.')
from env_common import *          # geometry, sunpos, shadow, CTX, PARTS, SITE, XE, polys ...
from matplotlib.patches import Rectangle
for n in ('Regular', 'Medium', 'Bold', 'ExtraBold'):
    fm.fontManager.addfont(f'fonts/Pretendard-{n}.ttf')
plt.rcParams['font.family'] = 'Pretendard'
plt.rcParams['axes.unicode_minus'] = False
# tokens (light theme)
SURF = '#ffffff'; PANEL = '#f0f3f7'; SOFT = '#f2f2f2'; INK = '#000000'; MUTED = '#595959'; LINE = '#a0a2a5'
NAVY = '#002060'; NAVYSOFT = '#dae3f3'; SLATE = '#8493b2'; PIN = '#c00000'; SIGNAL = '#ff0000'; GOLD = '#ffc000'
D1, D2, D3, D4, D5 = '#08205e', '#4272c4', '#7f9dcf', '#abbde0', '#dbe2f5'
CHAR = '#525252'; PARK = '#c9c9c9'; CELL = '#e7e6e6'
ZACT = '#b4c7e7'; ZRAMP = '#d4e6c7'; ZQUIET = '#eebbba'; ZCORE = '#ec8080'
WALK = '#ed7d31'; DRIVE = '#00b0ef'; VERT = '#7030a0'
FROOF = '#e2f0d9'; FFLEX = '#8faadc'; FCULT = '#b4c7e7'; FENTRY = '#dae3f3'


def base_map(ax, xl, yl):
    ax.add_patch(Rectangle((xl[0], yl[0]), xl[1] - xl[0], yl[1] - yl[0], fc=PANEL, ec='none', zorder=0))
    for r in CTX['roads']:
        xs = [p[0] for p in r['pts']]; ys = [p[1] for p in r['pts']]
        if max(xs) < xl[0] - 60 or min(xs) > xl[1] + 60 or max(ys) < yl[0] - 60 or min(ys) > yl[1] + 60:
            continue
        ax.plot(xs, ys, color='white', lw=max(1.0, r['w'] * 0.42), solid_capstyle='butt', solid_joinstyle='round', zorder=1)
    for b in CTX['buildings']:
        xs = [p[0] for p in b['pts']]; ys = [p[1] for p in b['pts']]
        if max(xs) < xl[0] - 30 or min(xs) > xl[1] + 30 or max(ys) < yl[0] - 30 or min(ys) > yl[1] + 30:
            continue
        col = '#c9c9c9' if b['h'] >= 45 else ('#d9d9d9' if b['h'] >= 20 else '#e4e4e4')
        ax.add_patch(MPoly(b['pts'], closed=True, fc=col, ec='none', zorder=2))
    ax.set_xlim(*xl); ax.set_ylim(*yl); ax.set_aspect('equal'); ax.axis('off')


def site_outline(ax, z=7):
    for q in polys(SITE):
        ax.add_patch(MPoly(list(q.exterior.coords), closed=True, fc='none', ec=PIN, lw=1.8, zorder=z))


def mass(ax, z=6):
    u = unary_union([g for g, h in PARTS]).buffer(0.05)
    for q in polys(u):
        ax.add_patch(MPoly(list(q.exterior.coords), closed=True, fc=CHAR, ec='none', zorder=z))


def north(ax, x, y, s=16):
    ax.add_patch(MPoly([[x, y + s], [x - s * 0.28, y], [x, y + s * 0.3], [x + s * 0.28, y]], closed=True, fc=INK, ec='none', zorder=20))
    ax.text(x, y + s * 1.18, 'N', ha='center', va='bottom', fontsize=9.5, fontweight='bold', color=INK, zorder=20)


def scale_bar(ax, x, y, L=20):
    ax.plot([x, x + L], [y, y], color=INK, lw=2, solid_capstyle='butt', zorder=20)
    ax.plot([x, x], [y - 1.2, y + 1.2], color=INK, lw=1, zorder=20)
    ax.plot([x + L, x + L], [y - 1.2, y + 1.2], color=INK, lw=1, zorder=20)
    ax.text(x + L / 2, y + 2.4, f'{L}m', ha='center', va='bottom', fontsize=8.5, color=INK, zorder=20)


def zone_line(ax, yl, label=True):
    ax.plot([XE + 45, XE + 45], [yl[0], yl[1]], color=NAVY, lw=1.2, ls=(0, (5, 4)), zorder=8)
    if label:
        ax.text(XE + 47, yl[0] + 22, '제3종일반주거지역 →', fontsize=8.5, color=NAVY, va='bottom', ha='left', fontweight='medium', zorder=9)


def save(fig, name, dpi=220):
    fig.savefig(f'img/{name}.png', dpi=dpi, facecolor='white', bbox_inches='tight', pad_inches=0.06)
    plt.close(fig)
