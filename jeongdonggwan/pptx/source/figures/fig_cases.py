import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, FancyArrowPatch
plt.rcParams['font.family']='Malgun Gothic'; plt.rcParams['axes.unicode_minus']=False
NAVY='#002060'; RED='#C8102E'; GRAY='#8a8f98'; LG='#E4E7EC'
# ---- 1111 Lincoln Road: open slab section with varying floor heights (7 ft ~ 34 ft per sources)
fig,ax=plt.subplots(figsize=(6,3.6),dpi=200)
levels=[0,3.2,6.4,10.4,13.6,17.0,27.4]   # schematic: heights are illustrative, ratio 2.1m..10.4m
labels=['지상층: 상업·카페(높은 층고)','','','','','','']
y=0; heights=[5.0,2.1,2.1,2.1,3.0,2.1,10.4]   # schematic stacking
tops=[]
for i,h in enumerate(heights):
    ax.add_patch(Rectangle((0,y),12,0.45,fc=NAVY,ec='none'))   # slab
    tops.append(y); y+=0.45+h
ax.add_patch(Rectangle((0,y),12,0.45,fc=NAVY,ec='none'))
for x in (1,4.2,7.4,10.6):
    ax.add_patch(Polygon([[x,0],[x+0.5,0],[x+0.8,y+0.45],[x+0.3,y+0.45]],fc='#9AA3B2',ec='none',alpha=0.8))
def dim(y0,y1,txt,xx=12.8,col=RED):
    ax.annotate('',xy=(xx,y1),xytext=(xx,y0),arrowprops=dict(arrowstyle='<->',color=col,lw=1.1))
    ax.text(xx+0.25,(y0+y1)/2,txt,va='center',fontsize=8.5,color=col)
dim(tops[1]+0.45,tops[2],'최소 약 2.1m\n(주차 기준 7ft)')
dim(tops[6]+0.45,y,'최대 약 10.4m\n(34ft, 행사·상업)')
dim(0.45,tops[1],'지상 상업층')
ax.text(6,y+1.2,'기둥·슬래브·램프만으로 이룬 개방 구조 — 외벽 없음',ha='center',fontsize=9.5,color=NAVY,fontweight='bold')
ax.text(6,-2.6,'분석 다이어그램 · 층고 변화(개념, 축척 없음) · 수치 출처: 건축 매체 보도',ha='center',fontsize=8,color=GRAY)
ax.set_xlim(-0.5,17); ax.set_ylim(-3.2,y+2.4); ax.axis('off')
plt.savefig('assets/diag_lincoln.png',bbox_inches='tight',facecolor='white'); plt.close()
# ---- JS tower: skip floor concept (west plate / east plate offset half level)
fig,ax=plt.subplots(figsize=(6,3.6),dpi=200)
H=3.3
for i in range(4):
    ax.add_patch(Rectangle((0,i*H*2),6,0.35,fc=NAVY,ec='none'))            # plate A (full levels)
    ax.add_patch(Rectangle((6.8,i*H*2+H),6,0.35,fc='#4272C4',ec='none'))   # plate B offset by half level
    ax.add_patch(Polygon([[6,i*H*2],[6.8,i*H*2+H],[6.8,i*H*2+H+0.35],[6,i*H*2+0.35]],fc=RED,ec='none',alpha=0.85))  # short ramp
    if i<3: ax.add_patch(Polygon([[6.8,i*H*2+H],[6,i*H*2+2*H],[6,i*H*2+2*H+0.35],[6.8,i*H*2+H+0.35]],fc=RED,ec='none',alpha=0.85))
ax.text(3,-2.2,'A판 · 전층 높이',ha='center',fontsize=9,color=NAVY,fontweight='bold')
ax.text(9.8,-2.2,'B판 · 반 층 엇갈림',ha='center',fontsize=9,color='#4272C4',fontweight='bold')
ax.text(6.4,4*H*2+1.2,'램프 = 반 층 높이만 오르내림 → 길이·면적 감소',ha='center',fontsize=9.5,color=RED,fontweight='bold')
ax.text(6.4,-3.9,'분석 다이어그램 · 스킵플로어 개념(층고·치수 개략)',ha='center',fontsize=8,color=GRAY)
ax.set_xlim(-0.5,13.5); ax.set_ylim(-4.5,4*H*2+2.4); ax.axis('off')
plt.savefig('assets/diag_skip.png',bbox_inches='tight',facecolor='white'); plt.close()
