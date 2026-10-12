import { chromium } from '/opt/node-tools/node_modules/playwright/index.mjs';
import fs from 'fs';
const [,, viewsFile, outDir] = process.argv;
const ctx = JSON.parse(fs.readFileSync('context.json')); const des = JSON.parse(fs.readFileSync('design.json'));
const views = JSON.parse(fs.readFileSync(viewsFile));
const js = fs.readFileSync('scene.js', 'utf8');
const browser = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
for (const [name, view] of Object.entries(views)) {
  const page = await browser.newPage({ viewport: { width: view.w, height: view.h } });
  page.on('console', m => console.log('console:', m.text())); page.on('pageerror', e => console.log('err:', e.message));
  const html = `<html><body style="margin:0;background:#000"><script type="importmap">{"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js","three/addons/":"https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"}}</script>
<script>window.DATA=${JSON.stringify({ ctx, des, view })};</script><script type="module">${js}</script></body></html>`;
  await page.setContent(html);
  await page.waitForFunction(() => window.DONE === true, null, { timeout: 180000 });
  await page.locator('canvas').screenshot({ path: `${outDir}/${name}.png` });
  console.log('saved', name); await page.close();
}
await browser.close();
