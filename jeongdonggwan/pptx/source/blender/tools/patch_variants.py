import os
p = os.path.join(os.environ['TEMP'], 'bl', 'build_scene.py')
s = open(p, encoding='utf8').read()
if 'JD_VARIANT' in s:
    print('already patched'); raise SystemExit


def rep(a, b):
    global s
    assert a in s, a[:60]
    s = s.replace(a, b, 1)


rep("NIGHT = bool(V.get('night')); DUSK = bool(V.get('dusk'))",
    "NIGHT = bool(V.get('night')) or bool(os.environ.get('JD_NIGHT')); DUSK = bool(V.get('dusk')) or bool(os.environ.get('JD_DUSK'))\nVARIANT = os.environ.get('JD_VARIANT', '')")

helpers = '''
import colorsys


def _tangent_nodes(nt):
    """returns (t_out, z_out): coordinate along a vertical wall (world) and height"""
    geo = nt.nodes.new('ShaderNodeNewGeometry')
    sp = nt.nodes.new('ShaderNodeSeparateXYZ'); nt.links.new(geo.outputs['Position'], sp.inputs['Vector'])
    sn = nt.nodes.new('ShaderNodeSeparateXYZ'); nt.links.new(geo.outputs['Normal'], sn.inputs['Vector'])
    m1 = nt.nodes.new('ShaderNodeMath'); m1.operation = 'MULTIPLY'; nt.links.new(sp.outputs['X'], m1.inputs[0]); nt.links.new(sn.outputs['Y'], m1.inputs[1])
    m2 = nt.nodes.new('ShaderNodeMath'); m2.operation = 'MULTIPLY'; nt.links.new(sp.outputs['Y'], m2.inputs[0]); nt.links.new(sn.outputs['X'], m2.inputs[1])
    tt = nt.nodes.new('ShaderNodeMath'); tt.operation = 'SUBTRACT'; nt.links.new(m2.outputs[0], tt.inputs[0]); nt.links.new(m1.outputs[0], tt.inputs[1])
    return tt.outputs[0], sp.outputs['Z'], geo


def _slat_thr(nt, t_out, pitch, slat):
    dv = nt.nodes.new('ShaderNodeMath'); dv.operation = 'DIVIDE'; dv.inputs[1].default_value = pitch; nt.links.new(t_out, dv.inputs[0])
    fr = nt.nodes.new('ShaderNodeMath'); fr.operation = 'FRACT'; nt.links.new(dv.outputs[0], fr.inputs[0])
    th = nt.nodes.new('ShaderNodeMath'); th.operation = 'LESS_THAN'; th.inputs[1].default_value = slat / pitch; nt.links.new(fr.outputs[0], th.inputs[0])
    return th.outputs[0]


def fin_color_mat(name, rgb, pitch=0.30, slat=0.22, metal=0.9, rough=0.22, emit_str=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); b = nt.nodes.new('ShaderNodeBsdfPrincipled')
    b.inputs['Base Color'].default_value = (*rgb, 1); b.inputs['Metallic'].default_value = metal; b.inputs['Roughness'].default_value = rough
    if emit_str > 0:
        b.inputs['Emission Color'].default_value = (*rgb, 1); b.inputs['Emission Strength'].default_value = emit_str
    t_out, z_out, geo = _tangent_nodes(nt)
    thr = _slat_thr(nt, t_out, pitch, slat)
    tp = nt.nodes.new('ShaderNodeBsdfTransparent'); mx = nt.nodes.new('ShaderNodeMixShader')
    nt.links.new(thr, mx.inputs['Fac']); nt.links.new(tp.outputs[0], mx.inputs[1]); nt.links.new(b.outputs['BSDF'], mx.inputs[2])
    nt.links.new(mx.outputs[0], out.inputs['Surface'])
    m.use_backface_culling = False
    return m


def green_wall_mat(name):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); b = nt.nodes.new('ShaderNodeBsdfPrincipled')
    tc = nt.nodes.new('ShaderNodeTexCoord')
    n1 = nt.nodes.new('ShaderNodeTexNoise'); n1.inputs['Scale'].default_value = 9.0; n1.inputs['Detail'].default_value = 7.0
    n2 = nt.nodes.new('ShaderNodeTexNoise'); n2.inputs['Scale'].default_value = 40.0; n2.inputs['Detail'].default_value = 4.0
    nt.links.new(tc.outputs['Object'], n1.inputs['Vector']); nt.links.new(tc.outputs['Object'], n2.inputs['Vector'])
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].color = (0.02, 0.07, 0.015, 1); ramp.color_ramp.elements[1].color = (0.30, 0.45, 0.08, 1)
    e = ramp.color_ramp.elements.new(0.5); e.color = (0.08, 0.2, 0.04, 1)
    nt.links.new(n1.outputs['Fac'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], b.inputs['Base Color']); b.inputs['Roughness'].default_value = 0.8
    bump = nt.nodes.new('ShaderNodeBump'); bump.inputs['Strength'].default_value = 1.0; bump.inputs['Distance'].default_value = 0.08
    nt.links.new(n2.outputs['Fac'], bump.inputs['Height']); nt.links.new(bump.outputs['Normal'], b.inputs['Normal'])
    t_out, z_out, geo = _tangent_nodes(nt)
    thr = _slat_thr(nt, t_out, 0.55, 0.30)
    nz = nt.nodes.new('ShaderNodeMath'); nz.operation = 'GREATER_THAN'; nz.inputs[1].default_value = 0.52; nt.links.new(n1.outputs['Fac'], nz.inputs[0])
    mxm = nt.nodes.new('ShaderNodeMath'); mxm.operation = 'MAXIMUM'; nt.links.new(thr, mxm.inputs[0]); nt.links.new(nz.outputs[0], mxm.inputs[1])
    tp = nt.nodes.new('ShaderNodeBsdfTransparent'); mx = nt.nodes.new('ShaderNodeMixShader')
    nt.links.new(mxm.outputs[0], mx.inputs['Fac']); nt.links.new(tp.outputs[0], mx.inputs[1]); nt.links.new(b.outputs['BSDF'], mx.inputs[2])
    nt.links.new(mx.outputs[0], out.inputs['Surface'])
    m.use_backface_culling = False
    return m


def lantern_mat(name, emit=6.0, cell=0.9):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); b = nt.nodes.new('ShaderNodeBsdfPrincipled')
    t_out, z_out, geo = _tangent_nodes(nt)
    def cellidx(src):
        dv = nt.nodes.new('ShaderNodeMath'); dv.operation = 'DIVIDE'; dv.inputs[1].default_value = cell; nt.links.new(src, dv.inputs[0])
        fl = nt.nodes.new('ShaderNodeMath'); fl.operation = 'FLOOR'; nt.links.new(dv.outputs[0], fl.inputs[0])
        return fl.outputs[0], dv.outputs[0]
    u, u_raw = cellidx(t_out); v, v_raw = cellidx(z_out)
    comb = nt.nodes.new('ShaderNodeCombineXYZ'); nt.links.new(u, comb.inputs['X']); nt.links.new(v, comb.inputs['Y'])
    wn = nt.nodes.new('ShaderNodeTexWhiteNoise'); wn.noise_dimensions = '3D'; nt.links.new(comb.outputs[0], wn.inputs['Vector'])
    ramp = nt.nodes.new('ShaderNodeValToRGB'); ramp.color_ramp.interpolation = 'CONSTANT'
    cols = [(0.0, 0.62, 0.68), (1.0, 0.55, 0.06), (0.95, 0.16, 0.2), (0.62, 0.05, 0.62), (0.96, 0.94, 0.86), (0.05, 0.3, 0.9)]
    el = ramp.color_ramp.elements
    el[0].position = 0.0; el[0].color = (*cols[0], 1); el[1].position = 1.0 / len(cols); el[1].color = (*cols[1], 1)
    for i in range(2, len(cols)):
        e = el.new(i / len(cols)); e.color = (*cols[i], 1)
    nt.links.new(wn.outputs['Value'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], b.inputs['Base Color']); nt.links.new(ramp.outputs['Color'], b.inputs['Emission Color'])
    b.inputs['Emission Strength'].default_value = emit; b.inputs['Roughness'].default_value = 0.15; b.inputs['Alpha'].default_value = 0.88
    # frame lines between cells (opaque dark)
    def edge(raw):
        fr = nt.nodes.new('ShaderNodeMath'); fr.operation = 'FRACT'; nt.links.new(raw, fr.inputs[0])
        lt = nt.nodes.new('ShaderNodeMath'); lt.operation = 'LESS_THAN'; lt.inputs[1].default_value = 0.045; nt.links.new(fr.outputs[0], lt.inputs[0])
        return lt.outputs[0]
    e1, e2 = edge(u_raw), edge(v_raw)
    ed = nt.nodes.new('ShaderNodeMath'); ed.operation = 'MAXIMUM'; nt.links.new(e1, ed.inputs[0]); nt.links.new(e2, ed.inputs[1])
    fr_m = nt.nodes.new('ShaderNodeBsdfPrincipled'); fr_m.inputs['Base Color'].default_value = (0.02, 0.02, 0.025, 1); fr_m.inputs['Metallic'].default_value = 0.8; fr_m.inputs['Roughness'].default_value = 0.35
    mx = nt.nodes.new('ShaderNodeMixShader')
    nt.links.new(ed.outputs[0], mx.inputs['Fac']); nt.links.new(b.outputs['BSDF'], mx.inputs[1]); nt.links.new(fr_m.outputs['BSDF'], mx.inputs[2])
    nt.links.new(mx.outputs[0], out.inputs['Surface'])
    m.use_backface_culling = False
    return m


def hsv(h, s_=0.85, v=0.95):
    return colorsys.hsv_to_rgb(h % 1.0, s_, v)


_SCR_CACHE = {}


def screen_for(part):
    if not VARIANT:
        return M['screen']
    L = max(0, min(6, round((part['z0'] - 3.0) / 3.3)))
    key = (VARIANT, L)
    if key in _SCR_CACHE:
        return _SCR_CACHE[key]
    if VARIANT == 'kinetic':
        h = 0.78 + (0.10 - 0.78 + 1.0) * (L / 6.0) if False else (0.80 - 0.70 * (L / 6.0))
        mat = fin_color_mat(f'kin{L}', hsv(h, 0.9, 0.95), pitch=0.27, slat=0.17, emit_str=(1.4 if LIT else 0.0))
    elif VARIANT == 'green':
        mat = M['greenwall']
    elif VARIANT == 'lantern':
        mat = M['lantern']
    else:
        mat = M['screen']
    _SCR_CACHE[key] = mat
    return mat

'''
rep("# ------------------------------------------------------------------ materials", helpers + "\n# ------------------------------------------------------------------ materials")
rep("M['screen'] = screen_mat('screen')",
    "M['screen'] = screen_mat('screen')\nif VARIANT == 'green': M['greenwall'] = green_wall_mat('greenwall')\nif VARIANT == 'lantern': M['lantern'] = lantern_mat('lantern', emit=(7.0 if NIGHT else 1.6))")
rep("        prism('screen', p['pts'], p['z0'], p['h'], M['screen'])",
    "        prism('screen', p['pts'], p['z0'], p['h'], screen_for(p))")

geom = '''
# ------------------------------------------------------------------ design variants (extra modeling)
if VARIANT == 'kinetic':
    lv = [7.0, 10.3, 13.6, 16.9]
    k = 0
    y = 59.0
    while y < 123.5:
        for li, z0 in enumerate(lv):
            h_ = 0.80 - 0.70 * (li + 1) / 6.0
            col = fin_color_mat(f'blade{li}', hsv(h_, 0.9, 0.98), pitch=100.0, slat=100.0, emit_str=(2.0 if LIT else 0.0))
            ang = 0.62 if k % 2 == 0 else -0.62
            ob = box('blade', (1.25, 0.07, 3.1), (-0.5, y, z0 + 0.35 + 1.55), (0, 0, ang), col)
        k += 1; y += 2.4
    # sky ribbon over the plaza: a thin curved canopy at +4.2m on the roof terrace edge
    for i in range(14):
        xx = 3 + i * 2.9
        box('rib', (0.2, 0.2, 3.0), (xx, 8.0, D['roofz'] + 1.5), (0, 0, 0), M['dark'])
    box('canopy', (42.0, 6.0, 0.18), (21.5, 8.0, D['roofz'] + 3.0), (0, 0, 0), fin_color_mat('canopy', hsv(0.07, 0.9, 1.0), pitch=100, slat=100, emit_str=(1.5 if LIT else 0.0)))

if VARIANT == 'green':
    from shapely.geometry import Polygon as _SP
    soil = simple_mat('planter', (0.25, 0.22, 0.2), rough=0.9)
    for p in D['parts']:
        if p['mat'] not in ('screen', 'base'): continue
        try:
            g = _SP(p['pts']).buffer(0.18, join_style=2)
        except Exception:
            continue
        if g.is_empty or g.geom_type != 'Polygon': continue
        o = prism('planter', [tuple(c) for c in list(g.exterior.coords)[:-1]], p['z0'], 0.55, soil)
        if o:
            o.data.materials.append(M['lawn'])
            for pgn in o.data.polygons:
                if pgn.normal.z > 0.5: pgn.material_index = 1
    # roof pergola
    z = D['roofz']; tl = simple_mat('timber', (0.22, 0.13, 0.07), rough=0.55)
    for xi in (4, 14, 24, 34):
        for yi in (6, 18, 30):
            box('pcol', (0.2, 0.2, 3.4), (xi, yi, z + 1.7), (0, 0, 0), tl)
    for yi in (6, 18, 30):
        box('pbeam', (34.4, 0.22, 0.3), (19, yi, z + 3.5), (0, 0, 0), tl)
    for k in range(70):
        box('pslat', (0.1, 26.4, 0.1), (3.0 + k * 0.5, 18.0, z + 3.75), (0, 0, 0), tl)

if VARIANT == 'lantern':
    led = simple_mat('led', (0.5, 0.9, 1.0), rough=0.4, emit=(0.4, 0.85, 1.0), emit_str=30.0)
    for pr in D.get('parapets', []):
        x1, y1, x2, y2, zz = pr; L = math.hypot(x2 - x1, y2 - y1)
        box('ledr', (L, 0.14, 0.14), ((x1 + x2) / 2, (y1 + y2) / 2, zz + 1.2), (0, 0, math.atan2(y2 - y1, x2 - x1)), led)
    ledm = simple_mat('ledm', (1, 0.3, 0.8), rough=0.4, emit=(1.0, 0.25, 0.8), emit_str=25.0)
    box('ledline', (0.3, 128.0, 0.1), (-6.8, 62.0, 0.12), (0, 0, 0), ledm)
    for k in range(9):
        box('ledcol', (0.25, 0.25, 6.0), (-5.2, 8 + k * 14.0, 3.0), (0, 0, 0), led)
'''
rep("for p in D.get('solar', []):\n    o = flat('solar'", geom + "\nfor p in D.get('solar', []):\n    o = flat('solar'")
# extra trees for green variant
rep("if TREE_SRC:\n    for i, t in enumerate(D.get('trees', [])):\n        place_tree(t[0], t[1], t[2], t[3] if len(t) > 3 else 1.0, i)",
    """TREES = list(D.get('trees', []))
if VARIANT == 'green':
    rr = random.Random(3)
    for _ in range(26):
        TREES.append([rr.uniform(3, 40), rr.uniform(4, 36), D['roofz'], rr.uniform(0.9, 1.35)])
    for yy in range(0, 128, 6):
        TREES.append([-5.2, yy, 0, 1.5])
if TREE_SRC:
    for i, t in enumerate(TREES):
        place_tree(t[0], t[1], t[2], t[3] if len(t) > 3 else 1.0, i)""")
open(p, 'w', encoding='utf8').write(s)
print('patched')
