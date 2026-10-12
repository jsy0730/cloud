import math
from PIL import Image, ImageEnhance, ImageOps
S='/tmp/claude-0/-home-user-cloud/76ed2005-4113-58c6-b90f-f280afa8844d/scratchpad'
K=0.3225  # m per eum ref px (1:1200)
# eum ref-frame polygons (px), traced on the 1:1200 확인도면 centred on 207-29
REF=dict(
 W=[(222,-38),(312,-38),(312,0),(280,120),(250,200),(222,270)],
 R=[(312,-38),(330,-38),(330,0),(300,120),(265,220),(222,350),(222,270),(250,200),(280,120),(312,0)],
 E=[(330,-38),(354,-38),(354,357),(222,357),(222,350),(265,220),(300,120),(330,0)],
)
def ref2ll(x,y):
    lat=35.15778-(y+60)*K/111200; lon=129.06545+(x-182)*K/91060; return lat,lon
def ref2m(x,y): return ((x-222)*K,(357-y)*K)   # local metres: x east, y north, origin = SW corner of block
def ll2m(lat,lon):
    x0lat,x0lon=ref2ll(222,357)
    return ((lon-x0lon)*91060,(lat-x0lat)*111200)
POLY_LL={k:[ref2ll(*p) for p in v] for k,v in REF.items()}
POLY_M={k:[ref2m(*p) for p in v] for k,v in REF.items()}
class Map:
    def __init__(s,z,lat0,lon0,lat1,lon1):
        s.z=z; n=2**z
        def t(lat,lon): return ((lon+180)/360*n*256,(1-math.asinh(math.tan(math.radians(lat)))/math.pi)/2*n*256)
        s.t=t; X0,Y0=t(lat0,lon0); X1,Y1=t(lat1,lon1); s.X0,s.Y0=X0,Y0
        W,H=int(X1-X0),int(Y1-Y0); im=Image.new('RGB',(W,H),'white')
        for tx in range(int(X0//256),int(X1//256)+1):
            for ty in range(int(Y0//256),int(Y1//256)+1):
                try: tile=Image.open(S+'/osm/tiles/%d_%d_%d.png'%(z,tx,ty)).convert('RGB')
                except Exception: continue
                im.paste(tile,(int(tx*256-X0),int(ty*256-Y0)))
        s.im=im
    def px(s,lat,lon):
        X,Y=s.t(lat,lon); return (X-s.X0,Y-s.Y0)
    def faded(s,sat=0.25,bright=1.05,contrast=0.8):
        im=ImageEnhance.Color(s.im).enhance(sat); im=ImageEnhance.Contrast(im).enhance(contrast); return ImageEnhance.Brightness(im).enhance(bright)
