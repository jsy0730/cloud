import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
s = open('build_scene3.py', encoding='utf8').read()
def rep(a, b):
    global s
    assert s.count(a) == 1, a[:60]
    s = s.replace(a, b)
rep("    for yy_ in (18.0, 72.0, 94.0, 114.0):\n        D.setdefault('trees', [])\n        D['trees'].append([-2.3, yy_, SW_H, 1.15])",
    "    D['trees'] = [t for t in D.get('trees', []) if t[2] > 1.0]       # keep roof trees only\n"
    "    for yy_ in (18.0, 72.0, 94.0, 114.0):\n        D['trees'].append([-2.3, yy_, SW_H, 1.15])\n"
    "    D['cars'] = []; D['walks'] = []")
open('build_scene3.py', 'w', encoding='utf8').write(s)
print('ok')
