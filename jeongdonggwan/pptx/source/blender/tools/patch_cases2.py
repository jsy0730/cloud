import os
p = os.path.join(os.environ['TEMP'], 'bl', 'build_scene.py')
s = open(p, encoding='utf8').read()
if "VARIANT == 'saintluc'" in s:
    print('already'); raise SystemExit


def rep(a, b):
    global s
    assert a in s, a[:70]
    s = s.replace(a, b, 1)


mats = '''
def saintluc_mat(name):
    """Saint-Luc parking garage: meandering hardwood slats, each slat its own timber tone"""
    base = os.path.join(PH, 'tex', 'dark_wood')
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); b = nt.nodes.new('ShaderNodeBsdfPrincipled')
    t_out, z_out, geo = _tangent_nodes(nt)
    # wave: t' = t + A * sin(z * k)
    zk = nt.nodes.new('ShaderNodeMath'); zk.operation = 'MULTIPLY'; zk.inputs[1].default_value = 0.62; nt.links.new(z_out, zk.inputs[0])
    sn = nt.nodes.new('ShaderNodeMath'); sn.operation = 'SINE'; nt.links.new(zk.outputs[0], sn.inputs[0])
    sa = nt.nodes.new('ShaderNodeMath'); sa.operation = 'MULTIPLY'; sa.inputs[1].default_value = 0.55; nt.links.new(sn.outputs[0], sa.inputs[0])
    tw = nt.nodes.new('ShaderNodeMath'); tw.operation = 'ADD'; nt.links.new(t_out, tw.inputs[0]); nt.links.new(sa.outputs[0], tw.inputs[1])
    pitch, slat = 0.22, 0.15
    dv = nt.nodes.new('ShaderNodeMath'); dv.operation = 'DIVIDE'; dv.inputs[1].default_value = pitch; nt.links.new(tw.outputs[0], dv.inputs[0])
    fl = nt.nodes.new('ShaderNodeMath'); fl.operation = 'FLOOR'; nt.links.new(dv.outputs[0], fl.inputs[0])
    fr = nt.nodes.new('ShaderNodeMath'); fr.operation = 'FRACT'; nt.links.new(dv.outputs[0], fr.inputs[0])
    th = nt.nodes.new('ShaderNodeMath'); th.operation = 'LESS_THAN'; th.inputs[1].default_value = slat / pitch; nt.links.new(fr.outputs[0], th.inputs[0])
    wn = nt.nodes.new('ShaderNodeTexWhiteNoise'); wn.noise_dimensions = '1D'; nt.links.new(fl.outputs[0], wn.inputs['W'])
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].color = (0.55, 0.50, 0.46, 1); ramp.color_ramp.elements[1].color = (1.55, 1.30, 1.05, 1)
    nt.links.new(wn.outputs['Value'], ramp.inputs['Fac'])
    tc = nt.nodes.new('ShaderNodeTexCoord'); mp = nt.nodes.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (2.2, 2.2, 0.55)
    nt.links.new(tc.outputs['Object'], mp.inputs['Vector'])
    d = nt.nodes.new('ShaderNodeTexImage'); d.image = img(os.path.join(base, 'dark_wood_Diffuse_1k.jpg'), False); d.projection = 'BOX'; d.projection_blend = 0.2
    r = nt.nodes.new('ShaderNodeTexImage'); r.image = img(os.path.join(base, 'dark_wood_Rough_1k.jpg'), True); r.projection = 'BOX'; r.projection_blend = 0.2
    nt.links.new(mp.outputs['Vector'], d.inputs['Vector']); nt.links.new(mp.outputs['Vector'], r.inputs['Vector'])
    mixc = nt.nodes.new('ShaderNodeMix'); mixc.data_type = 'RGBA'; mixc.blend_type = 'MULTIPLY'; mixc.inputs['Factor'].default_value = 1.0
    nt.links.new(d.outputs['Color'], mixc.inputs[6]); nt.links.new(ramp.outputs['Color'], mixc.inputs[7])
    nt.links.new(mixc.outputs[2], b.inputs['Base Color']); nt.links.new(r.outputs['Color'], b.inputs['Roughness'])
    tp = nt.nodes.new('ShaderNodeBsdfTransparent'); mx = nt.nodes.new('ShaderNodeMixShader')
    nt.links.new(th.outputs[0], mx.inputs['Fac']); nt.links.new(tp.outputs[0], mx.inputs[1]); nt.links.new(b.outputs['BSDF'], mx.inputs[2])
    nt.links.new(mx.outputs[0], out.inputs['Surface'])
    m.use_backface_culling = False
    return m


def blaibach_mat(name):
    """Concert Hall Blaibach: monolithic concrete with coarse granite chips, irregular vertical light slits"""
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); b = nt.nodes.new('ShaderNodeBsdfPrincipled')
    tc = nt.nodes.new('ShaderNodeTexCoord')
    vr = nt.nodes.new('ShaderNodeTexVoronoi'); vr.feature = 'DISTANCE_TO_EDGE' if False else 'F1'; vr.inputs['Scale'].default_value = 6.0
    nt.links.new(tc.outputs['Object'], vr.inputs['Vector'])
    nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 28.0; nz.inputs['Detail'].default_value = 8.0
    nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].color = (0.16, 0.16, 0.17, 1); ramp.color_ramp.elements[1].color = (0.52, 0.50, 0.47, 1)
    nt.links.new(nz.outputs['Fac'], ramp.inputs['Fac'])
    chips = nt.nodes.new('ShaderNodeMix'); chips.data_type = 'RGBA'; chips.blend_type = 'MULTIPLY'; chips.inputs['Factor'].default_value = 0.55
    nt.links.new(ramp.outputs['Color'], chips.inputs[6])
    vr2 = nt.nodes.new('ShaderNodeValToRGB'); vr2.color_ramp.elements[0].position = 0.15; vr2.color_ramp.elements[1].position = 0.55
    vr2.color_ramp.elements[0].color = (0.45, 0.45, 0.46, 1); vr2.color_ramp.elements[1].color = (1.1, 1.08, 1.05, 1)
    nt.links.new(vr.outputs['Distance'], vr2.inputs['Fac']); nt.links.new(vr2.outputs['Color'], chips.inputs[7])
    nt.links.new(chips.outputs[2], b.inputs['Base Color']); b.inputs['Roughness'].default_value = 0.92
    bump = nt.nodes.new('ShaderNodeBump'); bump.inputs['Strength'].default_value = 1.0; bump.inputs['Distance'].default_value = 0.06
    nt.links.new(vr.outputs['Distance'], bump.inputs['Height']); nt.links.new(bump.outputs['Normal'], b.inputs['Normal'])
    t_out, z_out, geo = _tangent_nodes(nt)
    cw = 1.1
    dv = nt.nodes.new('ShaderNodeMath'); dv.operation = 'DIVIDE'; dv.inputs[1].default_value = cw; nt.links.new(t_out, dv.inputs[0])
    fl = nt.nodes.new('ShaderNodeMath'); fl.operation = 'FLOOR'; nt.links.new(dv.outputs[0], fl.inputs[0])
    fr = nt.nodes.new('ShaderNodeMath'); fr.operation = 'FRACT'; nt.links.new(dv.outputs[0], fr.inputs[0])
    wn = nt.nodes.new('ShaderNodeTexWhiteNoise'); wn.noise_dimensions = '1D'; nt.links.new(fl.outputs[0], wn.inputs['W'])
    pick = nt.nodes.new('ShaderNodeMath'); pick.operation = 'LESS_THAN'; pick.inputs[1].default_value = 0.34; nt.links.new(wn.outputs['Value'], pick.inputs[0])
    # slit width varies per cell: edges at 0.30 .. 0.30 + 0.12*rand
    wv = nt.nodes.new('ShaderNodeMath'); wv.operation = 'MULTIPLY'; wv.inputs[1].default_value = 0.16; nt.links.new(wn.outputs['Value'], wv.inputs[0])
    wv2 = nt.nodes.new('ShaderNodeMath'); wv2.operation = 'ADD'; wv2.inputs[1].default_value = 0.40; nt.links.new(wv.outputs[0], wv2.inputs[0])
    a_ = nt.nodes.new('ShaderNodeMath'); a_.operation = 'GREATER_THAN'; a_.inputs[1].default_value = 0.30; nt.links.new(fr.outputs[0], a_.inputs[0])
    b_ = nt.nodes.new('ShaderNodeMath'); b_.operation = 'LESS_THAN'; nt.links.new(fr.outputs[0], b_.inputs[0]); nt.links.new(wv2.outputs[0], b_.inputs[1])
    ab = nt.nodes.new('ShaderNodeMath'); ab.operation = 'MULTIPLY'; nt.links.new(a_.outputs[0], ab.inputs[0]); nt.links.new(b_.outputs[0], ab.inputs[1])
    slit = nt.nodes.new('ShaderNodeMath'); slit.operation = 'MULTIPLY'; nt.links.new(ab.outputs[0], slit.inputs[0]); nt.links.new(pick.outputs[0], slit.inputs[1])
    tp = nt.nodes.new('ShaderNodeBsdfTransparent'); mx = nt.nodes.new('ShaderNodeMixShader')
    nt.links.new(slit.outputs[0], mx.inputs['Fac']); nt.links.new(b.outputs['BSDF'], mx.inputs[1]); nt.links.new(tp.outputs[0], mx.inputs[2])
    nt.links.new(mx.outputs[0], out.inputs['Surface'])
    m.use_backface_culling = False
    return m

'''
rep("_SCR_CACHE = {}\n", mats + "\n_SCR_CACHE = {}\n")
rep("    elif VARIANT == 'lantern':\n        mat = M['lantern']\n    else:",
    "    elif VARIANT == 'lantern':\n        mat = M['lantern']\n    elif VARIANT == 'saintluc':\n        mat = M['saintluc']\n    elif VARIANT == 'blaibach':\n        mat = M['blaibach']\n    else:")
rep("if VARIANT == 'green': M['greenwall'] = green_wall_mat('greenwall')",
    "if VARIANT == 'green': M['greenwall'] = green_wall_mat('greenwall')\nif VARIANT == 'saintluc': M['saintluc'] = saintluc_mat('saintluc')\nif VARIANT == 'blaibach': M['blaibach'] = blaibach_mat('blaibach')")
# blaibach: warm glow behind the slits
rep("    M['inner'] = simple_mat('inner_v', (0.035, 0.035, 0.045) if VARIANT != 'green' else (0.05, 0.075, 0.04), rough=0.9)",
    "    M['inner'] = simple_mat('inner_v', (0.035, 0.035, 0.045) if VARIANT != 'green' else (0.05, 0.075, 0.04), rough=0.9)\n    if VARIANT == 'blaibach':\n        M['inner'] = simple_mat('inner_b', (0.9, 0.55, 0.25), rough=0.9, emit=(1.0, 0.58, 0.22), emit_str=(5.0 if LIT else 0.4))")
# lincoln: open slab garage -> skip screens and their inner volume
rep("    if m in ('screen', 'base'):\n        prism('screen', p['pts'], p['z0'], p['h'], screen_for(p))",
    "    if m in ('screen', 'base') and VARIANT == 'lincoln':\n        continue\n    if m in ('screen', 'base'):\n        prism('screen', p['pts'], p['z0'], p['h'], screen_for(p))")
# blaibach: the 6F hall becomes the solid granite-concrete block
rep("    elif m in ('glass', 'fin'):\n        prism('glass', p['pts'], p['z0'], p['h'], M['glass'])",
    "    elif m == 'fin' and VARIANT == 'blaibach':\n        prism('block', p['pts'], p['z0'], p['h'], M['blaibach'])\n    elif m in ('glass', 'fin'):\n        prism('glass', p['pts'], p['z0'], p['h'], M['glass'])")

geom = '''
if VARIANT == 'saintluc':
    # green roof over the terrace + planted edge (Saint-Luc: roof returned to the park)
    for pg in D.get('roof', []):
        prism('greenroof', [tuple(c) for c in pg], D['roofz'], 0.12, M['lawn'])

if VARIANT == 'lincoln':
    import random as _r
    rr = _r.Random(9)
    def inside(pt, poly):
        x, y = pt; ins = False; n = len(poly)
        for i in range(n):
            x1, y1 = poly[i]; x2, y2 = poly[(i + 1) % n]
            if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1 + 1e-12) + x1:
                ins = not ins
        return ins
    big = [pp for pp in D['parts'] if pp['mat'] == 'slab' and abs(pp['z0'] - 16.9) < 0.01]
    base_poly = big[0]['pts'] if big else D['block'][0]
    conc_ = simple_mat('lcol', (0.66, 0.65, 0.62), rough=0.9)
    for gx in range(2, 44, 8):
        for gy in range(6, 124, 8):
            if not inside((gx, gy), base_poly): continue
            top = 29.1 if gy > 38.5 else 21.1
            box('lcolumn', (0.55, 0.55, top), (gx, gy, top / 2), (0, 0, 0), conc_)
    carc = [(0.9, 0.9, 0.9), (0.06, 0.06, 0.07), (0.5, 0.52, 0.55), (0.55, 0.1, 0.08), (0.1, 0.2, 0.4), (0.8, 0.77, 0.7)]
    ci = 0
    for z0, th in ((7.0, 0.35), (10.3, 0.35), (13.6, 0.35), (8.65, 0.35), (11.95, 0.35), (15.25, 0.35)):
        for gy in range(8, 120, 5):
            for gx in (6.0, 13.0, 30.0, 37.0):
                if rr.random() < 0.22 or not inside((gx, gy), base_poly): continue
                col_ = simple_mat(f'lc{ci % 6}', carc[ci % 6], rough=0.25, coat=0.8); ci += 1
                box('lcar', (1.8, 4.4, 1.35), (gx, gy, z0 + th + 0.7), (0, 0, 0), col_, bevel=0.12)
    for pp in D['parts']:
        if pp['mat'] == 'slab':
            prism('slabedge', pp['pts'], pp['z0'] - 0.25, 0.6, M['concrete'])
'''
rep("\nfor p in D.get('solar', []):\n    o = flat('solar'", geom + "\nfor p in D.get('solar', []):\n    o = flat('solar'")
open(p, 'w', encoding='utf8').write(s)
print('patched')
