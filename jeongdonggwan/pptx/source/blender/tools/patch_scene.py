import re, os
p = os.path.join(os.environ['TEMP'], 'bl', 'build_scene.py')
s = open(p, encoding='utf8').read()
a = s.index("def screen_mat(")
b = s.index("def window_wall_mat(")
new = '''def screen_mat(name, wood_tex='dark_wood', pitch=0.24, slat=0.15):
    """timber slat screen (목재 슬랫 스크린, Saint-Luc 방식): vertical hardwood slats with open gaps"""
    base = os.path.join(PH, 'tex', wood_tex)
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); b = nt.nodes.new('ShaderNodeBsdfPrincipled')
    geo = nt.nodes.new('ShaderNodeNewGeometry')
    sep_p = nt.nodes.new('ShaderNodeSeparateXYZ'); nt.links.new(geo.outputs['Position'], sep_p.inputs['Vector'])
    sep_n = nt.nodes.new('ShaderNodeSeparateXYZ'); nt.links.new(geo.outputs['Normal'], sep_n.inputs['Vector'])
    # tangent coordinate along a vertical wall: t = -x*ny + y*nx
    m1 = nt.nodes.new('ShaderNodeMath'); m1.operation = 'MULTIPLY'; nt.links.new(sep_p.outputs['X'], m1.inputs[0]); nt.links.new(sep_n.outputs['Y'], m1.inputs[1])
    m2 = nt.nodes.new('ShaderNodeMath'); m2.operation = 'MULTIPLY'; nt.links.new(sep_p.outputs['Y'], m2.inputs[0]); nt.links.new(sep_n.outputs['X'], m2.inputs[1])
    tt = nt.nodes.new('ShaderNodeMath'); tt.operation = 'SUBTRACT'; nt.links.new(m2.outputs[0], tt.inputs[0]); nt.links.new(m1.outputs[0], tt.inputs[1])
    # u = fract(t / pitch)  -> slat where u < slat/pitch
    dv = nt.nodes.new('ShaderNodeMath'); dv.operation = 'DIVIDE'; dv.inputs[1].default_value = pitch; nt.links.new(tt.outputs[0], dv.inputs[0])
    fr = nt.nodes.new('ShaderNodeMath'); fr.operation = 'FRACT'; nt.links.new(dv.outputs[0], fr.inputs[0])
    thr = nt.nodes.new('ShaderNodeMath'); thr.operation = 'LESS_THAN'; thr.inputs[1].default_value = slat / pitch; nt.links.new(fr.outputs[0], thr.inputs[0])
    # wood texture mapped on object coords (vertical grain along z)
    tc = nt.nodes.new('ShaderNodeTexCoord'); mp = nt.nodes.new('ShaderNodeMapping')
    mp.inputs['Scale'].default_value = (2.2, 2.2, 0.55)
    nt.links.new(tc.outputs['Object'], mp.inputs['Vector'])
    def it(suffix, nonc):
        t = nt.nodes.new('ShaderNodeTexImage'); t.image = img(os.path.join(base, f'{wood_tex}_{suffix}_1k.jpg'), nonc)
        t.projection = 'BOX'; t.projection_blend = 0.2; t.interpolation = 'Cubic'
        nt.links.new(mp.outputs['Vector'], t.inputs['Vector']); return t
    d = it('Diffuse', False); r = it('Rough', True); n = it('nor_gl', True)
    tint = nt.nodes.new('ShaderNodeMix'); tint.data_type = 'RGBA'; tint.blend_type = 'MULTIPLY'
    tint.inputs['Factor'].default_value = 1.0; tint.inputs[7].default_value = (1.35, 0.9, 0.65, 1)
    nt.links.new(d.outputs['Color'], tint.inputs[6])
    nm = nt.nodes.new('ShaderNodeNormalMap'); nm.inputs['Strength'].default_value = 0.6; nt.links.new(n.outputs['Color'], nm.inputs['Color'])
    bump = nt.nodes.new('ShaderNodeBump'); bump.inputs['Strength'].default_value = 0.5; bump.inputs['Distance'].default_value = 0.02
    nt.links.new(fr.outputs[0], bump.inputs['Height']); nt.links.new(nm.outputs['Normal'], bump.inputs['Normal'])
    nt.links.new(tint.outputs[2], b.inputs['Base Color']); nt.links.new(r.outputs['Color'], b.inputs['Roughness'])
    nt.links.new(bump.outputs['Normal'], b.inputs['Normal'])
    tp = nt.nodes.new('ShaderNodeBsdfTransparent')
    mx = nt.nodes.new('ShaderNodeMixShader')
    nt.links.new(thr.outputs[0], mx.inputs['Fac'])
    nt.links.new(tp.outputs[0], mx.inputs[1]); nt.links.new(b.outputs['BSDF'], mx.inputs[2])
    nt.links.new(mx.outputs[0], out.inputs['Surface'])
    m.use_backface_culling = False
    return m


'''
s = s[:a] + new + s[b:]
s = s.replace("M['steel_red'] = simple_mat('steel_red', (0.62, 0.07, 0.04), rough=0.35, metal=0.0, coat=0.5)",
              "M['steel_red'] = simple_mat('steel_black', (0.012, 0.012, 0.014), rough=0.32, metal=0.55, coat=0.6)")
s = s.replace("M['screen'] = screen_mat('screen')", "M['screen'] = screen_mat('screen')")
open(p, 'w', encoding='utf8').write(s)
print('patched')
