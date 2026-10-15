import json, os
R = os.path.join(os.environ['TEMP'], 'cloud_repo', 'jeongdonggwan', 'build', 'render') + os.sep
D = json.load(open(R + 'design.json', encoding='utf8'))
for i, p in enumerate(D['parts']):
    xs = [q[0] for q in p['pts']]; ys = [q[1] for q in p['pts']]
    print(i, p['mat'], 'z0', p['z0'], 'h', p['h'], 'x', round(min(xs), 1), round(max(xs), 1), 'y', round(min(ys), 1), round(max(ys), 1), len(p['pts']))
print('lane', [(round(x, 1), round(y, 1)) for x, y in D['lane'][0]])
for i in (0, ):
    print([(round(x, 1), round(y, 1)) for x, y in D['parts'][0]['pts']])
