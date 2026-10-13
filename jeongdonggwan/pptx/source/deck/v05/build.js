'use strict';
// measure → build loop:  node build.js [out.pptx]
//  1) deck.js runs; text blocks not in the measure cache are written to misses.json (exit 3)
//  2) mk_measure.js puts those blocks into a throw-away pptx (same XML as the deck, lang=ko-KR),
//     PowerPoint (COM) reads BoundHeight/BoundWidth of each → measure_cache.json
//  3) repeat until deck.js writes the pptx; then lang=ko-KR is stamped on every run (word-level Korean wrapping)
const { spawnSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const here = __dirname;
const out = path.resolve(process.argv[2] || path.join(here, 'v5.pptx'));
const cachePath = path.join(here, 'measure_cache.json');
const reqPath = path.join(here, 'misses.json');
const mPptx = path.join(here, 'measure_req.pptx');
const resPath = path.join(here, 'measured.json');
const env = Object.assign({}, process.env, { PYTHONUTF8: '1' });
const py = (args) => spawnSync('python', args, { encoding: 'utf8', env });

for (let pass = 1; pass <= 8; pass++) {
  const r = spawnSync(process.execPath, [path.join(here, 'deck.js')], { env: Object.assign({}, env, { DECK_RUN: '1', OUT: out }), encoding: 'utf8', maxBuffer: 64 * 1024 * 1024 });
  process.stdout.write(r.stdout || '');
  if (r.status === 0) { console.log(`build ok (pass ${pass})`); break; }
  if (r.status !== 3) { console.error(r.stdout, r.stderr || 'deck.js failed'); process.exit(1); }
  const misses = JSON.parse(fs.readFileSync(reqPath, 'utf8'));
  console.log(`pass ${pass}: measuring ${misses.length} text blocks via PowerPoint`);
  let m = spawnSync(process.execPath, [path.join(here, 'mk_measure.js'), reqPath, mPptx], { encoding: 'utf8' });
  if (m.status !== 0) { console.error(m.stdout, m.stderr); process.exit(2); }
  m = py([path.join(here, '..', 'fixlang.py'), mPptx]);
  if (m.status !== 0) { console.error(m.stdout, m.stderr); process.exit(2); }
  if (fs.existsSync(resPath)) fs.unlinkSync(resPath);
  m = spawnSync('powershell.exe', ['-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', path.join(here, 'measure2.ps1'), '-pptx', mPptx, '-outPath', resPath], { encoding: 'utf8', timeout: 600000 });
  if (m.status !== 0 || !fs.existsSync(resPath)) { console.error(m.stdout, m.stderr); process.exit(2); }
  const res = JSON.parse(fs.readFileSync(resPath, 'utf8'));
  const cache = fs.existsSync(cachePath) ? JSON.parse(fs.readFileSync(cachePath, 'utf8')) : {};
  Object.assign(cache, res);
  fs.writeFileSync(cachePath, JSON.stringify(cache));
}

const fl = py([path.join(here, '..', 'fixlang.py'), out]);
process.stdout.write(fl.stdout || '');
if (fl.status !== 0) { console.error(fl.stderr); process.exit(1); }
console.log('FINAL', out);
