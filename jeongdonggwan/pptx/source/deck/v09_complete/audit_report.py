import json, sys, itertools
d = json.load(open(sys.argv[1], encoding='utf8'))
by = {}
for r in d: by.setdefault(r['slide'], []).append(r)
issues = 0
YB = 6.80
for sl in sorted(by):
    rows = by[sl]
    for r in rows:
        if r['kind'] == 'table':
            if r['bottom'] > YB + 0.03 or r['right'] > 12.86:
                print(f"S{sl} TABLE {r['name']} bottom={r['bottom']} right={r['right']}"); issues += 1
        else:
            if r['over'] > 0.04 and r['wrap']:
                print(f"S{sl} OVERFLOW '{r['text']}' box={r['boxH']} text={r['textH']} (+{r['over']})"); issues += 1
            if r['right'] > 13.34 or r['bottom'] > 7.5:
                print(f"S{sl} OFFSLIDE '{r['text']}' right={r['right']} bottom={r['bottom']}"); issues += 1
    txt = [r for r in rows if r['kind'] == 'text']
    for a, b in itertools.combinations(txt, 2):
        ox = min(a['right'], b['right']) - max(a['bl'], b['bl'])
        oy = min(a['bottom'], b['bottom']) - max(a['bt'], b['bt'])
        if ox > 0.03 and oy > 0.03:
            print(f"S{sl} COLLIDE '{a['text']}' x '{b['text']}' ox={ox:.2f} oy={oy:.2f}"); issues += 1
print('issues:', issues)
