import json, os, math
R = os.path.join(os.environ['TEMP'], 'cloud_repo', 'jeongdonggwan', 'build', 'render') + os.sep
C = json.load(open(R + 'context.json', encoding='utf8'))
D = json.load(open(R + 'design.json', encoding='utf8'))
print(C.keys(), C['center'])
for r in C['roads']:
    xs=[p[0] for p in r['pts']]; ys=[p[1] for p in r['pts']]
    if max(xs) > -60 and min(xs) < 60 and max(ys) > -60 and min(ys) < 150:
        print(r.get('name'), r.get('hw'), r['w'], [(round(x,1),round(y,1)) for x,y in r['pts']][:8])
print('block', [(round(x,1),round(y,1)) for x,y in D['block'][0]])
print('lane', [[(round(x,1),round(y,1)) for x,y in p] for p in D['lane']])
print('tips', [[(round(x,1),round(y,1)) for x,y in p] for p in D['tips']])
print('pit', [[(round(x,1),round(y,1)) for x,y in p] for p in D['pit']])
for p in D['parts']:
    if p['mat']=='slab': print('slab', p['z0'], p['h'], len(p['pts']))
