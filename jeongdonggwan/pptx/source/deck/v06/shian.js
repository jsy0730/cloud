'use strict';
// 사업 배경 3쪽(03 · 04 · 05) 구조 시안 3종 — 내용은 v6과 같고 배치 · 도형만 바꿈
const fs = require('fs');
const path = require('path');
const L = require('./lay.js');
const { pres, C, FONT, SERIF, T, G, col, SP, rect, hline, vline, text, P, tag, barHeading, caption, imageW, imageH, imageBox, labeledPanel, panelHeight,
  noteBox, noteHeight, table, slide, sec } = L;
const SH = pres.shapes;
const WARN = [];
function check(name, bottom, limit) { if (bottom > limit + 0.005) WARN.push(`${name}: bottom ${bottom.toFixed(2)} > limit ${limit.toFixed(2)}`); }
const YB = G.YB, Y0 = G.Y0, X0 = G.X0, W = G.W;
const GOLD = C.GOLD, NAVY = C.NAVY;

// ---------------------------------------------------------------- shared content (v6 문구 그대로)
const TL = [
  ['예부터', '갯가의 밭', '田浦(밭개), 갯가의 논밭에서 온 이름'],
  ['1960~70년대', '공구 골목', '공장과 공구 · 철물점 500여 곳이 모인 산업 골목'],
  ['2009년~', '카페거리', '빈 점포에 청년이 카페를 열고 2017년 뉴욕타임스에 소개'],
  ['2026년', '청년 상권', '카페거리 · 공구길 · 사잇길이 통합 운영단 협약'],
  ['다음', '정동관', '53필지 4,964.5㎡ · 주차 약 600대 · 공연장 200석 · 옥상 광장'],
];
const NOW = ['평일 저녁 약 1만 명, 주말 이틀 5만 명 이상 방문(2018, 구 집계)', '반경 500m 공영주차장 27면, 인근 사설 3~4곳', '불법주차가 몰리는 구간 약 300m', '2026.9 구청 공청회에서 주민이 주차 공간 확충을 요구'];
const NEXT = ['교육청 신청사 계획: 놀이마루 부지, 연면적 약 4.35만㎡, 2031 이전 목표', '2026.4 세 상권을 묶는 "전포 청년 상권" 운영단 협약', '계획 · 협약 단계이며 확정된 것은 아님'];
const SRC1 = '부산역사문화대전(전포동) · 부산시 · 동의대신문(전포카페거리) · 국제신문 2018.10 · 중도일보 2026.9 · 부산일보 2024.9(교육청 신청사) · 부산진구(2026.4 협약) · 문화일보(사당) · 전국주차장정보표준데이터(2026.04) / 사당 수치는 구청 발표, 다른 사업 병행';
const NOTE1 = '전포의 변천은 부산역사문화대전(밭개), 동의대신문 등(공구 골목 · 카페)을 따름. 방문객 수는 부산진구 집계를 인용한 2018년 보도이며 현재 수치가 아님. 교육청 신청사 · 청년 상권 협약은 계획 · 협약 단계이며 2026년 진행 상황은 확인하지 못함. 사당 사례는 구청 발표이고 같은 기간 에스컬레이터 설치 등 다른 사업이 함께 진행되어 주차 확충만의 효과로 볼 수 없음.';
const SENSE = [
  { v: '먹고', sub: '맛 · 카페 · 식당', st: '채워짐', lines: ['2009년 첫 카페 이후 카페거리로 성장, 지금은 식당 · 술집이 카페 자리까지 채움(2025)', '골목마다 맛집 투어 코스로 소개됨'] },
  { v: '보고', sub: '풍경 · 사진 · SNS 감성', st: '채워짐', lines: ['2017년 뉴욕타임스가 소개한 거리, 골목마다 SNS 감성 가게가 이어짐', 'MZ가 찾는 서면 3 · 4번가와 사잇길까지 번짐'] },
  { v: '듣고', sub: '공연 · 음악 · 소리', st: '비어 있음', lines: ['반경 500m 객석형 소극장 없음(지하 라이브클럽 1곳)', '1km 안에도 소극장급 공연장 없음, 스탠딩 라이브홀 · 연회장 · 대극장뿐', '부산 공연장 55곳, 서울 319곳(2022)'] },
];
const WHY = [
  { label: '규모의 공백', title: '200~300석이 없음', lines: ['"부산에는 제대로 된 200석, 300석 극장이 없다"(지역 연극 제작자)', '소극장은 너무 작고 큰 공연장은 대관비가 부담'] },
  { label: '제도의 공백', title: '라이브클럽은 공연장이 아님', lines: ['법적으로 식품접객업으로 분류되어 예술 지원에서 빠짐', '부산 인디 공연이 한 곳에 몰린다는 보도'] },
  { label: '위치의 공백', title: '골목 안에 들어올 자리가 없음', lines: ['임대료 오르는 상권에서 객석 공연장은 버티기 어려움', '부산 소극장 2020년 두 곳 폐관(임대료 · 코로나)'] },
];
const SRC2 = '부산일보 2025.9(전포카페거리) · 시빅뉴스(서면 3 · 4번가 르포) · 뉴욕타임스 2017 · 문화체육관광부 공연예술조사 2022 · 부산일보 2022(전용극장) · 고대신문(라이브클럽) · 서울문화재단 대학로 연극 실태조사 2013 · 본 조사(반경 내 현황조사, 2026.9)';
const NOTE2 = '먹고 · 보고 · 듣고의 구분은 이 보고서의 설명 틀이며 통계 분류가 아님. 공연장 수는 문체부 공연예술조사 2022년 집계(전국 968곳 중 서울 319, 부산 55)이며 집계 기준에 따라 다른 수치도 있음. 대학로 관객 지출은 2013년 조사(공연 전 약 1.0만 원 + 후 약 1.0만 원)로 현재 수치가 아님. 1km 안 공연 시설 목록은 본 조사에서 대지 중심 직선거리로 확인한 것.';
const LINK = '공연이 들어오면 먹고 · 보고와 이어짐: 대학로 관객은 공연 전후 1인당 약 2만 원을 식사 · 음료 · 주류에 씀(2013)';
const ARG = [
  { n: '①', t: '극장 하나만으론 살아남기 어려움', l: ['부산 소극장 2020년 두 곳 폐관(임대료 상승 · 코로나)', '대학로 소극장 비율 31% → 20%, 전 회차 매진에 가까워야 적자를 면함'] },
  { n: '②', t: '건물이 문화시설을 품어야 함', l: ['주차는 낮~저녁, 공연은 저녁~밤이라 같은 땅을 하루 두 번 씀', '주차 수입이 공연장 운영을 받치는 구조를 건물이 만듦(사업성은 별도 검토)'] },
  { n: '③', t: '주차 건물이라 공연 소음이 건물 안에서는 문제가 적음', l: ['같은 건물에 주거 · 숙박 · 학습처럼 소음에 민감한 용도가 없음(5F 업무 공간만 이중창으로 대응)', '공연장은 지하에 두고 주차층이 도로와의 완충이 됨'] },
];
const CASES = [
  { name: '1111 Lincoln Road', meta: '마이애미비치 · Herzog & de Meuron · 2010', photo: 'c_lincoln.jpg', big: '약 300대', big2: '+ 행사 700명', facts: ['주차 약 300대 + 행사 공간(최대 700명)', '층고를 키워 파티 · 패션쇼 · 콘서트에 씀'] },
  { name: 'Bold Tendencies', meta: '런던 Peckham · 다층 주차빌딩 상층부 · 2008~', photo: null, big: '155,631명', big2: '2018년 19주 · 31회 공연', facts: ['쓰지 않던 주차 상층부에서 오페라 · 오케스트라', '지자체와 장기 임대로 존속(2017)'] },
  { name: 'Concert Hall Blaibach', meta: '독일 바이에른 · peter haimerl · 2014', photo: 'c_blaibach.jpg', big: '200석', big2: '지하 홀 + 지상 화강암', facts: ['200석 홀을 지하에 묻고 지상은 화강암 블록', '지하라 소음에 강함 → 정동관 B1~B2'] },
  { name: 'Park ’n’ Play', meta: '코펜하겐 · JAJA Architects · 2016', photo: 'c_pnp.jpg', big: '485대', big2: '옥상 24m 시민 공간', facts: ['485대 주차빌딩 옥상(24m)을 시민 공간으로', '주차 위에 공공 공간 → 정동관 옥상 광장'] },
];
const SRC3 = '부산일보(소극장 폐관) · 경향신문 2023.12(대학로 소극장) · ArchDaily(1111 Lincoln Road · Park ’n’ Play · Blaibach) · miamiandbeaches.com · Bold Tendencies(boldtendencies.com) · theartsdesk / 국내에서 주차장과 공연장을 한 건물에 완공한 사례는 확인하지 못함(자체 조사)';
const NOTE3 = '대학로 소극장 비율은 문화지구 지정 이전 31%에서 20%로 줄었다는 경향신문 보도를 인용함. 부산 소극장 2020년 폐관은 부산일보 기획 기사 기준. 주차 수입의 공연장 교차 보조는 사업성 검토가 필요한 제안이며 본 시안 범위 밖. 소음 논리는 설계 논리이며 실측 · 차음 설계로 검증해야 함.';

// ---------------------------------------------------------------- helpers
let NUM = 0;
function mk(num, title, sub, source, notes, label) {
  const s = slide(num, title, sub, 0, source, notes);
  tag(s, label, X0, 0.02, { h: 0.2, sz: T.src, fill: GOLD, color: C.INK });
  return s;
}
function pill(s, label, x, y, w, o = {}) {
  s.addText(label, { x, y, w, h: o.h || 0.3, fontFace: FONT, fontSize: o.sz || T.small, bold: true, align: 'center', valign: 'middle', margin: 0, isTextBox: true,
    color: o.color || C.NAVY, fill: { color: o.fill || C.NSOFT } });
}
function bullets(s, lines, x, y, w, o = {}) {
  return text(s, lines.map((t) => P(t, o.sz || T.small, { ind: o.ind || 10, sa: o.sa === undefined ? 3 : o.sa, color: o.color || C.INK })), x, y, w, o.h ? { h: o.h } : {});
}
function barChart(s, x, y, w, h, o = {}) {
  s.addChart(pres.charts.BAR, [{ name: '확보율(%)', labels: ['부산 전체(2021)', '부산진구(2023)', '개선지구 평균'], values: [130.5, 118.5, 69.1] }], {
    x, y, w, h, barDir: 'bar', chartColors: [C.NAVY, C.D2, C.SLATE], showValue: true, dataLabelFontSize: T.small, dataLabelFontFace: FONT, dataLabelColor: 'FFFFFF',
    dataLabelPosition: 'inEnd', dataLabelFormatCode: '0.0', catAxisLabelFontSize: T.small, catAxisLabelFontFace: FONT, catAxisLabelColor: C.INK, valAxisHidden: true,
    valAxisMaxVal: 150, valAxisMinVal: 0, valGridLine: { style: 'none' }, catGridLine: { style: 'none' }, showLegend: false, barGapWidthPct: 40, catAxisOrientation: 'maxMin' });
}
function caseImg(s, c, x, y, w, h, o = {}) {
  if (c.photo) { imageBox(s, c.photo, x, y, w, h); return; }
  rect(s, x, y, w, h, C.NSOFT);
  if (o.small) { text(s, [P('주차빌딩', T.cap, { b: true, color: C.NAVY, align: 'center' }), P('상층부', T.cap, { b: true, color: C.NAVY, align: 'center' })], x, y, w, { h, valign: 'middle' }); return; }
  text(s, [P('155,631명', T.h2, { b: true, color: C.NAVY, align: 'center', sa: 3 }), P('2018년 19주 · 31회 공연', T.cap, { color: C.MUTED, align: 'center' })], x + 0.04, y, w - 0.08, { h, valign: 'middle' });
}
function circle(s, label, x, y, d, o = {}) {
  s.addText(label, { shape: SH.OVAL, x, y, w: d, h: d, fontFace: FONT, fontSize: o.sz || 34, bold: true, align: 'center', valign: 'middle', margin: 0, isTextBox: true,
    color: o.color || C.NAVY, fill: o.fill ? { color: o.fill } : { type: 'none' }, line: o.line ? { color: o.line, width: o.lw || 2.25, dashType: o.dash || 'solid' } : { type: 'none' } });
}
function plate(s, label, x, y, w, h, fill, o = {}) {
  s.addText(label, { shape: o.shape || SH.PENTAGON, x, y, w, h, fontFace: FONT, fontSize: o.sz || T.body, bold: true, align: o.align || 'left', valign: 'middle', margin: [(o.ml === undefined ? 0.15 : o.ml) * 72, (o.mr === undefined ? 0.25 : o.mr) * 72, 0, 0], isTextBox: true,
    color: o.color || C.WHITE, fill: { color: fill }, line: { type: 'none' } });
}

// =====================================================================  비교 안내 쪽
{
  const s = slide('00', '사업 배경 3쪽 구조 시안', '같은 내용을 세 가지 구조로 배치함', 0, '본 시안 · 문구 · 수치는 v6 사업 배경 3쪽과 동일하며 배치와 도형만 바꿈', null);
  const t = table(s, X0, Y0, { cols: [1.55, 2.75, 3.1, 2.45, 2.483], head: ['시안', '3쪽 구성', '쓰는 도형', '잘 맞는 경우', '유의점'], size: T.body, rows: [
    [{ t: 'A 흐름형', b: true, color: C.NAVY }, '03 시간 흐름 띠(쉐브론) + 지금 ▶ 앞으로 / 04 원 3개(먹고 + 보고 + 듣고) / 05 단계 화살 3칸 + 사례 카드 4장', '쉐브론 · 원(점선 원 = 빈칸) · 오각 화살 · 삼각 화살', '말로 설명하며 순서를 따라갈 때', '도형이 많아 글자 수는 줄여야 함'],
    [{ t: 'B 숫자형', b: true, color: C.NAVY }, '03 어두운 세로 띠 + 큰 숫자 타일 4개 / 04 좌 채움 2줄 · 우 어두운 "듣고" 블록 / 05 번호 레일 + 사례 2×2', '큰 숫자 타일 · 어두운 블록 · 번호 레일', '심사에서 숫자로 설득할 때', '숫자 출처를 타일마다 달아야 함'],
    [{ t: 'C 도식형', b: true, color: C.NAVY }, '03 과거 · 지금 · 앞으로 세 열 + 얇은 시간선 / 04 퍼즐 띠(빈 조각) + 공백 표 / 05 건물 단면 도식 + 사례', '퍼즐 띠 · 건물 단면 막대 · 세 열 면', '건물 계획 논리를 그림으로 보여 줄 때', '작도할 도식이 늘어 수정 부담이 큼'],
  ] });
  const y = Y0 + t.h + SP.s3;
  barHeading(s, '공통', X0, y, W);
  bullets(s, ['공설기 v1.2의 색 · 글꼴 역할 · 헤더 · 푸터는 그대로 두고 본문 배치와 도형만 바꿈', '내용 · 수치 · 출처는 v6과 같음(새 주장 없음)', '시안마다 03 · 04 · 05 세 쪽씩이며 채택한 시안을 본 덱의 사업 배경 쪽에 반영함'], X0, y + 0.45, W, { sz: T.body });
}

// ======================================================================================================= 시안 A · 흐름형
{
  const s = mk('03', '사업 배경 Ⅰ', '사람을 받아 온 땅이 이제 차와 사람을 함께 받을 차례임', SRC1, NOTE1, '시안 A · 흐름형');
  // row 1: timeline chevrons (left) + photos (right)
  const tw = 8.35;
  barHeading(s, '전포가 받아 온 사람들', X0, Y0, tw);
  const cy = Y0 + 0.46, ch = 0.5, n = TL.length, ov = 0.12, cw = (tw + ov * (n - 1)) / n;
  const fills = [C.SLATE, C.SLATE, C.D3, C.D2, NAVY];
  TL.forEach((r, i) => {
    const x = X0 + i * (cw - ov);
    plate(s, r[0], x, cy, cw, ch, fills[i], { shape: SH.CHEVRON, sz: T.small, align: 'center', ml: 0.22, mr: 0.18 });
    const bw = cw - 0.2;
    text(s, [P(r[1], T.body, { b: true, color: i === n - 1 ? C.NAVY : C.INK, sa: 2 }), P(r[2], T.small, { color: C.MUTED })], x + 0.14, cy + ch + 0.1, bw, {});
  });
  const px = X0 + tw + SP.s3, pw = X0 + W - px;
  const phw = (pw - SP.s1) / 2, phh = 1.95;
  imageBox(s, 'p_alley1.jpg', px, Y0, phw, phh);
  imageBox(s, 'p_alley2.jpg', px + phw + SP.s1, Y0, phw, phh);
  caption(s, '전포동 이면도로 현장 (답사 2026.9)', px, Y0 + phh + 0.03, pw);
  // row 2: 지금 ▶ 앞으로 | chart + sadang
  const y2 = Y0 + 2.4, h2 = YB - y2;
  const pw2 = 3.95, gap = 0.5;
  const now = { label: '지금', sz: T.h2, lsz: T.lead, items: [{ title: '길 위에 서 있는 차', lines: NOW }] };
  const next = { label: '앞으로', sz: T.h2, lsz: T.lead, items: [{ title: '수요를 키우는 계획', lines: NEXT }] };
  labeledPanel(s, X0, y2, pw2, Object.assign({ h: h2 }, now));
  s.addShape(SH.RIGHT_ARROW, { x: X0 + pw2 + 0.08, y: y2 + h2 / 2 - 0.3, w: gap - 0.16, h: 0.6, fill: { color: C.SLATE }, line: { type: 'none' } });
  labeledPanel(s, X0 + pw2 + gap, y2, pw2, Object.assign({ h: h2 }, next));
  const rx = X0 + 2 * pw2 + gap + SP.s3, rw = X0 + W - rx;
  let yy = y2;
  yy += barHeading(s, '주차장 확보율 (%)', rx, yy, rw);
  barChart(s, rx, yy, rw, 1.25);
  yy += 1.25;
  yy += caption(s, '기준 130% · 개선지구는 노후주거지 등 67곳 평균', rx, yy, rw) + SP.s1;
  yy += barHeading(s, '주차 확충 후 상권(서울 사당)', rx, yy, rw);
  const sw = (rw - 2 * SP.s1) / 3;
  [['+4.5%', '유동인구'], ['+5.0%', '점포 수'], ['+10.2%', '상권 매출']].forEach((r, i) => {
    const x = rx + i * (sw + SP.s1);
    rect(s, x, yy, sw, 0.62, C.NSOFT);
    text(s, [P(r[0], T.h2, { b: true, color: NAVY, align: 'center' }), P(r[1], T.cap, { color: C.MUTED, align: 'center' })], x, yy + 0.04, sw, { h: 0.56, valign: 'middle' });
  });
  yy += 0.62 + SP.s1;
  text(s, [P('공영 145면 조성 후 · 구청 발표이며 다른 사업이 병행되어 주차 확충만의 효과는 아님', T.cap, { color: C.MUTED })], rx, yy, rw, {});
  check('A03', yy + 0.4, YB);
}
{
  const s = mk('04', '사업 배경 Ⅱ', '먹고 · 보고는 채워졌고 듣고만 비어 공연장이 필요함', SRC2, NOTE2, '시안 A · 흐름형');
  // left: three circles
  const lw = 7.7, d = 2.2, gx = (lw - 3 * d) / 2;
  const cy = Y0 + 0.45;
  const xs = [0, 1, 2].map((i) => X0 + i * (d + gx));
  circle(s, '먹고', xs[0], cy, d, { fill: C.NSOFT });
  circle(s, '보고', xs[1], cy, d, { fill: C.NSOFT });
  circle(s, '듣고', xs[2], cy, d, { line: GOLD, lw: 3, dash: 'dash', color: C.INK });
  [0, 1].forEach((i) => text(s, [P('+', 26, { b: true, color: C.MUTED, align: 'center' })], xs[i] + d, cy + d / 2 - 0.3, gx, { h: 0.6, valign: 'middle' }));
  SENSE.forEach((c, i) => {
    const x = xs[i];
    const dark = i === 2;
    pill(s, c.st, x + d / 2 - 0.55, cy + d + 0.14, 1.1, { fill: dark ? GOLD : C.NSOFT, color: dark ? C.INK : NAVY });
    text(s, [P(c.sub, T.small, { color: C.MUTED, align: 'center', sa: 5 })].concat(c.lines.map((t) => P(t, T.body, { ind: 10, sa: 4 }))), x - 0.12, cy + d + 0.58, d + 0.24, {});
  });
  // right: why
  const rx = X0 + lw + SP.s4, rw = X0 + W - rx;
  let y = Y0;
  y += barHeading(s, '왜 듣고만 비어 있는가', rx, y, rw);
  const hs = WHY.map((p) => L.measure([{ t: p.title, sz: T.lead, b: true, sa: 3 }].concat(p.lines.map((l) => ({ t: l, sz: T.small, ind: 9, sa: 1 }))), rw - 0.35).h + 0.22);
  const nH = noteHeight(rw, '연결', LINK);
  const room = YB - nH - SP.s2 - y;
  const grow = Math.max(0, (room - hs.reduce((a, b) => a + b, 0) - 2 * SP.s1) / 3);
  WHY.forEach((p, i) => {
    const h = hs[i] + grow;
    rect(s, rx, y, rw, h, C.SOFT);
    rect(s, rx, y, 0.06, h, GOLD);
    text(s, [P(p.label, T.fine, { b: true, color: C.NAVY, sa: 1 }), { runs: [{ t: p.title, b: true }], sz: T.lead, sa: 3 }].concat(p.lines.map((l) => P(l, T.small, { ind: 9, sa: 1 }))), rx + 0.2, y, rw - 0.3, { h, valign: 'middle' });
    y += h + SP.s1;
  });
  noteBox(s, rx, YB - nH, rw, '연결', LINK);
  check('A04', y, YB - nH);
}
{
  const s = mk('05', '사업 배경 Ⅲ', '주차장이 공연장을 받치고 공연장이 주차장을 살림', SRC3, NOTE3, '시안 A · 흐름형');
  const cw = (W - 2 * SP.s3) / 3;
  const fills = [C.SLATE, C.D2, NAVY];
  ARG.forEach((a, i) => {
    const x = X0 + i * (cw + SP.s3);
    plate(s, a.n + ' ' + a.t, x, Y0, cw + (i < 2 ? 0.1 : 0), 0.78, fills[i], { sz: T.small, ml: 0.18, mr: 0.4 });
    bullets(s, a.l, x + 0.05, Y0 + 0.92, cw - 0.2, { sz: T.body });
  });
  const y2 = Y0 + 2.45;
  const yb = y2 + barHeading(s, '한 건물 안에서 이미 이뤄지고 있음', X0, y2, W);
  const gw = (W - 3 * SP.s2) / 4;
  const ph = 1.3;
  const hAvail = YB - yb;
  CASES.forEach((c, i) => {
    const x = X0 + i * (gw + SP.s2);
    caseImg(s, c, x, yb, gw, ph);
    const ty = yb + ph + 0.08;
    text(s, [P(c.name, T.body, { b: true, sa: 1 }), P(c.meta, T.cap, { color: C.MUTED, sa: 4 })].concat(c.facts.map((f) => P(f, T.small, { ind: 9, sa: 2 }))), x, ty, gw, {});
  });
  caption(s, '국내에서 주차장과 공연장을 한 건물에 완공한 사례는 확인하지 못함', X0, YB - 0.22, W);
  void hAvail;
}

// ======================================================================================================= 시안 B · 숫자형
{
  const s = mk('03', '사업 배경 Ⅰ', '사람을 받아 온 땅이 이제 차와 사람을 함께 받을 차례임', SRC1, NOTE1, '시안 B · 숫자형');
  // left dark rail
  const lw = 3.9;
  rect(s, X0, Y0, lw, YB - Y0, C.PDARK);
  rect(s, X0, Y0, lw, 0.05, GOLD);
  text(s, [P('전포가 받아 온 사람들', T.lead, { b: true, color: C.WHITE })], X0 + 0.25, Y0 + 0.2, lw - 0.5, { h: 0.3 });
  const x0 = X0 + 0.32, y0 = Y0 + 0.78;
  const hs = TL.map((r) => L.measure([{ t: r[0] + '  ' + r[1], sz: T.body, b: true, sa: 2 }, { t: r[2], sz: T.small }], lw - 0.9).h);
  const avail = YB - 0.2 - y0;
  const gap = Math.max(0.1, (avail - hs.reduce((a, b) => a + b, 0)) / (TL.length - 1));
  let y = y0;
  vline(s, x0, y0 + 0.12, avail - 0.5, '4A4F5A', 1.25);
  TL.forEach((r, i) => {
    const last = i === TL.length - 1;
    s.addShape(SH.OVAL, { x: x0 - 0.075, y: y + 0.07, w: 0.15, h: 0.15, fill: { color: last ? GOLD : C.SLATE }, line: { type: 'none' } });
    text(s, [{ runs: [{ t: r[0] + '  ', color: GOLD, b: true }, { t: r[1], b: true, color: C.WHITE }], sz: T.body, sa: 2 }, P(r[2], T.small, { color: last ? C.WHITE : 'C9CED8' })], x0 + 0.28, y, lw - 0.9, {});
    y += hs[i] + gap;
  });
  // right: stat tiles
  const rx = X0 + lw + SP.s3, rw = X0 + W - rx;
  const tw = (rw - 3 * SP.s1) / 4, th = 1.55;
  const stats = [
    ['1만 · 5만+', '평일 저녁 · 주말 이틀 방문 인원(2018, 구 집계)'],
    ['27면', '반경 500m 공영주차장, 인근 사설 3~4곳'],
    ['69.1%', '주차환경개선지구 평균 확보율(부산 전체 130.5%)'],
    ['+10.2%', '서울 사당 공영 145면 조성 후 상권 매출(구청 발표)'],
  ];
  stats.forEach((r, i) => {
    const x = rx + i * (tw + SP.s1);
    rect(s, x, Y0, tw, th, C.NSOFT);
    rect(s, x, Y0, tw, 0.05, NAVY);
    text(s, [P(r[0], i === 0 ? 24 : 28, { b: true, color: NAVY, sa: 4 }), P(r[1], T.small)], x + 0.14, Y0 + 0.12, tw - 0.28, { h: th - 0.2 });
  });
  // middle: chart + photos
  const y2 = Y0 + th + SP.s2;
  const half = (rw - SP.s3) / 2;
  let yc = y2;
  yc += barHeading(s, '주차장 확보율 (%)', rx, yc, half);
  const chH = 1.6;
  barChart(s, rx, yc, half, chH);
  caption(s, '기준 130% · 개선지구는 노후주거지 등 67곳 평균', rx, yc + chH, half);
  const px = rx + half + SP.s3;
  const pw = (half - SP.s1) / 2, ph = chH + 0.4;
  imageBox(s, 'p_alley1.jpg', px, y2, pw, ph + 0.0);
  imageBox(s, 'p_alley2.jpg', px + pw + SP.s1, y2, pw, ph);
  caption(s, '전포동 이면도로 현장 (답사 2026.9)', px, y2 + ph + 0.03, half);
  // bottom: 지금 + 앞으로 bands
  const y3 = y2 + ph + 0.4;
  const hb = YB - y3;
  const cwid = (rw - SP.s3) / 2;
  const nowL = NOW.slice(2);
  rect(s, rx, y3, cwid, hb, C.SOFT);
  text(s, [P('지금 +', T.body, { b: true, color: NAVY, sa: 3 })].concat(nowL.map((t) => P(t, T.small, { ind: 9, sa: 3 }))), rx + 0.16, y3, cwid - 0.3, { h: hb, valign: 'middle' });
  rect(s, rx + cwid + SP.s3, y3, cwid, hb, C.SOFT);
  text(s, [P('앞으로', T.body, { b: true, color: NAVY, sa: 3 })].concat(NEXT.map((t) => P(t, T.small, { ind: 9, sa: 2 }))), rx + cwid + SP.s3 + 0.16, y3, cwid - 0.3, { h: hb, valign: 'middle' });
  check('B03', y3 + hb, YB);
}
{
  const s = mk('04', '사업 배경 Ⅱ', '먹고 · 보고는 채워졌고 듣고만 비어 공연장이 필요함', SRC2, NOTE2, '시안 B · 숫자형');
  const lw = 7.85;
  // 먹고 / 보고 rows
  const rh = 1.2;
  SENSE.slice(0, 2).forEach((c, i) => {
    const y = Y0 + i * (rh + SP.s1);
    rect(s, X0, y, lw, rh, C.SOFT);
    rect(s, X0, y, 1.9, rh, C.NSOFT);
    text(s, [P(c.v, 32, { b: true, color: NAVY, align: 'center', sa: 0 }), P(c.sub, T.cap, { color: C.MUTED, align: 'center' })], X0, y, 1.9, { h: rh, valign: 'middle' });
    text(s, c.lines.map((t) => P(t, T.body, { ind: 10, sa: 3 })), X0 + 2.1, y, lw - 3.25, { h: rh, valign: 'middle' });
    pill(s, c.st, X0 + lw - 1.15, y + rh / 2 - 0.15, 1.0);
  });
  // 3 gap cards
  const yg = Y0 + 2 * (rh + SP.s1) + SP.s1;
  const yb2 = yg + barHeading(s, '왜 듣고만 비어 있는가', X0, yg, lw);
  const gw = (lw - 2 * SP.s2) / 3;
  const nH = noteHeight(lw, '연결', LINK);
  const gh = YB - nH - SP.s2 - yb2;
  WHY.forEach((p, i) => {
    const x = X0 + i * (gw + SP.s2);
    s.addShape(SH.RECTANGLE, { x, y: yb2, w: gw, h: gh, fill: { type: 'none' }, line: { color: C.LINE, width: 0.75 } });
    text(s, [P(p.label, T.fine, { b: true, color: NAVY, sa: 2 }), P(p.title, T.body, { b: true, sa: 3 })].concat(p.lines.map((l) => P(l, T.small, { ind: 9, sa: 2 }))), x + 0.14, yb2 + 0.1, gw - 0.28, { h: gh - 0.2 });
  });
  noteBox(s, X0, YB - nH, lw, '연결', LINK);
  // right dark block
  const rx = X0 + lw + SP.s3, rw = X0 + W - rx;
  rect(s, rx, Y0, rw, YB - Y0, C.PDARK);
  rect(s, rx, Y0, rw, 0.05, GOLD);
  text(s, [P('듣고', 34, { b: true, color: GOLD })], rx + 0.25, Y0 + 0.2, 1.6, { h: 0.6, valign: 'middle' });
  pill(s, '비어 있음', rx + rw - 1.4, Y0 + 0.34, 1.15, { fill: GOLD, color: C.INK });
  text(s, [P('공연 · 음악 · 소리', T.small, { color: 'C9CED8' })], rx + 0.25, Y0 + 0.85, rw - 0.5, { h: 0.25 });
  hline(s, rx + 0.25, Y0 + 1.2, rw - 0.5, '4A4F5A', 0.75);
  text(s, [P('55 : 319', 34, { b: true, color: GOLD, sa: 2 }), P('부산 공연장 : 서울 공연장(2022)', T.small, { color: 'C9CED8' })], rx + 0.25, Y0 + 1.35, rw - 0.5, {});
  hline(s, rx + 0.25, Y0 + 2.5, rw - 0.5, '4A4F5A', 0.75);
  text(s, SENSE[2].lines.slice(0, 2).map((t) => P(t, T.lead, { ind: 12, sa: 14, color: C.WHITE })), rx + 0.25, Y0 + 2.75, rw - 0.5, {});
}
{
  const s = mk('05', '사업 배경 Ⅲ', '주차장이 공연장을 받치고 공연장이 주차장을 살림', SRC3, NOTE3, '시안 B · 숫자형');
  const lw = 4.7;
  barHeading(s, '왜 한 건물인가', X0, Y0, lw);
  const hs = ARG.map((a) => L.measure([{ t: a.t, sz: T.lead, b: true, sa: 4 }].concat(a.l.map((l) => ({ t: l, sz: T.small, ind: 9, sa: 2 }))), lw - 0.95).h);
  const y0 = Y0 + 0.5;
  const avail = YB - y0;
  const gap = Math.max(0.12, (avail - hs.reduce((a, b) => a + b, 0)) / 3);
  let y = y0;
  ARG.forEach((a, i) => {
    const h = hs[i];
    text(s, [P(String(i + 1), 40, { b: true, color: NAVY })], X0, y - 0.05, 0.8, { h: 0.8 });
    text(s, [P(a.t, T.lead, { b: true, sa: 4 })].concat(a.l.map((l) => P(l, T.small, { ind: 9, sa: 2 }))), X0 + 0.9, y, lw - 0.95, {});
    y += h + gap / 1;
    if (i < 2) hline(s, X0, y - gap / 2, lw, C.LINE, 0.75);
  });
  // right 2x2
  const rx = X0 + lw + SP.s4, rw = X0 + W - rx;
  const bh = barHeading(s, '한 건물 안에서 이미 이뤄지고 있음', rx, Y0, rw);
  const tw = (rw - SP.s3) / 2;
  const capH = 0.24;
  const th = (YB - capH - Y0 - bh - SP.s2) / 2;
  CASES.forEach((c, i) => {
    const x = rx + (i % 2) * (tw + SP.s3);
    const y = Y0 + bh + Math.floor(i / 2) * (th + SP.s2);
    rect(s, x, y, tw, th, C.SOFT);
    rect(s, x, y, tw, 0.05, NAVY);
    const pw = 1.05, phh = Math.min(th - 0.25, pw / 0.74);
    caseImg(s, c, x + 0.12, y + 0.17, pw, phh, { small: true });
    const tx = x + 0.12 + pw + 0.14, twd = tw - pw - 0.38;
    text(s, [P(c.big, T.num, { b: true, color: NAVY, sa: 0 }), P(c.big2, T.cap, { color: C.MUTED, sa: 5 }), P(c.name, T.body, { b: true, sa: 1 }), P(c.meta, T.cap, { color: C.MUTED, sa: 5 })].concat(c.facts.map((f) => P(f, T.small, { ind: 9, sa: 2 }))), tx, y + 0.14, twd, { h: th - 0.2 });
  });
  caption(s, '국내에서 주차장과 공연장을 한 건물에 완공한 사례는 확인하지 못함', rx, YB - capH + 0.02, rw);
}

// ======================================================================================================= 시안 C · 도식형
{
  const s = mk('03', '사업 배경 Ⅰ', '사람을 받아 온 땅이 이제 차와 사람을 함께 받을 차례임', SRC1, NOTE1, '시안 C · 도식형');
  // thin time line across the top
  const ty = Y0 + 0.28, n = TL.length;
  const seg = W / n;
  hline(s, X0, ty, W, C.SLATE, 1.5);
  TL.forEach((r, i) => {
    const cx = X0 + seg * i + seg / 2;
    const last = i === n - 1;
    s.addShape(SH.OVAL, { x: cx - 0.09, y: ty - 0.09, w: 0.18, h: 0.18, fill: { color: last ? NAVY : C.SLATE }, line: { color: C.WHITE, width: 1.5 } });
    text(s, [P(r[0], T.fine, { b: true, color: NAVY, align: 'center', sa: 1 }), P(r[1], T.body, { b: true, align: 'center', sa: 2 }), P(r[2], T.cap, { color: C.MUTED, align: 'center' })], cx - seg / 2 + 0.1, ty + 0.18, seg - 0.2, {});
  });
  // three columns below
  const yc = Y0 + 1.72, hc = YB - yc;
  const c1 = 3.25, c2 = 4.75, gap = SP.s3, c3 = W - c1 - c2 - 2 * gap;
  const x1 = X0, x2 = X0 + c1 + gap, x3 = x2 + c2 + gap;
  // col1 현장
  plate(s, '현장', x1, yc, c1, 0.34, C.SLATE, { sz: T.small, ml: 0.14, mr: 0.3 });
  const ph = (hc - 0.34 - SP.s1 - 0.3 - SP.s1) / 2;
  imageBox(s, 'p_alley1.jpg', x1, yc + 0.34 + SP.s1, c1, ph);
  imageBox(s, 'p_alley2.jpg', x1, yc + 0.34 + SP.s1 + ph + SP.s1, c1, ph);
  caption(s, '전포동 이면도로 현장 (답사 2026.9)', x1, YB - 0.22, c1);
  // col2 지금
  plate(s, '지금', x2, yc, c2, 0.34, C.D2, { sz: T.small, ml: 0.14, mr: 0.3 });
  let y = yc + 0.34 + SP.s1;
  const b2 = bullets(s, NOW, x2 + 0.05, y, c2 - 0.1, { sz: T.small });
  y += b2.h + SP.s2;
  y += barHeading(s, '주차장 확보율 (%)', x2, y, c2);
  const chh = YB - 0.28 - y;
  barChart(s, x2, y, c2, chh);
  caption(s, '기준 130% · 개선지구는 노후주거지 등 67곳 평균', x2, YB - 0.24, c2);
  // col3 앞으로 + 사례
  plate(s, '앞으로', x3, yc, c3, 0.34, NAVY, { sz: T.small, ml: 0.14, mr: 0.3 });
  y = yc + 0.34 + SP.s1;
  const b3 = bullets(s, NEXT, x3 + 0.05, y, c3 - 0.1, { sz: T.small });
  y += b3.h + SP.s2;
  y += barHeading(s, '주차를 늘려 상권이 산 사례', x3, y, c3);
  const tt = table(s, x3, y, { cols: [c3 - 1.0, 1.0], head: ['서울 사당 · 공영 145면', '조성 후'], aligns: ['left', 'right'], size: T.small, rows: [['상권 유동인구', '+4.5%'], ['점포 수', '+5.0%'], ['상권 매출', '+10.2%']] });
  y += tt.h + SP.s1;
  text(s, [P('구청 발표이며 같은 기간 에스컬레이터 설치 등 다른 사업이 병행되어 주차 확충만의 효과는 아님', T.cap, { color: C.MUTED })], x3, y, c3, {});
  check('C03', y + 0.4, YB);
}
{
  const s = mk('04', '사업 배경 Ⅱ', '먹고 · 보고는 채워졌고 듣고만 비어 공연장이 필요함', SRC2, NOTE2, '시안 C · 도식형');
  // puzzle band
  const bh = 2.35, bw = W / 3;
  SENSE.forEach((c, i) => {
    const x = X0 + i * bw;
    const dark = i === 2;
    if (!dark) {
      s.addShape(SH.RECTANGLE, { x, y: Y0, w: bw - 0.02, h: bh, fill: { color: i === 0 ? C.NSOFT : 'C5D3EC' }, line: { type: 'none' } });
      s.addShape(SH.RIGHT_TRIANGLE, { x: x + bw - 0.34, y: Y0 + bh / 2 - 0.2, w: 0.32, h: 0.4, flipH: true, fill: { color: C.WHITE }, line: { type: 'none' } });
    } else {
      s.addShape(SH.RECTANGLE, { x: x + 0.02, y: Y0 + 0.02, w: bw - 0.04, h: bh - 0.04, fill: { type: 'none' }, line: { color: GOLD, width: 3, dashType: 'dash' } });
    }
    text(s, [P(c.v, 38, { b: true, color: dark ? C.INK : NAVY })], x + 0.3, Y0 + 0.12, 1.9, { h: 0.7, valign: 'middle' });
    pill(s, c.st, x + bw - 1.5, Y0 + 0.3, 1.1, { fill: dark ? GOLD : C.WHITE, color: dark ? C.INK : NAVY });
    text(s, [P(c.sub, T.small, { color: C.MUTED })], x + 0.3, Y0 + 0.84, bw - 0.6, { h: 0.25 });
    text(s, c.lines.map((t) => P(t, T.small, { ind: 9, sa: 3 })), x + 0.3, Y0 + 1.15, bw - 0.7, {});
  });
  // table of gaps
  const y2 = Y0 + bh + SP.s2;
  const yb = y2 + barHeading(s, '왜 듣고만 비어 있는가', X0, y2, W);
  const nH = noteHeight(W, '연결', LINK);
  const t = table(s, X0, yb, { cols: [1.8, 3.3, W - 5.1], head: ['구분', '무엇이 비었나', '근거'], size: T.body, label: true, fillTo: YB - nH - SP.s2, maxPad: 0.25,
    rows: WHY.map((p) => [p.label, p.title, p.lines.join(' / ')]) });
  noteBox(s, X0, YB - nH, W, '연결', LINK);
  check('C04', yb + t.h, YB - nH);
}
{
  const s = mk('05', '사업 배경 Ⅲ', '주차장이 공연장을 받치고 공연장이 주차장을 살림', SRC3, NOTE3, '시안 C · 도식형');
  const w1 = 3.75, w2 = 4.85, gap = SP.s3, w3 = W - w1 - w2 - 2 * gap;
  const x1 = X0, x2 = X0 + w1 + gap, x3 = x2 + w2 + gap;
  // col1: arguments
  let y = Y0;
  y += barHeading(s, '왜 한 건물인가', x1, y, w1);
  const hs = ARG.map((a) => L.measure([{ t: a.t, sz: T.body, b: true, sa: 3 }].concat(a.l.map((l) => ({ t: l, sz: T.small, ind: 9, sa: 2 }))), w1 - 0.6).h + 0.16);
  const grow = Math.max(0, (YB - y - hs.reduce((p, q) => p + q, 0) - 2 * SP.s1) / 3);
  ARG.forEach((a, i) => {
    const h = hs[i] + grow;
    rect(s, x1, y, w1, h, C.SOFT);
    s.addText(String(i + 1), { x: x1, y, w: 0.42, h, fontFace: FONT, fontSize: T.lead, bold: true, color: C.WHITE, fill: { color: NAVY }, align: 'center', valign: 'middle', margin: 0, isTextBox: true });
    text(s, [P(a.t, T.body, { b: true, sa: 3 })].concat(a.l.map((l) => P(l, T.small, { ind: 9, sa: 2 }))), x1 + 0.55, y, w1 - 0.65, { h, valign: 'middle' });
    y += h + SP.s1;
  });
  // col2: building section diagram
  y = Y0;
  y += barHeading(s, '한 건물의 하루 (개념 단면)', x2, y, w2);
  const dw = 2.55, dx = x2 + (w2 - dw) / 2;
  const layers = [
    ['옥상 광장', 0.5, 'CFE5BD', null],
    ['6F 가변홀', 0.85, '8FAADC', 'perf'],
    ['2~5F 주차(스킵플로어)', 1.5, 'CFCFCF', 'park'],
    ['1F 서점 · 카페 · 근생', 0.62, 'FBF3A4', null],
    ['B1~B2 공연장 200석', 0.9, '8FAADC', 'perf2'],
    ['B3~B4 주차 · 설비', 0.7, 'CFCFCF', null],
  ];
  const tot = layers.reduce((a, l) => a + l[1], 0);
  const k = (YB - y - 0.1) / tot;
  let ly = y;
  const pos = {};
  layers.forEach((l) => {
    const h = l[1] * k;
    s.addShape(SH.RECTANGLE, { x: dx, y: ly, w: dw, h, fill: { color: l[2] }, line: { color: C.WHITE, width: 1.5 } });
    text(s, [P(l[0], T.small, { b: l[3] === 'perf' || l[3] === 'perf2', align: 'center' })], dx, ly, dw, { h, valign: 'middle' });
    if (l[3]) pos[l[3]] = [ly, h];
    ly += h;
  });
  const groundY = y + (layers[0][1] + layers[1][1] + layers[2][1] + layers[3][1]) * k;
  hline(s, dx - 0.35, groundY, dw + 0.7, C.INK, 1.5);
  text(s, [P('지반 ±0', T.cap, { color: C.MUTED })], dx + dw + 0.05, groundY - 0.22, 0.7, { h: 0.2 });
  // day (left): cars rest in parking
  const [py, ph] = pos.park;
  s.addShape(SH.RIGHT_ARROW, { x: x2 - 0.02, y: py + ph / 2 - 0.2, w: dx - x2 + 0.1, h: 0.4, fill: { color: C.SLATE }, line: { type: 'none' } });
  text(s, [P('낮', T.small, { b: true, color: NAVY, sa: 1 }), P('차가 들어와 쉼(停)', T.cap)], x2, py + ph / 2 + 0.22, dx - x2, {});
  // night (right): audience goes down to the hall
  const [hy, hh] = pos.perf2;
  s.addShape(SH.LEFT_ARROW, { x: dx + dw - 0.1, y: hy + hh / 2 - 0.2, w: x2 + w2 - (dx + dw) + 0.1, h: 0.4, fill: { color: GOLD }, line: { type: 'none' } });
  text(s, [P('밤', T.small, { b: true, color: NAVY, sa: 1 }), P('관객이 모여 내려감(動)', T.cap)], dx + dw + 0.02, hy + hh / 2 + 0.22, x2 + w2 - (dx + dw), {});
  // noise note on the parking layers
  const [ty2, th2] = pos.perf;
  text(s, [P('주거 · 숙박 ·', T.cap, { color: C.MUTED }), P('학습 용도 없음', T.cap, { color: C.MUTED })], x2, py + 0.08, dx - x2 - 0.04, {});
  // col3: cases
  y = Y0;
  y += barHeading(s, '한 건물 안에서 이미 이뤄지고 있음', x3, y, w3);
  const capH = 0.4;
  const rh = (YB - y - capH - 3 * SP.s1) / 4;
  CASES.forEach((c, i) => {
    const yy = y + i * (rh + SP.s1);
    s.addShape(SH.RECTANGLE, { x: x3, y: yy, w: w3, h: rh, fill: { type: 'none' }, line: { color: C.LINE, width: 0.75 } });
    const pw = Math.min(0.75, (rh - 0.16) * 0.74), phh = pw / 0.74;
    caseImg(s, c, x3 + 0.08, yy + 0.08, pw, phh, { small: true });
    text(s, [P(c.name, T.small, { b: true, sa: 1 }), P(c.facts[0], T.cap)], x3 + pw + 0.2, yy + 0.04, w3 - pw - 0.28, { h: rh - 0.08, valign: 'middle' });
  });
  caption(s, '국내에서 주차장과 공연장을 한 건물에 완공한 사례는 확인하지 못함', x3, YB - 0.36, w3);
  check('C05', y + rh * 4, YB);
}

// ---------------------------------------------------------------- finish
const miss = L.flushMisses();
if (require.main === module || process.env.DECK_RUN) {
  const out = process.env.OUT || path.join(__dirname, 'shian.pptx');
  if (miss.length) {
    fs.writeFileSync(path.join(__dirname, 'misses.json'), JSON.stringify(miss));
    console.log('MISSES', miss.length);
    process.exit(3);
  }
  pres.writeFile({ fileName: out }).then(() => { console.log('WROTE', out); WARN.forEach((w) => console.log('WARN', w)); });
}
