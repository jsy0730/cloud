import { chromium } from '/opt/node-tools/node_modules/playwright/index.mjs';
import fs from 'fs';
const ctx = JSON.parse(fs.readFileSync('context.json')); const js = fs.readFileSync('scene.js', 'utf8');
const browser = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
for (let i = 1; i <= 5; i++) {
  const des = JSON.parse(fs.readFileSync(`step${i}.json`));
  const view = { w: 760, h: 820, fov: 27, eye: [-200, -150, 175], target: [21, 60, 9], diagram: true, sunAz: 215, sunEl: 50 };
  const page = await browser.newPage({ viewport: { width: view.w, height: view.h } });
  page.on('pageerror', e => console.log('err:', e.message)); page.on('console', m => console.log('console:', m.text()));
  await page.setContent(`<html><body style="margin:0"><script type="importmap">{"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js","three/addons/":"https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"}}</script><script>window.DATA=${JSON.stringify({ ctx, des, view })};</script><script type="module">${js}</script></body></html>`);
  await page.waitForFunction(() => window.DONE === true, null, { timeout: 180000 });
  await page.locator('canvas').screenshot({ path: `out/step${i}.png` }); await page.close(); console.log('step', i);
}
await browser.close();
