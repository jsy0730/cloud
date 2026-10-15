# annotated case-drawing tiles (공설기 v1.2 colours): gold = applied element, blue = active/public, pink = stair/core, green = ramp/green
import os, json, math
from PIL import Image, ImageDraw, ImageFont
T = os.environ['TEMP'].replace(chr(92), '/')
W = T + '/work/'
L3 = W + 'web/lincoln3/'
DPI = 300
TW, TH = round(4.15 * DPI), round(2.5 * DPI)
GOLD = (255, 192, 0); BLUE = (86, 130, 210); PINK = (236, 128, 128); GREEN = (112, 173, 71); RED = (192, 0, 0); NAVY = (0, 32, 96); GREY = (160, 162, 165)
FB = ImageFont.truetype(W + 'fonts/Pretendard-Bold.ttf', 30)
FB2 = ImageFont.truetype(W + 'fonts/Pretendard-Bold.ttf', 36)


def load(p):
    return Image.open(p).convert('RGB')


class Panel:
    """a drawing placed in a rectangle (contain), with annotations given in SOURCE pixel coords"""
    def __init__(self, path, crop=None, bg=(255, 255, 255)):
        im = load(path)
        self.off = (0, 0)
        if crop:
            im = im.crop(crop); self.off = (crop[0], crop[1])
        self.im = im
        self.ops = []

    def poly(self, pts, color, a=0.45, outline=True):
        self.ops.append(('poly', pts, color, a, outline)); return self

    def rect(self, x0, y0, x1, y1, color, a=0.45, outline=True):
        return self.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], color, a, outline)

    def line(self, pts, color, w=14, a=0.85):
        self.ops.append(('line', pts, color, w, a)); return self

    def badge(self, x, y, n):
        self.ops.append(('badge', (x, y), n)); return self

    def render(self, w, h, label=None):
        sc = min(w / self.im.width, h / self.im.height)
        nw, nh = round(self.im.width * sc), round(self.im.height * sc)
        base = self.im.resize((nw, nh), Image.LANCZOS).convert('RGBA')
        lay = Image.new('RGBA', base.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)

        def T_(pt):
            return ((pt[0] - self.off[0]) * sc, (pt[1] - self.off[1]) * sc)
        for op in self.ops:
            if op[0] == 'poly':
                _, pts, col, a, ol = op
                P = [T_(p) for p in pts]
                d.polygon(P, fill=(*col, int(255 * a)))
                if ol: d.line(P + [P[0]], fill=(*col, 255), width=3)
            elif op[0] == 'line':
                _, pts, col, wd, a = op
                d.line([T_(p) for p in pts], fill=(*col, int(255 * a)), width=max(3, round(wd * sc)), joint='curve')
        base = Image.alpha_composite(base, lay)
        d = ImageDraw.Draw(base)
        for op in self.ops:
            if op[0] == 'badge':
                x, y = T_(op[1]); r = 24
                d.ellipse((x - r, y - r, x + r, y + r), fill=NAVY, outline=(255, 255, 255), width=4)
                tw = d.textlength(str(op[2]), font=FB2)
                d.text((x - tw / 2, y - 22), str(op[2]), font=FB2, fill=(255, 255, 255))
        canvas = Image.new('RGB', (w, h), (255, 255, 255))
        ox, oy = (w - nw) // 2, (h - nh) // 2
        canvas.paste(base.convert('RGB'), (ox, oy))
        if label:
            d = ImageDraw.Draw(canvas); tw = d.textlength(label, font=FB)
            d.rectangle((6, 6, 6 + tw + 20, 6 + 44), fill=NAVY); d.text((16, 12), label, font=FB, fill=(255, 255, 255))
        return canvas


def tile(panels, name):
    """panels: [(Panel, (fx, fy, fw, fh), label)] fractions of the tile"""
    c = Image.new('RGB', (TW, TH), (255, 255, 255))
    for p, (fx, fy, fw, fh), lab in panels:
        x, y, w, h = round(fx * TW), round(fy * TH), round(fw * TW), round(fh * TH)
        c.paste(p.render(w, h, lab), (x, y))
    ImageDraw.Draw(c).rectangle((0, 0, TW - 1, TH - 1), outline=GREY, width=2)
    c.save(W + 'img2/' + name, quality=90); print(name, c.size)


C = W + 'cases/'
# ---------------- Herma
p1 = Panel(C + 'herma_plan1.jpg', crop=(95, 60, 900, 540))
p1.poly([(270, 352), (300, 310), (350, 262), (390, 247), (652, 247), (652, 302), (402, 312), (352, 326), (320, 356), (306, 402)], GREEN, 0.5)
p1.poly([(118, 262), (232, 357), (302, 405), (302, 455), (118, 455)], GOLD, 0.5)
p1.rect(500, 352, 662, 458, PINK, 0.5)
p1.badge(500, 232, 1).badge(190, 440, 2).badge(580, 340, 3)
p2 = Panel(C + 'herma_elev.jpg', crop=(95, 90, 1020, 420))
p2.poly([(125, 198), (300, 203), (422, 228), (402, 250), (300, 252), (125, 247)], GOLD, 0.55)
p2.poly([(410, 258), (520, 228), (700, 216), (1005, 232), (1005, 298), (700, 298), (500, 288), (430, 276)], GOLD, 0.55)
p2.poly([(680, 380), (780, 358), (1005, 352), (1005, 402), (780, 402)], GOLD, 0.55)
p2.rect(128, 336, 545, 402, BLUE, 0.4)
p2.badge(250, 172, 4).badge(560, 160, 4).badge(330, 322, 5)
tile([(p1, (0.0, 0.0, 1.0, 0.56), '1층 평면'), (p2, (0.0, 0.56, 1.0, 0.44), '입면')], 'd_herma.jpg')

# ---------------- Saint-Luc
s1 = Panel(C + 'saintluc_section.jpg', crop=(450, 380, 1800, 862))
s1.rect(500, 478, 1290, 506, GREEN, 0.7)
s1.rect(500, 506, 1312, 600, GOLD, 0.30)
s1.rect(500, 600, 1312, 800, BLUE, 0.28)
s1.poly([(1312, 592), (1560, 615), (1482, 676), (1425, 742), (1352, 792), (1314, 794)], GREEN, 0.55)
s1.badge(900, 440, 1).badge(900, 552, 2).badge(900, 700, 3).badge(1440, 640, 4)
s2 = Panel(C + 'saintluc_floor0.jpg', crop=(150, 200, 1800, 1480))
s2.poly([(267, 233), (417, 308), (427, 1200), (358, 1192), (275, 1150), (250, 1067)], GREEN, 0.5)
s2.line([(803, 318), (560, 326), (442, 345), (436, 520), (432, 900), (424, 1180), (400, 1196)], GOLD, 22, 0.9)
s2.badge(330, 700, 4).badge(640, 290, 5)
tile([(s1, (0.0, 0.0, 1.0, 0.5), '단면'), (s2, (0.0, 0.5, 1.0, 0.5), '지상 평면')], 'd_saintluc.jpg')

# ---------------- Park 'n' Play
r1 = Panel(C + 'pnp_roof.jpg', crop=(0, 40, 1800, 900))
r1.poly([(42, 67), (1500, 67), (1667, 617), (1667, 880), (42, 880)], GOLD, 0.28)
r1.rect(1367, 67, 1500, 208, PINK, 0.65)
r1.badge(760, 480, 1).badge(1433, 138, 2)
e1 = Panel(C + 'pnp_elev_a.jpg', crop=(0, 100, 1800, 800))
e1.line([(67, 758), (175, 600), (308, 592), (567, 442), (733, 392), (933, 342), (1067, 275), (1300, 192), (1385, 175)], PINK, 46, 0.8)
e1.rect(1100, 180, 1650, 660, GREEN, 0.14, outline=False)
e1.badge(700, 420, 2).badge(1450, 330, 3)
t1 = Panel(C + 'pnp_typ.jpg', crop=(0, 0, 1800, 900))
t1.rect(1150, 342, 1600, 767, GREEN, 0.35)
t1.poly([(1500, 100), (1560, 100), (1667, 467), (1610, 467)], PINK, 0.6)
t1.badge(1380, 560, 4)
tile([(r1, (0.0, 0.0, 0.52, 0.56), '옥상 평면'), (t1, (0.52, 0.0, 0.48, 0.56), '주차층 평면'), (e1, (0.0, 0.56, 1.0, 0.44), '입면')], 'd_pnp.jpg')

# ---------------- Blaibach
bf = Panel(W + 'assets/blaibach_floor.jpg', crop=(100, 80, 1000, 1260))
bf.rect(300, 745, 600, 925, BLUE, 0.4)
bf.rect(275, 1000, 625, 1200, GOLD, 0.5)
bf.poly([(200, 262), (740, 120), (880, 420), (560, 500), (200, 360)], GREEN, 0.4)
bf.badge(450, 835, 1).badge(450, 1100, 2).badge(480, 330, 3)
bs = Panel(C + 'blaibach_section.jpg', crop=(380, 0, 1250, 440))
bs.poly([(672, 31), (1142, 220), (1111, 354), (892, 354), (738, 354), (738, 331), (603, 218)], GOLD, 0.5)
bs.rect(423, 251, 654, 328, BLUE, 0.4)
bs.line([(562, 228), (643, 280), (723, 331)], PINK, 30, 0.8)
bs.badge(900, 190, 4).badge(520, 300, 5).badge(690, 305, 6)
ph = Panel(W + 'web/ph2/blaibach_20.jpg')
tile([(bf, (0.0, 0.0, 0.40, 1.0), '평면'), (bs, (0.40, 0.0, 0.60, 0.50), '단면'), (ph, (0.40, 0.5, 0.60, 0.5), None)], 'd_blaibach.jpg')

# ---------------- 1111 Lincoln Road (official drawings via ArchEyes: (c) Herzog & de Meuron)
ls = Panel(L3 + 'sec_ew.jpg', crop=(535, 455, 1100, 860))
ls.rect(553, 518, 1062, 578, GOLD, 0.45)
ls.rect(553, 606, 1062, 670, GOLD, 0.45)
ls.rect(553, 794, 1079, 842, BLUE, 0.45)
ls.rect(760, 478, 822, 800, PINK, 0.5)
ls.badge(620, 548, 1).badge(791, 640, 2).badge(960, 820, 3)
l2 = Panel(L3 + 'lv2.jpg', crop=(540, 560, 1100, 1050))
l2.rect(560, 590, 1020, 1010, GREEN, 0.2, outline=False)
l2.rect(690, 700, 855, 910, PINK, 0.5)
l2.badge(610, 700, 4).badge(770, 690, 2)
l0 = Panel(L3 + 'site0.jpg', crop=(540, 540, 1490, 960))
l0.rect(560, 600, 1440, 945, BLUE, 0.28)
l0.poly([(800, 600), (840, 700), (860, 800), (805, 800), (785, 700), (760, 640)], PINK, 0.55)
l0.badge(1000, 780, 3).badge(820, 640, 2)
tile([(ls, (0.0, 0.0, 1.0, 0.5), '단면 S1(동서)'), (l2, (0.0, 0.5, 0.42, 0.5), '2층 평면'), (l0, (0.42, 0.5, 0.58, 0.5), '1층 평면')], 'd_lincoln.jpg')

# ---------------- 평택 JS타워 (사진 판독 + 자체 작성 단면)
ph = Panel(T + '/cloud_repo/jeongdonggwan/build/assets/case_pyeongtaek.jpg', crop=(0, 100, 1400, 943))
ph.poly([(118,590),(255,148),(1090,505),(1090,718),(268,598)], GOLD, 0.26)
ph.poly([(125,612),(290,598),(1170,727),(1170,895),(132,872)], BLUE, 0.28)
ph.poly([(776,782),(948,782),(948,905),(776,905)], GREEN, 0.55)
ph.poly([(280,600),(1140,728),(1140,790),(280,665)], GOLD, 0.22)
ph.badge(700, 330, 1).badge(520, 790, 2).badge(862, 845, 3).badge(700, 700, 4)
ph.render(TW, TH, '입면 사진 분석').save(W + 'img2/d_js.jpg', quality=92)
print('d_js ok')
