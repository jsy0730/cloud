import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
s = open('build_scene3.py', encoding='utf8').read()
def rep(a, b):
    global s
    assert s.count(a) == 1, a[:60]
    s = s.replace(a, b)
rep("M['wood'] = [wood_board_mat('wood0', (1.95, 1.5, 1.05)), wood_board_mat('wood1', (1.55, 1.2, 0.86)), wood_board_mat('wood2', (2.35, 1.85, 1.3))]",
    "M['wood'] = [wood_board_mat('wood0', (1.55, 1.5, 1.2)), wood_board_mat('wood1', (1.25, 1.22, 1.0)), wood_board_mat('wood2', (1.95, 1.85, 1.5))]")
rep("box('curb', (0.22, 127.4, SW_H + 0.03), (-SW_W - 0.11, 63.7, (SW_H + 0.03) / 2), (0, 0, 0), M['concrete'])",
    "box('curb', (0.22, 127.4, SW_H + 0.03), (-SW_W - 0.11, 63.7, (SW_H + 0.03) / 2), (0, 0, 0), simple_mat('curbmat', (0.62, 0.62, 0.6), rough=0.8))")
rep("emit_str=(14.0 if LIT else 5.0)", "emit_str=(9.0 if LIT else 2.2)")
rep("tint=(1.9, 1.85, 1.78, 1))", "tint=(2.3, 2.25, 2.15, 1))")
open('build_scene3.py', 'w', encoding='utf8').write(s)
print('ok')
