s = open('build_ds.js', encoding='utf8').read()
n = 0
def rep(a, b):
    global s, n
    if a not in s:
        print('MISSING:', a[:80]); return
    s = s.replace(a, b, 1); n += 1

# new takeaway: conclusion panel (navy tab + red conclusion + black evidence line)
a = s.index("function takeaway(s, text, x, y, w, o = {}) {"); b = s.index("function tag(s, text, x, y) {")
s = s[:a] + '''function takeaway(s, text, x, y, w, o = {}) {
  const h = o.h || (o.sub ? 0.7 : 0.5);
  R(s, x, y, w, h, PANEL);
  s.addText('결론', { x, y, w: 0.78, h, fontFace: F, fontSize: 12, bold: true, color: 'FFFFFF', fill: { color: NAVY }, align: 'center', valign: 'middle', margin: 0, isTextBox: true });
  const runs = [{ text: '→ ' + text, options: { bold: true, color: SIGNAL, fontSize: o.size || 13.5, breakLine: !!o.sub } }];
  if (o.sub) runs.push({ text: o.sub, options: { color: INK, fontSize: 10.5 } });
  T(s, runs, x + 0.95, y + 0.04, w - 1.1, h - 0.08, { valign: 'middle', lineSpacingMultiple: 1.05 });
}
''' + s[b:]; n += 1

# 1 사업 배경
rep("takeaway(s, '소규모 필지에 저층 점포가 밀집해 부설주차장을 확보할 수 없음. 상권 한가운데 거점형 주차장이 필요함', x2, 5.95, w2, { h: 0.8, size: 13 });",
    "takeaway(s, '소규모 필지에 점포가 밀집해 부설주차장이 어려워, 상권 한가운데 거점형 주차장이 필요함', x2, 5.85, w2, { h: 0.98, size: 13, sub: '부산진구 확보율 118.5%(기준 130%) · 대지 반경 500m 공영주차장 27면' });")
# 2 입지: tighten cards upward
rep("const y = 1.37 + i * 1.05;\n    R(s, x2, y, w2, 0.96, SOFT);", "const y = 1.37 + i * 0.98;\n    R(s, x2, y, w2, 0.9, SOFT);")
rep("barHeading(s, '접근 계획', x2, 4.6);\n  labeledPanel(s, x2, 4.95, 3.38,", "barHeading(s, '접근 계획', x2, 4.38);\n  labeledPanel(s, x2, 4.72, 3.38,")
rep("labeledPanel(s, x2 + 3.5, 4.95, 3.38,", "labeledPanel(s, x2 + 3.5, 4.72, 3.38,")
rep("takeaway(s, '두 역 도보권과 카페거리 사이, 반경 내 공영주차장이 거의 없는 곳임', x2, 6.35, w2, { h: 0.5, size: 13 });",
    "takeaway(s, '두 역 도보권과 카페거리 사이, 공영주차장이 거의 없어 거점형 입지로 적합함', x2, 5.95, w2, { h: 0.9, size: 13, sub: '서면역 737m · 전포역 529m, 반경 500m 공영 27면 · 1km 약 415면' });")
# 3 일조
rep("const hm = imgH(s, 'shadow_hours.png', M, y2, 2.2);\n  cap(s, '동지 09~15시 그림자 누적 시간', M, y2 + 2.22, hm, { align: 'left', fontSize: 8 });",
    "const hm = imgH(s, 'shadow_hours.png', M, y2, 1.85);\n  cap(s, '동지 09~15시 그림자 누적 시간', M, y2 + 1.87, hm, { align: 'left', fontSize: 8 });")
rep("takeaway(s, '서·동 면은 스크린으로, 광장과 근생은 남쪽에 둠', M, 6.45, w1 + 4, { h: 0.45, size: 13 });",
    "takeaway(s, '서·동 면은 목재 슬랫으로 일사를 거르고, 광장과 근생은 남쪽에 둠', M, 6.2, w1, { h: 0.72, size: 13, sub: '직사 서측 4.3h(오후) · 남측 8.6h(동지) · 옥상 광장은 동지 9~15시 그림자 영향 없음' });")
# 4 소음
rep("x: x2, y: 3.65, w: w2, h: 2.6, barDir: 'bar', chartColors: [NAVY, NAVY, D2, D2, SLATE]", "x: x2, y: 3.65, w: w2, h: 2.4, barDir: 'bar', chartColors: [NAVY, NAVY, D2, D2, SLATE]")
rep("takeaway(s, '소음이 큰 실은 지하와 최상층 안쪽에 둠', x2, 6.4, 7.98, { h: 0.45, size: 13 });",
    "takeaway(s, '소음이 큰 실은 지하와 최상층 안쪽에 두고, 서·북 도로변 면은 닫음', M, 6.2, CW, { h: 0.72, size: 13, sub: '서·북 도로변 추정 72~76dB(A, 가정) · 동측 주거 경계 약 67dB(A) · 전포동 실측으로 교체 필요' });")
# 5 볼륨
rep("], M, y, CW, [2.6, 4.0, 5.73], { size: 11.5, rowH: 0.44 });", "], M, y, CW, [2.6, 4.0, 5.73], { size: 11.5, rowH: 0.4 });")
rep("takeaway(s, '필지를 채우되 법정 이격과 건폐율은 두 끝을 비워 맞추고, 비운 자리가 건물의 얼굴이 됨', M, 6.4, CW, { h: 0.5, size: 13 });",
    "takeaway(s, '필지를 채우되 법정 이격과 건폐율은 두 끝을 비워 맞추고, 비운 자리가 건물의 얼굴이 됨', M, 6.25, CW, { h: 0.68, size: 13, sub: '건폐율 87.1%(상한 90%) · 비운 끝 코어 동측 약 352㎡ + 서측 약 158㎡ · 북·남 3m 이격' });")
# 6 투시도
rep("takeaway(s, take, M, 6.2, CW, { h: 0.5, size: 13 });", "takeaway(s, take, M, 6.05, CW, { h: 0.82, size: 13, sub: sub2 });")
rep("function renderSlide(num, title, sub, big, bigLabel, smalls, take, notes) {", "function renderSlide(num, title, sub, big, bigLabel, smalls, take, notes, sub2) {")
rep("'停은 목재 슬랫 스크린으로 차분하게, 動은 검은 순환 계단과 켜진 홀로 드러냄',\n  '렌더는 Blender 5.2 Cycles(192 샘플, OpenImageDenoise)이며 외피 슬랫 재질은 Poly Haven dark_wood 텍스처를 사용함. 슬랫 폭 0.15m, 피치 0.24m는 가정값임.');",
    "'停은 목재 슬랫 스크린으로 차분하게, 動은 검은 순환 계단과 켜진 홀로 드러냄',\n  '렌더는 Blender 5.2 Cycles(192 샘플, OpenImageDenoise)이며 외피 슬랫 재질은 Poly Haven dark_wood 텍스처를 사용함. 슬랫 폭 0.15m, 피치 0.24m는 가정값임.',\n  '주차층 목재 슬랫(피치 0.24m 가정) · 끝 코어 순환 계단은 검은 도장 강재 · 6F 가변홀 층고 8m');")
rep("'옥상 광장과 소로를 한 건물 안에서 보행과 차량으로 나눔',\n  '소로 시점은 황혼 조도로 렌더함. 사람과 차량은 단순 모형이며 실제 계획 인원과 무관함.');",
    "'옥상 광장과 소로를 한 건물 안에서 보행과 차량으로 나눔',\n  '소로 시점은 황혼 조도로 렌더함. 차량은 단순 모형이며 실제 계획과 무관함.',\n  '옥상 광장 약 1,380㎡(+21.1m, 5F 지붕) · 소로는 남→북 일방, 2층 바닥이 덮은 높이 7m 통로');")
# 7 실별 면적
rep("], M, 1.35, 7.55, [0.8, 5.65, 1.1], { size: 10.5, aligns: ['left', 'left', 'right'], boldRows: [8], rowH: 0.5 });",
    "], M, 1.35, 7.55, [0.8, 5.65, 1.1], { size: 10.5, aligns: ['left', 'left', 'right'], boldRows: [8], rowH: 0.42 });")
rep("takeaway(s, '건축면적 4,322.1㎡ · 건폐율 87.1% · 용적률 481.9%(지하 제외)', M, 6.3, 7.55, { h: 0.45, size: 12.5 });",
    "takeaway(s, '주차 비율 75.62%로 주차전용건축물 요건을 충족하고 건폐율 87.1%로 맞춤', M, 5.85, 7.55, { h: 0.95, size: 13, sub: '건축면적 4,322.1㎡ · 용적률 481.9%(지하 제외, 특례 상한 1,500%) · 주차 70% 이상 요건' });")
# 8 동선
rep("takeaway(s, '차량은 소로에 모으고, 보행은 1층 외곽 중심으로 분리함(소로 횡단 1곳)', x2, 5.0, w2, { h: 0.5, size: 13 });",
    "takeaway(s, '차량은 소로에 모으고, 보행은 1층 외곽 중심으로 분리함(소로 횡단 1곳)', x2, 4.95, w2, { h: 0.72, size: 12.5, sub: '소로 남→북 일방 · 입구와 출구 분리(400대 초과) · 하역 150㎡ · 이륜차 200㎡는 동측' });")
# 9 법규
rep("takeaway(s, '구조 · 방재는 제안이며, 설계 단계에서 작도와 계산으로 검증함', M, 6.45, CW, { h: 0.45, size: 13 });",
    "takeaway(s, '구조 · 방재는 확정 설계가 아닌 제안이며, 설계 단계에서 작도와 계산으로 검증함', M, 6.1, CW, { h: 0.78, size: 13, sub: '조건부 3건: 노외주차장 출입구(교차로 5m · 정류장 10m) · 주차장 구조(램프 17%) · 피난(보행거리 50m, 지하 공연장 30m)' });")
open('build_ds.js', 'w', encoding='utf8').write(s)
print('replacements', n)
