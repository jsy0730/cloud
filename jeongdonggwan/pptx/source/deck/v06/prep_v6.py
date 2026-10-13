# v6: derive every render-based image from the new Blender renders (f3_*.png): real timber slats, black asphalt, sidewalk, trees
import os, json, glob
from PIL import Image, ImageDraw, ImageEnhance, ImageOps

T = os.environ['TEMP'].replace(chr(92), '/')
W = T + '/work/'
S = T + '/bl/out/'
DPI = 300


def px(i): return round(i * DPI)


def load(n): return Image.open(S + n).convert('RGB')


def cover(im, w, h, fx=0.5, fy=0.5):
    r = max(w / im.width, h / im.height)
    nw, nh = round(im.width * r), round(im.height * r)
    im = im.resize((nw, nh), Image.LANCZOS)
    x = round((nw - w) * fx); y = round((nh - h) * fy)
    return im.crop((x, y, x + w, y + h))


def save(im, name, q=90):
    im.save(W + 'img2/' + name, quality=q); print(name, im.size)


hero = load('f3_hero_sw.png'); night = load('f3_night_sw.png'); street = load('f3_street_nw.png')
roof = load('f3_roof_view.png'); lane = load('f3_lane_entry.png'); aerial = load('f3_aerial.png')
stair = load('f3_stair_close.png'); sunken = load('f3_sunken.png')

# 16:10 big image for the render slides (top 80 % of the hero keeps sky + building)
h = hero.crop((0, 0, hero.width, round(hero.height * 0.80)))
save(cover(h, px(7.65), px(4.9), 0.42, 0.0), 'r_big_hero.jpg')
save(cover(roof, px(7.65), px(4.9), 0.5, 0.5), 'r_big_roof.jpg')
save(cover(night, px(4.55), px(2.4), 0.5, 0.5), 'r_small_night.jpg')
save(cover(street, px(4.55), px(2.4), 0.5, 0.5), 'r_small_street.jpg')
save(cover(stair, px(4.55), px(2.4), 0.5, 0.5), 'r_small_sunken.jpg')     # detailed stair view replaces the old 'sunken' crop
save(cover(lane, px(4.55), px(2.4), 0.5, 0.5), 'r_small_lane.jpg')

# cover (diagonal left edge), contents art, concept pair
hw, hh = px(7.9), px(7.5)
c = cover(hero, hw, hh, 0.50, 0.5).convert('RGBA')
mask = Image.new('L', (hw, hh), 0)
ImageDraw.Draw(mask).polygon([(round(hw * 0.30), 0), (hw, 0), (hw, hh), (0, hh)], fill=255)
c.putalpha(mask); c.save(W + 'img2/cover_hero.png'); print('cover_hero', c.size)
save(cover(night, px(4.5), px(7.5), 0.58, 0.5), 'contents_art.jpg')
save(cover(hero, px(4.7), px(7.5), 0.60, 0.5), 'concept_day.jpg')
save(cover(night, px(4.7), px(7.5), 0.60, 0.5), 'concept_night.jpg')

# aerial crop around the building and the 'roof view' tile used on the 조망 page
a = aerial
save(a.crop((345, 115, 1560, 965)), 'final_aerial_crop.jpg')
drone = load('f3_drone_a.png')
save(drone.resize((1900, round(drone.height * 1900 / drone.width)), Image.LANCZOS), 'final_drone.jpg', 88)
save(cover(roof, px(3.3), px(1.9), 0.5, 0.5), 'view_roof.jpg')


# alternatives (외피 대안 · 형태 대안) re-rendered with the same street / stair upgrades
for n, srcf, fx in (('saintluc', 'alt4_saintluc.png', 0.55), ('lincoln', 'alt4_lincoln.png', 0.55), ('blaibach', 'alt4_blaibach.png', 0.55),
                    ('A', 'form4_A_aerial.png', 0.45), ('B', 'form4_B_aerial.png', 0.45), ('C', 'form4_C_aerial.png', 0.45)):
    if os.path.exists(S + srcf):
        nm = f'alt_{n}.jpg' if n in ('saintluc', 'lincoln', 'blaibach') else f'form_{n}.jpg'
        save(cover(load(srcf), px(3.7), px(2.1), fx, 0.5), nm)
    else:
        print('missing', srcf)

dims = {}
for folder in ('img', 'img2'):
    for f in glob.glob(W + folder + '/*'):
        if f.lower().endswith(('.jpg', '.jpeg', '.png')):
            try: dims[os.path.basename(f)] = list(Image.open(f).size)
            except Exception as e: print('skip', f, e)
json.dump(dims, open(W + 'dims.json', 'w', encoding='utf8'), ensure_ascii=False)
print('dims', len(dims))
