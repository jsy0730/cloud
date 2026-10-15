import sys; sys.path.insert(0,'.')
from env_common import *
import shapely
XL=(-150,230); YL=(-110,240)
# source classes: (reference Leq at 10 m, dB(A), day) -- ASSUMED, to be replaced by field measurement
REF={'secondary':70,'primary':72,'trunk':72,'tertiary':63,'residential':58,'unclassified':58,'service':52,'living_street':50,'secondary_link':64,'trunk_link':66,'pedestrian':40,'footway':35}
lines=[]
for r in CTX['roads']:
    if len(r['pts'])<2: continue
    ls=LineString(r['pts'])
    if ls.distance(Point(21,63))>450: continue
    lines.append((ls,REF.get(r['hw'],55),r['w'],r['hw'],r['name']))
SRC=[]  # (x,y,I0*d0*dl/pi)
for ls,L0,w,hw,name in lines:
    n=max(1,int(ls.length/5)); dl=ls.length/n
    for i in range(n):
        p=ls.interpolate((i+0.5)*dl)
        SRC.append((p.x,p.y,10**(L0/10)*10.0*dl/math.pi))
SRC=np.array(SRC)
def levels(X,Y,night=False):
    I=np.zeros_like(X,dtype=float)
    for sx,sy,e in SRC:
        r2=(X-sx)**2+(Y-sy)**2+9.0
        I+=e/r2
    L=10*np.log10(I)
    return L-8.0 if night else L
def level(x,y,night=False): return float(levels(np.array([x]),np.array([y]),night)[0])
xs=np.arange(XL[0],XL[1],4.0); ys=np.arange(YL[0],YL[1],4.0)
X,Y=np.meshgrid(xs,ys)
Z=levels(X,Y)
fig,ax=plt.subplots(figsize=(6.6,6.0),dpi=170)
draw_ctx(ax,XL,YL)
lv=[50,58,60,62,64,66,68,70,72,74,80]
cmap=plt.get_cmap('YlOrRd')
cols=[cmap(0.08+0.85*i/(len(lv)-2)) for i in range(len(lv)-1)]
ax.contourf(X,Y,Z,levels=lv,colors=cols,alpha=0.72,zorder=3)
ax.contour(X,Y,Z,levels=[60,65,70],colors='#5a1a00',linewidths=[0.6,0.9,1.2],zorder=4)
draw_site(ax)
ax.axvline(XE+45,color=RED,ls=(0,(4,3)),lw=1.2,zorder=6)
for lab,(x,y) in {'W':(-2,60),'N':(21,131),'S':(20,-4),'E':(XE+4,60)}.items():
    ax.plot([x],[y],'o',color='white',mec='black',ms=6,zorder=8)
ax.set_xlim(*XL); ax.set_ylim(*YL); ax.set_aspect('equal'); ax.axis('off')
north_arrow(ax,XL[0]+14,YL[0]+8)
import matplotlib.patches as mp
leg=[mp.Patch(fc=cols[i],ec='none',label=f'{lv[i]}–{lv[i+1]}' if i>0 else f'{lv[1]} 미만') for i in range(len(cols))]
ax.legend(handles=leg[::-1],title='추정 주간 Leq dB(A)',loc='lower right',fontsize=7.5,title_fontsize=8,frameon=True,ncol=2)
plt.savefig('fig/noise_map.png',facecolor='white',bbox_inches='tight',pad_inches=0.08); plt.close()
# facade-level estimates (day / night) at facade mid-points, 1 m outside
pts={'서측(전포대로)':(-2,60),'북측(서전로)':(21,131),'남측(224번길)':(20,-4),'동측(이면도로)':(XE+4,60),'동측 주거 경계(+45m)':(XE+45,60)}
for k,(x,y) in pts.items():
    print(k,round(level(x,y),1),'night',round(level(x,y,True),1))
print('lines',len(lines),sorted({(h,l) for _,l,_,h,_ in lines}))
