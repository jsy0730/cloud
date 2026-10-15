import json, os
R = os.path.join(os.environ['TEMP'], 'cloud_repo', 'jeongdonggwan', 'build', 'render') + os.sep
D = json.load(open(R + 'design.json', encoding='utf8'))
print(list(D.keys()))
from collections import Counter
print(Counter(p['mat'] for p in D['parts']))
for p in D['parts']:
    if p['mat'] in ('screen', 'base'):
        xs = [q[0] for q in p['pts']]; ys = [q[1] for q in p['pts']]
        print('screen z0', p['z0'], 'h', p['h'], 'bbox', round(min(xs), 1), round(max(xs), 1), round(min(ys), 1), round(max(ys), 1), 'inner' in p, len(p['pts']))
print('stairs', D.get('stairs'))
print('walks', len(D.get('walks', [])), 'trees', D.get('trees'))
V = json.load(open(R + 'views4.json', encoding='utf8'))
print(json.dumps(V.get('hero_sw'), ensure_ascii=False))
print(list(V.keys()))
