// three.js scene: DATA = {ctx, des, view}
import * as THREE from 'three';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
const {ctx, des, view} = window.DATA;
const night = !!view.night; const diagram = !!view.diagram;
const renderer = new THREE.WebGLRenderer({antialias: true, preserveDrawingBuffer: true});
renderer.setPixelRatio(1); renderer.setSize(view.w, view.h);
renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = view.diagram ? THREE.NoToneMapping : THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = night ? 0.85 : 1.0;
document.body.appendChild(renderer.domElement);
const scene = new THREE.Scene();
{ const pm = new THREE.PMREMGenerator(renderer); scene.environment = pm.fromScene(new RoomEnvironment(renderer), 0.04).texture; scene.environmentIntensity = night ? 0.15 : (diagram ? 0.15 : 0.6); }
// sky gradient
const sky = document.createElement('canvas'); sky.width = 4; sky.height = 512;
{ const g = sky.getContext('2d'); const gr = g.createLinearGradient(0, 0, 0, 512);
  if (night) { gr.addColorStop(0, '#0b1630'); gr.addColorStop(0.55, '#33456e'); gr.addColorStop(1, '#c98a62'); }
  else { gr.addColorStop(0, '#7fa6cf'); gr.addColorStop(0.6, '#c9dbea'); gr.addColorStop(1, '#eef2f4'); }
  g.fillStyle = gr; g.fillRect(0, 0, 4, 512); }
const skyTex = new THREE.CanvasTexture(sky); skyTex.colorSpace = THREE.SRGBColorSpace; scene.background = diagram ? new THREE.Color(0xffffff) : skyTex;
if (!diagram) scene.fog = new THREE.Fog(night ? 0x26324f : 0xdfe7ee, 350, 1100);
// map: local (x east, y north, z up) -> three (x, y=up, z=-north)
const V = (x, y, z) => new THREE.Vector3(x, z, -y);
// lights
const hemi = new THREE.HemisphereLight(night ? 0x7080b0 : 0xdfeaf5, night ? 0x3a3530 : 0x8a8270, night ? 0.6 : 1.0); scene.add(hemi);
const sun = new THREE.DirectionalLight(night ? 0xffb58a : 0xfff1dc, night ? 0.25 : 2.6);
const az = (view.sunAz ?? 235) * Math.PI / 180, el = (view.sunEl ?? 38) * Math.PI / 180;
const c0 = ctx.center;
sun.position.copy(V(c0[0] + Math.sin(az) * Math.cos(el) * 400, c0[1] + Math.cos(az) * Math.cos(el) * 400, Math.sin(el) * 400));
sun.target.position.copy(V(c0[0], c0[1], 0)); scene.add(sun.target);
sun.castShadow = true; sun.shadow.mapSize.set(4096, 4096);
const sc = sun.shadow.camera; sc.left = -260; sc.right = 260; sc.top = 260; sc.bottom = -260; sc.near = 10; sc.far = 1200;
sun.shadow.bias = -0.0004; sun.shadow.normalBias = 0.6; scene.add(sun);
// textures
function canvasTex(wpx, hpx, draw, repW, repH) {
  const c = document.createElement('canvas'); c.width = wpx; c.height = hpx; draw(c.getContext('2d'), wpx, hpx);
  const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.colorSpace = THREE.SRGBColorSpace;
  t.anisotropy = 8; t.userData = {repW, repH}; return t;
}
function rnd(i) { const x = Math.sin(i * 127.1) * 43758.5453; return x - Math.floor(x); }
const TEX = {
  // 전돌 스크린 over dark parking interior: 3.0m x 2.95m tile
  screen: canvasTex(600, 590, (g, w, h) => {
    g.fillStyle = night ? '#7a5a34' : '#2a2c2f'; g.fillRect(0, 0, w, h);
    if (!night) { g.fillStyle = '#3a3d40'; g.fillRect(0, h * 0.55, w, h * 0.45); }
    const n = 24; for (let i = 0; i < n; i++) {
      const x = i * w / n; const bw = w / n * (0.62 + 0.12 * rnd(i));
      for (let j = 0; j < 30; j++) { const y = j * h / 30; const off = (j % 2) * 3;
        const s = 0.85 + 0.25 * rnd(i * 31 + j);
        g.fillStyle = night ? `rgb(${Math.round(70 * s)},${Math.round(52 * s)},${Math.round(40 * s)})` : `rgb(${Math.round(176 * s)},${Math.round(140 * s)},${Math.round(112 * s)})`;
        g.fillRect(x + off, y + 1, bw, h / 30 - 2); }
    }
  }, 3.0, 2.95),
  green: canvasTex(600, 590, (g, w, h) => {
    g.fillStyle = '#2f3a2a'; g.fillRect(0, 0, w, h);
    for (let i = 0; i < 1400; i++) { const x = rnd(i) * w, y = rnd(i + 999) * h, r = 4 + 10 * rnd(i + 77);
      const s = 0.6 + 0.6 * rnd(i + 5); g.fillStyle = `rgb(${Math.round(70 * s)},${Math.round(112 * s)},${Math.round(58 * s)})`;
      g.beginPath(); g.arc(x, y, r, 0, 7); g.fill(); }
    g.fillStyle = '#9b9a95'; for (let i = 0; i < 6; i++) g.fillRect(i * w / 6, 0, 3, h);
  }, 3.0, 2.95),
  glass: canvasTex(600, 1400, (g, w, h) => {
    const gr = g.createLinearGradient(0, 0, 0, h);
    if (night) { gr.addColorStop(0, '#ffd59a'); gr.addColorStop(1, '#f3b066'); }
    else { gr.addColorStop(0, '#8fa5b4'); gr.addColorStop(0.5, '#56677a'); gr.addColorStop(1, '#3b4552'); }
    g.fillStyle = gr; g.fillRect(0, 0, w, h);
    if (!night) { for (let i = 0; i < 5; i++) { g.fillStyle = `rgba(255,214,160,${0.18 + 0.2 * rnd(i)})`; g.fillRect(rnd(i + 3) * w * 0.7, h * 0.62, w * 0.25, h * 0.36); } }
    g.fillStyle = '#26292c'; g.fillRect(0, 0, 6, h); g.fillRect(w / 2 - 3, 0, 5, h); g.fillRect(0, h * 0.36, w, 8);
  }, 3.0, 7.0),
  hall: canvasTex(400, 760, (g, w, h) => {
    // channel glass upper, clear glass band (2.4m) at the bottom
    g.fillStyle = night ? '#fff1d6' : '#dfe3e2'; g.fillRect(0, 0, w, h);
    for (let i = 0; i < 16; i++) { g.fillStyle = night ? 'rgba(190,140,80,0.45)' : 'rgba(120,128,130,0.55)'; g.fillRect(i * w / 16, 0, 3, h * 0.68); }
    const gb = g.createLinearGradient(0, h * 0.68, 0, h);
    if (night) { gb.addColorStop(0, '#ffcf8a'); gb.addColorStop(1, '#f0a85a'); } else { gb.addColorStop(0, '#6f8291'); gb.addColorStop(1, '#3d4a56'); }
    g.fillStyle = gb; g.fillRect(0, h * 0.68, w, h * 0.32);
    g.fillStyle = '#2b2e31'; g.fillRect(0, h * 0.675, w, 8); g.fillRect(0, 0, w, 6); g.fillRect(0, 0, 5, h); g.fillRect(w / 2, h * 0.68, 4, h * 0.32);
  }, 2.0, 7.6),
  fin: canvasTex(600, 760, (g, w, h) => {
    const gr = g.createLinearGradient(0, 0, 0, h);
    if (night) { gr.addColorStop(0, '#ffe0b0'); gr.addColorStop(1, '#ffb768'); } else { gr.addColorStop(0, '#9fb3c2'); gr.addColorStop(0.55, '#6c8194'); gr.addColorStop(1, '#4a5a69'); }
    g.fillStyle = gr; g.fillRect(0, 0, w, h);
    if (!night) { for (let i = 0; i < 4; i++) { g.fillStyle = `rgba(255,236,200,${0.10 + 0.12 * rnd(i + 40)})`; g.fillRect(rnd(i + 9) * w * 0.8, h * 0.55, w * 0.18, h * 0.42); } }
    for (let i = 0; i < 12; i++) { const x = i * w / 12; g.fillStyle = night ? '#6b4a2e' : '#d8d4cc'; g.fillRect(x, 0, w / 12 * 0.32, h); g.fillStyle = 'rgba(0,0,0,0.25)'; g.fillRect(x + w / 12 * 0.32, 0, 4, h); }
    g.fillStyle = night ? '#4a3220' : '#e9e6df'; g.fillRect(0, 0, w, 10); g.fillRect(0, h * 0.52, w, 6);
  }, 3.0, 7.6),
  deck: canvasTex(512, 512, (g, w, h) => {
    g.fillStyle = '#a58d6f'; g.fillRect(0, 0, w, h);
    for (let i = 0; i < 32; i++) { g.fillStyle = `rgba(80,60,40,${0.15 + 0.15 * rnd(i)})`; g.fillRect(0, i * h / 32, w, 2); }
  }, 4, 4),
};
const M = {
  screen: new THREE.MeshStandardMaterial({map: TEX.screen, roughness: 0.85, emissive: night ? 0xffffff : 0x000000, emissiveMap: night ? TEX.screen : null, emissiveIntensity: night ? 0.22 : 0}),
  base: null,
  green: new THREE.MeshStandardMaterial({map: TEX.green, roughness: 0.95}),
  glass: new THREE.MeshStandardMaterial({map: TEX.glass, roughness: 0.25, metalness: 0.2, emissive: night ? 0xffffff : 0x000000, emissiveMap: night ? TEX.glass : null, emissiveIntensity: night ? 0.9 : 0}),
  hall: new THREE.MeshStandardMaterial({map: TEX.hall, roughness: 0.6, emissive: night ? 0xffffff : 0x000000, emissiveMap: night ? TEX.hall : null, emissiveIntensity: night ? 1.1 : 0}),
  slab: new THREE.MeshStandardMaterial({color: 0xe4e2dc, roughness: 0.8}),
  fin: new THREE.MeshStandardMaterial({map: TEX.fin, roughness: 0.3, metalness: 0.15, emissive: night ? 0xffffff : 0x000000, emissiveMap: night ? TEX.fin : null, emissiveIntensity: night ? 1.0 : 0}),
  roof: new THREE.MeshStandardMaterial({color: 0xcfcdc6, roughness: 0.9}),
  solar: null,
  roofdeck: new THREE.MeshStandardMaterial({map: TEX.deck, roughness: 0.9}),
  ctx: new THREE.MeshStandardMaterial({color: night ? 0x3b3f48 : 0xe9e8e4, roughness: 0.95}),
  ctxwin: new THREE.MeshStandardMaterial({color: 0x3b3f48, roughness: 0.9}),
  ground: new THREE.MeshStandardMaterial({color: night ? 0x2a2c30 : 0xcfcfc9, roughness: 1}),
  road: new THREE.MeshStandardMaterial({color: night ? 0x1d1f23 : 0x7d8083, roughness: 1}),
  lane: new THREE.MeshStandardMaterial({color: night ? 0x3a3c40 : 0x9a8f84, roughness: 1}),
  tree: new THREE.MeshStandardMaterial({color: 0x5f7f4c, roughness: 1}),
  trunk: new THREE.MeshStandardMaterial({color: 0x5a4a3a, roughness: 1}),
  car: [0xf2f2f2, 0x30343a, 0x8e969c, 0xa33a2f, 0x2c4c78].map(c => new THREE.MeshStandardMaterial({color: c, roughness: 0.4, metalness: 0.3})),
};
M.base = M.screen;
const DC = {dW: 0xf6e58d, dE: 0xf2c79a, dlane: 0x8f8f8f, dsite: 0xe6e2da, dpark: 0xd7b28c, dpark2: 0xc49a72, dcult: 0x8fb8e0, doff: 0xcdb8e6, dcore: 0xd2432a, droof: 0x9ccc7c};
for (const kk in DC) M[kk] = new THREE.MeshStandardMaterial({color: DC[kk], roughness: 0.85});
const solarTex = canvasTex(256, 256, (g, w, h) => { g.fillStyle = '#9aa3a8'; g.fillRect(0, 0, w, h); for (let i = 0; i < 4; i++) for (let j = 0; j < 2; j++) { g.fillStyle = '#1f2f45'; g.fillRect(i * 64 + 4, j * 128 + 6, 56, 116); g.fillStyle = 'rgba(160,190,220,0.25)'; g.fillRect(i * 64 + 4, j * 128 + 6, 56, 20); } }, 4, 4);
const solarM = new THREE.MeshStandardMaterial({map: solarTex, roughness: 0.35, metalness: 0.3});
// prism builder with metric UVs on walls
function prism(pts, z0, h, mat, opts = {}) {
  const pos = [], uv = [], idx = [];
  let ccw = 0; for (let i = 0; i < pts.length; i++) { const a = pts[i], b = pts[(i + 1) % pts.length]; ccw += (b[0] - a[0]) * (b[1] + a[1]); }
  const isCCW = ccw < 0; const group = new THREE.Group();
  const texM = mat.map ? mat.map.userData : {repW: 1, repH: 1};
  const wallsBy = {};
  let s = 0;
  for (let i = 0; i < pts.length; i++) {
    const a = pts[i], b = pts[(i + 1) % pts.length]; const L = Math.hypot(b[0] - a[0], b[1] - a[1]); if (L < 0.05) continue;
    let nx = (b[1] - a[1]) / L, ny = -(b[0] - a[0]) / L; if (!isCCW) { nx = -nx; ny = -ny; }
    let m = mat; if (opts.eastGreen && nx > 0.75) m = M.green;
    const key = m.uuid; (wallsBy[key] = wallsBy[key] || {m, pos: [], uv: [], idx: []});
    const W = wallsBy[key]; const base = W.pos.length / 3;
    const rw = (m.map ? m.map.userData.repW : 1), rh = (m.map ? m.map.userData.repH : 1);
    const quad = [[a, z0], [b, z0], [b, z0 + h], [a, z0 + h]];
    const us = [s / rw, (s + L) / rw];
    quad.forEach(([p, z], k) => { const v = V(p[0], p[1], z); W.pos.push(v.x, v.y, v.z); W.uv.push(k == 0 || k == 3 ? us[0] : us[1], (z - z0) / rh); });
    if (isCCW) W.idx.push(base, base + 1, base + 2, base, base + 2, base + 3); else W.idx.push(base, base + 2, base + 1, base, base + 3, base + 2);
    s += L;
  }
  for (const k in wallsBy) { const W = wallsBy[k]; const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.Float32BufferAttribute(W.pos, 3)); g.setAttribute('uv', new THREE.Float32BufferAttribute(W.uv, 2));
    g.setIndex(W.idx); g.computeVertexNormals(); const mesh = new THREE.Mesh(g, W.m); mesh.castShadow = mesh.receiveShadow = true;
    mesh.material.side = THREE.DoubleSide; group.add(mesh); }
  // caps
  const shape = new THREE.Shape(pts.map(p => new THREE.Vector2(p[0], p[1])));
  const capMat = opts.capMat || (mat === M.roofdeck ? M.roofdeck : M.slab);
  for (const [z, flip] of [[z0 + h, false], [z0, true]]) {
    const g = new THREE.ShapeGeometry(shape); g.rotateX(-Math.PI / 2); g.translate(0, z, 0);
    if (mat === M.roofdeck) { const uvA = g.attributes.uv; for (let i = 0; i < uvA.count; i++) uvA.setXY(i, uvA.getX(i) / 4, uvA.getY(i) / 4); }
    const mesh = new THREE.Mesh(g, flip ? M.slab : capMat); mesh.material.side = THREE.DoubleSide; mesh.castShadow = true; mesh.receiveShadow = true; group.add(mesh);
  }
  scene.add(group); return group;
}
// ground
const gnd = new THREE.Mesh(new THREE.PlaneGeometry(3000, 3000), M.ground); gnd.rotation.x = -Math.PI / 2; gnd.position.set(c0[0], -0.05, -c0[1]); gnd.receiveShadow = true; scene.add(gnd);
// roads as flat ribbons
for (const r of (diagram ? [] : ctx.roads)) {
  for (let i = 0; i < r.pts.length - 1; i++) {
    const a = r.pts[i], b = r.pts[i + 1]; const L = Math.hypot(b[0] - a[0], b[1] - a[1]); if (L < 0.1) continue;
    const g = new THREE.PlaneGeometry(L + r.w * 0.5, r.w); g.rotateX(-Math.PI / 2);
    const m = new THREE.Mesh(g, M.road); m.position.copy(V((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, 0.01 + (r.w / 1000)));
    m.rotation.y = Math.atan2(b[1] - a[1], b[0] - a[0]); m.receiveShadow = true; scene.add(m);
  }
}
// lane (소로) under the building
for (const p of (des.lane || [])) { const g = new THREE.ShapeGeometry(new THREE.Shape(p.map(q => new THREE.Vector2(q[0], q[1])))); g.rotateX(-Math.PI / 2); g.translate(0, 0.05, 0); const m = new THREE.Mesh(g, M.lane); m.receiveShadow = true; scene.add(m); }
// context buildings
if (!diagram) for (const b of ctx.buildings) prism(b.pts, 0, b.h, M.ctx, {capMat: M.ctx});
// design
for (const p of des.parts) { const gg = prism(p.pts, p.z0, p.h, M[p.mat], {eastGreen: !diagram && (p.mat === 'screen' || p.mat === 'base'), capMat: diagram ? M[p.mat] : undefined});
  if (diagram) gg.children.forEach(ch => { const e = new THREE.LineSegments(new THREE.EdgesGeometry(ch.geometry, 30), new THREE.LineBasicMaterial({color: 0x333333})); ch.add(e); }); }
// roof trees + street trees + cars
function tree(x, y, z, s = 1) { const t = new THREE.Mesh(new THREE.CylinderGeometry(0.15 * s, 0.2 * s, 2.5 * s), M.trunk); t.position.copy(V(x, y, z + 1.25 * s)); t.castShadow = true; scene.add(t);
  const c = new THREE.Mesh(new THREE.SphereGeometry(1.9 * s, 12, 10), M.tree); c.position.copy(V(x, y, z + 3.4 * s)); c.scale.set(1, 0.85, 1); c.castShadow = true; scene.add(c); }
(des.trees || []).forEach(t => tree(t[0], t[1], t[2], t[3] || 1));
(des.cars || []).forEach((c, i) => { const m = new THREE.Mesh(new THREE.BoxGeometry(4.5, 0.95, 1.85), M.car[i % 5]); m.position.copy(V(c[0], c[1], 0.75)); m.rotation.y = c[2] || 0; m.castShadow = true; scene.add(m); const cb = new THREE.Mesh(new THREE.BoxGeometry(2.4, 0.7, 1.7), M.car[1]); cb.position.copy(m.position); cb.position.y += 1.0; cb.rotation.y = m.rotation.y; scene.add(cb); });
const stairM = new THREE.MeshStandardMaterial({color: 0xd2432a, roughness: 0.5, metalness: 0.25, emissive: night ? 0x801a0a : 0x000000, emissiveIntensity: night ? 0.6 : 0});
const railM = new THREE.MeshPhysicalMaterial({color: 0xdfe7ea, roughness: 0.05, transparent: true, opacity: 0.35});
const postM = new THREE.MeshStandardMaterial({color: 0x2b2f33, roughness: 0.6, metalness: 0.4});
(des.posts || []).forEach(p => { const m = new THREE.Mesh(new THREE.BoxGeometry(0.3, p[2], 0.3), postM); m.position.copy(V(p[0], p[1], p[2] / 2)); m.castShadow = true; scene.add(m); });
(des.beams || []).forEach(b => { const [x1, y1, x2, y2, z] = b; const L = Math.hypot(x2 - x1, y2 - y1); const m = new THREE.Mesh(new THREE.BoxGeometry(L, 0.35, 0.25), postM); m.position.copy(V((x1 + x2) / 2, (y1 + y2) / 2, z)); m.rotation.y = Math.atan2(y2 - y1, x2 - x1); scene.add(m); });
(des.parapets || []).forEach(b => { const [x1, y1, x2, y2, z] = b; const L = Math.hypot(x2 - x1, y2 - y1); const m = new THREE.Mesh(new THREE.BoxGeometry(L, 1.2, 0.05), railM); m.position.copy(V((x1 + x2) / 2, (y1 + y2) / 2, z + 0.6)); m.rotation.y = Math.atan2(y2 - y1, x2 - x1); scene.add(m); });
(des.solar || []).forEach(p => { const g = new THREE.ShapeGeometry(new THREE.Shape(p.pts.map(q => new THREE.Vector2(q[0], q[1])))); g.rotateX(-Math.PI / 2); g.translate(0, p.z + 0.05, 0); scene.add(new THREE.Mesh(g, solarM)); });
(des.stairs || []).forEach(f => { const [x1, y1, z1, x2, y2, z2, wd] = f; const L = Math.hypot(x2 - x1, y2 - y1, z2 - z1);
  const g = new THREE.BoxGeometry(Math.hypot(x2 - x1, y2 - y1), 0.18, wd * 0.85); const m = new THREE.Mesh(g, stairM);
  m.position.copy(V((x1 + x2) / 2, (y1 + y2) / 2, (z1 + z2) / 2)); m.rotation.order = 'YZX'; m.rotation.y = Math.atan2(y2 - y1, x2 - x1);
  m.rotation.z = Math.atan2(z2 - z1, Math.hypot(x2 - x1, y2 - y1)); m.castShadow = true; scene.add(m);
  const r = new THREE.Mesh(new THREE.BoxGeometry(Math.hypot(x2 - x1, y2 - y1), 1.0, 0.04), railM); r.position.copy(m.position); r.position.y += 0.6; r.rotation.copy(m.rotation); r.translateZ(-wd / 2); scene.add(r); });
const shaftM = new THREE.MeshPhysicalMaterial({color: night ? 0xffd7a0 : 0xbfd3dc, roughness: 0.05, metalness: 0.1, transparent: true, opacity: 0.55, emissive: night ? 0xffc070 : 0x000000, emissiveIntensity: night ? 0.8 : 0});
(des.shafts || []).forEach(s => { const m = new THREE.Mesh(new THREE.BoxGeometry(2.8, s[2], 2.8), shaftM); m.position.copy(V(s[0], s[1], s[2] / 2)); scene.add(m);
  const fr = new THREE.Mesh(new THREE.BoxGeometry(3.0, 0.5, 3.0), stairM); fr.position.copy(V(s[0], s[1], s[2])); scene.add(fr); });
const pitM = new THREE.MeshStandardMaterial({color: night ? 0xffb760 : 0x2b2724, roughness: 1, emissive: night ? 0xff9a40 : 0x000000, emissiveIntensity: night ? 0.6 : 0});
(des.pit || []).forEach(p => { const g = new THREE.ShapeGeometry(new THREE.Shape(p.map(q => new THREE.Vector2(q[0], q[1])))); g.rotateX(-Math.PI / 2); g.translate(0, 0.06, 0); scene.add(new THREE.Mesh(g, pitM)); });
const tipFloor = new THREE.MeshStandardMaterial({color: night ? 0x50483f : 0xbdb6aa, roughness: 1});
(des.tips || []).forEach(p => { const g = new THREE.ShapeGeometry(new THREE.Shape(p.map(q => new THREE.Vector2(q[0], q[1])))); g.rotateX(-Math.PI / 2); g.translate(0, 0.03, 0); const m = new THREE.Mesh(g, tipFloor); m.receiveShadow = true; scene.add(m); });
const pplM = [0x2f3640, 0xc0392b, 0xe6e6e6, 0x34495e, 0xd35400, 0x7f8c8d].map(c => new THREE.MeshStandardMaterial({color: c, roughness: 0.8}));
(des.people || []).forEach((p, i) => { const m = new THREE.Mesh(new THREE.CapsuleGeometry(0.24, 1.15, 4, 8), pplM[i % pplM.length]); m.position.copy(V(p[0], p[1], (p[2] || 0) + 0.82)); m.castShadow = true; scene.add(m); });
if (diagram) gnd.material = new THREE.MeshStandardMaterial({color: 0xf4f3f0, roughness: 1});
if (night) { // light pools
  for (const p of (des.lights || [])) { const l = new THREE.PointLight(0xffc98a, p[3] || 400, 40, 1.6); l.position.copy(V(p[0], p[1], p[2])); scene.add(l); }
}
// camera
const cam = new THREE.PerspectiveCamera(view.fov || 45, view.w / view.h, 1, 4000);
cam.position.copy(V(...view.eye)); cam.lookAt(V(...view.target)); cam.updateProjectionMatrix();
renderer.render(scene, cam);
window.DONE = true;
