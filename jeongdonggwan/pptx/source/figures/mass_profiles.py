import sys, json, os
sys.path.insert(0, '.')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib import font_manager as fm
from shapely.geometry import Polygon
for n in ('Regular', 'Medium', 'Bold', 'ExtraBold'):
    fm.fontManager.addfont(f'fonts/Pretendard-{n}.ttf')
plt.rcParams['font.family'] = 'Pretendard'
T = os.environ['TEMP'].replace(chr(92), '/')
BASE = json.load(open(T + '/cloud_repo/jeongdonggwan/build/render/design.json', encoding='utf8'))['parts']
COL = {'slab': '#8a8a8a', 'screen': '#c9c9c9', 'base': '#c9c9c9', 'glass': '#b4c7e7', 'fin': '#8faadc', 'roof': '#525252', 'roofdeck': '#cfe5bd'}
K = 0.9568 ** 2
def area(parts):
    return sum(Polygon(p['pts']).area * K for p in parts if p['mat'] == 'slab' and p['z0'] >= 6.5)
def top(parts):
    return max(p['z0'] + p['h'] for p in parts)
sets = {'기준안': BASE}
for k in 'ABC':
    sets[k] = json.load(open(T + f'/bl/massing_{k}.json', encoding='utf8'))['parts']
res = {}
for name, parts in sets.items():
    res[name] = (round(area(parts)), round(top(parts), 1))
    fig, ax = plt.subplots(figsize=(3.3, 1.5), dpi=220)
    for p in sorted(parts, key=lambda q: q['z0']):
        poly = Polygon(p['pts']); y0, y1 = poly.bounds[1], poly.bounds[3]
        ax.add_patch(Rectangle((y0, p['z0']), y1 - y0, p['h'], fc=COL.get(p['mat'], '#ddd'), ec='#555', lw=0.2, alpha=0.55))
    ax.plot([-3, 130], [0, 0], color='black', lw=1.3)
    ax.set_xlim(-3, 130); ax.set_ylim(-1, 34); ax.set_aspect('equal'); ax.axis('off')
    ax.text(0, 31.5, '남', fontsize=7, color='#555'); ax.text(125, 31.5, '북', fontsize=7, color='#555')
    fig.savefig(f'img/prof_{name}.png', facecolor='white', bbox_inches='tight', pad_inches=0.03); plt.close(fig)
print(res)
json.dump(res, open('mass_stats.json', 'w'), ensure_ascii=False)
