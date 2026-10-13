'use strict';
// build a throw-away pptx that holds every requested text block (same XML as the deck) → measure2.ps1
const pptxgen = require('pptxgenjs');
const fs = require('fs');
const [, , inPath, outPath] = process.argv;
const reqs = JSON.parse(fs.readFileSync(inPath, 'utf8'));
const FONT = 'Malgun Gothic';
const p = new pptxgen(); p.layout = 'LAYOUT_WIDE';
let s = null;
reqs.forEach((r, i) => {
  if (i % 40 === 0) s = p.addSlide();          // many shapes per slide is fine; keep slides small
  const arr = [];
  r.paras.forEach((q, j) => {
    const o = { fontSize: q.sz, bold: !!q.b, fontFace: FONT, color: '000000', align: 'left' };
    if (q.ind) o.bullet = { indent: q.ind, characterCode: '2013' };
    if (q.sa) o.paraSpaceAfter = q.sa;
    if (j < r.paras.length - 1) o.breakLine = true;
    arr.push({ text: q.t, options: o });
  });
  s.addText(arr, { x: 0.1, y: 0.1, w: r.w, h: 1.0, margin: 0, valign: 'top', fontFace: FONT, isTextBox: true, wrap: true,
    lineSpacingMultiple: r.ls !== 1 ? r.ls : undefined, objectName: 'm_' + r.k });
});
p.writeFile({ fileName: outPath }).then(() => console.log('ok', reqs.length));
