import { chromium } from '/opt/node-tools/node_modules/playwright/index.mjs';
const [,, html, out, w, h] = process.argv;
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: +w, height: +h } });
await p.goto('file://' + html); await p.waitForTimeout(1500); await p.evaluate(() => document.fonts.ready);
await p.screenshot({ path: out }); await b.close();
