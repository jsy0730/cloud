# -*- coding: utf-8 -*-
import os, json
os.chdir(os.path.dirname(os.path.abspath(__file__)))
s = open('build_scene3.py', encoding='utf8').read()


def rep(a, b, count=1):
    global s
    assert s.count(a) == count, (s.count(a), a[:70])
    s = s.replace(a, b)


# custom views file
rep("V = json.load(open(os.path.join(ROOT, 'views4.json'), encoding='utf8'))[VIEW]",
    "V = json.load(open(os.environ.get('JD_VIEWS', os.path.join(ROOT, 'views4.json')), encoding='utf8'))[VIEW]")
# ribbons: keep paving strictly below asphalt (no light bands on the road)
rep("(cx, cy, z + (_RB % 160) * 0.0005)", "(cx, cy, z + (_RB % 160) * 0.00003)")
# slat proportions: wider boards, bigger gaps, lean
rep("SLAT_W, SLAT_P, SLAT_T = 0.32, 0.52, 0.12", "SLAT_W, SLAT_P, SLAT_T = 0.30, 0.62, 0.12")
# warmer, more natural timber tones
rep("M['wood'] = [wood_board_mat('wood0', (2.1, 1.45, 1.0)), wood_board_mat('wood1', (1.7, 1.15, 0.8)), wood_board_mat('wood2', (2.5, 1.75, 1.2))]",
    "M['wood'] = [wood_board_mat('wood0', (1.95, 1.5, 1.05)), wood_board_mat('wood1', (1.55, 1.2, 0.86)), wood_board_mat('wood2', (2.35, 1.85, 1.3))]")
# interior ceiling lights (so the deck behind the slats reads)
rep("    finish(cols, 'columns', [M['concrete']])\n",
    """    finish(cols, 'columns', [M['concrete']])
    lit = bmesh.new()
    for p in parts:
        pts = dedupe(p['pts'])
        if len(pts) < 3:
            continue
        zt = p['z0'] + p['h'] - 0.06
        xs = [q[0] for q in pts]; ys = [q[1] for q in pts]
        y = min(ys) + 3.0
        while y < max(ys):
            x = min(xs) + 2.0
            while x < max(xs):
                if pip((x, y), pts) and dist_edges((x, y), pts) > 0.8:
                    obox(lit, (x, y, zt), (1, 0, 0), (0, 1, 0), (0, 0, 1), 3.0, 0.18, 0.05)
                x += 6.0
            y += 5.2
    finish(lit, 'deck_lights', [simple_mat('decklight', (1.0, 0.95, 0.85), rough=0.5, emit=(1.0, 0.92, 0.78), emit_str=(14.0 if LIT else 5.0))])
""")
# trees: a few only
rep("for yy_ in (14.0, 24.0, 66.0, 84.0, 104.0, 118.0):", "for yy_ in (18.0, 72.0, 94.0, 114.0):")
open('build_scene3.py', 'w', encoding='utf8').write(s)
views = json.load(open(os.path.join(os.environ['TEMP'], 'cloud_repo', 'jeongdonggwan', 'build', 'render', 'views4.json'), encoding='utf8'))
views['stair_close'] = {"w": 1920, "h": 1080, "fov": 46, "eye": [-9.5, 18.0, 2.0], "target": [3.5, 43.0, 6.5], "sunAz": 215, "sunEl": 40}
json.dump(views, open('views_v3.json', 'w', encoding='utf8'), ensure_ascii=False)
print('patched')
