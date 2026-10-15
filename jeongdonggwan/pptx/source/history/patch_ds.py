s = open('build_ds.js', encoding='utf8').read()


def rep(a, b):
    global s
    if a not in s:
        print('MISSING:', a[:80])
        return
    s = s.replace(a, b, 1)


# labeledPanel: optional fixed height
rep("    h += 0.06;\n    R(s, x, yy, w, h, SOFT);", "    h += 0.06;\n    if (o.minH) h = Math.max(h, o.minH);\n    R(s, x, yy, w, h, SOFT);")
# contents spacing
rep("['INTRODUCTION', ['사업 배경 · 사업 개요'], 1.0],", "['INTRODUCTION', ['사업 배경 · 사업 개요'], 1.1],")
rep("'볼륨 도출 · 최종안 · 투시도'], 2.2],", "'볼륨 도출 · 최종안 · 투시도'], 2.35],")
rep("'확인할 것'], 4.6],", "'확인할 것'], 4.45],")
# slide 4
rep("const h = imgW(s, 'site_eum.jpg', M, 1.0, 3.95);", "const h = imgW(s, 'site_eum.jpg', M, 1.0, 4.15);")
rep("cap(s, '토지이용계획 확인도면 · 필지군 표시(개략)', M, 1.0 + h + 0.04, 3.95);", "cap(s, '토지이용계획 확인도면 · 필지군 표시(개략)', M, 1.0 + h + 0.04, 4.15);")
rep("const x2 = 4.8, w2 = 8.03;\n  barHeading(s, '대지 개요', x2, 1.0);", "const x2 = 4.95, w2 = 7.88;\n  barHeading(s, '대지 개요', x2, 1.0);")
rep("], x2, 1.35, w2, [1.3, 0.7, 1.1, 4.93], { size: 10.5, aligns: ['left', 'right', 'right', 'left'], boldRows: [3] });",
    "], x2, 1.35, w2, [1.3, 0.7, 1.1, 4.78], { size: 11.5, aligns: ['left', 'right', 'right', 'left'], boldRows: [3], rowH: 0.36 });")
rep("barHeading(s, '배치 조건', x2, 3.15);\n  labeledPanel(s, x2, 3.5, 3.9,", "barHeading(s, '배치 조건', x2, 3.35);\n  labeledPanel(s, x2, 3.72, 3.8,")
rep("], { size: 10.5 });\n  labeledPanel(s, x2 + 4.03, 3.5, 4.0,", "], { size: 11, minH: 2.3 });\n  labeledPanel(s, x2 + 3.93, 3.72, 3.95,")
rep("] }], { size: 10.5 });\n  noteBox(s, x2, 6.2, w2, 0.55, '확인할 것',", "] }], { size: 11, minH: 2.3 });\n  noteBox(s, x2, 6.2, w2, 0.55, '확인할 것',")
# slide 5
rep("lines: ['끝 코어 2곳(개방 순환 계단 + 승강기)', '동측 주거 쪽 차량 진출입 없음'] }] }], { size: 10 });\n}",
    "lines: ['끝 코어 2곳(개방 순환 계단 + 승강기)', '동측 주거 쪽 차량 진출입 없음'] }] }], { size: 10 });\n  takeaway(s, '두 역 도보권과 카페거리 사이, 공영주차장이 비어 있는 곳임', x2, 6.35, w2, { h: 0.5, size: 13 });\n}")
# slide 6 lower part
a = s.index("  const y2 = 1.0 + h1 + 0.4;\n  table(s, ['면', '직사 동지'")
b = s.index("  const x2 = 8.85, w2 = 3.98;")
new6 = """  const y2 = 1.0 + h1 + 0.45;
  const hm = imgH(s, 'shadow_hours.png', M, y2, 2.2);
  cap(s, '동지 09~15시 그림자 누적 시간', M, y2 + 2.22, hm, { align: 'left', fontSize: 8 });
  table(s, ['면', '직사 동지', '직사 하지', '관찰'], [
    ['서측 · 전포대로', '4.3h (오후)', '6.7h', '서향 일사와 도로 소음이 함께 닿는 면'],
    ['동측 · 이면도로', '4.3h (오전)', '6.8h', '동지 15시경에야 주거 경계에 이름'],
    ['남측 · 224번길', '8.6h', '6.9h', '동지 고도 31.4°로 깊이 들어옴'],
    ['북측 · 서전로', '0h', '새벽·저녁', '직사 없이 확산광, 그림자는 도로 쪽'],
  ], M + hm + 0.2, y2, w1 - hm - 0.2, [1.45, 0.95, 0.9, w1 - hm - 0.2 - 3.3], { size: 10, aligns: ['left', 'center', 'center', 'left'], rowH: 0.42 });
"""
s = s[:a] + new6 + s[b:]
rep("takeaway(s, '서·동 면은 스크린으로, 광장과 근생은 남쪽에 둠', M, 6.4, w1, { h: 0.45, size: 13 });",
    "takeaway(s, '서·동 면은 스크린으로, 광장과 근생은 남쪽에 둠', M, 6.45, w1 + 4, { h: 0.45, size: 13 });")
# slide 7
rep("const wm = 4.35;\n  const hm = imgW(s, 'noise_map.png', M, 1.0, wm);", "const wm = 3.95;\n  const hm = imgW(s, 'noise_map.png', M, 1.0, wm);")
rep("const py = 1.0 + hm + 0.32;\n  img(s, 'n_p1.jpg', M, py, 1.4, 1.2); img(s, 'n_p2.jpg', M + 1.475, py, 1.4, 1.2); img(s, 'n_p3.jpg', M + 2.95, py, 1.4, 1.2);",
    "const py = 1.0 + hm + 0.3;\n  img(s, 'n_p1.jpg', M, py, 1.27, 1.1); img(s, 'n_p2.jpg', M + 1.34, py, 1.27, 1.1); img(s, 'n_p3.jpg', M + 2.68, py, 1.27, 1.1);")
rep("'「환경정책기본법 시행령」 별표(원문 대조 필요), OpenStreetMap contributors, 현장 답사(2026.9) · 전포동 측정값 없음, 그림의 dB은 개략 추정(실측 필요) · 사진: Petr Meissner, CC BY 2.0(Wikimedia Commons)',",
    "'「환경정책기본법 시행령」 별표, OpenStreetMap contributors, 현장 답사(2026.9) · 전포동 측정값 없음, dB은 개략 추정 · 사진: Petr Meissner, CC BY 2.0',")
rep("const x2 = 5.15, w2 = 3.75;\n  barHeading(s, '소음 환경기준 (dB)', x2, 1.0);", "const x2 = 4.85, w2 = 4.05;\n  barHeading(s, '소음 환경기준 (dB)', x2, 1.0);")
rep("], x2, 1.35, w2, [1.5, 0.5, 0.5, 1.25], { size: 10, aligns: ['left', 'center', 'center', 'left'] });",
    "], x2, 1.35, w2, [1.6, 0.55, 0.55, 1.35], { size: 10.5, aligns: ['left', 'center', 'center', 'left'], rowH: 0.34 });")
rep("barHeading(s, '면별 주간 추정치 (dB(A), 가정)', x2, 3.15);", "barHeading(s, '면별 주간 추정치 (dB(A), 가정)', x2, 3.3);")
rep("x: x2, y: 3.5, w: w2, h: 2.55, barDir: 'bar', chartColors: [NAVY, NAVY, D2, D2, SLATE]", "x: x2, y: 3.65, w: w2, h: 2.6, barDir: 'bar', chartColors: [NAVY, NAVY, D2, D2, SLATE]")
rep("const x3 = 9.1, w3 = 3.73;", "const x3 = 9.15, w3 = 3.68;")
rep("takeaway(s, '소음이 큰 실은 지하와 최상층 안쪽에 둠', x2, 6.3, 7.7, { h: 0.45, size: 13 });", "takeaway(s, '소음이 큰 실은 지하와 최상층 안쪽에 둠', x2, 6.4, 7.98, { h: 0.45, size: 13 });")
# slide 8
a = s.index("  const h = imgW(s, 'view_profile.png', M, 1.0, CW);")
b = s.index("// =====================================================================\n// 09 콘셉트")
new8 = """  const h = imgW(s, 'view_profile.png', M, 1.0, CW);
  cap(s, '스카이라인 앙각 분석 · 옥상 광장과 1층 가로, 주변 건물과 정동관 매스 포함', M, 1.0 + h, CW);
  const y2 = 1.0 + h + 0.3;
  img(s, 'view_jeonpo.jpg', M, y2, 3.75, 1.74);
  img(s, 'view_roof.jpg', M + 3.82, y2, 3.0, 1.74);
  cap(s, 'BIFC · 서면 일대 조망', M, y2 + 1.76, 3.75, { align: 'left' });
  cap(s, '옥상 광장 시뮬레이션(개념 모델)', M + 3.82, y2 + 1.76, 3.0, { align: 'left' });
  const x2 = 7.6, w2 = 5.23;
  table(s, ['대상', '방위 · 거리', '앙각', '옥상'], [
    ['황령산 정상 427m', '동 87° · 1.47km', '15.1°', { t: '상단만 보임', o: { color: SIGNAL, bold: true } }],
    ['BIFC 289m', '남 184° · 1.15km', '12.6°', { t: '보임', o: { bold: true, color: NAVY } }],
    ['서면 도심', '서 · 약 0.6km', '고층군', { t: '보임', o: { bold: true, color: NAVY } }],
  ], x2, y2, w2, [1.6, 1.6, 0.8, 1.23], { size: 10, rowH: 0.3 });
  labeledPanel(s, x2, y2 + 1.3, w2, [{ label: '관찰', items: [
    { title: '1층 가로 · 옥상 광장', lines: ['1층: 자체 매스가 동쪽을 가려 황령산이 보이지 않음', '옥상: 열린 각도 약 128°, 동남동 29~30층 아파트 위로 능선 상단이 걸침'], wrap: 1 },
  ] }], { size: 9.5, lineH: 0.19 });
}

"""
s = s[:a] + new8 + s[b:]
rep("'OSM 좌표, 「위키백과」 황령산 427m · BIFC 289m, 본 시안 매스 · 앙각은 지면 8m 가정, 능선 형상은 반영 안 됨 · 사진: Christian Bolz, CC BY-SA 4.0(Wikimedia Commons)',",
    "'OSM 좌표, 「위키백과」 황령산 427m · BIFC 289m, 본 시안 매스 · 앙각은 지면 8m 가정 · 사진: Christian Bolz, CC BY-SA 4.0',")
# slide 9
rep("s.addImage({ path: find('concept_grey.jpg'), x: SW - 6.4, y: 0, w: 6.4, h: 7.5 });\n  s.addShape(pres.shapes.RECTANGLE, { x: SW - 6.4, y: 0, w: 6.4, h: 7.5,",
    "s.addImage({ path: find('concept_grey.jpg'), x: SW - 4.7, y: 0, w: 4.7, h: 7.5 });\n  s.addShape(pres.shapes.RECTANGLE, { x: SW - 4.7, y: 0, w: 4.7, h: 7.5,")
rep("4.0, 1.6, 5.1, 2.4, { fontFace: SERIF, bold: true, fontSize: 17,", "3.9, 1.5, 4.6, 2.7, { fontFace: SERIF, bold: true, fontSize: 17,")
rep("T(s, '停과 動이 교대하는 하루', 4.0, 4.5, 5.1, 0.4,", "T(s, '停과 動이 교대하는 하루', 3.9, 4.5, 4.6, 0.4,")
rep("붉은 계단과 켜진 홀로 드러냄', 4.0, 4.95, 5.1, 1.0,", "붉은 계단과 켜진 홀로 드러냄', 3.9, 4.95, 4.6, 1.2,")
# case column
rep("T(s, facts, x, y + 3.22, w, 1.15, { fontSize: 10, lineSpacingMultiple: 1.05 });\n  R(s, x, y + 4.4, w, 0.72, PDARK);\n  T(s, '정동관 적용', x + 0.15, y + 4.4, 1.15, 0.72, { fontSize: 10.5, bold: true, color: 'FFFFFF', valign: 'middle' });\n  T(s, c.apply, x + 1.3, y + 4.4, w - 1.45, 0.72, { fontSize: 10.5, color: 'FFFFFF', valign: 'middle' });",
    "T(s, facts, x, y + 3.25, w, 1.5, { fontSize: 10.5, lineSpacingMultiple: 1.08 });\n  R(s, x, y + 4.85, w, 0.8, PDARK);\n  T(s, '정동관 적용', x + 0.15, y + 4.85, 1.2, 0.8, { fontSize: 11, bold: true, color: GOLD, valign: 'middle' });\n  T(s, c.apply, x + 1.4, y + 4.85, w - 1.55, 0.8, { fontSize: 11, color: 'FFFFFF', valign: 'middle' });")
rep("'ArchDaily · JOHO Architecture(헤르마 주차빌딩, 사진 Namgoong Sun · Jeonghoon Lee), arch2o, 서울경제 2016.02.26, 팀 조사(2026.9) · JS타워 사진 및 다이어그램은 팀 작성 · 규모·객석 수는 출처마다 달라 근거로 쓰지 않음');",
    "'ArchDaily · JOHO Architecture(헤르마 주차빌딩, 사진 Namgoong Sun · Jeonghoon Lee), arch2o, 서울경제 2016.02.26, 팀 조사(2026.9) · 다이어그램은 팀 작성');")
rep("'ArchDaily · de Jong Gortemaker Algra + MODULO(Saint-Luc, 사진 Lieven Van Landschoot), JAJA Architects(Park ’n’ Play, 사진 Rasmus Hjortshøj / COAST), Lonely Planet, 팀 조사(2026.9)');",
    "'ArchDaily · dJGA + MODULO(Saint-Luc, 사진 Lieven Van Landschoot), JAJA Architects(Park ’n’ Play, 사진 Rasmus Hjortshøj / COAST), 팀 조사(2026.9)');")
rep("'ArchDaily · peter haimerl.architektur(Concert Hall Blaibach, 도면 · 사진 NAARO), Herzog & de Meuron(1111 Lincoln Road), 사진: Phillip Pessar, CC BY 2.0(Wikimedia Commons), 팀 조사(2026.9)');",
    "'ArchDaily · peter haimerl.architektur(Blaibach, 도면 · 사진 NAARO), Herzog & de Meuron(1111 Lincoln Road, 사진 Phillip Pessar, CC BY 2.0), 팀 조사(2026.9)');")
# slide 13
rep("], M, y, CW, [2.5, 4.0, 5.83], { size: 10.5 });", "], M, y, CW, [2.6, 4.0, 5.73], { size: 11.5, rowH: 0.44 });")
rep("takeaway(s, '필지를 채우되 법정 이격과 건폐율은 두 끝을 비워 맞추고, 비운 자리가 건물의 얼굴이 됨', M, 6.35, CW, { h: 0.5, size: 13 });",
    "takeaway(s, '필지를 채우되 법정 이격과 건폐율은 두 끝을 비워 맞추고, 비운 자리가 건물의 얼굴이 됨', M, 6.4, CW, { h: 0.5, size: 13 });")
# slide 15
rep("w: Math.min(5.8, label.length * 0.145 + 0.3)", "w: Math.min(5.8, label.length * 0.118 + 0.35)")
# slide 17
rep("{ size: 10 });\n  labeledPanel(s, M + 6.28, y, 6.05, [{ label: 'B 횡단면'", "{ size: 10.5, minH: 1.5 });\n  labeledPanel(s, M + 6.28, y, 6.05, [{ label: 'B 횡단면'")
rep("지하 공연장은 박스인박스와 방진 바닥으로 차량 진동 차단을 제안'] }] }], { size: 10 });", "지하 공연장은 박스인박스와 방진 바닥으로 차량 진동 차단을 제안'] }] }], { size: 10.5, minH: 1.5 });")
# slide 18
rep("], M, 1.35, 7.55, [0.75, 5.75, 1.05], { size: 9.5, aligns: ['left', 'left', 'right'], boldRows: [8] });",
    "], M, 1.35, 7.55, [0.8, 5.65, 1.1], { size: 10.5, aligns: ['left', 'left', 'right'], boldRows: [8], rowH: 0.5 });")
# slide 19
rep("noteBox(s, x2, 5.45, w2, 0.7, '확인할 것',", "takeaway(s, '차량은 소로에 모으고, 보행은 1층 외곽으로 분리함', x2, 5.0, w2, { h: 0.5, size: 13 });\n  noteBox(s, x2, 5.75, w2, 0.7, '확인할 것',")
# slide 20
rep("], M, 1.0, CW, [2.0, 2.6, 4.0, 2.2, 1.53], { size: 9.5 });\n  const y = 4.35;", "], M, 1.0, CW, [2.1, 2.7, 3.9, 2.2, 1.43], { size: 10.5, rowH: 0.5 });\n  const y = 4.75;")
rep("takeaway(s, '구조 · 방재는 제안이며, 설계 단계에서 작도와 계산으로 검증함', M, 6.35, CW, { h: 0.45, size: 13 });",
    "takeaway(s, '구조 · 방재는 제안이며, 설계 단계에서 작도와 계산으로 검증함', M, 6.45, CW, { h: 0.45, size: 13 });")
# slide 21
rep("], M, 1.0, 8.2, [0.45, 4.45, 3.3], { size: 10, aligns: ['center', 'left', 'left'] });\n  noteBox(s, M, 5.15, 8.2, 0.9,",
    "], M, 1.0, 8.2, [0.45, 4.45, 3.3], { size: 11, aligns: ['center', 'left', 'left'], rowH: 0.55 });\n  noteBox(s, M, 5.6, 8.2, 0.9,")
rep("확정은 법규 원문 확인과 설계 단계의 작도에서 이뤄짐'", "확정은 법규 원문 확인과 작도에서 이뤄짐'")
open('build_ds.js', 'w', encoding='utf8').write(s)
print('patched')
