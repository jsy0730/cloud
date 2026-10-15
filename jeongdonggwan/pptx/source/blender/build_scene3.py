# -*- coding: utf-8 -*-
# 정동관 photoreal scene for Blender 5.x (Cycles)
# usage: blender -b --python build_scene.py -- <view> <out.png> <samples> <res_x> [save.blend]
import bpy, bmesh, json, math, os, random, sys
from mathutils import Vector, Matrix, Euler

ARGS = sys.argv[sys.argv.index('--') + 1:]
VIEW, OUT, SAMPLES, RESX = ARGS[0], ARGS[1], int(ARGS[2]), int(ARGS[3])
SAVE = ARGS[4] if len(ARGS) > 4 else None
ROOT = os.environ['JD_ROOT']      # .../build/render
PH = os.environ['JD_PH']          # Poly Haven assets dir
D = json.load(open(os.path.join(ROOT, 'design.json'), encoding='utf8'))
C = json.load(open(os.path.join(ROOT, 'context.json'), encoding='utf8'))
V = json.load(open(os.environ.get('JD_VIEWS', os.path.join(ROOT, 'views4.json')), encoding='utf8'))[VIEW]
NIGHT = bool(V.get('night')) or bool(os.environ.get('JD_NIGHT')); DUSK = bool(V.get('dusk')) or bool(os.environ.get('JD_DUSK'))
VARIANT = os.environ.get('JD_VARIANT', '')
LIT = NIGHT or DUSK
random.seed(11)

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
coll = scene.collection


# ------------------------------------------------------------------ helpers
def dedupe(pts):
    out = []
    for p in pts:
        if not out or abs(out[-1][0] - p[0]) > 1e-4 or abs(out[-1][1] - p[1]) > 1e-4:
            out.append(tuple(p))
    if len(out) > 1 and abs(out[0][0] - out[-1][0]) < 1e-4 and abs(out[0][1] - out[-1][1]) < 1e-4:
        out.pop()
    return out


def link(ob, parent_coll=None):
    (parent_coll or coll).objects.link(ob)
    return ob


def prism(name, pts, z0, h, mat, caps=True):
    pts = dedupe(pts)
    if len(pts) < 3:
        return None
    bm = bmesh.new()
    vs = [bm.verts.new((x, y, z0)) for x, y in pts]
    try:
        f = bm.faces.new(vs)
    except ValueError:
        bm.free(); return None
    if f.normal.z > 0:
        f.normal_flip()
    ret = bmesh.ops.extrude_face_region(bm, geom=[f])
    verts = [e for e in ret['geom'] if isinstance(e, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, verts=verts, vec=(0, 0, h))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me)
    ob.data.materials.append(mat)
    link(ob)
    return ob


def flat(name, pts, z, mat):
    return prism(name, pts, z, 0.02, mat)


def box(name, size, loc, rot, mat, bevel=0.0):
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co.x *= size[0]; v.co.y *= size[1]; v.co.z *= size[2]
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me); ob.location = loc; ob.rotation_euler = rot
    ob.data.materials.append(mat); link(ob)
    if bevel > 0:
        m = ob.modifiers.new('bev', 'BEVEL'); m.width = bevel; m.segments = 2
    return ob


def img(path, nonc=False):
    im = bpy.data.images.load(path, check_existing=True)
    if nonc:
        im.colorspace_settings.name = 'Non-Color'
    return im


def tex_mat(name, tex_id, scale=2.0, nstr=0.6, tint=None, rough_mul=1.0, extra_rough=None):
    base = os.path.join(PH, 'tex', tex_id)
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled')
    tc = nt.nodes.new('ShaderNodeTexCoord'); mp = nt.nodes.new('ShaderNodeMapping')
    mp.inputs['Scale'].default_value = (1 / scale, 1 / scale, 1 / scale)
    nt.links.new(tc.outputs['Object'], mp.inputs['Vector'])
    def it(suffix, nonc):
        t = nt.nodes.new('ShaderNodeTexImage'); t.image = img(os.path.join(base, f'{tex_id}_{suffix}_1k.jpg'), nonc)
        t.projection = 'BOX'; t.projection_blend = 0.25; t.interpolation = 'Cubic'
        nt.links.new(mp.outputs['Vector'], t.inputs['Vector']); return t
    d = it('Diffuse', False); r = it('Rough', True); n = it('nor_gl', True)
    col = d.outputs['Color']
    if tint:
        mx = nt.nodes.new('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.blend_type = 'MULTIPLY'
        mx.inputs['Factor'].default_value = 1.0; mx.inputs[7].default_value = tint
        nt.links.new(d.outputs['Color'], mx.inputs[6]); col = mx.outputs[2]
    # (mesh has no UVs: a tangent-space normal map renders black on some orientations -> use a bump from the albedo)
    bw = nt.nodes.new('ShaderNodeRGBToBW'); nt.links.new(d.outputs['Color'], bw.inputs['Color'])
    nm = nt.nodes.new('ShaderNodeBump'); nm.inputs['Strength'].default_value = min(1.0, nstr * 0.6); nm.inputs['Distance'].default_value = 0.03
    nt.links.new(bw.outputs[0], nm.inputs['Height'])
    nt.links.new(col, bsdf.inputs['Base Color'])
    rv = r.outputs['Color']
    if rough_mul != 1.0:
        mm = nt.nodes.new('ShaderNodeMath'); mm.operation = 'MULTIPLY'; mm.inputs[1].default_value = rough_mul
        nt.links.new(rv, mm.inputs[0]); rv = mm.outputs[0]
    nt.links.new(rv, bsdf.inputs['Roughness'])
    nt.links.new(nm.outputs['Normal'], bsdf.inputs['Normal'])
    nt.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    return m


def simple_mat(name, color, rough=0.5, metal=0.0, emit=None, emit_str=0.0, coat=0.0, spec=0.5):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*color, 1)
    b.inputs['Roughness'].default_value = rough; b.inputs['Metallic'].default_value = metal
    for k, v in (('Coat Weight', coat),):
        if k in b.inputs: b.inputs[k].default_value = v
    if emit is not None:
        b.inputs['Emission Color'].default_value = (*emit, 1); b.inputs['Emission Strength'].default_value = emit_str
    return m


def glass_mat(name, tint=(0.62, 0.74, 0.8), reflect_rough=0.03, dark=0.18):
    """thin-walled glass: transparent mixed with fresnel reflection + a little tint"""
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    tr = nt.nodes.new('ShaderNodeBsdfTransparent'); tr.inputs['Color'].default_value = (*tint, 1)
    gl = nt.nodes.new('ShaderNodeBsdfGlossy'); gl.inputs['Roughness'].default_value = reflect_rough; gl.inputs['Color'].default_value = (0.9, 0.95, 1, 1)
    df = nt.nodes.new('ShaderNodeBsdfDiffuse'); df.inputs['Color'].default_value = (0.05, 0.07, 0.09, 1)
    fr = nt.nodes.new('ShaderNodeFresnel'); fr.inputs['IOR'].default_value = 1.5
    m1 = nt.nodes.new('ShaderNodeMixShader'); m1.inputs['Fac'].default_value = dark
    nt.links.new(tr.outputs[0], m1.inputs[1]); nt.links.new(df.outputs[0], m1.inputs[2])
    m2 = nt.nodes.new('ShaderNodeMixShader')
    # reflection strength: fresnel but boosted for architectural glass
    mth = nt.nodes.new('ShaderNodeMath'); mth.operation = 'MULTIPLY'; mth.inputs[1].default_value = 2.0; mth.use_clamp = True
    nt.links.new(fr.outputs[0], mth.inputs[0])
    nt.links.new(mth.outputs[0], m2.inputs['Fac'])
    nt.links.new(m1.outputs[0], m2.inputs[1]); nt.links.new(gl.outputs[0], m2.inputs[2])
    nt.links.new(m2.outputs[0], out.inputs['Surface'])
    m.use_backface_culling = False
    return m


def screen_mat(name, wood_tex='dark_wood', pitch=0.24, slat=0.15):
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
    tint.inputs['Factor'].default_value = 1.0; tint.inputs[7].default_value = (1.9, 1.35, 0.95, 1)
    nt.links.new(d.outputs['Color'], tint.inputs[6])
    bump = nt.nodes.new('ShaderNodeBump'); bump.inputs['Strength'].default_value = 0.5; bump.inputs['Distance'].default_value = 0.02
    nt.links.new(fr.outputs[0], bump.inputs['Height'])
    nt.links.new(tint.outputs[2], b.inputs['Base Color']); nt.links.new(r.outputs['Color'], b.inputs['Roughness'])
    nt.links.new(bump.outputs['Normal'], b.inputs['Normal'])
    tp = nt.nodes.new('ShaderNodeBsdfTransparent')
    mx = nt.nodes.new('ShaderNodeMixShader')
    nt.links.new(thr.outputs[0], mx.inputs['Fac'])
    nt.links.new(tp.outputs[0], mx.inputs[1]); nt.links.new(b.outputs['BSDF'], mx.inputs[2])
    nt.links.new(mx.outputs[0], out.inputs['Surface'])
    m.use_backface_culling = False
    return m


def window_wall_mat(name, wall=(0.72, 0.7, 0.66), glass=(0.08, 0.1, 0.12), floor_h=3.3, bay=3.0, win_frac=0.55):
    """context building facade: concrete wall with ribbon of glass windows (procedural)"""
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    wl = nt.nodes.new('ShaderNodeBsdfPrincipled'); wl.inputs['Base Color'].default_value = (*wall, 1); wl.inputs['Roughness'].default_value = 0.85
    gl = nt.nodes.new('ShaderNodeBsdfPrincipled'); gl.inputs['Base Color'].default_value = (*glass, 1); gl.inputs['Roughness'].default_value = 0.08
    gl.inputs['Metallic'].default_value = 0.0
    if 'Specular IOR Level' in gl.inputs: gl.inputs['Specular IOR Level'].default_value = 0.8
    tc = nt.nodes.new('ShaderNodeTexCoord'); sep = nt.nodes.new('ShaderNodeSeparateXYZ'); nt.links.new(tc.outputs['Object'], sep.inputs['Vector'])
    hs = nt.nodes.new('ShaderNodeMath'); hs.operation = 'ADD'; nt.links.new(sep.outputs['X'], hs.inputs[0]); nt.links.new(sep.outputs['Y'], hs.inputs[1])
    comb = nt.nodes.new('ShaderNodeCombineXYZ'); nt.links.new(hs.outputs[0], comb.inputs['X']); nt.links.new(sep.outputs['Z'], comb.inputs['Y'])
    br = nt.nodes.new('ShaderNodeTexBrick'); br.offset = 0.0
    br.inputs['Color1'].default_value = (1, 1, 1, 1); br.inputs['Color2'].default_value = (1, 1, 1, 1); br.inputs['Mortar'].default_value = (0, 0, 0, 1)
    br.inputs['Brick Width'].default_value = bay; br.inputs['Row Height'].default_value = floor_h
    br.inputs['Mortar Size'].default_value = 0.02 + (1 - win_frac) * 0.12; br.inputs['Mortar Smooth'].default_value = 0.0
    nt.links.new(comb.outputs[0], br.inputs['Vector'])
    # no windows on the top 1.2 m (parapet) and below 0.9 m
    mx = nt.nodes.new('ShaderNodeMixShader')
    nt.links.new(br.outputs['Color'], mx.inputs['Fac']); nt.links.new(wl.outputs[0], mx.inputs[1]); nt.links.new(gl.outputs[0], mx.inputs[2])
    nt.links.new(mx.outputs[0], out.inputs['Surface'])
    return m



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
    elif VARIANT == 'pnp':
        mat = M['pnp']
    elif VARIANT == 'herma':
        mat = M['herma']
    elif VARIANT == 'saintluc':
        mat = M['saintluc']
    elif VARIANT == 'blaibach':
        mat = M['blaibach']
    else:
        mat = M['screen']
    _SCR_CACHE[key] = mat
    return mat



# ================================================================== v3 additions
SLATS = os.environ.get('JD_SLATS', '1') == '1' and not VARIANT
SLAT_W, SLAT_P, SLAT_T = 0.30, 0.62, 0.12      # width, pitch, thickness (m)
LEAN = 0.36                                    # tan of lean angle (~20 deg), alternates by floor


def hexa(bm, v):
    vs = [bm.verts.new(c) for c in v]
    for f in ((0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)):
        try:
            bm.faces.new([vs[i] for i in f])
        except ValueError:
            pass


def obox(bm, c, ux, uy, uz, sx, sy, sz):
    """oriented box centred at c with unit axes ux,uy,uz and full sizes sx,sy,sz"""
    c = Vector(c); ux = Vector(ux); uy = Vector(uy); uz = Vector(uz)
    hx, hy, hz = ux * sx / 2, uy * sy / 2, uz * sz / 2
    v = [c - hx - hy - hz, c + hx - hy - hz, c + hx + hy - hz, c - hx + hy - hz,
         c - hx - hy + hz, c + hx - hy + hz, c + hx + hy + hz, c - hx + hy + hz]
    hexa(bm, [tuple(x) for x in v])


def finish(bm, name, mats):
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    for m in mats:
        me.materials.append(m)
    ob = bpy.data.objects.new(name, me); link(ob)
    return ob


def wood_board_mat(name, tint, rough_mul=1.0):
    base = os.path.join(PH, 'tex', 'dark_wood')
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); b = nt.nodes.new('ShaderNodeBsdfPrincipled')
    tc = nt.nodes.new('ShaderNodeTexCoord'); mp = nt.nodes.new('ShaderNodeMapping')
    mp.inputs['Scale'].default_value = (1.6, 1.6, 0.45)
    nt.links.new(tc.outputs['Object'], mp.inputs['Vector'])
    def it(suffix, nonc):
        t = nt.nodes.new('ShaderNodeTexImage'); t.image = img(os.path.join(base, f'dark_wood_{suffix}_1k.jpg'), nonc)
        t.projection = 'BOX'; t.projection_blend = 0.2; t.interpolation = 'Cubic'
        nt.links.new(mp.outputs['Vector'], t.inputs['Vector']); return t
    d = it('Diffuse', False); r = it('Rough', True)
    tn = nt.nodes.new('ShaderNodeMix'); tn.data_type = 'RGBA'; tn.blend_type = 'MULTIPLY'
    tn.inputs['Factor'].default_value = 1.0; tn.inputs[7].default_value = (*tint, 1)
    nt.links.new(d.outputs['Color'], tn.inputs[6])
    bw = nt.nodes.new('ShaderNodeRGBToBW'); nt.links.new(d.outputs['Color'], bw.inputs['Color'])
    bump = nt.nodes.new('ShaderNodeBump'); bump.inputs['Strength'].default_value = 0.35; bump.inputs['Distance'].default_value = 0.01
    nt.links.new(bw.outputs[0], bump.inputs['Height'])
    nt.links.new(tn.outputs[2], b.inputs['Base Color']); nt.links.new(r.outputs['Color'], b.inputs['Roughness'])
    nt.links.new(bump.outputs['Normal'], b.inputs['Normal'])
    nt.links.new(b.outputs['BSDF'], out.inputs['Surface'])
    return m


def poly_area(pts):
    return sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1] for i in range(len(pts))) / 2.0


def pip(pt, poly):
    x, y = pt; ins = False; n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]; x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1 + 1e-12) + x1:
            ins = not ins
    return ins


def dist_edges(pt, poly):
    best = 1e9; n = len(poly)
    for i in range(n):
        ax, ay = poly[i]; bx, by = poly[(i + 1) % n]
        dx, dy = bx - ax, by - ay; L2 = dx * dx + dy * dy or 1e-9
        t = max(0.0, min(1.0, ((pt[0] - ax) * dx + (pt[1] - ay) * dy) / L2))
        best = min(best, math.hypot(pt[0] - (ax + t * dx), pt[1] - (ay + t * dy)))
    return best


def build_slats(parts, mats):
    rnd = random.Random(7)
    bms = [bmesh.new() for _ in mats]
    rails = bmesh.new()
    for pi, p in enumerate(parts):
        pts = dedupe(p['pts']); n = len(pts)
        if n < 3:
            continue
        sgn = 1.0 if poly_area(pts) > 0 else -1.0       # CCW: outward normal is right of the edge
        level = int(round(p['z0'] / 3.3))
        lean = LEAN * (1 if level % 2 == 0 else -1)
        z0, h = p['z0'] + 0.02, p['h'] - 0.04
        for i in range(n):
            a = pts[i]; b = pts[(i + 1) % n]
            L = math.hypot(b[0] - a[0], b[1] - a[1])
            if L < 0.9:
                continue
            u = Vector(((b[0] - a[0]) / L, (b[1] - a[1]) / L, 0.0))
            nn = Vector((sgn * u.y, -sgn * u.x, 0.0))
            zz = Vector((0, 0, 1))
            cnt = max(1, int((L - SLAT_W) / SLAT_P) + 1)
            off = (L - ((cnt - 1) * SLAT_P + SLAT_W)) / 2 + SLAT_W / 2
            for k in range(cnt):
                s0 = off + k * SLAT_P
                jit = lean * (1 + rnd.uniform(-0.12, 0.12))
                dl = h * jit
                s_top = max(SLAT_W / 2, min(L - SLAT_W / 2, s0 + dl))
                s_bot = max(SLAT_W / 2, min(L - SLAT_W / 2, s0))
                base = Vector((a[0], a[1], z0)) + nn * 0.03
                hw = u * (SLAT_W / 2); th = nn * SLAT_T
                bot = base + u * s_bot; top = base + u * s_top + zz * h
                v = [bot - hw, bot + hw, bot + hw + th, bot - hw + th,
                     top - hw, top + hw, top + hw + th, top - hw + th]
                hexa(bms[rnd.randrange(len(bms))], [tuple(c) for c in v])
            # horizontal steel rails behind the boards (mid + top)
            for zr in (z0 + h * 0.5, z0 + h):
                obox(rails, Vector((a[0], a[1], zr)) + u * (L / 2) + nn * 0.02, u, nn, zz, L, 0.05, 0.06)
    out = []
    for k, bm in enumerate(bms):
        out.append(finish(bm, f'slats{k}', [mats[k]]))
    out.append(finish(rails, 'slatrails', [M['dark']]))
    return out


def build_interior(parts):
    """open parking deck behind the slats: columns + parked cars (instanced)"""
    rnd = random.Random(23)
    cols = bmesh.new()
    carcols = [(0.88, 0.88, 0.86), (0.04, 0.045, 0.05), (0.42, 0.45, 0.48), (0.42, 0.07, 0.05), (0.1, 0.17, 0.32), (0.72, 0.7, 0.62)]
    car_meshes = []
    for ci, cc in enumerate(carcols):
        bm = bmesh.new()
        body = []
        # lower body, cabin, wheels as one mesh with 3 material slots
        def carbox(c, sx, sy, sz, mi):
            q = bmesh.new()
            obox(q, c, (1, 0, 0), (0, 1, 0), (0, 0, 1), sx, sy, sz)
            return q
        me = bpy.data.meshes.new(f'car{ci}')
        bmc = bmesh.new()
        obox(bmc, (0, 0, 0.62), (1, 0, 0), (0, 1, 0), (0, 0, 1), 4.4, 1.8, 0.7)
        obox(bmc, (-0.15, 0, 1.2), (1, 0, 0), (0, 1, 0), (0, 0, 1), 2.4, 1.62, 0.55)
        for dx, dy in ((1.4, 0.9), (1.4, -0.9), (-1.4, 0.9), (-1.4, -0.9)):
            obox(bmc, (dx, dy, 0.33), (1, 0, 0), (0, 1, 0), (0, 0, 1), 0.66, 0.24, 0.66)
        bmesh.ops.recalc_face_normals(bmc, faces=bmc.faces)
        bmc.to_mesh(me); bmc.free()
        me.materials.append(simple_mat(f'icar{ci}', cc, rough=0.25, coat=1.0))
        car_meshes.append(me)
    ncar = 0
    for p in parts:
        pts = dedupe(p['pts'])
        if len(pts) < 3:
            continue
        zf = p['z0'] + (0.04 if p['z0'] < 1 else 0.0)
        xs = [q[0] for q in pts]; ys = [q[1] for q in pts]
        # columns on a structural grid
        gx = 0.0
        x = min(xs) + 3.0
        while x < max(xs):
            y = min(ys) + 4.0
            while y < max(ys):
                if pip((x, y), pts) and dist_edges((x, y), pts) > 1.0:
                    obox(cols, (x, y, zf + p['h'] / 2), (1, 0, 0), (0, 1, 0), (0, 0, 1), 0.55, 0.55, p['h'])
                y += 8.1
            x += 7.5
        # parked cars: stalls along the facade zone (visible depth ~ 9 m)
        x = min(xs) + 1.5
        while x < max(xs) - 1.0:
            y = min(ys) + 2.0
            while y < max(ys) - 1.0:
                pt = (x, y)
                d = dist_edges(pt, pts)
                if pip(pt, pts) and 2.6 < d < 9.5 and rnd.random() < 0.62:
                    # park nose-in: cars point along x (west/east facades) most of the time
                    yaw = math.pi / 2 if rnd.random() < 0.15 else 0.0
                    ob = bpy.data.objects.new('icar', car_meshes[rnd.randrange(len(car_meshes))])
                    ob.location = (x, y, zf); ob.rotation_euler = (0, 0, yaw + math.pi / 2); link(ob); ncar += 1
                y += 2.6
            x += 5.6
    finish(cols, 'columns', [M['concrete']])
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
    finish(lit, 'deck_lights', [simple_mat('decklight', (1.0, 0.95, 0.85), rough=0.5, emit=(1.0, 0.92, 0.78), emit_str=(9.0 if LIT else 2.2))])
    print('interior cars', ncar)


# ------------------------------------------------------------------ materials
M = {}
M['concrete'] = tex_mat('concrete', 'concrete_wall_003', scale=3.0, nstr=0.5, tint=(0.85, 0.88, 0.92, 1))
M['slab'] = simple_mat('slab', (0.58, 0.58, 0.57), rough=0.85)
M['asphalt'] = tex_mat('asphalt', 'asphalt_02', scale=4.0, nstr=0.6, tint=(0.30, 0.30, 0.32, 1)) if SLATS else tex_mat('asphalt', 'asphalt_02', scale=4.0, nstr=0.8, tint=(1.5, 1.5, 1.5, 1))
M['paving'] = tex_mat('paving', 'concrete_floor_worn_001', scale=3.0, nstr=0.5, tint=(0.95, 0.93, 0.9, 1))
M['sidewalk'] = tex_mat('sidewalk', 'concrete_floor_worn_001', scale=1.4, nstr=0.5, tint=(2.3, 2.25, 2.15, 1))
M['tread'] = simple_mat('tread', (0.035, 0.035, 0.04), rough=0.5, metal=0.35)
M['nose'] = simple_mat('nose', (0.32, 0.32, 0.34), rough=0.55)
if SLATS:
    M['wood'] = [wood_board_mat('wood0', (1.55, 1.5, 1.2)), wood_board_mat('wood1', (1.25, 1.22, 1.0)), wood_board_mat('wood2', (1.95, 1.85, 1.5))]
M['deckpave'] = tex_mat('deckpave', 'concrete_floor_worn_001', scale=1.6, nstr=0.4, tint=(2.3, 2.25, 2.15, 1))
if os.environ.get('JD_DEBUG') == 'paving':
    M['paving'] = simple_mat('paving_dbg', (1, 0, 0), rough=0.5)
if os.environ.get('JD_DEBUG') == 'asphalt':
    M['asphalt'] = simple_mat('asph_dbg', (0, 0, 1), rough=0.5)
M['screen'] = screen_mat('screen')
if VARIANT == 'green': M['greenwall'] = green_wall_mat('greenwall')
if VARIANT == 'pnp': M['pnp'] = pnp_mat('pnp')
if VARIANT == 'saintluc': M['saintluc'] = saintluc_mat('saintluc')
if VARIANT == 'blaibach': M['blaibach'] = blaibach_mat('blaibach')
if VARIANT == 'herma': M['herma'] = herma_mat('herma')
if VARIANT == 'lantern': M['lantern'] = lantern_mat('lantern', emit=(2.6 if NIGHT else 0.9))

M['glass'] = glass_mat('glass')
M['glass_rail'] = glass_mat('glass_rail', tint=(0.85, 0.92, 0.95), dark=0.05)
M['roof'] = simple_mat('roof', (0.62, 0.64, 0.66), rough=0.5, metal=0.6)
M['soffit'] = simple_mat('soffit', (0.14, 0.14, 0.15), rough=0.9)
M['inner'] = simple_mat('inner', (0.2, 0.17, 0.15), rough=0.95)
M['steel_red'] = simple_mat('steel_black', (0.012, 0.012, 0.014), rough=0.32, metal=0.55, coat=0.6)
M['dark'] = simple_mat('dark', (0.04, 0.045, 0.05), rough=0.45, metal=0.8)
M['pit'] = simple_mat('pit', (0.55, 0.52, 0.47), rough=0.9)
M['ground'] = simple_mat('ground', (0.32, 0.32, 0.31), rough=0.95)
if os.environ.get('JD_DEBUG') == 'ground':
    M['ground'] = simple_mat('ground_dbg', (1, 0.1, 0.1), rough=0.9)
def grass_mat():
    m = bpy.data.materials.new('lawn'); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); b = nt.nodes.new('ShaderNodeBsdfPrincipled')
    tc = nt.nodes.new('ShaderNodeTexCoord'); n1 = nt.nodes.new('ShaderNodeTexNoise'); n1.inputs['Scale'].default_value = 1.4; n1.inputs['Detail'].default_value = 6
    n2 = nt.nodes.new('ShaderNodeTexNoise'); n2.inputs['Scale'].default_value = 90.0; n2.inputs['Detail'].default_value = 2
    nt.links.new(tc.outputs['Object'], n1.inputs['Vector']); nt.links.new(tc.outputs['Object'], n2.inputs['Vector'])
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].color = (0.07, 0.14, 0.03, 1); ramp.color_ramp.elements[1].color = (0.27, 0.36, 0.1, 1)
    nt.links.new(n1.outputs['Fac'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], b.inputs['Base Color']); b.inputs['Roughness'].default_value = 0.95
    bump = nt.nodes.new('ShaderNodeBump'); bump.inputs['Strength'].default_value = 0.6; bump.inputs['Distance'].default_value = 0.05
    nt.links.new(n2.outputs['Fac'], bump.inputs['Height']); nt.links.new(bump.outputs['Normal'], b.inputs['Normal'])
    nt.links.new(b.outputs['BSDF'], out.inputs['Surface'])
    return m


M['lawn'] = grass_mat()
M['lamp'] = simple_mat('lamp', (0.1, 0.1, 0.11), rough=0.5, metal=0.8)
M['line'] = simple_mat('line', (0.8, 0.78, 0.65), rough=0.7)
M['white'] = simple_mat('white', (0.78, 0.78, 0.76), rough=0.7)
M['ctxroof'] = simple_mat('ctxroof', (0.5, 0.5, 0.49), rough=0.9)
if LIT:
    M['interior'] = simple_mat('interior', (1.0, 0.72, 0.4), rough=1.0, emit=(1.0, 0.62, 0.28), emit_str=(1.1 if NIGHT else 0.5))
    M['inner'] = simple_mat('inner', (0.5, 0.35, 0.2), rough=0.9, emit=(1.0, 0.55, 0.25), emit_str=(0.6 if NIGHT else 0.15))
    M['bulb'] = simple_mat('bulb', (1, 0.85, 0.6), rough=0.4, emit=(1.0, 0.75, 0.4), emit_str=35.0)
else:
    M['interior'] = simple_mat('interior', (0.52, 0.48, 0.42), rough=0.9)
    M['bulb'] = simple_mat('bulb', (1, 1, 0.9), rough=0.4, emit=(1, 1, 0.9), emit_str=2.0)
# context facade variants
CTXM = [window_wall_mat('ctx0', (0.8, 0.78, 0.74), bay=4.2, win_frac=0.5), window_wall_mat('ctx1', (0.7, 0.68, 0.64), bay=3.6, win_frac=0.45), window_wall_mat('ctx2', (0.86, 0.84, 0.8), bay=5.0, win_frac=0.4),
        window_wall_mat('ctx3', (0.64, 0.66, 0.68), glass=(0.1, 0.14, 0.18), bay=4.0, win_frac=0.55)]

if VARIANT:
    M['interior'] = simple_mat('interior_v', (0.10, 0.085, 0.075), rough=0.9, emit=(1.0, 0.6, 0.3), emit_str=(0.35 if LIT else 0.0))
    M['inner'] = simple_mat('inner_v', (0.035, 0.035, 0.045) if VARIANT != 'green' else (0.05, 0.075, 0.04), rough=0.9)
    if VARIANT == 'blaibach':
        M['inner'] = simple_mat('inner_b', (0.9, 0.55, 0.25), rough=0.9, emit=(1.0, 0.58, 0.22), emit_str=(5.0 if LIT else 0.4))

# ------------------------------------------------------------------ ground / roads
R = 900
gb = [(C['center'][0] - R, C['center'][1] - R), (C['center'][0] + R, C['center'][1] - R), (C['center'][0] + R, C['center'][1] + R), (C['center'][0] - R, C['center'][1] + R)]
ground = prism('ground', gb, -6.0, 6.0, M['ground'])
for p in D.get('pit', []):
    cut = prism('pitcut', p, -4.5, 8.0, M['pit'])
    mod = ground.modifiers.new('cut', 'BOOLEAN'); mod.operation = 'DIFFERENCE'; mod.object = cut; mod.solver = 'EXACT'
    bpy.context.view_layer.objects.active = ground
    bpy.ops.object.select_all(action='DESELECT'); ground.select_set(True)
    bpy.ops.object.modifier_apply(modifier='cut')
    bpy.data.objects.remove(cut)
    prism('pitfloor', p, -4.5, 0.05, M['pit'])


_RB = 0


def ribbon(a, b, w, z, mat, ext=0.3):
    L = math.hypot(b[0] - a[0], b[1] - a[1])
    if L < 0.1: return
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    cx, cy = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    global _RB
    _RB += 1
    # unique tiny z per ribbon: coplanar overlaps cause self-shadowing black patches in Cycles
    box('rb', (L + ext, w, 0.02), (cx, cy, z + (_RB % 160) * 0.00003), (0, 0, ang), mat)


for r in C['roads']:
    for i in range(len(r['pts']) - 1):
        ribbon(r['pts'][i], r['pts'][i + 1], r['w'] + 6, 0.01, M['paving'])
for r in C['roads']:
    for i in range(len(r['pts']) - 1):
        ribbon(r['pts'][i], r['pts'][i + 1], r['w'], 0.025 + r['w'] / 3000, M['asphalt'])
for r in C['roads']:
    if r['w'] >= 12:
        for i in range(len(r['pts']) - 1):
            a, b = r['pts'][i], r['pts'][i + 1]
            L = math.hypot(b[0] - a[0], b[1] - a[1])
            t = 0.0
            while t < L - 4:
                t0, t1 = t / L, (t + 4.5) / L
                ribbon((a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0), (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1), 0.16, 0.05 + r['w'] / 3000, M['line'], 0)
                t += 9
flat('plaza', D['block'][0], 0.03, M['paving'])

if SLATS:
    # raised sidewalk + curb along the west frontage, interrupted at the lane (소로) mouth so the road flows straight into it
    SW_W, SW_H = 4.6, 0.16
    LANE_Y1 = 29.5                                     # lane mouth spans y = 2.3 .. 28.1 on the west edge
    sw_len = 127.4 - LANE_Y1
    box('sidewalk', (SW_W, sw_len, SW_H), (-SW_W / 2, LANE_Y1 + sw_len / 2, SW_H / 2), (0, 0, 0), M['sidewalk'])
    box('curb', (0.22, sw_len, SW_H + 0.03), (-SW_W - 0.11, LANE_Y1 + sw_len / 2, (SW_H + 0.03) / 2), (0, 0, 0), simple_mat('curbmat', (0.62, 0.62, 0.6), rough=0.8))
    # a short curb return where the sidewalk ends beside the lane mouth
    box('curbret', (SW_W + 0.22, 0.22, SW_H + 0.03), (-SW_W / 2 - 0.11, LANE_Y1 - 0.11, (SW_H + 0.03) / 2), (0, 0, 0), simple_mat('curbmat2', (0.62, 0.62, 0.6), rough=0.8))
    # asphalt apron: carriageway -> lane, same black surface, no kerb in between
    flat('lane_apron', [(-26.0, -2.0), (0.6, -2.0), (0.6, 29.5), (-26.0, 29.5)], 0.05, M['asphalt'])
    D['trees'] = [t for t in D.get('trees', []) if t[2] > 1.0]       # keep roof trees only
    for yy_ in (62.0, 80.0, 100.0, 116.0):
        D['trees'].append([-2.3, yy_, SW_H, 1.15])
    D['cars'] = []; D['walks'] = []
    D['lamps'] = [l for l in D.get('lamps', []) if l[1] > 40 or l[1] < 0]     # keep the lane mouth and the stair clear
for p in D.get('lane', []): flat('lane', p, 0.04, M['asphalt'])
for p in D.get('tips', []): flat('tip', p, 0.045, M['paving'])
for p in D.get('walks', []): prism('walk', p, 0, 0.14, M['paving'])

# ------------------------------------------------------------------ context buildings
for i, b in enumerate(C['buildings']):
    o = prism(f'ctx{i}', b['pts'], 0, max(b['h'], 3.0), CTXM[i % len(CTXM)])
    if o: o.data.materials.append(M['ctxroof'])
    # roof cap face uses second material
    if o:
        for pgn in o.data.polygons:
            if pgn.normal.z > 0.5: pgn.material_index = 1

FILL = os.path.join(os.environ.get('JD_FILL', ''), 'fillers.json')
if os.path.exists(FILL):
    for i, b in enumerate(json.load(open(FILL))):
        o = prism(f'fill{i}', b['pts'], 0, b['h'], CTXM[(i * 7 + 3) % len(CTXM)])
        if o:
            o.data.materials.append(M['ctxroof'])
            for pgn in o.data.polygons:
                if pgn.normal.z > 0.5: pgn.material_index = 1

ROOMS = json.load(open(os.path.join(os.environ.get('JD_FILL', ''), 'rooms.json'))) if os.path.exists(os.path.join(os.environ.get('JD_FILL', ''), 'rooms.json')) else []
# ------------------------------------------------------------------ the building
SLAT_PARTS = []
for p in D['parts']:
    m = p['mat']
    if m in ('screen', 'base') and VARIANT == 'lincoln':
        continue
    if m in ('screen', 'base') and SLATS:
        SLAT_PARTS.append(p)
    elif m in ('screen', 'base'):
        prism('screen', p['pts'], p['z0'], p['h'], screen_for(p))
        if p.get('inner'):
            o = prism('inner', p['inner'], p['z0'], p['h'], M['inner'])
    elif m == 'fin' and VARIANT == 'blaibach':
        prism('block', p['pts'], p['z0'], p['h'], M['blaibach'])
    elif m in ('glass', 'fin'):
        prism('glass', p['pts'], p['z0'], p['h'], M['glass'])
        ins = Polygon_inset = None
        # interior volume so the glazing reads as a lit room, not a see-through box
        pi_ = D['parts'].index(p)
        rm = [r for r in ROOMS if r['i'] == pi_]
        if rm:
            _im = M['interior']
            if VARIANT:
                _im = simple_mat('interior_v', (0.07, 0.065, 0.06), rough=0.9, emit=(1.0, 0.62, 0.3), emit_str=(0.5 if LIT else 0.0))
            prism('room', rm[0]['pts'], p['z0'] + 0.1, p['h'] - 0.2, _im)
    elif m == 'slab':
        prism('slab', p['pts'], p['z0'], p['h'], M['slab'])
    elif m == 'roof':
        prism('roofcap', p['pts'], p['z0'], p['h'], M['roof'])
    elif m == 'roofdeck':
        prism('deck', p['pts'], p['z0'], p['h'], M['deckpave'])


if SLAT_PARTS:
    build_slats(SLAT_PARTS, M['wood'])
    build_interior(SLAT_PARTS)

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
    def offset_poly(pts, d):
        pts = dedupe(pts); n = len(pts)
        ar = sum(pts[i][0] * pts[(i + 1) % n][1] - pts[(i + 1) % n][0] * pts[i][1] for i in range(n)) / 2.0
        sgn = 1.0 if ar > 0 else -1.0     # CCW -> outward normal is right of the edge
        out_ = []
        for i in range(n):
            p0, p1, p2 = pts[i - 1], pts[i], pts[(i + 1) % n]
            def nrm(a_, b_):
                dx, dy = b_[0] - a_[0], b_[1] - a_[1]; L = math.hypot(dx, dy) or 1.0
                return (sgn * dy / L, -sgn * dx / L)
            n1, n2 = nrm(p0, p1), nrm(p1, p2)
            bx, by = n1[0] + n2[0], n1[1] + n2[1]; bl = math.hypot(bx, by) or 1.0
            cosh = max(0.35, (bx / bl) * n1[0] + (by / bl) * n1[1])
            out_.append((p1[0] + bx / bl * d / cosh, p1[1] + by / bl * d / cosh))
        return out_
    soil = simple_mat('planter', (0.25, 0.22, 0.2), rough=0.9)
    for p in D['parts']:
        if p['mat'] not in ('screen', 'base'): continue
        o = prism('planter', offset_poly(p['pts'], 0.18), p['z0'], 0.55, soil)
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

if VARIANT == 'saintluc':
    for pg in D.get('roof', []):
        prism('greenroof', [tuple(c) for c in pg], D['roofz'], 0.12, M['lawn'])

for p in D.get('solar', []):
    o = flat('solar', p['pts'], p['z'] + 0.06, simple_mat('solar', (0.03, 0.06, 0.12), rough=0.12, metal=0.4))
for p in D.get('lawns', []): prism('lawn', p, D['roofz'], 0.08, M['lawn'])
for pst in D.get('posts', []): box('post', (0.32, 0.32, pst[2]), (pst[0], pst[1], pst[2] / 2), (0, 0, 0), M['dark'])
for bm in D.get('beams', []):
    x1, y1, x2, y2, z = bm; L = math.hypot(x2 - x1, y2 - y1)
    box('beam', (L, 0.24, 0.34), ((x1 + x2) / 2, (y1 + y2) / 2, z), (0, 0, math.atan2(y2 - y1, x2 - x1)), M['dark'])
for pr in D.get('parapets', []):
    x1, y1, x2, y2, z = pr; L = math.hypot(x2 - x1, y2 - y1); yaw = math.atan2(y2 - y1, x2 - x1)
    box('par', (L, 0.05, 1.15), ((x1 + x2) / 2, (y1 + y2) / 2, z + 0.58), (0, 0, yaw), M['glass_rail'])
    box('parr', (L, 0.08, 0.05), ((x1 + x2) / 2, (y1 + y2) / 2, z + 1.16), (0, 0, yaw), M['dark'])
_st = bmesh.new(); _tr = bmesh.new(); _nz = bmesh.new()
_Z = Vector((0, 0, 1))
for sf in D.get('stairs', []):
    x1, y1, z1, x2, y2, z2, wd = sf
    P1 = Vector((x1, y1, z1)); P2 = Vector((x2, y2, z2))
    hv = Vector((x2 - x1, y2 - y1, 0.0)); run = hv.length; d = hv / run
    sv = Vector((-d.y, d.x, 0.0))                       # sideways (horizontal)
    tv = (P2 - P1).normalized(); nv = tv.cross(sv)       # along the slope / up from the slope
    if nv.z < 0: nv = -nv
    ln = (P2 - P1).length
    nst = max(8, int(round(run / 0.42)))
    g = run / nst; rise = (z2 - z1) / nst
    for i in range(nst):
        # tread (with a nosing overhang) and riser
        c = P1 + d * ((i + 0.5) * g + 0.015) + _Z * (i * rise + rise - 0.02)
        obox(_tr, c, d, sv, _Z, g + 0.03, wd, 0.04)
        obox(_nz, P1 + d * ((i + 1) * g - 0.02) + _Z * (i * rise + rise + 0.003), d, sv, _Z, 0.05, wd * 0.98, 0.012)
        obox(_st, P1 + d * (i * g) + _Z * (i * rise + rise / 2), d, sv, _Z, 0.025, wd, rise)
    mid = (P1 + P2) / 2
    # stringers (side beams) and soffit
    for sd in (-1, 1):
        obox(_st, mid + sv * sd * (wd / 2 + 0.03) + nv * -0.11, tv, sv, nv, ln, 0.06, 0.34)
    obox(_st, mid + nv * -0.20, tv, sv, nv, ln, wd, 0.05)
    # handrails (top + mid), balusters every 0.11 m, newel posts
    for sd in (-1, 1):
        sp = sv * sd * (wd / 2 + 0.03)
        obox(_st, mid + sp + _Z * 1.0, tv, sv, nv, ln, 0.06, 0.05)
        obox(_st, mid + sp + _Z * 0.55, tv, sv, nv, ln, 0.04, 0.03)
        nb = int(ln / 0.11)
        for j in range(nb + 1):
            t = j / nb
            pbase = P1 + (P2 - P1) * t + sp
            obox(_st, pbase + _Z * 0.52, d, sv, _Z, 0.022, 0.022, 1.0)
        for t in (0.0, 1.0):
            pp = P1 + (P2 - P1) * t + sp
            obox(_st, pp + _Z * 0.58, d, sv, _Z, 0.07, 0.07, 1.16)
    # landing pad beyond the end of the flight
    obox(_st, P2 + d * 0.9 + _Z * -0.02, d, sv, _Z, 1.8, wd + 0.1, 0.06)
    for sd in (-1, 1):
        obox(_st, P2 + d * 0.9 + sv * sd * (wd / 2 + 0.03) + _Z * 0.97, d, sv, _Z, 1.8, 0.06, 0.05)
finish(_st, 'stairs_steel', [M['steel_red']])
finish(_tr, 'stairs_tread', [M['tread']])
finish(_nz, 'stairs_nosing', [M['nose']])
for sh in D.get('shafts', []):
    box('shaft', (2.8, 2.8, sh[2]), (sh[0], sh[1], sh[2] / 2), (0, 0, 0), M['glass'])
    box('shaftframe', (3.0, 3.0, 0.4), (sh[0], sh[1], sh[2]), (0, 0, 0), M['dark'])

# ------------------------------------------------------------------ entourage: trees (Poly Haven), lamps, cars, benches, people
KEEP = {'tree_small_02': ('tree_small_02_trunk', 'tree_small_02_LOD1'),
        'jacaranda_tree': ('jacaranda_tree_trunk_LOD1', 'jacaranda_tree_LOD1')}


def append_tree(blend, names):
    with bpy.data.libraries.load(blend, link=False) as (src, dst):
        dst.objects = [n for n in src.objects if n in names]
    return [o for o in dst.objects if o is not None]


TREE_SRC = []
for tid in ('tree_small_02', 'jacaranda_tree'):
    p_ = os.path.join(PH, 'models', tid, f'{tid}_1k.blend')
    if os.path.exists(p_):
        TREE_SRC.append((tid, append_tree(p_, KEEP[tid])))
trees_coll = bpy.data.collections.new('trees'); coll.children.link(trees_coll)
for tid, objs in TREE_SRC:
    for o in objs:
        trees_coll.objects.link(o)
        o.hide_render = True; o.hide_viewport = True


def place_tree(x, y, z, s, k):
    # roof planters: small tree; street: alternate small tree / scaled-down jacaranda
    idx = 0 if (z > 1 or k % 2 == 0) else (1 if len(TREE_SRC) > 1 else 0)
    tid, objs = TREE_SRC[idx]
    base = 1.0 if tid == 'tree_small_02' else 0.3
    yaw = random.uniform(0, 6.28)
    sc = s * base * random.uniform(0.9, 1.3) * (1.5 if tid == 'tree_small_02' and z <= 1 else 1.0)
    e = bpy.data.objects.new('tree', None); e.location = (x, y, z); e.rotation_euler = (0, 0, yaw); e.scale = (sc, sc, sc); link(e)
    for o in objs:
        n = o.copy(); n.hide_render = False; n.hide_viewport = False
        n.parent = e; n.matrix_parent_inverse = Matrix.Identity(4); link(n)


TREES = list(D.get('trees', []))
if VARIANT == 'green':
    rr = random.Random(3)
    for _ in range(26):
        TREES.append([rr.uniform(3, 40), rr.uniform(4, 36), D['roofz'], rr.uniform(0.9, 1.35)])
    for yy in range(0, 128, 6):
        TREES.append([-5.2, yy, 0, 1.5])
if TREE_SRC:
    for i, t in enumerate(TREES):
        place_tree(t[0], t[1], t[2], t[3] if len(t) > 3 else 1.0, i)

for lp in D.get('lamps', []):
    box('pole', (0.12, 0.12, 6.5), (lp[0], lp[1], 3.25), (0, 0, 0), M['lamp'])
    box('head', (1.2, 0.3, 0.12), (lp[0] + 0.5, lp[1], 6.5), (0, 0, 0), M['bulb'])
wood_b = simple_mat('wood', (0.35, 0.22, 0.12), rough=0.6)
for bn in D.get('benches', []):
    z = D['roofz']
    box('bench_seat', (2.0, 0.5, 0.08), (bn[0], bn[1], z + 0.46), (0, 0, bn[2]), wood_b)
    for sx in (-0.8, 0.8):
        lx = bn[0] + math.cos(bn[2]) * sx; ly = bn[1] + math.sin(bn[2]) * sx
        box('bench_leg', (0.08, 0.4, 0.42), (lx, ly, z + 0.21), (0, 0, bn[2]), M['dark'])

carcols = [(0.9, 0.9, 0.9), (0.04, 0.045, 0.05), (0.45, 0.48, 0.5), (0.45, 0.08, 0.06), (0.1, 0.18, 0.35), (0.75, 0.72, 0.65), (0.08, 0.08, 0.09)]
for i, c in enumerate(D.get('cars', [])):
    x, y, yaw = c
    body = simple_mat(f'car{i}', carcols[i % len(carcols)], rough=0.22, metal=0.0, coat=1.0)
    g = box('carlow', (4.5, 1.8, 0.7), (x, y, 0.62), (0, 0, yaw), body, bevel=0.15)
    cab = box('cab', (2.4, 1.62, 0.62), (x, y, 1.25), (0, 0, yaw), simple_mat('cg', (0.03, 0.04, 0.05), rough=0.05, metal=0.2), bevel=0.15)
    cab.location = (x - math.cos(yaw) * 0.2, y - math.sin(yaw) * 0.2, 1.25)
    for dx, dy in ((1.4, 0.9), (1.4, -0.9), (-1.4, 0.9), (-1.4, -0.9)):
        wx = x + math.cos(yaw) * dx - math.sin(yaw) * dy; wy = y + math.sin(yaw) * dx + math.cos(yaw) * dy
        box('wheel', (0.7, 0.24, 0.7), (wx, wy, 0.35), (0, 0, yaw), M['dark'], bevel=0.1)

tops = [(0.75, 0.75, 0.72), (0.2, 0.25, 0.35), (0.55, 0.18, 0.15), (0.85, 0.8, 0.65), (0.15, 0.3, 0.22), (0.9, 0.9, 0.9), (0.4, 0.4, 0.45)]
legs_c = [(0.06, 0.07, 0.1), (0.15, 0.17, 0.22), (0.3, 0.28, 0.25), (0.05, 0.05, 0.05)]
skin_c = [(0.78, 0.6, 0.5), (0.65, 0.48, 0.38), (0.5, 0.36, 0.28)]
people = [p for p in D.get('people', [])]
if V.get('clearPeople'):
    cx_, cy_, r_ = V['eye'][0], V['eye'][1], V['clearPeople']
    people = [p for p in people if math.hypot(p[0] - cx_, p[1] - cy_) > r_]
if os.environ.get('JD_NOPEOPLE'):
    people = []
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

# lights (night)
if LIT:
    for l in D.get('lights', []):
        ld = bpy.data.lights.new('pl', 'POINT'); ld.energy = l[3] * 14; ld.color = (1.0, 0.72, 0.45); ld.shadow_soft_size = 0.6
        lo = bpy.data.objects.new('pl', ld); lo.location = (l[0], l[1], l[2]); link(lo)
    for lp in D.get('lamps', []):
        ld = bpy.data.lights.new('lamp', 'POINT'); ld.energy = 900; ld.color = (1.0, 0.8, 0.55); ld.shadow_soft_size = 0.2
        lo = bpy.data.objects.new('lamp', ld); lo.location = (lp[0] + 0.5, lp[1], 6.3); link(lo)
    for ll in D.get('laneLamps', []):
        ld = bpy.data.lights.new('ll', 'POINT'); ld.energy = 250; ld.color = (1.0, 0.85, 0.6)
        lo = bpy.data.objects.new('ll', ld); lo.location = (ll[0], ll[1], ll[2] - 0.3); link(lo)
    for sl in D.get('stringLights', []):
        box('bulb', (0.14, 0.14, 0.14), (sl[0], sl[1], sl[2]), (0, 0, 0), M['bulb'])

import numpy as np


def aligned_hdri(path, az_target_rad):
    """roll an equirect HDRI so its sun sits at compass azimuth az_target (Blender mapping: u = atan2(y,-x)/2pi + .5)"""
    src = bpy.data.images.load(path, check_existing=True)
    w, h = src.size
    arr = np.empty(w * h * 4, dtype=np.float32); src.pixels.foreach_get(arr)
    a = arr.reshape(h, w, 4)
    lum = a[..., :3].mean(axis=2)
    thr = np.percentile(lum, 99.995)
    ys, xs = np.where(lum >= thr)
    wts = lum[ys, xs]
    cu = float((xs * wts).sum() / wts.sum()) / w
    sun_el = (float((ys * wts).sum() / wts.sum()) / h - 0.5) * math.pi
    # target column from desired azimuth (elevation does not matter for u)
    ut = (0.25 + az_target_rad / (2 * math.pi)) % 1.0   # Cycles equirect: u = 0.5 - atan2(y,x)/2pi
    shift = int(round((ut - cu) * w))
    sun_mask = lum > 40.0
    a[..., :3][sun_mask] *= float(os.environ.get('JD_SUNSCALE', '0.45'))   # soften the sun so shadows keep detail
    rolled = np.roll(a, shift, axis=1)
    out = bpy.data.images.new('hdri_aligned', w, h, float_buffer=True, alpha=False)
    out.pixels.foreach_set(rolled.ravel()); out.pack() if False else None
    return out, math.degrees(sun_el)


# ------------------------------------------------------------------ world / sun / camera
world = bpy.data.worlds.new('world'); scene.world = world; world.use_nodes = True
wn = world.node_tree; wn.nodes.clear()
wout = wn.nodes.new('ShaderNodeOutputWorld'); bg = wn.nodes.new('ShaderNodeBackground')
az = math.radians(V.get('sunAz', 215)); el = math.radians(V.get('sunEl', 40))
if NIGHT or DUSK:
    hdr = 'satara_night_no_lamps_2k.hdr' if NIGHT else 'belfast_sunset_puresky_2k.hdr'
    env = wn.nodes.new('ShaderNodeTexEnvironment'); env.image = img(os.path.join(PH, 'hdri', hdr))
    mp = wn.nodes.new('ShaderNodeMapping'); tcn = wn.nodes.new('ShaderNodeTexCoord')
    mp.inputs['Rotation'].default_value = (0, 0, math.radians(100 if NIGHT else 220))
    wn.links.new(tcn.outputs['Generated'], mp.inputs['Vector']); wn.links.new(mp.outputs['Vector'], env.inputs['Vector'])
    wn.links.new(env.outputs['Color'], bg.inputs['Color'])
    bg.inputs['Strength'].default_value = 0.22 if NIGHT else 0.8
else:
    himg, hel = aligned_hdri(os.path.join(PH, 'hdri', 'kloofendal_48d_partly_cloudy_puresky_2k.hdr'), az)
    print('HDRI sun elevation', round(hel, 1))
    env = wn.nodes.new('ShaderNodeTexEnvironment'); env.image = himg
    wn.links.new(env.outputs['Color'], bg.inputs['Color']); bg.inputs['Strength'].default_value = 1.0
wn.links.new(bg.outputs[0], wout.inputs['Surface'])
if DUSK:
    sd = bpy.data.lights.new('sun', 'SUN'); sd.energy = 1.2; sd.angle = math.radians(1.0); sd.color = (1.0, 0.7, 0.45)
    so = bpy.data.objects.new('sun', sd)
    sunpos = Vector((math.sin(az) * math.cos(0.17), math.cos(az) * math.cos(0.17), math.sin(0.17)))
    so.rotation_euler = (-sunpos).to_track_quat('-Z', 'Y').to_euler(); link(so)

cam = bpy.data.cameras.new('cam'); cam.sensor_fit = 'VERTICAL'; cam.sensor_height = 24.0
cam.lens = 12.0 / math.tan(math.radians(V['fov']) / 2)
cam.clip_start = 0.1; cam.clip_end = 3000
co = bpy.data.objects.new('cam', cam); co.location = Vector(V['eye']); link(co)
direction = Vector(V['target']) - Vector(V['eye'])
if os.environ.get('JD_TESTSUN'):
    direction = Vector((math.sin(az) * math.cos(el), math.cos(az) * math.cos(el), math.sin(el)))
co.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
scene.camera = co
if os.environ.get('JD_TOPDOWN'):
    cam.type = 'ORTHO'; cam.ortho_scale = 140.0
    co.location = Vector((-20, 40, 150)); co.rotation_euler = (0, 0, 0)

# ------------------------------------------------------------------ render settings
for o in list(bpy.data.objects):
    h = os.environ.get('JD_HIDE', '')
    if h and any(o.name.startswith(k) for k in h.split(',')):
        o.hide_render = True
scene.render.engine = 'CYCLES'
cy = scene.cycles
cy.samples = SAMPLES; cy.use_adaptive_sampling = True; cy.adaptive_threshold = 0.02
cy.use_denoising = True; cy.denoiser = 'OPENIMAGEDENOISE'
cy.max_bounces = 10; cy.transmission_bounces = 12; cy.transparent_max_bounces = 24; cy.glossy_bounces = 6
cy.sample_clamp_indirect = 10.0
try:
    prefs = bpy.context.preferences.addons['cycles'].preferences
    prefs.compute_device_type = 'HIP'; prefs.get_devices()
    for d in prefs.devices:
        d.use = (d.type == 'HIP' and 'RX 9060' in d.name)
    if any(d.use for d in prefs.devices): cy.device = 'GPU'
except Exception as e:
    print('GPU setup failed:', e)
scene.render.resolution_x = RESX; scene.render.resolution_y = int(RESX * 9 / 16); scene.render.resolution_percentage = 100
scene.view_settings.view_transform = 'AgX'
try:
    scene.view_settings.look = 'AgX - Medium High Contrast'
except Exception:
    pass
scene.view_settings.exposure = float(os.environ.get('JD_EXPO', '0.0' if not LIT else ('0.3' if NIGHT else '-0.4')))
scene.render.image_settings.file_format = 'PNG'; scene.render.image_settings.color_depth = '8'
scene.render.filepath = OUT
if SAVE:
    bpy.ops.wm.save_as_mainfile(filepath=SAVE)
if os.environ.get('JD_RAYCAST'):
    dg = bpy.context.evaluated_depsgraph_get()
    tv = math.tan(math.radians(V['fov']) / 2); th = tv * 16 / 9
    for nx, ny in ((0.30, -0.25), (0.45, -0.30), (0.20, -0.20), (0.5, -0.1)):
        d = (co.matrix_world.to_3x3() @ Vector((nx * th, ny * tv, -1.0))).normalized()
        hit, loc, nrm, idx, ob, mtx = scene.ray_cast(dg, co.location, d)
        if not ob:
            print('RAY miss', (nx, ny)); continue
        print('RAY', (nx, ny), hit, ob.name if ob else None, tuple(round(v, 1) for v in loc), [m.name for m in ob.data.materials] if ob else None,
              'loc', tuple(round(v, 1) for v in ob.location), 'dim', tuple(round(v, 2) for v in ob.dimensions), 'rotz', round(math.degrees(ob.rotation_euler.z), 1), 'scale', tuple(ob.scale))
    pt = Vector((9e3, 9e3, 0.1))
    for dirv in ((0, 0, 1), (0.3, 0, 1), (-0.3, 0, 1), (0, 0.3, 1), (0, -0.3, 1), (0.7, 0.7, 0.5), (-0.7, -0.7, 0.5)):
        hit, loc, nrm, idx, ob, mtx = scene.ray_cast(dg, pt, Vector(dirv).normalized())
        print('UPRAY', dirv, hit, ob.name if ob else None, tuple(round(v, 1) for v in loc), (tuple(round(v, 1) for v in ob.dimensions) if ob else None))
    for ob in bpy.data.objects:
        if ob.name.startswith('rb'):
            lp = ob.matrix_world.inverted() @ Vector((-21.4, 40.0, 0.0))
            if abs(lp.x) <= ob.dimensions.x / 2 and abs(lp.y) <= ob.dimensions.y / 2:
                pass #print('COVER', ob.name, 'dim', tuple(round(v, 2) for v in ob.dimensions), 'z', round(ob.location.z, 4), 'mat', ob.data.materials[0].name)
    for xx in ():
        hit, loc, nrm, idx, ob, mtx = scene.ray_cast(dg, Vector((xx, 40.0, 50.0)), Vector((0, 0, -1)))
        print('DOWNRAY', xx, ob.name if ob else None, tuple(round(v, 3) for v in loc), [m.name for m in ob.data.materials] if ob else None, 'n', tuple(round(v, 2) for v in nrm))
    raise SystemExit
bpy.ops.render.render(write_still=True)
print('RENDER_DONE', OUT)
