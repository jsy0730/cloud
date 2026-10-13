import json, os, sys, urllib.request
UA = {'User-Agent': 'jeongdonggwan-study/1.0'}
OUT = os.path.join(os.environ['TEMP'], 'bl', 'ph')
os.makedirs(OUT, exist_ok=True)

def get(u):
    return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60))

def dl(u, p):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    if os.path.exists(p): return os.path.getsize(p)
    open(p, 'wb').write(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=180).read())
    return os.path.getsize(p)

total = 0
# HDRIs (2k hdr)
for a in ('kloofendal_48d_partly_cloudy_puresky', 'satara_night_no_lamps', 'belfast_sunset_puresky'):
    f = get(f'https://api.polyhaven.com/files/{a}')
    u = f['hdri']['2k']['hdr']['url']
    n = dl(u, os.path.join(OUT, 'hdri', a + '_2k.hdr')); total += n; print('hdri', a, n // 1024, 'KB')
# PBR textures (1k jpg: diffuse, normal gl, roughness)
for a in ('red_brick_03', 'concrete_wall_003', 'asphalt_02', 'concrete_floor_worn_001'):
    f = get(f'https://api.polyhaven.com/files/{a}')
    for m in ('Diffuse', 'nor_gl', 'Rough'):
        if m in f:
            u = f[m]['1k']['jpg']['url']
            n = dl(u, os.path.join(OUT, 'tex', a, f'{a}_{m}_1k.jpg')); total += n
    print('tex', a)
# tree models (blend + included textures, 1k)
for a in ('tree_small_02', 'jacaranda_tree'):
    f = get(f'https://api.polyhaven.com/files/{a}')
    b = f['blend']['1k']['blend']
    base = os.path.join(OUT, 'models', a)
    n = dl(b['url'], os.path.join(base, a + '_1k.blend')); total += n
    for rel, meta in b.get('include', {}).items():
        total += dl(meta['url'], os.path.join(base, rel))
    print('model', a)
print('total MB', round(total / 1e6, 1))
