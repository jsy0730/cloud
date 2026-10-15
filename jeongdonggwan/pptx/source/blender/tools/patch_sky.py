import os
p = os.path.join(os.environ['TEMP'], 'bl', 'build_scene.py')
s = open(p, encoding='utf8').read()

# 1) HDRI sun alignment helper (inserted before world setup)
marker = "# ------------------------------------------------------------------ world / sun / camera"
helper = '''import numpy as np


def aligned_hdri(path, az_target_rad):
    """roll an equirect HDRI so its sun sits at compass azimuth az_target (Blender mapping: u = atan2(y,-x)/2pi + .5)"""
    src = bpy.data.images.load(path, check_existing=True)
    w, h = src.size
    arr = np.empty(w * h * 4, dtype=np.float32); src.pixels.foreach_get(arr)
    a = arr.reshape(h, w, 4)
    lum = a[..., :3].mean(axis=2)
    thr = np.percentile(lum, 99.995)
    ys, xs = np.where(lum >= thr)
    wts = lum[ys, xs]
    cu = float((xs * wts).sum() / wts.sum()) / w
    sun_el = (float((ys * wts).sum() / wts.sum()) / h - 0.5) * math.pi
    # target column from desired azimuth (elevation does not matter for u)
    ut = math.atan2(math.cos(az_target_rad), -math.sin(az_target_rad)) / (2 * math.pi) + 0.5
    shift = int(round((ut - cu) * w))
    rolled = np.roll(a, shift, axis=1)
    out = bpy.data.images.new('hdri_aligned', w, h, float_buffer=True, alpha=False)
    out.pixels.foreach_set(rolled.ravel()); out.pack() if False else None
    return out, math.degrees(sun_el)


'''
s = s.replace(marker, helper + marker)

# 2) day world: aligned HDRI instead of Nishita sky + lamp
a = s.index("else:\n    sky = wn.nodes.new('ShaderNodeTexSky')")
b = s.index("wn.links.new(bg.outputs[0], wout.inputs['Surface'])")
new = '''else:
    himg, hel = aligned_hdri(os.path.join(PH, 'hdri', 'kloofendal_48d_partly_cloudy_puresky_2k.hdr'), az)
    print('HDRI sun elevation', round(hel, 1))
    env = wn.nodes.new('ShaderNodeTexEnvironment'); env.image = himg
    wn.links.new(env.outputs['Color'], bg.inputs['Color']); bg.inputs['Strength'].default_value = 1.0
'''
s = s[:a] + new + s[b:]
# wood tint more brown, asphalt lighter, exposure
s = s.replace("tint.inputs[7].default_value = (1.35, 0.9, 0.65, 1)", "tint.inputs[7].default_value = (1.05, 0.72, 0.5, 1)")
s = s.replace("M['asphalt'] = tex_mat('asphalt', 'asphalt_02', scale=4.0, nstr=0.8, tint=(0.8, 0.8, 0.8, 1))", "M['asphalt'] = tex_mat('asphalt', 'asphalt_02', scale=4.0, nstr=0.8, tint=(1.5, 1.5, 1.5, 1))")
s = s.replace("scene.view_settings.exposure = -0.2 if not LIT else 0.6", "scene.view_settings.exposure = float(os.environ.get('JD_EXPO', '-0.3' if not LIT else '0.6'))")
open(p, 'w', encoding='utf8').write(s)
print('ok')
