import os
import numpy as np
from PIL import Image
R = os.environ['TEMP'].replace(chr(92), '/') + '/cloud_repo/jeongdonggwan/build/'
W = os.environ['TEMP'].replace(chr(92), '/') + '/work/img/'


def recolor(src, dst, maxw):
    im = Image.open(src).convert('RGB')
    a = np.asarray(im).astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    # saturated red (stair zig-zags, red labels): R high, G/B low  -> near black
    mask = (r > 140) & (g < 100) & (b < 100) & (r - g > 80)
    a[mask] = (28, 28, 30)
    out = Image.fromarray(a.astype('uint8'))
    if out.width > maxw:
        out = out.resize((maxw, round(out.height * maxw / out.width)), Image.LANCZOS)
    out.save(dst, quality=90)
    print(dst, out.size, int(mask.sum()))


recolor(R + 'section/secA_new.png', W + 'secA.jpg', 1900)
recolor(R + 'section/secB_new.png', W + 'secB.jpg', 900)
