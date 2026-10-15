import sys; sys.path.insert(0,'.')
from env_common import *
import shapely
from geo import ll2m
LM={'황령산 정상(427m)':(35.1573354,129.0819088,427.0),'BIFC(289m)':(35.14641389,129.06485,289.0)}
GZ=8.0   # assumed ground level near site (m a.s.l.) -- rough
lm={}
for k,(la,lo,h) in LM.items(): lm[k]=(ll2m(la,lo),h)
tc=TERR.centroid
eyes={'1층 가로(전포대로변)':(Point(-14,60),1.6),'옥상 광장(+21.1m)':(Point(tc.x,tc.y),21.1+1.6)}
az=np.arange(0,360,0.5)
obst=[(Polygon(b['pts']),b['h']) for b in CTX['buildings']]+[(q,h) for g,h in PARTS for q in polys(g)]
def skyline(eye,eh):
    rays=[LineString([(eye.x,eye.y),(eye.x+500*math.sin(math.radians(a)),eye.y+500*math.cos(math.radians(a)))]) for a in az]
    rays=np.array(rays,dtype=object)
    best=np.full(len(az),-90.0)
    for poly,h in obst:
        if h<=eh: continue
        if not poly.is_valid: poly=poly.buffer(0)
        inter=shapely.intersection(rays,poly)
        ok=~shapely.is_empty(inter)
        if not ok.any(): continue
        d=shapely.distance(inter[ok],eye)
        d=np.maximum(d,1.0)
        ang=np.degrees(np.arctan2(h-eh,d))
        idx=np.where(ok)[0]
        best[idx]=np.maximum(best[idx],ang)
    return best
fig,ax=plt.subplots(figsize=(12,3.6),dpi=170)
cols={'1층 가로(전포대로변)':'#9AA3B2','옥상 광장(+21.1m)':NAVY}
res={}
for name,(eye,eh) in eyes.items():
    sk=skyline(eye,eh); res[name]=sk
    ax.fill_between(az,-6,np.maximum(sk,-6),color=cols[name],alpha=0.55 if '1층' in name else 0.85,step='mid',label=f'{name} 시선에서의 스카이라인',zorder=2 if '1층' in name else 3)
for k,((x,y),h) in lm.items():
    for name,(eye,eh) in eyes.items():
        dx,dy=x-eye.x,y-eye.y; d=math.hypot(dx,dy); a=(math.degrees(math.atan2(dx,dy))+360)%360
        top=math.degrees(math.atan2(h-GZ-eh,d)); sk=res[name][int(round(a/0.5))%720]
        vis='보임' if top>sk else '가려짐'
        print(f'{k} from {name}: az {a:.0f} dist {d:.0f} m top angle {top:.1f} deg, skyline there {sk:.1f} deg -> {vis}')
        if '옥상' in name:
            ax.plot([a,a],[math.degrees(math.atan2(-eh,d)),top],color=RED,lw=3,zorder=6)
            pos={'황령산 정상(427m)':(a-70,31.5),'BIFC(289m)':(a+14,22.5)}[k]
            ax.annotate(f'{k}\n방위 {a:.0f}° · {d/1000:.2f}km · 앙각 {top:.1f}°',xy=(a,top),xytext=pos,ha='left',va='center',fontsize=9,fontweight='bold',color=RED,arrowprops=dict(arrowstyle='-',color=RED),zorder=7,bbox=dict(fc='white',ec='none',alpha=0.85,pad=1.5))

ax.set_xlim(0,360); ax.set_ylim(-4,36)
ax.set_xticks([0,45,90,135,180,225,270,315,360]); ax.set_xticklabels(['N 0°','NE 45°','E 90°','SE 135°','S 180°','SW 225°','W 270°','NW 315°','N 360°'],fontsize=9)
ax.set_ylabel('앙각 (°)',fontsize=9); ax.grid(axis='x',color='#e5e5e5',lw=0.6,zorder=0); ax.axhline(0,color='black',lw=0.8,zorder=5)
for s in ('top','right'): ax.spines[s].set_visible(False)
ax.legend(loc='upper center',bbox_to_anchor=(0.5,-0.13),ncol=2,fontsize=8.5,frameon=False)
plt.savefig('fig/view_profile.png',facecolor='white',bbox_inches='tight',pad_inches=0.08); plt.close()
# summary: share of 360° open above 10 deg etc
for n,sk in res.items(): print(n,'open sector (<6 deg skyline) =',round(float((sk<6).mean()*360)),'deg; max',round(float(sk.max()),1),'; E sector 60-120 mean',round(float(sk[(az>=60)&(az<=120)].mean()),1))
