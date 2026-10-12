# isometric massing of 停棟(east) and 動棟(west) on the merged block
import sys; sys.path.insert(0,'.')
from geo import *
from shapely.geometry import Polygon, box as sbox
from PIL import ImageDraw
def scaled(k,actual):
    p=Polygon(POLY_M[k]); s=(actual/p.area)**0.5
    return Polygon([(x*s,y*s) for x,y in p.exterior.coords])
WEST=Polygon(POLY_M['W']); EAST=Polygon(POLY_M['E'])
WB=WEST.buffer(-3,join_style=2); EB=EAST.buffer(-3,join_style=2)
# trim east buildable north tip (too narrow for parking): keep y<=95m
EBT=EB.intersection(sbox(-10,-10,60,95))
COL={'park':(58,63,66),'park2':(31,34,36),'biz':(232,213,160),'cult':(124,142,150),'core':(180,185,187),'roof':(227,229,228),'site':(214,217,216)}
def iso(x,y,z,sc=7.2,ox=0,oy=0):
    # view from SW: rotate so we see west+south faces
    a=math.radians(30)
    X=(x - y)*math.cos(a)*sc; Y=-(x + y)*math.sin(a)*sc - z*sc
    return (X+ox,Y+oy)
def draw(path, W_stack, E_stack, size=(1600,1150), sc=7.6):
    blds=W_stack if isinstance(W_stack,list) and W_stack and isinstance(W_stack[0][1],Polygon) else [('E',EBT,E_stack),('W',WB,W_stack)]
    # bounds
    xs=[];ys=[]
    for poly in (Polygon(POLY_M['W']),Polygon(POLY_M['E'])):
        for x,y in poly.exterior.coords:
            for z in (0,22):
                X,Y=iso(x,y,z,sc=sc); xs.append(X); ys.append(Y)
    ox=(size[0]-(max(xs)-min(xs)))/2-min(xs); oy=(size[1]-(max(ys)-min(ys)))/2-min(ys)
    P=lambda x,y,z: iso(x,y,z,sc=sc,ox=ox,oy=oy)
    im=Image.new('RGBA',size,(244,245,244,0)); d=ImageDraw.Draw(im)
    for poly,col in ((Polygon(POLY_M['W']),COL['site']),(Polygon(POLY_M['E']),COL['site']),(Polygon(POLY_M['R']),(200,204,203))):
        d.polygon([P(x,y,0) for x,y in poly.exterior.coords],fill=col+(255,),outline=(107,114,118,255))
    blds.sort(key=lambda b:-(b[1].centroid.x+b[1].centroid.y))
    for nm,fp,stack in blds:
        z=0
        for h,parts in stack:
            # draw parts far-to-near
            geoms=[]
            for col,cut in parts:
                g=fp if cut is None else fp.intersection(cut)
                if g.is_empty: continue
                for pg in ([g] if g.geom_type=='Polygon' else [q for q in g.geoms if q.geom_type=='Polygon']):
                    geoms.append((pg,col))
            geoms.sort(key=lambda t:-(t[0].centroid.x+t[0].centroid.y))
            for pg,col in geoms:
                pg=pg.buffer(0)
                pts=list(pg.exterior.coords)[:-1]
                ccw=pg.exterior.is_ccw
                faces=[]
                for i in range(len(pts)):
                    (x1,y1),(x2,y2)=pts[i],pts[(i+1)%len(pts)]
                    nx,ny=(y2-y1),-(x2-x1)
                    if not ccw: nx,ny=-nx,-ny
                    L=math.hypot(nx,ny) or 1
                    if (-nx-ny)/L>0.02: faces.append(((x1,y1),(x2,y2),nx/L,ny/L))
                faces.sort(key=lambda f:-(f[0][0]+f[0][1]+f[1][0]+f[1][1]))
                c=COL[col]
                for (x1,y1),(x2,y2),nx,ny in faces:
                    shade=0.86 if abs(nx)>abs(ny) else 0.70
                    cc=tuple(int(v*shade) for v in c)
                    d.polygon([P(x1,y1,z),P(x2,y2,z),P(x2,y2,z+h),P(x1,y1,z+h)],fill=cc+(255,),outline=(31,34,36,255))
                d.polygon([P(x,y,z+h) for x,y in pts],fill=c+(255,),outline=(31,34,36,255))
            z+=h
    im.save(path)
    return P

from shapely.ops import unary_union
BLOCK=unary_union([Polygon(POLY_M['W']),Polygon(POLY_M['R']),Polygon(POLY_M['E'])]).buffer(0.01).buffer(-0.01)
W1=Polygon(POLY_M['W']); E1=Polygon(POLY_M['E'])
def cut_y(g,y0,y1): return g.intersection(sbox(-20,y0,80,y1))
# 6F hall footprint: northern part of block (~3,400 of 4,964 real) -> drawn proportion
def y_for_share(g,share):
    lo,hi=0,130
    for _ in range(40):
        mid=(lo+hi)/2
        if cut_y(g,mid,200).area/g.area>share: lo=mid
        else: hi=mid
    return (lo+hi)/2
Y6=y_for_share(BLOCK,3400/4964.5)
def massing(path):
    # one combined stack drawn as single 'building' list ordered bottom-up, parts per level
    levels=[(7.0,[('biz',W1),('park',cut_y(E1,14,200)),('biz',cut_y(E1,-5,14))]),
            (3.3,[('park2',BLOCK)]),(3.3,[('park',BLOCK)]),(3.3,[('park2',BLOCK)]),
            (4.2,[('park',cut_y(BLOCK,-5,70)),('biz',cut_y(BLOCK,70,200))]),
            (8.0,[('cult',cut_y(BLOCK,Y6,200))]),(0.8,[('roof',cut_y(BLOCK,Y6,200))])]
    return draw_levels(path,levels)
def draw_levels(path,levels,size=(1600,1200),sc=7.4):
    xs=[];ys=[]
    for x,y in BLOCK.exterior.coords:
        for z in (0,32):
            X,Y=iso(x,y,z,sc=sc); xs.append(X); ys.append(Y)
    ox=(size[0]-(max(xs)-min(xs)))/2-min(xs); oy=(size[1]-(max(ys)-min(ys)))/2-min(ys)
    P=lambda x,y,z: iso(x,y,z,sc=sc,ox=ox,oy=oy)
    im=Image.new('RGBA',size,(244,245,244,0)); d=ImageDraw.Draw(im)
    for poly,col in ((BLOCK,COL['site']),(Polygon(POLY_M['R']),(196,200,199))):
        d.polygon([P(x,y,0) for x,y in poly.exterior.coords],fill=col+(255,),outline=(107,114,118,255))
    z=0; anchors=[]
    for h,parts in levels:
        geoms=[]
        for col,g in parts:
            g=g.buffer(0)
            if g.is_empty: continue
            for pg in ([g] if g.geom_type=='Polygon' else [q for q in g.geoms if q.geom_type=='Polygon']):
                if pg.area>1: geoms.append((pg,col))
        geoms.sort(key=lambda t:-(t[0].centroid.x+t[0].centroid.y))
        for pg,col in geoms:
            pts=list(pg.exterior.coords)[:-1]; ccw=pg.exterior.is_ccw; faces=[]
            for i in range(len(pts)):
                (x1,y1),(x2,y2)=pts[i],pts[(i+1)%len(pts)]
                nx,ny=(y2-y1),-(x2-x1)
                if not ccw: nx,ny=-nx,-ny
                L=math.hypot(nx,ny) or 1
                if (-nx-ny)/L>0.02: faces.append(((x1,y1),(x2,y2),nx/L,ny/L))
            faces.sort(key=lambda f:-(f[0][0]+f[0][1]+f[1][0]+f[1][1]))
            c=COL[col]
            for (x1,y1),(x2,y2),nx,ny in faces:
                shade=0.86 if abs(nx)>abs(ny) else 0.70
                cc=tuple(int(v*shade) for v in c)
                d.polygon([P(x1,y1,z),P(x2,y2,z),P(x2,y2,z+h),P(x1,y1,z+h)],fill=cc+(255,),outline=(31,34,36,255))
            d.polygon([P(x,y,z+h) for x,y in pts],fill=c+(255,),outline=(31,34,36,255))
        anchors.append((z,h)); z+=h
    im.save(path)
    return P,anchors
if __name__=='__main__':
    P,an=massing('iso.png'); print('Y6',Y6, BLOCK.area)
