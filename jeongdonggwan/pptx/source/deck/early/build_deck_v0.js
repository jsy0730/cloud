// 전포 정동관 — PPTX builder (21 slides)
const pptxgen = require('pptxgenjs');
const path = require('path');
const fs = require('fs');
const DIMS = JSON.parse(fs.readFileSync(path.join(__dirname, 'dims.json'), 'utf8'));
const IMG = (n) => path.join(__dirname, 'img', n);

const NAVY = '002060', RED = 'C8102E', GOLD = 'FFC000', INK = '1A1A1A', GRAY = '595959', LIGHT = 'F2F2F2', MID = 'D9DCE1', BLUE = '4272C4', BRICK = 'B5533C';
const F = 'Malgun Gothic', SERIF = 'Batang';
const pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE'; // 13.333 x 7.5
pres.title = '전포 정동관 · 복합주차장 시안';
pres.author = '정성윤';
pres.theme = { headFontFace: F, bodyFontFace: F };
const SW = 13.333, SH = 7.5, M = 0.5;

// ---------- layouts
pres.defineSlideMaster({ title: 'CONTENT', background: { color: 'FFFFFF' }, objects: [
  { text: { text: '停動館', options: { x: M, y: 7.02, w: 1.1, h: 0.36, fontFace: SERIF, fontSize: 16, color: NAVY, bold: true, margin: 0, valign: 'middle' } } },
  { text: { text: '전포 정동관', options: { x: 11.2, y: 7.02, w: 1.1, h: 0.36, fontFace: F, fontSize: 10, color: GRAY, margin: 0, align: 'right', valign: 'middle' } } },
], slideNumber: { x: 12.3, y: 7.02, w: 0.55, h: 0.36, fontFace: F, fontSize: 10, color: GRAY, align: 'right' } });
pres.defineSlideMaster({ title: 'DARK', background: { color: '101216' }, objects: [] });

let N = 0;
const SEC = ['INTRODUCTION', 'MAIN SUBJECT', 'CONCLUSION'];
const _added = new Set();
function sec(i) { if (!_added.has(i)) { pres.addSection({ title: SEC[i] }); _added.add(i); } }

function T(s, text, x, y, w, h, o = {}) {
  s.addText(text, Object.assign({ x, y, w, h, fontFace: F, fontSize: 12, color: INK, margin: 0, valign: 'top', isTextBox: true }, o));
}
function bullets(items, o = {}) { // items: strings or [text,{opts}]
  return items.map((it, i) => {
    const t = Array.isArray(it) ? it[0] : it; const oo = Array.isArray(it) ? it[1] : {};
    return { text: t, options: Object.assign({ bullet: { indent: 12 }, breakLine: i < items.length - 1, paraSpaceAfter: 4 }, o, oo) };
  });
}
function pic(s, name, x, y, w, h, o = {}) { // contain inside box, centered
  const [iw, ih] = DIMS[name]; const r = iw / ih;
  let ww = Math.min(w, h * r), hh = ww / r;
  const xx = x + (w - ww) / 2, yy = o.top ? y : y + (h - hh) / 2;
  s.addImage(Object.assign({ path: IMG(name), x: xx, y: yy, w: ww, h: hh }, o.opts || {}));
  return { x: xx, y: yy, w: ww, h: hh };
}
function picW(s, name, x, y, w, o = {}) { // fixed width, height by ratio
  const [iw, ih] = DIMS[name]; const h = w * ih / iw;
  s.addImage(Object.assign({ path: IMG(name), x, y, w, h }, o)); return h;
}
function picH(s, name, x, y, h, o = {}) {
  const [iw, ih] = DIMS[name]; const w = h * iw / ih;
  s.addImage(Object.assign({ path: IMG(name), x, y, w, h }, o)); return w;
}
function cap(s, text, x, y, w, o = {}) { T(s, text, x, y, w, 0.3, Object.assign({ fontSize: 10, color: GRAY, italic: true }, o)); }
function src(s, text) { T(s, text, 1.75, 7.02, 9.3, 0.36, { fontSize: 9, color: GRAY, valign: 'middle' }); }
function takeaway(s, text, y = 6.45, x = M, w = 12.33) { T(s, '→ ' + text, x, y, w, 0.45, { fontSize: 14, color: RED, bold: true, valign: 'middle' }); }
function card(s, x, y, w, h, head, lines, o = {}) {
  s.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: o.fill || LIGHT }, line: { color: o.fill || LIGHT, width: 0 } });
  const runs = [];
  if (head) runs.push({ text: head, options: { bold: true, color: o.headColor || NAVY, fontSize: o.headSize || 13, breakLine: true, paraSpaceAfter: 3 } });
  lines.forEach((l, i) => runs.push({ text: l, options: { fontSize: o.size || 11.5, color: o.color || INK, breakLine: i < lines.length - 1, paraSpaceAfter: 3 } }));
  T(s, runs, x + 0.12, y + 0.08, w - 0.24, h - 0.14, { valign: 'top' });
}
function header(s, num, title, sub, active) {
  T(s, num, M, 0.28, 0.8, 0.62, { fontSize: 32, bold: true, color: NAVY, valign: 'middle' });
  T(s, title, 1.3, 0.26, 7.7, 0.5, { fontSize: 24, bold: true, color: INK, valign: 'middle' });
  T(s, sub, 1.3, 0.76, 7.7, 0.32, { fontSize: 13, color: GRAY, valign: 'middle' });
  SEC.forEach((t, i) => {
    const on = i === active;
    s.addText(t, { x: 9.28 + i * 1.2, y: 0.3, w: 1.16, h: 0.3, fontFace: F, fontSize: 8.5, bold: true, align: 'center', valign: 'middle', margin: 0, isTextBox: true,
      color: on ? 'FFFFFF' : '8C8C8C', fill: { color: on ? NAVY : LIGHT } });
  });
}
function slide(num, title, sub, active, notes) {
  const s = pres.addSlide({ masterName: 'CONTENT', sectionTitle: SEC[active] });
  header(s, num, title, sub, active);
  if (notes) s.addNotes(notes);
  return s;
}
const HF = { fill: { color: '767171' }, color: 'FFFFFF', bold: true, valign: 'middle' };
function table(s, head, rows, x, y, w, colW, o = {}) {
  const fs = o.size || 11;
  const hr = head ? [head.map((h, i) => ({ text: h, options: Object.assign({ align: (o.aligns && o.aligns[i]) || 'left', fontSize: fs }, HF) }))] : [];
  const body = rows.map((r, ri) => r.map((c, ci) => {
    const base = { fontSize: fs, valign: 'middle', align: (o.aligns && o.aligns[ci]) || 'left', color: INK, fill: { color: ri % 2 ? 'F0F3F7' : 'E7E6E6' } };
    if (o.boldRows && o.boldRows.includes(ri)) base.bold = true;
    if (typeof c === 'object' && c !== null) return { text: c.t, options: Object.assign(base, c.o || {}) };
    return { text: String(c), options: base };
  }));
  s.addTable(hr.concat(body), { x, y, w, colW, fontFace: F, border: { type: 'solid', pt: 0.5, color: 'FFFFFF' }, margin: [3, 6, 3, 6], rowH: o.rowH, autoPage: false });
}
const dark = (s) => s.background = { color: '101216' };

// =====================================================================
// 01 표지
{
  sec(0);
  const s = pres.addSlide({ masterName: 'DARK', sectionTitle: SEC[0] });
  s.addImage({ path: IMG('hero_sw.jpg'), x: 0, y: 0, w: SW, h: SH });
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 8.6, h: SH, fill: { color: '080C18', transparency: 22 }, line: { color: '080C18', width: 0 } });
  T(s, '2026 · 공학설계기초', 0.7, 0.55, 6, 0.4, { fontSize: 16, bold: true, color: 'FFFFFF' });
  T(s, '停動館', 0.7, 1.2, 7.5, 1.9, { fontFace: SERIF, fontSize: 96, color: 'FFFFFF', bold: true, valign: 'middle' });
  T(s, '전포 정동관', 0.7, 3.25, 7.5, 0.9, { fontSize: 44, bold: true, color: 'FFFFFF', valign: 'middle' });
  T(s, '낮에는 주차장, 밤에는 공연과 옥상 광장', 0.7, 4.3, 7.8, 0.5, { fontSize: 22, bold: true, color: GOLD });
  T(s, '복합주차장 시안 · 부산진구 전포동 207번지 일대 53필지 4,964.5㎡\n지하 4층 · 지상 6층 + 옥상 · 연면적 43,623.7㎡ · 주차 약 600대', 0.7, 5.0, 7.8, 0.8, { fontSize: 14, color: 'FFFFFF' });
  T(s, '202325137 정성윤', 0.7, 6.3, 5, 0.4, { fontSize: 16, bold: true, color: 'FFFFFF' });
  T(s, '투시도는 개념 볼륨 모델로 만든 이미지이며 실제 설계안이 아님', 0.7, 6.82, 8, 0.3, { fontSize: 10, color: 'D9D9D9' });
}

// =====================================================================
// 02 사업 배경 · 개요
{
  sec(0);
  const s = slide('01', '사업 배경 · 개요', '상권 한가운데 주차 공급이 모자란 곳', 0,
    '확보율 = 주차면수 ÷ 주차수요 × 100. 69.1%는 "상가밀집지역"이 아니라 노후주거지 밀집 등 주차환경개선지구 67곳의 평균이다(파이낸셜뉴스 2022.07.11).');
  T(s, '주차장 확보율 비교 (%)', M, 1.3, 4.3, 0.3, { fontSize: 13, bold: true, color: NAVY });
  s.addChart(pres.charts.BAR, [{ name: '확보율(%)', labels: ['부산 전체(2021)', '부산진구(2023)', '개선지구 평균'], values: [130.5, 118.5, 69.1] }], {
    x: M, y: 1.55, w: 4.3, h: 2.2, barDir: 'bar', chartColors: [NAVY, BLUE, '8493B2'], showValue: true, dataLabelFontSize: 11, dataLabelFontFace: F, dataLabelColor: INK,
    dataLabelFormatCode: '0.0', catAxisLabelFontSize: 11, catAxisLabelFontFace: F, catAxisLabelColor: INK, valAxisHidden: true, valAxisMaxVal: 160, valAxisMinVal: 0,
    valGridLine: { style: 'none' }, catGridLine: { style: 'none' }, showLegend: false, barGapWidthPct: 45, catAxisOrientation: 'maxMin' });
  cap(s, '기준선 130% · 부산진구는 등록 대비 118.5%', M, 3.78, 4.3);
  picH(s, 'photo_parking1.jpg', M, 4.15, 2.45, {});
  picH(s, 'photo_parking2.jpg', M + 1.95, 4.15, 2.45, {});
  cap(s, '전포동 이면도로 현장(답사 2026.9) · 불법주차와 보행 혼재', M, 6.63, 4.4);

  T(s, '수급 실태 지표', 5.2, 1.3, 4, 0.3, { fontSize: 13, bold: true, color: NAVY });
  table(s, ['지표', '값', '출처'], [
    ['부산진구 확보율(등록 대비)', '118.5% · 기준 130% 대비 약 1.7만 면 부족', '구 수급실태조사(2023)'],
    ['대지 반경 500m 공영주차장', '27면 (1km 이내 약 415면)', '표준데이터, 시설공단'],
    ['부산진구 불법주정차 단속', '부산 1위 (2021.1~10월 109,993건)', '글로벌경제 2021'],
    ['시 공급 계획', '2025년까지 6,092면 · 1,995억 원', '부산시 주차종합계획'],
  ], 5.2, 1.6, 7.63, [2.35, 3.3, 1.98], { size: 10.5 });
  T(s, '정동관 개요', 5.2, 3.72, 4, 0.3, { fontSize: 13, bold: true, color: NAVY });
  table(s, null, [
    [{ t: '위치·용도지역', o: { bold: true } }, '부산진구 전포동 207번지 일대 53필지 · 일반상업지역 · 방화지구'],
    [{ t: '대지·연면적', o: { bold: true } }, '4,964.5㎡ · 43,623.7㎡ (지상 23,923.7 + 지하 19,700.0)'],
    [{ t: '규모', o: { bold: true } }, '지하 4층 · 지상 6층 + 옥상, 지상 약 29.1m'],
    [{ t: '건폐율·용적률', o: { bold: true } }, '87.1% (상한 90%) · 481.9% (지하 제외)'],
    [{ t: '주차', o: { bold: true } }, '약 600대 · 주차 비율 75.62%'],
    [{ t: '주요 시설', o: { bold: true } }, '1F 서점·카페·근생 · 5F 상인회 · 6F 가변홀 · B1~B2 공연장 200석 · 옥상 광장'],
  ], 5.2, 4.02, 7.63, [1.75, 5.88], { size: 10.5 });
  takeaway(s, '소규모 필지에 점포가 밀집해 부설주차장 확보가 어려워, 상권 한가운데 거점형 주차장이 필요함', 6.55, 5.2, 7.63);
  src(s, '파이낸셜뉴스 2022.07.11 · 부산일보 2024.07.04 · 글로벌경제 2021 · 토지이음(2026.10.11) · 69.1%는 주차환경개선지구 67곳 평균');
}

// =====================================================================
// 03 대지 분석
{
  sec(1);
  const s = slide('02', '대지 분석', '53필지를 한 블록으로 묶어 쓰는 조건', 1);
  const h = picW(s, 'site_eum.jpg', M, 1.3, 3.75);
  cap(s, '토지이용계획 확인도면 · 필지군 표시(개략)', M, 1.3 + h + 0.05, 3.75);
  T(s, '대지 개요', 4.5, 1.3, 4, 0.3, { fontSize: 13, bold: true, color: NAVY });
  table(s, ['구역', '필지', '면적㎡', '형상 · 접도'], [
    ['서측 쐐기', '19', '1,531.9', '전포대로(서)에 면한 쐐기형, 남단이 뾰족함'],
    ['소로 부지', '5', '733.1', '두 구역 사이 폭 약 6m, 남단 전포대로 · 북단 서전로'],
    ['동측 블록', '29', '2,699.5', '서전로 · 224번길 · 동측 이면도로에 면한 삼각형'],
    ['합계', '53', '4,964.5', '지목 대 48필지, 도로 5필지'],
  ], 4.5, 1.6, 8.33, [1.4, 0.7, 1.1, 5.13], { size: 11, aligns: ['left', 'right', 'right', 'left'], boldRows: [3] });
  T(s, '배치 조건', 4.5, 3.4, 4, 0.3, { fontSize: 13, bold: true, color: NAVY });
  const cw = 4.1, ch = 1.1;
  card(s, 4.5, 3.72, cw, ch, '용도지역 · 높이', ['일반상업지역 · 방화지구', '가로구역별 최고높이 기준 130m · 최고 180m'], { size: 12.5, headSize: 13.5 });
  card(s, 4.5 + cw + 0.13, 3.72, cw, ch, '건축선 3m 이격', ['공연장 1,000㎡ 이상이라 북(서전로)·남(224번길)을 띄움, 전포대로 쪽은 면제'], { size: 12.5, headSize: 13.5 });
  card(s, 4.5, 3.72 + ch + 0.12, cw, ch, '두 뾰족한 끝을 비움', ['동측 북단 약 352㎡, 서측 남단 약 158㎡ → 개방 순환 계단 코어'], { size: 12.5, headSize: 13.5 });
  card(s, 4.5 + cw + 0.13, 3.72 + ch + 0.12, cw, ch, '결과', ['2층 이상 건축면적 4,322.1㎡', '건폐율 87.1% (상한 90%)'], { size: 12.5, headSize: 13.5 });
  card(s, 4.5, 6.1, 8.33, 0.7, null, ['확인할 것 · 207-15·79는 제3종일반주거지역도 표기(상업지역으로 계산) · 207-84·85는 지목 대이나 도로로 쓰임'], { fill: 'FFF3CC', size: 11 });
  src(s, '토지이음 필지별 토지이용계획 조회(2026.10.11) · 부산 건축조례 별표4 · 필지 위치는 확인도면 정합으로 판별, 치수 개략');
}

// =====================================================================
// 04 입지 · 접근
{
  sec(1);
  const s = slide('03', '부지 선정 · 교통 및 동선', '수요와 접근이 맞는 곳', 1);
  const h = picW(s, 'transit_map.jpg', M, 1.3, 4.9);
  cap(s, '주변 현황도 · 지도 © OpenStreetMap contributors, 위치 개략', M, 1.3 + h + 0.05, 4.9);
  T(s, '입지 근거 세 가지', 5.7, 1.3, 4, 0.3, { fontSize: 13, bold: true, color: NAVY });
  const loc = [['1', '지하철 두 역 도보권', '1호선 서면역 737m · 2호선 전포역 529m. 주차 이용객뿐 아니라 공연·광장 방문객도 걸어서 접근'],
    ['2', '카페거리 상권 사이', '전리단길 · 전포카페거리 · 전포사잇길 사이. 낮 방문객과 밤 관객 수요를 함께 받음'],
    ['3', '공영주차장 공백지대', '반경 500m 공영 27면, 1km 약 415면. 2022 시의회에서 대지 옆 놀이마루 부지 공영주차장 건립이 제안됨']];
  loc.forEach((c, i) => {
    const y = 1.62 + i * 0.95;
    s.addShape(pres.shapes.RECTANGLE, { x: 5.7, y, w: 7.13, h: 0.85, fill: { color: LIGHT }, line: { color: LIGHT, width: 0 } });
    T(s, c[0], 5.82, y, 0.45, 0.85, { fontSize: 26, bold: true, color: NAVY, valign: 'middle' });
    T(s, [{ text: c[1], options: { bold: true, fontSize: 13, breakLine: true } }, { text: c[2], options: { fontSize: 11 } }], 6.3, y + 0.07, 6.4, 0.75, {});
  });
  T(s, '접근 계획', 5.7, 4.55, 4, 0.3, { fontSize: 13, bold: true, color: NAVY });
  const tiles = [['차량', '남단 진입 · 북단 진출, 소로는 남→북 일방 전용. 400대 초과 입구·출구 분리'], ['보행', '1층 외곽을 한 바퀴, 소로 중간에 횡단보도 1곳. 서점·카페·로비는 전포대로 쪽'],
    ['수직', '끝 코어 2곳(개방 순환 계단 + 승강기), 지하는 같은 자리에 특별피난계단'], ['하역·이륜차', '동측 이면도로 쪽 1층 북쪽, 일반 차량과 분리. 동측 주거 쪽 차량 진출입 없음']];
  tiles.forEach((t, i) => card(s, 5.7 + (i % 2) * 3.62, 4.87 + Math.floor(i / 2) * 0.88, 3.51, 0.8, t[0], [t[1]], { size: 10.5, headSize: 12 }));
  takeaway(s, '두 역 도보권과 카페거리 사이의 공영주차장 공백지라 거점형 입지로 적합함', 6.62, 5.7, 7.13);
  src(s, '카카오맵 도보 환산, 팀 상권 조사, 부산버스정보시스템(2026.9.30), 시설공단 · 표준데이터(2026.04), 시의회 5분 발언(2022.08)');
}

// =====================================================================
// 05 향 · 일조
{
  sec(1);
  const s = slide('04', '향 · 일조', '남북 장축 블록의 일사와 그림자', 1,
    '가정과 한계: 그림자는 NOAA 태양 위치 근사식(북위 35.157°)과 본 시안 매스(옥상 광장 +21.1m, 홀 29.8m)로 계산했다. 주변 건물은 OpenStreetMap 등록분만 반영해 저층 건물이 빠져 있다. 일조 판단 시간대는 동지 9~15시로 가정했다. 건축법상 정북 일조 제한은 주거지역에만 적용되어 상업지역 대지에는 해당하지 않는다.');
  const h1 = picW(s, 'shadow3.png', M, 1.3, 8.2);
  cap(s, '정동관 그림자 · 동지 09/12/15시 (높이 29.8m 기준, 붉은 점선 = 제3종일반주거 경계 약 45m)', M, 1.3 + h1 + 0.04, 8.2);
  const y0 = 4.5;
  const fac = [
    ['서측 · 전포대로', '직사 동지 4.3h · 하지 6.7h (오후)', '서향 일사와 도로 소음을 함께 받는 면', '타공 전돌 스크린, 6F는 세로 핀 유리(미정)'],
    ['동측 · 이면도로', '직사 동지 4.3h · 하지 6.8h (오전)', '동지 15시경에야 주거 경계에 도달, 9~15시 최대 0.5h 미만', '일조 침해 낮음, 차량 진출입 없음'],
    ['남측 · 224번길', '직사 동지 8.6h · 하지 6.9h', '동지 고도 31°로 깊이 입사, 하지는 78°', '1층 근생 남단 + 옥상 광장 남향 배치'],
    ['북측 · 서전로', '동지 직사 0h · 하지는 새벽·저녁만', '확산광이라 밝기가 일정, 그림자는 북쪽 도로로', '6F 홀을 북쪽에 둠, 광장은 홀 남쪽'],
  ];
  fac.forEach((f, i) => card(s, M + i * 2.07, y0, 2.0, 1.85, f[0], [f[1], f[2], '→ ' + f[3]], { size: 10.5, headSize: 12 }));
  takeaway(s, '동지에도 동측 주거지 그림자는 0.5h 미만, 옥상 광장은 그림자 영향 없음', 6.45, M, 8.2);
  const w2 = 3.93, x2 = 8.9;
  const h2 = picW(s, 'sunpath.png', x2, 1.3, w2);
  cap(s, '태양 경로 · 동지·춘추분·하지 (대지 위치)', x2, 1.3 + h2 + 0.04, w2);
  const yh = 1.3 + h2 + 0.45;
  picW(s, 'shadow_hours.png', x2 + 0.25, yh, 3.4);
  cap(s, '동지 09~15시 그림자 누적 시간(h)', x2, 6.62, w2);
  src(s, 'NOAA 태양 위치 근사식 · OpenStreetMap contributors(건물 층수·높이 일부 추정) · 본 시안 매스 계산, 직사 시간은 고도 5° 이상 · 가림 없음 가정');
}

// =====================================================================
// 06 소음
{
  sec(1);
  const s = slide('05', '소음', '서·북 도로변 소음원과 동측 주거 경계', 1,
    '가정과 한계: 소음 분포는 실측이 아니라 개략 추정이다. OSM 도로를 5m 간격 점음원으로 바꾸고 10m 기준 Leq를 광로·대로 70, 3차 63, 주거 58 dB(A)로 가정했다. 건물 차폐와 지면 효과는 반영하지 않아 실제와 다를 수 있다. 현장 낮·밤 실측으로 교체해야 한다.');
  const h = picW(s, 'noise_map.png', M, 1.3, 4.45);
  cap(s, '주간 소음 분포 추정 · 가정 교통량, 건물 차폐 미반영 · 점 = 4면 평가점', M, 1.3 + h + 0.04, 4.45);
  const py = 1.3 + h + 0.42;
  s.addImage({ path: IMG('photo_parking2.jpg'), x: M, y: py, w: 2.15, h: 1.15, sizing: { type: 'cover', w: 2.15, h: 1.15 } });
  s.addImage({ path: IMG('jeonpo_street.jpg'), x: M + 2.3, y: py, w: 2.15, h: 1.15, sizing: { type: 'cover', w: 2.15, h: 1.15 } });

  const x1 = 5.2;
  T(s, '환경기준 · 소음 dB(A)', x1, 1.3, 4, 0.3, { fontSize: 13, bold: true, color: NAVY });
  table(s, ['구분', '낮', '밤', '적용'], [
    ['일반지역 다(상업)', '65', '55', '대지(상업)'],
    ['도로변 다(상업)', '70', '60', '서·북 도로변'],
    ['일반지역 나(주거)', '55', '45', '동측 3종주거'],
    ['도로변 가·나(주거)', '65', '55', '동측 주거변'],
  ], x1, 1.6, 3.9, [1.4, 0.45, 0.45, 1.6], { size: 10, aligns: ['left', 'center', 'center', 'left'] });
  cap(s, '환경정책기본법 시행령 · 낮 06~22시, 밤 22~06시', x1, 3.5, 3.9);
  T(s, '면별 주간 추정치 (dB(A), 가정)', x1, 3.85, 4, 0.3, { fontSize: 13, bold: true, color: NAVY });
  s.addChart(pres.charts.BAR, [{ name: '주간 Leq 추정', labels: ['북(서전로)', '서(전포대로)', '남(224번길)', '동(이면도로)', '동측 주거 경계'], values: [76, 72, 70, 69, 67] }], {
    x: x1, y: 4.15, w: 3.9, h: 2.5, barDir: 'bar', chartColors: [RED, RED, 'E07A00', 'E07A00', BLUE], showValue: true, dataLabelFontSize: 10.5, dataLabelFontFace: F, dataLabelColor: INK,
    catAxisLabelFontSize: 10.5, catAxisLabelFontFace: F, catAxisLabelColor: INK, valAxisHidden: true, valAxisMinVal: 50, valAxisMaxVal: 82, valGridLine: { style: 'none' }, catGridLine: { style: 'none' },
    showLegend: false, barGapWidthPct: 40, catAxisOrientation: 'maxMin' });

  const x2 = 9.35, w2 = 3.48;
  T(s, '공간별 대응', x2, 1.3, 3, 0.3, { fontSize: 13, bold: true, color: NAVY });
  const resp = [
    ['지하 공연장 B1~B2', '박스인박스 + 방진 바닥, 선큰 마당 쪽 로비가 완충. 실내 배경소음 NC 20~25 목표(제안)'],
    ['6F 가변홀', '이중 차음 지붕, 소음원인 서·북 면은 닫고 광장(남)으로 개구'],
    ['소로 · 램프', '2층 바닥이 덮은 높이 7m 통로라 엔진·경적 소음이 내부에 갇힘'],
    ['5F 상인회', '동측 이면 쪽 배치, 서측 면은 2중창'],
    ['동측 주거 경계', '차량 진출입 없음, 하역·이륜차는 운영시간 제한'],
  ];
  resp.forEach((r, i) => card(s, x2, 1.62 + i * 0.99, w2, 0.92, r[0], [r[1]], { size: 10, headSize: 11.5 }));
  src(s, '환경정책기본법 시행령 · 전포동 측정값 없음(부산시 측정망 목록에 전포동 지점 없음) · 표의 dB은 개략 추정, 실측 필요');
}

// =====================================================================
// 07 조망
{
  sec(1);
  const s = slide('06', '조망', '황령산 · BIFC · 서면 도심, 옥상 광장에서 열림', 1,
    '황령산 정상(427m)은 OSM 좌표 기준 대지에서 동쪽 약 1.47km, BIFC(289m, 문현금융단지)는 남쪽 약 1.15km이다. 눈높이는 1층 1.6m, 옥상 광장 22.7m(+21.1m 지붕 위 1.6m)로 두었다. 주변 건물은 OSM 등록분(반경 약 420m)만 반영하므로 저층 건물이 빠져 조망이 실제보다 열려 보일 수 있다.');
  const h = picW(s, 'view_profile.png', M, 1.3, 8.35);
  cap(s, '스카이라인 앙각 분석 · 옥상 광장 vs 1층 가로 (주변 건물 + 정동관 매스)', M, 1.3 + h + 0.03, 8.35);
  const y2 = 1.3 + h + 0.4;
  s.addImage({ path: IMG('jeonpo_view.jpg'), x: M, y: y2, w: 4.1, h: 1.85 });
  s.addImage({ path: IMG('roof_view.jpg'), x: M + 4.2, y: y2, w: 3.3, h: 1.85 });
  cap(s, 'BIFC·서면 일대 조망 · Christian Bolz, CC BY-SA 4.0', M, y2 + 1.88, 4.1, { fontSize: 9 });
  cap(s, '옥상 광장 시뮬레이션(개념 모델)', M + 4.2, y2 + 1.88, 3.3, { fontSize: 9 });
  const x2 = 9.1, w2 = 3.73;
  T(s, '조망 대상', x2, 1.3, 3, 0.3, { fontSize: 13, bold: true, color: NAVY });
  table(s, ['대상', '방위·거리', '앙각', '옥상 판정'], [
    ['황령산 정상', '동 87° · 1.47km', '15.1°', { t: '상단만 보임', o: { color: RED, bold: true } }],
    ['BIFC', '남 184° · 1.15km', '12.6°', { t: '보임', o: { color: NAVY, bold: true } }],
    ['서면 도심', '서 · 약 0.6km', '고층', { t: '보임', o: { color: NAVY, bold: true } }],
  ], x2, 1.6, w2, [0.95, 1.2, 0.58, 1.0], { size: 9.5 });
  card(s, x2, 3.2, w2, 1.7, '시점별 차이', ['1층 가로: 동쪽은 자체 매스가 가려 황령산 안 보임, 남쪽 전포대로 축으로 BIFC만 보임', '옥상 광장: 열린 각도 약 128°(스카이라인 6° 미만), 동남동 29~30층 아파트 위로 능선 상단이 걸침'], { size: 10.5, headSize: 12 });
  card(s, x2, 5.0, w2, 1.35, '설계 반영', ['조망 개구부는 남(BIFC)과 동(황령산 능선)에 집중', '북·서 면은 차음과 일사 때문에 닫음', '동·남 모서리에 벤치, 난간은 낮게'], { size: 10.5, headSize: 12, fill: 'E8EEF9' });
  T(s, '→ 조망은 옥상에서, 남·동으로만 열음', x2, 6.45, w2, 0.45, { fontSize: 13, bold: true, color: RED, valign: 'middle' });
  src(s, 'OSM 좌표 · 위키백과 · 토지이음 · 본 시안 매스 · 앙각은 지면 8m 가정 · 사진: Wikimedia Commons(CC BY-SA 4.0) · 능선 형상은 반영 안 됨');
}

// =====================================================================
// 08 콘셉트 (dark)
{
  const s = pres.addSlide({ masterName: 'DARK', sectionTitle: SEC[1] });
  s.addImage({ path: IMG('night_sw.jpg'), x: 0, y: 0, w: SW, h: SH, transparency: 40 });
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: SW, h: SH, fill: { color: '0A0C10', transparency: 35 }, line: { color: '0A0C10', width: 0 } });
  ['停', '動', '館'].forEach((c, i) => T(s, c, 0.9, 0.55 + i * 1.95, 2.2, 1.9, { fontFace: SERIF, fontSize: 96, bold: true, color: 'FFFFFF', align: 'center', valign: 'middle' }));
  T(s, '정동관', 0.9, 6.45, 3, 0.7, { fontSize: 32, bold: true, color: 'FFFFFF' });
  T(s, '낮에는 주차장,\n밤에는 공연과 옥상 광장', 4.0, 0.95, 8.8, 1.9, { fontSize: 44, bold: true, color: 'FFFFFF', valign: 'top' });
  T(s, '停動館의 뜻', 4.0, 3.15, 6, 0.5, { fontSize: 22, bold: true, color: GOLD });
  T(s, '停은 멈춤, 動은 움직임, 館은 건물임. 차가 멈추는 주차층(停)은 차분한 전돌 스크린으로 감싸고, 사람이 움직이는 계단 · 홀 · 광장(動)은 붉은 순환 계단과 빛나는 홀로 드러냄. 낮에는 상권의 차를 받고, 밤에는 지하 공연장 · 6F 가변홀 · 옥상 광장이 켜짐', 4.0, 3.75, 8.3, 2.0, { fontSize: 17, color: 'FFFFFF', lineSpacingMultiple: 1.25 });
  T(s, '정동관은 주차 건물이 아니라 멈춤과 움직임이 하루 안에서 교대하는 건물을 목표로 함', 4.0, 6.25, 8.3, 0.7, { fontSize: 14, color: 'D9D9D9' });
}

module.exports = { pres, slide, sec, T, table, card, pic, picW, picH, cap, src, takeaway, bullets, header, IMG, DIMS, NAVY, RED, GOLD, INK, GRAY, LIGHT, MID, BLUE, BRICK, F, SERIF, M, SW, SH, SEC, HF };
