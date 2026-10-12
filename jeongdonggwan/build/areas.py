# 정동관 면적 모델 v3 (3m 이격, 뾰족한 끝 코어 2곳, 보조 피난계단 2곳)
import json, sys
sys.path.insert(0, '/tmp/claude-0/-home-user-cloud/76ed2005-4113-58c6-b90f-f280afa8844d/scratchpad/build')
from numbers_base import *
SITE = 4964.5
CORE_TIP = 45.0      # 끝 코어 1곳의 닫힌 부분(승강기 2대+전실), 층당
AUX = 30.0           # 보조 피난계단 1곳, 층당
bf = round(BF.area, 1); w1 = round(W1.area, 1); e1 = round(E1.area, 1)
F = {}
def fl(name, h, rows): F[name] = {'h': h, 'rows': rows}
# rows: (실, 면적, 분류)  분류: park/cult/biz/core/mep/sup
fl('6F', 8.0, [('체육·공연 가변홀', 1500, 'cult'), ('다목적·연습실', 700, 'cult'), ('공연 지원(분장·대기·창고)', 650, 'cult'), ('코어(끝 코어 2·보조 계단)', 150, 'core')])
fl('5F', 4.2, [('상인회·회의·공유오피스', 1200, 'biz'), ('주차(전환 가능 층)', round(bf - 1200 - 2 * AUX, 1), 'park'), ('코어', 150, 'core')])
for n in ('4F', '3F', '2F'):
    fl(n, 3.3, [('주차(구획·차로·반 층 램프)', round(bf - 2 * AUX, 1), 'park'), ('코어', 150, 'core')])
e_rest = round(e1 - (600 + 100 + 900 + 150 + 200 + AUX), 1)
w_rest = round(w1 - (400 + 400 + 300 + AUX), 1)
fl('1F', 7.0, [('서점', 400, 'biz'), ('카페', 400, 'biz'), ('공연 로비·매표', 300, 'cult'), ('근생 소점포(10곳 안팎)', 600, 'biz'),
               ('진입·진출 램프', 900, 'park'), ('정산·관리', 100, 'park'), ('이륜차·자전거 주차', 200, 'park'), ('하역·창고', 150, 'sup'),
               ('화장실·방재실·창고', round(e_rest + w_rest, 1), 'sup'), ('코어(끝 코어 2·보조 계단 2)', 2 * CORE_TIP + 2 * AUX, 'core')])
TIP2 = round(tW.area, 1)
b1 = round(SITE - TIP2, 1)
fl('B1', 4.5, [('공연장 로비·바(선큰 마당 접함)', 500, 'cult'), ('객석 상부·음향조정', 300, 'cult'), ('주차', round(b1 - 800 - 150, 1), 'park'), ('코어(특별피난계단 4)', 150, 'core')])
fl('B2', 4.5, [('공연장 200석(객석·무대)', 800, 'cult'), ('분장·창고', 300, 'cult'), ('주차', round(SITE - 1100 - 150, 1), 'park'), ('코어', 150, 'core')])
fl('B3', 3.3, [('전기·기계실', 300, 'mep'), ('주차', round(SITE - 300 - 150, 1), 'park'), ('코어', 150, 'core')])
fl('B4', 3.3, [('펌프·저수조', 600, 'mep'), ('주차', round(SITE - 600 - 150, 1), 'park'), ('코어', 150, 'core')])
tot = {k: round(sum(r[1] for r in v['rows']), 1) for k, v in F.items()}
above = round(sum(tot[k] for k in ('1F', '2F', '3F', '4F', '5F', '6F')), 1)
below = round(sum(tot[k] for k in ('B1', 'B2', 'B3', 'B4')), 1)
gfa = round(above + below, 1)
cat = {}
for v in F.values():
    for r in v['rows']: cat[r[2]] = round(cat.get(r[2], 0) + r[1], 1)
ba = round(bf + 2 * CORE_TIP, 1)
roof_terrace = round(bf - (3000 - 2 * CORE_TIP - 2 * AUX), 1)
out = dict(site=SITE, bf=bf, w1=w1, e1=e1, lane=round(L1.area, 1), tip1=round(tE.area, 1), tip2=TIP2, ba=ba, bcr=round(ba / SITE * 100, 1),
           floors=F, tot=tot, above=above, below=below, gfa=gfa, far=round(above / SITE * 100, 1), cat=cat,
           park_ratio=round(cat['park'] / gfa * 100, 2), roof_terrace=roof_terrace, height=29.1, depth=15.6)
json.dump(out, open('areas.json', 'w'), ensure_ascii=False, indent=1)
for k in ('6F', '5F', '4F', '3F', '2F', '1F', 'B1', 'B2', 'B3', 'B4'): print(k, tot[k], F[k]['rows'])
print({k: out[k] for k in ('bf', 'w1', 'e1', 'lane', 'tip1', 'tip2', 'ba', 'bcr', 'above', 'below', 'gfa', 'far', 'park_ratio', 'roof_terrace')})
print(cat, {k: round(v / gfa * 100, 2) for k, v in cat.items()})
