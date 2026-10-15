import sys; sys.path.insert(0,'.')
from env_common import *
XL=(-110,190); YL=(-70,200)
WINTER=(2026,12,21); SUMMER=(2026,6,21); EQ=(2026,3,21)
# ---------- 3-panel shadow study
fig,axs=plt.subplots(1,3,figsize=(13.2,4.9),dpi=170)
for ax,(hh,lab) in zip(axs,[(9,'09:00'),(12,'12:00'),(15,'15:00')]):
    az,el=sunpos(*WINTER,hh)
    draw_ctx(ax,XL,YL)
    sh=site_shadow(az,el)
    for q in polys(sh): ax.add_patch(MPoly(list(q.exterior.coords),closed=True,fc=NAVY,ec='none',alpha=0.30,zorder=4))
    draw_site(ax)
    # zone line: 3종일반주거 starts ~45 m east of block
    ax.axvline(XE+45,color=RED,ls=(0,(4,3)),lw=1.2,zorder=6)
    ax.set_xlim(*XL); ax.set_ylim(*YL); ax.set_aspect('equal'); ax.axis('off')
    ax.set_title(f'동지 {lab}  (방위 {az:.0f}°, 고도 {el:.1f}°)',fontsize=11.5,fontweight='bold',color=NAVY)
    north_arrow(ax,XL[0]+14,YL[0]+8)
    ax.text(XE+47,YL[1]-4,'제3종일반주거 ▶',color=RED,fontsize=8.5,va='top')
plt.tight_layout(); plt.savefig('fig/shadow3.png',facecolor='white',bbox_inches='tight',pad_inches=0.08); plt.close()
# ---------- hours map (winter solstice 09-15h, 30-min steps)
xs=np.arange(XL[0],XL[1],2.0); ys=np.arange(YL[0],YL[1],2.0)
X,Y=np.meshgrid(xs,ys)
import shapely
cnt=np.zeros_like(X)
steps=[h+m/60 for h in range(9,15) for m in (0,30)]+[15.0]
for t in steps:
    az,el=sunpos(*WINTER,int(t),int(round((t%1)*60)))
    sh=site_shadow(az,el)
    if sh is None: continue
    cnt+=shapely.contains_xy(sh,X,Y)
hours=cnt*0.5
# exclude the building itself
inside=shapely.contains_xy(SITE,X,Y); hours[inside]=np.nan
fig,ax=plt.subplots(figsize=(6.4,6.4),dpi=170)
draw_ctx(ax,XL,YL)
im=ax.pcolormesh(X,Y,np.ma.masked_where((hours==0)|np.isnan(hours),hours),cmap='YlOrRd',vmin=0,vmax=6,alpha=0.78,zorder=4,shading='auto')
draw_site(ax)
ax.axvline(XE+45,color=RED,ls=(0,(4,3)),lw=1.2,zorder=6)
ax.set_xlim(*XL); ax.set_ylim(*YL); ax.set_aspect('equal'); ax.axis('off')
cb=plt.colorbar(im,ax=ax,fraction=0.04,pad=0.01,shrink=0.7); cb.set_label('동지 09–15시 그림자 시간(h)',fontsize=9)
north_arrow(ax,XL[0]+14,YL[0]+8)
plt.tight_layout(); plt.savefig('fig/shadow_hours.png',facecolor='white',bbox_inches='tight',pad_inches=0.08); plt.close()
# numbers: shadow hours falling on east residential strip (x > XE+45) and on road/west
sel=(X>XE+45)&(X<XE+45+60)&(Y>-20)&(Y<150)
print('east strip (45-105m from block): max h',np.nanmax(hours[sel]),'mean h',round(float(np.nanmean(hours[sel])),2),'share>0',round(float((hours[sel]>0).mean()),2),'share>=2h',round(float((hours[sel]>=2).mean()),2))
for hh in (9,10,11,12,13,14,15):
    az,el=sunpos(*WINTER,hh); sh=site_shadow(az,el)
    # farthest reach east
    e=sh.bounds
    print(hh,round(az),round(el,1),'shadow bounds x',round(e[0]),round(e[2]),'y',round(e[1]),round(e[3]))
