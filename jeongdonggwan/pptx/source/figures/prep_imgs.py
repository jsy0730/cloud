import os, json, glob
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageEnhance
T = os.environ['TEMP'].replace(chr(92), '/')
W = T + '/work/'
R = T + '/cloud_repo/jeongdonggwan/build/'
os.makedirs(W + 'img2', exist_ok=True)
FONT = ImageFont.truetype(W + 'fonts/Pretendard-Bold.ttf', 30)
FONTR = ImageFont.truetype(W + 'fonts/Pretendard-Regular.ttf', 26)

def load(p): return Image.open(p).convert('RGB')

def cover(im, w, h, fx=0.5, fy=0.5):
    r = max(w / im.width, h / im.height)
    nw, nh = round(im.width * r), round(im.height * r)
    im = im.resize((nw, nh), Image.LANCZOS)
    x = round((nw - w) * fx); y = round((nh - h) * fy)
    return im.crop((x, y, x + w, y + h))

def contain(im, w, h, bg=(255, 255, 255)):
    r = min(w / im.width, h / im.height)
    nw, nh = max(1, round(im.width * r)), max(1, round(im.height * r))
    im = im.resize((nw, nh), Image.LANCZOS)
    c = Image.new('RGB', (w, h), bg); c.paste(im, ((w - nw) // 2, (h - nh) // 2)); return c

def save(im, name, q=88):
    im.save(W + 'img2/' + name, quality=q); print(name, im.size)

DPI = 300
def px(inch): return round(inch * DPI)

# ---- photo tiles for case columns (2.5 x 2.5 in)
P = W + 'web/'
def tile(src, name, fx=0.5, fy=0.5, w=1.85, h=2.5):
    save(cover(load(src), px(w), px(h), fx, fy), name)
tile(P + 'big/herma_10_stringio.jpg', 'c_herma.jpg', 0.42, 0.5)
tile(P + 'ph2/saintluc_05.jpg', 'c_saintluc.jpg', 0.62, 0.5)
tile(P + 'ph2/pnpthumb_03.jpg', 'c_pnp.jpg', 0.55, 0.5)
tile(P + 'ph2/blaibach_00.jpg', 'c_blaibach.jpg', 0.55, 0.5)
tile(R + 'assets/lincoln.jpg', 'c_lincoln.jpg', 0.5, 0.5)

# ---- composite drawing tiles (3.55 x 2.5 in)
CW, CH = px(3.55), px(2.5)
def label(d, x, y, t):
    tw = d.textlength(t, font=FONT)
    d.rectangle((x, y, x + tw + 22, y + 44), fill=(0, 32, 96))
    d.text((x + 11, y + 6), t, font=FONT, fill=(255, 255, 255))

def comp(items, name, bg=(255, 255, 255)):
    c = Image.new('RGB', (CW, CH), bg); d = ImageDraw.Draw(c)
    for (src, rect, lab, mode) in items:
        x, y, w, h = [round(v * CW) if i % 2 == 0 else round(v * CH) for i, v in enumerate(rect)]
        im = load(src)
        if mode == 'cover': t = cover(im, w, h)
        else: t = contain(im, w, h)
        c.paste(t, (x, y))
        if lab: label(d, x + 6, y + 6, lab)
    # hairline frame
    d.rectangle((0, 0, CW - 1, CH - 1), outline=(160, 162, 165), width=2)
    save(c, name)

C = W + 'cases/'
comp([(C + 'herma_plan1.jpg', (0.0, 0.0, 1.0, 0.60), '1층 평면', 'contain'), (C + 'herma_elev.jpg', (0.0, 0.62, 1.0, 0.38), '입면', 'contain')], 'd_herma.jpg')
comp([(C + 'saintluc_section.jpg', (0.0, 0.0, 1.0, 0.56), '단면', 'contain'), (C + 'saintluc_floor0.jpg', (0.0, 0.58, 0.5, 0.42), '지상 평면', 'contain'),
      (C + 'saintluc_floormin3.jpg', (0.5, 0.58, 0.5, 0.42), '지하 3층 평면', 'contain')], 'd_saintluc.jpg')
comp([(C + 'pnp_roof.jpg', (0.0, 0.0, 0.5, 0.56), '옥상 평면', 'contain'), (C + 'pnp_typ.jpg', (0.5, 0.0, 0.5, 0.56), '주차층 평면', 'contain'),
      (C + 'pnp_elev_a.jpg', (0.0, 0.58, 1.0, 0.42), '입면', 'contain')], 'd_pnp.jpg')
# blaibach: crop section to the building
sec = load(C + 'blaibach_section.jpg'); sec = sec.crop((int(sec.width * 0.30), 0, int(sec.width * 0.86), sec.height)); sec.save(W + 'img2/_bsec.jpg')
comp([(W + 'assets/blaibach_floor.jpg', (0.0, 0.0, 0.34, 1.0), '평면', 'contain'), (W + 'img2/_bsec.jpg', (0.35, 0.0, 0.65, 0.5), '단면', 'contain'),
      (P + 'ph2/blaibach_20.jpg', (0.35, 0.51, 0.65, 0.49), None, 'cover')], 'd_blaibach.jpg')
comp([(W + 'img/diag_lincoln.png', (0.0, 0.0, 0.68, 1.0), None, 'contain'), (P + 'big/lincoln_05_stringio.jpg', (0.69, 0.0, 0.31, 0.5), None, 'cover'),
      (P + 'big/lincoln_04_stringio.jpg', (0.69, 0.51, 0.31, 0.49), None, 'cover')], 'd_lincoln.jpg')

# ---- cover hero with diagonal left edge (RGBA) 7.9 x 7.5 in
hw, hh = px(7.9), px(7.5)
hero = cover(load(W + 'img/hero_sw.jpg'), hw, hh, 0.35, 0.5).convert('RGBA')
mask = Image.new('L', (hw, hh), 0); md = ImageDraw.Draw(mask)
top = round(hw * 0.30); bot = 0
md.polygon([(top, 0), (hw, 0), (hw, hh), (bot, hh)], fill=255)
hero.putalpha(mask); hero.save(W + 'img2/cover_hero.png'); print('cover_hero', hero.size)

# ---- contents art (4.7 x 7.5 in) navy-soft ground + night render
save(cover(load(W + 'img/night_sw.jpg'), px(4.5), px(7.5), 0.58, 0.5), 'contents_art.jpg')
# ---- concept grey photo (6.3 x 7.5)
g = ImageOps.grayscale(cover(load(W + 'img/night_sw.jpg'), px(4.7), px(7.5), 0.6, 0.5)).convert('RGB')
g = ImageEnhance.Contrast(g).enhance(1.08); save(g, 'concept_grey.jpg')
# ---- render grid cells (6.1 x 2.66)
for n, f, fx, fy in (('r_hero', 'hero_sw', 0.5, 0.55), ('r_night', 'night_sw', 0.5, 0.55), ('r_roof', 'roof_view', 0.5, 0.55), ('r_sunken', 'sunken', 0.5, 0.5)):
    save(cover(load(W + f'img/{f}.jpg'), px(6.1), px(2.66), fx, fy), n + '.jpg')
# ---- misc covers
save(cover(load(W + 'img/aerial.jpg'), px(6.4), px(3.6), 0.5, 0.5), 'final_aerial.jpg')
save(cover(load(W + 'img/jeonpo_view.jpg'), px(4.1), px(1.9), 0.5, 0.45), 'view_jeonpo.jpg')
save(cover(load(W + 'img/roof_view.jpg'), px(3.3), px(1.9), 0.5, 0.5), 'view_roof.jpg')
for n, f in (('n_p1', 'photo_parking1.jpg'), ('n_p2', 'photo_parking2.jpg')):
    save(cover(load(W + 'img/' + f), px(1.5), px(1.3), 0.5, 0.55), n + '.jpg')
save(cover(load(W + 'img/jeonpo_street.jpg'), px(1.5), px(1.3), 0.5, 0.5), 'n_p3.jpg')
dims = {os.path.basename(f): Image.open(f).size for f in glob.glob(W + 'img2/*') + glob.glob(W + 'img/*') if f.lower().endswith(('.jpg', '.png'))}
json.dump(dims, open(W + 'dims.json', 'w'))

for n, f in (('p_alley1', 'photo_parking1.jpg'), ('p_alley2', 'photo_parking2.jpg')):
    save(cover(load(W + 'img/' + f), px(2.44), px(2.05), 0.5, 0.58), n + '.jpg')
dims = {os.path.basename(f): Image.open(f).size for f in glob.glob(W + 'img2/*') + glob.glob(W + 'img/*') if f.lower().endswith(('.jpg', '.png'))}
json.dump(dims, open(W + 'dims.json', 'w'))

# --- render slides (2 x 3-up layouts): big 7.65x4.9 + two 4.55x2.4
def rc(src, name, w, h, fx=0.5, fy=0.5): save(cover(load(W + 'img/' + src), px(w), px(h), fx, fy), name)
_h = load(W + 'img/hero_sw.jpg'); _h = _h.crop((0, 0, _h.width, round(_h.height * 0.80)))
save(cover(_h, px(7.65), px(4.9), 0.42, 0.0), 'r_big_hero.jpg')
rc('night_sw.jpg', 'r_small_night.jpg', 4.55, 2.4, 0.5, 0.5)
rc('street_nw.jpg', 'r_small_street.jpg', 4.55, 2.4, 0.5, 0.5)
rc('roof_view.jpg', 'r_big_roof.jpg', 7.65, 4.9, 0.5, 0.5)
rc('sunken.jpg', 'r_small_sunken.jpg', 4.55, 2.4, 0.5, 0.45)
rc('lane_entry.jpg', 'r_small_lane.jpg', 4.55, 2.4, 0.5, 0.5)
dims = {os.path.basename(f): Image.open(f).size for f in glob.glob(W + 'img2/*') + glob.glob(W + 'img/*') if f.lower().endswith(('.jpg', '.png'))}
json.dump(dims, open(W + 'dims.json', 'w'))

# --- alternatives slide tiles (3.7 x 2.1)
ALT = os.environ['TEMP'].replace(chr(92), '/') + '/bl/out/'
for n in ('saintluc', 'lincoln', 'blaibach'):
    f = ALT + f'alt_{n}.png'
    if os.path.exists(f):
        save(cover(load(f), px(3.7), px(2.1), 0.55, 0.5), f'alt_{n}.jpg')
dims = {os.path.basename(f): Image.open(f).size for f in glob.glob(W + 'img2/*') + glob.glob(W + 'img/*') if f.lower().endswith(('.jpg', '.png'))}
json.dump(dims, open(W + 'dims.json', 'w'))

FRM = os.environ['TEMP'].replace(chr(92), '/') + '/bl/out/'
for k in 'ABC':
    f = FRM + f'form_{k}_aerial.png'
    if os.path.exists(f):
        save(cover(load(f), px(3.7), px(2.1), 0.45, 0.5), f'form_{k}.jpg')
dims = {os.path.basename(f): Image.open(f).size for f in glob.glob(W + 'img2/*') + glob.glob(W + 'img/*') if f.lower().endswith(('.jpg', '.png'))}
json.dump(dims, open(W + 'dims.json', 'w'))
