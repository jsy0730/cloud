# 정동관 단면 · 공설기 v1.2 재작도 (원본 section4.py 좌표 이식)
import os, sys
sys.path.insert(0, '.')
from vecexport import export_ax
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, FancyBboxPatch, Circle
from matplotlib import font_manager as fm
for n in ('Regular', 'Medium', 'Bold', 'ExtraBold'):
    fm.fontManager.addfont(f'fonts/Pretendard-{n}.ttf')
plt.rcParams['font.family'] = 'Pretendard'
plt.rcParams['axes.unicode_minus'] = False
import matplotlib.axes as _ma
_orig_text = _ma.Axes.text
def _snap(z): return 11.0 if z >= 10 else (9.5 if z >= 8.75 else 8.5)
def _text(self, x, y, s, *a, **k):
    k['fontsize'] = _snap(k.get('fontsize', 10))
    return _orig_text(self, x, y, s, *a, **k)
_ma.Axes.text = _text
INK = '#000000'; MUTED = '#595959'; NAVY = '#002060'; GOLD = '#FFC000'; PIN = '#C00000'
C = dict(park='#d6d6d6', mep='#a9a9a9', cult='#b4c7e7', biz='#fbf3a4', off='#eebbba', hall='#8faadc', roof='#cfe5bd', sunk='#dae3f3',
         lane='#e7e6e6', core='#ec8080', earth='#ece9e4', ent='#dae3f3')
Ln = 121.9
fig_dpi = 220


def blk(ax, a, b, z0, h, kind, label='', size=9, bold=False, ec=INK, lw=0.8, color=None):
    ax.add_patch(Rectangle((a, z0), b - a, h, fc=color or C[kind], ec=ec, lw=lw, zorder=3))
    if label:
        ax.text((a + b) / 2, z0 + h / 2, label, ha='center', va='center', fontsize=size, fontweight='bold' if bold else 'medium', color=INK, zorder=6)


def zig(ax, a, b, z0, z1, n=1.75, color=INK, lw=1.7):
    xs, zs = [], []
    z = z0; i = 0
    while z < z1 - 0.01:
        dz = min(n, z1 - z); x0, x1 = (a, b) if i % 2 == 0 else (b, a)
        xs += [x0, x1]; zs += [z, z + dz]; z += dz; i += 1
    ax.plot(xs, zs, color=color, lw=lw, zorder=7, solid_joinstyle='miter')


def badge(ax, x, z, n, r=1.55):
    ax.add_patch(Circle((x, z), r, fc=NAVY, ec='white', lw=1.4, zorder=12))
    ax.text(x, z - 0.05, str(n), ha='center', va='center', fontsize=9.5, fontweight='bold', color='white', zorder=13)


def tree(ax, x, z, s=1.0):
    ax.plot([x, x], [z, z + 2.3 * s], color='#5a4a3c', lw=1.3, zorder=5)
    ax.add_patch(Circle((x, z + 3.3 * s), 1.5 * s, fc='#9bc27d', ec='#4d7a3a', lw=0.8, zorder=5))


def hl(ax, x0, z0, w, h, color=GOLD, lw=2.2, ls='-'):
    ax.add_patch(Rectangle((x0, z0), w, h, fc='none', ec=color, lw=lw, ls=ls, zorder=9))


# ------------------------------------------------------------------ A
def section_A():
    fig = plt.figure(figsize=(9.0, 3.85), dpi=fig_dpi); ax = fig.add_axes([0, 0, 1, 1])
    ax.add_patch(Rectangle((-8, -18), Ln + 16, 18, fc=C['earth'], ec='none', zorder=0))
    ax.plot([-8, Ln + 8], [0, 0], color=INK, lw=2.2, zorder=8)
    a0, a1 = 3.0, Ln - 3.0
    # basement
    blk(ax, 0, 14, -15.6, 3.3, 'mep', '펌프·저수조', 7.5); blk(ax, 14, Ln, -15.6, 3.3, 'park', '주차')
    blk(ax, 0, 10, -12.3, 3.3, 'mep', '전기', 7.5); blk(ax, 10, Ln, -12.3, 3.3, 'park', '주차')
    blk(ax, 0, 26, -9.0, 9.0, 'park', '주차')
    blk(ax, 26, 56, -9.0, 4.5, 'cult', '공연장 200석', 10, True)
    blk(ax, 56, 68, -9.0, 4.5, 'cult', '분장', 8)
    blk(ax, 38, 54, -4.5, 4.5, 'cult', '로비·바', 9, True)
    blk(ax, 26, 29, -4.5, 4.5, 'park', ''); blk(ax, 54, 68, -4.5, 4.5, 'cult', '객석 상부', 8)
    blk(ax, 68, Ln, -9.0, 4.5, 'park', '주차'); blk(ax, 68, Ln, -4.5, 4.5, 'park', '주차')
    # sunken court
    ax.add_patch(Rectangle((29, -4.5), 26, 4.5, fc=C['sunk'], ec=INK, lw=0.8, zorder=2))
    # 1F + upper plates
    blk(ax, a0, 29, 0, 8.65, 'biz', '근생 소점포', 9, True)
    blk(ax, 55, 85, 0, 8.65, 'park', '램프·정산·이륜차', 8)
    for (p, q) in ((a0, 29), (55, 85)):
        for z, h in ((8.65, 3.3), (11.95, 3.3), (15.25, 1.65)):
            blk(ax, p, q, z, h, 'park', '')
        blk(ax, p, q, 16.9, 4.2, 'park', '')
    ax.text(16, 12.9, '스킵플로어 주차', ha='center', va='center', fontsize=9.5, fontweight='bold', zorder=6)
    ax.text(16, 19.0, '주차(전환 층)', ha='center', va='center', fontsize=8, zorder=6)
    ax.text(70, 12.9, '스킵플로어 주차', ha='center', va='center', fontsize=9.5, fontweight='bold', zorder=6)
    blk(ax, 66, 85, 16.9, 4.2, 'off', '상인회·오피스', 8)
    blk(ax, 55, 85, 21.1, 8.0, 'hall', '6F 가변홀', 10, True)
    ax.add_patch(Rectangle((55, 29.1), 30, 0.7, fc='#7f7f7f', ec='none', zorder=4))
    # roof plaza over 3..29
    ax.add_patch(Rectangle((a0, 21.1), 26, 0.55, fc=C['roof'], ec=INK, lw=0.8, zorder=4))
    for i in range(4): tree(ax, a0 + 3 + i * 6.3, 21.65, 1.0)
    ax.text(19, 30.4, '옥상 광장', ha='center', va='center', fontsize=10.5, fontweight='bold', zorder=6)
    # open stair cores (tips)
    ax.add_patch(Rectangle((29, -4.5), 26, 26.1, fc='white', ec=MUTED, lw=1.2, ls=(0, (5, 3)), zorder=2))
    ax.add_patch(Rectangle((29, -4.5), 26, 26.1, fc=C['sunk'], ec='none', alpha=0.45, zorder=1))
    zig(ax, 31, 53, 0, 21.6)
    zig(ax, 30.5, 37, -4.5, 0, n=1.5)
    ax.text(42, 27.4, '끝 코어②', ha='center', va='center', fontsize=9.5, fontweight='bold', zorder=6)
    ax.text(42, 24.8, '개방 순환 계단', ha='center', va='center', fontsize=9.5, fontweight='bold', zorder=6)
    ax.add_patch(Rectangle((85, 0), 22, 29.8, fc='white', ec=MUTED, lw=1.2, ls=(0, (5, 3)), zorder=2))
    zig(ax, 87, 107, 0, 29.8)
    ax.add_patch(Rectangle((108, -15.6 + 15.6), 5.6, 31.4 + 15.6 - 0.0, fc='#cfe3ea', ec='#5a7a88', lw=0.9, zorder=3, alpha=0.9)) if False else None
    ax.add_patch(Rectangle((108, 0), 5.6, 31.4, fc='#cfe3ea', ec='#5a7a88', lw=0.9, zorder=3))
    ax.text(110.8, 15.5, '승강기', ha='center', va='center', fontsize=7.5, color='#2c4a56', zorder=6, rotation=90)
    ax.text(96, 33.2, '끝 코어①', ha='center', va='bottom', fontsize=9.5, fontweight='bold', zorder=6)
    ax.text(96, 30.6, '순환 계단 + 승강기', ha='center', va='bottom', fontsize=9.5, fontweight='bold', zorder=6)
    # special escape stairs (underground)
    ax.add_patch(Rectangle((27.5, -15.6 + 0.0), 3.0, 11.1 + 4.5 * 0, fc=C['core'], ec=INK, lw=0.8, zorder=4))
    ax.text(29.0, -14.7 + 3.0, '특피', ha='center', va='center', fontsize=7.5, rotation=90, zorder=6)
    ax.add_patch(Rectangle((85, -15.6), 6.0, 15.6, fc=C['core'], ec=INK, lw=0.8, zorder=4))
    ax.text(88, -7.8, '특피', ha='center', va='center', fontsize=7.5, rotation=90, zorder=6)
    # 3 m setbacks
    for xx in (a0, a1): ax.plot([xx, xx], [0, 31.5], color='#2e75b6', lw=1.0, ls=(0, (4, 3)), zorder=2)
    ax.text(1.5, 4.5, '3m', fontsize=7.5, color='#2e75b6', ha='center'); ax.text(a1 + 1.5, 4.5, '3m', fontsize=7.5, color='#2e75b6', ha='center')
    # highlights (selected programme) + numbered markers
    hl(ax, 26, -9.0, 30, 4.5); hl(ax, 3, 21.1, 26, 0.55 + 7.2, lw=1.6, ls=(0, (4, 3)))
    hl(ax, 55, 21.1, 30, 8.0); hl(ax, 29, -4.5, 26, 26.1, color=PIN, lw=1.6, ls=(0, (6, 3))); hl(ax, 85, 0, 22, 29.8, color=PIN, lw=1.6, ls=(0, (6, 3)))
    badge(ax, 41, -11.4, 1); badge(ax, 9.5, 30.4, 2); badge(ax, 70, 31.0, 3); badge(ax, 42, 10.0, 4); badge(ax, 88, -2.2, 5)
    # levels
    for nm, z, h in [('B4', -15.6, 3.3), ('B3', -12.3, 3.3), ('B2', -9.0, 4.5), ('B1', -4.5, 4.5), ('1F', 0, 7.0), ('2F', 7.0, 3.3), ('3F', 10.3, 3.3), ('4F', 13.6, 3.3), ('5F', 16.9, 4.2), ('6F', 21.1, 8.0)]:
        ax.text(-3.0, z + h / 2, nm, ha='right', va='center', fontsize=9.5, fontweight='bold')
    ax.text(-3.0, 31.2, '+29.1m', ha='right', fontsize=7.5, color=MUTED); ax.text(-3.0, -17.4, '−15.6m', ha='right', fontsize=7.5, color=MUTED)
    ax.text(0, -17.6, '← 남 · 전포대로 · 224번길', ha='left', fontsize=8, color=MUTED); ax.text(Ln, -17.6, '서전로 · 북 →', ha='right', fontsize=8, color=MUTED)
    ax.set_xlim(-16, Ln + 8); ax.set_ylim(-19, 36.5); ax.axis('off')
    export_ax(fig, ax, 'img/secA.json')
    fig.savefig('img/secA.png', dpi=fig_dpi, facecolor='white'); plt.close(fig)


# ------------------------------------------------------------------ B
def section_B():
    fig = plt.figure(figsize=(3.3, 3.85), dpi=fig_dpi); ax = fig.add_axes([0, 0, 1, 1])
    w1, lw_, w2 = 16.7, 6.2, 17.8; Wt = w1 + lw_ + w2
    ax.add_patch(Rectangle((-5, -18), Wt + 10, 18, fc=C['earth'], ec='none', zorder=0))
    ax.plot([-5, Wt + 5], [0, 0], color=INK, lw=2.2, zorder=8)
    for z, h in ((-15.6, 3.3), (-12.3, 3.3)): blk(ax, 0, Wt, z, h, 'park', '주차')
    blk(ax, 0, Wt, -9.0, 9.0, 'park', '주차')
    blk(ax, 0, w1, 0, 7.0, 'biz', '카페·서점', 8.5, True)
    ax.add_patch(Rectangle((w1, 0), lw_, 7.0, fc=C['lane'], ec=INK, lw=0.8, zorder=3))
    ax.text(w1 + lw_ / 2, 4.6, '소로', ha='center', va='center', fontsize=8.5, fontweight='bold', zorder=6)
    ax.text(w1 + lw_ / 2, 2.4, '차로', ha='center', va='center', fontsize=7, zorder=6)
    ax.add_patch(FancyBboxPatch((w1 + lw_ / 2 - 1.5, 0.3), 3.0, 1.2, boxstyle='round,pad=0,rounding_size=0.5', fc='#404040', ec='none', zorder=5))
    blk(ax, w1 + lw_, Wt, 0, 8.65, 'park', '이륜차·하역', 7.5)
    mid = w1 + lw_ / 2
    ax.add_patch(Rectangle((0, 7.0), Wt, 14.1, fc=C['park'], ec=INK, lw=0.8, zorder=3))
    for z in (7.0, 10.3, 13.6, 16.9): ax.plot([0, mid], [z, z], color=INK, lw=1.8, zorder=6)
    for z in (8.65, 11.95, 15.25): ax.plot([mid, Wt], [z, z], color=INK, lw=1.8, zorder=6)
    ax.plot([mid, mid], [7.0, 16.9], color=PIN, lw=1.5, ls=(0, (4, 3)), zorder=7)
    ax.add_patch(Rectangle((1, 10.5), Wt - 2, 5.6, fc='white', ec='none', alpha=0.92, zorder=7))
    ax.text(Wt / 2, 14.7, '스킵플로어', ha='center', va='center', fontsize=10, fontweight='bold', zorder=8)
    ax.text(Wt / 2, 11.5, '소로 위에서 반 층 엇갈림', ha='center', va='center', fontsize=7.5, zorder=8)
    ax.text(Wt / 2, 19.0, '주차(전환 층)', ha='center', va='center', fontsize=8, zorder=6)
    blk(ax, 0, Wt, 21.1, 8.0, 'hall', '6F 가변홀', 10, True)
    ax.add_patch(Rectangle((0, 29.1), Wt, 0.7, fc='#7f7f7f', ec='none', zorder=4))
    hl(ax, 0, 7.0, Wt, 14.1, color=GOLD, lw=2.2); badge(ax, Wt - 3.2, 19.0, 6)
    ax.text(0, -17.6, '← 서 · 전포대로', ha='left', fontsize=8, color=MUTED); ax.text(Wt, -17.6, '동 →', ha='right', fontsize=8, color=MUTED)
    ax.set_xlim(-6, Wt + 6); ax.set_ylim(-19, 36.5); ax.axis('off')
    export_ax(fig, ax, 'img/secB.json')
    fig.savefig('img/secB.png', dpi=fig_dpi, facecolor='white'); plt.close(fig)


section_A(); section_B()
print('ok')
