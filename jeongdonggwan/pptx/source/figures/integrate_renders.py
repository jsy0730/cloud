import os, shutil, json, glob
from PIL import Image
T = os.environ['TEMP'].replace(chr(92), '/')
S = T + '/bl/out/'
W = T + '/work/img/'
m = {'hero_sw': 'hero_sw.jpg', 'night_sw': 'night_sw.jpg', 'street_nw': 'street_nw.jpg', 'roof_view': 'roof_view.jpg',
     'sunken': 'sunken.jpg', 'lane_entry': 'lane_entry.jpg', 'aerial': 'aerial.jpg'}
for k, v in m.items():
    src = S + f'f_{k}.png'
    if not os.path.exists(src):
        print('missing', k); continue
    im = Image.open(src).convert('RGB')
    if im.width > 1700: im = im.resize((1700, round(im.height * 1700 / im.width)), Image.LANCZOS)
    im.save(W + v, quality=90); print(v, im.size, os.path.getsize(W + v) // 1024, 'KB')
