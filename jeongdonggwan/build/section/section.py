# schematic sections of 정동관 -> section.html (rendered by shot.mjs)
import json, sys
CFG = json.load(open('cfg.json'))
s = 9.0                      # px per metre
LV = [('B4', -15.6, 3.3), ('B3', -12.3, 3.3), ('B2', -9.0, 4.5), ('B1', -4.5, 4.5), ('1F', 0, 7.0),
      ('2F', 7.0, 3.3), ('3F', 10.3, 3.3), ('4F', 13.6, 3.3), ('5F', 16.9, 4.2), ('6F', 21.1, 8.0)]
C = dict(park='#f4d3b0', cult='#9dc3e6', biz='#fbf3a4', off='#d9cbe9', mep='#c9c9c9', lane='#c3dcb4', roof='#a9d18e', core='#ec8080', earth='#e9e4da')
out = []; txt = []
def R(x, y, w, h, fill, stroke='#000', sw=1.5, extra=''):
    out.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>')
def T(x, y, t, size=22, anchor='middle', weight=400, fill='#000'):
    txt.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" fill="{fill}">{t}</text>')
def L(x1, y1, x2, y2, stroke='#000', sw=1.5, extra=''):
    out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}" {extra}/>')
TOP = 29.7
def Y(z, oy): return oy + (TOP - z) * s
def block(ox, oy, x0, x1, z0, h, kind, label='', size=22):
    R(ox + x0 * s, Y(z0 + h, oy), (x1 - x0) * s, h * s, C[kind])
    if label: T(ox + (x0 + x1) / 2 * s, Y(z0 + h / 2, oy) + size * 0.35, label, size)
def section_A(ox, oy, Ln):
    # schematic long section, south (x=0) -> north (x=Ln)
    y6, yo = CFG['y6s'], CFG['office_ys']
    # earth
    R(ox - 30, Y(0, oy), Ln * s + 60, 16.4 * s, C['earth'], stroke='none')
    # basement
    for nm, z, h in LV[:4]:
        if nm == 'B4': block(ox, oy, 0, 14, z, h, 'mep', '펌프·저수조'); block(ox, oy, 14, Ln, z, h, 'park', '주차')
        if nm == 'B3': block(ox, oy, 0, 10, z, h, 'mep', '전기'); block(ox, oy, 10, Ln, z, h, 'park', '주차')
    block(ox, oy, 0, 30, -9.0, 9.0, 'park', '주차')
    block(ox, oy, 30, 62, -9.0, 9.0, 'cult', '공연장 120석', 24)
    block(ox, oy, 62, 78, -4.5, 4.5, 'cult', '로비')
    block(ox, oy, 62, 78, -9.0, 4.5, 'cult', '분장·창고', 20)
    block(ox, oy, 78, Ln, -9.0, 4.5, 'park', '주차'); block(ox, oy, 78, Ln, -4.5, 4.5, 'park', '주차')
    # 1F
    block(ox, oy, 0, 16, 0, 7.0, 'biz', '근생')
    block(ox, oy, 16, 70, 0, 7.0, 'park', '진출입·정산·램프')
    block(ox, oy, 70, Ln, 0, 7.0, 'biz', '서점·카페·공연 로비')
    # 2-4F
    for nm, z, h in LV[5:8]: block(ox, oy, 0, Ln, z, h, 'park', '주차 (스킵플로어)' if nm == '3F' else '주차')
    block(ox, oy, 0, yo, 16.9, 4.2, 'park', '주차'); block(ox, oy, yo, Ln, 16.9, 4.2, 'off', '상인회·공유오피스')
    block(ox, oy, y6, Ln, 21.1, 8.0, 'cult', '체육·공연 겸용홀 (층고 8m)', 24)
    R(ox + y6 * s, Y(29.7, oy), (Ln - y6) * s, 0.6 * s, '#7f7f7f')
    # roof plaza
    R(ox, Y(21.6, oy), y6 * s, 0.5 * s, C['roof'])
    for i in range(5):
        tx = ox + (4 + i * (y6 - 8) / 4) * s; ty = Y(21.6, oy)
        L(tx, ty, tx, ty - 22, '#5a4a3a', 3); out.append(f'<circle cx="{tx:.1f}" cy="{ty - 34:.1f}" r="16" fill="#7fae5f" stroke="#3d5a2c"/>')
    T(ox + y6 / 2 * s, Y(21.6, oy) - 64, '옥상 광장 (밤 개방)', 24, weight=700)
    # external stair (Park 'n' Play) on south face
    sx = ox - 4.5 * s
    pts = []
    for i in range(6):
        z0 = i * 3.6; pts += [(sx + (0 if i % 2 == 0 else 4.0 * s), Y(z0, oy)), (sx + (4.0 * s if i % 2 == 0 else 0), Y(z0 + 3.6, oy))]
    out.append('<polyline points="' + ' '.join(f'{a:.1f},{b:.1f}' for a, b in pts) + '" fill="none" stroke="#2e75b6" stroke-width="3"/>')
    T(sx + 2.0 * s, Y(22.6, oy), '외부 계단', 20, anchor='middle', fill='#2e75b6')
    # core
    for cx in (23, 110):
        R(ox + cx * s, Y(29.1 if cx > y6 else 21.1, oy), 5 * s, ((29.1 if cx > y6 else 21.1) + 15.6) * s, C['core'], extra='fill-opacity="0.55"')
    # ground & road labels
    L(ox - 60, Y(0, oy), ox + Ln * s + 60, Y(0, oy), '#000', 3)
    T(ox, Y(-15.6, oy) + 30, '← 남 · 전포대로224번길', 22, anchor='start', fill='#595959')
    T(ox + Ln * s, Y(-15.6, oy) + 30, '서전로 · 북 →', 22, anchor='end', fill='#595959')
    T(ox + Ln * s / 2, Y(-15.6, oy) + 72, 'A  남북 종단면 (개념)', 28, weight=700)
def section_B(ox, oy):
    w1, lw, w2 = CFG['wW'], CFG['wLane'], CFG['wE']
    Wt = w1 + lw + w2
    R(ox - 30, Y(0, oy), Wt * s + 60, 16.4 * s, C['earth'], stroke='none')
    block(ox, oy, 0, Wt, -15.6, 3.3, 'park', '주차'); block(ox, oy, 0, Wt, -12.3, 3.3, 'park', '주차')
    block(ox, oy, 0, w1 + 2, -9.0, 9.0, 'cult', '공연장', 22)
    block(ox, oy, w1 + 2, Wt, -9.0, 4.5, 'park', '주차'); block(ox, oy, w1 + 2, Wt, -4.5, 4.5, 'park', '주차')
    block(ox, oy, 0, w1, 0, 7.0, 'biz', '서점·카페', 20)
    block(ox, oy, w1, w1 + lw, 0, 7.0, 'lane', '')
    lx = ox + (w1 + lw / 2) * s
    T(lx, Y(4.6, oy), '소로', 20, weight=700, fill='#1e5a24'); T(lx, Y(2.9, oy), '차로', 18, fill='#1e5a24')
    block(ox, oy, w1 + lw, Wt, 0, 7.0, 'park', '램프')
    # skip floors: west half at floor level, east half +1.65m (half level)
    mid = w1 + lw / 2
    R(ox, Y(16.9, oy), Wt * s, 9.9 * s, C['park'])
    for z in (7.0, 10.3, 13.6, 16.9):
        L(ox, Y(z, oy), ox + mid * s, Y(z, oy), '#000', 2.5)
    for z in (8.65, 11.95, 15.25):
        L(ox + mid * s, Y(z, oy), ox + Wt * s, Y(z, oy), '#000', 2.5)
    L(ox + mid * s, Y(16.9, oy), ox + mid * s, Y(7.0, oy), '#000', 1.2, 'stroke-dasharray="3 4"')
    out.append(f'<rect x="{ox + Wt * s / 2 - 70:.1f}" y="{Y(13.1, oy):.1f}" width="140" height="56" fill="#fff" fill-opacity="0.85"/>')
    T(ox + Wt * s / 2, Y(12.0, oy) - 2, '스킵플로어', 22, weight=700); T(ox + Wt * s / 2, Y(12.0, oy) + 24, '반 층 엇갈림', 20)
    block(ox, oy, 0, Wt, 16.9, 4.2, 'park', '주차')
    block(ox, oy, 0, Wt, 21.1, 8.0, 'cult', '겸용홀', 22)
    R(ox, Y(29.7, oy), Wt * s, 0.6 * s, '#7f7f7f')
    L(ox - 60, Y(0, oy), ox + Wt * s + 60, Y(0, oy), '#000', 3)
    # car + arrow on lane
    cx = ox + (w1 + lw / 2) * s
    R(cx - 18, Y(1.6, oy), 36, 1.4 * s, '#404040', stroke='none', extra='rx="4"')
    T(ox, Y(-15.6, oy) + 30, '← 서 · 전포대로', 22, anchor='start', fill='#595959')
    T(ox + Wt * s, Y(-15.6, oy) + 30, '동 →', 22, anchor='end', fill='#595959')
    T(ox + Wt * s / 2, Y(-15.6, oy) + 72, 'B  동서 횡단면 (소로 통과)', 28, weight=700)
def levels(ox, oy, x1):
    for nm, z, h in LV:
        L(ox, Y(z, oy), x1, Y(z, oy), '#8c8c8c', 1, 'stroke-dasharray="4 6"')
        T(ox - 10, Y(z + h / 2, oy) + 8, nm, 22, anchor='end', weight=700)
    T(ox - 10, Y(29.1, oy) - 6, '+29.1m', 20, anchor='end', fill='#595959')
    T(ox - 10, Y(-15.6, oy) + 24, '−15.6m', 20, anchor='end', fill='#595959')
Ln = CFG['len']
W = 1920; H = 600
oyA = 70
oxA = 210
section_A(oxA, oyA, Ln)
oxB = oxA + Ln * s + 170
section_B(oxB, oyA)
levels(oxA - 64, oyA, oxA - 64)
svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Pretendard, sans-serif">' + '<rect width="100%" height="100%" fill="#fff"/>' + ''.join(out) + ''.join(txt) + '</svg>'
html = '<html><head><link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.css"></head><body style="margin:0">' + svg + '</body></html>'
open('section.html', 'w').write(html)
print('B starts', oxB, 'B width', (CFG['wW'] + CFG['wLane'] + CFG['wE']) * s)
