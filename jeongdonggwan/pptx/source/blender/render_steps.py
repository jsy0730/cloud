# volume-derivation diagrams: five axonometric steps from the repo's step{i}.json massing models
# blender -b --python render_steps.py -- <jsondir> <outdir> <w> <h> <azimuth_deg> <elevation_deg> <ortho_height_m>
import bpy, bmesh, json, math, sys, os
from mathutils import Vector

argv = sys.argv[sys.argv.index('--') + 1:]
src, outdir = argv[0], argv[1]
W, H = int(argv[2]), int(argv[3])
az, el = math.radians(float(argv[4])), math.radians(float(argv[5]))
ORTHO = float(argv[6])
MODE = argv[7] if len(argv) > 7 else 'studio'
ONLY = int(argv[8]) if len(argv) > 8 else 0
PAL = dict(dW='f6e58d', dE='f2c79a', dlane='8f8f8f', dsite='e6e2da', dpark='d7b28c', dpark2='c49a72',
           dcult='8fb8e0', doff='cdb8e6', dcore='d2432a', droof='9ccc7c')
os.makedirs(outdir, exist_ok=True)


def rgb(h):
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def srgb2lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


for i in range(1, 6):
    if ONLY and i != ONLY:
        continue
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    d = json.load(open(f'{src}/step{i}.json'))
    allp = []
    for k, p in enumerate(d['parts']):
        me = bpy.data.meshes.new(f'm{k}')
        ob = bpy.data.objects.new(f'o{k}', me)
        sc.collection.objects.link(ob)
        bm = bmesh.new()
        vs = [bm.verts.new((x, y, p['z0'])) for x, y in p['pts']]
        f = bm.faces.new(vs)
        r = bmesh.ops.extrude_face_region(bm, geom=[f])
        top = [v for v in r['geom'] if isinstance(v, bmesh.types.BMVert)]
        bmesh.ops.translate(bm, vec=(0, 0, p['h']), verts=top)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
        bm.to_mesh(me)
        bm.free()
        c = rgb(PAL[p['mat']])
        ob.color = (tuple(srgb2lin(v) for v in c) if MODE.endswith('lin') else c) + (1,)
        allp += [Vector((x, y, p['z0'])) for x, y in p['pts']]
    # fixed frame for all five steps so they line up: centre of the full site
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
    direction = target - co.location
    co.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    sc.camera = co
    sc.render.engine = 'BLENDER_WORKBENCH'
    sc.render.resolution_x, sc.render.resolution_y = W, H
    sc.render.film_transparent = False
    sh = sc.display.shading
    sh.light = {'studio': 'STUDIO', 'flat': 'FLAT', 'matcap': 'MATCAP'}.get(MODE.split('_')[0], 'STUDIO')
    sh.color_type = 'OBJECT'
    sh.show_object_outline = True
    sh.object_outline_color = (0.18, 0.18, 0.2)
    sh.show_shadows = True
    sh.shadow_intensity = 0.35
    sh.show_cavity = False
    sc.display.render_aa = '16'
    sc.display.shading.background_type = 'THEME' if False else 'WORLD'
    w = bpy.data.worlds.new('w')
    w.color = (1, 1, 1)
    sc.world = w
    sc.view_settings.view_transform = 'Standard'
    sc.render.image_settings.file_format = 'PNG'
    sc.render.filepath = os.path.join(outdir, f'step{i}_{MODE}.png' if ONLY else f'step{i}.png')
    bpy.ops.render.render(write_still=True)
    print('step', i, 'done')
