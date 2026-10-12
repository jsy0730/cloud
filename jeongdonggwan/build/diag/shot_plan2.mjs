import { chromium } from '/opt/node-tools/node_modules/playwright/index.mjs';
const D='/tmp/claude-0/-home-user-cloud/76ed2005-4113-58c6-b90f-f280afa8844d/scratchpad/build/diag/';
const b=await chromium.launch(); const p=await b.newPage({viewport:{width:660,height:900},deviceScaleFactor:2});
await p.goto('file://'+D+'plan2.html'); await p.waitForTimeout(1500); await p.evaluate(()=>document.fonts.ready);
const h = await p.evaluate(()=>document.querySelector('svg').getBoundingClientRect().height);
await p.setViewportSize({width:660,height:Math.ceil(h)});
await p.screenshot({path:D+'plan2.png',clip:{x:0,y:0,width:660,height:Math.ceil(h)}}); await b.close(); console.log(h);
