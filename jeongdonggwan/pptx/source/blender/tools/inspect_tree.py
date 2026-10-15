import bpy, os
PH = os.environ['JD_PH']
for tid in ('tree_small_02', 'jacaranda_tree'):
    p = os.path.join(PH, 'models', tid, f'{tid}_1k.blend')
    with bpy.data.libraries.load(p, link=False) as (src, dst):
        dst.objects = list(src.objects)
    tot = 0
    for o in dst.objects:
        if o is None: continue
        n = len(o.data.polygons) if o.type == 'MESH' else 0
        tot += n
        print(tid, o.name, o.type, 'polys', n, 'mods', [m.type for m in o.modifiers], 'dims', tuple(round(v,1) for v in o.dimensions))
    print(tid, 'TOTAL polys', tot)
