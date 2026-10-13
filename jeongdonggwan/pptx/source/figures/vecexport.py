# export a matplotlib Axes into plain JSON primitives so PowerPoint can draw them as editable native shapes
import json
import numpy as np
from matplotlib import colors as mc
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch, Polygon as MPolygon


def _hex(c):
    if c is None: return None
    try:
        r = mc.to_rgba(c)
    except Exception:
        return None
    return mc.to_hex(r[:3]).lstrip('#').upper(), float(r[3])


def _ls(ls):
    if ls in ('-', 'solid', None): return 'solid'
    if isinstance(ls, tuple): return 'dash'
    return {'--': 'dash', ':': 'sysDot', '-.': 'dashDot'}.get(ls, 'solid')


def export_ax(fig, ax, path):
    fig.canvas.draw()
    bb = ax.get_window_extent()
    width_in = bb.width / fig.dpi
    height_in = bb.height / fig.dpi
    items = []
    for p in ax.patches:
        z = p.get_zorder(); a = p.get_alpha()
        fc = p.get_facecolor(); ec = p.get_edgecolor()
        fh = _hex(fc) if p.get_fill() and fc[3] > 0 else None
        eh = _hex(ec) if p.get_linewidth() > 0 and ec[3] > 0 else None
        alpha = 1.0 if a is None else float(a)
        d = {'z': z, 'fill': fh[0] if fh else None, 'fa': (fh[1] if fh else 1.0) * alpha,
             'line': eh[0] if eh else None, 'lw': float(p.get_linewidth()), 'ls': _ls(p.get_linestyle())}
        if isinstance(p, Circle):
            cx, cy = p.center; r = p.radius
            d.update(type='ellipse', x=cx - r, y=cy - r, w=2 * r, h=2 * r)
        elif isinstance(p, FancyBboxPatch):
            d.update(type='rrect', x=p.get_x(), y=p.get_y(), w=p.get_width(), h=p.get_height())
        elif isinstance(p, Rectangle):
            d.update(type='rect', x=p.get_x(), y=p.get_y(), w=p.get_width(), h=p.get_height())
        elif isinstance(p, MPolygon):
            d.update(type='poly', pts=[[float(a_), float(b_)] for a_, b_ in p.get_xy()])
        else:
            continue
        items.append(d)
    for l in ax.lines:
        xs, ys = l.get_xdata(), l.get_ydata()
        if len(xs) < 2: continue
        h = _hex(l.get_color())
        items.append({'type': 'line', 'z': l.get_zorder(), 'pts': [[float(a_), float(b_)] for a_, b_ in zip(xs, ys)],
                      'color': h[0], 'lw': float(l.get_linewidth()), 'ls': _ls(l.get_linestyle())})
    for t in ax.texts:
        if not t.get_text().strip(): continue
        x, y = t.get_position()
        h = _hex(t.get_color())
        items.append({'type': 'text', 'z': t.get_zorder(), 'x': float(x), 'y': float(y), 'text': t.get_text(), 'size': float(t.get_fontsize()),
                      'bold': t.get_fontweight() in ('bold', 'heavy', 700, 800, 'semibold') or (isinstance(t.get_fontweight(), (int, float)) and t.get_fontweight() >= 600),
                      'color': h[0], 'ha': t.get_ha(), 'va': t.get_va(), 'rot': float(t.get_rotation())})
    items.sort(key=lambda d: d['z'])
    xl, yl = ax.get_xlim(), ax.get_ylim()
    json.dump({'xlim': list(xl), 'ylim': list(yl), 'width_in': float(width_in), 'height_in': float(height_in), 'items': items}, open(path, 'w'), ensure_ascii=False)
    print('exported', path, len(items), 'items')
