# -*- coding: utf-8 -*-
# build_scene3.py = build_scene.py + (real timber slats, open-deck interior, detailed stairs, black asphalt, sidewalk, street trees)
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
s = open('build_scene.py', encoding='utf8').read()


def rep(a, b, count=1):
    global s
    assert s.count(a) == count, (s.count(a), a[:70])
    s = s.replace(a, b)


# ---- 1. helper block (inserted before the material section)
HELP = r'''
# ================================================================== v3 additions
SLATS = os.environ.get('JD_SLATS', '1') == '1' and not VARIANT
SLAT_W, SLAT_P, SLAT_T = 0.32, 0.52, 0.12      # width, pitch, thickness (m)
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
    print('interior cars', ncar)

'''
rep("# ------------------------------------------------------------------ materials\n", HELP + "\n# ------------------------------------------------------------------ materials\n")

# ---- 2. materials: black asphalt, light sidewalk, wood tones
rep("M['asphalt'] = tex_mat('asphalt', 'asphalt_02', scale=4.0, nstr=0.8, tint=(1.5, 1.5, 1.5, 1))",
    "M['asphalt'] = tex_mat('asphalt', 'asphalt_02', scale=4.0, nstr=0.6, tint=(0.30, 0.30, 0.32, 1)) if SLATS else tex_mat('asphalt', 'asphalt_02', scale=4.0, nstr=0.8, tint=(1.5, 1.5, 1.5, 1))")
rep("M['paving'] = tex_mat('paving', 'concrete_floor_worn_001', scale=3.0, nstr=0.5, tint=(0.95, 0.93, 0.9, 1))",
    "M['paving'] = tex_mat('paving', 'concrete_floor_worn_001', scale=3.0, nstr=0.5, tint=(0.95, 0.93, 0.9, 1))\n"
    "M['sidewalk'] = tex_mat('sidewalk', 'concrete_floor_worn_001', scale=1.4, nstr=0.5, tint=(1.9, 1.85, 1.78, 1))\n"
    "M['tread'] = simple_mat('tread', (0.035, 0.035, 0.04), rough=0.5, metal=0.35)\n"
    "M['nose'] = simple_mat('nose', (0.32, 0.32, 0.34), rough=0.55)\n"
    "if SLATS:\n"
    "    M['wood'] = [wood_board_mat('wood0', (2.1, 1.45, 1.0)), wood_board_mat('wood1', (1.7, 1.15, 0.8)), wood_board_mat('wood2', (2.5, 1.75, 1.2))]")

# ---- 3. building loop: slats replace the masked screen prisms
rep("""    if m in ('screen', 'base'):
        prism('screen', p['pts'], p['z0'], p['h'], screen_for(p))
        if p.get('inner'):
            o = prism('inner', p['inner'], p['z0'], p['h'], M['inner'])""",
    """    if m in ('screen', 'base') and SLATS:
        SLAT_PARTS.append(p)
    elif m in ('screen', 'base'):
        prism('screen', p['pts'], p['z0'], p['h'], screen_for(p))
        if p.get('inner'):
            o = prism('inner', p['inner'], p['z0'], p['h'], M['inner'])""")
rep("# ------------------------------------------------------------------ the building\n",
    "# ------------------------------------------------------------------ the building\nSLAT_PARTS = []\n")
rep("# ------------------------------------------------------------------ design variants (extra modeling)\n",
    "if SLAT_PARTS:\n    build_slats(SLAT_PARTS, M['wood'])\n    build_interior(SLAT_PARTS)\n\n# ------------------------------------------------------------------ design variants (extra modeling)\n")

# ---- 4. detailed stairs
a = s.index("for sf in D.get('stairs', []):")
b = s.index("for sh in D.get('shafts', []):")
STAIRS = r'''_st = bmesh.new(); _tr = bmesh.new(); _nz = bmesh.new()
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
'''
s = s[:a] + STAIRS + s[b:]

# ---- 5. sidewalk + curb in front of the building (west frontage) and street trees
SIDE = r'''
if SLATS:
    # raised sidewalk strip with a curb along the west frontage (the road keeps its black asphalt)
    SW_W, SW_H = 4.6, 0.16
    box('sidewalk', (SW_W, 127.4, SW_H), (-SW_W / 2, 63.7, SW_H / 2), (0, 0, 0), M['sidewalk'])
    box('curb', (0.22, 127.4, SW_H + 0.03), (-SW_W - 0.11, 63.7, (SW_H + 0.03) / 2), (0, 0, 0), M['concrete'])
    for yy_ in (14.0, 24.0, 66.0, 84.0, 104.0, 118.0):
        D.setdefault('trees', [])
        D['trees'].append([-2.3, yy_, SW_H, 1.15])
'''
rep("flat('plaza', D['block'][0], 0.03, M['paving'])\n", "flat('plaza', D['block'][0], 0.03, M['paving'])\n" + SIDE)
open('build_scene3.py', 'w', encoding='utf8').write(s)
print('build_scene3.py written', len(s))
