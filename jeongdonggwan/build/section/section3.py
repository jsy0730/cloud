# 정동관 단면 v3: A 남북 종단면(개념), B 동서 횡단면(y≈50, 서측 끝 코어②·소로·스킵플로어)
s = 9.0; TOP = 30.5
C = dict(park='#f4d3b0', cult='#9dc3e6', biz='#fbf3a4', off='#d9cbe9', mep='#c9c9c9', lane='#bfbfbf', roof='#a9d18e', core='#ec8080', earth='#e9e4da', void='#ffffff', sunk='#dbeef4')
out = []; txt = []
def Y(z, oy): return oy + (TOP - z) * s
def R(x, y, w, h, fill, stroke='#000', sw=1.5, extra=''): out.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>')
def T(x, y, t, size=21, anchor='middle', weight=400, fill='#000'): txt.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" fill="{fill}">{t}</text>')
def L(x1, y1, x2, y2, stroke='#000', sw=1.5, extra=''): out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}" {extra}/>')
def blk(ox, oy, x0, x1, z0, h, kind, label='', size=21):
    R(ox + x0 * s, Y(z0 + h, oy), (x1 - x0) * s, h * s, C[kind])
    if label: T(ox + (x0 + x1) / 2 * s, Y(z0 + h / 2, oy) + size * 0.35, label, size)
def zig(ox, oy, x0, x1, z0, z1, color='#d2432a'):
    pts = []; z = z0; i = 0
    while z < z1 - 0.01:
        dz = min(1.75, z1 - z); a, b = (x0, x1) if i % 2 == 0 else (x1, x0)
        pts += [(ox + a * s, Y(z, oy)), (ox + b * s, Y(z + dz, oy))]; z += dz; i += 1
    out.append('<polyline points="' + ' '.join(f'{p:.1f},{q:.1f}' for p, q in pts) + f'" fill="none" stroke="{color}" stroke-width="3.5"/>')
def trees(ox, oy, x0, x1, z, n):
    for i in range(n):
        tx = ox + (x0 + (i + 0.5) * (x1 - x0) / n) * s; ty = Y(z, oy)
        L(tx, ty, tx, ty - 20, '#5a4a3a', 3); out.append(f'<circle cx="{tx:.1f}" cy="{ty - 31:.1f}" r="14" fill="#7fae5f" stroke="#3d5a2c"/>')
def section_A(ox, oy, Ln=121.9):
    R(ox - 30, Y(0, oy), Ln * s + 60, 16.4 * s, C['earth'], stroke='none')
    a0, a1 = 3.0, Ln - 3.0      # 3m 이격 (지상부)
    # basement (full site)
    blk(ox, oy, 0, 14, -15.6, 3.3, 'mep', '펌프·저수조'); blk(ox, oy, 14, Ln, -15.6, 3.3, 'park', '주차')
    blk(ox, oy, 0, 10, -12.3, 3.3, 'mep', '전기'); blk(ox, oy, 10, Ln, -12.3, 3.3, 'park', '주차')
    blk(ox, oy, 0, 29, -9.0, 9.0, 'park', '주차')
    blk(ox, oy, 35, 42, -9.0, 4.5, 'park', '')
    blk(ox, oy, 42, 64, -9.0, 4.5, 'cult', '공연장 200석', 21)
    R(ox + 29 * s, Y(0, oy), 13 * s, 4.5 * s, C['sunk'])
    T(ox + 38 * s, Y(-2.6, oy), '선큰 마당', 18, fill='#1f5f7a', weight=700)
    blk(ox, oy, 42, 56, -4.5, 4.5, 'cult', '로비·바')
    blk(ox, oy, 64, 70, -9.0, 4.5, 'cult', '', 18); blk(ox, oy, 56, 70, -4.5, 4.5, 'cult', '객석 상부', 18)
    blk(ox, oy, 70, Ln, -9.0, 4.5, 'park', ''); blk(ox, oy, 70, Ln, -4.5, 4.5, 'park', ''); T(ox + 80 * s, Y(-6.75, oy) + 7, '주차', 21); T(ox + 80 * s, Y(-2.25, oy) + 7, '주차', 21)
    # 1F (east plate 8.65 / west 7.0 shown as 7.0 programme strip)
    blk(ox, oy, a0, 29, 0, 8.65, 'biz', '근생 소점포')
    blk(ox, oy, 56, 89, 0, 8.65, 'park', '램프·정산·이륜차', 19)
    blk(ox, oy, 42, 56, 0, 7.0, 'biz', '공연 로비', 18)
    R(ox + 29 * s, Y(8.65, oy), 13 * s, 0.01, '#000')
    # skip floors (schematic: full bands with half-level marks)
    for z in (7.0, 10.3, 13.6):
        blk(ox, oy, 42, 89, z if z > 7.0 else 8.65, 3.3 if z > 7.0 else 1.65, 'park', '')
    blk(ox, oy, a0, 29, 8.65, 8.25, 'park', '')
    for z in (10.3, 13.6): L(ox + a0 * s, Y(z + 1.65, oy), ox + 29 * s, Y(z + 1.65, oy), '#000', 1.5)
    blk(ox, oy, 42, 89, 7.0, 9.9, 'park', '')
    for z in (10.3, 13.6): L(ox + 42 * s, Y(z, oy), ox + 89 * s, Y(z, oy), '#000', 1.5)
    T(ox + 65 * s, Y(12.2, oy), '주차 · 스킵플로어 (반 층 엇갈림)', 21, weight=700)
    T(ox + 16 * s, Y(13, oy), '주차', 21)
    # 5F
    blk(ox, oy, a0, 29, 16.9, 4.2, 'park', '주차(전환 층)', 18); blk(ox, oy, 42, 63, 16.9, 4.2, 'park', '주차(전환 층)', 18); blk(ox, oy, 63, 89, 16.9, 4.2, 'off', '상인회·공유오피스', 19)
    # 6F hall + terrace
    blk(ox, oy, 37, 89, 21.1, 8.0, 'cult', '체육·공연 가변홀 (층고 8m)', 22)
    R(ox + 37 * s, Y(29.8, oy), 52 * s, 0.7 * s, '#7f7f7f')
    R(ox + a0 * s, Y(21.6, oy), 26 * s, 0.5 * s, C['roof']); trees(ox, oy, a0 + 1, 28, 21.6, 4)
    T(ox + 16 * s, Y(21.6, oy) - 58, '옥상 광장', 22, weight=700)
    # tip core ② (open stair void, 29~42 region) : B1 sunken -> terrace
    R(ox + 29 * s, Y(21.6, oy), 13 * s, 21.6 * s, C['void'], stroke='#d2432a', sw=2, extra='stroke-dasharray="6 4"')
    zig(ox, oy, 30.5, 40.5, 0, 21.6); zig(ox, oy, 29.6, 33.2, -4.5, 0)
    T(ox + 35.5 * s, Y(23.0, oy), '끝 코어②', 20, weight=700, fill='#d2432a')
    R(ox + 29 * s, Y(-4.5, oy), 6 * s, 11.1 * s, C['core'], extra='fill-opacity="0.9"')
    T(ox + 32 * s, Y(-11, oy), '특피', 17)
    # tip core ① north end (89~a1): open stair to roof
    R(ox + 89 * s, Y(29.8, oy), (a1 - 89) * s, 29.8 * s, C['void'], stroke='#d2432a', sw=2, extra='stroke-dasharray="6 4"')
    zig(ox, oy, 91, 100, 0, 29.8)
    R(ox + 102 * s, Y(31.0, oy), 3.0 * s, 46.6 * s, '#cfe3ea', stroke='#5a7a88')
    T(ox + 106 * s, Y(10, oy), '승강기', 18, anchor='start', fill='#3c5a66')
    T(ox + 95 * s, Y(31.4, oy) - 6, '끝 코어①', 20, weight=700, fill='#d2432a')
    R(ox + 90 * s, Y(0, oy), 8 * s, 15.6 * s, C['core'], extra='fill-opacity="0.9"')
    T(ox + 94 * s, Y(-11, oy), '특피', 17)
    # 3m setbacks
    for xx in (a0, a1): L(ox + xx * s, Y(31, oy), ox + xx * s, Y(0, oy), '#2e75b6', 2, 'stroke-dasharray="6 5"')
    T(ox + a1 * s + 6, Y(4, oy), '3m', 18, anchor='start', fill='#2e75b6')
    L(ox - 50, Y(0, oy), ox + Ln * s + 50, Y(0, oy), '#000', 3)
    T(ox, Y(-15.6, oy) + 30, '← 남 · 전포대로224번길', 21, anchor='start', fill='#595959')
    T(ox + Ln * s, Y(-15.6, oy) + 30, '서전로 · 북 →', 21, anchor='end', fill='#595959')
    T(ox + Ln * s / 2, Y(-15.6, oy) + 66, 'A  남북 종단면 (개념)', 27, weight=700)
def section_B(ox, oy):
    w1, lw, w2 = 9.2, 6.7, 24.8; Wt = w1 + lw + w2; mid = w1 + lw / 2
    R(ox - 30, Y(0, oy), Wt * s + 60, 16.4 * s, C['earth'], stroke='none')
    blk(ox, oy, 0, Wt, -15.6, 3.3, 'park', '주차'); blk(ox, oy, 0, Wt, -12.3, 3.3, 'park', '주차')
    blk(ox, oy, 0, mid + 8, -9.0, 4.5, 'cult', '공연장', 21); blk(ox, oy, mid + 8, Wt, -9.0, 4.5, 'park', '주차')
    R(ox, Y(0, oy), w1 * s, 4.5 * s, C['sunk']); T(ox + w1 * 0.72 * s, Y(-2.6, oy), '선큰', 17, fill='#1f5f7a', weight=700)
    blk(ox, oy, w1, mid + 8, -4.5, 4.5, 'cult', '로비', 19); blk(ox, oy, mid + 8, Wt, -4.5, 4.5, 'park', '주차')
    # tip void on west (sunken -> terrace)
    R(ox, Y(21.6, oy), w1 * s, 21.6 * s, C['void'], stroke='#d2432a', sw=2, extra='stroke-dasharray="6 4"')
    zig(ox, oy, 0.8, w1 - 0.8, 0, 21.6); zig(ox, oy, 0.4, 3.6, -4.5, 0)
    T(ox + w1 / 2 * s, Y(23.2, oy), '코어②', 19, weight=700, fill='#d2432a')
    # lane
    blk(ox, oy, w1, w1 + lw, 0, 7.0, 'lane', '')
    T(ox + (w1 + lw / 2) * s, Y(4.4, oy), '소로', 19, weight=700); T(ox + (w1 + lw / 2) * s, Y(2.6, oy), '차로', 17)
    R(ox + (w1 + lw / 2) * s - 17, Y(1.5, oy), 34, 1.3 * s, '#404040', stroke='none', extra='rx="4"')
    blk(ox, oy, w1 + lw, Wt, 0, 8.65, 'park', '램프·근생', 18)
    # skip floors: west plate (w1..mid) 7.0/10.3/13.6, east plate (mid..Wt) 8.65/11.95/15.25
    R(ox + w1 * s, Y(16.9, oy), (Wt - w1) * s, 9.9 * s, C['park'])
    R(ox + (w1 + lw) * s, Y(8.65, oy), (Wt - w1 - lw) * s, 0.01, '#000')
    for z in (7.0, 10.3, 13.6, 16.9): L(ox + w1 * s, Y(z, oy), ox + mid * s, Y(z, oy), '#000', 2.5)
    for z in (8.65, 11.95, 15.25): L(ox + mid * s, Y(z, oy), ox + Wt * s, Y(z, oy), '#000', 2.5)
    L(ox + mid * s, Y(16.9, oy), ox + mid * s, Y(7.0, oy), '#d2432a', 2.5, 'stroke-dasharray="5 4"')
    out.append(f'<rect x="{ox + (mid + Wt) / 2 * s - 80:.1f}" y="{Y(12.6, oy) - 24:.1f}" width="180" height="56" fill="#fff" fill-opacity="0.9"/>')
    T(ox + (mid + Wt) / 2 * s + 10, Y(12.6, oy), '스킵플로어', 21, weight=700); T(ox + (mid + Wt) / 2 * s + 10, Y(12.6, oy) + 24, '소로 위에서 반 층', 18)
    blk(ox, oy, w1, Wt, 16.9, 4.2, 'park', '주차(전환 층)', 19)
    blk(ox, oy, w1, Wt, 21.1, 8.0, 'cult', '가변홀', 22)
    R(ox + w1 * s, Y(29.8, oy), (Wt - w1) * s, 0.7 * s, '#7f7f7f')
    L(ox - 50, Y(0, oy), ox + Wt * s + 50, Y(0, oy), '#000', 3)
    T(ox, Y(-15.6, oy) + 30, '← 서 · 전포대로', 21, anchor='start', fill='#595959')
    T(ox + Wt * s, Y(-15.6, oy) + 30, '동 →', 21, anchor='end', fill='#595959')
    T(ox + Wt * s / 2, Y(-15.6, oy) + 66, 'B  동서 횡단면 (코어②·소로)', 27, weight=700)
LV = [('B4', -15.6, 3.3), ('B3', -12.3, 3.3), ('B2', -9.0, 4.5), ('B1', -4.5, 4.5), ('1F', 0, 7.0), ('2F', 7.0, 3.3), ('3F', 10.3, 3.3), ('4F', 13.6, 3.3), ('5F', 16.9, 4.2), ('6F', 21.1, 8.0)]
def levels(x, oy):
    for nm, z, h in LV: T(x, Y(z + h / 2, oy) + 8, nm, 21, anchor='end', weight=700)
    T(x, Y(29.1, oy) - 2, '+29.1m', 18, anchor='end', fill='#595959'); T(x, Y(-15.6, oy) + 22, '−15.6m', 18, anchor='end', fill='#595959')
oy = 70; oxA = 150
section_A(oxA, oy); levels(oxA - 40, oy)
oxB = oxA + 121.9 * s + 140
section_B(oxB, oy)
Wd, Hd = 1920, 620
svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{Wd}" height="{Hd}" viewBox="0 0 {Wd} {Hd}" font-family="Pretendard, sans-serif"><rect width="100%" height="100%" fill="#fff"/>' + ''.join(out) + ''.join(txt) + '</svg>'
open('section3.html', 'w').write('<html><head><link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.css"></head><body style="margin:0">' + svg + '</body></html>')
print('B start', oxB, 'B end', oxB + 40.7 * s)
