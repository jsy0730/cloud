// 정동관 realistic-ish scene (three.js r160). DATA = {ctx, des, view}
import * as THREE from 'three';
import { Sky } from 'three/addons/objects/Sky.js';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
import { SSAOPass } from 'three/addons/postprocessing/SSAOPass.js';
import { ShaderPass } from 'three/addons/postprocessing/ShaderPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';

const { ctx, des, view } = window.DATA;
const night = !!view.night;
const dusk = !!view.dusk;
const lit = night || dusk;
const PR = view.pr || 1.5;
const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
renderer.setPixelRatio(PR); renderer.setSize(view.w, view.h);
renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = night ? 0.8 : (dusk ? 0.9 : 0.62);
document.body.style.margin = '0'; document.body.appendChild(renderer.domElement);
const scene = new THREE.Scene();
const c0 = ctx.center;
const V = (x, y, z) => new THREE.Vector3(x, z, -y);
function rnd(i) { const x = Math.sin(i * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); }

// ---------- sky / environment ----------
const sunAz = (view.sunAz ?? 235) * Math.PI / 180, sunEl = (view.sunEl ?? 38) * Math.PI / 180;
const sunDir = V(Math.sin(sunAz) * Math.cos(sunEl), Math.cos(sunAz) * Math.cos(sunEl), Math.sin(sunEl)).normalize();
const pm = new THREE.PMREMGenerator(renderer);
if (!night) {
  const sky = new Sky(); sky.scale.setScalar(5000);
  const u = sky.material.uniforms;
  u.turbidity.value = dusk ? 6 : 3.2; u.rayleigh.value = dusk ? 2.2 : 1.1; u.mieCoefficient.value = 0.004; u.mieDirectionalG.value = 0.8;
  u.sunPosition.value.copy(sunDir);
  const envScene = new THREE.Scene(); envScene.add(sky);
  scene.environment = pm.fromScene(envScene, 0.02).texture; scene.environmentIntensity = dusk ? 0.55 : 0.9;
  scene.add(sky.clone());
} else {
  const cv = document.createElement('canvas'); cv.width = 4; cv.height = 512; const g = cv.getContext('2d'); const gr = g.createLinearGradient(0, 0, 0, 512);
  gr.addColorStop(0, '#060c1e'); gr.addColorStop(0.5, '#1c2c52'); gr.addColorStop(0.85, '#4a5a86'); gr.addColorStop(1, '#a98a78'); g.fillStyle = gr; g.fillRect(0, 0, 4, 512);
  const t = new THREE.CanvasTexture(cv); t.colorSpace = THREE.SRGBColorSpace; scene.background = t;
  const es = new THREE.Scene(); es.background = t; scene.environment = pm.fromScene(es, 0.02).texture; scene.environmentIntensity = 0.5;
}
scene.fog = new THREE.Fog(night ? 0x1b2745 : (dusk ? 0xc9b3a8 : 0xcfd9e2), 260, 1300);
const hemi = new THREE.HemisphereLight(night ? 0x5a6a9a : 0xcfe0f2, night ? 0x2a2622 : 0x7a7466, night ? 0.35 : 0.5); scene.add(hemi);
const sun = new THREE.DirectionalLight(night ? 0x8fa2d8 : (dusk ? 0xffb27a : 0xfff0d8), night ? 0.25 : (dusk ? 2.0 : 3.0));
sun.position.copy(sunDir.clone().multiplyScalar(450).add(V(c0[0], c0[1], 0)));
sun.target.position.copy(V(c0[0], c0[1], 0)); scene.add(sun.target);
sun.castShadow = true; sun.shadow.mapSize.set(4096, 4096);
const sc = sun.shadow.camera; sc.left = -230; sc.right = 230; sc.top = 230; sc.bottom = -230; sc.near = 20; sc.far = 1300;
sun.shadow.bias = -0.0003; sun.shadow.normalBias = 0.5; sun.shadow.radius = 3; scene.add(sun);

// ---------- procedural textures ----------
function ctex(w, h, draw, rw, rh, opts = {}) {
  const c = document.createElement('canvas'); c.width = w; c.height = h; draw(c.getContext('2d'), w, h);
  const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.anisotropy = 8;
  if (!opts.linear) t.colorSpace = THREE.SRGBColorSpace; t.userData = { rw, rh }; return t;
}
// perforated terracotta brick screen: 3.0m x 2.95m module. returns [color, alpha, bump]
const SW = 1024, SH = 1008;
function brickPattern(g, w, h, mode) {
  // mode: 'color' | 'alpha' | 'bump'
  const cols = 30, rows = 28, cw = w / cols, rh = h / rows;
  if (mode === 'alpha') { g.fillStyle = '#000'; g.fillRect(0, 0, w, h); }
  else if (mode === 'bump') { g.fillStyle = '#000'; g.fillRect(0, 0, w, h); }
  else { g.fillStyle = '#3a2e27'; g.fillRect(0, 0, w, h); }
  for (let j = 0; j < rows; j++) for (let i = 0; i < cols; i++) {
    const off = (j % 2) * cw * 0.5, x = i * cw + off, y = j * rh;
    const r = rnd(i * 37 + j * 91);
    // open pattern: every brick is solid, but alternating perforation every 3rd pair
    const hole = ((i + (j % 2) * 2) % 3 === 0) && (j % 4 !== 3);
    if (mode === 'alpha') { g.fillStyle = hole ? '#000' : '#fff'; g.fillRect(x + 1, y + 1, cw - 2, rh - 2); g.fillRect(x - w + 1, y + 1, cw - 2, rh - 2); }
    else if (mode === 'bump') { if (!hole) { g.fillStyle = `rgb(${200 + 40 * r | 0},${200 + 40 * r | 0},${200 + 40 * r | 0})`; g.fillRect(x + 1.5, y + 1.5, cw - 3, rh - 3); g.fillRect(x - w + 1.5, y + 1.5, cw - 3, rh - 3); } }
    else {
      if (hole) continue;
      const k = 0.78 + 0.34 * r, tint = rnd(i * 13 + j * 7);
      g.fillStyle = `rgb(${Math.round((150 + 22 * tint) * k)},${Math.round((100 + 16 * tint) * k)},${Math.round((78 + 12 * tint) * k)})`;
      g.fillRect(x + 1, y + 1, cw - 2, rh - 2); g.fillRect(x - w + 1, y + 1, cw - 2, rh - 2);
      g.fillStyle = 'rgba(255,230,200,0.10)'; g.fillRect(x + 1, y + 1, cw - 2, 2);
    }
  }
}
const TX = {};
TX.screen = ctex(SW, SH, (g, w, h) => brickPattern(g, w, h, 'color'), 3.0, 2.95);
TX.screenA = ctex(SW, SH, (g, w, h) => brickPattern(g, w, h, 'alpha'), 3.0, 2.95, { linear: true });
TX.screenB = ctex(SW, SH, (g, w, h) => brickPattern(g, w, h, 'bump'), 3.0, 2.95, { linear: true });
TX.inner = ctex(512, 512, (g, w, h) => {
  g.fillStyle = '#26262a'; g.fillRect(0, 0, w, h);
  for (let i = 0; i < 4; i++) { g.fillStyle = 'rgba(255,255,255,0.05)'; g.fillRect(i * 128, 0, 3, h); }
  g.fillStyle = night ? '#ffd9a0' : '#4a4a4e'; g.fillRect(40, 14, 120, 10); g.fillRect(300, 14, 120, 10);
  g.fillStyle = night ? '#ffd9a0' : '#56565a'; g.fillRect(0, h * 0.5, w, 3);
}, 4.0, 3.3);
TX.green = ctex(512, 512, (g, w, h) => {
  g.fillStyle = '#2c3a28'; g.fillRect(0, 0, w, h);
  for (let i = 0; i < 2200; i++) { const x = rnd(i) * w, y = rnd(i + 999) * h, r = 3 + 9 * rnd(i + 77), s = 0.55 + 0.7 * rnd(i + 5);
    g.fillStyle = `rgb(${Math.round(70 * s)},${Math.round(118 * s)},${Math.round(56 * s)})`; g.beginPath(); g.arc(x, y, r, 0, 7); g.fill(); }
}, 3.0, 2.95);
TX.glass = ctex(512, 1024, (g, w, h) => {
  const gr = g.createLinearGradient(0, 0, 0, h);
  if (night) { gr.addColorStop(0, '#ffd9a6'); gr.addColorStop(0.5, '#ffc582'); gr.addColorStop(1, '#f1a85c'); } else { gr.addColorStop(0, '#34485a'); gr.addColorStop(0.55, '#4a5d6c'); gr.addColorStop(1, '#6e6250'); }
  g.fillStyle = gr; g.fillRect(0, 0, w, h);
  // interior: ceiling light rows + shelves silhouettes (soft)
  for (let i = 0; i < 3; i++) { g.fillStyle = night ? 'rgba(255,248,225,0.8)' : 'rgba(255,240,205,0.55)'; g.fillRect(40 + i * 150, h * 0.46, 90, 8); }
  for (let i = 0; i < 5; i++) { const x = rnd(i + 3) * w * 0.85, yy = h * 0.58 + rnd(i + 9) * h * 0.1; const gg = g.createLinearGradient(0, yy, 0, yy + h * 0.3); gg.addColorStop(0, night ? 'rgba(120,70,30,0.0)' : 'rgba(255,225,170,0.0)'); gg.addColorStop(1, night ? 'rgba(120,70,30,0.35)' : 'rgba(255,225,170,0.22)'); g.fillStyle = gg; g.fillRect(x, yy, w * 0.14, h * 0.3); }
  g.fillStyle = '#1d2024'; g.fillRect(0, 0, 8, h); g.fillRect(w / 2 - 3, 0, 6, h); g.fillRect(0, h * 0.42, w, 8); g.fillRect(0, h - 9, w, 9);
}, 3.0, 7.0);
TX.fin = ctex(512, 640, (g, w, h) => {
  const gr = g.createLinearGradient(0, 0, 0, h);
  if (night) { gr.addColorStop(0, '#ffe3b8'); gr.addColorStop(1, '#ffb468'); } else { gr.addColorStop(0, '#a9bccb'); gr.addColorStop(0.6, '#7d92a3'); gr.addColorStop(1, '#5d7082'); }
  g.fillStyle = gr; g.fillRect(0, 0, w, h);
  for (let i = 0; i < 16; i++) { const x = i * w / 16; g.fillStyle = night ? 'rgba(110,70,35,0.5)' : 'rgba(235,240,245,0.55)'; g.fillRect(x, 0, w / 16 * 0.3, h); g.fillStyle = 'rgba(0,0,0,0.22)'; g.fillRect(x + w / 16 * 0.3, 0, 3, h); }
  g.fillStyle = night ? '#6a4a2e' : '#e8e8e4'; g.fillRect(0, 0, w, 8); g.fillRect(0, h * 0.55, w, 5);
}, 3.0, 7.6);
TX.deck = ctex(512, 512, (g, w, h) => {
  g.fillStyle = '#a3896a'; g.fillRect(0, 0, w, h);
  for (let i = 0; i < 24; i++) { g.fillStyle = `rgba(70,50,30,${0.12 + 0.18 * rnd(i)})`; g.fillRect(0, i * h / 24, w, 2); for (let j = 0; j < 8; j++) { g.fillStyle = 'rgba(0,0,0,0.12)'; g.fillRect((j * 64 + rnd(i * 9 + j) * 60) | 0, i * h / 24, 2, h / 24); } }
}, 4, 4);
TX.asphalt = ctex(512, 512, (g, w, h) => {
  g.fillStyle = '#7c7e82'; g.fillRect(0, 0, w, h);
  for (let i = 0; i < 9000; i++) { const s = rnd(i) * 255 | 0; g.fillStyle = `rgba(${s},${s},${s},0.07)`; g.fillRect(rnd(i + 5) * w, rnd(i + 17) * h, 2, 2); }
  for (let i = 0; i < 14; i++) { g.strokeStyle = 'rgba(20,20,22,0.18)'; g.lineWidth = 1.5; g.beginPath(); g.moveTo(rnd(i) * w, rnd(i + 2) * h); g.lineTo(rnd(i + 4) * w, rnd(i + 6) * h); g.stroke(); }
}, 6, 6);
TX.paving = ctex(512, 512, (g, w, h) => {
  g.fillStyle = '#b9b3a8'; g.fillRect(0, 0, w, h);
  for (let j = 0; j < 8; j++) for (let i = 0; i < 8; i++) { const k = 0.9 + 0.2 * rnd(i * 8 + j); g.fillStyle = `rgb(${185 * k | 0},${178 * k | 0},${166 * k | 0})`; g.fillRect(i * 64 + 2, j * 64 + 2, 60, 60); }
}, 4, 4);
const ctxWalls = [0xe6e2d8, 0xd8d4ca, 0xc9ccd0, 0xe2d9c8, 0xd2cec4, 0xb9b4a8].map((c, k) => {
  const wc = '#' + c.toString(16).padStart(6, '0');
  return ctex(256, 256, (g, w, h) => {
    g.fillStyle = wc; g.fillRect(0, 0, w, h);
    for (let i = 0; i < 3; i++) { g.fillStyle = night ? (rnd(i + k * 5) > 0.45 ? '#ffd7a0' : '#2d3340') : '#3b4552'; g.fillRect(i * 85 + 14, 40, 56, 128);
      if (!night) { g.fillStyle = 'rgba(190,210,225,0.35)'; g.fillRect(i * 85 + 14, 40, 56, 40); } }
    g.fillStyle = 'rgba(0,0,0,0.10)'; g.fillRect(0, h - 10, w, 10);
  }, 4.0, 3.3);
});

// ---------- materials ----------
const MT = {};
MT.screen = new THREE.MeshStandardMaterial({ map: TX.screen, alphaMap: TX.screenA, bumpMap: TX.screenB, bumpScale: 1.6, alphaTest: 0.5, roughness: 0.85, side: THREE.DoubleSide,
  emissive: night ? 0x331c0c : 0x000000, emissiveMap: night ? TX.screen : null, emissiveIntensity: night ? 0.35 : 0 });
MT.inner = new THREE.MeshStandardMaterial({ map: TX.inner, roughness: 1, emissive: night ? 0xffffff : 0x000000, emissiveMap: night ? TX.inner : null, emissiveIntensity: night ? 0.9 : 0 });
MT.green = new THREE.MeshStandardMaterial({ map: TX.green, roughness: 0.95 });
MT.glass = new THREE.MeshPhysicalMaterial({ map: TX.glass, roughness: 0.09, metalness: 0.45, envMapIntensity: 0.75, clearcoat: 0.5,
  emissive: night ? 0xffffff : 0x000000, emissiveMap: night ? TX.glass : null, emissiveIntensity: night ? 0.85 : 0 });
MT.fin = new THREE.MeshPhysicalMaterial({ map: TX.fin, roughness: 0.18, metalness: 0.35, envMapIntensity: 1.2,
  emissive: night ? 0xffffff : 0x000000, emissiveMap: night ? TX.fin : null, emissiveIntensity: night ? 1.0 : 0 });
MT.slab = new THREE.MeshStandardMaterial({ color: 0xe6e3dc, roughness: 0.75 });
MT.roof = new THREE.MeshStandardMaterial({ color: 0xc9c7c0, roughness: 0.85 });
MT.roofdeck = new THREE.MeshStandardMaterial({ map: TX.deck, roughness: 0.9 });
MT.soffit = new THREE.MeshStandardMaterial({ color: 0x3a3a3e, roughness: 1, emissive: lit ? 0x2a1a0c : 0x000000, emissiveIntensity: lit ? 1 : 0 });
MT.steel = new THREE.MeshStandardMaterial({ color: 0xcf3a22, roughness: 0.42, metalness: 0.35, emissive: lit ? 0x6a1608 : 0x000000, emissiveIntensity: lit ? 0.7 : 0 });
MT.dark = new THREE.MeshStandardMaterial({ color: 0x2a2d31, roughness: 0.55, metalness: 0.4 });
MT.rail = new THREE.MeshPhysicalMaterial({ color: 0xe5eef2, roughness: 0.04, transparent: true, opacity: 0.32 });
MT.shaft = new THREE.MeshPhysicalMaterial({ color: night ? 0xffe0b0 : 0xb9d0da, roughness: 0.05, metalness: 0.1, transparent: true, opacity: 0.5, emissive: night ? 0xffc27a : 0x000000, emissiveIntensity: night ? 0.7 : 0 });
MT.asphalt = new THREE.MeshStandardMaterial({ map: TX.asphalt, roughness: 0.97, envMapIntensity: 0.25, color: 0xb8b4ac });
MT.paving = new THREE.MeshStandardMaterial({ map: TX.paving, roughness: 0.92, envMapIntensity: 0.35 });
MT.ground = new THREE.MeshStandardMaterial({ color: night ? 0x34363a : 0xa9a8a2, roughness: 1, envMapIntensity: 0.3 });
MT.lane = new THREE.MeshStandardMaterial({ map: TX.asphalt, color: 0x9a9690, roughness: 0.92, envMapIntensity: 0.25 });

const leafTex = ctex(256, 256, (g, w, h) => { g.fillStyle = '#4f6a3a'; g.fillRect(0, 0, w, h);
  for (let i = 0; i < 1800; i++) { const x = rnd(i) * w, y = rnd(i + 31) * h, r = 2 + 5 * rnd(i + 9), t = rnd(i + 70); g.fillStyle = `rgba(${(60 + 60 * t) | 0},${(95 + 70 * t) | 0},${(40 + 30 * t) | 0},0.85)`; g.beginPath(); g.ellipse(x, y, r, r * 0.6, rnd(i) * 6, 0, 7); g.fill(); }
  for (let i = 0; i < 400; i++) { g.fillStyle = 'rgba(25,40,18,0.35)'; g.fillRect(rnd(i + 3) * w, rnd(i + 8) * h, 3, 3); } }, 2, 2);
MT.leaf = [0xd8dcc4, 0xcfd6b8, 0xc4cdae, 0xe0e4cc].map(c => new THREE.MeshStandardMaterial({ map: leafTex, color: c, roughness: 0.95 }));
MT.trunk = new THREE.MeshStandardMaterial({ color: 0x594a3b, roughness: 1 });
MT.white = new THREE.MeshBasicMaterial({ color: 0xf2f2ee });
MT.pit = new THREE.MeshStandardMaterial({ color: night ? 0xffb066 : 0xcfc7b6, roughness: 1, emissive: night ? 0xff8a30 : 0x000000, emissiveIntensity: night ? 0.5 : 0 });
MT.pitwall = new THREE.MeshStandardMaterial({ color: 0xb4b0a6, roughness: 0.95 });
const carCols = [0xf0f0f0, 0x2c3036, 0x8c949b, 0x9e2b22, 0x24467a, 0xd8d2c0, 0x1f1f22];

// prism with metric UVs. returns group
function prism(pts, z0, h, mat, o = {}) {
  let a2 = 0; for (let i = 0; i < pts.length; i++) { const a = pts[i], b = pts[(i + 1) % pts.length]; a2 += (b[0] - a[0]) * (b[1] + a[1]); }
  const ccw = a2 < 0, grp = new THREE.Group(), by = {}; let s = 0;
  for (let i = 0; i < pts.length; i++) {
    const a = pts[i], b = pts[(i + 1) % pts.length], L = Math.hypot(b[0] - a[0], b[1] - a[1]); if (L < 0.05) continue;
    let nx = (b[1] - a[1]) / L, ny = -(b[0] - a[0]) / L; if (!ccw) { nx = -nx; ny = -ny; }
    let m = mat; if (o.green && nx > 0.78) m = MT.green;
    const key = m.uuid; by[key] = by[key] || { m, pos: [], uv: [], idx: [] };
    const W = by[key], base = W.pos.length / 3; const ud = m.map ? m.map.userData : { rw: 4, rh: 3.3 };
    const rw = ud.rw, rh = ud.rh;
    [[a, z0, 0], [b, z0, 1], [b, z0 + h, 1], [a, z0 + h, 0]].forEach(([p, z, e], k) => { const v = V(p[0], p[1], z); W.pos.push(v.x, v.y, v.z); W.uv.push((e ? s + L : s) / rw, (z - z0) / rh); });
    if (ccw) W.idx.push(base, base + 1, base + 2, base, base + 2, base + 3); else W.idx.push(base, base + 2, base + 1, base, base + 3, base + 2);
    s += L;
  }
  for (const k in by) { const W = by[k], g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.Float32BufferAttribute(W.pos, 3)); g.setAttribute('uv', new THREE.Float32BufferAttribute(W.uv, 2));
    g.setIndex(W.idx); g.computeVertexNormals(); const me = new THREE.Mesh(g, W.m); me.castShadow = o.noShadow ? false : true; me.receiveShadow = true;
    if (W.m === MT.screen) me.customDepthMaterial = new THREE.MeshDepthMaterial({ depthPacking: THREE.RGBADepthPacking, map: TX.screenA, alphaTest: 0.5 });
    grp.add(me); }
  if (!o.noCaps) {
    const shape = new THREE.Shape(pts.map(p => new THREE.Vector2(p[0], p[1])));
    for (const [z, bot] of [[z0 + h, false], [z0, true]]) {
      const g = new THREE.ShapeGeometry(shape); g.rotateX(-Math.PI / 2); g.translate(0, z, 0);
      if (mat === MT.roofdeck && !bot) { const u = g.attributes.uv; for (let i = 0; i < u.count; i++) u.setXY(i, u.getX(i) / 4, u.getY(i) / 4); }
      const cm = bot ? (o.botMat || MT.soffit) : (o.capMat || (mat === MT.roofdeck ? MT.roofdeck : (mat === MT.roof ? MT.roof : MT.slab)));
      const me = new THREE.Mesh(g, cm); me.material.side = THREE.DoubleSide; me.castShadow = true; me.receiveShadow = true; grp.add(me);
    }
  }
  scene.add(grp); return grp;
}
function flat(pts, z, mat, uvScale = 1 / 4) {
  const g = new THREE.ShapeGeometry(new THREE.Shape(pts.map(q => new THREE.Vector2(q[0], q[1])))); g.rotateX(-Math.PI / 2); g.translate(0, z, 0);
  const u = g.attributes.uv; for (let i = 0; i < u.count; i++) u.setXY(i, u.getX(i) * uvScale, u.getY(i) * uvScale);
  const m = new THREE.Mesh(g, mat); m.receiveShadow = true; scene.add(m); return m;
}

// ---------- ground with sunken-court hole ----------
{
  const R = 1500, shape = new THREE.Shape([new THREE.Vector2(c0[0] - R, c0[1] - R), new THREE.Vector2(c0[0] + R, c0[1] - R), new THREE.Vector2(c0[0] + R, c0[1] + R), new THREE.Vector2(c0[0] - R, c0[1] + R)]);
  (des.pit || []).forEach(p => { shape.holes.push(new THREE.Path(p.map(q => new THREE.Vector2(q[0], q[1])).reverse())); });
  const g = new THREE.ShapeGeometry(shape); g.rotateX(-Math.PI / 2); const m = new THREE.Mesh(g, MT.ground); m.receiveShadow = true; scene.add(m);
}
// roads: sidewalk under, asphalt, markings
function ribbon(a, b, w, y, mat, ext = 0.5) {
  const L = Math.hypot(b[0] - a[0], b[1] - a[1]); if (L < 0.1) return;
  const g = new THREE.PlaneGeometry(L + ext, w); g.rotateX(-Math.PI / 2);
  const u = g.attributes.uv; for (let i = 0; i < u.count; i++) u.setXY(i, u.getX(i) * (L + ext) / 6, u.getY(i) * w / 6);
  const m = new THREE.Mesh(g, mat); m.position.copy(V((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, y)); m.rotation.y = Math.atan2(b[1] - a[1], b[0] - a[0]); m.receiveShadow = true; scene.add(m);
}
for (const r of ctx.roads) { for (let i = 0; i < r.pts.length - 1; i++) ribbon(r.pts[i], r.pts[i + 1], r.w + 6, 0.012, MT.paving); }
for (const r of ctx.roads) { for (let i = 0; i < r.pts.length - 1; i++) ribbon(r.pts[i], r.pts[i + 1], r.w, 0.02 + r.w / 3000, MT.asphalt); }
const lineM = new THREE.MeshBasicMaterial({ color: 0xe9e5d2 });
for (const r of ctx.roads) if (r.w >= 12) for (let i = 0; i < r.pts.length - 1; i++) {
  const a = r.pts[i], b = r.pts[i + 1], L = Math.hypot(b[0] - a[0], b[1] - a[1]);
  for (let t = 0; t < L - 4; t += 9) { const t0 = t / L, t1 = (t + 4.5) / L; ribbon([a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0], [a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1], 0.16, 0.05 + r.w / 3000, lineM, 0); }
}
// site plaza (3m setbacks + tips) paving
flat(des.block[0], 0.03, MT.paving);
(des.lane || []).forEach(p => flat(p, 0.04, MT.lane, 1 / 6));
(des.tips || []).forEach(p => flat(p, 0.045, MT.paving));
(des.walks || []).forEach(p => { prism(p, 0, 0.14, MT.paving, { capMat: MT.paving, botMat: MT.paving }); });
// pit
(des.pit || []).forEach(p => {
  flat(p, -4.5, MT.pit);
  const n = p.length; for (let i = 0; i < n; i++) { const a = p[i], b = p[(i + 1) % n]; const L = Math.hypot(b[0] - a[0], b[1] - a[1]); if (L < 0.1) continue;
    const g = new THREE.PlaneGeometry(L, 4.5); const m = new THREE.Mesh(g, MT.pitwall); m.position.copy(V((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, -2.25));
    m.rotation.y = Math.atan2(b[1] - a[1], b[0] - a[0]) + Math.PI; m.material.side = THREE.DoubleSide; scene.add(m); }
});

// ---------- context buildings ----------
for (let i = 0; i < ctx.buildings.length; i++) { const b = ctx.buildings[i]; const wt = ctxWalls[i % ctxWalls.length]; prism(b.pts, 0, b.h, new THREE.MeshStandardMaterial({ map: wt, roughness: 0.9 }), { capMat: MT.roof, botMat: MT.roof }); }

// ---------- design ----------
for (const p of des.parts) {
  if (p.mat === 'screen' || p.mat === 'base') {
    prism(p.pts, p.z0, p.h, MT.screen, { green: false, noCaps: true });
    if (p.inner) prism(p.inner, p.z0, p.h, MT.inner, { noShadow: true, noCaps: false, capMat: MT.soffit, botMat: MT.soffit });
    // east-facing green wall layer (solid) on top of screen for east-facing edges
    const g2 = prism(p.pts.map(q => q), p.z0, p.h, MT.screen, { green: false, noCaps: true, noShadow: true }); g2.visible = false;
  } else if (p.mat === 'glass') prism(p.pts, p.z0, p.h, MT.glass);
  else if (p.mat === 'fin') prism(p.pts, p.z0, p.h, MT.fin);
  else if (p.mat === 'slab') prism(p.pts, p.z0, p.h, MT.slab);
  else if (p.mat === 'roof') prism(p.pts, p.z0, p.h, MT.roof);
  else if (p.mat === 'roofdeck') prism(p.pts, p.z0, p.h, MT.roofdeck);
}
// solar + rails + steel
const solarTex = ctex(256, 256, (g, w, h) => { g.fillStyle = '#8f989d'; g.fillRect(0, 0, w, h); for (let i = 0; i < 4; i++) for (let j = 0; j < 2; j++) { g.fillStyle = '#1b2a40'; g.fillRect(i * 64 + 3, j * 128 + 5, 58, 118); g.fillStyle = 'rgba(150,185,215,0.22)'; g.fillRect(i * 64 + 3, j * 128 + 5, 58, 24); } }, 6, 6);
(des.solar || []).forEach(p => flat(p.pts, p.z + 0.06, new THREE.MeshStandardMaterial({ map: solarTex, roughness: 0.3, metalness: 0.3 })));
(des.posts || []).forEach(p => { const m = new THREE.Mesh(new THREE.BoxGeometry(0.32, p[2], 0.32), MT.dark); m.position.copy(V(p[0], p[1], p[2] / 2)); m.castShadow = true; scene.add(m); });
(des.beams || []).forEach(b => { const [x1, y1, x2, y2, z] = b, L = Math.hypot(x2 - x1, y2 - y1); const m = new THREE.Mesh(new THREE.BoxGeometry(L, 0.34, 0.24), MT.dark); m.position.copy(V((x1 + x2) / 2, (y1 + y2) / 2, z)); m.rotation.y = Math.atan2(y2 - y1, x2 - x1); m.castShadow = true; scene.add(m); });
(des.parapets || []).forEach(b => { const [x1, y1, x2, y2, z] = b, L = Math.hypot(x2 - x1, y2 - y1); const m = new THREE.Mesh(new THREE.BoxGeometry(L, 1.15, 0.05), MT.rail); m.position.copy(V((x1 + x2) / 2, (y1 + y2) / 2, z + 0.58)); m.rotation.y = Math.atan2(y2 - y1, x2 - x1); scene.add(m);
  const t = new THREE.Mesh(new THREE.BoxGeometry(L, 0.05, 0.08), MT.dark); t.position.copy(V((x1 + x2) / 2, (y1 + y2) / 2, z + 1.16)); t.rotation.y = m.rotation.y; scene.add(t); });
(des.stairs || []).forEach(f => { const [x1, y1, z1, x2, y2, z2, wd] = f, run = Math.hypot(x2 - x1, y2 - y1), ang = Math.atan2(z2 - z1, run), yaw = Math.atan2(y2 - y1, x2 - x1);
  const cx = (x1 + x2) / 2, cy = (y1 + y2) / 2, cz = (z1 + z2) / 2, len = Math.hypot(run, z2 - z1);
  const slab = new THREE.Mesh(new THREE.BoxGeometry(len, 0.14, wd), MT.steel); slab.position.copy(V(cx, cy, cz)); slab.rotation.order = 'YZX'; slab.rotation.y = yaw; slab.rotation.z = ang; slab.castShadow = true; scene.add(slab);
  const stp = Math.max(4, Math.round(len / 0.3)); const ns = Math.round(len / 0.32);
  const rg = new THREE.Mesh(new THREE.BoxGeometry(len, 1.0, 0.035), MT.rail); rg.position.copy(V(cx, cy, cz + 0.55)); rg.rotation.copy(slab.rotation); rg.translateZ(wd / 2 - 0.05); scene.add(rg);
  const rg2 = rg.clone(); rg2.translateZ(-(wd - 0.1)); scene.add(rg2);
  const hr = new THREE.Mesh(new THREE.BoxGeometry(len, 0.05, 0.07), MT.steel); hr.position.copy(rg.position); hr.rotation.copy(rg.rotation); hr.translateY(0.5); scene.add(hr); const hr2 = hr.clone(); hr2.translateZ(-(wd - 0.1)); scene.add(hr2); });
(des.shafts || []).forEach(s => { const m = new THREE.Mesh(new THREE.BoxGeometry(2.8, s[2], 2.8), MT.shaft); m.position.copy(V(s[0], s[1], s[2] / 2)); scene.add(m);
  const fr = new THREE.Mesh(new THREE.BoxGeometry(3.0, 0.4, 3.0), MT.dark); fr.position.copy(V(s[0], s[1], s[2])); scene.add(fr); });

// ---------- entourage ----------
function tree(x, y, z, s = 1, i = 0) {
  const grp = new THREE.Group(); const tr = new THREE.Mesh(new THREE.CylinderGeometry(0.13 * s, 0.2 * s, 2.6 * s, 7), MT.trunk); tr.position.y = 1.3 * s; tr.castShadow = true; grp.add(tr);
  for (let k = 0; k < 11; k++) { const r = (0.8 + 0.5 * rnd(i * 7 + k)) * s; const sp = new THREE.Mesh(new THREE.IcosahedronGeometry(r, 2), MT.leaf[(i + k) % 4]);
    sp.position.set((rnd(i * 3 + k) - 0.5) * 1.8 * s, (2.8 + rnd(i * 5 + k) * 1.6) * s, (rnd(i * 11 + k) - 0.5) * 1.8 * s); sp.scale.y = 0.85; sp.castShadow = true; grp.add(sp); }
  grp.position.copy(V(x, y, z)); scene.add(grp);
}
(des.trees || []).forEach((t, i) => tree(t[0], t[1], t[2], t[3] || 1, i));
function car(x, y, yaw, i) {
  const col = carCols[i % carCols.length], body = new THREE.MeshStandardMaterial({ color: col, roughness: 0.28, metalness: 0.5 }), glassM = new THREE.MeshStandardMaterial({ color: 0x1c242c, roughness: 0.1, metalness: 0.7 });
  const grp = new THREE.Group(); const lo = new THREE.Mesh(new THREE.BoxGeometry(4.5, 0.75, 1.8), body); lo.position.y = 0.62; lo.castShadow = true; grp.add(lo);
  const cab = new THREE.Mesh(new THREE.BoxGeometry(2.3, 0.62, 1.64), glassM); cab.position.set(-0.15, 1.28, 0); cab.castShadow = true; grp.add(cab);
  const roof = new THREE.Mesh(new THREE.BoxGeometry(2.0, 0.07, 1.6), body); roof.position.set(-0.15, 1.62, 0); grp.add(roof);
  for (const [dx, dz] of [[1.4, 0.9], [1.4, -0.9], [-1.4, 0.9], [-1.4, -0.9]]) { const w = new THREE.Mesh(new THREE.CylinderGeometry(0.34, 0.34, 0.22, 12), MT.dark); w.rotation.x = Math.PI / 2; w.position.set(dx, 0.34, dz); grp.add(w); }
  if (lit) { const hl = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.18, 1.3), new THREE.MeshBasicMaterial({ color: 0xfff2c0 })); hl.position.set(2.26, 0.7, 0); grp.add(hl); const tl = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.16, 1.3), new THREE.MeshBasicMaterial({ color: 0xff3020 })); tl.position.set(-2.26, 0.75, 0); grp.add(tl); }
  grp.position.copy(V(x, y, 0)); grp.rotation.y = yaw; scene.add(grp);
}
(des.cars || []).forEach((c, i) => car(c[0], c[1], c[2] || 0, i));
const pc = [0x3b4048, 0x6b4a40, 0xcfc8ba, 0x2f3d52, 0x8a7a62, 0x55606b, 0x4a5a4c, 0x7a4252, 0x1f2227, 0xa89a82];
(des.people || []).forEach((p, i) => { const grp = new THREE.Group(); const mat = new THREE.MeshStandardMaterial({ color: pc[i % pc.length], roughness: 0.9 }); const sk = new THREE.MeshStandardMaterial({ color: [0xd5ad8a, 0xc79a78, 0xe0bd9c][i % 3], roughness: 0.8 });
  const dark = new THREE.MeshStandardMaterial({ color: [0x23262c, 0x34383f, 0x4a4338][i % 3], roughness: 0.9 });
  const hs = 0.92 + 0.12 * rnd(i + 3);
  const torso = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.17, 0.62, 10), mat); torso.position.y = 1.2; torso.castShadow = true; grp.add(torso);
  const sh = new THREE.Mesh(new THREE.SphereGeometry(0.21, 10, 8), mat); sh.scale.set(1, 0.5, 0.7); sh.position.y = 1.5; grp.add(sh);
  for (const sx of [-0.09, 0.09]) { const lg = new THREE.Mesh(new THREE.CylinderGeometry(0.075, 0.06, 0.88, 8), dark); lg.position.set(sx, 0.45, 0); lg.castShadow = true; grp.add(lg); }
  for (const sx of [-0.24, 0.24]) { const ar = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.045, 0.58, 8), mat); ar.position.set(sx, 1.22, 0); grp.add(ar); }
  const head = new THREE.Mesh(new THREE.SphereGeometry(0.115, 10, 8), sk); head.position.y = 1.7; grp.add(head);
  const hair = new THREE.Mesh(new THREE.SphereGeometry(0.12, 10, 8, 0, 6.3, 0, 1.4), new THREE.MeshStandardMaterial({ color: [0x15110e, 0x2a1d14, 0x5a4636][i % 3], roughness: 1 })); hair.position.y = 1.72; grp.add(hair);
  grp.scale.setScalar(hs); grp.position.copy(V(p[0], p[1], p[2] || 0)); grp.rotation.y = rnd(i) * 6; scene.add(grp); });
// street lamps
const lampPts = (des.lamps || []);
lampPts.forEach(p => { const pole = new THREE.Mesh(new THREE.CylinderGeometry(0.07, 0.1, 8, 6), MT.dark); pole.position.copy(V(p[0], p[1], 4)); scene.add(pole);
  const head = new THREE.Mesh(new THREE.BoxGeometry(0.9, 0.12, 0.3), new THREE.MeshBasicMaterial({ color: lit ? 0xfff0c8 : 0x999999 })); head.position.copy(V(p[0], p[1], 8)); scene.add(head); });
if (lit) { for (const p of (des.lights || [])) { const l = new THREE.PointLight(0xffc98a, p[3] || 300, 45, 1.7); l.position.copy(V(p[0], p[1], p[2])); scene.add(l); } }
// lane soffit lamps
(des.laneLamps || []).forEach(p => { const m = new THREE.Mesh(new THREE.BoxGeometry(1.2, 0.08, 0.25), new THREE.MeshBasicMaterial({ color: 0xfff0d0 })); m.position.copy(V(p[0], p[1], p[2])); scene.add(m); });

// distant hills (황령산 to the east, other ridges)
{ const hm = new THREE.MeshStandardMaterial({ color: night ? 0x16221c : 0x5d7656, roughness: 1, fog: true });
  for (const [dx, dy, r, hh] of [[2300, -200, 1100, 420]]) { const m = new THREE.Mesh(new THREE.SphereGeometry(r, 36, 18), hm); m.scale.set(1, hh / r, 1); m.position.copy(V(c0[0] + dx, c0[1] + dy, 0)); scene.add(m); } }
// terrace features
const lawnM = new THREE.MeshStandardMaterial({ map: TX.green, roughness: 1, color: 0xb9c9a0 });
(des.lawns || []).forEach(p => flat(p, des.roofz + 0.05, lawnM, 1 / 3));
(des.benches || []).forEach(b => { const m = new THREE.Mesh(new THREE.BoxGeometry(2.0, 0.08, 0.5), new THREE.MeshStandardMaterial({ color: 0x8a6a48, roughness: 0.8 })); m.position.copy(V(b[0], b[1], des.roofz + 0.46)); m.rotation.y = b[2] || 0; m.castShadow = true; scene.add(m);
  for (const sx of [-0.8, 0.8]) { const l = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.42, 0.42), MT.dark); l.position.copy(V(b[0] + Math.cos(b[2] || 0) * sx, b[1] + Math.sin(b[2] || 0) * sx, des.roofz + 0.22)); scene.add(l); } });
(des.shrubs || []).forEach((p, i) => { const m = new THREE.Mesh(new THREE.IcosahedronGeometry(p[2], 1), MT.leaf[i % 4]); m.position.copy(V(p[0], p[1], des.roofz + p[2] * 0.7)); m.scale.y = 0.7; m.castShadow = true; scene.add(m); });
if (lit) (des.stringLights || []).forEach(p => { const m = new THREE.Mesh(new THREE.SphereGeometry(0.12, 6, 6), new THREE.MeshBasicMaterial({ color: 0xffe3a0 })); m.position.copy(V(p[0], p[1], p[2])); scene.add(m); });

// ---------- camera + post ----------
const cam = new THREE.PerspectiveCamera(view.fov || 50, view.w / view.h, 1.5, 3000);
cam.position.copy(V(...view.eye)); cam.lookAt(V(...view.target)); cam.updateProjectionMatrix();
const comp = new EffectComposer(renderer); comp.setPixelRatio(PR); comp.setSize(view.w, view.h);
comp.addPass(new RenderPass(scene, cam));
if (!view.noAO) { const ao = new SSAOPass(scene, cam, view.w * PR, view.h * PR); ao.kernelRadius = view.aoR ?? 7; ao.minDistance = 0.0006; ao.maxDistance = 0.03; comp.addPass(ao); }
if (lit) comp.addPass(new UnrealBloomPass(new THREE.Vector2(view.w, view.h), night ? 0.55 : 0.35, 0.7, 0.82));
comp.addPass(new OutputPass());
const grade = new ShaderPass({ uniforms: { tDiffuse: { value: null }, vig: { value: 0.32 }, warm: { value: lit ? 0.0 : 0.035 } },
  vertexShader: 'varying vec2 vUv; void main(){ vUv=uv; gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.0); }',
  fragmentShader: 'uniform sampler2D tDiffuse; uniform float vig; uniform float warm; varying vec2 vUv; void main(){ vec4 c=texture2D(tDiffuse,vUv); float d=distance(vUv,vec2(0.5)); c.rgb*=1.0-vig*smoothstep(0.35,0.95,d); c.rgb+=vec3(warm,warm*0.4,-warm*0.6); c.rgb=mix(vec3(dot(c.rgb,vec3(0.299,0.587,0.114))),c.rgb,1.06); gl_FragColor=c; }' });
comp.addPass(grade);
comp.render();
window.DONE = true;
