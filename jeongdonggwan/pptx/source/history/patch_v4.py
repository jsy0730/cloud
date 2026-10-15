s = open('build_ds.js', encoding='utf8').read()
n = 0
def cut(start_marker, end_marker, new):
    global s, n
    a = s.index(start_marker); a = s.rindex("// =====", 0, a)
    e = s.index(end_marker); e = s.rindex("// =====", 0, e)
    s = s[:a] + new + s[e:]; n += 1

# ---- concept: day / night
concept = '''// =====================================================================
// 09-10 콘셉트 · 낮 / 밤
function conceptSlide(night) {
  sec(1);
  const s = pres.addSlide({ masterName: 'GS', sectionTitle: SEC[1] }); PAGE += 1;
  const bg = night ? '0A1122' : PANEL, ink = night ? 'F2F4F8' : INK, sub = night ? 'A7B0C2' : MUTED, dim = night ? '3D4864' : 'C9CED8';
  const key = night ? GOLD : NAVY, nav = night ? '8FB0EC' : NAVY;
  R(s, 0, 0, SW, 7.5, bg);
  s.addImage({ path: find(night ? 'concept_night.jpg' : 'concept_day.jpg'), x: SW - 4.7, y: 0, w: 4.7, h: 7.5 });
  // glyphs: the half of the day in focus is lit
  [['停', !night], ['動', night], ['館', false]].forEach(([c, on], i) =>
    T(s, c, 0.75, 0.45 + i * 2.2, 2.0, 2.15, { fontFace: SERIF, fontSize: 110, bold: true, valign: 'middle', align: 'center', color: on ? key : dim }));
  T(s, ['정', '동', '관'].map((c, i) => ({ text: c, options: { breakLine: i < 2 } })), 2.9, 0.9, 0.7, 5.5, { fontSize: 32, bold: true, color: sub, lineSpacingMultiple: 2.0 });
  s.addText(night ? '밤 · 動' : '낮 · 停', { x: 3.9, y: 0.75, w: 1.5, h: 0.4, fontFace: F, fontSize: 14, bold: true, color: night ? '0A1122' : 'FFFFFF', fill: { color: night ? GOLD : NAVY }, align: 'center', valign: 'middle', margin: 0, isTextBox: true });
  const hi = { bold: true, color: key };
  T(s, [
    { text: '‘정동관’은 차가 멈추는 주차층(停)과 사람이 움직이는 계단 · 홀 · 광장(動)을 한 건물 안에 두어, ' },
    { text: '낮에는 상권의 차를 받고', options: night ? {} : hi }, { text: ' ' },
    { text: '밤에는 공연과 옥상 광장이 켜지는', options: night ? hi : {} }, { text: ' 건물을 뜻함' }],
    3.9, 1.5, 4.6, 2.7, { fontFace: SERIF, bold: true, fontSize: 17, lineSpacingMultiple: 1.45, align: 'center', valign: 'middle', color: ink });
  T(s, '停과 動이 교대하는 하루', 3.9, 4.5, 4.6, 0.4, { fontSize: 15, bold: true, align: 'center', color: ink });
  T(s, '차가 멈추는 주차층은 목재 슬랫 스크린으로 차분히 감싸고, 사람이 움직이는 순환 계단 · 6F 가변홀 · 옥상 광장은 검은 계단과 켜진 홀로 드러냄', 3.9, 4.95, 4.6, 1.2, { fontSize: 11, color: sub, align: 'center', lineSpacingMultiple: 1.3 });
  T(s, '停動館', M, 7.0, 1.1, 0.4, { fontFace: SERIF, bold: true, fontSize: 16, color: nav, valign: 'middle' });
  T(s, '담당자 정성윤 · ' + String(PAGE).padStart(2, '0'), 3.9, 7.06, 4.6, 0.3, { fontSize: 8, color: sub, align: 'right' });
  s.addNotes(night ? '밤 장면: 같은 내용, 야간 렌더(Blender Cycles)와 공설기 Night 토큰(#0a1122 · 금색 select)으로 낮과 대비함.' : '낮 장면: 같은 내용, 주간 렌더(Blender Cycles)와 공설기 Deck 토큰으로 구성함.');
}
conceptSlide(false);
conceptSlide(true);

'''
cut("// 09 콘셉트", "// case column", concept)

# ---- program figure (replace FloorStack shapes)
a = s.index("  // FloorStack\n"); e = s.index("  const x2 = 6.7, w2 = 6.13;\n  barHeading(s, '용도별 위치와 선정 근거'")
s = s[:a] + """  barHeading(s, '층별 용도 구성', M, 1.0);
  const hp = imgW(s, 'program_stack.png', M, 1.4, 6.0);
  T(s, '지상 23,923.7㎡ + 지하 19,700.0㎡ = 연면적 43,623.7㎡', M, 1.4 + hp + 0.1, 6.0, 0.3, { fontSize: 10, bold: true });
""" + s[e:]; n += 1

# ---- sections
a = s.index("  const wa = 8.45;\n  const ha = imgW(s, 'secA.jpg'")
e = s.index("// =====", a)
e = s.rindex("}\n", a, e)
new = """  const wa = 8.7;
  const ha = imgW(s, 'secA.png', M, 1.0, wa);
  const hb = imgW(s, 'secB.png', 9.45, 1.0, 2.75);
  imgW(s, 'keyplan.jpg', 12.3, 1.0, 0.55);
  cap(s, '단면선', 12.2, 2.0, 0.65, { fontSize: 8 });
  const y = Math.max(1.0 + ha, 1.0 + hb) + 0.3;
  labeledPanel(s, M, y, 6.05, [{ label: 'A 종단면', items: [
    { title: '① 공연장 200석 · ② 옥상 광장 · ③ 6F 가변홀 · ④ 개방 순환 계단 · ⑤ 특별피난계단', lines: ['두 끝은 지상에서 비어 있고 지하는 특별피난계단', '지하 공연장은 선큰 마당으로 빛이 닿음'], wrap: 1.5 }] }], { size: 10.5, minH: 1.55 });
  labeledPanel(s, M + 6.28, y, 6.05, [{ label: 'B 횡단면', items: [
    { title: '⑥ 서측 판 7.0 · 10.3 · 13.6m, 동측 판 +1.65m', lines: ['서 · 동 판이 소로 위에서 반 층 엇갈려 램프 길이를 줄임', '지하 공연장은 박스인박스와 방진 바닥으로 차량 진동 차단을 제안'] }] }], { size: 10.5, minH: 1.55 });
"""
s = s[:a] + new + s[e:]; n += 1
open('build_ds.js', 'w', encoding='utf8').write(s)
print('patched', n)
