import json, os
R = os.path.join(os.environ['TEMP'], 'cloud_repo', 'jeongdonggwan', 'build', 'render') + os.sep
D = json.load(open(R + 'design.json', encoding='utf8'))
for i in (1, 2, 9):
    print(i, D['parts'][i]['mat'], [(round(x, 1), round(y, 1)) for x, y in D['parts'][i]['pts']])
print('block', [(round(x, 1), round(y, 1)) for x, y in D['block'][0]])
print('pit', [(round(x, 1), round(y, 1)) for x, y in D['pit'][0]])
