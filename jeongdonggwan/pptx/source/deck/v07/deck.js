'use strict';
// 전포 정동관 · v5 (공설기 v1.2 유지, PowerPoint 실측 레이아웃 · 한글 어절 줄바꿈)
const fs = require('fs');
const path = require('path');
const L = require('./lay.js');
const { pres, C, FONT, SERIF, T, G, col, SP, rect, hline, vline, text, P, tag, barHeading, caption, imageW, imageH, imageBox, labeledPanel, panelHeight,
  noteBox, noteHeight, conclusion, conclusionHeight, table, drawVector, slide, blank, footer, sec } = L;
const SERIF_MID = 'Noto Serif KR SemiBold';

const WARN = [];
function check(name, bottom, limit) { if (bottom > limit + 0.005) WARN.push(`${name}: bottom ${bottom.toFixed(2)} > limit ${limit.toFixed(2)}`); }
const YB = G.YB, Y0 = G.Y0;
let NUM = 0;
const S = (title, sub, active, source, notes) => slide(String(++NUM).padStart(2, '0'), title, sub, active, source, notes);
const widthOf = (paras, w) => L.measure(paras, w);

const X0 = G.X0, W = G.W, SH = pres.shapes, GOLD = C.GOLD, NAVY = C.NAVY;
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



// =====================================================================  표지
{
  sec(0);
  const s = blank(0);
  s.background = { color: 'FFFFFF' };
  s.addImage({ path: L.imgPath('cover_hero.png'), x: G.SW - 7.9, y: 0, w: 7.9, h: 7.5 });
  text(s, [P('2026 · 공학설계기초', T.lead, { b: true })], 0.7, 0.75, 6, { h: 0.4 });
  text(s, [P('전포동', 50, { b: true })], 0.7, 1.55, 6.5, { h: 0.95, valign: 'middle', charSpacing: -1 });
  text(s, [P('복합주차장 정동관', 50, { b: true, color: C.NAVY })], 0.7, 2.6, 7.4, { h: 0.95, valign: 'middle', charSpacing: -1 });
  text(s, [P('건축계획', 50, { b: true })], 0.7, 3.65, 6.5, { h: 0.95, valign: 'middle', charSpacing: -1 });
  text(s, [P('낮에는 주차장, 밤에는 공연과 옥상 광장', T.h2, { color: C.MUTED })], 0.7, 5.0, 6.4, { h: 0.4 });
  text(s, [P('부산진구 전포동 207번지 일대 53필지 4,964.5㎡', T.body, { sa: 2 }), P('지하 4층 · 지상 6층 + 옥상 · 연면적 43,623.7㎡ · 주차 약 600대', T.body)], 0.7, 5.55, 6.6, {});
  text(s, [P('202325137 정성윤', T.lead, { b: true })], 0.7, 6.75, 4, { h: 0.3 });
  text(s, [P('停動館', 46, { face: SERIF, color: C.WHITE, align: 'right' })], G.SW - 4.2, 6.2, 3.8, { h: 0.9, valign: 'middle' });
  rect(s, G.SW - 6.15, 7.13, 6.15, 0.37, '101216');
  text(s, [P('투시도는 개념 볼륨 모델로 만든 이미지이며 실제 설계안이 아님', T.fine, { color: C.WHITE, align: 'right' })], G.SW - 6.0, 7.13, 5.8, { h: 0.37, valign: 'middle' });
}

// =====================================================================  목차
{
  const s = blank(0);
  rect(s, G.SW - 4.7, 0, 4.7, 7.5, C.NSOFT);
  s.addImage({ path: L.imgPath('contents_art.jpg'), x: G.SW - 4.5, y: 0, w: 4.5, h: 7.5 });
  text(s, [P('停動館', 50, { face: SERIF, color: C.WHITE, align: 'right' })], G.SW - 4.5, 6.3, 4.1, { h: 0.9, valign: 'middle' });
  text(s, [P('CONTENTS', 30, { b: true, color: C.NAVY })], 0.9, 0.8, 5, { h: 0.6, charSpacing: -0.5 });
  text(s, [P('전포 정동관 · 낮에는 주차장, 밤에는 공연과 옥상 광장', T.body, { color: C.MUTED })], 0.9, 1.45, 7, { h: 0.3 });
  const groups = [
    ['INTRODUCTION', [['사업 배경 Ⅰ · Ⅱ · Ⅲ', '03–05']]],
    ['MAIN SUBJECT', [['대지 분석 · 부지 선정', '06–07'], ['향 · 일조 · 소음 · 조망', '08–10'], ['콘셉트 · 사례 분석 Ⅰ~Ⅲ', '11–15'], ['볼륨 도출 · 최종안 · 투시도 Ⅰ · Ⅱ', '16–19']]],
    ['CONCLUSION', [['용도 선정 · 층별 계획 · 단면도', '20–21'], ['실별 면적 · 동선 및 진입', '22–23'], ['법규 검토 · 구조 · 방재 제안', '24'], ['사례 차용 외피 대안 · 형태 대안', '25–26'], ['확인할 것', '27']]],
  ];
  const x0 = 0.9, xi = 3.55, xr = 8.2, pitch = 0.37;
  let y = 2.3;
  groups.forEach(([g, items]) => {
    hline(s, x0, y - 0.1, xr - x0, C.LINE, 0.75);
    text(s, [P(g, T.lead, { b: true, color: C.NAVY })], x0, y, 2.5, { h: 0.3, valign: 'middle' });
    items.forEach(([t, pg], i) => {
      text(s, [P(t, T.body)], xi, y + i * pitch, 3.9, { h: 0.3, valign: 'middle' });
      text(s, [P(pg, T.small, { color: C.MUTED, align: 'right' })], xr - 0.9, y + i * pitch, 0.9, { h: 0.3, valign: 'middle' });
    });
    y += items.length * pitch + 0.3;
  });
  hline(s, x0, y - 0.1, xr - x0, C.LINE, 0.75);
  text(s, [P('발표자', T.small, { color: C.MUTED, sa: 2 }), P('정성윤', T.h2, { b: true })], x0, y - 0.95, 3, {});
}

// =====================================================================  01 사업 배경 Ⅰ (시안 C · 도식형)
{
  const s = S('사업 배경 Ⅰ', '사람을 받아 온 땅이 이제 차와 사람을 함께 받을 차례임', 0, SRC1, NOTE1);
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
// =====================================================================  02 사업 배경 Ⅱ (시안 C · 도식형)
{
  const s = S('사업 배경 Ⅱ', '먹고 · 보고는 채워졌고 듣고만 비어 공연장이 필요함', 0, SRC2, NOTE2);
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
// =====================================================================  03 사업 배경 Ⅲ (시안 B · 숫자형)
{
  const s = S('사업 배경 Ⅲ', '주차장이 공연장을 받치고 공연장이 주차장을 살림', 0, SRC3, NOTE3);
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
// =====================================================================  02 대지 분석
{
  const s = S('대지 분석', '53필지를 합쳐 한 블록으로 쓸 수 있는 대지임', 1,
    '토지이음 필지별 토지이용계획 조회(2026.10.11) · 「부산광역시 건축 조례」 별표4 / 필지 위치는 확인도면 정합으로 판별함, 치수 개략');
  const mapH = YB - Y0 - 0.27;
  const mw = imageH(s, 'site_eum.jpg', G.X0, Y0, mapH, { frame: true }).w;
  caption(s, '토지이용계획 확인도면 · 필지군 표시(개략)', G.X0, Y0 + mapH + 0.03, mw);
  const bx = G.X0 + mw + SP.s4, bw = G.X0 + G.W - bx;
  let y = Y0;
  y += barHeading(s, '대지 개요', bx, y, bw);
  let t = table(s, bx, y, { cols: [1.3, 0.7, 1.05, bw - 3.05], head: ['구역', '필지', '면적㎡', '형상 · 접도'], aligns: ['left', 'right', 'right', 'left'], boldRows: [3], rows: [
    ['서측 쐐기', '19', '1,531.9', '전포대로(서)에 면한 쐐기형, 남단이 뾰족함'],
    ['소로 부지', '5', '733.1', '두 구역 사이 폭 약 6m, 남단 전포대로 · 북단 서전로'],
    ['동측 블록', '29', '2,699.5', '서전로 · 224번길 · 동측 이면도로에 면한 삼각형'],
    ['합계', '53', '4,964.5', '지목 대 48필지, 도로 5필지'],
  ] });
  y += t.h + SP.s3;
  y += barHeading(s, '배치 조건', bx, y, bw);
  const pw = (bw - SP.s3) / 2;
  const itemsL = [
    { title: '일반상업지역 · 방화지구', lines: ['가로구역별 최고높이 기준 130m, 최고 180m', '일조 제한은 주거지역에만 적용됨'] },
    { title: '건폐율 상한 90%', lines: ['주차전용건축물은 용적률 1,500% 이하', '계획은 건폐율 87.1%'] },
  ];
  const itemsR = [
    { title: '건축선 3m 이격', lines: ['공연장 1,000㎡ 이상으로 북 · 남 면을 띄움', '전포대로 쪽은 면제'] },
    { title: '두 뾰족한 끝을 비움', lines: ['동측 북단 약 352㎡, 서측 남단 약 158㎡', '건폐율을 맞추고 끝 코어 자리로 씀'] },
  ];
  const noteTxt = '207-15 · 79는 제3종일반주거지역도 표기됨(상업지역으로 계산함). 207-84 · 85는 지목 대이나 도로로 쓰임';
  const nH = noteHeight(bw, '확인할 것', noteTxt);
  const ny = YB - nH;
  const ph = Math.max(ny - SP.s3 - y, panelHeight(pw, { items: itemsL }), panelHeight(pw, { items: itemsR }));
  labeledPanel(s, bx, y, pw, { label: '용도지역 · 높이', items: itemsL, h: ph });
  labeledPanel(s, bx + pw + SP.s3, y, pw, { label: '건축선 · 건폐율', items: itemsR, h: ph });
  check('s02', y + ph, ny - SP.s2);
  noteBox(s, bx, ny, bw, '확인할 것', noteTxt);
}

// =====================================================================  04 부지 선정
{
  const s = S('부지 선정', '수요 · 공백 · 형상이 모두 이 땅에 겹침', 1,
    '카카오맵 도보 환산 · 토지이음 필지별 토지이용계획(2026.10.11) · 전국주차장정보표준데이터(2026.04) · 시설공단 · 부산진구(2026.4 협약) · 「주차장법 시행규칙」 제5조 / 지도 © OpenStreetMap contributors',
    '도보 거리는 카카오맵 환산값. 소로 폭 약 6m · 5필지 733.1㎡는 토지이음 확인도면 기준 개략. 400대 초과 노외주차장은 입구와 출구를 분리해야 함(시행규칙 제5조). 대안 부지 비교는 하지 않았으며, 위 근거는 이 대지가 가진 이점의 나열임.');
  const mapH = YB - Y0 - 0.27;
  const mw = imageH(s, 'transit_map.jpg', G.X0, Y0, mapH, { frame: true }).w;
  caption(s, '주변 현황도 · 위치 개략', G.X0, Y0 + mapH + 0.03, mw);
  const bx = G.X0 + mw + SP.s4, bw = G.X0 + G.W - bx;
  const cLine = '수요(두 역 · 세 상권), 공백(공영주차장), 형상(소로 · 세 도로)이 모두 이 땅에 겹침';
  const cH = -SP.s2;
  const limit = YB - cH - SP.s2;
  let y = Y0;
  y += barHeading(s, '이 땅이어야 하는 이유', bx, y, bw);
  const rs = [
    ['두 역 사이에 놓인 땅', '서면역 737m · 전포역 529m, 어느 역에서도 걸어서 닿음'],
    ['세 상권이 만나는 결절점', '카페거리 · 공구길 · 사잇길이 2026.4 통합 청년 상권 협약으로 묶임'],
    ['공영주차장이 비어 있는 자리', '반경 500m 공영 27면, 1km 이내 약 415면'],
    ['이미 있는 6m 소로를 씀', '새 길을 뚫지 않고 소로 5필지(733.1㎡)를 차량 전용 차로로 돌려 씀'],
    ['세 도로에 면해 입구와 출구를 가름', '전포대로(서) · 서전로(북) · 224번길(남), 400대 초과 시 입출구 분리 요건'],
  ];
  const nw = 0.5;
  const hs = rs.map((r) => L.measure([{ t: r[0], sz: T.lead, b: true, sa: 2 }, { t: r[1], sz: T.small }], bw - nw - 0.1).h + 0.2);
  const grow = Math.max(0, (limit - y - hs.reduce((p, q) => p + q, 0) - 4 * SP.s1) / 5);
  rs.forEach((r, i) => {
    const h = hs[i] + grow;
    hline(s, bx, y + h + SP.s1 / 2, bw, C.LINE, 0.75);
    text(s, [P(String(i + 1), 22, { b: true, color: C.NAVY, align: 'center' })], bx, y, nw, { h, valign: 'middle' });
    text(s, [P(r[0], T.lead, { b: true, sa: 2 }), P(r[1], T.small, { color: C.MUTED })], bx + nw, y, bw - nw - 0.1, { h, valign: 'middle' });
    y += h + SP.s1;
  });
  check('s04', y - SP.s1, limit);
}

// =====================================================================  04 향 · 일조
{
  const s = S('향 · 일조', '서 · 동 면은 슬랫으로 거르고 광장은 남쪽에 둠', 1,
    'NOAA 태양 위치 근사식(북위 35.157°) · OpenStreetMap contributors(주변 건물 일부 누락) · 본 시안 매스 계산 / 직사 시간은 고도 5° 이상, 가림 없음 가정',
    '그림자는 본 시안 매스(5F 지붕 21.1m, 6F 홀 29.8m)와 NOAA 근사식으로 계산함. 주변 건물은 OSM 등록분만 반영해 저층이 빠져 있음. 일조 판단 시간대는 동지 9~15시로 가정함. 정북 일조 제한은 주거지역에만 적용되어 상업지역 대지에는 해당하지 않음.');
  const A = col(0, 8), B = col(8, 4);
  const cLine = '서 · 동 면은 목재 슬랫으로 일사를 거르고, 광장과 근생은 남쪽에 둠';
  const cH = -SP.s2;
  const limit = YB - cH - SP.s2;
  let y = Y0;
  const h1 = A.w / L.ratio('shadow3.png');
  imageW(s, 'shadow3.png', A.x, y, A.w);
  y += h1;
  y += caption(s, '정동관 그림자 · 동지 09 · 12 · 15시, 지붕 설비 포함 높이 29.8m 기준 (붉은 선 = 대지, 점선 = 제3종일반주거 경계 약 45m)', A.x, y + 0.03, A.w) + 0.03;
  y += SP.s2;
  const hh = limit - y;
  const capH2 = 0.42;
  const hw = imageH(s, 'shadow_hours.png', A.x, y, hh - capH2).w;
  caption(s, '동지 09~15시 그림자 누적 시간', A.x, y + hh - capH2 + 0.03, hw, { align: 'left' });
  const tx = A.x + hw + SP.s3, tw = A.x + A.w - tx;
  const t = table(s, tx, y, { cols: [1.45, 1.95, tw - 3.4], head: ['면', '직사 동지 / 하지', '관찰'], size: T.small, aligns: ['left', 'center', 'left'], rows: [
    ['서측 · 전포대로', '4.3h(오후) / 6.7h', '서향 일사와 도로 소음이 함께 닿음'],
    ['동측 · 이면도로', '4.3h(오전) / 6.8h', '동지 15시경 주거 경계에 이름'],
    ['남측 · 224번길', '8.6h / 6.9h', '동지 고도 31.4°, 깊이 들어옴'],
    ['북측 · 서전로', '0h / 새벽 · 저녁', '직사 없음, 그림자는 도로 쪽'],
  ], fillTo: limit, maxPad: 0.12 });
  check('s04 table', y + t.h, limit);
  // right column: sun path + observation (runs to the bottom line)
  let yy = Y0;
  const spH = 3.25;
  const spW = spH * L.ratio('sunpath.png');
  imageH(s, 'sunpath.png', B.x + (B.w - spW) / 2, yy, spH);
  yy += spH;
  yy += caption(s, '태양 경로 · 대지 위치 (원 안쪽이 높은 고도)', B.x, yy + 0.03, B.w) + 0.03;
  yy += SP.s2;
  const items = [{ title: '옥상 광장', lines: ['동지 9~15시 그림자 영향 없음', '홀(29.1m)이 광장의 북쪽에 있음'] }, { title: '동측 주거 경계', lines: ['동지 9~15시 그림자 0.5h 미만'] }];
  labeledPanel(s, B.x, yy, B.w, { label: '관찰', items, h: YB - yy });
  check('s04 panel', yy + panelHeight(B.w, { items }), YB);
}

// =====================================================================  05 소음
{
  const s = S('소음', '소음 큰 실은 지하 · 최상층 안쪽에 두고 서 · 북 면은 닫음', 1,
    '「환경정책기본법 시행령」 별표 · OpenStreetMap contributors · 현장 답사(2026.9) / dB은 가정 교통량 기반 개략 추정 / 사진: Petr Meissner, CC BY 2.0',
    '소음 분포는 실측이 아니라 개략 추정임. OSM 도로를 5m 간격 점음원으로 바꾸고 10m 기준 Leq를 광로 · 대로 70, 3차 63, 주거 58 dB(A)로 가정했으며 건물 차폐와 지면 효과는 넣지 않음. 부산시 소음 측정망에 전포동 지점이 없어 현장 낮 · 밤 실측으로 교체해야 함.');
  const A = col(0, 4), B = col(4, 4), Cc = col(8, 4);
  const cLine = '소음이 큰 실은 지하와 최상층 안쪽에 두고, 서 · 북 도로변 면은 닫음';
  const cH = -SP.s2;
  const limit = YB - cH - SP.s2;
  let y = Y0;
  const mapH = 3.3;
  const mw = ((mapH * L.ratio('noise_map.png')));
  imageH(s, 'noise_map.png', A.x + (A.w - mw) / 2, y, mapH);
  y += mapH;
  y += caption(s, '주간 Leq 추정 분포 · ● 면별 평가점(북 · 서 · 남 · 동 · 주거 경계)', A.x, y + 0.03, A.w, { align: 'center' }) + 0.03;
  y += SP.s1;
  const pw = (A.w - 2 * SP.s1) / 3, phh = limit - y;
  ['n_p1.jpg', 'n_p2.jpg', 'n_p3.jpg'].forEach((n, i) => imageBox(s, n, A.x + i * (pw + SP.s1), y, pw, phh));
  let ym = Y0;
  ym += barHeading(s, '소음 환경기준 (dB)', B.x, ym, B.w);
  let t = table(s, B.x, ym, { cols: [1.7, 0.45, 0.45, B.w - 2.6], head: ['구분', '낮', '밤', '해당'], size: T.small, aligns: ['left', 'center', 'center', 'left'], rows: [
    ['일반지역 다(상업)', '65', '55', '대지'], ['도로변 다(상업)', '70', '60', '서·북 도로변'], ['일반지역 나(주거)', '55', '45', '동측 주거'], ['도로변 가 · 나(주거)', '65', '55', '동측 도로변'],
  ] });
  ym += t.h + SP.s3;
  ym += barHeading(s, '면별 주간 추정치 (dB(A), 가정)', B.x, ym, B.w);
  const capN = 0.3;
  caption(s, '가정 교통량 기반 개략 추정 · 현장 실측으로 교체 필요', B.x, limit - capN + 0.06, B.w);
  s.addChart(pres.charts.BAR, [{ name: '주간 Leq 추정', labels: ['북 · 서전로', '서 · 전포대로', '남 · 224번길', '동 · 이면도로', '동측 주거 경계'], values: [76, 72, 70, 69, 67] }], {
    x: B.x, y: ym, w: B.w, h: limit - ym - capN, barDir: 'bar', chartColors: [C.NAVY, C.NAVY, C.D2, C.D2, C.SLATE], showValue: true, dataLabelFontSize: T.small, dataLabelFontFace: FONT,
    dataLabelColor: 'FFFFFF', dataLabelPosition: 'inEnd', catAxisLabelFontSize: T.small, catAxisLabelFontFace: FONT, catAxisLabelColor: C.INK, valAxisHidden: true, valAxisMinVal: 0,
    valAxisMaxVal: 90, valGridLine: { style: 'none' }, catGridLine: { style: 'none' }, showLegend: false, barGapWidthPct: 35, catAxisOrientation: 'maxMin' });
  let yc = Y0;
  yc += barHeading(s, '공간별 대응', Cc.x, yc, Cc.w);
  const g1 = { label: '공연 · 홀', items: [
    { title: '지하 공연장 B1~B2', lines: ['박스인박스와 방진 바닥 제안', '선큰 마당 쪽 로비가 완충'] },
    { title: '6F 가변홀', lines: ['이중 차음 지붕', '서 · 북 면은 닫고 남쪽 광장으로 개구'] }] };
  const g2 = { label: '주차 · 업무', items: [
    { title: '소로 · 램프', lines: ['2층 바닥이 덮은 높이 7m 통로'] },
    { title: '동측 하역 · 이륜차', lines: ['운영시간 제한 검토'] },
    { title: '5F 상인회', lines: ['동측 이면 쪽, 서측 이중창 검토'] }] };
  const h1 = panelHeight(Cc.w, g1), h2 = panelHeight(Cc.w, g2);
  const spare = Math.max(0, limit - yc - h1 - h2 - SP.s2);
  const ex1 = spare * h1 / (h1 + h2), ex2 = spare - ex1;
  labeledPanel(s, Cc.x, yc, Cc.w, Object.assign({ h: h1 + ex1 }, g1));
  labeledPanel(s, Cc.x, yc + h1 + ex1 + SP.s2, Cc.w, Object.assign({ h: h2 + ex2 }, g2));
  check('s05 right', yc + h1 + h2 + SP.s2, limit);
}

// =====================================================================  06 조망
{
  const s = S('조망', '조망은 옥상 광장에서 얻고 남 · 동으로만 엶', 1,
    'OSM 좌표 · 「위키백과」 황령산 427m · BIFC 289m · 본 시안 매스 / 앙각은 지면 8m 가정, 능선 형상은 반영 안 됨 / 사진: Christian Bolz, CC BY-SA 4.0',
    '황령산 정상(427m)은 OSM 좌표 기준 대지에서 동쪽 약 1.47km, BIFC(289m)는 남쪽 약 1.15km. 눈높이는 1층 1.6m, 옥상 광장 22.7m. 주변 건물은 OSM 등록분(반경 약 420m)만 반영해 저층이 빠져 있어 조망이 실제보다 열려 보일 수 있음.');
  const cLine = '조망은 옥상 광장에서 얻고, 남 · 동으로만 열어 서측 일사 · 소음 면은 닫음';
  const cH = -SP.s2;
  const limit = YB - cH - SP.s2;
  let y = Y0;
  const hp = G.W / L.ratio('view_profile.png');
  imageW(s, 'view_profile.png', G.X0, y, G.W);
  y += hp;
  y += caption(s, '스카이라인 앙각 분석 · 옥상 광장과 1층 가로, 주변 건물과 정동관 매스 포함', G.X0, y + 0.02, G.W) + 0.02;
  y += SP.s2;
  const hh = limit - y;
  const A = col(0, 3), B = col(3, 3), Cc = col(6, 6);
  imageBox(s, 'view_jeonpo.jpg', A.x, y, A.w, hh - 0.26);
  caption(s, 'BIFC · 서면 일대 조망', A.x, y + hh - 0.24, A.w, { align: 'left' });
  imageBox(s, 'view_roof.jpg', B.x, y, B.w, hh - 0.26);
  caption(s, '옥상 광장 시뮬레이션(개념 모델)', B.x, y + hh - 0.24, B.w, { align: 'left' });
  const noteTxt = '1층 가로는 자체 매스가 동쪽을 가려 황령산이 보이지 않음. 옥상 광장은 열린 각도 약 128°, 동남동 29~30층 아파트 위로 능선 상단이 걸침';
  const nH = noteHeight(Cc.w, '관찰', noteTxt);
  const t = table(s, Cc.x, y, { cols: [1.8, 1.75, 0.85, Cc.w - 4.4], head: ['대상', '방위 · 거리', '앙각', '옥상'], size: T.small, minRow: 0.3, fillTo: limit - nH - SP.s2, maxPad: 0.1, rows: [
    ['황령산 정상 427m', '동 87° · 1.47km', '15.1°', { t: '상단만 보임', color: C.SIGNAL, b: true }],
    ['BIFC 289m', '남 184° · 1.15km', '12.6°', { t: '보임', color: C.NAVY, b: true }],
    ['서면 도심', '서 · 약 0.6km', '고층군', { t: '보임', color: C.NAVY, b: true }],
  ] });
  const ny = Math.max(y + t.h + SP.s2, limit - nH);
  noteBox(s, Cc.x, ny, Cc.w, '관찰', noteTxt);
  check('s06 note', ny + nH, limit);
}

// =====================================================================  콘셉트 · 낮 / 밤
function conceptSlide(night) {
  const s = blank(1);
  const bg = night ? '0A1122' : C.PANEL, ink = night ? 'F2F4F8' : C.INK, sub = night ? 'A7B0C2' : C.MUTED, dim = night ? '3D4864' : 'C9CED8';
  const key = night ? C.GOLD : C.NAVY;
  const textW = 4.6, tx = 3.9, imgW = 4.7;
  rect(s, 0, 0, G.SW, 7.5, bg);
  s.addImage({ path: L.imgPath(night ? 'concept_night.jpg' : 'concept_day.jpg'), x: G.SW - imgW, y: 0, w: imgW, h: 7.5 });
  [['停', '정', !night], ['動', '동', night], ['館', '관', false]].forEach(([c, k, on], i) => {
    const yy = 0.4 + i * 2.2;
    text(s, [P(c, 110, { face: SERIF, color: on ? key : dim, align: 'center' })], 0.75, yy, 2.0, { h: 2.15, valign: 'middle' });
    text(s, [P(k, 28, { b: true, color: on ? key : sub, align: 'center' })], 2.88, yy, 0.8, { h: 2.15, valign: 'middle' });
  });
  s.addText(night ? '밤 · 動' : '낮 · 停', { x: tx, y: 0.75, w: 1.45, h: 0.4, fontFace: FONT, fontSize: T.lead, bold: true, color: night ? '0A1122' : 'FFFFFF', fill: { color: night ? C.GOLD : C.NAVY }, align: 'center', valign: 'middle', margin: 0, isTextBox: true });
  const hi = { face: SERIF, b: false, color: key };
  text(s, [{ runs: [{ t: '‘정동관’은 차가 멈추는 주차층(停)과 사람이 움직이는 계단 · 홀 · 광장(動)을 한 건물 안에 두어, ' },
    Object.assign({ t: '낮에는 상권의 차를 받고' }, night ? {} : hi), { t: ' ' }, Object.assign({ t: '밤에는 공연과 옥상 광장이 켜지는' }, night ? hi : {}), { t: ' 건물을 뜻함' }],
    sz: T.h2, color: ink, face: SERIF_MID, align: 'center' }], tx, 1.5, textW, { ls: 1.4, h: 2.7, valign: 'middle' });
  hline(s, tx + textW / 2 - 0.4, 4.4, 0.8, night ? '3D4864' : C.LINE, 1);
  text(s, [P('停과 動이 교대하는 하루', T.h2, { b: true, color: ink, align: 'center' })], tx, 4.6, textW, { h: 0.4 });
  text(s, [P('차가 멈추는 주차층은 목재 슬랫 스크린으로 차분히 감싸고, 사람이 움직이는 순환 계단 · 6F 가변홀 · 옥상 광장은 검은 계단과 켜진 홀로 드러냄', T.body, { color: sub, align: 'center' })], tx, 5.1, textW, { ls: 1.2 });
  footer(s, '', L.pageNo(), { dark: night, xL: 1.68, xR: G.SW - imgW - 0.3 });
  s.addNotes(night ? '밤 장면: 같은 내용, 야간 렌더(Blender Cycles)와 공설기 Night 토큰(#0a1122 · 금색 select)으로 낮과 대비함.' : '낮 장면: 같은 내용, 주간 렌더(Blender Cycles)와 공설기 Deck 토큰으로 구성함.');
}
conceptSlide(false);
conceptSlide(true);

// =====================================================================  07-09 사례 분석
const CIRC = '①②③④⑤⑥⑦⑧⑨⑩';
function parseFact(f) {
  const m = f.match(/^([①②③④⑤⑥⑦⑧⑨⑩]+)\s*/);
  let mk = '', rest = f;
  if (m) { mk = [...m[1]].map((c) => String(CIRC.indexOf(c) + 1)).join('·'); rest = f.slice(m[0].length); }
  let kw = '', body = rest;
  const ci = rest.indexOf(':');
  if (ci > 0 && ci <= 8) { kw = rest.slice(0, ci).trim(); body = rest.slice(ci + 1).trim(); }
  return { mk, kw, body };
}
function caseSlide(title, sub, source, cases) {
  const s = S(title, sub, 1, source);
  const w = col(0, 6).w, xs = [col(0, 6).x, col(6, 6).x];
  const bandH = 0.72, bandY = YB - bandH;
  const imgY = Y0 + 0.62;
  const ph = (w - SP.s1) / (0.74 + 1.66);          // photo 0.74 : drawing 1.66, both uncropped
  const pw = ph * 0.74;
  const BW = 0.5;
  cases.forEach((c, i) => {
    const x = xs[i];
    text(s, [P(c.name, T.h2, { b: true })], x, Y0, w, { h: 0.3 });
    text(s, [P(c.meta, T.fine, { color: C.MUTED })], x, Y0 + 0.31, w, { h: 0.2 });
    imageH(s, c.photo, x, imgY, ph);
    imageH(s, c.draw, x + pw + SP.s1, imgY, ph, { frame: true });
    // fact cards: number badge matches the marks on the drawing
    const facts = c.facts.map(parseFact);
    const hs = facts.map((f) => L.measure([{ t: (f.kw ? f.kw + '  ' : '') + f.body, sz: T.small }], w - BW - 0.22).h + 0.1);
    const fy0 = imgY + ph + SP.s2;
    const gap = 0.06;
    const room = bandY - SP.s2 - fy0;
    const grow = Math.max(0, Math.min(0.12, (room - hs.reduce((p, q) => p + q, 0) - gap * (facts.length - 1)) / facts.length));
    let fy = fy0;
    facts.forEach((f, k) => {
      const h = hs[k] + grow;
      hline(s, x, fy + h + gap / 2, w, C.LINE, 0.5);
      if (f.mk) {
        s.addText(f.mk, { x, y: fy, w: BW, h, fontFace: FONT, fontSize: f.mk.length > 3 ? T.small : T.lead, bold: true, color: C.WHITE, fill: { color: C.NAVY }, align: 'center', valign: 'middle', margin: 0, isTextBox: true });
      } else {
        rect(s, x, fy, BW, h, C.SLATE);
        text(s, [P('+', T.lead, { b: true, color: C.WHITE, align: 'center' })], x, fy, BW, { h, valign: 'middle' });
      }
      text(s, [{ runs: (f.kw ? [{ t: f.kw + '  ', b: true, color: C.NAVY }] : []).concat([{ t: f.body }]), sz: T.small }], x + BW + 0.12, fy, w - BW - 0.22, { h, valign: 'middle' });
      fy += h + gap;
    });
    check('case ' + title + ' ' + c.name, fy - gap, bandY - SP.s1);
    rect(s, x, bandY, w, bandH, C.PDARK);
    rect(s, x, bandY, 0.06, bandH, C.GOLD);
    text(s, [P('정동관 적용', T.body, { b: true, color: C.GOLD })], x + 0.22, bandY, 1.3, { h: bandH, valign: 'middle' });
    text(s, [P(c.apply, T.body, { color: C.WHITE })], x + 1.55, bandY, w - 1.55 - 0.18, { h: bandH, valign: 'middle' });
  });
}
caseSlide('사례 분석 Ⅰ', '좁은 대지의 주차빌딩은 램프를 줄이고 1층을 열었음',
  'ArchDaily · JOHO Architecture(헤르마 주차빌딩, 사진 Namgoong Sun · Jeonghoon Lee) · arch2o · 서울경제 2016.02.26 · 자체 조사(2026.9) / 평택 JS타워는 도면 미공개로 사진 판독, 사진 출처 미확인(저장소 자료)', [
    { name: '헤르마 주차빌딩', meta: 'JOHO Architecture · 용인 죽전 카페거리 초입 · 2010', photo: 'c_herma.jpg', draw: 'd_herma.jpg',
      facts: ['①② 평면: 폭 약 14m의 사선 대지에서 램프 폭을 6m에서 3.3m로 줄이고 삼각 보이드를 계단이 감아 오름, ③ 코어는 평면 중앙에 둠',
        '④ 외피: 반투명 폴리카보네이트 패널과 타공 밴드, 층마다 개구 패턴이 달라 자연환기와 확산광을 얻음',
        '⑤ 1층 상가가 가로와 주차층 사이 완충이 되고 밤에는 차량 불빛이 외피를 통해 가로에 비침'],
      apply: '1층을 가로에 열고, 뾰족한 끝을 순환 계단 코어로 둠' },
    { name: '평택 JS타워', meta: '평택 · 대지 2,505㎡', photo: 'c_js.jpg', draw: 'd_js.jpg',
      facts: ['① 상부: 수평 곡면 금속 루버 밴드가 층마다 이어져 주차층을 감싸고 일사와 외부 시선을 거름(사진 판독)',
        '② 1층: 흑벽돌 아치 상가가 가로를 향해 열리고 ③ 진출입은 중앙 한 곳으로 모음, ④ 벽돌 타공 띠가 상가와 주차층을 구분함',
        '단면: 스킵플로어로 램프 면적을 줄여 주차 효율을 높임(자체 작성 단면)'],
      apply: '2층 이상 스킵플로어, 줄인 램프 면적을 공연장에 배분함' }]);
caseSlide('사례 분석 Ⅱ', '외피는 슬랫으로 감싸고 옥상은 시민에게 열었음',
  'ArchDaily · dJGA + MODULO(Saint-Luc, 사진 Lieven Van Landschoot) · JAJA Architects(Park ’n’ Play, 사진 Rasmus Hjortshøj / COAST) · 자체 조사(2026.9)', [
    { name: 'Saint-Luc 주차건물', meta: 'de Jong Gortemaker Algra + MODULO · 브뤼셀 · 2016', photo: 'c_saintluc.jpg', draw: 'd_saintluc.jpg',
      facts: ['①②③ 단면: 옥상 녹지 아래 지상 2층 · 지하 3층 데크(985대), 경사지에 묻혀 지붕이 녹지로 이어짐',
        '④ 협곡: 건물 둘레의 구불구불한 틈이 최하층까지 빛과 공기를 들임',
        '⑤ 외피: 물결치는 목재 슬랫 입면이 주차 데크를 감쌈'],
      apply: '주차층 외피를 목재 슬랫 스크린으로 구성, 두 끝을 비워 지하 공연장까지 빛을 내림' },
    { name: 'Park ’n’ Play', meta: 'JAJA Architects · 코펜하겐 노르드하운 · 2016', photo: 'c_pnp.jpg', draw: 'd_pnp.jpg',
      facts: ['① 옥상: 지상 약 24m에서 시민에게 열린 놀이 · 운동 공간, 코펜하겐 항구 방향이 열림',
        '② 외부 공공계단 두 줄이 지상에서 옥상까지 비스듬히 이어짐(평면 코너 계단과 같은 동선)',
        '③ 플랜터 그리드와 타공 벽체가 주차층을 자연환기함, ④ 주차층 평면의 원형 램프가 층을 이음'],
      apply: '옥상 광장(약 1,380㎡)과 개방 순환 계단' }]);
caseSlide('사례 분석 Ⅲ', '공연과 행사는 지하 홀과 높은 층고에 담았음',
  'ArchDaily · peter haimerl.architektur(Blaibach, 도면 · 사진 NAARO) · Herzog & de Meuron(1111 Lincoln Road, 사진 Phillip Pessar CC BY 2.0 · 삽입 사진 ArchDaily) · 자체 조사(2026.9)', [
    { name: 'Concert Hall Blaibach', meta: 'peter haimerl.architektur · 독일 바이에른 · 2014', photo: 'c_blaibach.jpg', draw: 'd_blaibach.jpg',
      facts: ['①② 평면: 200석 객석과 무대를 지하에 묻어 길게 배치, ③ 로비 · 바 · 화장실이 객석 위쪽에서 완충층이 됨',
        '④ 단면: 기울어진 화강암 블록만 지상에 노출, ⑤ 지하 로비와 ⑥ 계단이 블록 밑면에서 내려감',
        '콘크리트 셸이 음향과 차음을 함께 풀고, 지상 블록은 마을 광장의 랜드마크가 됨'],
      apply: '공연장을 B1~B2에 두고 선큰 마당에서 내려가는 진입' },
    { name: '1111 Lincoln Road', meta: 'Herzog & de Meuron · 마이애미 비치 · 2010', photo: 'c_lincoln.jpg', draw: 'd_lincoln.jpg',
      facts: ['① 층고: 슬래브 · 기둥 · 램프만으로 이룬 개방 구조, 층고는 약 2.1m(주차)에서 최대 약 10.4m까지 변함',
        '② 중앙 계단과 보이드가 층 사이를 열고 ④ 주차 데크는 외기에 열림(공식 도면 S1 · 2층 평면)',
        '③ 1층 소매 14개 유닛이 가로를 향해 열리고 상부 층은 행사 · 문화 · 상업에 탄력적으로 쓰임'],
      apply: '6F 가변홀(층고 8m)과 5F 전환 층' }]);

// =====================================================================  10 볼륨 도출
{
  const s = S('볼륨 도출', '두 끝을 비워 이격을 맞추고 그 자리를 얼굴로 씀', 1, '본 시안(개념 볼륨 스터디, 축측 투영: Blender) · 면적은 개략이며 형태는 실제 설계안이 아님');
  const cLine = '필지를 채우되 법정 이격과 건폐율은 두 끝을 비워 맞추고, 비운 자리가 건물의 얼굴이 됨';
  const cH = -SP.s2;
  const limit = YB - cH - SP.s2;
  const steps = [
    ['①', '53필지 합필', '서측 + 소로 + 동측 4,964.5㎡', '서측 쐐기만으로는 건축 가능 바닥이 약 920㎡라 램프가 면적을 잠식함'],
    ['②', '차량 전용 소로', '1층 층고 7m, 차로 위는 비움', '차량을 소로에 모으고 가로에는 차가 드나들지 않게 함'],
    ['③', '2층부터 한 판', '소로 위로 이은 바닥, 북 · 남 3m 이격', '한 층 4,322.1㎡의 정형 바닥, 법정 이격 확보'],
    ['④', '두 끝을 비워 코어로', '순환 계단 + 승강기, 건폐율 87.1%', '주차가 어려운 좁은 끝을 사람 이동의 중심으로 씀'],
    ['⑤', '스킵플로어·홀·광장', '소로가 반 층의 이음매, 6F 가변홀', '램프를 줄이고 비는 시간과 위아래 층에 공연 · 체육 · 광장을 담음'],
  ];
  const pitch = G.W / 5, cw = 2.33;
  const iw = 2.2, ih = iw / L.ratio('vol_step1.png');
  const asParas = (st) => [{ t: st[0] + ' ' + st[1], sz: T.lead, b: true, sa: 4 }, { t: '결정  ' + st[2], sz: T.body, sa: 4 }, { t: '이유  ' + st[3], sz: T.body }];
  const ch = Math.max(...steps.map((st) => widthOf(asParas(st), cw - 0.28).h)) + 0.3;
  const spare = Math.max(0, limit - Y0 - ih - SP.s2 - ch);
  const iy = Y0 + spare * 0.4;
  const cy = iy + ih + SP.s2;
  steps.forEach((st, i) => {
    const cx = G.X0 + (i + 0.5) * pitch;
    imageW(s, `vol_step${i + 1}.png`, cx - iw / 2, iy, iw);
    if (i < 4) text(s, [P('›', 22, { color: C.MUTED, align: 'center' })], G.X0 + (i + 1) * pitch - 0.2, iy + ih / 2 - 0.22, 0.4, { h: 0.44, valign: 'middle' });
    rect(s, cx - cw / 2, cy, cw, ch, C.SOFT);
    text(s, [
      { runs: [{ t: st[0] + ' ', color: C.NAVY, b: true }, { t: st[1], b: true }], sz: T.lead, sa: 4 },
      { runs: [{ t: '결정  ', b: true, color: C.NAVY }, { t: st[2] }], sz: T.body, sa: 4 },
      { runs: [{ t: '이유  ', b: true, color: C.NAVY }, { t: st[3] }], sz: T.body },
    ], cx - cw / 2 + 0.14, cy + 0.15, cw - 0.28, {});
  });
  check('s10', cy + ch, limit);
}

// =====================================================================  11 최종안
{
  const s = S('최종안', '주차 75.62%로 요건을 맞추고 공연과 광장을 얹음', 1, '본 시안(면적 계산 · 투시도) · 「주차장법」 제12조의2 / 모든 수치는 개략');
  const A = col(0, 6), B = col(6, 6);
  const numsRows = [
    ['대지면적', '4,964.5㎡', '건축면적', '4,322.1㎡ (건폐율 87.1%)'],
    ['연면적', '43,623.7㎡', '용적률', '481.9% (지하 제외)'],
    ['높이', '지상 약 29.1m', '주차', '약 600대 (75.62%)'],
  ];
  const tblH = 3 * 0.34;
  const capH = 0.26;
  const rh = YB - tblH - SP.s2 - capH - Y0;
  imageBox(s, 'final_drone.jpg', A.x, Y0, A.w, rh);
  caption(s, '드론 시점 조감 투시도 · 남서쪽 상공', A.x, Y0 + rh + 0.03, A.w);
  table(s, A.x, YB - tblH, { cols: [0.95, 1.7, 0.95, A.w - 3.6], style: 'spec', size: T.small, rows: numsRows, label: true, minRow: 0.34 });
  let y = Y0;
  const tabW = 1.15;
  s.addText('사업 요구', { x: B.x, y, w: tabW, h: 0.3, fontFace: FONT, fontSize: T.fine, bold: true, color: C.MUTED, fill: { color: C.SOFT }, align: 'center', valign: 'middle', margin: 0, isTextBox: true });
  s.addText('설계 의도', { x: B.x + tabW + 0.04, y, w: tabW, h: 0.3, fontFace: FONT, fontSize: T.fine, bold: true, color: C.WHITE, fill: { color: C.NAVY }, align: 'center', valign: 'middle', margin: 0, isTextBox: true });
  y += 0.3;
  const intent = ['주차를 한 블록에 모아 상권의 주차 부족과 이면도로 불법주차를 흡수함', '비는 시간과 위아래 층에 공연 · 체육 · 광장을 담음', '상인회와 주민이 쓰는 공용 공간을 둠'];
  const im = L.measure(intent.map((t) => ({ t, sz: T.body, ind: 12, sa: 3 })), B.w - 0.4);
  const ih = im.h + 0.28;
  s.addShape(pres.shapes.RECTANGLE, { x: B.x, y, w: B.w, h: ih, fill: { type: 'none' }, line: { color: C.NAVY, width: 1.25 } });
  text(s, intent.map((t) => P(t, T.body, { ind: 12, bch: '2022', sa: 3 })), B.x + 0.2, y + 0.14, B.w - 0.4, {});
  y += ih + SP.s2;
  s.addText('요구 및 의도 Check', { x: B.x, y, w: 1.75, h: 0.28, fontFace: FONT, fontSize: T.fine, bold: true, color: C.WHITE, fill: { color: C.NAVY }, align: 'center', valign: 'middle', margin: 0, isTextBox: true });
  y += 0.28;
  const chk = [
    { runs: [{ t: '필요 시설을 한 블록에 모두 배치한 것 확인' }], sz: T.small, sa: 2 },
    { runs: [{ t: '주차 비율 75.62%', color: C.GOLD, b: true }, { t: '(요건 70% 이상)로 주차전용건축물 요건 충족' }], sz: T.small, sa: 2 },
    { runs: [{ t: '차량 동선(소로)과 보행 동선(1층 외곽) 분리 확인' }], sz: T.small },
  ];
  const ckm = L.measure(chk.map((p) => ({ t: p.runs.map((r) => r.t).join(''), sz: p.sz, sa: p.sa })), B.w - 0.4);
  const ckh = ckm.h + 0.28;
  rect(s, B.x, y, B.w, ckh, C.CALLOUT);
  text(s, chk.map((p) => Object.assign(p, { color: C.WHITE })), B.x + 0.2, y + 0.14, B.w - 0.4, {});
  y += ckh + SP.s3;
  y += barHeading(s, '최종안 요약', B.x, y, B.w);
  const t = table(s, B.x, y, { cols: [1.05, B.w - 1.05], size: T.small, label: true, fillTo: YB, maxPad: 0.12, rows: [
    ['1층', '서측 서점 · 카페 · 공연 로비 / 소로 차량 전용 차로 / 동측 근생 · 램프 · 정산 · 이륜차'],
    ['2~4층', '스킵플로어 주차 (서측 판 7.0 · 10.3 · 13.6m, 동측 판 +1.65m)'],
    ['5층', '상인회 · 회의 · 공유오피스 1,200㎡ + 전환 가능 주차층'],
    ['6층 · 옥상', '생활체육 · 공연 가변홀(층고 8m) + 옥상 광장 약 1,380㎡'],
    ['지하', 'B1 · B2 공연장 200석(선큰 마당으로 진입), B3 · B4 주차 · 설비'],
    ['코어 · 외피', '끝 코어 2곳 + 보조 피난계단 2곳, 주차층 목재 슬랫 스크린 · 검은 순환 계단'],
  ] });
  check('s11 right', y + t.h, YB);
}

// =====================================================================  12-13 투시도
function renderSlide(title, sub, big, bigLabel, smalls, line, subLine, notes) {
  const s = S(title, sub, 1,
    '투시도: 개념 볼륨 모델, Blender Cycles 렌더 · 하늘 HDRI · 텍스처 · 나무: Poly Haven(CC0) · 주변 건물: OpenStreetMap 높이 자료와 단순 가상 매스 / 실제 설계안이 아님', notes);
  const bottom = YB - 0.3;
  const H = bottom - Y0;
  const bigW = Math.round((H * 1.56) * 100) / 100;
  const sx = G.X0 + bigW + SP.s3, sw = G.X0 + G.W - sx, sh = (H - SP.s2) / 2;
  const lab = (label, x, y) => tag(s, label, x + 0.12, y);
  imageBox(s, big, G.X0, Y0, bigW, H);
  lab(bigLabel, G.X0, Y0 + H - 0.4);
  smalls.forEach(([f, label], i) => {
    const y = Y0 + i * (sh + SP.s2);
    imageBox(s, f, sx, y, sw, sh);
    lab(label, sx, y + sh - 0.4);
  });
  caption(s, subLine, G.X0, YB - 0.24, G.W, { align: 'left' });
}
renderSlide('투시도 Ⅰ', '주차층은 슬랫으로 감싸고 홀과 계단은 켜서 드러냄', 'r_big_hero.jpg', '주간 외관 · 전포대로(서측)에서 본 모습',
  [['r_small_night.jpg', '밤 · 주차층은 낮게, 1층과 6F 홀이 켜짐'], ['r_small_street.jpg', '서전로 × 전포대로 모퉁이 · 1층이 가로를 향해 열림']],
  '停은 목재 슬랫 스크린으로 차분하게, 動은 검은 순환 계단과 켜진 홀로 드러냄',
  '주차층 목재 슬랫(피치 0.24m 가정) · 끝 코어 순환 계단은 검은 도장 강재 · 6F 가변홀 층고 8m',
  '렌더는 Blender 5.2 Cycles(192 샘플, OpenImageDenoise)이며 외피 슬랫 재질은 Poly Haven dark_wood 텍스처를 사용함. 슬랫 폭 0.15m, 피치 0.24m는 가정값임.');
renderSlide('투시도 Ⅱ', '옥상 광장과 소로가 보행과 차량을 한 건물에서 나눔', 'r_big_roof.jpg', '옥상 광장 · 5F 지붕 +21.1m, 맞은편 6F 가변홀',
  [['r_small_sunken.jpg', '끝 코어 · 검은 순환 계단이 지상에서 이어짐'], ['r_small_lane.jpg', '소로 안 · 남→북 일방 차로, 위는 2층 바닥이 덮음']],
  '옥상 광장과 소로를 한 건물 안에서 보행과 차량으로 나눔',
  '옥상 광장 약 1,380㎡(+21.1m, 5F 지붕) · 소로는 남→북 일방, 2층 바닥이 덮은 높이 7m 통로',
  '소로 시점은 황혼 조도로 렌더함. 차량은 단순 모형이며 실제 계획과 무관함.');

// =====================================================================  14 용도 선정 · 층별 계획
{
  const s = S('용도 선정 · 층별 계획', '반경 안에 없는 용도를 층별로 쌓아 한 건물에 모음', 2,
    '부산진구 문화시설 · 공공체육시설현황(data.go.kr) · 부산시 공연장목록 · 현장 답사(2026.9) · 본 시안 / 미등록 민간 공간은 빠졌을 수 있음');
  const wL = 5.2;
  let y = Y0;
  y += barHeading(s, '층별 용도 구성', G.X0, y, wL);
  const hp = drawVector(s, 'program_stack.json', G.X0, y, wL);
  y += hp + SP.s1;
  text(s, [P('지상 23,923.7㎡ + 지하 19,700.0㎡ = 연면적 43,623.7㎡', T.small, { b: true })], G.X0, y, wL, {});
  check('s14 left', y + 0.22, YB);
  const xR = G.X0 + wL + SP.s4, wR = G.X0 + G.W - xR;
  let yr = Y0;
  yr += barHeading(s, '용도별 위치와 선정 근거', xR, yr, wR);
  let t = table(s, xR, yr, { cols: [1.7, 1.05, 0.85, wR - 3.6], head: ['용도', '위치', '면적㎡', '선정 근거'], size: T.small, aligns: ['left', 'left', 'right', 'left'], rows: [
    ['주차장', 'B4~5F, 1F 램프', '32,988.4', '부산진구 확보율 118.5%(기준 130%), 반경 500m 공영 27면'],
    ['공연장 200석', 'B1~B2', '1,900', '1km 안 객석형 소극장 없음, 지하는 전포대로 소음에 강함'],
    ['생활체육 · 공연 가변홀', '6F', '2,850', '1km 안 공연 겸용 가변 홀 없음, 행사에 따라 객석 · 코트를 바꿈'],
    ['서점 · 카페 · 근생', '1F', '1,400', '카페거리 방문객을 건물로 유도, 근생은 10곳 안팎 소점포'],
    ['상인회 · 공유오피스', '5F', '1,200', '답사 범위에서 상인회 사무실을 확인하지 못함'],
    ['옥상 광장', '5F 지붕', '약 1,380', '쉼터 · 공용 공간 부족, 밤에는 공연과 이어 개방'],
  ] });
  yr += t.h + SP.s3;
  yr += barHeading(s, '반경 내 현황조사 (대지 중심 직선거리)', xR, yr, wR);
  t = table(s, xR, yr, { cols: [1.7, 2.0, wR - 3.7], head: ['구분', '500m 안', '1km 안'], size: T.small, fillTo: YB, maxPad: 0.14, rows: [
    ['객석형 소극장', '없음 (지하 라이브클럽 1곳)', '없음 (스탠딩 라이브홀 · 연회장 · 1,727석 대극장)'],
    ['공공 체육관', '없음', '국민체육센터 0.73km (다목적체육관 1,394㎡)'],
    ['공연 겸용 가변 홀', '없음', '없음'],
  ] });
  check('s14 right', yr + t.h, YB);
}

// =====================================================================  15 단면도
{
  const s = S('단면도', '소로를 따라 자른 단면에서 차와 사람의 길이 갈림', 2, '본 시안 개념 단면 · 구조 · 설비 두께는 표현하지 않음, 층고 · 면적 개략');
  const wA = 8.95, xB = G.X0 + wA + 0.1, wB = G.X0 + G.W - xB;
  const ha = drawVector(s, 'secA.json', G.X0, Y0, wA);
  const hb = drawVector(s, 'secB.json', xB, Y0, wB);
  const hmax = Math.max(ha, hb);
  caption(s, 'A 종단면 (남 → 북) · 개념, 층고 · 면적 개략', G.X0, Y0 + hmax + 0.03, wA);
  caption(s, 'B 횡단면 (y = 70m)', xB, Y0 + hmax + 0.03, wB);
  const y = Y0 + hmax + 0.28 + SP.s1;
  const pw = (G.W - SP.s3) / 2;
  const pa = { label: 'A 종단면', items: [{ title: '번호별 구성', lines: ['① 공연장(B1~B2) · ② 옥상 광장 · ③ 6F 가변홀', '④ 개방 순환 계단(지상) · ⑤ 특별피난계단(지하)', '두 끝은 지상에서 비어 있고, 지하 공연장은 선큰 마당으로 빛이 닿음'] }] };
  const pb = { label: 'B 횡단면', items: [{ title: '⑥ 서측 판 7.0 · 10.3 · 13.6m, 동측 판 +1.65m', lines: ['서 · 동 판이 소로 위에서 반 층 엇갈려 램프 길이를 줄임', '지하 공연장은 박스인박스와 방진 바닥으로 차량 진동 차단을 제안'] }] };
  const ph = Math.max(YB - y, panelHeight(pw, pa), panelHeight(pw, pb));
  labeledPanel(s, G.X0, y, pw, Object.assign({ h: ph }, pa));
  labeledPanel(s, G.X0 + pw + SP.s3, y, pw, Object.assign({ h: ph }, pb));
  check('s15', y + ph, YB);
}

// =====================================================================  16 실별 면적
{
  const s = S('실별 면적', '주차 비율 75.62%로 주차전용건축물 요건을 충족함', 2, '본 시안 면적 계산(1평 = 3.3058㎡) · 3m 이격 · 끝 코어 2곳 · 보조 피난계단 2곳 반영 / 모든 면적은 개략');
  const A = col(0, 8), B = col(8, 4);
  const cLine = '주차 비율 75.62%로 주차전용건축물 요건을 충족하고 건폐율 87.1%로 맞춤';
  const cH = -SP.s2;
  const limit = YB - cH - SP.s2;
  let y = Y0;
  y += barHeading(s, '층별 면적 (㎡)', A.x, y, A.w);
  const t = table(s, A.x, y, { cols: [0.85, A.w - 0.85 - 1.15, 1.15], head: ['층', '주요 실', '면적㎡'], size: T.small, aligns: ['left', 'left', 'right'], boldRows: [8], fillTo: limit, maxPad: 0.2, rows: [
    ['6F', '체육 · 공연 가변홀 1,500.0 · 다목적 · 연습실 700.0 · 공연 지원 650.0 · 코어 150.0', '3,000.0'],
    ['5F', '상인회 · 회의 · 공유오피스 1,200.0 · 주차(전환 가능) 2,972.1 · 코어 150.0', '4,322.1'],
    ['2~4F', '주차 4,172.1 · 코어 150.0 (층당)', '4,322.1'],
    ['1F', '서점 400.0 · 카페 400.0 · 공연 로비 300.0 · 근생 600.0 · 램프 900.0 · 정산 100.0 · 이륜차 200.0 · 하역 150.0 · 기타 435.3 · 코어 150.0', '3,635.3'],
    ['B1', '공연장 로비 500.0 · 객석 상부 300.0 · 주차 3,856.5 · 코어 150.0', '4,806.5'],
    ['B2', '공연장 200석 800.0 · 분장 · 창고 300.0 · 주차 3,714.5 · 코어 150.0', '4,964.5'],
    ['B3', '전기 · 기계실 300.0 · 주차 4,514.5 · 코어 150.0', '4,964.5'],
    ['B4', '펌프 · 저수조 600.0 · 주차 4,214.5 · 코어 150.0', '4,964.5'],
    ['합계', '지상 23,923.7(7,237평) + 지하 19,700.0(5,959평)', '43,623.7'],
  ] });
  check('s16 table', y + t.h, limit);
  let yr = Y0;
  yr += barHeading(s, '용도별 구성비', B.x, yr, B.w);
  const dh = 2.55;
  s.addChart(pres.charts.DOUGHNUT, [{ name: '구성비', labels: ['주차장', '문화 · 공연', '상업 · 상인', '코어', '설비 · 지원'], values: [75.62, 11.58, 5.96, 3.44, 3.4] }], {
    x: B.x, y: yr, w: B.w, h: dh, holeSize: 58, chartColors: [C.D1, C.D2, C.D3, C.D4, C.D5], showLegend: false, showPercent: false, showValue: false, dataBorder: { pt: 1.5, color: 'FFFFFF' } });
  text(s, [P('75.62%', T.h2, { b: true, color: C.NAVY, align: 'center' })], B.x + B.w / 2 - 0.8, yr + dh / 2 - 0.27, 1.6, { h: 0.3 });
  text(s, [P('주차장', T.small, { color: C.MUTED, align: 'center' })], B.x + B.w / 2 - 0.8, yr + dh / 2 + 0.03, 1.6, { h: 0.25 });
  yr += dh + SP.s2;
  const lg = [['주차장', '75.62% · 32,988.4㎡', C.D1], ['문화 · 공연', '11.58% · 5,050.0㎡', C.D2], ['상업 · 상인', '5.96% · 2,600.0㎡', C.D3], ['코어', '3.44% · 1,500.0㎡', C.D4], ['설비 · 지원', '3.40% · 1,485.3㎡', C.D5]];
  lg.forEach(([a, b, c], i) => {
    const yy = yr + i * 0.31;
    rect(s, B.x, yy + 0.03, 0.2, 0.2, c);
    text(s, [P(a, T.small, { b: true })], B.x + 0.3, yy, 1.3, { h: 0.26, valign: 'middle' });
    text(s, [P(b, T.small)], B.x + 1.55, yy, B.w - 1.55, { h: 0.26, valign: 'middle' });
  });
  yr += 5 * 0.31 + SP.s2;
  const nTxt = '주차장 32,988.4㎡에는 1F 램프 · 정산 · 이륜차 1,200㎡ 포함. 주차 비율 75.62%, 요건 70% 이상';
  const nh = noteHeight(B.w, null, nTxt);
  noteBox(s, B.x, YB - nh, B.w, null, nTxt);
  check('s16 right', yr, YB - nh - SP.s1);
}

// =====================================================================  17 동선 및 진입 계획
{
  const s = S('동선 및 진입 계획', '차량은 소로로, 보행은 1층 외곽으로 나눔', 2, '본 시안 · 진출입 위치는 구청 · 경찰 협의 전 개념이며 도면은 개략 / 「주차장법 시행규칙」 제5 · 6조');
  const planH = YB - Y0 - 0.28;
  const pw0 = imageH(s, 'plan1f.jpg', G.X0, Y0, planH, { frame: true }).w;
  caption(s, '1층 동선 개념도 · 위치와 폭은 개략', G.X0, Y0 + planH + 0.03, pw0, { align: 'left' });
  const x2 = G.X0 + pw0 + SP.s4, w2 = G.X0 + G.W - x2, cw = (w2 - SP.s3) / 2;
  const cLine = '차량은 소로에 모으고, 보행은 1층 외곽 중심으로 분리함(소로 횡단 1곳)';
  const cH = -SP.s2;
  const noteTxt = '처리 용량(피크 대기행렬) · 소로 남단이 224번길 모퉁이 · 횡단보도 · 정류장과 떨어진 거리 · 출입구 설치 금지 구간(교차로 5m, 정류장 10m)';
  const nH = noteHeight(w2, '확인할 것', noteTxt);
  const g = [
    { label: '차량 동선', items: [{ title: '남단 진입 · 북단 진출', lines: ['소로는 남→북 일방, 차량 전용', '입구 · 출구가 서로 만나지 않음', '400대 초과 노외주차장의 분리 기준'] }] },
    { label: '보행 동선', items: [{ title: '1층 외곽을 한 바퀴', lines: ['전포대로변, 북 · 남 3m 이격 마당, 동측 도로변', '소로 중간에 횡단보도 1곳', '서점 · 카페 · 로비는 전포대로 쪽'] }] },
    { label: '수직 동선', items: [{ title: '끝 코어 2곳이 이동의 중심', lines: ['지상 개방 순환 계단 + 승강기', '지하는 같은 자리에 특별피난계단', '공연 관객은 끝 코어②에서 선큰 마당으로'] }] },
    { label: '하역 · 이륜차', items: [{ title: '동측 이면도로 쪽', lines: ['하역 150㎡, 이륜차 · 자전거 200㎡', '1층 동측 북쪽, 일반 차량과 분리', '주 진출입은 남 · 북단 소로만 사용'] }] },
  ];
  const opt = { sz: T.h2, lsz: T.lead };
  const hs = g.map((p) => panelHeight(cw, Object.assign({}, opt, p)));
  const rowH = [Math.max(hs[0], hs[1]), Math.max(hs[2], hs[3])];
  const avail = YB - Y0 - cH - SP.s2 - nH - SP.s2 - SP.s2;
  const extra = Math.max(0, avail - rowH[0] - rowH[1]) / 2;
  let y = Y0;
  [0, 1].forEach((r) => {
    [0, 1].forEach((c) => labeledPanel(s, x2 + c * (cw + SP.s3), y, cw, Object.assign({ h: rowH[r] + extra }, opt, g[r * 2 + c])));
    y += rowH[r] + extra + SP.s2;
  });
  noteBox(s, x2, y, w2, '확인할 것', noteTxt);
  check('s17', y + nH, YB - cH - SP.s2);
}

// =====================================================================  18 법규 검토 · 구조 · 방재 제안
{
  const s = S('법규 검토 · 구조 · 방재 제안', '주차 요건은 적합하고 출입구 · 구조 · 피난은 조건부임', 2, '법제처 국가법령정보센터 현행본(2026.10.11 조회) · 판정은 참고용이며 최종 판단은 원문으로 다시 확인함 / 구조 · 방재는 확정 설계가 아닌 제안');
  const cLine = '구조 · 방재는 확정 설계가 아닌 제안이며, 설계 단계에서 작도와 계산으로 검증함';
  const cSub = '조건부 3건: 노외주차장 출입구(교차로 5m · 정류장 10m) · 주차장 구조(램프 17%) · 피난(보행거리 50m, 지하 공연장 30m)';
  const nTxtC = cLine + ' ' + cSub;
  const cH = noteHeight(G.W, '주의', nTxtC);
  const limit = YB - cH - SP.s2;
  const ps = [
    { label: '구조', items: [{ title: '주차 모듈에 맞춘 기둥 격자', lines: ['약 7.5~8.1m 단위로 제안', '6F 가변홀은 트러스 · 전이보로 무주 공간 검토'] }] },
    { label: '방재 · 피난', items: [{ title: '지하 공연장과 순환 계단', lines: ['방화구획과 전용 특별피난계단(보행거리 30m)', '개방 순환 계단의 피난계단 인정 여부 검토'] }] },
    { label: '설비 · 운영', items: [{ title: '자연환기와 후속 과제', lines: ['개방 외피로 주차층 자연환기, 지하는 기계환기', '소음 · 조명 운영시간, 처리 용량은 후속 검토'] }] },
  ];
  const pw = (G.W - 2 * SP.s3) / 3;
  const ph = Math.max(...ps.map((p) => panelHeight(pw, p)));
  const t = table(s, G.X0, Y0, { cols: [2.2, 2.75, 3.9, 2.1, 1.383], head: ['항목', '조문', '기준', '계획값', '판정(참고)'], size: T.small, fillTo: limit - ph - SP.s3, maxPad: 0.1, rows: [
    ['주차전용건축물 요건', '「주차장법 시행령」 제1조의2', '주차 외 용도가 근생 · 문화집회 등이면 주차 70% 이상', '75.62%', '적합'],
    ['건폐율 · 용적률', '「주차장법」 제12조의2', '90% 이하 · 1,500% 이하', '87.1% · 481.9%', '적합'],
    ['대지 안의 공지', '「부산광역시 건축 조례」 별표4', '문화집회 1,000㎡ 이상: 건축선에서 3m (20m 이상 도로 면 면제)', '북 · 남 3m, 전포대로 0m', '적합(반영)'],
    ['노외주차장 출입구', '「주차장법 시행규칙」 제5조', '400대 초과 시 입구 · 출구 분리, 교차로 5m · 정류장 10m 안 금지', '남단 진입 · 북단 진출 분리', { t: '조건부', b: true, color: C.NAVY }],
    ['주차장 구조', '「주차장법 시행규칙」 제6조', '경사로 직선 17% · 곡선 14% 이하, 주차부분 높이 2.1m', '층고 3.3m, 반 층 램프', { t: '조건부', b: true, color: C.NAVY }],
    ['피난', '「건축법 시행령」 제34 · 35조', '보행거리 50m(지하 공연장 30m), 지하 3층 이하 특별피난계단', '끝 코어 2 + 보조 2, 지하 특피 4', { t: '조건부', b: true, color: C.NAVY }],
  ] });
  const y = Math.max(Y0 + t.h + SP.s3, limit - ph);
  ps.forEach((p, i) => labeledPanel(s, G.X0 + i * (pw + SP.s3), y, pw, Object.assign({ h: limit - y }, p)));
  check('s18', y + ph, limit);
  noteBox(s, G.X0, YB - cH, G.W, '주의', nTxtC);
}

// =====================================================================  19-20 대안
function altCols(s, items, kind) {
  const cw = (G.W - 2 * SP.s4) / 3;
  const bandH = 0.8;
  const by = YB - bandH;
  items.forEach(([tg, name, sub, ref, f, bl, lim, extra], i) => {
    const x = G.X0 + i * (cw + SP.s4);
    let y = Y0;
    const tw = tag(s, tg, x, y + 0.02, { h: 0.28 }).w;
    text(s, [P(name, T.h2, { b: true })], x + tw + 0.12, y, cw - tw - 0.12, { h: 0.32, valign: 'middle' });
    y += 0.36;
    text(s, [P(sub, T.small, { color: C.MUTED })], x, y, cw, { h: 0.24 });
    y += 0.26 + SP.s1;
    const ih = cw / 1.762;
    imageBox(s, f, x, y, cw, ih);
    y += ih + SP.s2;
    if (kind === 'skin') {
      const rw = 0.95, rh = 1.25;
      imageBox(s, ref, x, y, rw, rh);
      text(s, [P('사례 사진', T.cap, { i: true, color: C.MUTED, align: 'center' })], x, y + rh + 0.03, rw, { h: 0.2 });
      const m = text(s, bl.map((t) => P(t, T.small, { ind: 10, sa: 4 })), x + rw + SP.s2, y, cw - rw - SP.s2, {});
      check('alt skin ' + i, y + Math.max(m.h, rh + 0.23), by - SP.s1);
    } else {
      const pw2 = imageH(s, ref, x, y, 0.62).w;
      const [a1, a2] = extra.split('|');
      text(s, [P('상부 바닥면적', T.cap, { color: C.MUTED, sa: 1 }), P(a1, T.small, { b: true, color: C.NAVY, sa: 1 }), P(a2, T.small, { b: true, color: C.NAVY })], x + pw2 + SP.s2, y, cw - pw2 - SP.s2, { h: 0.62, valign: 'middle' });
      y += 0.62 + SP.s2;
      const m = text(s, bl.map((t) => P(t, T.small, { ind: 10, sa: 4 })), x, y, cw, {});
      check('alt form ' + i, y + m.h, by - SP.s1);
    }
    rect(s, x, by, cw, bandH, C.PDARK);
    text(s, [{ runs: [{ t: '한계  ', b: true, color: C.GOLD }, { t: lim }], sz: T.small, color: C.WHITE }], x + 0.16, by, cw - 0.32, { h: bandH, valign: 'middle' });
  });
}
{
  const s = S('사례 차용 외피 대안', '같은 매스에 사례의 외피 방식만 바꿔 비교함', 2,
    'ArchDaily(Saint-Luc Lieven Van Landschoot, Blaibach NAARO) · Phillip Pessar CC BY 2.0(1111 Lincoln Road) / 투시도: Blender Cycles, 비용 · 법규 · 구조 검토 전',
    '기준안은 목재 슬랫 스크린(투시도 Ⅰ·Ⅱ). 아래 3안은 같은 매스에 사례의 외피 방식만 바꾼 비교용 렌더임. 평면 · 단면 · 면적은 바뀌지 않음.');
  altCols(s, [
    ['Alt 1', 'Saint-Luc 주차건물', '물결치는 목재 슬랫', 'c_saintluc.jpg', 'alt_saintluc.jpg',
      ['슬랫이 층 높이에 따라 물결치고, 슬랫마다 목재 톤이 다름', '옥상 광장을 녹지로 돌려 주는 방식도 함께 차용'], '슬랫 유지관리와 방화 · 내후성 검토 필요'],
    ['Alt 2', '1111 Lincoln Road', '외벽 없는 개방 슬래브', 'c_lincoln.jpg', 'alt_lincoln.jpg',
      ['외벽 없이 슬래브 · 기둥 · 램프만으로 구성, 주차 차량이 보임', '슬래브 단면이 그대로 외관이 되어 층고 변화가 드러남'], '서향 일사 · 도로 소음 차단 수단이 없어 6F 홀 보완 필요'],
    ['Alt 3', 'Concert Hall Blaibach', '화강암 골재 콘크리트 블록', 'c_blaibach.jpg', 'alt_blaibach.jpg',
      ['거친 화강암 칩 콘크리트 매스에 불규칙한 세로 슬릿으로 빛이 새어 나옴', '6F 홀과 주차층을 하나의 단단한 덩어리로 표현'], '자연환기 면적 부족, 기계환기 · 슬릿 방화 검토 필요'],
  ], 'skin');
}
{
  const s = S('형태 대안 3종', '같은 대지에서 매스만 바꾸면 바닥면적이 최대 19% 줄어듦', 2,
    '본 시안 매스 스터디 · 상부 바닥면적은 2층 이상 슬래브 면적 합(개략) · 외피는 Alt 1 · 2 · 3 방식을 각각 적용 / 법규 · 구조 · 주차 대수 검토 전',
    '기준안(상부 바닥면적 약 19,851㎡, 높이 29.8m)과 비교. 끝 코어 2곳과 1층 구성은 유지하고 2층 이상의 매스만 바꿈. 면적은 슬래브 폴리곤 면적 합이며 주차 대수는 재계산하지 않음.');
  altCols(s, [
    ['형태 A', '계단식 테라스', '남→북 1 · 2 · 4 · 6층', 'prof_A.png', 'form_A.jpg',
      ['단마다 녹지 테라스가 생겨 옥상 광장이 3개로 늘어남', '외피는 Saint-Luc식 물결 슬랫, 지붕을 녹지로 돌려 줌'], '바닥면적이 줄어 주차 대수 재검토 필요', '약 16,100㎡|−19% · 최고 30.8m'],
    ['형태 B', '엇갈린 슬래브', '층마다 폭 · 위치 · 층고가 다름', 'prof_B.png', 'form_B.jpg',
      ['슬래브가 서로 내밀고 들어가 그림자와 처마가 생김', '1111 Lincoln Road처럼 외벽 없이 기둥 · 슬래브 · 램프만 보임'], '서향 일사 · 도로 소음 차단 수단이 없어 보완 필요', '약 18,600㎡|−6% · 최고 31.4m'],
    ['형태 C', '대각선 협곡', '틈 폭 약 9m, 6F 홀이 위에서 이음', 'prof_C.png', 'form_C.jpg',
      ['매스를 대각선 틈으로 갈라 빛과 바람이 들고, 틈 안 검은 계단이 옥상까지 오름', '외피는 Blaibach식 화강암 골재 콘크리트와 세로 슬릿'], '두 판으로 나뉘어 동선 · 방화구획 · 코어 재계획 필요', '약 19,700㎡|−1% · 최고 30.5m'],
  ], 'form');
}

// =====================================================================  21 확인할 것 + THANK YOU
{
  const s = S('확인할 것', '남은 일은 법규 원문 확인과 작도임', 2, '본 시안의 열린 이슈 · 수치는 모두 개략이며 확정은 법규 원문 확인과 작도에서 이뤄짐');
  const A = col(0, 8), B = col(8, 4);
  const nTxt = '사업성(토지 매입 · 공사비 · 주차 수입) · 합필 방식과 운영 주체 · 침수 · 지반 · 소음 실측 · 상세 평면 · 단면(미작성)';
  const nh = noteHeight(A.w, '본 보고서에서 다루지 않은 사항', nTxt);
  const t = table(s, A.x, Y0, { cols: [0.5, 4.6, A.w - 5.1], head: ['#', '확인할 것', '이유 · 방향'], size: T.body, aligns: ['center', 'left', 'left'], fillTo: YB - nh - SP.s3, maxPad: 0.3, rows: [
    ['1', '약 600대와 주차 면적 약 33,000㎡의 관계', '1대당 약 55㎡로 계산됨, 기준층 배치로 확인'],
    ['2', '진입부(소로 남단)와 224번길 모퉁이 · 횡단보도 · 정류장 거리', '출입구 설치 금지 구간(5m · 10m)'],
    ['3', '개방 순환 계단의 피난계단 인정 여부', '안 되면 보조 피난계단 2곳이 법정 계단 역할'],
    ['4', '대지 안의 공지의 지하층 적용 여부', '지금은 지하를 대지 전체로 계산'],
    ['5', '207-15 · 79 용도지역 표기', '제3종일반주거지역 동시 표기'],
    ['6', '보행거리 작도(코어 4곳 50m, 지하 공연장 30m)', '피난 조건부 판정 해소'],
    ['7', '6F 외피 재료, 소음 · 조명 운영시간, 소음 실측', '후속 설계 과제'],
  ] });
  noteBox(s, A.x, YB - nh, A.w, '본 보고서에서 다루지 않은 사항', nTxt);
  check('s21', Y0 + t.h, YB - nh - SP.s2);
  rect(s, B.x, Y0, B.w, YB - Y0, C.DIVG);
  text(s, [P('THANK', 40, { b: true, color: C.WHITE, align: 'center' }), P('YOU', 40, { b: true, color: C.WHITE, align: 'center' })], B.x, Y0 + 0.9, B.w, { ls: 1.0 });
  text(s, [P('停動館', 34, { face: SERIF, color: C.WHITE, align: 'center' })], B.x, Y0 + 2.5, B.w, { h: 0.8, valign: 'middle' });
  text(s, [P('전포 정동관', T.body, { b: true, color: C.WHITE, align: 'center', sa: 3 }), P('낮에는 주차장, 밤에는 공연과 옥상 광장', T.small, { color: C.WHITE, align: 'center' })], B.x + 0.2, Y0 + 3.5, B.w - 0.4, {});
  text(s, [P('202325137 정성윤', T.body, { b: true, color: C.WHITE, align: 'center' })], B.x, YB - 0.7, B.w, { h: 0.4, valign: 'middle' });
}

// ---------------------------------------------------------------- finish
const miss = L.flushMisses();
if (require.main === module || process.env.DECK_RUN) {
  const out = process.env.OUT || path.join(__dirname, 'v5.pptx');
  if (miss.length) {
    fs.writeFileSync(path.join(__dirname, 'misses.json'), JSON.stringify(miss));
    console.log('MISSES', miss.length);
    process.exit(3);
  }
  pres.writeFile({ fileName: out }).then(() => { console.log('WROTE', out); WARN.forEach((w) => console.log('WARN', w)); });
}
