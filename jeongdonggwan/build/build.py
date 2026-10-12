import sys, json, math
sys.path.insert(0, '.')
from kit import *
from geo import POLY_M, REF, K
from shapely.geometry import Polygon, box as sbox
from PIL import Image

B = '/tmp/claude-0/-home-user-cloud/76ed2005-4113-58c6-b90f-f280afa8844d/scratchpad/build/'
IMG = B + 'img/'
MAPS = json.load(open(B + 'maps.json'))
TOTAL = 14
D = Deck(TOTAL, base=B + '../r/deck.pptx', keep=1)

# ----------------------------------------------------------------- programme (잠정)
SITE_W, SITE_E, ROAD = 1531.9, 2699.5, 733.1
G1 = SITE_W + SITE_E                  # 4,231.4 (1F 바닥: 소로 부분은 공공 통로로 비움)
SITE = SITE_W + SITE_E + ROAD         # 4,964.5 (도로 부지 편입)
BLK = SITE
# floor: (name, gfa, non-parking, height m, uses)
FL = [('옥상', 0, 0, 0, '옥상 녹지·광장 (6F 상부 약 3,400㎡ · 밤 개방)'),
      ('6F', 3400, 3400, 8.0, '체육·공연 겸용홀 1,500 · 다목적·연습 900 · 지원 600 · 코어 400 + 옥외 테라스 약 1,560'),
      ('5F', BLK, 1600, 4.2, '상인회·회의·공유오피스 1,200 · 코어 400 · 주차 3,365'),
      ('4F', BLK, 400, 3.3, '주차 4,565 · 코어 400'),
      ('3F', BLK, 400, 3.3, '주차 4,565 · 코어 400'),
      ('2F', BLK, 400, 3.3, '주차 4,565 · 코어 400 (도로 상공 연결 시작)'),
      ('1F', G1, G1 - 1800, 7.0, '서측: 서점 400·카페 400·공연 로비 300 / 동측: 진출입·정산·램프 1,800·남측 근생 600 / 하역 150·코어 580'),
      ('B1', BLK, 900, 4.5, '공연장 로비·객석 상부 900 · 주차 4,065'),
      ('B2', BLK, 1000, 4.5, '공연장 120석(객석·무대) 700 · 분장·창고 300 · 주차 3,965'),
      ('B3', BLK, 300, 3.3, '전기·기계 300 · 주차 4,665'),
      ('B4', BLK, 600, 3.3, '펌프·저수조 600(침수 고려) · 주차 4,365')]
GFA = sum(f[1] for f in FL); NON = sum(f[2] for f in FL); PARK = GFA - NON
ABOVE = sum(f[1] for f in FL if f[0][0] in '0123456789'); BELOW = GFA - ABOVE
PR = PARK / GFA * 100; FAR = ABOVE / SITE * 100; BCR = BLK / SITE * 100
CARS = round(PARK / 35, -1)
H_ABOVE = sum(f[3] for f in FL if f[0][0] in '0123456789'); H_BELOW = sum(f[3] for f in FL if f[0][0] == 'B')
assert abs(GFA - 47347.4) < 0.5 and abs(PR - 75.86) < 0.05
f1 = lambda v: f'{v:.1f}'
LEG = [('ink2', '주차 駐車'), ('beige', '낮 상권 商圈·상인'), ('blue', '공연·체육·창작 公演'), ('line', '코어·지원·설비')]


def legend(sl, x, y, items=LEG, size=12, gap=2.6):
    for i, (c, t) in enumerate(items):
        box(sl, x + i * gap, y + 0.06, 0.22, 0.22, fill=C[c])
        text(sl, x + i * gap + 0.28, y, gap - 0.3, 0.32, t, size=size, color='ink2')


def card(sl, x, y, w, h, title, body, title_fill='ink', size=13, tsize=14):
    text(sl, x, y, w, 0.42, title, size=tsize, bold=True, color='bg', fill=C[title_fill], anchor='m', inset=0.1)
    text(sl, x, y + 0.42, w, h - 0.42, body, size=size, color='ink', fill=C['pale'], inset=0.12, spacing=1.1)


def bullets(sl, x, y, w, items, size=14, nw=0.36, gap=0.12, lh=None, numfill='ink'):
    """numbered points; items = [(title, body)] ; returns y"""
    for i, (t, b) in enumerate(items, 1):
        num(sl, x, y + 0.03, nw, str(i), fill=numfill, size=12)
        nl = max(1, math.ceil(len(b) / (w * 4.2 / (size / 14))))
        h = lh or (0.38 + 0.3 * nl)
        text(sl, x + nw + 0.12, y, w - nw - 0.12, h, [[(t, {'bold': True})], b], size=size, spacing=1.05)
        y += h + gap
    return y


# ================================================================ 2. 목차
def s_toc():
    sl = D.slide()
    text(sl, 1.15, 0.62, 6, 0.4, 'CONTENTS', size=15, color='mute', bold=True)
    text(sl, 1.15, 1.02, 10, 0.72, '목차', size=34, bold=True)
    hline(sl, 1.15, 1.84, 17.7, 'mute')
    rows_ = [('01', '사업 배경', '事業槪要', '사업 개요와 문제 · 停棟과 動棟 컨셉 · 세 가지 역할', '3–4'),
             ('02', '대지 분석', '垈地分析', '통합 대지 4,965㎡ · 향·소음·조망 · 교통과 동선', '5–7'),
             ('03', '참고 사례', '事例分析', '헤르마(입지) · 평택 JS타워(주차) · 블라이바흐(공연장)', '8'),
             ('04', '계획과 조닝', '計畫槪要', '배치·매스 · 수직/수평 조닝 · 두 동 연결과 램프 · 피난·차음', '9–13'),
             ('05', '법규 검토', '法規檢討', '두 대지 각각의 기준 · 연결통로 · 확인 필요 항목', '14'),
             ]
    y = 2.35
    for n, k, h, d, p in rows_:
        text(sl, 1.15, y, 1.0, 0.7, n, size=30, bold=True, color='ink' if n != '—' else 'mute', anchor='m')
        text(sl, 2.3, y, 4.6, 0.7, [[(k, {'bold': True, 'size': 24}), ('  ' + h, {'color': 'mute', 'size': 16})]], anchor='m')
        text(sl, 7.2, y, 9.8, 0.7, d, size=17, color='ink2', anchor='m')
        text(sl, 17.0, y, 1.85, 0.7, p, size=17, color='mute', align='r', anchor='m')
        hline(sl, 1.15, y + 0.86, 17.7, 'line')
        y += 1.08
    # change note
    text(sl, 1.15, 9.0, 17.7, 0.9,
         [[('이번 판에서 바뀐 것  ', {'bold': True}),
           ('대지를 소로3류와 동측 삼각 블록까지 넓혔다(1,531.9㎡ → 4,964.5㎡, 도로 부지 편입). 1층은 소로 자리를 공공 통로로 비워 두 동으로 나누고, 2층 이상과 지하 4개 층은 한 판으로 필지를 꽉 채운다(지하 4층·지상 6층+옥상). '
            '향·소음·조망 분석을 새로 넣고, 단계별로 겹치던 장표(23장)를 15장으로 합쳤다.', {})]],
         size=15, fill=C['pale'], inset=0.15, anchor='m')
    footer(D, sl)


# ================================================================ 3. 사업 개요 + 문제
def s_overview():
    sl = D.slide()
    box(sl, 0, 0, 6.25, 11.25, fill=C['ink'])
    kp = [('4,965㎡', '대지면적 (서측 1,531.9 + 소로 733.1 + 동측 2,699.5)'),
          (f'{GFA:,.0f}㎡', f'연면적 (지상 {ABOVE:,.0f} + 지하 {BELOW:,.0f})'),
          (f'{PR:.1f}%', '주차부 비율 (특례 기준 70% 이상)'),
          (f'약 {CARS:,.0f}대', '주차대수 (잠정 · 대당 약 35㎡ · 기존안 180~210)')]
    y = 1.3
    for v, t in kp:
        text(sl, 1.0, y, 5.0, 1.0, v, size=58, bold=True, color='pale')
        text(sl, 1.0, y + 1.02, 5.0, 0.4, t, size=14, color='line')
        y += 2.2
    x0, w = 6.9, 11.95
    header(sl, 1, '사업 개요 — 흩어진 주차를 한 블록에 모으고, 남는 시간은 공공에', x0=x0, w=w)
    text(sl, x0, 2.0, w, 0.45, '소필지 상권의 주차를 한 거점이 떠안고, 비는 시간에는 공연·체육·상인 공간으로 쓰는 주차전용건축물',
         size=16, color='ink')
    rows(sl, x0, 2.55, w, [
        ('사업명', '전포 정동관(停動館) — 두 필지를 2층부터 잇는 주차·문화 복합건축물'),
        ('위치', '부산진구 전포동 207-1 외 52필지 (서측 19 · 소로 5 · 동측 29필지)'),
        ('대지', '4,964.5㎡ = 서측 1,531.9 + 소로3류 부지 733.1 + 동측 2,699.5 · 소로는 1층 공공 통로로 유지'),
        ('지역지구', '일반상업지역 · 방화지구 · 가로구역별 최고높이(기준 130m / 최고 180m)'),
        ('규모', f'지하 4층 · 지상 6층 + 옥상 (높이 약 {H_ABOVE:.0f}m) · 1F 두 동, 2F 이상·지하는 도로 위·아래로 연결'),
        ('연면적', f'약 {GFA:,.0f}㎡ (지상 {ABOVE:,.0f} + 지하 {BELOW:,.0f}) · 용적률 {FAR:.1f}%'),
        ('주요 시설', '1F 서점·카페·근생 · 2~5F 주차 · 5F 상인회 · 6F 체육·공연 겸용홀 · B1~B2 공연장 120석 · 옥상 광장'),
    ], kw=1.6, size=14.5, rh=0.43)
    # problem
    y0 = 5.85
    text(sl, x0, y0, 5.6, 0.4, '왜 여기인가 — 양이 아니라 분포의 문제', size=17, bold=True)
    text(sl, x0, y0 + 0.5, 5.6, 0.3, '부산 전체 주차 확보율 (2022)', size=12.5, color='mute')
    box(sl, x0, y0 + 0.85, 4.0, 0.42, fill=C['ink']); text(sl, x0 + 4.1, y0 + 0.8, 1.5, 0.5, '130.5%', size=20, bold=True)
    text(sl, x0, y0 + 1.37, 5.6, 0.3, '주차환경개선지구(상가밀집지역)', size=12.5, color='mute')
    box(sl, x0, y0 + 1.72, 4.0 * 69 / 130.5, 0.42, fill=C['mute']); text(sl, x0 + 2.2, y0 + 1.67, 1.5, 0.5, '69%', size=20, bold=True)
    text(sl, x0, y0 + 2.25, 5.6, 0.5, '격차 61.5%p · 시 계획: 2025년까지 6,092면 추가, 1,995억 원(목표 75.6%)', size=12, color='ink2')
    for i, (n, t, b) in enumerate([('01', '주차 부족', '이면도로 불법주차 상시'), ('02', '보행 위협', '좁은 보도를 주차 차량이 잠식'),
                                   ('03', '공용 공간 부재', '상인회 사무실·주민 휴게공간 없음')]):
        yy = y0 + 2.85 + i * 0.5
        chip(sl, x0, yy, 0.45, 0.42, n, size=12)
        text(sl, x0 + 0.55, yy, 5.1, 0.42, [[(t + '  ', {'bold': True}), (b, {'color': 'ink2'})]], size=13.5, anchor='m')
    pic_crop(sl, IMG + 'image3.jpeg', x0 + 5.85, y0, 2.95, 2.55)
    pic_crop(sl, IMG + 'image4.jpeg', x0 + 8.95, y0, 3.0, 2.55)
    text(sl, x0 + 5.85, y0 + 2.6, 6.1, 0.3, '이면도로 불법주차·이륜차 (전포동 현장)', size=11.5, color='mute')
    text(sl, x0 + 5.85, y0 + 3.0, 6.1, 1.35,
         [[('지하철이 가까운데 왜 주차장인가? ', {'bold': True}),
           ('공급을 늘리는 시설이 아니라 이면도로에 흩어진 주차를 한 블록으로 재배치하는 시설이다. 주차장은 상주 인구가 없어 층간소음 민원 주체가 없으므로 공연·체육을 곁에 둘 수 있다.', {})]],
         size=13, fill=C['pale'], inset=0.12, spacing=1.08)
    footer(D, sl, '부산시 주차종합계획(2022) · 파이낸셜뉴스 2022.07.11 · 정책브리핑 · 토지이음(2026-10-11 조회) · 면적·대수는 잠정', x0=x0, w=w)


# ================================================================ 4. 컨셉
def s_concept():
    sl = D.slide()
    header(sl, 1, '停과 動 — 낮에는 주차장, 밤에는 광장')
    x, y = 1.15, 2.1
    cw = [1.35, 3.45, 3.45]
    text(sl, x, y, sum(cw), 0.45, [[('층별 쓰임 ', {'bold': True, 'size': 17}), ('낮엔 停이, 밤엔 動이 우세', {'color': 'mute'})]], size=13, anchor='m')
    y += 0.5
    for k, h in enumerate(['층', '晝 낮 · 停 우세', '夜 밤 · 動 우세']):
        text(sl, x + sum(cw[:k]), y, cw[k] - 0.04, 0.38, h, size=12.5, bold=True, color='bg', fill=C['mute'], align='c', anchor='m')
    y += 0.42
    R = [('옥상', ('휴게 녹지', 'pale'), ('옥상 광장 개방', 'blue')),
         ('6F', ('체육 (겸용홀)', 'blue'), ('공연 (무대 가변)', 'blue')),
         ('5F', ('상인회·회의 + 주차', 'beige'), ('주민 모임 · 주차', 'beige')),
         ('2~4F', ('주차', 'ink2'), ('주차', 'ink2')),
         ('1F 서측', ('서점·카페', 'beige'), ('공연 로비·카페', 'beige')),
         ('1F 동측', ('진출입·정산 · 남측 근생', 'beige'), ('진출입 · 근생', 'beige')),
         ('B1~B2', ('리허설 · 휴지 + 주차', 'pale'), ('공연장 120석 + 관객 주차', 'blue')),
         ('B3~B4', ('주차·설비', 'ink2'), ('주차·설비', 'ink2'))]
    rh = 0.5
    for fl, a, b in R:
        text(sl, x, y, cw[0] - 0.04, rh - 0.05, fl, size=12.5, bold=True, fill=C['pale'], align='c', anchor='m')
        for k, (t, c) in enumerate((a, b)):
            dark = c in ('ink2', 'blue', 'mute')
            text(sl, x + cw[0] + k * cw[1], y, cw[1] - 0.04, rh - 0.05, t, size=12.5, color='bg' if dark else 'ink', fill=C[c], align='c', anchor='m')
        y += rh
    text(sl, x, y + 0.1, sum(cw), 0.62,
         '주차층(2~5F, B1~B4)은 밤에도 운영된다. 바뀌는 것은 그 위아래 층(6F·옥상, B1~B2)과 1층의 쓰임이다. 1층 두 동 사이 소로는 2층 아래 지붕 덮인 가로가 된다.',
         size=12.5, color='ink2', spacing=1.05)
    legend(sl, x, y + 0.85, size=11.5, gap=2.05)
    rx, rw = 9.9, 8.95
    text(sl, rx, 2.1, rw, 0.45, '세 가지 역할', size=17, bold=True)
    roles = [('停', '주차 거점 — 차를 모은다', f'상가밀집지역 확보율 69%를 메우고, 이면도로 불법주차를 한 블록으로 흡수한다. 약 {CARS:,.0f}대(잠정) 중 법정 부설분을 뺀 나머지가 상권·방문객 몫.'),
             ('動', '공연 거점 — 사람을 모은다', '밤과 주말, 지하 공연장(120석)과 6F 겸용홀로 사람이 모인다. 관객은 주차층에서 코어로 바로 공연장 로비에 닿는다.'),
             ('標', '랜드마크 — 전포동의 얼굴', '전포사거리 모퉁이에서 낮엔 서점·카페, 밤엔 공연과 옥상 광장이 켜진다. 도로 위로 걸친 2층 이상 매스가 블록 전체를 하나의 얼굴로 묶는다.')]
    yy = 2.65
    for m, t, b in roles:
        text(sl, rx, yy, 1.0, 1.2, m, size=40, bold=True, color='bg', fill=C['ink'], align='c', anchor='m')
        text(sl, rx + 1.1, yy, rw - 1.1, 1.2, [[(t, {'bold': True, 'size': 15})], b], size=13, fill=C['pale'], inset=0.12, spacing=1.05)
        yy += 1.32
    text(sl, rx, yy + 0.05, rw, 0.4, '공연장이 두 곳인 이유', size=15, bold=True)
    table(sl, rx, yy + 0.5, [1.3, 3.8, 3.85], [
        ['', '지하 B1~B2 · 120석', '6F 겸용홀 · 약 1,500㎡'],
        ['성격', '음향 우선 · 클래식·연극형', '낮 체육 · 밤 공연 겸용 (무대 가변)'],
        ['이유', '지하는 외부 소음(전포대로)에 강하다', '최상층이라 진동 민원이 적고 옥상과 이어진다'],
    ], rh=0.38, size=12)
    text(sl, rx, 9.6, rw, 0.55, [[('선순환  ', {'bold': True}), ('공연·행사 → 방문객 증가 → 주차 수요 → 주차 수익 → 주변 상권 매출', {})]],
         size=13, fill=C['beige'], inset=0.12, anchor='m')
    footer(D, sl, '조닝 · 공연장 조성 매뉴얼(예술경영지원센터, 2008) · 면적·대수는 잠정')


# ================================================================ 5. 통합 대지
def plan_shape(sl, ox, oy, s, pts_m, **kw):
    """draw polygon given in local metres (x east, y north) with origin at (ox,oy) inches = SW corner, s in/m"""
    return freeform(sl, [(ox + x * s, oy - y * s) for x, y in pts_m], **kw)


def s_site():
    sl = D.slide()
    header(sl, 2, '대지 — 쐐기·소로·삼각 블록을 한 필지로, 합계 4,964.5㎡')
    # left table
    x = 1.15
    table(sl, x, 2.1, [1.15, 1.75, 1.6, 1.75, 1.0], [
        ['', '서측', '소로3류 부지', '동측', '합계'],
        ['지번', '207-2 외 18', '207-15 외 4', '207-1 외 28', '53필지'],
        ['면적', ('1,531.9㎡', {'bold': True}), ('733.1㎡', {'bold': True}), ('2,699.5㎡', {'bold': True}), ('4,964.5', {'bold': True})],
        ['형상', '남북 약 96m\n쐐기(북이 넓음)', '폭 8m 미만\n사선 띠', '남북 약 125m\n삼각(남이 넓음)', '정형 블록'],
        ['접도', '서 전포대로\n(광로2류)', '북 서전로\n남 224번길', '북 서전로 · 남\n224번길 · 동 이면도로', '4면 도로'],
        ['1F 쓰임', '서점·카페\n공연 로비', '공공 통로\n(차량·보행)', '진출입·정산\n램프 · 남측 근생', '2F~ 한 판'],
    ], rh=0.62, size=12, rhs=[0.42, 0.42, 0.42, 0.72, 0.72, 0.72], aligns=['l', 'c', 'c', 'c', 'c'])
    yy = 2.1 + 0.42 * 3 + 0.72 * 3 + 0.15
    text(sl, x, yy, 7.2, 1.55,
         [[('소로3류 부지를 대지에 넣는다  ', {'bold': True}),
           ('207-15·38·79(지목 도로)와 207-84·85(지목 대, 도로로 이용). 도로 용도폐지·매입을 전제로 대지에 편입하고, 1층은 그 자리를 공공 통로로 열어 기존 통행을 이어 준다(폐도·대체 통로 협의 확인 필요).', {})]],
         size=12.5, fill=C['pale'], inset=0.12, spacing=1.05)
    yy += 1.68
    text(sl, x, yy, 7.2, 1.3,
         [[('왜 넓히나  ', {'bold': True}),
           ('기존 대지는 건축 가능 영역이 약 920㎡뿐이라 용적률(326%)보다 바닥이 먼저 막혔다. 세 필지군을 합치면 한 층이 약 4,965㎡인 정형 바닥이 생겨 램프·주차 효율이 크게 오른다.', {})]],
         size=12.5, fill=C['beige'], inset=0.12, spacing=1.05)
    yy += 1.42
    text(sl, x, yy, 7.2, 0.75,
         '서측 207-2·4·18·20·41·42·43·44·46·47·57·63·67·68·69·70·83·87·103 / 소로 207-15·38·79·84·85 / 동측 207-1·3·5·6·7·9·10·24·26·28·29·30·32·34·35·36·37·40·50·52·54·55·73·75·77·86·89·90·102',
         size=9.5, color='mute', spacing=1.0)
    # middle: eum capture with overlay
    im = Image.open(B + '../eum/p2400x2.png').convert('RGBA')
    from PIL import ImageDraw
    ov = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    to2400 = lambda p: (p[0] + 300, p[1] + 250)
    d.polygon([to2400(p) for p in REF['W']], fill=(232, 213, 160, 150), outline=(31, 34, 36, 255))
    d.polygon([to2400(p) for p in REF['E']], fill=(124, 142, 150, 150), outline=(31, 34, 36, 255))
    d.polygon([to2400(p) for p in REF['R']], fill=(181, 82, 59, 90), outline=(31, 34, 36, 255))
    for k in 'WE':
        d.line([to2400(p) for p in REF[k] + [REF[k][0]]], fill=(31, 34, 36, 255), width=4)
    cap = Image.alpha_composite(im, ov).crop((395, 150, 865, 720)).convert('RGB')
    cap.save(B + 'eum_site.png')
    pic(sl, B + 'eum_site.png', 8.65, 2.1, w=5.0)
    text(sl, 8.65, 2.1 + 5.0 * cap.height / cap.width + 0.05, 5.0, 0.55, '토지이음 확인도면(1:2,400) 위 개략 표시\n노랑 = 서측(기존) · 회청 = 동측 · 빗금 = 소로 부지', size=11, color='mute')
    # right: schematic plan with dims
    s = 0.056; ox, oy = 15.2, 9.55
    road = Polygon(POLY_M['R'])
    plan_shape(sl, ox, oy, s, [(-25, -10), (0, -10), (0, 135), (-25, 135)], fill='line')        # 전포대로
    plan_shape(sl, ox, oy, s, [(-25, 127.4), (55, 127.4), (55, 135), (-25, 135)], fill='line')   # 서전로
    plan_shape(sl, ox, oy, s, [(-25, -10), (55, -10), (55, 0), (-25, 0)], fill='line')          # 남측
    plan_shape(sl, ox, oy, s, [(42.6, -10), (48.6, -10), (48.6, 135), (42.6, 135)], fill='line')  # 동측 이면도로
    plan_shape(sl, ox, oy, s, list(road.exterior.coords)[:-1], fill='pale', line='mute', dash=True)
    plan_shape(sl, ox, oy, s, POLY_M['W'], fill='beige', line='ink', lw=1.5)
    plan_shape(sl, ox, oy, s, POLY_M['E'], fill='blue', line='ink', lw=1.5)
    WB = Polygon(POLY_M['W']).buffer(-3, join_style=2); EB = Polygon(POLY_M['E']).buffer(-3, join_style=2)
    lab = lambda xm, ym, t, **kw: text(sl, ox + xm * s - 0.9, oy - ym * s - 0.16, 1.8, 0.32, t, align='c', anchor='m', **kw)
    lab(9, 100, '서측', size=12, bold=True)
    lab(31, 30, '동측', size=12, bold=True, color='bg')
    text(sl, ox - 25 * s, oy - 70 * s - 1.0, 25 * s, 2.0, '전포대로', size=11.5, color='ink2', align='c', anchor='m')
    text(sl, ox - 0.3, oy - 135 * s, 3.5, 0.3, '서전로 · 전포사거리', size=11.5, color='ink2')
    text(sl, ox, oy + 0.02, 3.0, 0.3, '전포대로224번길', size=11.5, color='ink2')
    text(sl, ox + 48.8 * s, oy - 70 * s - 0.15, 1.2, 0.3, '이면도로', size=11.5, color='ink2')
    text(sl, ox + 13 * s, oy - 58 * s, 1.0, 0.3, '소로3류', size=10.5, color='ink2')
    # dims
    line(sl, ox + 52 * s + 0.75, oy - 127.4 * s, ox + 52 * s + 0.75, oy, 'ink', 0.75)
    text(sl, ox + 52 * s + 0.8, oy - 64 * s - 0.15, 1.2, 0.3, '약 125m', size=11.5, bold=True)
    line(sl, ox, oy + 0.42, ox + 42.6 * s, oy + 0.42, 'ink', 0.75)
    text(sl, ox, oy + 0.45, 42.6 * s, 0.3, '약 42m', size=11.5, bold=True, align='c')
    # north arrow + scale
    freeform(sl, [(18.55, 2.15), (18.75, 2.6), (18.35, 2.6)], fill='ink')
    text(sl, 18.3, 2.62, 0.5, 0.3, 'N', size=12, bold=True, align='c')
    hline(sl, 17.6, 10.15, 20 * s, 'ink', 0.03); text(sl, 17.6, 9.85, 1.2, 0.3, '20m', size=10.5)
    text(sl, 13.95, 2.1, 3.6, 0.5, '점선 = 소로3류 부지 (대지 편입,\n1F는 공공 통로로 비움)', size=10.5, color='mute')
    footer(D, sl, '토지이음 토지이용계획열람(필지별 지목·면적, 2026-10-11 조회) · 필지 위치는 확인도면 정합으로 판별 · 형상·치수는 개략, 법적 효력은 토지대장 기준')


# ================================================================ 6. 환경 분석
def s_env():
    sl = D.slide()
    header(sl, 2, '향·소음·조망 — 남은 동측 1층이, 소음은 지하가, 조망은 옥상이 맡는다')
    mx, my, mw = 1.15, 2.1, 7.6
    W0, H0 = MAPS['size']; s = mw / W0; mh = H0 * s
    pic(sl, B + 'env_map.png', mx, my, w=mw)
    box(sl, mx, my, mw, mh, line=C['line'])
    P = lambda p: (mx + p[0] * s, my + p[1] * s)
    def tag(p, t, dx=0.08, dy=-0.14, w=1.9, fill='bg', color='ink', size=11, bold=True):
        x, y = P(p)
        text(sl, x + dx, y + dy, w, 0.3, t, size=size, bold=bold, color=color, fill=C.get(fill, fill), inset=0.04, anchor='m')
    sun = MAPS['sun']
    tag(sun['noon'], '남중 · 동지 31.4° / 하지 78.3°', dx=0.1, dy=-0.05, w=3.0)
    tag(sun['summer_rise'], '하지 일출 62°', dx=0.05, w=1.45)
    tag(sun['summer_set'], '하지 일몰 298°', dx=-1.5, w=1.45)
    tag(sun['winter_rise'], '동지 일출 118°', dx=0.05, w=1.45)
    tag(sun['winter_set'], '동지 일몰 242°', dx=-1.5, w=1.45)
    v = MAPS['view']
    tag(v['황령산'], '→ 황령산 1.5km', dx=-1.75, dy=-0.4, w=1.7, fill='ink', color='bg')
    tag(v['BIFC'], '↓ 문현 BIFC 약 1.2km', dx=0.08, dy=-0.15, w=2.0, fill='ink', color='bg')
    tag(v['서면 도심'], '← 서면 도심 0.6km', dx=0.0, dy=-0.42, w=1.8, fill='ink', color='bg')
    tag(v['시민공원'], '↖ 시민공원 1.6km', dx=-0.2, dy=-0.4, w=1.7, fill='ink', color='bg')
    for lv, p in MAPS['tall']:
        if lv >= 22:
            tag(p, f'{lv}F', dx=0.1, dy=-0.15, w=0.48, fill='ink2', color='bg', size=10)
    text(sl, mx + mw - 2.15, my + 0.1, 2.05, 0.55, '빗금 = 제3종일반주거지역\n(동측 이면도로에서 약 45m)', size=10, color='ink2', fill=C['bg'], inset=0.04)
    text(sl, mx + 0.1, my + 0.1, 2.3, 0.3, '붉은 띠 = 교통 소음원', size=10, color='red', fill=C['bg'], inset=0.04, bold=True)
    text(sl, mx, my + mh + 0.05, mw, 0.5, '태양 방위는 북위 35.157° 기준 계산 · 검은 면 = 15층 이상 건물(OSM 층수) · 점선 = 조망축', size=10.5, color='mute')
    # right table
    rx = 9.0; cw = [1.25, 2.85, 2.85, 2.85]
    table(sl, rx, 2.1, cw, [
        ['', '향 向', '소음 騷音', '조망 眺望'],
        ['현황', '블록 장축이 정남북. 서측 쐐기는 긴 면이 서·동향, 동측 삼각만 남측 도로에 약 40m 면한다.',
         '서측 전포대로(광로2류·6차로 내외)와 북측 서전로가 소음원. 동측 약 45m부터 제3종일반주거지역.',
         '정동 1.5km 황령산(427m), 남 1.2km 문현 BIFC, 서 0.6km 서면 도심. 동남동 260~400m에 29~30층 아파트.'],
        ['근거', '동지 남중 31.4°, 하지 78.3°. 서측 22층(80m)이 여름 17~19시 서향 일사를 일부 가린다. 동남동 30층 단지는 동지 오전 8~9시 그늘 가능(추정).',
         '용도지역은 토지이음, 도로 등급은 도시계획시설. 실측 dB는 아직 없음 → 현장 측정 예정(낮 15시·밤 21시).',
         '6F(약 22m)에서 황령산 정상 앙각 약 15.4°, 동남동 아파트 지붕 약 13~14° → 능선 윗부분만 보인다(추정).'],
        ['대응', '동측 1F 남단 근생을 남향 테라스로. 옥상 광장도 남향. 서측(전포대로) 면은 주차층 타공 차양, 6F 홀은 북측 천창·서측 차양.',
         '공연장은 지하 B1~B2. 6F 홀은 이중 차음 지붕. 진출입은 서전로·남측 도로로 내고 주거 쪽(동측)엔 내지 않는다. 동측 면 타공판·녹화로 전조등·소음 차단.',
         '6F 홀·테라스는 동측(황령산)으로 연다. 옥상 광장(약 29m)은 남향 — BIFC·도심 야경. 1F는 전포사거리 모퉁이로 연다.'],
    ], rh=1.0, size=11.5, rhs=[0.42, 1.25, 1.55, 1.65], aligns=['c', 'l', 'l', 'l'])
    yy = 2.1 + 0.42 + 1.25 + 1.55 + 1.65 + 0.2
    text(sl, rx, yy, 9.8, 0.38, '계절별 태양 (대지 위치 계산값)', size=14, bold=True)
    table(sl, rx, yy + 0.42, [1.6, 2.1, 3.0, 3.1], [
        ['', '남중고도', '일출 → 일몰 방위', '오후 3시 (고도 / 방위)'],
        ['동지 12/21', '31.4°', '118° → 242°', '20° / 219°'],
        ['춘·추분', '54.4°', '90° → 270°', '40° / 232°'],
        ['하지 6/21', '78.3°', '62° → 298°', '55° / 261°'],
    ], rh=0.36, size=12, aligns=['l', 'c', 'c', 'c'])
    footer(D, sl, '태양 위치: NOAA 근사식(북위 35.157°, 동경 129.066°) · 건물 층수·도로: OpenStreetMap · 용도지역: 토지이음 · 조망 앙각은 개략 추정, 현장 확인 필요')


# ================================================================ 7. 교통·동선
def s_access():
    sl = D.slide()
    header(sl, 2, '교통과 동선 — 두 역은 도보권, 차는 북에서 들고 남으로 난다')
    x = 1.15
    text(sl, x, 2.1, 4.6, 0.3, '전포역 (2호선) 8번 출구', size=13, color='mute')
    text(sl, x, 2.4, 4.6, 0.7, [[('약 529m', {'bold': True, 'size': 30}), ('  도보 약 9분', {'color': 'ink2'})]], size=14, anchor='m')
    text(sl, x, 3.15, 4.6, 0.3, '서면역 (1·2호선) 10번 출구', size=13, color='mute')
    text(sl, x, 3.45, 4.6, 0.7, [[('약 737m', {'bold': True, 'size': 30}), ('  도보 약 11분*', {'color': 'ink2'})]], size=14, anchor='m')
    text(sl, x, 4.15, 4.6, 0.3, '* 737m를 4km/h로 환산 · 거리는 기존 대지 중심 기준', size=10.5, color='mute')
    text(sl, x, 4.55, 4.6, 0.35, '가까운 정류장', size=14, bold=True)
    yy = 4.95
    for n, nm, dist in [('8', '전포사거리 05257 남행', '68m'), ('7', '전포사거리 (마을)', '140m'), ('9', '전포사거리 05357 북행', '146m'), ('6', 'NC서면점 05253', '242m')]:
        num(sl, x, yy + 0.02, 0.32, n, fill='beige', color='ink', size=11)
        text(sl, x + 0.42, yy, 3.3, 0.36, nm, size=12.5, anchor='m')
        text(sl, x + 3.6, yy, 1.0, 0.36, dist, size=12.5, bold=True, align='r', anchor='m')
        hline(sl, x, yy + 0.4, 4.6, 'line'); yy += 0.45
    text(sl, x, yy + 0.02, 4.6, 0.3, '외 11개소 · 부산버스정보시스템(BIMS)', size=10.5, color='mute')
    pic_crop(sl, IMG + 'image9.jpeg', x, yy + 0.4, 4.6, 2.15)
    text(sl, x, yy + 2.58, 4.6, 0.3, '전포사거리 남행 정류장에서 본 대지', size=10.5, color='mute')
    # map
    mx, my, mh = 6.0, 2.1, 8.1
    W0, H0 = MAPS['t_size']; s = mh / H0; mw = W0 * s
    pic(sl, B + 'transit_map.png', mx, my, h=mh)
    box(sl, mx, my, mw, mh, line=C['line'])
    P = lambda p: (mx + p[0] * s, my + p[1] * s)
    for k, p in MAPS['bus'].items():
        X, Y = P(p); num(sl, X - 0.15, Y - 0.15, 0.3, k, fill='beige', color='ink', size=10.5)
    for k, t, dx in (('jp8', '전포역 8번 출구 · 529m', 0.12), ('sm10', '서면역 10번 출구 · 737m', -0.3)):
        X, Y = P(MAPS['t'][k]); box(sl, X - 0.09, Y - 0.09, 0.18, 0.18, fill=C['ink'])
        text(sl, X + dx, Y + 0.12, 2.6, 0.3, t, size=11, bold=True, fill=C['bg'], inset=0.04)
    sx, sy = P(MAPS['t_site'])
    text(sl, sx + 0.35, sy - 0.15, 1.35, 0.3, '정동관', size=12, bold=True, color='bg', fill=C['ink'], align='c', anchor='m')
    # right: circulation
    rx = mx + mw + 0.3; rw = 18.85 - rx
    text(sl, rx, 2.1, rw, 0.4, '동선 계획', size=17, bold=True)
    bullets(sl, rx, 2.6, rw, [
        ('차량 — 북 진입 · 남 진출', '서전로에서 동측 북단 협소부(폭 약 8m)를 일방 진입로로 쓴다. 진출은 남측 전포대로224번길 → 전포대로. 램프는 동측 1F에서 위(2~5F)·아래(B1~B4)로.'),
        ('주거 쪽엔 내지 않는다', '동측 이면도로(건너 제3종일반주거)에는 진출입을 두지 않아 야간 전조등·공회전 소음을 막는다.'),
        ('보행 — 사거리 모퉁이로', '정류장 8·9와 전포대로변 보행은 서측 1F 서점·카페·로비로, 전포역 방향 보행은 남측에서 든다.'),
        ('관객 — 비 맞지 않는 길', '주차층 → 코어 → B1 공연장 로비. 지하·상층이 한 판이라 건너갈 길이 따로 필요 없다.'),
        ('하역 — 따로', '공연 물품은 서측 1F 남단 소로변 하역 → 화물용 승강기로 B2 무대. 일반 차량과 분리.'),
        ('사이 소로 — 지붕 덮인 가로', '1F 소로3류는 2F 아래(층고 약 7m) 지붕 덮인 가로가 된다. 보행 우선 공유가로(속도 저감·바닥 포장) 검토.'),
    ], size=12.5, gap=0.1, lh=1.12)
    footer(D, sl, '지도: © OpenStreetMap contributors · 노선: BIMS 2026-09-30 조회 · 정류장 위치는 개략 · 진출입 위치는 구청·경찰 협의 전 개념')


# ================================================================ 8. 사례
def s_cases():
    sl = D.slide()
    header(sl, 3, '참고 사례 — 어디에, 주차는 어떻게, 무엇을 담나')
    cols = [
        ('01 어디에', '헤르마 주차빌딩', '용인 죽전 카페거리 초입 · 조호건축 · 2010', 'image17.jpeg', 'image21.jpeg',
         ['카페거리 1층 상가 — 상가 절반 계속 입점, 임대료 최고 수준', '반투명 폴리카보네이트 파사드 — 밤엔 차량 불빛이 비침', '폭 14m 대지, 램프 6m → 3.3m로 줄여 상업 면적 확보'],
         '1F를 카페거리처럼 열고, 북단 일방 진입로 폭은 3.3m를 참고', '규모·프로그램(공연장 없음)은 근거로 쓰지 않는다'),
        ('02 주차는 어떻게', '평택 JS타워', '평택 · 대지 2,505㎡ · 모서리 깎인 사다리꼴', 'image22.jpeg', 'image24.jpeg',
         ['스킵플로어 — 반 층씩 오르내려 램프 면적을 줄인다', '볼륨 이원화 — 1F 근생은 층고를 반 층 높여 개방감', '알루미늄 타공판 밴드 — 단열·밀폐 없이 상층 주차부를 감쌈'],
         '2F 이상이 폭 약 42m 정형 바닥이 되어 스킵플로어 적용 가능. 기존 쐐기 대지에선 어려웠던 항목', '연면적·주차대수는 미확인'),
        ('03 무엇을 담나', '콘체르트하우스 블라이바흐', '독일 · Peter Haimerl · 2014', 'image26.jpeg', 'image28.jpeg',
         ['200석 대부분을 지하에 묻고 화강암 블록만 돌출', '지하 로비(바·코트룸·화장실)를 거쳐 홀로 — 로비가 완충층', '주름진 콘크리트 셸(최대 60cm)로 음향·차음 동시 해결'],
         '공연장을 지하로 내려 1F를 시민에게 돌려주고, 내려가는 동선을 공연 경험으로', '객석·면적 기준으로는 쓰지 않는다'),
    ]
    cw, gap = 5.75, 0.225
    for i, (tag, nm, sub, im1, im2, pts, app, lim) in enumerate(cols):
        x = 1.15 + i * (cw + gap)
        text(sl, x, 2.05, cw, 0.36, tag, size=13, bold=True, color='mute')
        text(sl, x, 2.38, cw, 0.5, nm, size=20, bold=True)
        text(sl, x, 2.86, cw, 0.3, sub, size=11, color='mute')
        pic_crop(sl, IMG + im1, x, 3.22, cw * 0.62, 2.55)
        pic_crop(sl, IMG + im2, x + cw * 0.62 + 0.06, 3.22, cw * 0.38 - 0.06, 2.55)
        yy = 5.9
        for j, p in enumerate(pts, 1):
            num(sl, x, yy + 0.04, 0.3, f'{j}', fill='mute', size=10.5)
            text(sl, x + 0.38, yy, cw - 0.38, 0.62, p, size=12.5, spacing=1.0)
            yy += 0.66
        text(sl, x, yy + 0.05, cw, 1.05, [[('전포동 적용  ', {'bold': True, 'color': 'beige'}), (app, {'color': 'bg'})]], size=12.5, fill=C['ink'], inset=0.12, spacing=1.05)
        text(sl, x, yy + 1.18, cw, 0.5, '한계 · ' + lim, size=11, color='mute')
    footer(D, sl, '서울경제 2016.02.26 · ArchDaily · 언폴드 · Architect Magazine · Yatzer · Divisare')


s_toc(); s_overview(); s_concept(); s_site(); s_env(); s_access(); s_cases()
exec(open(B + 'build2.py').read())
D.save(B + 'out.pptx')
print('saved', D.n)
