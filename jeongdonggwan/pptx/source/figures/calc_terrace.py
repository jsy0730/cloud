import sys; sys.path.insert(0,'.')
from env_common import *
import shapely
WIN=(2026,12,21); SUM=(2026,6,21); EQ=(2026,3,21)
ctx=[(Polygon(b['pts']).buffer(0),b['h']) for b in CTX['buildings'] if b['h']>=12]
def ctx_shadow(az,el):
    s=[shadow(p,h,az,el) for p,h in ctx]
    s=[x for x in s if x is not None and not x.is_empty]
    return unary_union(s) if s else None
# sample points on the terrace (roof plaza 21.1 m)
minx,miny,maxx,maxy=TERR.bounds
pts=[(x,y) for x in np.arange(minx,maxx,2.0) for y in np.arange(miny,maxy,2.0) if TERR.contains(Point(x,y))]
P=shapely.points(np.array(pts))
for nm,d in (('동지',WIN),('춘분',EQ),('하지',SUM)):
    sun=np.zeros(len(pts)); tot=0
    for t in np.arange(9,15.01,0.5):
        az,el=sunpos(*d,int(t),int(round((t%1)*60)))
        if el<=0: continue
        tot+=0.5
        # shadows on the 21.1 m roof level: own tall parts (hall, core TE) + context taller than 21.1
        own=[shadow(q,h-21.1,az,el) for g,h in ((HALL,29.8),(TE,29.8)) for q in polys(g)]
        c=[shadow(p,h-21.1,az,el) for p,h in ctx if h>21.1]
        allsh=unary_union([x for x in own+c if x is not None and not x.is_empty])
        sun+=~shapely.contains_xy(allsh,np.array([p[0] for p in pts]),np.array([p[1] for p in pts]))*0.5
    print(nm,'09-15h terrace direct sun hours: mean',round(float(sun.mean()),1),'min',round(float(sun.min()),1),'max',round(float(sun.max()),1),'of',tot)
# east residential strip shading incl. context buildings? (own building only)
