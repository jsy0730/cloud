import sys; sys.path.insert(0,'/tmp/claude-0/-home-user-cloud/76ed2005-4113-58c6-b90f-f280afa8844d/scratchpad/build')
from geo import POLY_M
from shapely.geometry import Polygon, box
from shapely.affinity import scale
from shapely.ops import unary_union
W,R,E=(Polygon(POLY_M[k]) for k in 'WRE'); B=unary_union([W,R,E]).buffer(0.01).buffer(-0.01); k=(4964.5/B.area)**0.5
W,R,E,B=(scale(g,k,k,origin=(0,0)) for g in (W,R,E,B))
H=B.bounds[3]
tE=E.intersection(box(-10,85,80,200)); tW=W.intersection(box(-10,-10,80,55))
SB=box(-10,3,80,H-3)
BF=B.intersection(SB).difference(tE).difference(tW)
W1=W.intersection(SB).difference(tW); E1=E.intersection(SB).difference(tE); L1=R.intersection(SB)
def polys(g):
    if g.is_empty: return []
    if g.geom_type=='Polygon': return [g]
    return [p for p in getattr(g,'geoms',[]) if p.geom_type=='Polygon']
def rows(w):
    if w>=32.6: return 4
    if w>=21.5: return 3
    if w>=16.2: return 2
    if w>=11.2: return 1
    return 0
def count(g,step=2.55):
    n=0; y=g.bounds[1]
    while y<g.bounds[3]:
        for p in polys(g.intersection(box(-10,y,80,y+step))):
            n+=rows(p.area/step)
        y+=step
    return n
