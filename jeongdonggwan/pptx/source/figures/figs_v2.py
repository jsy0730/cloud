from fig_ds import *
import shapely
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.patches import Patch
WIN = (2026, 12, 21); SUM = (2026, 6, 21); EQ = (2026, 3, 21)
XL = (-95, 185); YL = (-62, 198)

# ---------- 1. shadow study (3 panels) ----------
fig, axs = plt.subplots(1, 3, figsize=(12.6, 4.6))
for ax, (hh, lab) in zip(axs, [(9, '09:00'), (12, '12:00'), (15, '15:00')]):
    az, el = sunpos(*WIN, hh)
    base_map(ax, XL, YL)
    sh = site_shadow(az, el)
    for q in polys(sh):
        ax.add_patch(MPoly(list(q.exterior.coords), closed=True, fc=NAVY, alpha=0.30, ec=NAVY, lw=0.7, zorder=4))
    mass(ax); site_outline(ax); zone_line(ax, YL)
    north(ax, XL[0] + 14, YL[0] + 8); scale_bar(ax, XL[1] - 42, YL[0] + 8)
    ax.set_title(f'동지 {lab}', loc='left', fontsize=13.5, fontweight='bold', color=NAVY, pad=6)
    ax.text(XL[1] - 1, YL[1] + 3, f'방위 {az:.0f}° · 고도 {el:.1f}°', fontsize=9.5, color=MUTED, va='bottom', ha='right')
plt.subplots_adjust(wspace=0.04)
save(fig, 'shadow3')

# ---------- 2. polar sun path ----------
fig = plt.figure(figsize=(5.4, 5.6)); ax = fig.add_subplot(111, projection='polar')
ax.set_theta_zero_location('N'); ax.set_theta_direction(-1); ax.set_ylim(0, 90)
ax.set_facecolor(PANEL)
ax.set_rgrids([15, 30, 45, 60, 75, 90], labels=[], angle=0)
ax.set_thetagrids([0, 90, 180, 270], labels=['북', '동', '남', '서'], fontsize=12, fontweight='bold', color=INK)
ax.grid(color='white', lw=1.2); ax.spines['polar'].set_color(LINE)
th = np.radians(np.linspace(235, 305, 40)); ax.fill_between(th, 0, 90, color=ZQUIET, alpha=0.55, zorder=0)
ax.text(np.radians(270), 83, '서향\n일사', fontsize=8.5, color='#7a2b2b', ha='center', va='center', fontweight='medium', linespacing=1.1)
for r, l in ((30, '고도 60°'), (60, '30°')):
    ax.text(np.radians(158), r + 1, l, fontsize=8, color=MUTED, ha='left', va='bottom')
for nm, d, col, lw in [('동지', WIN, D1, 2.6), ('춘·추분', EQ, D2, 2.2), ('하지', SUM, '#e07a00', 2.2)]:
    A = []; R = []
    for t in np.arange(4.5, 19.51, 0.1):
        a, e = sunpos(*d, int(t), int(round((t % 1) * 60)))
        if e > 0:
            A.append(np.radians(a)); R.append(90 - e)
    ax.plot(A, R, color=col, lw=lw, label=nm, zorder=5, solid_capstyle='round')
    for h in (8, 10, 12, 14, 16):
        a, e = sunpos(*d, h)
        if e > 0:
            ax.plot(np.radians(a), 90 - e, 'o', ms=5.5, mfc='white', mec=col, mew=1.6, zorder=6)
            if nm in ('동지', '하지'):
                ax.text(np.radians(a), 90 - e + (5.8 if nm == '하지' else -6.2), str(h), fontsize=7.5, color=col, ha='center', va='center', fontweight='bold')
ax.set_yticklabels([])
ax.tick_params(axis='x', pad=10)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=3, frameon=False, fontsize=10.5, handlelength=1.6)
save(fig, 'sunpath')

# ---------- 3. winter shadow hours map ----------
xs = np.arange(XL[0], XL[1], 1.5); ys = np.arange(YL[0], YL[1], 1.5); X, Y = np.meshgrid(xs, ys)
cnt = np.zeros_like(X)
for t in [h + m / 60 for h in range(9, 15) for m in (0, 30)] + [15.0]:
    az, el = sunpos(*WIN, int(t), int(round((t % 1) * 60))); sh = site_shadow(az, el)
    if sh is not None:
        cnt += shapely.contains_xy(sh, X, Y)
hours = cnt * 0.5
hours[shapely.contains_xy(SITE, X, Y)] = np.nan
fig, ax = plt.subplots(figsize=(5.2, 5.2))
base_map(ax, XL, YL)
cols = [D5, D4, D3, D2, D1, '#050f33']
cm = ListedColormap(cols); nm_ = BoundaryNorm([0.25, 1, 2, 3, 4, 5, 6.1], cm.N)
hm = np.ma.masked_where((hours < 0.25) | np.isnan(hours), hours)
ax.pcolormesh(X, Y, hm, cmap=cm, norm=nm_, alpha=0.85, zorder=4, shading='auto')
mass(ax); site_outline(ax); zone_line(ax, YL); north(ax, XL[0] + 14, YL[0] + 8); scale_bar(ax, XL[1] - 42, YL[0] + 8)
ax.legend(handles=[Patch(fc=c, label=l) for c, l in zip(cols, ['~1h', '1~2h', '2~3h', '3~4h', '4~5h', '5h~'])],
          loc='upper center', bbox_to_anchor=(0.5, 0.0), ncol=6, frameon=False, fontsize=9, handlelength=1.2, columnspacing=0.9, borderaxespad=0.4)
save(fig, 'shadow_hours')
print('ok')
