import { chromium } from '/opt/node-tools/node_modules/playwright/index.mjs';
const [,, outdir, ...pages] = process.argv;
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
for (const f of pages) { await p.goto('file://' + f); await p.waitForTimeout(700); await p.evaluate(() => document.fonts.ready);
  const r = await p.evaluate(() => { const s = document.querySelector('section'); const bad = []; const sr = s.getBoundingClientRect();
    s.querySelectorAll('*').forEach(e => { const r = e.getBoundingClientRect(); if (r.width && (r.bottom > 1081 || r.right > 1921)) bad.push((e.tagName + ':' + (e.textContent || '').slice(0, 24)).replace(/\s+/g, ' ') + ' b=' + Math.round(r.bottom) + ' r=' + Math.round(r.right)); });
    return bad.slice(0, 4); });
  await p.screenshot({ path: f.replace('.html', '.png') }); console.log(f.split('/').pop(), r.length ? 'OVERFLOW ' + r.join(' | ') : 'ok'); }
await b.close();