import sys
from PIL import Image, ImageDraw
def grid(path, out, step=50, scale=1.0, box=None):
    im = Image.open(path).convert('RGB')
    if box: im = im.crop(box)
    x0, y0 = (box[0], box[1]) if box else (0, 0)
    if scale != 1.0: im = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)
    d = ImageDraw.Draw(im)
    W, H = im.size
    gx = (x0 // step + 1) * step
    while (gx - x0) * scale < W:
        X = (gx - x0) * scale; major = gx % (step * 2) == 0
        d.line([(X, 0), (X, H)], fill=(255, 0, 0) if major else (255, 190, 190), width=1)
        if major: d.text((X + 2, 2), str(gx), fill=(255, 0, 0))
        gx += step
    gy = (y0 // step + 1) * step
    while (gy - y0) * scale < H:
        Y = (gy - y0) * scale; major = gy % (step * 2) == 0
        d.line([(0, Y), (W, Y)], fill=(0, 0, 255) if major else (190, 190, 255), width=1)
        if major: d.text((2, Y + 2), str(gy), fill=(0, 0, 255))
        gy += step
    im.save(out); print(out, im.size)
if __name__ == '__main__':
    p, o, step, sc = sys.argv[1], sys.argv[2], int(sys.argv[3]), float(sys.argv[4])
    box = tuple(int(v) for v in sys.argv[5].split(',')) if len(sys.argv) > 5 else None
    grid(p, o, step, sc, box)
