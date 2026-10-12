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


