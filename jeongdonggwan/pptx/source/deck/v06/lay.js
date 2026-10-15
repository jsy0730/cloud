'use strict';
// 전포 정동관 · 공설기 v1.2 레이아웃 라이브러리 (PowerPoint COM 실측 기반)
const pptxgen = require('pptxgenjs');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const HERE = __dirname;
const WORK = path.resolve(HERE, '..');
const IMGDIRS = [path.join(WORK, 'img2'), path.join(WORK, 'img')];

// ---------------------------------------------------------------- tokens (공설기 v1.2, Deck/light)
const C = {
  INK: '000000', MUTED: '595959', LINE: 'A0A2A5', PANEL: 'F0F3F7', SOFT: 'F2F2F2', TABOFF: '8C8C8C',
  THEAD: '767171', TCELL: 'E7E6E6', CHAR: '525252', CALLOUT: '323232', DIVG: '4C4C4C', PDARK: '141414',
  NAVY: '002060', NSOFT: 'DAE3F3', SLATE: '8493B2', GOLD: 'FFC000', SIGNAL: 'FF0000', PIN: 'C00000', WHITE: 'FFFFFF',
  D1: '08205E', D2: '4272C4', D3: '7F9DCF', D4: 'ABBDE0', D5: 'DBE2F5',
};
const FONT = 'Malgun Gothic';
const SERIF = 'Noto Serif KR Black';
// fixed type scale (pt) — roles, never scaled by box size
const T = { src: 8.5, tab: 8.5, cap: 9.5, fine: 9.5, small: 11, body: 12, lead: 13.5, h2: 15, title: 17, num: 30 };
// 12-col grid on a 13.333 × 7.5 in slide (1280 × 720 px, 48 px gutter, 32 px column gap)
const G = { X0: 0.5, W: 12.333, CG: 1 / 3, Y0: 1.14, YB: 6.8, SW: 13.333, SH: 7.5 };
const CW = (G.W - 11 * G.CG) / 12;
const col = (i, n) => ({ x: G.X0 + i * (CW + G.CG), w: n * CW + (n - 1) * G.CG });
const SP = { s1: 0.083, s2: 0.167, s3: 0.25, s4: 0.333 };   // 8 · 16 · 24 · 32 px

// ---------------------------------------------------------------- measurement (PowerPoint COM, cached)
const CACHE_PATH = path.join(HERE, 'measure_cache.json');
let CACHE = fs.existsSync(CACHE_PATH) ? JSON.parse(fs.readFileSync(CACHE_PATH, 'utf8')) : {};
const MISS = {};
function mkey(req) { return crypto.createHash('md5').update(JSON.stringify(req)).digest('hex').slice(0, 16); }
function measure(paras, w, ls = 1.0) {
  const req = { v: 2, w: Math.round(w * 1000) / 1000, ls, paras: paras.map((p) => ({ t: p.t, sz: p.sz, b: !!p.b, sa: p.sa || 0, ind: p.ind || 0 })) };
  const k = mkey(req);
  if (CACHE[k]) return CACHE[k];
  MISS[k] = Object.assign({ k }, req);
  let h = 0, wm = 0;
  req.paras.forEach((p, i) => {
    const cpl = Math.max(3, Math.floor((req.w - p.ind / 72) / (p.sz / 72 * 0.95)));
    const lines = Math.max(1, Math.ceil([...p.t].length / cpl));
    h += lines * p.sz * 1.2 / 72 * ls + (i < req.paras.length - 1 ? p.sa / 72 : 0);
    wm = Math.max(wm, Math.min(req.w, [...p.t].length * p.sz / 72 * 0.95));
  });
  return { h, w: wm, est: true };
}
function flushMisses() {
  const keys = Object.keys(MISS);
  return keys.length ? keys.map((k) => MISS[k]) : [];
}
function saveCache(extra) { CACHE = Object.assign(CACHE, extra); fs.writeFileSync(CACHE_PATH, JSON.stringify(CACHE)); }

// ---------------------------------------------------------------- deck
const pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE';
pres.title = '전포 정동관 · 복합주차장 시안 (공설기 v1.2)';
pres.author = '정성윤';
pres.theme = { headFontFace: FONT, bodyFontFace: FONT };
pres.defineSlideMaster({ title: 'GS', background: { color: 'FFFFFF' }, objects: [] });
const SEC = ['INTRODUCTION', 'MAIN SUBJECT', 'CONCLUSION'];
const _sec = new Set();
function sec(i) { if (!_sec.has(i)) { pres.addSection({ title: SEC[i] }); _sec.add(i); } }
let PAGE = 0;

// ---------------------------------------------------------------- image helpers
function imgPath(n) {
  for (const d of IMGDIRS) { const p = path.join(d, n); if (fs.existsSync(p)) return p; }
  throw new Error('image not found: ' + n);
}
const DIMS = JSON.parse(fs.readFileSync(path.join(WORK, 'dims.json'), 'utf8'));
function dims(n) { const d = DIMS[n]; if (!d) throw new Error('no dims for ' + n); return d; }
function ratio(n) { const [w, h] = dims(n); return w / h; }

// ---------------------------------------------------------------- primitives
function rect(s, x, y, w, h, fill, o = {}) {
  s.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: fill, transparency: o.tr || 0 }, line: o.line ? { color: o.line, width: o.lw || 0.75 } : { type: 'none' } });
}
function hline(s, x, y, w, color = C.LINE, wt = 0.75) { s.addShape(pres.shapes.LINE, { x, y, w, h: 0, line: { color, width: wt } }); }
function vline(s, x, y, h, color = C.LINE, wt = 0.75) { s.addShape(pres.shapes.LINE, { x, y, w: 0, h, line: { color, width: wt } }); }

// paras: [{t | runs:[{t,b,color,i,face}], sz, b, color, i, sa, ind, align, face}]
function text(s, paras, x, y, w, o = {}) {
  const ls = o.ls || 1.0;
  const flat = (p) => (p.runs ? p.runs.map((r) => r.t).join('') : p.t);
  const m = measure(paras.map((p) => ({ t: flat(p), sz: p.sz, b: p.b, sa: p.sa, ind: p.ind })), w, ls);
  const arr = [];
  paras.forEach((p, i) => {
    const runs = p.runs || [{ t: p.t }];
    runs.forEach((r, j) => {
      const opt = {
        fontSize: p.sz, bold: r.b !== undefined ? r.b : !!p.b, italic: !!(r.i || p.i), color: r.color || p.color || o.color || C.INK,
        fontFace: r.face || p.face || o.face || FONT,
      };
      if (j === 0) {
        if (p.ind) opt.bullet = { indent: p.ind, characterCode: p.bch || '2013' };
        if (p.sa) opt.paraSpaceAfter = p.sa;
        opt.align = p.align || o.align || 'left';
      }
      if (j === runs.length - 1 && i < paras.length - 1) opt.breakLine = true;
      arr.push({ text: r.t, options: opt });
    });
  });
  const h = o.h !== undefined ? o.h : m.h + 0.02;
  s.addText(arr, {
    x, y, w, h, margin: 0, valign: o.valign || 'top', fontFace: FONT, isTextBox: true, wrap: true,
    lineSpacingMultiple: ls !== 1 ? ls : undefined, charSpacing: o.charSpacing, rotate: o.rotate, objectName: o.name,
  });
  return { h: m.h, w: m.w };
}
const P = (t, sz = T.body, o = {}) => Object.assign({ t, sz }, o);

function tag(s, label, x, y, o = {}) {
  const sz = o.sz || T.fine;
  const w = measure([{ t: label, sz, b: true }], 6).w + 0.22;
  const h = o.h || 0.26;
  s.addText(label, { x, y, w, h, fontFace: FONT, fontSize: sz, bold: true, color: o.color || C.WHITE, fill: { color: o.fill || C.NAVY }, align: 'center', valign: 'middle', margin: 0, isTextBox: true });
  return { w, h };
}

// BarHeading (v1.2): short heavy navy bar + bold label
function barHeading(s, label, x, y, w = 6) {
  const h = measure([{ t: label, sz: T.lead, b: true }], w).h;
  rect(s, x, y + 0.03, 0.055, h - 0.04, C.NAVY);
  text(s, [P(label, T.lead, { b: true })], x + 0.15, y, w, { h });
  return h + SP.s1 + 0.04;
}

// caption (v1.2): italic, muted, right-aligned under the thing it supports
function caption(s, label, x, y, w, o = {}) {
  const m = text(s, [P(label, T.cap, { i: true, color: C.MUTED, align: o.align || 'right' })], x, y, w);
  return m.h + 0.02;
}

// image placed with aspect ratio; returns {h}
function imageW(s, name, x, y, w, o = {}) {
  const h = o.h || w / ratio(name);
  if (o.cover) {
    const [iw, ih] = dims(name);
    s.addImage({ path: imgPath(name), x, y, w: iw / 100, h: ih / 100, sizing: { type: 'cover', w, h } });
  } else {
    s.addImage({ path: imgPath(name), x, y, w, h });
  }
  if (o.frame) s.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { type: 'none' }, line: { color: C.LINE, width: 0.75 } });
  return { h };
}
function imageH(s, name, x, y, h, o = {}) {
  const w = h * ratio(name);
  s.addImage({ path: imgPath(name), x, y, w, h });
  if (o.frame) s.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { type: 'none' }, line: { color: C.LINE, width: 0.75 } });
  return { w };
}
function imageBox(s, name, x, y, w, h, o = {}) {      // cover-crop into a box
  const [iw, ih] = dims(name);
  s.addImage({ path: imgPath(name), x, y, w: iw / 100, h: ih / 100, sizing: { type: 'cover', w, h } });
  if (o.frame) s.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { type: 'none' }, line: { color: C.LINE, width: 0.75 } });
}

// ---------------------------------------------------------------- LabeledPanel (navy tag + ▶ topics + dash lines)
// groups-less single panel: {label, items:[{title, lines:[]}]} ; returns height
function panelHeight(w, o) {
  const inner = w - 0.34;
  let h = 0.12 + 0.26 + 0.1;
  o.items.forEach((it, i) => {
    const paras = [P('▶ ' + it.title, o.sz || T.body, { b: true, sa: 2 })].concat((it.lines || []).map((l) => P(l, o.lsz || T.small, { ind: 9, sa: 1 })));
    h += measure(paras, inner).h + (i < o.items.length - 1 ? 0.1 : 0);
  });
  return h + 0.14;
}
function labeledPanel(s, x, y, w, o) {
  const nat = panelHeight(w, o);
  const h = Math.max(o.h || 0, nat);
  rect(s, x, y, w, h, C.SOFT);
  tag(s, o.label, x + 0.14, y + 0.12);
  const inner = w - 0.34;
  const n = o.items.length;
  const spare = Math.max(0, h - nat) / (n + 1);
  let cy = y + 0.12 + 0.26 + 0.1 + spare;
  o.items.forEach((it, i) => {
    const paras = [{ runs: [{ t: '▶ ', color: C.SLATE, b: true }, { t: it.title, b: true }], sz: o.sz || T.body, sa: 2 }]
      .concat((it.lines || []).map((l) => P(l, o.lsz || T.small, { ind: 9, sa: 1 })));
    const m = text(s, paras, x + 0.17, cy, inner);
    cy += m.h + 0.1 + spare;
  });
  return h;
}

// ---------------------------------------------------------------- NoteBox (rounded, hairline)
function noteHeight(w, label, body, sz = T.small) {
  const runs = (label ? label.length : 0);
  return measure([{ t: (label ? label + '  ' : '') + body, sz }], w - 0.36).h + 0.2;
}
function noteBox(s, x, y, w, label, body, o = {}) {
  const sz = o.sz || T.small;
  const h = noteHeight(w, label, body, sz);
  s.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: C.PANEL }, line: { type: 'none' } });
  const runs = [];
  if (label) runs.push({ t: label + '  ', b: true, color: C.NAVY });
  runs.push({ t: body });
  text(s, [{ runs, sz }], x + 0.18, y + 0.1, w - 0.36, { h: h - 0.2, valign: 'middle' });
  return h;
}

// ---------------------------------------------------------------- Conclusion (Takeaway): navy tab + red conclusion + evidence line
function conclusionHeight(w, line, sub) {
  const inner = w - 0.78 - 0.35;
  const paras = [P('→ ' + line, T.lead, { b: true, sa: 3 })];
  if (sub) paras.push(P(sub, T.small));
  return measure(paras, inner).h + 0.26;
}
function conclusion(s, line, sub, o = {}) {
  const x = o.x !== undefined ? o.x : G.X0, w = o.w !== undefined ? o.w : G.W;
  const h = conclusionHeight(w, line, sub);
  const y = o.y !== undefined ? o.y : G.YB - h;
  rect(s, x, y, w, h, C.PANEL);
  s.addText('결론', { x, y, w: 0.78, h, fontFace: FONT, fontSize: T.body, bold: true, color: C.WHITE, fill: { color: C.NAVY }, align: 'center', valign: 'middle', margin: 0, isTextBox: true });
  const paras = [{ t: '→ ' + line, sz: T.lead, b: true, color: C.SIGNAL, sa: 3 }];
  if (sub) paras.push(P(sub, T.small));
  text(s, paras, x + 0.78 + 0.18, y, w - 0.78 - 0.35, { h, valign: 'middle' });
  return { y, h };
}

// ---------------------------------------------------------------- tables
// o: {cols:[in], head:[..], rows:[[cell]], size, aligns, label:boolean (first col bold), style:'data'|'spec', boldRows, padX, padY}
function table(s, x, y, o) {
  const sz = o.size || T.body;
  const padX = o.padX || 0.1, padY = o.padY || 0.055;
  const spec = o.style === 'spec';
  const al = (i) => (o.aligns && o.aligns[i]) || 'left';
  const cell = (c) => (typeof c === 'object' && c !== null && !Array.isArray(c) ? c : { t: String(c) });
  const rowsAll = (o.head ? [o.head.map((t) => ({ t, head: true }))] : []).concat(o.rows.map((r, ri) => r.map((c, ci) => Object.assign(cell(c), { ri, ci }))));
  const heights = rowsAll.map((r, rix) => {
    let mh = 0;
    r.forEach((c, ci) => {
      const bold = c.head || c.b || (o.label && ci === 0) || (o.boldRows && o.boldRows.includes(c.ri));
      const m = measure([{ t: c.t, sz: c.sz || sz, b: !!bold }], o.cols[ci] - 2 * padX);
      mh = Math.max(mh, m.h);
    });
    return Math.max(o.minRow || 0.3, mh + 2 * padY);
  });
  const body = rowsAll.map((r) => r.map((c, ci) => {
    const bold = c.head || c.b || (o.label && ci === 0) || (o.boldRows && o.boldRows.includes(c.ri));
    let fill = C.TCELL, color = c.color || C.INK;
    if (c.head) { fill = C.THEAD; color = C.WHITE; }
    else if (spec) { fill = ci === 0 ? C.PANEL : C.WHITE; }
    else if (o.label && ci === 0) { fill = C.PANEL; }
    if (c.fill) fill = c.fill;
    return { text: c.t, options: { fontSize: c.sz || sz, bold: !!bold, color, fill: { color: fill }, align: c.head ? (o.aligns ? al(ci) : 'left') : (spec && ci === 0 ? 'center' : al(ci)), valign: 'middle', fontFace: FONT } };
  }));
  const w = o.cols.reduce((a, b) => a + b, 0);
  if (o.fillTo) {
    const nat = heights.reduce((a, b) => a + b, 0);
    const nb = heights.length - (o.head ? 1 : 0);
    const add = Math.max(0, Math.min((o.fillTo - y - nat) / nb, o.maxPad || 0.28));
    for (let i = o.head ? 1 : 0; i < heights.length; i++) heights[i] += add;
  }
  s.addTable(body, {
    x, y, w, colW: o.cols, rowH: heights, fontFace: FONT,
    border: spec ? { type: 'solid', pt: 1, color: C.INK } : { type: 'solid', pt: 1.5, color: C.WHITE },
    margin: [padY, padX, padY, padX],
  });
  return { h: heights.reduce((a, b) => a + b, 0), rows: heights };
}

// ---------------------------------------------------------------- vector drawing (editable native shapes) from matplotlib export
function drawVector(s, jsonName, x0, y0, w, o = {}) {
  const V = JSON.parse(fs.readFileSync(path.join(WORK, 'img', jsonName), 'utf8'));
  const [xmin, xmax] = V.xlim, [ymin, ymax] = V.ylim;
  const sc = w / (xmax - xmin), f = w / V.width_in;
  const Hh = w * V.height_in / V.width_in, sy = Hh / (ymax - ymin);
  const px = (X) => x0 + (X - xmin) * sc, py = (Y) => y0 + (ymax - Y) * sy;
  const dash = (ls) => (ls === 'dash' ? 'dash' : ls === 'sysDot' ? 'sysDot' : ls === 'dashDot' ? 'dashDot' : 'solid');
  const emw = (t, size) => { let w_ = 0; for (const ch of t) w_ += ch.charCodeAt(0) > 0x2E80 ? 1.0 : 0.58; return w_ * size / 72; };
  const fixed = o.sizes || [8.5, 9.5, 11];
  V.items.forEach((d) => {
    if (d.type === 'rect' || d.type === 'rrect' || d.type === 'ellipse') {
      const sh = { x: px(d.x), y: py(d.y + d.h), w: d.w * sc, h: d.h * sy };
      sh.fill = d.fill ? { color: d.fill, transparency: Math.round((1 - d.fa) * 100) } : { type: 'none' };
      sh.line = d.line ? { color: d.line, width: Math.max(0.25, d.lw * f), dashType: dash(d.ls) } : { type: 'none' };
      if (d.type === 'rrect') sh.rectRadius = 0.04;
      s.addShape(d.type === 'ellipse' ? pres.shapes.OVAL : d.type === 'rrect' ? pres.shapes.ROUNDED_RECTANGLE : pres.shapes.RECTANGLE, sh);
    } else if (d.type === 'line') {
      for (let i = 0; i < d.pts.length - 1; i++) {
        const ax = px(d.pts[i][0]), ay = py(d.pts[i][1]), bx = px(d.pts[i + 1][0]), by = py(d.pts[i + 1][1]);
        const w_ = Math.abs(bx - ax), h_ = Math.abs(by - ay);
        if (w_ < 0.002 && h_ < 0.002) continue;
        s.addShape(pres.shapes.LINE, { x: Math.min(ax, bx), y: Math.min(ay, by), w: w_, h: h_, flipV: (bx - ax) * (by - ay) < 0, line: { color: d.color, width: Math.max(0.25, d.lw * f), dashType: dash(d.ls) } });
      }
    } else if (d.type === 'text') {
      const size = d.size >= 10 ? fixed[2] : d.size >= 9 ? fixed[1] : fixed[0];
      const tw = emw(d.text, size) + 0.1, th = size * 1.4 / 72;
      const cx = px(d.x), cy = py(d.y);
      let bx = cx - tw / 2, by = cy - th / 2;
      if (!d.rot) {
        if (d.ha === 'left') bx = cx; else if (d.ha === 'right') bx = cx - tw;
        if (d.va === 'bottom' || d.va === 'baseline') by = cy - th; else if (d.va === 'top') by = cy;
      }
      s.addText(d.text, { x: bx, y: by, w: tw, h: th, fontFace: FONT, fontSize: size, bold: !!d.bold, color: d.color, margin: 0, wrap: false, isTextBox: true,
        align: d.rot ? 'center' : (d.ha === 'left' ? 'left' : d.ha === 'right' ? 'right' : 'center'), valign: 'middle', rotate: d.rot ? (360 - d.rot) % 360 : 0 });
    }
  });
  return Hh;
}

// ---------------------------------------------------------------- slide chrome (term voice)
function header(s, num, title, sub, active) {
  const NUMW = 0.66;
  text(s, [P(num, T.num, { b: true, color: C.NAVY })], G.X0, 0.2, NUMW, { h: 0.62, valign: 'middle' });
  const tx = G.X0 + NUMW + 0.06;
  const tw = measure([{ t: title, sz: T.title, b: true }], 9).w + 0.12;
  text(s, [P(title, T.title, { b: true })], tx, 0.2, tw, { h: 0.62, valign: 'middle', charSpacing: -0.3 });
  const bx = tx + tw + 0.08;
  rect(s, bx, 0.36, 0.045, 0.3, C.NAVY);
  const sw = measure([{ t: sub, sz: T.body }], 7).w + 0.1;
  text(s, [P(sub, T.body, { color: C.MUTED })], bx + 0.15, 0.2, sw, { h: 0.62, valign: 'middle' });
  const tabW = 1.18, tabG = 0.04, tabsW = 3 * tabW + 2 * tabG;
  const tabX = G.X0 + G.W - tabsW;
  const lx = bx + 0.15 + sw + 0.2;
  if (tabX - 0.2 - lx > 0.3) hline(s, lx, 0.51, tabX - 0.2 - lx, C.NAVY, 0.75);
  SEC.forEach((t, i) => {
    const on = i === active;
    s.addText(t, { x: tabX + i * (tabW + tabG), y: 0.38, w: tabW, h: 0.28, fontFace: FONT, fontSize: T.tab, bold: on, align: 'center', valign: 'middle', margin: 0, isTextBox: true,
      color: on ? C.WHITE : C.TABOFF, fill: { color: on ? C.NAVY : C.SOFT } });
  });
}
function footer(s, source, page, o = {}) {
  const dark = !!o.dark;
  const xL = o.xL !== undefined ? o.xL : 1.68, xR = o.xR !== undefined ? o.xR : G.X0 + G.W;
  text(s, [P('停動館', 15, { face: SERIF, color: dark ? '8FB0EC' : C.NAVY })], G.X0, 6.98, 1.1, { h: 0.42, valign: 'middle' });
  hline(s, xL, 7.03, xR - xL, dark ? '3D4864' : '7F7F7F', 0.5);
  if (source) text(s, [P('출처: ' + source, T.src, { color: dark ? 'A7B0C2' : C.MUTED })], xL, 7.08, Math.min(9.4, xR - xL - 1.8), { h: 0.34 });
  text(s, [P('담당자 정성윤 · ' + String(page).padStart(2, '0'), T.src, { color: dark ? 'A7B0C2' : C.MUTED, align: 'right' })], xR - 1.733, 7.08, 1.733, { h: 0.2 });
}
function slide(num, title, sub, active, source, notes) {
  sec(active);
  const s = pres.addSlide({ masterName: 'GS', sectionTitle: SEC[active] });
  PAGE += 1;
  header(s, num, title, sub, active);
  footer(s, source, PAGE);
  if (notes) s.addNotes(notes);
  return s;
}
function blank(active) {
  sec(active);
  const s = pres.addSlide({ masterName: 'GS', sectionTitle: SEC[active] });
  PAGE += 1;
  return s;
}

module.exports = { pres, C, FONT, SERIF, T, G, CW, col, SP, measure, flushMisses, saveCache, MISS, rect, hline, vline, text, P, tag, barHeading, caption, imageW, imageH, imageBox,
  labeledPanel, panelHeight, noteBox, noteHeight, conclusion, conclusionHeight, table, drawVector, header, footer, slide, blank, SEC, sec, imgPath, dims, ratio, pageNo: () => PAGE };
