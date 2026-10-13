import sys; sys.path.insert(0,'.')
from env_common import *
DATES={'동지 12/21':(2026,12,21),'춘·추분 3/21':(2026,3,21),'하지 6/21':(2026,6,21)}
COL={'동지 12/21':'#1F4E9C','춘·추분 3/21':'#6A994E','하지 6/21':'#E07A00'}
fig,ax=plt.subplots(figsize=(7.2,3.7),dpi=170)
for nm,d in DATES.items():
    ts=np.arange(5,20.01,0.1); A=[];E=[]
    for t in ts:
        a,e=sunpos(*d,int(t),int(round((t%1)*60)))
        if e>0: A.append(a);E.append(e)
    ax.plot(A,E,color=COL[nm],lw=2.2,label=nm)
    for h in range(7,19):
        a,e=sunpos(*d,h)
        if e>0:
            ax.plot(a,e,'o',color=COL[nm],ms=3.5)
            if nm.startswith('동지') or nm.startswith('하지'):
                ax.text(a,e+(2.5 if nm.startswith('하지') else -5.5),f'{h}',fontsize=6.5,ha='center',color=COL[nm])
ax.axvspan(247,293,color='#C8102E',alpha=0.10)  # west facade ~ 서향 low sun
ax.text(270,84,'서향 일사\n(전포대로 면)',ha='center',va='top',fontsize=8,color='#C8102E')
for x,l in ((90,'E'),(180,'S'),(270,'W')): ax.axvline(x,color='#999',lw=0.6,ls=':')
ax.set_xlim(55,305); ax.set_ylim(0,85)
ax.set_xticks([60,90,120,150,180,210,240,270,300]); ax.set_xticklabels(['60°','E 90°','120°','150°','S 180°','210°','240°','W 270°','300°'],fontsize=8)
ax.set_ylabel('태양 고도 (°)',fontsize=9); ax.legend(loc='lower center',ncol=3,fontsize=8.5,frameon=False)
for s in ('top','right'): ax.spines[s].set_visible(False)
ax.grid(color='#eee',lw=0.6)
plt.savefig('fig/sunpath.png',facecolor='white',bbox_inches='tight',pad_inches=0.06); plt.close()
# direct-sun hours per facade orientation
print('facade  ',list(DATES))
for fn,nb in (('북',0),('동',90),('남',180),('서',270)):
    row=[]
    for nm,d in DATES.items():
        n=0
        for m in range(0,24*60,6):
            a,e=sunpos(*d,m//60,m%60)
            if e>0 and abs((a-nb+180)%360-180)<90-1e-9 and e>=5: n+=1
        row.append(round(n*0.1,1))
    print(fn,row)
for nm,d in DATES.items():
    a,e=sunpos(*d,12); print(nm,'noon',round(a),round(e,1), 'rise/set approx', [ (h,round(sunpos(*d,h)[0]),round(sunpos(*d,h)[1],1)) for h in (6,7,17,18)])
