import re, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
d = open('../v6/deck.js', encoding='utf8').read()
sh = open('../v6/shian.js', encoding='utf8').read()

# 1. helpers + shared content from shian.js (without the 시안 tag helpers)
hs = sh.index("// ---------------------------------------------------------------- shared content")
he = sh.index("// =====================================================================  비교 안내 쪽")
helpers = sh[hs:he]
mkpos = helpers.index("let NUM = 0;\nfunction mk(")
mkend = helpers.index("function pill(")
helpers = helpers[:mkpos] + helpers[mkend:]
helpers = "const X0 = G.X0, W = G.W, SH = pres.shapes, GOLD = C.GOLD, NAVY = C.NAVY;\n" + helpers

# 2. the three blocks to borrow: shian pp.8 (C03), 9 (C04), 7 (B05)
idx = [m.start() for m in re.finditer(r"\n\{\n  const s = mk\(", sh)]
assert len(idx) == 9, len(idx)
end = sh.index("// ---------------------------------------------------------------- finish")
bounds = idx + [end]
blocks = [sh[bounds[i] + 1:bounds[i + 1]] for i in range(9)]
def conv(b):
    b = re.sub(r"const s = mk\('\d\d', ('[^']*'), ('[^']*'), (SRC\d), (NOTE\d), '[^']*'\);", r"const s = S(\1, \2, 0, \3, \4);", b)
    assert "mk(" not in b, b[:200]
    return b
c03, c04, b05 = conv(blocks[6]), conv(blocks[7]), conv(blocks[5])

# 3. swap in deck.js
a = d.index("// =====================================================================  01 사업 배경 Ⅰ")
b = d.index("// =====================================================================  02 대지 분석")
new_blocks = ("// =====================================================================  01 사업 배경 Ⅰ (시안 C · 도식형)\n" + c03 +
              "\n// =====================================================================  02 사업 배경 Ⅱ (시안 C · 도식형)\n" + c04 +
              "\n// =====================================================================  03 사업 배경 Ⅲ (시안 B · 숫자형)\n" + b05 + "\n")
d = d[:a] + new_blocks + d[b:]
# helpers go right after the S() wrapper
m = "const widthOf = (paras, w) => L.measure(paras, w);\n"
assert d.count(m) == 1
d = d.replace(m, m + "\n" + helpers + "\n")
open('deck.js', 'w', encoding='utf8').write(d)
print('v7 deck.js written', len(d))
