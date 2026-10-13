import os
p = os.path.join(os.environ['TEMP'], 'bl', 'build_scene.py')
s = open(p, encoding='utf8').read()


def rep(a, b):
    global s
    if a not in s:
        print('MISSING', a[:70]); return
    s = s.replace(a, b, 1)


# fillers
rep("# ------------------------------------------------------------------ the building",
    """FILL = os.path.join(os.environ.get('JD_FILL', ''), 'fillers.json')
if os.path.exists(FILL):
    for i, b in enumerate(json.load(open(FILL))):
        o = prism(f'fill{i}', b['pts'], 0, b['h'], CTXM[(i * 7 + 3) % len(CTXM)])
        if o:
            o.data.materials.append(M['concrete'])
            for pgn in o.data.polygons:
                if pgn.normal.z > 0.5: pgn.material_index = 1

# ------------------------------------------------------------------ the building""")
# remove floating lift box
rep("    box('lift', (1.6, 1.6, 2.2), (sh[0], sh[1], 3.5), (0, 0, 0), M['interior'])\n", "")
# night / dusk interior glow lower
rep("M['interior'] = simple_mat('interior', (1.0, 0.72, 0.4), rough=1.0, emit=(1.0, 0.62, 0.28), emit_str=5.0)",
    "M['interior'] = simple_mat('interior', (1.0, 0.72, 0.4), rough=1.0, emit=(1.0, 0.62, 0.28), emit_str=(1.1 if NIGHT else 0.5))")
rep("M['inner'] = simple_mat('inner', (0.5, 0.35, 0.2), rough=0.9, emit=(1.0, 0.55, 0.25), emit_str=0.9)",
    "M['inner'] = simple_mat('inner', (0.5, 0.35, 0.2), rough=0.9, emit=(1.0, 0.55, 0.25), emit_str=(0.6 if NIGHT else 0.15))")
rep("    bg.inputs['Strength'].default_value = 0.9 if NIGHT else 1.0", "    bg.inputs['Strength'].default_value = 0.22 if NIGHT else 0.8")
rep("os.environ.get('JD_EXPO', '0.0' if not LIT else '0.6')", "os.environ.get('JD_EXPO', '0.0' if not LIT else ('0.3' if NIGHT else '-0.4'))")
# lawn: noisy grass look
rep("M['lawn'] = simple_mat('lawn', (0.1, 0.2, 0.05), rough=0.95)", """def grass_mat():
    m = bpy.data.materials.new('lawn'); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); b = nt.nodes.new('ShaderNodeBsdfPrincipled')
    tc = nt.nodes.new('ShaderNodeTexCoord'); n1 = nt.nodes.new('ShaderNodeTexNoise'); n1.inputs['Scale'].default_value = 1.4; n1.inputs['Detail'].default_value = 6
    n2 = nt.nodes.new('ShaderNodeTexNoise'); n2.inputs['Scale'].default_value = 90.0; n2.inputs['Detail'].default_value = 2
    nt.links.new(tc.outputs['Object'], n1.inputs['Vector']); nt.links.new(tc.outputs['Object'], n2.inputs['Vector'])
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].color = (0.035, 0.09, 0.02, 1); ramp.color_ramp.elements[1].color = (0.16, 0.26, 0.07, 1)
    nt.links.new(n1.outputs['Fac'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], b.inputs['Base Color']); b.inputs['Roughness'].default_value = 0.95
    bump = nt.nodes.new('ShaderNodeBump'); bump.inputs['Strength'].default_value = 0.6; bump.inputs['Distance'].default_value = 0.05
    nt.links.new(n2.outputs['Fac'], bump.inputs['Height']); nt.links.new(bump.outputs['Normal'], b.inputs['Normal'])
    nt.links.new(b.outputs['BSDF'], out.inputs['Surface'])
    return m


M['lawn'] = grass_mat()""")
# roof deck lighter paving
rep("        prism('deck', p['pts'], p['z0'], p['h'], M['paving'])", "        prism('deck', p['pts'], p['z0'], p['h'], M['deckpave'])")
rep("M['paving'] = tex_mat('paving', 'concrete_floor_worn_001', scale=3.0, nstr=0.5, tint=(0.95, 0.93, 0.9, 1))",
    "M['paving'] = tex_mat('paving', 'concrete_floor_worn_001', scale=3.0, nstr=0.5, tint=(0.95, 0.93, 0.9, 1))\nM['deckpave'] = tex_mat('deckpave', 'concrete_floor_worn_001', scale=1.6, nstr=0.4, tint=(1.5, 1.45, 1.38, 1))")
# people: slimmer, legs + torso + head
a = s.index("fig_cols = [")
b = s.index("# lights (night)")
new = '''tops = [(0.75, 0.75, 0.72), (0.2, 0.25, 0.35), (0.55, 0.18, 0.15), (0.85, 0.8, 0.65), (0.15, 0.3, 0.22), (0.9, 0.9, 0.9), (0.4, 0.4, 0.45)]
legs_c = [(0.06, 0.07, 0.1), (0.15, 0.17, 0.22), (0.3, 0.28, 0.25), (0.05, 0.05, 0.05)]
skin_c = [(0.78, 0.6, 0.5), (0.65, 0.48, 0.38), (0.5, 0.36, 0.28)]
people = [p for p in D.get('people', [])]
if V.get('clearPeople'):
    cx_, cy_, r_ = V['eye'][0], V['eye'][1], V['clearPeople']
    people = [p for p in people if math.hypot(p[0] - cx_, p[1] - cy_) > r_]
for i, p in enumerate(people):
    h = random.uniform(1.58, 1.84); yaw = random.uniform(0, 6.2)
    lm = simple_mat(f'leg{i % 4}', legs_c[i % 4], rough=0.85)
    tm = simple_mat(f'top{i % 7}', tops[i % 7], rough=0.8)
    sm = simple_mat(f'skin{i % 3}', skin_c[i % 3], rough=0.6)
    z0 = p[2]
    for off in (-0.085, 0.085):
        lx = p[0] - math.sin(yaw) * off; ly = p[1] + math.cos(yaw) * off
        box('leg', (0.14, 0.14, h * 0.5), (lx, ly, z0 + h * 0.25), (0, 0, yaw), lm, bevel=0.03)
    box('torso', (0.24, 0.40, h * 0.34), (p[0], p[1], z0 + h * 0.5 + h * 0.17), (0, 0, yaw), tm, bevel=0.05)
    for off in (-0.25, 0.25):
        ax_ = p[0] - math.sin(yaw) * off; ay_ = p[1] + math.cos(yaw) * off
        box('arm', (0.1, 0.1, h * 0.33), (ax_, ay_, z0 + h * 0.5 + h * 0.15), (0, 0, yaw), tm, bevel=0.03)
    bm_ = bmesh.new(); bmesh.ops.create_uvsphere(bm_, u_segments=12, v_segments=8, radius=0.115)
    me = bpy.data.meshes.new('head'); bm_.to_mesh(me); bm_.free()
    ho = bpy.data.objects.new('head', me); ho.location = (p[0], p[1], z0 + h * 0.5 + h * 0.34 + 0.14); ho.data.materials.append(sm); link(ho)

'''
s = s[:a] + new + s[b:]
open(p, 'w', encoding='utf8').write(s)
print('ok')
