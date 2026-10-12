import sys,math,json; sys.path.insert(0,'.')
from geo import *
from PIL import ImageDraw, ImageFilter
SITE_C=(35.15715,129.06578)
def poly_layer(m,im,alpha=1.0,outline=True):
    ov=Image.new('RGBA',im.size,(0,0,0,0)); d=ImageDraw.Draw(ov)
    d.polygon([m.px(*p) for p in POLY_LL['W']],fill=(232,213,160,int(235*alpha)),outline=(31,34,36,255))
    d.polygon([m.px(*p) for p in POLY_LL['E']],fill=(124,142,150,int(235*alpha)),outline=(31,34,36,255))
    if outline:
        for k in 'WE': d.line([m.px(*p) for p in POLY_LL[k]+[POLY_LL[k][0]]],fill=(31,34,36,255),width=3)
    return ov
def dest(lat,lon,brg,dist):
    return lat+dist*math.cos(math.radians(brg))/111200, lon+dist*math.sin(math.radians(brg))/91060
out={}
# ---------- environment map ----------
m=Map(17,35.1612,129.0600,35.1530,129.0712)
im=m.faded(sat=0.0,bright=1.08,contrast=0.55).convert('RGBA')
ov=Image.new('RGBA',im.size,(0,0,0,0)); d=ImageDraw.Draw(ov)
# 3종일반주거지역 (approx: east of lon 129.06659 within view)
x3,_=m.px(SITE_C[0],129.06659)
for i in range(-im.height,im.width,14): d.line([(x3+i,0),(x3+i+im.height,im.height)],fill=(107,114,118,60),width=2)
d.rectangle([0,0,x3,im.height],fill=(244,245,244,0))
ov2=Image.new('RGBA',im.size,(0,0,0,0)); ov2.paste(ov.crop((int(x3),0,im.width,im.height)),(int(x3),0)); ov=ov2; d=ImageDraw.Draw(ov)
d.line([(x3,0),(x3,im.height)],fill=(107,114,118,200),width=2)
# noise sources: 전포대로 & 서전로 bands
for (a,b) in [((35.1612,129.06545),(35.1530,129.06545)),((35.15778,129.0600),(35.15778,129.0712))]:
    d.line([m.px(*a),m.px(*b)],fill=(181,82,59,90),width=26 if a[1]==b[1] else 18)
# sun path rays from site centre: 동지 (8~17h) and 하지 (7~19h) azimuth extremes, plus 남중
cx,cy=m.px(*SITE_C)
def ray(az,L,col,w,dash=False):
    x2=cx+L*math.sin(math.radians(az)); y2=cy-L*math.cos(math.radians(az))
    if not dash: d.line([(cx,cy),(x2,y2)],fill=col,width=w)
    else:
        n=int(L/16)
        for i in range(n):
            if i%2==0: d.line([(cx+(x2-cx)*i/n,cy+(y2-cy)*i/n),(cx+(x2-cx)*(i+1)/n,cy+(y2-cy)*(i+1)/n)],fill=col,width=w)
    return (x2,y2)
R=330
# winter sun sector 123°→239° , summer 62°(sunrise ~ 60) → 298°
def arc(r,a0,a1,col,w):
    pts=[(cx+r*math.sin(math.radians(a)),cy-r*math.cos(math.radians(a))) for a in [a0+(a1-a0)*i/60 for i in range(61)]]
    d.line(pts,fill=col,width=w)
arc(R,62,298,(232,190,90,230),6); arc(R*0.78,118,242,(181,130,40,230),6)
for az in (62,298): ray(az,R,(232,190,90,200),2,True)
for az in (118,242): ray(az,R*0.78,(181,130,40,200),2,True)
ray(180,R*0.95,(181,130,40,255),3)
out['sun']={'summer_rise':(cx+R*math.sin(math.radians(62)),cy-R*math.cos(math.radians(62))),'summer_set':(cx+R*math.sin(math.radians(298)),cy-R*math.cos(math.radians(298))),
            'winter_rise':(cx+R*.78*math.sin(math.radians(118)),cy-R*.78*math.cos(math.radians(118))),'winter_set':(cx+R*.78*math.sin(math.radians(242)),cy-R*.78*math.cos(math.radians(242))),'noon':(cx,cy+R*0.95)}
# tall buildings markers (OSM levels)
tall=[('30F',35.1568,129.0690),('25F',35.15841,129.06580),('22F',35.15733,129.06495)]
osm_pts=[]
import xml.etree.ElementTree as ET
t=ET.parse(S+'/osm/map.osm').getroot()
nodes={n.get('id'):(float(n.get('lat')),float(n.get('lon'))) for n in t.iter('node')}
for w in t.iter('way'):
    tg={x.get('k'):x.get('v') for x in w.iter('tag')}
    lv=tg.get('building:levels')
    if 'building' in tg and lv and lv.isdigit() and int(lv)>=15:
        pts=[nodes[n.get('ref')] for n in w.iter('nd') if n.get('ref') in nodes]
        d.polygon([m.px(*p) for p in pts],fill=(31,34,36,200))
        la=sum(p[0] for p in pts)/len(pts); lo=sum(p[1] for p in pts)/len(pts)
        osm_pts.append((int(lv),m.px(la,lo)))
out['tall']=osm_pts
im=Image.alpha_composite(im,ov); im=Image.alpha_composite(im,poly_layer(m,im))
# view rays (to edge)
d=ImageDraw.Draw(im)
views={'황령산':90,'BIFC':178,'서면 도심':262,'시민공원':318}
vend={}
for k,az in views.items():
    L=420 if k!='BIFC' else 300
    p=ray(az,L,(31,34,36,255),3,True); vend[k]=p
out['view']=vend
out['site']=(cx,cy); out['size']=im.size
im.convert('RGB').save('env_map.png')
# ---------- transit map ----------
m2=Map(17,35.1612,129.0575,35.1515,129.0705)
im2=m2.faded(sat=0.35,bright=1.03,contrast=0.75).convert('RGBA')
im2=Image.alpha_composite(im2,poly_layer(m2,im2))
d=ImageDraw.Draw(im2)
st={'jp8':(35.1541640,129.0656214),'jp':(35.1528166,129.0653430),'sm':(35.1581948,129.0594510),'sm10':(35.15790,129.06025)}
sc=m2.px(*SITE_C)
for k in ('jp8','sm10'):
    p=m2.px(*st[k]); 
    n=40
    for i in range(n):
        if i%2==0: d.line([(sc[0]+(p[0]-sc[0])*i/n,sc[1]+(p[1]-sc[1])*i/n),(sc[0]+(p[0]-sc[0])*(i+1)/n,sc[1]+(p[1]-sc[1])*(i+1)/n)],fill=(31,34,36,255),width=4)
out['t']={k:m2.px(*v) for k,v in st.items()}; out['t_site']=sc; out['t_size']=im2.size
# bus stops (BIMS names from original deck; positions approximate around 전포사거리)
bus={'8':(35.15745,129.06528),'9':(35.15805,129.06562),'7':(35.15810,129.06620),'6':(35.15765,129.06300)}
out['bus']={k:m2.px(*v) for k,v in bus.items()}
im2.convert('RGB').save('transit_map.png')
json.dump(out,open('maps.json','w'))
print(out['size'],out['t_size'])
