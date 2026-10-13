# 층별 용도 구성 (공설기 v1.2 FloorStack vocabulary: 면적 비례 막대 + 용도 색)
# v5: 슬라이드에 놓이는 크기(5.2in)로 직접 작도 → 글자 크기 고정(8.5 / 9.5 / 11pt), 막대 안 라벨은 들어갈 때만 표기
import sys
sys.path.insert(0, '.')
from vecexport import export_ax
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib import font_manager as fm
for n in ('Regular', 'Medium', 'Bold', 'ExtraBold'):
    fm.fontManager.addfont(f'fonts/Pretendard-{n}.ttf')
plt.rcParams['font.family'] = 'Pretendard'
S, M, L = 8.5, 9.5, 11.0
INK = '#000000'; MUTED = '#595959'; NAVY = '#002060'; GOLD = '#FFC000'
COL = dict(park='#cfcfcf', perf='#8faadc', cult='#b4c7e7', shop='#fbf3a4', biz='#eebbba', core='#ec8080', mep='#9a9a9a', plaza='#cfe5bd', ramp='#e9e0c9')
FL = [
 ('RF', '옥상', None, [('옥상 광장', 'plaza', 1380.0)]),
 ('6F', '8.0m', 3000.0, [('가변홀', 'perf', 1500.0), ('다목적', 'cult', 700.0), ('공연지원', 'cult', 650.0), ('', 'core', 150.0)]),
 ('5F', '4.2m', 4322.1, [('상인회·오피스', 'biz', 1200.0), ('주차(전환)', 'park', 2972.1), ('', 'core', 150.0)]),
 ('2~4F', '3.3m', 4322.1, [('주차', 'park', 4172.1), ('', 'core', 150.0)]),
 ('1F', '7.0m', 3635.3, [('서점', 'shop', 400.0), ('카페', 'shop', 400.0), ('로비', 'cult', 300.0), ('근생', 'shop', 600.0), ('램프·정산·이륜차', 'ramp', 1350.0), ('기타', 'park', 435.3), ('', 'core', 150.0)]),
 ('B1', '4.5m', 4806.5, [('공연 로비', 'cult', 800.0), ('주차', 'park', 3856.5), ('', 'core', 150.0)]),
 ('B2', '4.5m', 4964.5, [('200석', 'perf', 800.0), ('분장', 'cult', 300.0), ('주차', 'park', 3714.5), ('', 'core', 150.0)]),
 ('B3', '3.3m', 4964.5, [('', 'mep', 300.0), ('주차', 'park', 4514.5), ('', 'core', 150.0)]),
 ('B4', '3.3m', 4964.5, [('', 'mep', 600.0), ('주차', 'park', 4214.5), ('', 'core', 150.0)]),
]
W_IN, H_IN = 5.2, 4.55
XL = (-640, 5640)
IN_PER_U = W_IN / (XL[1] - XL[0])
CH = 0.118          # inches per hangul at 8.5pt (conservative)
fig = plt.figure(figsize=(W_IN, H_IN), dpi=220)
ax = fig.add_axes([0, 0, 1, 1])
n = len(FL); H = 0.62; GAP = 0.18; ROW = H + GAP
ytop = n * ROW
for i, (fl, hh, tot, segs) in enumerate(FL):
    y = (n - 1 - i) * ROW
    if fl == 'B1':
        ax.plot([-90, 5150], [y + H + GAP / 2] * 2, color=INK, lw=1.4, ls=(0, (6, 3)), zorder=1)
        ax.text(5190, y + H + GAP / 2, '지반 ±0', fontsize=S, va='center', color=MUTED)
    x = 0.0
    for name, kind, area in segs:
        ax.add_patch(Rectangle((x, y), area, H, fc=COL[kind], ec='white', lw=1.2, zorder=3))
        if name and (len(name) * CH + 0.05) <= area * IN_PER_U:
            ax.text(x + area / 2, y + H / 2, name, ha='center', va='center', fontsize=M if area > 1100 else S,
                    fontweight='bold' if kind in ('perf', 'plaza') else 'medium', color=INK, zorder=5)
        x += area
    ax.text(-100, y + H / 2, fl, ha='right', va='center', fontsize=L, fontweight='bold')
    if hh != '옥상':
        ax.text(x + 70, y + H / 2, hh, ha='left', va='center', fontsize=S, color=MUTED)
# highlights: performance volumes
for row, w in ((6, 800), (1, 1500), (0, 1380)):
    ax.add_patch(Rectangle((0, (n - 1 - row) * ROW - 0.03), w, H + 0.06, fc='none', ec=GOLD, lw=2.4, zorder=6))
# notes
ax.text(0, ytop + 0.12, '가로 길이 = 층 면적 (최대 4,964.5㎡)', fontsize=S, color=MUTED, va='bottom')
ax.text(5640, ytop + 0.12, '지상 약 29.1m · 지하 약 15.6m', fontsize=S, color=MUTED, ha='right', va='bottom')
# legend (two rows)
items = [('perf', '공연·체육 가변'), ('cult', '문화 지원'), ('shop', '상업'), ('biz', '상인회'), ('park', '주차'), ('core', '코어'), ('plaza', '광장'), ('mep', '설비')]
rows = [items[:4], items[4:]]
for r, row in enumerate(rows):
    lx = 0.0
    ly = -0.55 - r * 0.5
    for k, t in row:
        ax.add_patch(Rectangle((lx, ly - 0.15), 150, 0.3, fc=COL[k], ec='none', zorder=3))
        ax.text(lx + 210, ly, t, fontsize=S, va='center', zorder=5)
        lx += 210 + (len(t) * CH + 0.15) / IN_PER_U
ax.set_xlim(*XL); ax.set_ylim(-1.55, ytop + 0.55); ax.axis('off')
export_ax(fig, ax, 'img/program_stack.json')
fig.savefig('img/program_stack.png', dpi=220, facecolor='white'); plt.close(fig)
print('ok', W_IN, H_IN)
