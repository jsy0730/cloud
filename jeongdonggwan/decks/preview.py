# preview harness: render slide html files with a plain browser (margins reset) to check overflow
import sys, os, json, re, subprocess
D = '/tmp/claude-0/-home-user-cloud/76ed2005-4113-58c6-b90f-f280afa8844d/scratchpad/'
A = D + 'build/assets/'
KEY2FILE = {'aerial': 'aerial.jpg', 'hero': 'hero_sw.jpg', 'street': 'street_nw.jpg', 'night': 'night_sw.jpg', 'lane': 'lane_entry.jpg', 'roof': 'roof_view.jpg', 'sunken': 'sunken.jpg',
            'secA': 'secA.png', 'secB': 'secB.png', 'keyplan': 'keyplan.png', 'plan1f': 'plan1f.png', 'steps': 'steps.png', 'site': 'site_eum.png', 'env': 'env_map.png', 'transit': 'transit_map.png',
            'pk1': 'photo_parking1.jpg', 'pk2': 'photo_parking2.jpg', 'herma': 'case_herma.jpg', 'pyeong': 'case_pyeongtaek.jpg', 'blai': 'case_bleibach.jpg', 'lincoln': 'lincoln.jpg', 'pnp': 'parknplay.jpg', 'ballet': 'balletvalet.jpg'}
def build_pages(deck, which):
    amap = json.load(open(D + 'decks/assets.json'))[which]
    inv = {v: KEY2FILE[k] for k, v in amap.items()}
    sdir = D + f'decks/{deck}/project/slides/'
    outdir = D + f'decks/{deck}/preview/'; os.makedirs(outdir, exist_ok=True)
    order = json.load(open(D + f'decks/{deck}/project/deck.json'))['order']
    css = '''<style>*{margin:0;box-sizing:border-box} body{background:#888} section{position:relative;width:1920px;height:1080px;overflow:hidden} ul,ol{padding-left:40px}
table{border-collapse:collapse;width:100%} td,th{padding:0.35em 0.6em;border:1px solid #c9c9c9;vertical-align:middle} th{font-weight:700}
@font-face{font-family:'Pretendard';src:url(file:///tmp/claude-0/-home-user-cloud/76ed2005-4113-58c6-b90f-f280afa8844d/scratchpad/decks/fonts/Pretendard-Regular.woff2)}
@font-face{font-family:'Pretendard Bold';src:url(file:///tmp/claude-0/-home-user-cloud/76ed2005-4113-58c6-b90f-f280afa8844d/scratchpad/decks/fonts/Pretendard-Bold.woff2)}
@font-face{font-family:'Pretendard ExtraBold';src:url(file:///tmp/claude-0/-home-user-cloud/76ed2005-4113-58c6-b90f-f280afa8844d/scratchpad/decks/fonts/Pretendard-ExtraBold.woff2)}</style>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@900&display=swap">'''
    pages = []
    for sid in order:
        h = open(sdir + sid + '.html').read()
        h = re.sub(r'/_blob/([0-9a-f]{32})', lambda m: 'file://' + A + inv[m.group(1)], h)
        h = re.sub(r'<aside>.*?</aside>', '', h, flags=re.S)
        p = outdir + sid + '.html'; open(p, 'w').write('<html><head><meta charset="utf-8">' + css + '</head><body>' + h + '</body></html>'); pages.append(p)
    return pages, outdir, order
if __name__ == '__main__':
    deck, which = sys.argv[1], sys.argv[2]; only = sys.argv[3].split(',') if len(sys.argv) > 3 else None
    pages, outdir, order = build_pages(deck, which)
    js = '''import { chromium } from '/opt/node-tools/node_modules/playwright/index.mjs';
const [,, outdir, ...pages] = process.argv;
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
for (const f of pages) { await p.goto('file://' + f); await p.waitForTimeout(700); await p.evaluate(() => document.fonts.ready);
  const r = await p.evaluate(() => { const s = document.querySelector('section'); const bad = []; const sr = s.getBoundingClientRect();
    s.querySelectorAll('*').forEach(e => { const r = e.getBoundingClientRect(); if (r.width && (r.bottom > 1081 || r.right > 1921)) bad.push((e.tagName + ':' + (e.textContent || '').slice(0, 24)).replace(/\\s+/g, ' ') + ' b=' + Math.round(r.bottom) + ' r=' + Math.round(r.right)); });
    return bad.slice(0, 4); });
  await p.screenshot({ path: f.replace('.html', '.png') }); console.log(f.split('/').pop(), r.length ? 'OVERFLOW ' + r.join(' | ') : 'ok'); }
await b.close();'''
    open(D + 'decks/shot_prev.mjs', 'w').write(js)
    sel = [pg for pg, sid in zip(pages, order) if (not only or sid in only)]
    subprocess.run(['node', D + 'decks/shot_prev.mjs', outdir] + sel)
