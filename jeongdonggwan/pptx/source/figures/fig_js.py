import sys, os
sys.path.insert(0, '.')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon as MP, FancyBboxPatch, Circle, FancyArrowPatch
from matplotlib import font_manager as fm
for n in ('Regular', 'Medium', 'Bold', 'ExtraBold'):
    fm.fontManager.addfont(f'fonts/Pretendard-{n}.ttf')
plt.rcParams['font.family'] = 'Pretendard'
INK = '#000000'; MUTED = '#595959'; NAVY = '#002060'; GOLD = '#FFC000'
fig, ax = plt.subplots(figsize=(1.85, 2.5), dpi=300)
H = 3.0; T = 0.28
# two half-level plates (A: full levels, B: offset by half a level) around a short-ramp seam
cols = [(0.0, 3.4), (3.9, 7.3)]
ax.add_patch(Rectangle((0.0, 0), 7.7, 0.4, fc='#9a9a9a', ec='none'))             # ground
# 1F raised retail (half level up)
ax.add_patch(Rectangle((4.3, 0.4), 3.4, 1.8, fc='#dae3f3', ec=INK, lw=0.5))
ax.text(6.0, 1.3, '1층 근생', ha='center', va='center', fontsize=5.2, fontweight='bold')
ax.add_patch(Rectangle((0.0, 0.4), 3.4, 1.5, fc='#e7e6e6', ec=INK, lw=0.5)); ax.text(1.7, 1.15, '진출입 · 램프', ha='center', va='center', fontsize=4.8)
levels_A = [1.9 + H * i for i in range(4)]
levels_B = [z + 1.5 for z in levels_A]
for i, z in enumerate(levels_A):
    ax.add_patch(Rectangle((0.0, z), 3.4, T, fc='#525252', ec='none'))
    ax.add_patch(Rectangle((0.0, z + T), 3.4, H - T - 0.05, fc='#d6d6d6', ec=INK, lw=0.4) if i < 3 else Rectangle((0, 0), 0, 0))
for i, z in enumerate(levels_B):
    if z > levels_A[-1] + 1.6: continue
    ax.add_patch(Rectangle((4.3, z), 3.4, T, fc='#525252', ec='none'))
    if i < 3: ax.add_patch(Rectangle((4.3, z + T), 3.4, H - T - 0.05, fc='#c4cfe3', ec=INK, lw=0.4))
# short half-level ramps in the seam
for i in range(4):
    za = levels_A[i] + T / 2; zb = levels_B[i] + T / 2 if i < len(levels_B) else None
    if zb is None or zb > levels_A[-1] + 1.6: continue
    ax.add_patch(MP([[3.4, za], [4.3, zb], [4.3, zb + T], [3.4, za + T]], fc='#00b0ef', ec='none'))
    if i < 3:
        zn = levels_A[i + 1] + T / 2
        ax.add_patch(MP([[4.3, zb], [3.4, zn], [3.4, zn + T], [4.3, zb + T]], fc='#00b0ef', ec='none'))
# columns
for x in (0.2, 1.7, 3.3, 4.4, 6.0, 7.6):
    ax.add_patch(Rectangle((x - 0.08, 0.4), 0.16, levels_A[-1] + H - 0.4, fc='#7f7f7f', ec='none', zorder=0))
# cars
for z in levels_A[:3]:
    for x in (0.5, 1.5, 2.5):
        ax.add_patch(FancyBboxPatch((x, z + T + 0.05), 0.62, 0.35, boxstyle='round,pad=0,rounding_size=0.12', fc='#404040', ec='none'))
# highlight the seam (ramps) and labels
ax.add_patch(Rectangle((3.25, 2.0), 1.2, levels_A[-1] + 0.6, fc='none', ec=GOLD, lw=1.4, ls=(0, (3, 2))))
ax.text(1.7, levels_A[-1] + H + 0.45, 'A판', ha='center', fontsize=7, fontweight='bold', color=NAVY)
ax.text(6.0, levels_A[-1] + H + 0.45, 'B판', ha='center', fontsize=5.6, fontweight='bold', color='#4272c4')
ax.add_patch(Circle((3.85, 13.9), 0.42, fc=NAVY, ec='white', lw=0.8, zorder=9)); ax.text(3.85, 13.88, '1', ha='center', va='center', fontsize=6, color='white', fontweight='bold', zorder=10)
ax.text(3.85, 14.9, '반 층 램프', ha='center', fontsize=5.2, fontweight='bold', color='#007bb0')
ax.set_xlim(-0.2, 7.9); ax.set_ylim(-0.2, 15.6); ax.set_aspect('equal'); ax.axis('off')
ax.text(3.85, -0.15, 'A · B판이 반 층 엇갈림 · 단면 개념(자체 작성)', ha='center', fontsize=4.8, color=MUTED, va='top')
fig.savefig('img2/c_js.jpg', facecolor='white', dpi=300, pil_kwargs={'quality': 92}); plt.close(fig)
print('section ok')
