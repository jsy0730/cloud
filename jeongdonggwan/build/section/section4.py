# 정동관 단면 v4 (scaled plan coords: site 4,964.5㎡, length 121.9m). A: 꺾인 종단면, B: 횡단면(y=70), 키 플랜
import sys, json, math
sys.path.insert(0, '/tmp/claude-0/-home-user-cloud/76ed2005-4113-58c6-b90f-f280afa8844d/scratchpad/build')
from numbers_base import *
from shapely.geometry import box
s = 9.2; TOP = 31.5; FS = 24
C = dict(park='#f4d3b0', cult='#9dc3e6', biz='#fbf3a4', off='#d9cbe9', mep='#c9c9c9', lane='#bfbfbf', roof='#a9d18e', core='#ec8080', earth='#ebe6dc', void='#ffffff', sunk='#cfe9f1', hall='#8fb8e0')
out = []; txt = []
def Y(z, oy): return oy + (TOP - z) * s
def R_(x, y, w, h, fill, stroke='#000', sw=1.6, extra=''): out.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>')
def T(x, y, t, size=FS, anchor='middle', weight=400, fill='#000'): txt.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" fill="{fill}">{t}</text>')
def L_(x1, y1, x2, y2, stroke='#000', sw=1.6, extra=''): out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}" {extra}/>')
def blk(ox, oy, a, b, z0, h, kind, label='', size=FS - 2):
    R_(ox + a * s, Y(z0 + h, oy), (b - a) * s, h * s, C[kind])
    if label: T(ox + (a + b) / 2 * s, Y(z0 + h / 2, oy) + size * 0.35, label, size)
def zig(ox, oy, a, b, z0, z1, color='#d2432a', n=1.75):
    pts = []; z = z0; i = 0
    while z < z1 - 0.01:
        dz = min(n, z1 - z); x0, x1 = (a, b) if i % 2 == 0 else (b, a)
        pts += [(ox + x0 * s, Y(z, oy)), (ox + x1 * s, Y(z + dz, oy))]; z += dz; i += 1
    out.append('<polyline points="' + ' '.join(f'{p:.1f},{q:.1f}' for p, q in pts) + f'" fill="none" stroke="{color}" stroke-width="3.5"/>')
def trees(ox, oy, a, b, z, n):
    for i in range(n):
        tx = ox + (a + (i + 0.5) * (b - a) / n) * s; ty = Y(z, oy)
        L_(tx, ty, tx, ty - 22, '#5a4a3a', 3); out.append(f'<circle cx="{tx:.1f}" cy="{ty - 34:.1f}" r="15" fill="#7fae5f" stroke="#3d5a2c"/>')
Ln = 121.9
def section_A(ox, oy):
    R_(ox - 40, Y(0, oy), Ln * s + 80, 16.4 * s, C['earth'], stroke='none')
    a0, a1 = 3.0, Ln - 3.0
    # basement: full length
    blk(ox, oy, 0, 14, -15.6, 3.3, 'mep', '펌프·저수조', FS - 4); blk(ox, oy, 14, Ln, -15.6, 3.3, 'park', '주차')
    blk(ox, oy, 0, 10, -12.3, 3.3, 'mep', '전기', FS - 4); blk(ox, oy, 10, Ln, -12.3, 3.3, 'park', '주차')
    blk(ox, oy, 0, 26, -9.0, 9.0, 'park', '주차'); blk(ox, oy, 26, 56, -9.0, 4.5, 'cult', '공연장 200석', FS)
    blk(ox, oy, 56, 68, -9.0, 4.5, 'cult', '분장', FS - 6)
    txt.append(f'<rect x="{ox + 37.5 * s:.1f}" y="{Y(-0.9, oy):.1f}" width="{9.5 * s:.1f}" height="34" fill="#fff" fill-opacity="0.92" rx="4"/>'); blk(ox, oy, 32, 52, -4.5, 4.5, 'cult', '로비·바', FS - 2); blk(ox, oy, 52, 68, -4.5, 4.5, 'cult', '객석 상부', FS - 6); blk(ox, oy, 26, 32, -4.5, 4.5, 'park', '')
    blk(ox, oy, 68, Ln, -9.0, 4.5, 'park', ''); blk(ox, oy, 68, Ln, -4.5, 4.5, 'park', ''); T(ox + 100 * s, Y(-6.75, oy) + 8, '주차'); T(ox + 100 * s, Y(-2.25, oy) + 8, '주차')
    # sunken court (tip 2) 29..55
    R_(ox + 29 * s, Y(0, oy), 26 * s, 4.5 * s, C['sunk']); txt.append(f'<rect x="{ox + 29.2 * s:.1f}" y="{Y(-1.0, oy):.1f}" width="{9.0 * s:.1f}" height="34" fill="#fff" fill-opacity="0.92" rx="4"/>'); T(ox + 34 * s, Y(-2.2, oy) + 2, '선큰 마당', FS - 6, weight=700, fill='#1f5f7a')
    # 1F + upper plates (east plate levels) for y 3..29 and 55..85
    for (p, q) in ((a0, 29), (55, 85)):
        lab = {a0: '근생 소점포'}.get(p, '')
        blk(ox, oy, p, q, 0, 8.65, 'biz' if p == a0 else 'park', lab if p == a0 else '')
        for z, h in ((8.65, 3.3), (11.95, 3.3), (15.25, 1.65)):
            blk(ox, oy, p, q, z, h, 'park', '')
        blk(ox, oy, p, q, 16.9, 4.2, 'park', '')
    T(ox + 70 * s, Y(4.3, oy) + 8, '램프·정산·이륜차', FS - 6)
    T(ox + 16 * s, Y(12.9, oy), '스킵플로어 주차', FS - 2, weight=700); T(ox + 16 * s, Y(19, oy), '주차(전환 층)', FS - 6)
    # 5F offices north part of 55..85
    blk(ox, oy, 66, 85, 16.9, 4.2, 'off', '상인회·오피스', FS - 6)
    # 6F hall over 55..85 ; terrace over 3..29
    blk(ox, oy, 55, 85, 21.1, 8.0, 'hall', '가변홀', FS)
    R_(ox + 55 * s, Y(29.8, oy), 30 * s, 0.7 * s, '#7f7f7f')
    R_(ox + a0 * s, Y(21.6, oy), 26 * s, 0.5 * s, C['roof']); trees(ox, oy, a0 + 1, 28, 21.6, 4); T(ox + 16 * s, Y(21.6, oy) - 60, '옥상 광장', FS, weight=700)
    # tip2 void (29..55) with open stair
    R_(ox + 29 * s, Y(21.6, oy), 26 * s, 26.1 * s, C['void'], stroke='#d2432a', sw=2, extra='stroke-dasharray="7 5"')
    zig(ox, oy, 31, 53, -4.5, 21.6, n=1.75)
    T(ox + 42 * s, Y(24.0, oy), '끝 코어② (개방 순환 계단)', FS - 4, weight=700, fill='#d2432a')
    R_(ox + 27.5 * s, Y(-4.5, oy), 3.5 * s, 11.0 * s, C['core'], extra='fill-opacity="0.9"'); T(ox + 29.2 * s, Y(-11.5, oy), '특피', 16)
    # tip1 void (85..a1)
    R_(ox + 85 * s, Y(29.8, oy), (a1 - 85) * s, 29.8 * s, C['void'], stroke='#d2432a', sw=2, extra='stroke-dasharray="7 5"')
    zig(ox, oy, 87, 107, 0, 29.8)
    R_(ox + 108 * s, Y(31.4, oy), 5.6 * s, 47.0 * s, '#cfe3ea', stroke='#5a7a88'); T(ox + 110.8 * s, Y(13.2, oy), '승강기', FS - 8, fill='#2c4a56')
    T(ox + 95 * s, Y(31.0, oy) - 8, '끝 코어① (순환 계단 + 승강기)', FS - 4, weight=700, fill='#d2432a')
    R_(ox + 85 * s, Y(0, oy), 8 * s, 15.6 * s, C['core'], extra='fill-opacity="0.9"'); T(ox + 89 * s, Y(-11.5, oy), '특피', 16)
    for xx in (a0, a1): L_(ox + xx * s, Y(31.5, oy), ox + xx * s, Y(0, oy), '#2e75b6', 2, 'stroke-dasharray="6 5"')
    T(ox + 1.5 * s, Y(5, oy), '3m', 18, fill='#2e75b6'); T(ox + (a1 + 1.5) * s, Y(5, oy), '3m', 18, fill='#2e75b6')
    L_(ox - 50, Y(0, oy), ox + Ln * s + 50, Y(0, oy), '#000', 3)
    T(ox, Y(-15.6, oy) + 34, '← 남 · 전포대로224번길', FS - 2, anchor='start', fill='#595959'); T(ox + Ln * s, Y(-15.6, oy) + 34, '서전로 · 북 →', FS - 2, anchor='end', fill='#595959')
    T(ox + Ln * s / 2, Y(-15.6, oy) + 78, 'A  소로를 따라 펼친 종단면 (개념)', FS + 4, weight=700)
def section_B(ox, oy):
    yy = 70; w1 = 16.7; lw = 6.2; w2 = 17.8; Wt = w1 + lw + w2
    R_(ox - 40, Y(0, oy), Wt * s + 80, 16.4 * s, C['earth'], stroke='none')
    for z, h in ((-15.6, 3.3), (-12.3, 3.3)): blk(ox, oy, 0, Wt, z, h, 'park', '주차')
    blk(ox, oy, 0, Wt, -9.0, 9.0, 'park', ''); T(ox + Wt / 2 * s, Y(-6.75, oy) + 8, '주차'); T(ox + Wt / 2 * s, Y(-2.25, oy) + 8, '주차')
    # 1F
    blk(ox, oy, 0, w1, 0, 7.0, 'biz', '카페·서점', FS - 2)
    R_(ox + w1 * s, Y(7.0, oy), lw * s, 7.0 * s, C['lane']); T(ox + (w1 + lw / 2) * s, Y(4.6, oy), '소로', FS - 4, weight=700); T(ox + (w1 + lw / 2) * s, Y(2.4, oy) + 4, '차로', FS - 8)
    R_(ox + (w1 + lw / 2) * s - 17, Y(1.5, oy), 34, 1.2 * s, '#404040', stroke='none', extra='rx="4"')
    blk(ox, oy, w1 + lw, Wt, 0, 8.65, 'park', '이륜차·하역', FS - 6)
    # plates
    mid = w1 + lw / 2
    R_(ox + 0 * s, Y(16.9, oy), (Wt) * s, 9.9 * s, C['park'])
    for z in (7.0, 10.3, 13.6, 16.9): L_(ox, Y(z, oy), ox + mid * s, Y(z, oy), '#000', 2.8)
    for z in (8.65, 11.95, 15.25): L_(ox + mid * s, Y(z, oy), ox + Wt * s, Y(z, oy), '#000', 2.8)
    L_(ox + mid * s, Y(16.9, oy), ox + mid * s, Y(7.0, oy), '#d2432a', 2.8, 'stroke-dasharray="6 4"')
    out.append(f'<rect x="{ox + 6:.1f}" y="{Y(13.4, oy) - 26:.1f}" width="{Wt * s - 12:.1f}" height="62" fill="#fff" fill-opacity="0.9"/>')
    T(ox + Wt / 2 * s, Y(12.9, oy) - 2, '스킵플로어', FS, weight=700); T(ox + Wt / 2 * s, Y(12.9, oy) + 26, '소로 위에서 반 층 엇갈림', FS - 6)
    blk(ox, oy, 0, Wt, 16.9, 4.2, 'park', '주차(전환 층)', FS - 4)
    blk(ox, oy, 0, Wt, 21.1, 8.0, 'hall', '6F 가변홀', FS)
    R_(ox, Y(29.8, oy), Wt * s, 0.7 * s, '#7f7f7f')
    L_(ox - 50, Y(0, oy), ox + Wt * s + 50, Y(0, oy), '#000', 3)
    T(ox, Y(-15.6, oy) + 34, '← 서 · 전포대로', FS - 2, anchor='start', fill='#595959'); T(ox + Wt * s, Y(-15.6, oy) + 34, '동 →', FS - 2, anchor='end', fill='#595959')
    T(ox + Wt * s / 2, Y(-15.6, oy) + 78, 'B  횡단면 (y=70m 지점)', FS + 4, weight=700)
LV = [('B4', -15.6, 3.3), ('B3', -12.3, 3.3), ('B2', -9.0, 4.5), ('B1', -4.5, 4.5), ('1F', 0, 7.0), ('2F', 7.0, 3.3), ('3F', 10.3, 3.3), ('4F', 13.6, 3.3), ('5F', 16.9, 4.2), ('6F', 21.1, 8.0)]
def levels(x, oy):
    for nm, z, h in LV: T(x, Y(z + h / 2, oy) + 9, nm, FS - 2, anchor='end', weight=700)
    T(x, Y(29.1, oy) - 6, '+29.1m', FS - 6, anchor='end', fill='#595959'); T(x, Y(-15.6, oy) + 24, '−15.6m', FS - 6, anchor='end', fill='#595959')
oy = 62; oxA = 140
section_A(oxA, oy); levels(oxA - 30, oy)
oxB = oxA + Ln * s + 150
section_B(oxB, oy)
Wd = int(oxB + 40.7 * s + 80); Hd = int(Y(-15.6, oy) + 100)
svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{Wd}" height="{Hd}" viewBox="0 0 {Wd} {Hd}" font-family="Pretendard, sans-serif"><rect width="100%" height="100%" fill="#fff"/>' + ''.join(out) + ''.join(txt) + '</svg>'
open('section4.html', 'w').write('<html><head><link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.css"></head><body style="margin:0">' + svg + '</body></html>')
json.dump({'Wd': Wd, 'Hd': Hd, 'oxA': oxA, 'oxB': oxB, 'Aend': oxA + Ln * s + 60, 'Bw': 40.7 * s}, open('sec4.json', 'w'))
print(Wd, Hd, oxB)
