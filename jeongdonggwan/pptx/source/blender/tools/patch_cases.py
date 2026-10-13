import os
p = os.path.join(os.environ['TEMP'], 'bl', 'build_scene.py')
s = open(p, encoding='utf8').read()
if "'pnp'" in s:
    print('already'); raise SystemExit


def rep(a, b):
    global s
    assert a in s, a[:70]
    s = s.replace(a, b, 1)


mats = '''
def pnp_mat(name):
    """Park 'n' Play: concrete frame grid, planter band in every bay, open (perforated) above"""
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    t_out, z_out, geo = _tangent_nodes(nt)
    def fr(src, div):
        dv = nt.nodes.new('ShaderNodeMath'); dv.operation = 'DIVIDE'; dv.inputs[1].default_value = div; nt.links.new(src, dv.inputs[0])
        f = nt.nodes.new('ShaderNodeMath'); f.operation = 'FRACT'; nt.links.new(dv.outputs[0], f.inputs[0]); return f.outputs[0]
    def lt(src, v):
        n = nt.nodes.new('ShaderNodeMath'); n.operation = 'LESS_THAN'; n.inputs[1].default_value = v; nt.links.new(src, n.inputs[0]); return n.outputs[0]
    def gt(src, v):
        n = nt.nodes.new('ShaderNodeMath'); n.operation = 'GREATER_THAN'; n.inputs[1].default_value = v; nt.links.new(src, n.inputs[0]); return n.outputs[0]
    def mx_(a, b, op):
        n = nt.nodes.new('ShaderNodeMath'); n.operation = op; nt.links.new(a, n.inputs[0]); nt.links.new(b, n.inputs[1]); return n.outputs[0]
    u = fr(t_out, 3.75); w = fr(z_out, 3.3)
    post = lt(u, 0.07); slab = lt(w, 0.085)
    frame = mx_(post, slab, 'MAXIMUM')
    band = mx_(gt(w, 0.085), lt(w, 0.30), 'MULTIPLY')                    # planter strip above each slab
    band = mx_(band, mx_(gt(u, 0.07), lt(u, 0.995), 'MULTIPLY'), 'MULTIPLY')
    # shaders
    conc = nt.nodes.new('ShaderNodeBsdfPrincipled'); conc.inputs['Base Color'].default_value = (0.62, 0.61, 0.58, 1); conc.inputs['Roughness'].default_value = 0.85
    tc = nt.nodes.new('ShaderNodeTexCoord'); nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 14.0; nz.inputs['Detail'].default_value = 6.0
    nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].color = (0.05, 0.12, 0.03, 1); ramp.color_ramp.elements[1].color = (0.26, 0.42, 0.09, 1)
    nt.links.new(nz.outputs['Fac'], ramp.inputs['Fac'])
    grn = nt.nodes.new('ShaderNodeBsdfPrincipled'); grn.inputs['Roughness'].default_value = 0.9
    nt.links.new(ramp.outputs['Color'], grn.inputs['Base Color'])
    tp = nt.nodes.new('ShaderNodeBsdfTransparent')
    m1 = nt.nodes.new('ShaderNodeMixShader'); nt.links.new(band, m1.inputs['Fac']); nt.links.new(tp.outputs[0], m1.inputs[1]); nt.links.new(grn.outputs['BSDF'], m1.inputs[2])
    m2 = nt.nodes.new('ShaderNodeMixShader'); nt.links.new(frame, m2.inputs['Fac']); nt.links.new(m1.outputs[0], m2.inputs[1]); nt.links.new(conc.outputs['BSDF'], m2.inputs[2])
    nt.links.new(m2.outputs[0], out.inputs['Surface'])
    m.use_backface_culling = False
    return m


def herma_mat(name, emit_night=2.4):
    """Herma Parking Building: translucent polycarbonate in a diagonal (triangulated) aluminium frame; lit cells at night"""
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    t_out, z_out, geo = _tangent_nodes(nt)
    def add(a, b, op):
        n = nt.nodes.new('ShaderNodeMath'); n.operation = op; nt.links.new(a, n.inputs[0]); nt.links.new(b, n.inputs[1]); return n.outputs[0]
    pitch = 2.4
    sc = nt.nodes.new('ShaderNodeMath'); sc.operation = 'MULTIPLY'; sc.inputs[1].default_value = 1.0; nt.links.new(z_out, sc.inputs[0])
    d1 = nt.nodes.new('ShaderNodeMath'); d1.operation = 'ADD'; nt.links.new(t_out, d1.inputs[0]); nt.links.new(sc.outputs[0], d1.inputs[1])
    d2 = nt.nodes.new('ShaderNodeMath'); d2.operation = 'SUBTRACT'; nt.links.new(t_out, d2.inputs[0]); nt.links.new(sc.outputs[0], d2.inputs[1])
    def cell(src):
        dv = nt.nodes.new('ShaderNodeMath'); dv.operation = 'DIVIDE'; dv.inputs[1].default_value = pitch; nt.links.new(src, dv.inputs[0])
        fl = nt.nodes.new('ShaderNodeMath'); fl.operation = 'FLOOR'; nt.links.new(dv.outputs[0], fl.inputs[0])
        fr = nt.nodes.new('ShaderNodeMath'); fr.operation = 'FRACT'; nt.links.new(dv.outputs[0], fr.inputs[0])
        return fl.outputs[0], fr.outputs[0]
    i1, f1 = cell(d1.outputs[0]); i2, f2 = cell(d2.outputs[0])
    def lt(src, v):
        n = nt.nodes.new('ShaderNodeMath'); n.operation = 'LESS_THAN'; n.inputs[1].default_value = v; nt.links.new(src, n.inputs[0]); return n.outputs[0]
    frame = add(lt(f1, 0.055), lt(f2, 0.055), 'MAXIMUM')
    comb = nt.nodes.new('ShaderNodeCombineXYZ'); nt.links.new(i1, comb.inputs['X']); nt.links.new(i2, comb.inputs['Y'])
    wn = nt.nodes.new('ShaderNodeTexWhiteNoise'); wn.noise_dimensions = '3D'; nt.links.new(comb.outputs[0], wn.inputs['Vector'])
    # polycarbonate cell
    pc = nt.nodes.new('ShaderNodeBsdfPrincipled'); pc.inputs['Base Color'].default_value = (0.86, 0.93, 0.98, 1); pc.inputs['Roughness'].default_value = 0.45
    pw = nt.nodes.new('ShaderNodeMath'); pw.operation = 'POWER'; pw.inputs[1].default_value = 3.0; nt.links.new(wn.outputs['Value'], pw.inputs[0])
    es = nt.nodes.new('ShaderNodeMath'); es.operation = 'MULTIPLY'; es.inputs[1].default_value = emit_night if NIGHT or DUSK else 0.0; nt.links.new(pw.outputs[0], es.inputs[0])
    nt.links.new(es.outputs[0], pc.inputs['Emission Strength'])
    pc.inputs['Emission Color'].default_value = (1.0, 0.82, 0.55, 1)
    tp = nt.nodes.new('ShaderNodeBsdfTransparent'); tp.inputs['Color'].default_value = (0.9, 0.96, 1.0, 1)
    op = nt.nodes.new('ShaderNodeMath'); op.operation = 'MULTIPLY'; op.inputs[1].default_value = 0.55; nt.links.new(wn.outputs['Value'], op.inputs[0])
    op2 = nt.nodes.new('ShaderNodeMath'); op2.operation = 'ADD'; op2.inputs[1].default_value = 0.30; nt.links.new(op.outputs[0], op2.inputs[0])
    cellmix = nt.nodes.new('ShaderNodeMixShader'); nt.links.new(op2.outputs[0], cellmix.inputs['Fac'])
    nt.links.new(tp.outputs[0], cellmix.inputs[1]); nt.links.new(pc.outputs['BSDF'], cellmix.inputs[2])
    al = nt.nodes.new('ShaderNodeBsdfPrincipled'); al.inputs['Base Color'].default_value = (0.72, 0.74, 0.76, 1); al.inputs['Metallic'].default_value = 0.9; al.inputs['Roughness'].default_value = 0.32
    fm = nt.nodes.new('ShaderNodeMixShader'); nt.links.new(frame, fm.inputs['Fac']); nt.links.new(cellmix.outputs[0], fm.inputs[1]); nt.links.new(al.outputs['BSDF'], fm.inputs[2])
    nt.links.new(fm.outputs[0], out.inputs['Surface'])
    m.use_backface_culling = False
    return m

'''
rep("_SCR_CACHE = {}\n", mats + "\n_SCR_CACHE = {}\n")
rep("    elif VARIANT == 'lantern':\n        mat = M['lantern']\n    else:",
    "    elif VARIANT == 'lantern':\n        mat = M['lantern']\n    elif VARIANT == 'pnp':\n        mat = M['pnp']\n    elif VARIANT == 'herma':\n        mat = M['herma']\n    else:")
rep("if VARIANT == 'green': M['greenwall'] = green_wall_mat('greenwall')",
    "if VARIANT == 'green': M['greenwall'] = green_wall_mat('greenwall')\nif VARIANT == 'pnp': M['pnp'] = pnp_mat('pnp')\nif VARIANT == 'herma': M['herma'] = herma_mat('herma')")
# lincoln: open slab garage -> skip screens and their inner volume
rep("    if m in ('screen', 'base'):\n        prism('screen', p['pts'], p['z0'], p['h'], screen_for(p))",
    "    if m in ('screen', 'base') and VARIANT == 'lincoln':\n        continue\n    if m in ('screen', 'base'):\n        prism('screen', p['pts'], p['z0'], p['h'], screen_for(p))")

geom = '''
if VARIANT == 'pnp':
    # long exterior public stair up the west (전포대로) side to the roof, black steel
    steel = M['steel_red']
    x_st, y0_, y1_, z1_ = -1.7, 6.0, 40.0, D['roofz']
    run = y1_ - y0_; ang = math.atan2(z1_, run); ln = math.hypot(run, z1_)
    st = box('pnp_stair', (2.4, ln, 0.16), (x_st, (y0_ + y1_) / 2, z1_ / 2), (0, 0, 0), steel)
    st.rotation_mode = 'XYZ'; st.rotation_euler = (ang, 0, 0)
    for side in (-1, 1):
        for k in range(0, 9):
            t_ = k / 8.0
            yy = y0_ + run * t_; zz = z1_ * t_
            box('pnp_post', (0.06, 0.06, 1.05), (x_st + side * 1.15, yy, zz + 0.55), (0, 0, 0), steel)
        rl = box('pnp_rail', (0.06, ln, 0.06), (x_st + side * 1.15, (y0_ + y1_) / 2, z1_ / 2 + 1.05), (0, 0, 0), steel)
        rl.rotation_mode = 'XYZ'; rl.rotation_euler = (ang, 0, 0)
    for k in range(3):
        yy = y0_ + run * (k + 1) / 4.0; zz = z1_ * (k + 1) / 4.0
        box('pnp_landing', (3.2, 3.0, 0.18), (x_st, yy, zz), (0, 0, 0), steel)
    # rooftop play discs (rubber), PnP roof plan
    cols = [(0.78, 0.26, 0.22), (0.12, 0.55, 0.58), (0.92, 0.7, 0.14), (0.35, 0.3, 0.62), (0.88, 0.45, 0.5)]
    rr = random.Random(21)
    zr = D['roofz'] + 0.1
    spots = [(9, 10, 3.6), (22, 9, 4.4), (35, 12, 3.2), (14, 24, 4.8), (30, 26, 3.8), (6, 31, 2.8), (38, 32, 2.6)]
    for i, (cx_, cy_, r_) in enumerate(spots):
        bm_ = bmesh.new(); bmesh.ops.create_cone(bm_, cap_ends=True, segments=48, radius1=r_, radius2=r_, depth=0.06)
        me_ = bpy.data.meshes.new('disc'); bm_.to_mesh(me_); bm_.free()
        ob_ = bpy.data.objects.new('disc', me_); ob_.location = (cx_, cy_, zr); ob_.data.materials.append(simple_mat(f'disc{i}', cols[i % len(cols)], rough=0.8)); link(ob_)
        if i % 2 == 0:
            bm_ = bmesh.new(); bmesh.ops.create_cone(bm_, cap_ends=True, segments=32, radius1=r_ * 0.55, radius2=r_ * 0.55, depth=0.08)
            me_ = bpy.data.meshes.new('disc2'); bm_.to_mesh(me_); bm_.free()
            ob2 = bpy.data.objects.new('disc2', me_); ob2.location = (cx_, cy_, zr + 0.01); ob2.data.materials.append(simple_mat(f'discb{i}', (0.96, 0.95, 0.9), rough=0.7)); link(ob2)

if VARIANT == 'lincoln':
    # open garage: columns and slab edges only, cars visible on every level
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
    hall_y = 38.5
    for gx in range(2, 44, 8):
        for gy in range(6, 124, 8):
            if not inside((gx, gy), base_poly): continue
            top = 29.1 if gy > hall_y else 21.1
            box('lcolumn', (0.55, 0.55, top), (gx, gy, top / 2), (0, 0, 0), conc_)
    carc = [(0.9, 0.9, 0.9), (0.06, 0.06, 0.07), (0.5, 0.52, 0.55), (0.55, 0.1, 0.08), (0.1, 0.2, 0.4), (0.8, 0.77, 0.7)]
    levels = [(7.0, 0.35), (10.3, 0.35), (13.6, 0.35), (8.65, 0.35), (11.95, 0.35), (15.25, 0.35)]
    ci = 0
    for z0, th in levels:
        for gy in range(8, 120, 5):
            for gx in (6.0, 13.0, 30.0, 37.0):
                if rr.random() < 0.22 or not inside((gx, gy), base_poly): continue
                col_ = simple_mat(f'lc{ci % 6}', carc[ci % 6], rough=0.25, coat=0.8); ci += 1
                box('lcar', (1.8, 4.4, 1.35), (gx, gy, z0 + th + 0.7), (0, 0, 0), col_, bevel=0.12)
    # thick white slab edge band on every level (reads as the exposed concrete plates of 1111 Lincoln Road)
    for pp in D['parts']:
        if pp['mat'] == 'slab':
            prism('slabedge', pp['pts'], pp['z0'] - 0.25, 0.6, M['concrete'])
'''
rep("\nfor p in D.get('solar', []):\n    o = flat('solar'", geom + "\nfor p in D.get('solar', []):\n    o = flat('solar'")
open(p, 'w', encoding='utf8').write(s)
print('patched')
