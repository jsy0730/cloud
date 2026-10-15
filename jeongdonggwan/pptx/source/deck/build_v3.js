// 전포 정동관 — 공설기 v1.2 스타일 PPTX (21장)
const pptxgen = require('pptxgenjs');
const path = require('path');
const fs = require('fs');
const DIMS = JSON.parse(fs.readFileSync(path.join(__dirname, 'dims.json'), 'utf8'));
const find = (n) => fs.existsSync(path.join(__dirname, 'img2', n)) ? path.join(__dirname, 'img2', n) : path.join(__dirname, 'img', n);

// ---- design tokens (공설기 v1.2, light)
const NAVY = '002060', INK = '000000', MUTED = '595959', LINE = 'A0A2A5', PANEL = 'F0F3F7', SOFT = 'F2F2F2', TABOFF = '8C8C8C';
const THEAD = '767171', TCELL = 'E7E6E6', CHAR = '525252', CALLOUT = '323232', DIVG = '4C4C4C', PDARK = '141414';
const GOLD = 'FFC000', SELTXT = '8A6400', SIGNAL = 'FF0000', PIN = 'C00000', SLATE = '8493B2', NSOFT = 'DAE3F3';
const D1 = '08205E', D2 = '4272C4', D3 = '7F9DCF', D4 = 'ABBDE0', D5 = 'DBE2F5';
const FROOF = 'E2F0D9', FFLEX = '8FAADC', FCULT = 'B4C7E7', FENTRY = 'DAE3F3', FPARK = 'C9C9C9';
const F = 'Malgun Gothic', SERIF = 'Batang';
const M = 0.5, CW = 12.33, SW = 13.333;

const pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE';
pres.title = '전포 정동관 · 복합주차장 시안 (공설기 v1.2)';
pres.author = '정성윤';
pres.theme = { headFontFace: F, bodyFontFace: F };
pres.defineSlideMaster({ title: 'GS', background: { color: 'FFFFFF' }, objects: [] });
const SEC = ['INTRODUCTION', 'MAIN SUBJECT', 'CONCLUSION'];
const added = new Set();
function sec(i) { if (!added.has(i)) { pres.addSection({ title: SEC[i] }); added.add(i); } }

// ---- primitives
function T(s, text, x, y, w, h, o = {}) {
  s.addText(text, Object.assign({ x, y, w, h, fontFace: F, fontSize: 11, color: INK, margin: 0, valign: 'top', isTextBox: true }, o));
}
function R(s, x, y, w, h, fill, o = {}) {
  s.addShape(pres.shapes.RECTANGLE, Object.assign({ x, y, w, h, fill: { color: fill }, line: o.line ? { color: o.line, width: o.lw || 0.75 } : { type: 'none' } }, o.shape || {}));
}
function HL(s, x, y, w, color = LINE, wt = 0.75) { s.addShape(pres.shapes.LINE, { x, y, w, h: 0, line: { color, width: wt } }); }
function img(s, name, x, y, w, h) { s.addImage({ path: find(name), x, y, w, h }); }
function imgW(s, name, x, y, w) { const [iw, ih] = DIMS[name]; const h = w * ih / iw; s.addImage({ path: find(name), x, y, w, h }); return h; }
function imgH(s, name, x, y, h) { const [iw, ih] = DIMS[name]; const w = h * iw / ih; s.addImage({ path: find(name), x, y, w, h }); return w; }
// native (editable) vector drawing from matplotlib export
function drawVector(s, name, x0, y0, w) {
  const V = JSON.parse(fs.readFileSync(path.join(__dirname, 'img', name), 'utf8'));
  const [xmin, xmax] = V.xlim, [ymin, ymax] = V.ylim;
  const sc = w / (xmax - xmin), f = w / V.width_in;
  const Hh = w * V.height_in / V.width_in, sy = Hh / (ymax - ymin);
  const px = (X) => x0 + (X - xmin) * sc, py = (Y) => y0 + (ymax - Y) * sy;
  const dash = (ls) => (ls === 'dash' ? 'dash' : ls === 'sysDot' ? 'sysDot' : ls === 'dashDot' ? 'dashDot' : 'solid');
  const emw = (t, size) => { let w_ = 0; for (const ch of t) w_ += ch.charCodeAt(0) > 0x2E80 ? 1.0 : 0.56; return w_ * size / 72; };
  V.items.forEach((d) => {
    if (d.type === 'rect' || d.type === 'rrect' || d.type === 'ellipse') {
      const o = { x: px(d.x), y: py(d.y + d.h), w: d.w * sc, h: d.h * sy };
      if (d.fill) o.fill = { color: d.fill, transparency: Math.round((1 - d.fa) * 100) }; else o.fill = { type: 'none' };
      if (d.line) o.line = { color: d.line, width: Math.max(0.25, d.lw * f), dashType: dash(d.ls) }; else o.line = { type: 'none' };
      if (d.type === 'rrect') o.rectRadius = 0.04;
      s.addShape(d.type === 'ellipse' ? pres.shapes.OVAL : d.type === 'rrect' ? pres.shapes.ROUNDED_RECTANGLE : pres.shapes.RECTANGLE, o);
    } else if (d.type === 'poly') {
      const xs = d.pts.map((p) => px(p[0])), ys = d.pts.map((p) => py(p[1]));
      const x = Math.min(...xs), y = Math.min(...ys), w_ = Math.max(...xs) - x, h_ = Math.max(...ys) - y;
      s.addShape(pres.shapes.CUSTOM_GEOMETRY ? pres.shapes.CUSTOM_GEOMETRY : pres.shapes.RECTANGLE, { x, y, w: w_, h: h_, fill: d.fill ? { color: d.fill, transparency: Math.round((1 - d.fa) * 100) } : { type: 'none' }, line: { type: 'none' }, points: d.pts.map((p, i) => ({ x: xs[i] - x, y: ys[i] - y })) });
    } else if (d.type === 'line') {
      for (let i = 0; i < d.pts.length - 1; i++) {
        const ax = px(d.pts[i][0]), ay = py(d.pts[i][1]), bx = px(d.pts[i + 1][0]), by = py(d.pts[i + 1][1]);
        const w_ = Math.abs(bx - ax), h_ = Math.abs(by - ay);
        if (w_ < 0.002 && h_ < 0.002) continue;
        const flipV = (bx - ax) * (by - ay) < 0;
        s.addShape(pres.shapes.LINE, { x: Math.min(ax, bx), y: Math.min(ay, by), w: w_, h: h_, flipV, line: { color: d.color, width: Math.max(0.25, d.lw * f), dashType: dash(d.ls) } });
      }
    } else if (d.type === 'text') {
      const size = Math.max(5, d.size * f);
      const tw = emw(d.text, size) + 0.12, th = size * 1.5 / 72;
      const cx = px(d.x), cy = py(d.y);
      let bx = cx - tw / 2, by = cy - th / 2;
      if (!d.rot) {
        if (d.ha === 'left') bx = cx; else if (d.ha === 'right') bx = cx - tw;
        if (d.va === 'bottom' || d.va === 'baseline') by = cy - th; else if (d.va === 'top') by = cy;
      }
      s.addText(d.text, { x: bx, y: by, w: tw, h: th, fontFace: F, fontSize: size, bold: !!d.bold, color: d.color, margin: 0, wrap: false, isTextBox: true,
        align: d.rot ? 'center' : (d.ha === 'left' ? 'left' : d.ha === 'right' ? 'right' : 'center'), valign: 'middle', rotate: d.rot ? (360 - d.rot) % 360 : 0 });
    }
  });
  return Hh;
}
function cap(s, text, x, y, w, o = {}) { T(s, text, x, y, w, 0.26, Object.assign({ fontSize: 9, italic: true, color: MUTED, align: 'right' }, o)); }
function barHeading(s, text, x, y, w = 5) {
  R(s, x, y + 0.03, 0.055, 0.26, NAVY);
  T(s, text, x + 0.14, y, w, 0.32, { fontSize: 13, bold: true, valign: 'middle' });
}
function takeaway(s, text, x, y, w, o = {}) {
  const h = o.h || (o.sub ? 0.7 : 0.5);
  R(s, x, y, w, h, PANEL);
  s.addText('결론', { x, y, w: 0.78, h, fontFace: F, fontSize: 12, bold: true, color: 'FFFFFF', fill: { color: NAVY }, align: 'center', valign: 'middle', margin: 0, isTextBox: true });
  const runs = [{ text: '→ ' + text, options: { bold: true, color: SIGNAL, fontSize: o.size || 13.5, breakLine: !!o.sub } }];
  if (o.sub) runs.push({ text: o.sub, options: { color: INK, fontSize: 10.5 } });
  T(s, runs, x + 0.95, y + 0.04, w - 1.1, h - 0.08, { valign: 'middle', lineSpacingMultiple: 1.05 });
}
function tag(s, text, x, y) {
  const w = Math.max(0.7, text.length * 0.115 + 0.28);
  s.addText(text, { x, y, w, h: 0.26, fontFace: F, fontSize: 9.5, bold: true, color: 'FFFFFF', fill: { color: NAVY }, margin: 0, align: 'center', valign: 'middle', isTextBox: true });
  return w;
}
// LabeledPanel: groups = [{label, items:[{title, lines:[]}]}] ; returns total height
function labeledPanel(s, x, y, w, groups, o = {}) {
  const fs = o.size || 10.5; const lh = fs * 0.0185 * 1.18;
  let yy = y;
  groups.forEach((g, gi) => {
    let h = 0.42;
    g.items.forEach((it) => { h += 0.26 + it.lines.length * (o.lineH || 0.2) * (it.wrap || 1) + 0.06; });
    h += 0.06;
    if (o.minH) h = Math.max(h, o.minH);
    R(s, x, yy, w, h, SOFT);
    tag(s, g.label, x + 0.14, yy + 0.1);
    let cy = yy + 0.46;
    g.items.forEach((it) => {
      const runs = [{ text: '▶ ', options: { color: SLATE, fontSize: fs - 1.5, bold: true } }, { text: it.title, options: { bold: true, fontSize: fs + 0.5, breakLine: true } }];
      it.lines.forEach((l, i) => runs.push({ text: '- ' + l, options: { fontSize: fs, breakLine: i < it.lines.length - 1 } }));
      const hh = 0.26 + it.lines.length * (o.lineH || 0.2) * (it.wrap || 1);
      T(s, runs, x + 0.16, cy, w - 0.3, hh, {});
      cy += hh + 0.06;
    });
    yy += h + 0.1;
  });
  return yy - y;
}
function noteBox(s, x, y, w, h, title, text, o = {}) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.1, fill: { color: PANEL }, line: { color: LINE, width: 0.75 } });
  const runs = [];
  if (title) runs.push({ text: title + '  ', options: { bold: true, color: NAVY, fontSize: o.size || 10.5 } });
  runs.push({ text, options: { fontSize: o.size || 10.5 } });
  T(s, runs, x + 0.15, y + 0.06, w - 0.3, h - 0.12, { valign: 'middle' });
}
function table(s, head, rows, x, y, w, colW, o = {}) {
  const fs = o.size || 10.5;
  const hr = head ? [head.map((h, i) => ({ text: h, options: { fill: { color: THEAD }, color: 'FFFFFF', bold: true, fontSize: fs, align: (o.aligns && o.aligns[i]) || 'left', valign: 'middle' } }))] : [];
  const body = rows.map((r, ri) => r.map((c, ci) => {
    const base = { fontSize: fs, color: INK, valign: 'middle', align: (o.aligns && o.aligns[ci]) || 'left', fill: { color: (o.label && ci === 0) ? PANEL : (ri % 2 ? 'F0F3F7' : TCELL) } };
    if ((o.boldRows && o.boldRows.includes(ri)) || (o.label && ci === 0)) base.bold = true;
    if (typeof c === 'object' && c !== null) return { text: c.t, options: Object.assign(base, c.o || {}) };
    return { text: String(c), options: base };
  }));
  s.addTable(hr.concat(body), { x, y, w, colW, fontFace: F, border: { type: 'solid', pt: 1.5, color: 'FFFFFF' }, margin: [0.03, 0.08, 0.03, 0.08], rowH: o.rowH });
}
function specTable(s, rows, x, y, w, colW, o = {}) {
  const fs = o.size || 10.5;
  const body = rows.map((r) => r.map((c, ci) => ({ text: c, options: { fontSize: fs, color: INK, valign: 'middle', bold: ci === 0, align: ci === 0 ? 'center' : 'left', fill: { color: ci === 0 ? PANEL : 'FFFFFF' } } })));
  s.addTable(body, { x, y, w, colW, fontFace: F, border: { type: 'solid', pt: 1, color: INK }, margin: [0.03, 0.1, 0.03, 0.1], rowH: o.rowH });
}

// ---- header / footer (term voice)
let PAGE = 0;
function header(s, num, title, sub, active) {
  const tw = title.length * 0.255 + 0.15;
  T(s, num, M, 0.22, 0.7, 0.6, { fontSize: 30, bold: true, color: NAVY, valign: 'middle', fontFace: F });
  T(s, title, M + 0.72, 0.22, tw, 0.6, { fontSize: 17, bold: true, valign: 'middle', charSpacing: -0.3 });
  const bx = M + 0.72 + tw + 0.05;
  R(s, bx, 0.36, 0.045, 0.32, NAVY);
  T(s, sub, bx + 0.14, 0.22, 4.6, 0.6, { fontSize: 11.5, color: MUTED, valign: 'middle' });
  const sx = bx + 0.14 + sub.length * 0.185 + 0.2;
  const tabX = 12.83 - 3 * 1.2 - 0.0;
  if (sx < tabX - 0.2) HL(s, sx, 0.52, tabX - 0.15 - sx, NAVY, 0.75);
  SEC.forEach((t, i) => {
    const on = i === active;
    s.addText(t, { x: tabX + i * 1.2 + 0.0, y: 0.38, w: 1.16, h: 0.28, fontFace: F, fontSize: 8, bold: on, align: 'center', valign: 'middle', margin: 0, isTextBox: true, color: on ? 'FFFFFF' : TABOFF, fill: { color: on ? NAVY : SOFT } });
  });
}
function footer(s, source, page) {
  T(s, '停動館', M, 7.0, 1.1, 0.4, { fontFace: SERIF, bold: true, fontSize: 16, color: NAVY, valign: 'middle' });
  HL(s, 1.65, 7.02, 11.18, '7F7F7F', 0.5);
  T(s, '출처: ' + source, 1.65, 7.06, 9.55, 0.4, { fontSize: 8.5, color: MUTED, valign: 'top' });
  T(s, '담당자 정성윤 · ' + String(page).padStart(2, '0'), 11.2, 7.06, 1.63, 0.34, { fontSize: 8, color: MUTED, align: 'right' });
}
function slide(num, title, sub, active, source, notes) {
  sec(active);
  const s = pres.addSlide({ masterName: 'GS', sectionTitle: SEC[active] });
  PAGE += 1;
  header(s, num, title, sub, active);
  footer(s, source, PAGE + 0);
  if (notes) s.addNotes(notes);
  return s;
}
const nextPage = () => PAGE + 1;

// =====================================================================
// 01 TitleSlide
{
  sec(0);
  const s = pres.addSlide({ masterName: 'GS', sectionTitle: SEC[0] }); PAGE += 1;
  s.background = { color: 'FFFFFF' };
  s.addImage({ path: find('cover_hero.png'), x: SW - 7.9, y: 0, w: 7.9, h: 7.5 });
  T(s, '2026 · 공학설계기초', 0.7, 0.75, 6, 0.4, { fontSize: 15, bold: true });
  T(s, '전포동', 0.7, 1.7, 6.5, 1.0, { fontSize: 50, bold: true, charSpacing: -1 });
  T(s, '복합주차장 정동관', 0.7, 2.75, 7.2, 1.0, { fontSize: 50, bold: true, color: NAVY, charSpacing: -1 });
  T(s, '건축계획', 0.7, 3.8, 6.5, 1.0, { fontSize: 50, bold: true, charSpacing: -1 });
  T(s, '낮에는 주차장, 밤에는 공연과 옥상 광장', 0.7, 5.15, 6.4, 0.4, { fontSize: 15, color: MUTED });
  T(s, '부산진구 전포동 207번지 일대 53필지 4,964.5㎡\n지하 4층 · 지상 6층 + 옥상 · 연면적 43,623.7㎡ · 주차 약 600대', 0.7, 5.65, 6.4, 0.7, { fontSize: 11, color: INK });
  T(s, '202325137 정성윤', 0.7, 6.75, 4, 0.3, { fontSize: 12, bold: true });
  T(s, '停動館', SW - 3.6, 6.35, 3.2, 0.9, { fontFace: SERIF, fontSize: 46, bold: true, color: 'FFFFFF', transparency: 100, outline: { size: 1.5, color: 'FFFFFF' }, align: 'right', valign: 'middle' });
  R(s, SW - 6.15, 7.13, 6.15, 0.37, '101216');
  T(s, '투시도는 개념 볼륨 모델로 만든 이미지이며 실제 설계안이 아님', SW - 6.0, 7.13, 5.8, 0.37, { fontSize: 9, color: 'FFFFFF', align: 'right', valign: 'middle' });
}

// =====================================================================
// 02 Contents
{
  sec(0);
  const s = pres.addSlide({ masterName: 'GS', sectionTitle: SEC[0] }); PAGE += 1;
  R(s, SW - 4.7, 0, 4.7, 7.5, NSOFT);
  s.addImage({ path: find('contents_art.jpg'), x: SW - 4.5, y: 0, w: 4.5, h: 7.5 });
  T(s, '停動館', SW - 4.5, 6.35, 4.1, 0.9, { fontFace: SERIF, fontSize: 50, bold: true, color: 'FFFFFF', transparency: 100, outline: { size: 1.5, color: 'FFFFFF' }, align: 'right', valign: 'middle' });
  T(s, 'CONTENTS', 0.9, 0.85, 4, 0.7, { fontSize: 30, bold: true, color: NAVY, charSpacing: -0.5 });
  T(s, '전포 정동관 · 낮에는 주차장, 밤에는 공연과 옥상 광장', 0.9, 1.5, 6.5, 0.3, { fontSize: 11 });
  T(s, '발표자', 0.9, 5.9, 2, 0.25, { fontSize: 10 });
  T(s, '정성윤', 0.9, 6.15, 3, 0.4, { fontSize: 15, bold: true });
  const G = [
    ['INTRODUCTION', ['사업 배경 · 사업 개요'], 1.1],
    ['MAIN SUBJECT', ['대지 분석 · 부지 선정 · 교통 및 동선', '향 · 일조 · 소음 · 조망', '콘셉트 · 사례 분석', '볼륨 도출 · 최종안 · 투시도'], 2.35],
    ['CONCLUSION', ['용도 선정 · 층별 계획 · 단면도', '실별 면적 · 동선 및 진입', '법규 검토 · 구조 · 방재 제안', '확인할 것'], 4.45],
  ];
  G.forEach(([h, items, yy]) => {
    R(s, 5.1, yy + 0.04, 0.04, 0.26, INK);
    T(s, h, 5.25, yy, 3.4, 0.34, { fontSize: 13, bold: true, valign: 'middle' });
    T(s, items.map((t, i) => ({ text: '- ' + t, options: { breakLine: i < items.length - 1 } })), 5.4, yy + 0.42, 3.5, items.length * 0.28, { fontSize: 11, lineSpacingMultiple: 1.2 });
  });
}

// =====================================================================
// 03 사업 배경 · 개요
{
  const s = slide('01', '사업 배경 · 개요', '상권 한가운데 주차 공급이 모자란 곳', 0,
    '파이낸셜뉴스(2022.07.11), 부산일보(2024.07.04), 부산진구 수급실태조사(2023), 글로벌경제(2021), 전국주차장정보표준데이터(2026.04), 토지이음(2026.10.11) · 69.1%는 주차환경개선지구 67곳 평균',
    '확보율 = 주차면수 ÷ 주차수요 × 100. 69.1%는 상가밀집지역이 아니라 노후주거지 밀집 등 주차환경개선지구 67곳의 평균임.');
  barHeading(s, '주차장 확보율 비교 (%)', M, 1.0);
  s.addChart(pres.charts.BAR, [{ name: '확보율(%)', labels: ['부산 전체(2021)', '부산진구(2023)', '개선지구 평균'], values: [130.5, 118.5, 69.1] }], {
    x: M, y: 1.35, w: 4.95, h: 2.3, barDir: 'bar', chartColors: [NAVY, D2, SLATE], showValue: true, dataLabelFontSize: 12, dataLabelFontFace: F, dataLabelColor: 'FFFFFF', dataLabelPosition: 'inEnd',
    dataLabelFormatCode: '0.0', catAxisLabelFontSize: 11, catAxisLabelFontFace: F, catAxisLabelColor: INK, valAxisHidden: true, valAxisMaxVal: 150, valAxisMinVal: 0,
    valGridLine: { style: 'none' }, catGridLine: { style: 'none' }, showLegend: false, barGapWidthPct: 40, catAxisOrientation: 'maxMin' });
  cap(s, '기준 130% · 부산 전체는 2021년, 부산진구는 등록 대비 2023년 값', M, 3.68, 4.95);
  img(s, 'p_alley1.jpg', M, 4.1, 2.44, 2.05);
  img(s, 'p_alley2.jpg', M + 2.51, 4.1, 2.44, 2.05);
  cap(s, '전포동 이면도로 현장 (답사 2026.9)', M, 6.2, 4.95);

  const x2 = 5.8, w2 = 7.03;
  barHeading(s, '수급 실태 지표', x2, 1.0);
  table(s, ['지표', '값', '출처'], [
    ['부산진구 확보율(등록 대비)', '118.5%, 기준 130% 대비 약 1.7만 면 부족', '부산진구 수급실태조사(2023)'],
    ['대지 반경 500m 공영주차장', '27면 (1km 이내 약 415면)', '표준데이터, 시설공단'],
    ['부산진구 불법주정차 단속', '부산 1위 (2021.1~10월 109,993건)', '글로벌경제 2021'],
    ['시 공급 계획', '2025년까지 6,092면 · 1,995억 원', '부산시 주차종합계획'],
  ], x2, 1.35, w2, [2.35, 2.85, 1.83], { size: 10 });
  barHeading(s, '정동관 개요', x2, 3.3);
  specTable(s, [
    ['위치', '부산진구 전포동 207번지 일대 53필지 · 일반상업지역 · 방화지구'],
    ['대지 · 연면적', '4,964.5㎡ · 43,623.7㎡ (지상 23,923.7 + 지하 19,700.0)'],
    ['규모', '지하 4층 · 지상 6층 + 옥상, 지상 약 29.1m'],
    ['건폐율 · 용적률', '87.1% (상한 90%) · 481.9% (지하 제외)'],
    ['주차', '약 600대 · 주차 비율 75.62%'],
    ['주요 시설', '1F 서점·카페·근생 · 5F 상인회 · 6F 가변홀 · B1~B2 공연장 200석 · 옥상 광장'],
  ], x2, 3.65, w2, [1.35, 5.68], { size: 10, rowH: 0.34 });
  takeaway(s, '소규모 필지에 점포가 밀집해 부설주차장이 어려워, 상권 한가운데 거점형 주차장이 필요함', x2, 5.85, w2, { h: 0.98, size: 13, sub: '부산진구 확보율 118.5%(기준 130%) · 대지 반경 500m 공영주차장 27면' });
}

// =====================================================================
// 04 대지 분석
{
  const s = slide('02', '대지 분석', '53필지를 한 블록으로 쓰는 조건', 1,
    '토지이음 필지별 토지이용계획 조회(2026.10.11), 「부산광역시 건축 조례」 별표4 · 필지 위치는 확인도면 정합으로 판별함, 치수 개략');
  const h = imgW(s, 'site_eum.jpg', M, 1.0, 4.15);
  cap(s, '토지이용계획 확인도면 · 필지군 표시(개략)', M, 1.0 + h + 0.04, 4.15);
  const x2 = 4.95, w2 = 7.88;
  barHeading(s, '대지 개요', x2, 1.0);
  table(s, ['구역', '필지', '면적㎡', '형상 · 접도'], [
    ['서측 쐐기', '19', '1,531.9', '전포대로(서)에 면한 쐐기형, 남단이 뾰족함'],
    ['소로 부지', '5', '733.1', '두 구역 사이 폭 약 6m, 남단 전포대로 · 북단 서전로'],
    ['동측 블록', '29', '2,699.5', '서전로 · 224번길 · 동측 이면도로에 면한 삼각형'],
    ['합계', '53', '4,964.5', '지목 대 48필지, 도로 5필지'],
  ], x2, 1.35, w2, [1.3, 0.7, 1.1, 4.78], { size: 11.5, aligns: ['left', 'right', 'right', 'left'], boldRows: [3], rowH: 0.36 });
  barHeading(s, '배치 조건', x2, 3.35);
  labeledPanel(s, x2, 3.72, 3.8, [{ label: '용도지역 · 높이', items: [
    { title: '일반상업지역 · 방화지구', lines: ['가로구역별 최고높이 기준 130m, 최고 180m', '일조 제한은 주거지역에만 적용됨'] },
  ] }], { size: 11, minH: 2.3 });
  labeledPanel(s, x2 + 3.93, 3.72, 3.95, [{ label: '건축선 · 건폐율', items: [
    { title: '건축선 3m 이격', lines: ['공연장 1,000㎡ 이상으로 북·남 면을 띄움', '전포대로 쪽은 면제'] },
    { title: '두 뾰족한 끝을 비움', lines: ['동측 북단 약 352㎡, 서측 남단 약 158㎡', '건폐율 87.1%(상한 90%)'] },
  ] }], { size: 11, minH: 2.3 });
  noteBox(s, x2, 6.2, w2, 0.55, '확인할 것', '207-15·79는 제3종일반주거지역도 표기됨(상업지역으로 계산함). 207-84·85는 지목 대이나 도로로 쓰임');
}

// =====================================================================
// 05 부지 선정 · 교통 및 동선
{
  const s = slide('03', '부지 선정 · 교통 및 동선', '수요와 접근이 맞는 곳', 1,
    '카카오맵 도보 환산, 부산버스정보시스템(2026.9.30), 시설공단, 전국주차장정보표준데이터(2026.04), 시의회 5분 발언(2022.08) · 지도 © OpenStreetMap contributors');
  const h = imgW(s, 'transit_map.jpg', M, 1.0, 5.1);
  cap(s, '주변 현황도 · 위치 개략', M, 1.0 + h + 0.04, 5.1);
  const x2 = 5.95, w2 = 6.88;
  barHeading(s, '입지 근거', x2, 1.0);
  const cards = [['‘지하철 두 역 도보권’', '1호선 서면역 737m, 2호선 전포역 529m. 주차 이용객과 공연·광장 방문객이 걸어서 접근함'],
    ['‘카페거리 상권 사이’', '전리단길 · 전포카페거리 · 전포사잇길 사이. 낮 방문객과 밤 관객 수요를 함께 받음'],
    ['‘공영주차장 공백지대’', '반경 500m 공영 27면, 1km 약 415면. 2022 시의회에서 대지 옆 놀이마루 부지 공영주차장 건립이 제안됨']];
  cards.forEach((c, i) => {
    const y = 1.37 + i * 0.98;
    R(s, x2, y, w2, 0.9, SOFT);
    T(s, c[0], x2 + 0.2, y + 0.09, w2 - 0.4, 0.3, { fontSize: 12.5, bold: true, color: NAVY });
    T(s, c[1], x2 + 0.2, y + 0.42, w2 - 0.4, 0.5, { fontSize: 10.5 });
  });
  barHeading(s, '접근 계획', x2, 4.38);
  labeledPanel(s, x2, 4.72, 3.38, [{ label: '차량', items: [{ title: '남단 진입 · 북단 진출', lines: ['소로는 남→북 일방, 차량 전용', '400대 초과 입구·출구 분리'] }] }], { size: 10 });
  labeledPanel(s, x2 + 3.5, 4.72, 3.38, [{ label: '보행 · 수직', items: [{ title: '1층 외곽을 한 바퀴', lines: ['끝 코어 2곳(개방 순환 계단 + 승강기)', '동측 주거 쪽 주 차량 진출입 없음'] }] }], { size: 10 });
  takeaway(s, '두 역 도보권과 카페거리 사이, 공영주차장이 거의 없어 거점형 입지로 적합함', x2, 5.95, w2, { h: 0.9, size: 13, sub: '서면역 737m · 전포역 529m, 반경 500m 공영 27면 · 1km 약 415면' });
}

// =====================================================================
// 06 향 · 일조
{
  const s = slide('04', '향 · 일조', '남북 장축 블록의 일사와 그림자', 1,
    'NOAA 태양 위치 근사식(북위 35.157°), OpenStreetMap contributors(주변 건물 일부 누락), 본 시안 매스 계산 · 직사 시간은 고도 5° 이상, 가림 없음 가정',
    '그림자는 본 시안 매스(5F 지붕 21.1m, 6F 홀 29.8m)와 NOAA 근사식으로 계산함. 주변 건물은 OSM 등록분만 반영해 저층이 빠져 있음. 일조 판단 시간대는 동지 9~15시로 가정함. 정북 일조 제한은 주거지역에만 적용되어 상업지역 대지에는 해당하지 않음.');
  const w1 = 8.0;
  const h1 = imgW(s, 'shadow3.png', M, 1.0, w1);
  cap(s, '정동관 그림자 · 동지 09·12·15시, 지붕 설비 포함 높이 29.8m 기준 (붉은 선 = 대지, 점선 = 제3종일반주거 경계 약 45m)', M, 1.0 + h1 + 0.03, w1);
  const y2 = 1.0 + h1 + 0.45;
  const hm = imgH(s, 'shadow_hours.png', M, y2, 1.85);
  cap(s, '동지 09~15시 그림자 누적 시간', M, y2 + 1.87, hm, { align: 'left', fontSize: 8 });
  table(s, ['면', '직사 동지', '직사 하지', '관찰'], [
    ['서측 · 전포대로', '4.3h (오후)', '6.7h', '서향 일사와 도로 소음이 함께 닿는 면'],
    ['동측 · 이면도로', '4.3h (오전)', '6.8h', '동지 15시경에야 주거 경계에 이름'],
    ['남측 · 224번길', '8.6h', '6.9h', '동지 고도 31.4°로 깊이 들어옴'],
    ['북측 · 서전로', '0h', '새벽·저녁', '직사 없이 확산광, 그림자는 도로 쪽'],
  ], M + hm + 0.2, y2, w1 - hm - 0.2, [1.45, 0.95, 0.9, w1 - hm - 0.2 - 3.3], { size: 10, aligns: ['left', 'center', 'center', 'left'], rowH: 0.42 });
  const x2 = 8.85, w2 = 3.98;
  const hp = imgW(s, 'sunpath.png', x2 + 0.35, 1.0, 3.3);
  cap(s, '태양 경로 · 대지 위치 (원 안쪽이 높은 고도)', x2, 1.0 + hp + 0.02, w2);
  labeledPanel(s, x2, 1.0 + hp + 0.35, w2, [{ label: '관찰', items: [
    { title: '옥상 광장', lines: ['동지 9~15시 그림자 영향 없음', '홀(29.1m, 지붕 설비 포함 29.8m)이 광장의 북쪽에 있음'] },
    { title: '동측 주거 경계', lines: ['동지 9~15시 그림자 0.5h 미만'] },
  ] }], { size: 10 });
  takeaway(s, '서·동 면은 목재 슬랫으로 일사를 거르고, 광장과 근생은 남쪽에 둠', M, 6.2, w1, { h: 0.72, size: 13, sub: '직사 서측 4.3h(오후) · 남측 8.6h(동지) · 옥상 광장은 동지 9~15시 그림자 영향 없음' });
}

// =====================================================================
// 07 소음
{
  const s = slide('05', '소음', '서·북 도로변 소음원과 동측 주거 경계', 1,
    '「환경정책기본법 시행령」 별표, OpenStreetMap contributors, 현장 답사(2026.9) · 전포동 측정값 없음, dB은 개략 추정 · 사진: Petr Meissner, CC BY 2.0',
    '소음 분포는 실측이 아니라 개략 추정임. OSM 도로를 5m 간격 점음원으로 바꾸고 10m 기준 Leq를 광로·대로 70, 3차 63, 주거 58 dB(A)로 가정했으며 건물 차폐와 지면 효과는 넣지 않음. 부산시 소음 측정망에 전포동 지점이 없어 현장 낮·밤 실측으로 교체해야 함.');
  const wm = 3.95;
  const hm = imgW(s, 'noise_map.png', M, 1.0, wm);
  cap(s, '● = 면별 평가점(북·서·남·동·주거 경계)', M, 1.0 + hm + 0.02, wm);
  const py = 1.0 + hm + 0.3;
  img(s, 'n_p1.jpg', M, py, 1.27, 1.1); img(s, 'n_p2.jpg', M + 1.34, py, 1.27, 1.1); img(s, 'n_p3.jpg', M + 2.68, py, 1.27, 1.1);
  const x2 = 4.85, w2 = 4.05;
  barHeading(s, '소음 환경기준 (dB)', x2, 1.0);
  table(s, ['구분', '낮', '밤', '해당'], [
    ['일반지역 다(상업)', '65', '55', '대지'],
    ['도로변 다(상업)', '70', '60', '서·북 도로변'],
    ['일반지역 나(주거)', '55', '45', '동측 주거'],
    ['도로변 가·나(주거)', '65', '55', '동측 도로변'],
  ], x2, 1.35, w2, [1.6, 0.55, 0.55, 1.35], { size: 10.5, aligns: ['left', 'center', 'center', 'left'], rowH: 0.34 });
  barHeading(s, '면별 주간 추정치 (dB(A), 가정)', x2, 3.3);
  s.addChart(pres.charts.BAR, [{ name: '주간 Leq 추정', labels: ['북 · 서전로', '서 · 전포대로', '남 · 224번길', '동 · 이면도로', '동측 주거 경계'], values: [76, 72, 70, 69, 67] }], {
    x: x2, y: 3.65, w: w2, h: 2.4, barDir: 'bar', chartColors: [NAVY, NAVY, D2, D2, SLATE], showValue: true, dataLabelFontSize: 11, dataLabelFontFace: F, dataLabelColor: 'FFFFFF', dataLabelPosition: 'inEnd',
    catAxisLabelFontSize: 10, catAxisLabelFontFace: F, catAxisLabelColor: INK, valAxisHidden: true, valAxisMinVal: 0, valAxisMaxVal: 90, valGridLine: { style: 'none' }, catGridLine: { style: 'none' },
    showLegend: false, barGapWidthPct: 35, catAxisOrientation: 'maxMin' });
  const x3 = 9.15, w3 = 3.68;
  barHeading(s, '공간별 대응', x3, 1.0);
  labeledPanel(s, x3, 1.35, w3, [
    { label: '공연 · 홀', items: [
      { title: '지하 공연장 B1~B2', lines: ['박스인박스와 방진 바닥 제안', '선큰 마당 쪽 로비가 완충'], wrap: 1 },
      { title: '6F 가변홀', lines: ['이중 차음 지붕', '서·북 면은 닫고 남쪽 광장으로 개구'] } ] },
    { label: '주차 · 지원', items: [
      { title: '소로 · 램프', lines: ['2층 바닥이 덮은 높이 7m 통로'] },
      { title: '동측 하역 · 이륜차', lines: ['운영시간 제한 검토'] } ] },
    { label: '업무 · 상업', items: [
      { title: '5F 상인회', lines: ['동측 이면 쪽에 배치', '서측 면은 이중창 검토'] } ] },
  ], { size: 9.5, lineH: 0.19 });
  takeaway(s, '소음이 큰 실은 지하와 최상층 안쪽에 두고, 서·북 도로변 면은 닫음', M, 6.2, CW, { h: 0.72, size: 13, sub: '서·북 도로변 추정 72~76dB(A, 가정) · 동측 주거 경계 약 67dB(A) · 전포동 실측으로 교체 필요' });
}

// =====================================================================
// 08 조망
{
  const s = slide('06', '조망', '황령산 · BIFC · 서면 도심', 1,
    'OSM 좌표, 「위키백과」 황령산 427m · BIFC 289m, 본 시안 매스 · 앙각은 지면 8m 가정 · 사진: Christian Bolz, CC BY-SA 4.0',
    '황령산 정상(427m)은 OSM 좌표 기준 대지에서 동쪽 약 1.47km, BIFC(289m)는 남쪽 약 1.15km. 눈높이는 1층 1.6m, 옥상 광장 22.7m. 주변 건물은 OSM 등록분(반경 약 420m)만 반영해 저층이 빠져 있어 조망이 실제보다 열려 보일 수 있음.');
  const h = imgW(s, 'view_profile.png', M, 1.0, CW);
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

// =====================================================================
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

// =====================================================================
// case column (CaseSplit vocabulary: case on white, 적용방안 on panel-dark)
function caseCol(s, x, y, c) {
  const w = 6.05;
  T(s, c.name, x, y, w, 0.32, { fontSize: 14, bold: true });
  T(s, c.meta, x, y + 0.32, w, 0.25, { fontSize: 9.5, color: MUTED });
  img(s, c.photo, x, y + 0.62, 1.85, 2.5);
  img(s, c.draw, x + 1.85 + 0.05, y + 0.62, 4.15, 2.5);
  // legend (ZoneLegend style)
  const lg = [['FFC000', '핵심·적용'], ['A9BEE6', '공공·활성'], ['F4B8B8', '계단·코어'], ['B8D4A0', '램프·녹지']];
  lg.forEach(([col, t], i) => {
    const lx = x + 1.9 + i * 1.05;
    R(s, lx, y + 3.2, 0.14, 0.14, col);
    T(s, t, lx + 0.19, y + 3.16, 0.85, 0.22, { fontSize: 8.5, color: MUTED, valign: 'middle' });
  });
  const facts = c.facts.map((f, i) => ({ text: '✓ ' + f, options: { breakLine: i < c.facts.length - 1, paraSpaceAfter: 3 } }));
  T(s, facts, x, y + 3.45, w, 1.35, { fontSize: 10.5, lineSpacingMultiple: 1.05 });
  R(s, x, y + 4.85, w, 0.8, PDARK);
  T(s, '정동관 적용', x + 0.15, y + 4.85, 1.2, 0.8, { fontSize: 11, bold: true, color: GOLD, valign: 'middle' });
  T(s, c.apply, x + 1.4, y + 4.85, w - 1.55, 0.8, { fontSize: 11, color: 'FFFFFF', valign: 'middle' });
}

// =====================================================================
// case column (CaseSplit vocabulary: case on white, 적용방안 on panel-dark)
function caseCol(s, x, y, c) {
  const w = 6.05;
  T(s, c.name, x, y, w, 0.32, { fontSize: 14, bold: true });
  T(s, c.meta, x, y + 0.32, w, 0.25, { fontSize: 9.5, color: MUTED });
  img(s, c.photo, x, y + 0.62, 2.5, 2.5);
  img(s, c.draw, x + 2.5 + 0.05, y + 0.62, 3.5, 2.5);
  const facts = c.facts.map((f, i) => ({ text: '✓ ' + f, options: { breakLine: i < c.facts.length - 1, paraSpaceAfter: 3 } }));
  T(s, facts, x, y + 3.25, w, 1.5, { fontSize: 10.5, lineSpacingMultiple: 1.08 });
  R(s, x, y + 4.85, w, 0.8, PDARK);
  T(s, '정동관 적용', x + 0.15, y + 4.85, 1.2, 0.8, { fontSize: 11, bold: true, color: GOLD, valign: 'middle' });
  T(s, c.apply, x + 1.4, y + 4.85, w - 1.55, 0.8, { fontSize: 11, color: 'FFFFFF', valign: 'middle' });
}
// 10 사례 Ⅰ
{
  const s = slide('07', '사례 분석 Ⅰ', '좁은 상업 대지의 주차빌딩', 1,
    'ArchDaily · JOHO Architecture(헤르마 주차빌딩, 사진 Namgoong Sun · Jeonghoon Lee), arch2o, 서울경제 2016.02.26, 자체 조사(2026.9) · 다이어그램은 자체 작성 · 평택 JS타워 사진은 출처 미확인(저장소 자료), 도면 미공개로 사진 판독');
  caseCol(s, M, 1.0, { name: '헤르마 주차빌딩', meta: 'JOHO Architecture · 용인 죽전 카페거리 초입 · 2010', photo: 'c_herma.jpg', draw: 'd_herma.jpg',
    facts: ['①② 평면: 폭 약 14m의 사선 대지에서 램프 폭을 6m에서 3.3m로 줄이고 삼각 보이드를 계단이 감아 오름, ③ 코어는 평면 중앙에 둠', '④ 외피: 반투명 폴리카보네이트 패널과 타공 밴드, 층마다 개구 패턴이 달라 자연환기와 확산광을 얻음', '⑤ 1층 상가가 가로와 주차층 사이 완충이 되고 밤에는 차량 불빛이 외피를 통해 가로에 비침'],
    apply: '1층을 가로에 열고, 뾰족한 끝을 순환 계단 코어로 둠' });
  caseCol(s, M + 6.28, 1.0, { name: '평택 JS타워', meta: '평택 · 대지 2,505㎡', photo: 'c_js.jpg', draw: 'd_js.jpg',
    facts: ['① 상부: 수평 곡면 금속 루버 밴드가 층마다 이어져 주차층을 감싸고 일사와 외부 시선을 거름(사진 판독)', '② 1층: 흑벽돌 아치 상가가 가로를 향해 열리고 ③ 진출입은 중앙 한 곳으로 모음, ④ 벽돌 타공 띠가 상가와 주차층을 구분함', '단면: 스킵플로어로 램프 면적을 줄여 주차 효율을 높임(자체 작성 단면)'],
    apply: '2층 이상 스킵플로어, 줄인 램프 면적을 공연장에 배분함' });
}
// 11 사례 Ⅱ
{
  const s = slide('08', '사례 분석 Ⅱ', '주차 건물의 외피와 옥상', 1,
    'ArchDaily · dJGA + MODULO(Saint-Luc, 사진 Lieven Van Landschoot), JAJA Architects(Park ’n’ Play, 사진 Rasmus Hjortshøj / COAST), 자체 조사(2026.9)');
  caseCol(s, M, 1.0, { name: 'Saint-Luc 주차건물', meta: 'de Jong Gortemaker Algra + MODULO · 브뤼셀 · 2016', photo: 'c_saintluc.jpg', draw: 'd_saintluc.jpg',
    facts: ['①②③ 단면: 옥상 녹지 아래 지상 2층 · 지하 3층 데크(985대), 경사지에 묻혀 지붕이 녹지로 이어짐', '④ 협곡: 건물 둘레의 구불구불한 틈이 최하층까지 빛과 공기를 들임', '⑤ 외피: 물결치는 목재 슬랫 입면이 주차 데크를 감쌈'],
    apply: '주차층 외피를 목재 슬랫 스크린으로 구성, 두 끝을 비워 지하 공연장까지 빛을 내림' });
  caseCol(s, M + 6.28, 1.0, { name: 'Park ’n’ Play', meta: 'JAJA Architects · 코펜하겐 노르드하운 · 2016', photo: 'c_pnp.jpg', draw: 'd_pnp.jpg',
    facts: ['① 옥상: 지상 약 24m에서 시민에게 열린 놀이 · 운동 공간, 코펜하겐 항구 방향이 열림', '② 외부 공공계단 두 줄이 지상에서 옥상까지 비스듬히 이어짐(평면 코너 계단과 같은 동선)', '③ 플랜터 그리드와 타공 벽체가 주차층을 자연환기함, ④ 주차층 평면의 원형 램프가 층을 이음'],
    apply: '옥상 광장(약 1,380㎡)과 개방 순환 계단' });
}
// 12 사례 Ⅲ
{
  const s = slide('09', '사례 분석 Ⅲ', '공연과 행사를 담는 구조', 1,
    'ArchDaily · peter haimerl.architektur(Blaibach, 도면 · 사진 NAARO), Herzog & de Meuron(1111 Lincoln Road, 사진 Phillip Pessar, CC BY 2.0 · 삽입 사진 ArchDaily), 자체 조사(2026.9)');
  caseCol(s, M, 1.0, { name: 'Concert Hall Blaibach', meta: 'peter haimerl.architektur · 독일 바이에른 · 2014', photo: 'c_blaibach.jpg', draw: 'd_blaibach.jpg',
    facts: ['①② 평면: 200석 객석과 무대를 지하에 묻어 길게 배치, ③ 로비 · 바 · 화장실이 객석 위쪽에서 완충층이 됨', '④ 단면: 기울어진 화강암 블록만 지상에 노출, ⑤ 지하 로비와 ⑥ 계단이 블록 밑면에서 내려감', '콘크리트 셸이 음향과 차음을 함께 풀고, 지상 블록은 마을 광장의 랜드마크가 됨'],
    apply: '공연장을 B1~B2에 두고 선큰 마당에서 내려가는 진입' });
  caseCol(s, M + 6.28, 1.0, { name: '1111 Lincoln Road', meta: 'Herzog & de Meuron · 마이애미 비치 · 2010', photo: 'c_lincoln.jpg', draw: 'd_lincoln.jpg',
    facts: ['① 층고: 슬래브 · 기둥 · 램프만으로 이룬 개방 구조, 층고는 약 2.1m(주차)에서 최대 약 10.4m까지 변함', '② 중앙 계단과 보이드가 층 사이를 열고 ④ 주차 데크는 외기에 열림(공식 도면 S1 · 2층 평면)', '③ 1층 소매 14개 유닛이 가로를 향해 열리고 상부 층은 행사 · 문화 · 상업에 탄력적으로 쓰임'],
    apply: '6F 가변홀(층고 8m)과 5F 전환 층' });
}

// =====================================================================
// 13 볼륨 도출
{
  const s = slide('10', '볼륨 도출', '필지 합필에서 최종 볼륨까지', 1,
    '본 시안(개념 볼륨 스터디) · 면적은 개략이며 형태는 실제 설계안이 아님');
  const h = imgW(s, 'steps.jpg', M, 1.0, CW);
  const y = 1.0 + h + 0.2;
  table(s, ['단계', '결정', '이유'], [
    ['① 53필지 합필', '서측 + 소로 + 동측 4,964.5㎡', '서측 쐐기만으로는 건축 가능 바닥이 약 920㎡라 램프가 면적을 잠식함'],
    ['② 소로 = 차량 전용 차로', '1층 층고 7m, 차로 위는 비움', '차량을 소로에 모으고 가로에는 차가 드나들지 않게 함'],
    ['③ 2층부터 한 판', '소로 위로 이은 바닥, 북·남 3m 이격', '한 층 4,322.1㎡의 정형 바닥, 법정 이격 확보'],
    ['④ 두 끝을 비워 코어로', '개방 순환 계단 + 승강기, 건폐율 87.1%', '주차가 어려운 좁은 끝을 사람 이동의 중심으로 씀'],
    ['⑤ 스킵플로어 · 홀 · 광장', '서·동 판을 반 층 엇갈림, 6F 가변홀, 옥상 광장', '램프를 줄이고 비는 시간과 위아래 층에 공연·체육·광장을 담음'],
  ], M, y, CW, [2.6, 4.0, 5.73], { size: 11.5, rowH: 0.4 });
  takeaway(s, '필지를 채우되 법정 이격과 건폐율은 두 끝을 비워 맞추고, 비운 자리가 건물의 얼굴이 됨', M, 6.25, CW, { h: 0.68, size: 13, sub: '건폐율 87.1%(상한 90%) · 비운 끝 코어 동측 약 352㎡ + 서측 약 158㎡ · 북·남 3m 이격' });
}

// =====================================================================
// 14 최종안
{
  const s = slide('11', '최종안', 'Final Draft와 요구 · 의도', 1,
    '본 시안(면적 계산 · 투시도), 「주차장법」 제12조의2 · 모든 수치는 개략');
  img(s, 'final_aerial.jpg', M, 1.0, 6.4, 3.6);
  cap(s, '조감 투시도 · 남서쪽 상공', M, 4.63, 6.4);
  const st = [['4,964.5㎡', '대지면적'], ['43,623.7㎡', '연면적'], ['87.1%', '건폐율'], ['약 600대', '주차']];
  st.forEach((t, i) => {
    const x = M + i * 1.62;
    R(s, x, 5.0, 1.54, 1.05, PANEL);
    T(s, t[0], x, 5.1, 1.54, 0.45, { fontSize: 14, bold: true, color: NAVY, align: 'center', valign: 'middle' });
    T(s, t[1], x, 5.58, 1.54, 0.3, { fontSize: 9.5, color: MUTED, align: 'center' });
  });
  // intent panel
  const x2 = 7.2, w2 = 5.63;
  s.addText('사업 요구', { x: x2, y: 1.0, w: 1.2, h: 0.32, fontFace: F, fontSize: 10, bold: true, color: MUTED, fill: { color: SOFT }, align: 'center', valign: 'middle', margin: 0, isTextBox: true });
  s.addText('설계 의도', { x: x2 + 1.25, y: 1.0, w: 1.2, h: 0.32, fontFace: F, fontSize: 10, bold: true, color: 'FFFFFF', fill: { color: NAVY }, align: 'center', valign: 'middle', margin: 0, isTextBox: true });
  s.addShape(pres.shapes.RECTANGLE, { x: x2, y: 1.32, w: w2, h: 1.0, fill: { color: 'FFFFFF' }, line: { color: NAVY, width: 1 } });
  T(s, [{ text: '주차를 한 블록에 모아 상권의 주차 부족과 이면도로 불법주차를 흡수함', options: { bullet: { indent: 12 }, breakLine: true } }, { text: '비는 시간과 위아래 층에 공연 · 체육 · 광장을 담음', options: { bullet: { indent: 12 }, breakLine: true } }, { text: '상인회와 주민이 쓰는 공용 공간을 둠', options: { bullet: { indent: 12 } } }], x2 + 0.15, 1.38, w2 - 0.3, 0.9, { fontSize: 10, valign: 'middle' });
  R(s, x2, 2.5, 1.9, 0.28, NAVY);
  T(s, '요구 및 의도 Check', x2, 2.5, 1.9, 0.28, { fontSize: 9, bold: true, color: 'FFFFFF', align: 'center', valign: 'middle' });
  R(s, x2, 2.78, w2, 0.82, CALLOUT);
  T(s, [{ text: '필요 시설을 한 블록에 모두 배치한 것 확인', options: { breakLine: true } }, { text: [{ text: '주차 비율 75.62%', options: { color: GOLD, bold: true } }].map((r) => r.text).join('') + '(요건 70% 이상)로 주차전용건축물 요건 충족', options: { breakLine: true } }, { text: '차량 동선(소로)과 보행 동선(1층 외곽) 분리 확인' }], x2 + 0.15, 2.8, w2 - 0.3, 0.78, { fontSize: 9.5, color: 'FFFFFF', align: 'center', valign: 'middle' });
  barHeading(s, '최종안 요약', x2, 3.78, 3);
  table(s, null, [
    ['1층', '서측 서점 · 카페 · 공연 로비 / 소로 차량 전용 차로 / 동측 근생 · 램프 · 정산 · 이륜차'],
    ['2~4층', '스킵플로어 주차 (서측 판 7.0 · 10.3 · 13.6m, 동측 판 +1.65m)'],
    ['5층', '상인회 · 회의 · 공유오피스 1,200㎡ + 전환 가능 주차층'],
    ['6층 · 옥상', '생활체육 · 공연 가변홀(층고 8m) + 옥상 광장 약 1,380㎡'],
    ['지하', 'B1 · B2 공연장 200석(선큰 마당으로 진입), B3 · B4 주차 · 설비'],
    ['코어 · 외피', '끝 코어 2곳 + 보조 피난계단 2곳, 주차층 목재 슬랫 스크린 · 검은 순환 계단'],
  ], x2, 4.13, w2, [1.0, 4.63], { size: 9.5, label: true, rowH: 0.42 });
}

// =====================================================================
// 15 투시도 Ⅰ
function renderSlide(num, title, sub, big, bigLabel, smalls, take, notes, sub2) {
  const s = slide(num, title, sub, 1,
    '투시도: 개념 볼륨 모델, Blender Cycles 렌더 · 하늘 HDRI · 텍스처 · 나무: Poly Haven(CC0) · 주변 건물: OpenStreetMap 높이 자료와 단순 가상 매스 · 실제 설계안이 아님', notes);
  const tag_ = (label, x, y) => s.addText(label, { x, y, w: Math.min(6.2, label.length * 0.125 + 0.4), h: 0.28, fontFace: F, fontSize: 9.5, bold: true, color: 'FFFFFF', fill: { color: NAVY }, margin: 0, align: 'center', valign: 'middle', isTextBox: true });
  img(s, big, M, 1.0, 7.65, 4.9);
  tag_(bigLabel, M + 0.1, 1.0 + 4.9 - 0.4);
  smalls.forEach(([f, label], i) => {
    const y = 1.0 + i * 2.5;
    img(s, f, 8.28, y, 4.55, 2.4);
    tag_(label, 8.28 + 0.1, y + 2.4 - 0.38);
  });
  takeaway(s, take, M, 6.05, CW, { h: 0.82, size: 13, sub: sub2 });
  return s;
}
renderSlide('12', '투시도 Ⅰ', '주간과 밤, 목재 슬랫 외피', 'r_big_hero.jpg', '주간 외관 · 전포대로(서측)에서 본 모습',
  [['r_small_night.jpg', '밤 · 주차층은 낮게, 1층과 6F 홀이 켜짐'], ['r_small_street.jpg', '서전로 × 전포대로 모퉁이 · 1층이 가로를 향해 열림']],
  '停은 목재 슬랫 스크린으로 차분하게, 動은 검은 순환 계단과 켜진 홀로 드러냄',
  '렌더는 Blender 5.2 Cycles(192 샘플, OpenImageDenoise)이며 외피 슬랫 재질은 Poly Haven dark_wood 텍스처를 사용함. 슬랫 폭 0.15m, 피치 0.24m는 가정값임.',
  '주차층 목재 슬랫(피치 0.24m 가정) · 끝 코어 순환 계단은 검은 도장 강재 · 6F 가변홀 층고 8m');
renderSlide('13', '투시도 Ⅱ', '옥상 광장 · 끝 코어 · 소로', 'r_big_roof.jpg', '옥상 광장 · 5F 지붕 +21.1m, 맞은편 6F 가변홀',
  [['r_small_sunken.jpg', '끝 코어 · 검은 순환 계단이 지상에서 이어짐'], ['r_small_lane.jpg', '소로 안 · 남→북 일방 차로, 위는 2층 바닥이 덮음']],
  '옥상 광장과 소로를 한 건물 안에서 보행과 차량으로 나눔',
  '소로 시점은 황혼 조도로 렌더함. 차량은 단순 모형이며 실제 계획과 무관함.',
  '옥상 광장 약 1,380㎡(+21.1m, 5F 지붕) · 소로는 남→북 일방, 2층 바닥이 덮은 높이 7m 통로');

// =====================================================================
// 16 용도 · 층별
{
  const s = slide('14', '용도 선정 · 층별 계획', '용도 여섯 가지와 층별 쓰임', 2,
    '부산진구 문화시설 · 공공체육시설현황(data.go.kr), 부산시 공연장목록, 현장 답사(2026.9), 본 시안 · 미등록 민간 공간은 빠졌을 수 있음');
  barHeading(s, '층별 용도 구성', M, 1.0);
  const hp = drawVector(s, 'program_stack.json', M, 1.35, 5.45);
  T(s, '지상 23,923.7㎡ + 지하 19,700.0㎡ = 연면적 43,623.7㎡', M, 1.35 + hp + 0.08, 6.0, 0.3, { fontSize: 10, bold: true });
  const x2 = 6.7, w2 = 6.13;
  barHeading(s, '용도별 위치와 선정 근거', x2, 1.0);
  table(s, ['용도', '위치', '면적㎡', '선정 근거'], [
    ['주차장', 'B4~5F, 1F 램프', '32,988.4', '부산진구 확보율 118.5%(기준 130%), 반경 500m 공영 27면'],
    ['공연장 200석', 'B1~B2', '1,900', '1km 안 객석형 소극장 없음, 지하는 전포대로 소음에 강함'],
    ['생활체육 · 공연 가변홀', '6F', '2,850', '1km 안 공연 겸용 가변 홀 없음, 행사에 따라 객석 · 코트를 바꿈'],
    ['서점 · 카페 · 근생', '1F', '1,400', '카페거리 방문객을 건물로 유도, 근생은 10곳 안팎 소점포'],
    ['상인회 · 공유오피스', '5F', '1,200', '답사 범위에서 상인회 사무실을 확인하지 못함'],
    ['옥상 광장', '5F 지붕', '약 1,380', '쉼터 · 공용 공간 부족, 밤에는 공연과 이어 개방'],
  ], x2, 1.35, w2, [1.45, 0.95, 0.85, 2.88], { size: 9.5, aligns: ['left', 'left', 'right', 'left'] });
  barHeading(s, '반경 내 현황조사 (대지 중심 직선거리)', x2, 4.6);
  table(s, ['구분', '500m 안', '1km 안'], [
    ['객석형 소극장', '없음 (지하 라이브클럽 1곳)', '없음 (스탠딩 라이브홀 · 연회장 · 1,727석 대극장)'],
    ['공공 체육관', '없음', '국민체육센터 0.73km (다목적체육관 1,394㎡)'],
    ['공연 겸용 가변 홀', '없음', '없음'],
  ], x2, 4.95, w2, [1.55, 1.7, 2.88], { size: 9.5 });
}

// =====================================================================
// 17 단면도
{
  const s = slide('15', '단면도', '소로를 따라 펼친 종단면과 횡단면', 2, '본 시안 개념 단면 · 구조 · 설비 두께는 표현하지 않음, 층고 · 면적 개략');
  const wa = 8.7;
  const ha = drawVector(s, 'secA.json', M, 1.0, wa);
  const hb = drawVector(s, 'secB.json', 9.45, 1.0, 2.75);
  imgW(s, 'keyplan.jpg', 12.3, 1.0, 0.55);
  cap(s, '단면선', 12.2, 2.0, 0.65, { fontSize: 8 });
  const y = Math.max(1.0 + ha, 1.0 + hb) + 0.3;
  labeledPanel(s, M, y, 6.05, [{ label: 'A 종단면', items: [
    { title: '① 공연장 200석 · ② 옥상 광장 · ③ 6F 가변홀 · ④ 개방 순환 계단 · ⑤ 특별피난계단', lines: ['두 끝은 지상에서 비어 있고 지하는 특별피난계단', '지하 공연장은 선큰 마당으로 빛이 닿음'], wrap: 1.5 }] }], { size: 10.5, minH: 1.55 });
  labeledPanel(s, M + 6.28, y, 6.05, [{ label: 'B 횡단면', items: [
    { title: '⑥ 서측 판 7.0 · 10.3 · 13.6m, 동측 판 +1.65m', lines: ['서 · 동 판이 소로 위에서 반 층 엇갈려 램프 길이를 줄임', '지하 공연장은 박스인박스와 방진 바닥으로 차량 진동 차단을 제안'] }] }], { size: 10.5, minH: 1.55 });
}

// =====================================================================
// 18 실별 면적
{
  const s = slide('16', '실별 면적', '지상 · 지하 면적과 구성비', 2, '본 시안 면적 계산(1평 = 3.3058㎡) · 3m 이격 · 끝 코어 2곳 · 보조 피난계단 2곳 반영, 모든 면적은 개략');
  barHeading(s, '층별 면적 (㎡)', M, 1.0);
  table(s, ['층', '주요 실', '면적㎡'], [
    ['6F', '체육 · 공연 가변홀 1,500.0 · 다목적 · 연습실 700.0 · 공연 지원 650.0 · 코어 150.0', '3,000.0'],
    ['5F', '상인회 · 회의 · 공유오피스 1,200.0 · 주차(전환 가능) 2,972.1 · 코어 150.0', '4,322.1'],
    ['2~4F', '주차 4,172.1 · 코어 150.0 (층당)', '4,322.1'],
    ['1F', '서점 400.0 · 카페 400.0 · 공연 로비 300.0 · 근생 600.0 · 램프 900.0 · 정산 100.0 · 이륜차 200.0 · 하역 150.0 · 기타 435.3 · 코어 150.0', '3,635.3'],
    ['B1', '공연장 로비 500.0 · 객석 상부 300.0 · 주차 3,856.5 · 코어 150.0', '4,806.5'],
    ['B2', '공연장 200석 800.0 · 분장 · 창고 300.0 · 주차 3,714.5 · 코어 150.0', '4,964.5'],
    ['B3', '전기 · 기계실 300.0 · 주차 4,514.5 · 코어 150.0', '4,964.5'],
    ['B4', '펌프 · 저수조 600.0 · 주차 4,214.5 · 코어 150.0', '4,964.5'],
    ['합계', '지상 23,923.7(7,237평) + 지하 19,700.0(5,959평)', '43,623.7'],
  ], M, 1.35, 7.55, [0.8, 5.65, 1.1], { size: 10.5, aligns: ['left', 'left', 'right'], boldRows: [8], rowH: 0.42 });
  takeaway(s, '주차 비율 75.62%로 주차전용건축물 요건을 충족하고 건폐율 87.1%로 맞춤', M, 5.85, 7.55, { h: 0.95, size: 13, sub: '건축면적 4,322.1㎡ · 용적률 481.9%(지하 제외, 특례 상한 1,500%) · 주차 70% 이상 요건' });
  const x2 = 8.4, w2 = 4.43;
  barHeading(s, '용도별 구성비', x2, 1.0);
  s.addChart(pres.charts.DOUGHNUT, [{ name: '구성비', labels: ['주차장', '문화 · 공연', '상업 · 상인', '코어', '설비 · 지원'], values: [75.62, 11.58, 5.96, 3.44, 3.4] }], {
    x: x2, y: 1.35, w: w2, h: 3.0, holeSize: 58, chartColors: [D1, D2, D3, D4, D5], showLegend: false, showPercent: false, showValue: false, dataBorder: { pt: 1.5, color: 'FFFFFF' } });
  T(s, '75.62%', x2 + w2 / 2 - 0.8, 2.4, 1.6, 0.5, { fontSize: 20, bold: true, color: NAVY, align: 'center' });
  T(s, '주차장', x2 + w2 / 2 - 0.8, 2.85, 1.6, 0.3, { fontSize: 10, color: MUTED, align: 'center' });
  const lg = [['주차장', '75.62% · 32,988.4㎡', D1], ['문화 · 공연', '11.58% · 5,050.0㎡', D2], ['상업 · 상인', '5.96% · 2,600.0㎡', D3], ['코어', '3.44% · 1,500.0㎡', D4], ['설비 · 지원', '3.40% · 1,485.3㎡', D5]];
  lg.forEach(([a, b, c], i) => {
    R(s, x2, 4.5 + i * 0.36, 0.24, 0.24, c);
    T(s, a, x2 + 0.35, 4.5 + i * 0.36, 1.5, 0.26, { fontSize: 10.5, bold: true, valign: 'middle' });
    T(s, b, x2 + 1.8, 4.5 + i * 0.36, 2.6, 0.26, { fontSize: 10.5, valign: 'middle' });
  });
  noteBox(s, x2, 6.2, w2, 0.62, null, '주차장 32,988.4㎡에는 1F 램프 · 정산 · 이륜차 1,200㎡가 포함됨. 주차 비율 75.62%(요건 70% 이상)', { size: 9.5 });
}

// =====================================================================
// 19 동선 및 진입
{
  const s = slide('17', '동선 및 진입 계획', '1층 배치와 수직 동선', 2, '본 시안 · 진출입 위치는 구청 · 경찰 협의 전 개념이며 도면은 개략, 「주차장법 시행규칙」 제5 · 6조');
  const h = 5.7; const w = imgH(s, 'plan1f.jpg', M, 1.0, h);
  cap(s, '1층 동선 개념도 · 위치와 폭은 개략', M, 1.0 + h + 0.02, w, { align: 'left' });
  const x2 = M + w + 0.35, w2 = 12.83 - x2, cw = (w2 - 0.2) / 2;
  labeledPanel(s, x2, 1.0, cw, [{ label: '차량 동선', items: [
    { title: '남단 진입 · 북단 진출', lines: ['소로는 남→북 일방, 차량 전용', '입구 · 출구가 서로 만나지 않음', '400대 초과 노외주차장의 분리 기준'], wrap: 1 }] }], { size: 10 });
  labeledPanel(s, x2 + cw + 0.2, 1.0, cw, [{ label: '보행 동선', items: [
    { title: '1층 외곽을 한 바퀴', lines: ['전포대로변, 북 · 남 3m 이격 마당, 동측 도로변', '소로 중간에 횡단보도 1곳', '서점 · 카페 · 로비는 전포대로 쪽'], wrap: 1 }] }], { size: 10 });
  labeledPanel(s, x2, 3.1, cw, [{ label: '수직 동선', items: [
    { title: '끝 코어 2곳이 이동의 중심', lines: ['지상 개방 순환 계단 + 승강기', '지하는 같은 자리에 특별피난계단', '공연 관객은 끝 코어②에서 선큰 마당으로'], wrap: 1 }] }], { size: 10 });
  labeledPanel(s, x2 + cw + 0.2, 3.1, cw, [{ label: '하역 · 이륜차', items: [
    { title: '동측 이면도로 쪽', lines: ['하역 150㎡, 이륜차 · 자전거 200㎡', '1층 동측 북쪽, 일반 차량과 분리', '주 진출입은 남·북단 소로만 사용'], wrap: 1 }] }], { size: 10 });
  takeaway(s, '차량은 소로에 모으고, 보행은 1층 외곽 중심으로 분리함(소로 횡단 1곳)', x2, 4.95, w2, { h: 0.72, size: 12.5, sub: '소로 남→북 일방 · 입구와 출구 분리(400대 초과) · 하역 150㎡ · 이륜차 200㎡는 동측' });
  noteBox(s, x2, 5.75, w2, 0.7, '확인할 것', '처리 용량(피크 대기행렬) · 소로 남단이 224번길 모퉁이 · 횡단보도 · 정류장과 떨어진 거리 · 출입구 설치 금지 구간(교차로 5m, 정류장 10m)');
}

// =====================================================================
// 20 법규 · 구조 · 방재
{
  const s = slide('18', '법규 검토 · 구조 · 방재 제안', '계획값과 조건부 항목', 2, '법제처 국가법령정보센터 현행본(2026.10.11 조회) · 판정은 참고용이며 최종 판단은 원문으로 다시 확인함 · 구조 · 방재는 확정 설계가 아닌 제안');
  table(s, ['항목', '조문', '기준', '계획값', '판정(참고)'], [
    ['주차전용건축물 요건', '「주차장법 시행령」 제1조의2', '주차 외 용도가 근생 · 문화집회 등이면 주차 70% 이상', '75.62%', '적합'],
    ['건폐율 · 용적률', '「주차장법」 제12조의2', '90% 이하 · 1,500% 이하', '87.1% · 481.9%', '적합'],
    ['대지 안의 공지', '「부산광역시 건축 조례」 별표4', '문화집회 1,000㎡ 이상: 건축선에서 3m (20m 이상 도로 면 면제)', '북 · 남 3m, 전포대로 0m', '적합(반영)'],
    ['노외주차장 출입구', '「주차장법 시행규칙」 제5조', '400대 초과 시 입구 · 출구 분리, 교차로 5m · 정류장 10m 안 금지', '남단 진입 · 북단 진출 분리', '조건부'],
    ['주차장 구조', '「주차장법 시행규칙」 제6조', '경사로 직선 17% · 곡선 14% 이하, 주차부분 높이 2.1m', '층고 3.3m, 반 층 램프', '조건부'],
    ['피난', '「건축법 시행령」 제34 · 35조', '보행거리 50m(지하 공연장 30m), 지하 3층 이하 특별피난계단', '끝 코어 2 + 보조 2, 지하 특피 4', '조건부'],
  ], M, 1.0, CW, [2.1, 2.7, 3.9, 2.2, 1.43], { size: 10.5, rowH: 0.5 });
  const y = 4.75;
  labeledPanel(s, M, y, 3.95, [{ label: '구조', items: [{ title: '주차 모듈에 맞춘 기둥 격자', lines: ['약 7.5~8.1m 단위로 제안', '6F 가변홀은 트러스 · 전이보로 무주 공간 검토'] }] }], { size: 9.5, lineH: 0.19 });
  labeledPanel(s, M + 4.19, y, 3.95, [{ label: '방재 · 피난', items: [{ title: '지하 공연장과 순환 계단', lines: ['방화구획과 전용 특별피난계단(보행거리 30m)', '개방 순환 계단의 피난계단 인정 여부 검토'] }] }], { size: 9.5, lineH: 0.19 });
  labeledPanel(s, M + 8.38, y, 3.95, [{ label: '설비 · 운영', items: [{ title: '자연환기와 후속 과제', lines: ['개방 외피로 주차층 자연환기, 지하는 기계환기', '소음 · 조명 운영시간, 처리 용량은 후속 검토'] }] }], { size: 9.5, lineH: 0.19 });
  takeaway(s, '구조 · 방재는 확정 설계가 아닌 제안이며, 설계 단계에서 작도와 계산으로 검증함', M, 6.1, CW, { h: 0.78, size: 13, sub: '조건부 3건: 노외주차장 출입구(교차로 5m · 정류장 10m) · 주차장 구조(램프 17%) · 피난(보행거리 50m, 지하 공연장 30m)' });
}

// =====================================================================
// 사례 차용 외피 대안 3종 (CaseSplit vocabulary: 사례 사진 + 적용 렌더)
{
  const s = slide('19', '사례 차용 외피 대안', 'Saint-Luc · 1111 Lincoln Road · Blaibach', 2,
    '사진: ArchDaily(Saint-Luc Lieven Van Landschoot, Blaibach NAARO), Phillip Pessar CC BY 2.0(1111 Lincoln Road) · 투시도: Blender Cycles 렌더, 비용 · 법규 · 구조 검토 전',
    '기준안은 목재 슬랫 스크린(투시도 Ⅰ·Ⅱ). 아래 3안은 같은 매스에 사례의 외피 방식만 바꾼 비교용 렌더임. 평면 · 단면 · 면적은 바뀌지 않음.');
  const opts = [
    ['Alt 1', 'Saint-Luc 주차건물', '물결치는 목재 슬랫', 'c_saintluc.jpg', 'alt_saintluc.jpg',
      ['슬랫이 층 높이에 따라 물결치고, 슬랫마다 목재 톤이 다름', '옥상 광장을 녹지로 돌려 주는 방식도 함께 차용'],
      '한계: 슬랫 유지관리와 방화 · 내후성 검토 필요'],
    ['Alt 2', '1111 Lincoln Road', '외벽 없는 개방 슬래브', 'c_lincoln.jpg', 'alt_lincoln.jpg',
      ['외벽 없이 슬래브 · 기둥 · 램프만으로 구성, 주차 차량이 보임', '슬래브 단면이 그대로 외관이 되어 층고 변화가 드러남'],
      '한계: 서향 일사 · 도로 소음 차단 수단이 없어 6F 홀 보완 필요'],
    ['Alt 3', 'Concert Hall Blaibach', '화강암 골재 콘크리트 블록', 'c_blaibach.jpg', 'alt_blaibach.jpg',
      ['거친 화강암 칩 콘크리트 매스에 불규칙한 세로 슬릿으로 빛이 새어 나옴', '6F 홀과 주차층을 하나의 단단한 덩어리로 표현'],
      '한계: 자연환기 면적 부족, 기계환기 · 슬릿 방화 검토 필요'],
  ];
  const cw = 3.98, gap = 0.195;
  opts.forEach(([tg, name, sub, ref, f, bl, lim], i) => {
    const x = M + i * (cw + gap), y = 1.0;
    R(s, x, y, cw, 5.5, SOFT);
    s.addText(tg, { x: x + 0.15, y: y + 0.15, w: 0.75, h: 0.27, fontFace: F, fontSize: 10, bold: true, color: 'FFFFFF', fill: { color: NAVY }, align: 'center', valign: 'middle', margin: 0, isTextBox: true });
    T(s, name, x + 1.0, y + 0.12, cw - 1.15, 0.32, { fontSize: 14, bold: true, valign: 'middle' });
    T(s, sub, x + 0.15, y + 0.52, cw - 0.3, 0.26, { fontSize: 10, color: MUTED });
    img(s, f, x + 0.14, y + 0.86, cw - 0.28, 2.1);
    img(s, ref, x + 0.14, y + 3.08, 0.9, 1.22);
    T(s, '사례 사진', x + 0.14, y + 4.32, 0.9, 0.22, { fontSize: 8, italic: true, color: MUTED, align: 'center' });
    T(s, bl.map((t, k) => ({ text: t, options: { bullet: { indent: 10 }, breakLine: k < bl.length - 1, paraSpaceAfter: 4 } })), x + 1.18, y + 3.06, cw - 1.32, 1.5, { fontSize: 10, lineSpacingMultiple: 1.05 });
    R(s, x, y + 4.72, cw, 0.78, PDARK);
    T(s, lim, x + 0.15, y + 4.72, cw - 0.3, 0.78, { fontSize: 10, color: 'FFFFFF', valign: 'middle' });
  });
}

// =====================================================================
// 형태 대안 3종 (매스 스터디)
{
  const s = slide('20', '형태 대안 3종', '같은 대지, 다른 매스 · 규모는 비슷하게 유지', 2,
    '본 시안 매스 스터디 · 상부 바닥면적은 2층 이상 슬래브 면적 합(개략) · 외피는 Alt 1 · 2 · 3 방식을 각각 적용 · 법규 · 구조 · 주차 대수 검토 전',
    '기준안(상부 바닥면적 약 19,851㎡, 높이 29.8m)과 비교. 끝 코어 2곳과 1층 구성은 유지하고 2층 이상의 매스만 바꿈. 면적은 슬래브 폴리곤 면적 합이며 주차 대수는 재계산하지 않음.');
  const forms = [
    ['형태 A', '계단식 테라스', '남→북 1 · 2 · 4 · 6층', 'form_A.jpg', 'prof_A.png', '약 16,100㎡ (−19%) · 30.8m',
      ['단마다 녹지 테라스가 생겨 옥상 광장이 3개로 늘어남', '외피는 Saint-Luc식 물결 슬랫, 지붕을 녹지로 돌려 줌'],
      '한계: 바닥면적이 줄어 주차 대수 재검토 필요'],
    ['형태 B', '엇갈린 슬래브', '층마다 폭 · 위치 · 층고가 다름', 'form_B.jpg', 'prof_B.png', '약 18,600㎡ (−6%) · 31.4m',
      ['슬래브가 서로 내밀고 들어가 그림자와 처마가 생김', '1111 Lincoln Road처럼 외벽 없이 기둥 · 슬래브 · 램프만 보임'],
      '한계: 서향 일사 · 도로 소음 차단 수단이 없어 보완 필요'],
    ['형태 C', '대각선 협곡', '틈 폭 약 9m, 6F 홀이 위에서 이음', 'form_C.jpg', 'prof_C.png', '약 19,700㎡ (−1%) · 30.5m',
      ['매스를 대각선 틈으로 갈라 빛과 바람이 들고, 틈 안 검은 계단이 옥상까지 오름', '외피는 Blaibach식 화강암 골재 콘크리트와 세로 슬릿'],
      '한계: 두 판으로 나뉘어 동선 · 방화구획 · 코어 재계획 필요'],
  ];
  const cw = 3.98, gap = 0.195;
  forms.forEach(([tg, name, sub, f, prof, stat, bl, lim], i) => {
    const x = M + i * (cw + gap), y = 1.0;
    R(s, x, y, cw, 5.5, SOFT);
    s.addText(tg, { x: x + 0.15, y: y + 0.15, w: 0.95, h: 0.27, fontFace: F, fontSize: 10, bold: true, color: 'FFFFFF', fill: { color: NAVY }, align: 'center', valign: 'middle', margin: 0, isTextBox: true });
    T(s, name, x + 1.2, y + 0.12, cw - 1.35, 0.32, { fontSize: 14, bold: true, valign: 'middle' });
    T(s, sub, x + 0.15, y + 0.5, cw - 0.3, 0.26, { fontSize: 10, color: MUTED });
    img(s, f, x + 0.14, y + 0.82, cw - 0.28, 2.1);
    const pw = imgH(s, prof, x + 0.14, y + 3.05, 0.78);
    T(s, [{ text: '상부 바닥면적', options: { color: MUTED, fontSize: 9, breakLine: true } }, { text: stat, options: { bold: true, fontSize: 10.5, color: NAVY } }], x + 0.14 + pw + 0.12, y + 3.07, cw - pw - 0.4, 0.8, { valign: 'middle' });
    T(s, bl.map((t, k) => ({ text: t, options: { bullet: { indent: 10 }, breakLine: k < bl.length - 1, paraSpaceAfter: 3 } })), x + 0.2, y + 3.93, cw - 0.4, 0.8, { fontSize: 9.5, lineSpacingMultiple: 1.02 });
    R(s, x, y + 4.85, cw, 0.65, PDARK);
    T(s, lim, x + 0.15, y + 4.85, cw - 0.3, 0.65, { fontSize: 9.5, color: 'FFFFFF', valign: 'middle' });
  });
}

// =====================================================================
// 21 확인할 것 + THANK YOU
{
  const s = slide('21', '확인할 것', '한계와 다음 단계', 2, '본 시안의 열린 이슈 · 수치는 모두 개략이며 확정은 법규 원문 확인과 작도에서 이뤄짐');
  table(s, ['#', '확인할 것', '이유 · 방향'], [
    ['1', '약 600대와 주차 면적 약 33,000㎡의 관계', '1대당 약 55㎡로 계산됨, 기준층 배치로 확인'],
    ['2', '진입부(소로 남단)와 224번길 모퉁이 · 횡단보도 · 정류장 거리', '출입구 설치 금지 구간(5m · 10m)'],
    ['3', '개방 순환 계단의 피난계단 인정 여부', '안 되면 보조 피난계단 2곳이 법정 계단 역할'],
    ['4', '대지 안의 공지의 지하층 적용 여부', '지금은 지하를 대지 전체로 계산'],
    ['5', '207-15 · 79 용도지역 표기', '제3종일반주거지역 동시 표기'],
    ['6', '보행거리 작도(코어 4곳 50m, 지하 공연장 30m)', '피난 조건부 판정 해소'],
    ['7', '6F 외피 재료, 소음 · 조명 운영시간, 소음 실측', '후속 설계 과제'],
  ], M, 1.0, 8.2, [0.45, 4.45, 3.3], { size: 11, aligns: ['center', 'left', 'left'], rowH: 0.55 });
  noteBox(s, M, 5.6, 8.2, 0.9, '본 보고서에서 다루지 않은 사항', '사업성(토지 매입 · 공사비 · 주차 수입) · 합필 방식과 운영 주체 · 침수 · 지반 · 소음 실측 · 상세 평면 · 단면(미작성)', { size: 10 });
  R(s, 9.0, 1.0, 3.83, 5.85, DIVG);
  T(s, 'THANK\nYOU', 9.0, 1.5, 3.83, 2.2, { fontSize: 48, bold: true, color: 'FFFFFF', transparency: 100, outline: { size: 1.5, color: 'FFFFFF' }, align: 'center', valign: 'middle' });
  T(s, '停動館', 9.0, 3.9, 3.83, 0.9, { fontFace: SERIF, fontSize: 34, bold: true, color: 'FFFFFF', align: 'center', valign: 'middle' });
  T(s, '전포 정동관\n낮에는 주차장, 밤에는 공연과 옥상 광장', 9.2, 4.9, 3.43, 0.7, { fontSize: 11, color: 'FFFFFF', align: 'center' });
  T(s, '202325137 정성윤', 9.2, 6.1, 3.43, 0.4, { fontSize: 11, bold: true, color: 'FFFFFF', align: 'center' });
}

module.exports = { pres };
if (require.main === module) {
  pres.writeFile({ fileName: path.join(__dirname, 'jeongdonggwan_gs.pptx') }).then((f) => { require('child_process').execFileSync('python', ['-I', path.join(__dirname, 'nobreak.py'), f], { stdio: 'inherit' }); console.log('wrote', f); });
}
