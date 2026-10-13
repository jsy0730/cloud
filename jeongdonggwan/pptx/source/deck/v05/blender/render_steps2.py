# volume-derivation diagrams (Cycles, soft sun + sky, Freestyle outlines) from the repo's step{i}.json massing models
# blender -b --python render_steps2.py -- <jsondir> <outdir> <w> <h> <azimuth_deg> <elevation_deg> <ortho_height_m> [only]
import bpy, json, math, sys, os
from mathutils import Vector, geometry

argv = sys.argv[sys.argv.index('--') + 1:]
src, outdir = argv[0], argv[1]
W, H = int(argv[2]), int(argv[3])
az, el = math.radians(float(argv[4])), math.radians(float(argv[5]))
ORTHO = float(argv[6])
ONLY = int(argv[7]) if len(argv) > 7 else 0
PAL = dict(dW='f6e58d', dE='f2c79a', dlane='8f8f8f', dsite='e6e2da', dpark='d7b28c', dpark2='c49a72',
           dcult='8fb8e0', doff='cdb8e6', dcore='d2432a', droof='9ccc7c')
os.makedirs(outdir, exist_ok=True)


def lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def rgb(h):
    return tuple(lin(int(h[i:i + 2], 16) / 255) for i in (0, 2, 4))


for i in range(1, 6):
    if ONLY and i != ONLY:
        continue
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    d = json.load(open(f'{src}/step{i}.json'))
    mats = {}
    for k, p in enumerate(d['parts']):
        me = bpy.data.meshes.new(f'm{k}')
        ob = bpy.data.objects.new(f'o{k}', me)
        sc.collection.objects.link(ob)
        pts = [tuple(q) for q in p['pts']]
        ar = sum(pts[u][0] * pts[(u + 1) % len(pts)][1] - pts[(u + 1) % len(pts)][0] * pts[u][1] for u in range(len(pts)))
        if ar < 0:
            pts = pts[::-1]
        n = len(pts)
        z0, z1 = p['z0'], p['z0'] + p['h']
        verts = [(x, y, z0) for x, y in pts] + [(x, y, z1) for x, y in pts]
        faces = []
        tris = geometry.tessellate_polygon([[Vector((x, y, 0.0)) for x, y in pts]])
        for t in tris:
            a_, b_, c_ = t
            sa = (pts[b_][0] - pts[a_][0]) * (pts[c_][1] - pts[a_][1]) - (pts[c_][0] - pts[a_][0]) * (pts[b_][1] - pts[a_][1])
            if sa < 0:
                b_, c_ = c_, b_
            faces.append((n + a_, n + b_, n + c_))      # top, counter-clockwise (normal +z)
            faces.append((c_, b_, a_))                  # bottom, normal -z
        for q in range(n):
            j = (q + 1) % n
            faces.append((q, j, n + j, n + q))
        me.from_pydata(verts, [], faces)
        me.update()
        m = mats.get(p['mat'])
        if m is None:
            m = bpy.data.materials.new(p['mat'])
            m.use_nodes = True
            bsdf = m.node_tree.nodes['Principled BSDF']
            bsdf.inputs['Base Color'].default_value = rgb(PAL[p['mat']]) + (1,)
            bsdf.inputs['Roughness'].default_value = 1.0
            mats[p['mat']] = m
        me.materials.append(m)
    target = Vector((21.0, 62.0, 8.0))
    dist = 400.0
    cam = bpy.data.cameras.new('cam')
    cam.type = 'ORTHO'
    cam.ortho_scale = ORTHO
    cam.sensor_fit = 'VERTICAL'
    cam.clip_start, cam.clip_end = 1, 2000
    co = bpy.data.objects.new('cam', cam)
    sc.collection.objects.link(co)
    co.location = target + Vector((math.sin(az) * math.cos(el), math.cos(az) * math.cos(el), math.sin(el))) * dist
    co.rotation_euler = (target - co.location).to_track_quat('-Z', 'Y').to_euler()
    sc.camera = co
    # sun from the south-west, a little above the camera side
    sun = bpy.data.lights.new('sun', 'SUN')
    sun.energy = 2.7
    sun.angle = math.radians(4)
    so = bpy.data.objects.new('sun', sun)
    sc.collection.objects.link(so)
    saz, sel = math.radians(235.0), math.radians(46.0)
    so.rotation_euler = (Vector((-math.sin(saz) * math.cos(sel), -math.cos(saz) * math.cos(sel), -math.sin(sel)))).to_track_quat('-Z', 'Y').to_euler()
    w = bpy.data.worlds.new('w')
    w.use_nodes = True
    bg = w.node_tree.nodes['Background']
    bg.inputs['Color'].default_value = (1, 1, 1, 1)
    bg.inputs['Strength'].default_value = 0.62
    sc.world = w
    sc.render.engine = 'CYCLES'
    sc.cycles.samples = 48
    sc.cycles.use_denoising = True
    sc.cycles.device = 'CPU'
    sc.render.resolution_x, sc.render.resolution_y = W, H
    sc.render.film_transparent = True
    sc.view_settings.view_transform = 'Standard'
    sc.render.image_settings.file_format = 'PNG'
    sc.render.image_settings.color_mode = 'RGBA'
    # outlines
    sc.render.use_freestyle = True
    vl = sc.view_layers[0]
    vl.use_freestyle = True
    fs = vl.freestyle_settings
    ls = fs.linesets.new('outline') if len(fs.linesets) == 0 else fs.linesets[0]
    ls.select_by_visibility = True
    ls.select_by_edge_types = True
    ls.select_silhouette = True
    ls.select_border = True
    ls.select_crease = True
    ls.select_by_face_marks = False
    st = ls.linestyle or bpy.data.linestyles.new('ls')
    ls.linestyle = st
    st.color = (0.16, 0.17, 0.2)
    st.thickness = 1.6 * (W / 700.0)
    sc.render.line_thickness_mode = 'ABSOLUTE'
    sc.render.line_thickness = 1.0
    sc.render.filepath = os.path.join(outdir, f'step{i}_cy.png')
    bpy.ops.render.render(write_still=True)
    print('step', i, 'done')
