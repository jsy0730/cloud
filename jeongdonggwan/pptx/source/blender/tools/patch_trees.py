import os
p = os.path.join(os.environ['TEMP'], 'bl', 'build_scene.py')
s = open(p, encoding='utf8').read()
a = s.index("def append_tree(blend, collname=None):")
b = s.index("for lp in D.get('lamps', []):")
new = '''KEEP = {'tree_small_02': ('tree_small_02_trunk', 'tree_small_02_LOD1'),
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


if TREE_SRC:
    for i, t in enumerate(D.get('trees', [])):
        place_tree(t[0], t[1], t[2], t[3] if len(t) > 3 else 1.0, i)

'''
s = s[:a] + new + s[b:]
open(p, 'w', encoding='utf8').write(s)
print('ok')
