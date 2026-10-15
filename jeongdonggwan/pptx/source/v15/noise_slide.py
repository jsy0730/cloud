"""v15: 07 소음 쪽 — 가운데 '소음 크기 비교' 보강, 오른쪽을 '소음원과 대응' 표로. usage: python3 -I noise_slide.py <unpacked>"""
import sys, os, re, copy
from lxml import etree
U = sys.argv[1]
NS = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main",
      "p": "http://schemas.openxmlformats.org/presentationml/2006/main"}
A = "{%s}" % NS["a"]; P = "{%s}" % NS["p"]
E = 914400
f = os.path.join(U, "ppt/slides/slide9.xml")
tree = etree.parse(f); root = tree.getroot()
spTree = root.find("p:cSld/p:spTree", NS)

def by_name(n):
    for el in spTree:
        c = el.find(".//p:cNvPr", NS)
        if c is not None and c.get("name") == n: return el
    raise KeyError(n)
ids = [int(c.get("id")) for c in root.iter(P + "cNvPr")]
nid = [max(ids)]
def new_id(el, prefix):
    nid[0] += 1
    c = el.find(".//p:cNvPr", NS); c.set("id", str(nid[0])); c.set("name", f"{prefix} {nid[0]-1}")
    return el
def place(el, x, y, w, h):
    off = el.find(".//a:off", NS); ext = el.find(".//a:ext", NS)
    off.set("x", str(int(x * E))); off.set("y", str(int(y * E))); ext.set("cx", str(int(w * E))); ext.set("cy", str(int(h * E)))
    return el
def set_text(el, text):
    ts = list(el.iter(A + "t")); ts[0].text = text
    for t in ts[1:]:
        r = t.getparent(); r.getparent().remove(r)
    return el

RPR = ('<a:rPr xmlns:a="%s" lang="ko-KR" altLang="en-US" sz="{sz}"{b} dirty="0"><a:solidFill><a:srgbClr val="{c}"/></a:solidFill>'
       '<a:latin typeface="Malgun Gothic" pitchFamily="34" charset="0"/><a:ea typeface="Malgun Gothic" pitchFamily="34" charset="-122"/>'
       '<a:cs typeface="Malgun Gothic" pitchFamily="34" charset="-120"/></a:rPr>') % NS["a"]
def para(text, sz, bold=False, color="000000", algn="l"):
    p = etree.SubElement(etree.Element(A + "dummy"), A + "p")
    ppr = etree.SubElement(p, A + "pPr", marL="0", indent="0", algn=algn); etree.SubElement(ppr, A + "buNone")
    r = etree.SubElement(p, A + "r")
    r.append(etree.fromstring(RPR.format(sz=int(sz * 100), b=' b="1"' if bold else "", c=color)))
    etree.SubElement(r, A + "t").text = text
    return p
def textbox(x, y, w, h, paras, anchor="t"):
    el = copy.deepcopy(by_name("TextBox 20"))
    new_id(el, "TextBox"); place(el, x, y, w, h)
    tb = el.find("p:txBody", NS); tb.find("a:bodyPr", NS).set("anchor", anchor)
    for p in tb.findall("a:p", NS): tb.remove(p)
    for p in paras: tb.append(p)
    return el
def rect(x, y, w, h, color, line=False):
    el = copy.deepcopy(by_name("직사각형 19")); new_id(el, "직사각형"); place(el, x, y, w, h)
    el.find(".//a:srgbClr", NS).set("val", color)
    return el

# ---- 오른쪽 기존 패널 제거, 아래 캡션 제거
for n in ["직사각형 28", "TextBox 29", "TextBox 30", "TextBox 31", "직사각형 32", "TextBox 33", "TextBox 34", "TextBox 35", "TextBox 36", "TextBox 24"]:
    spTree.remove(by_name(n))
set_text(by_name("TextBox 27"), "소음원과 대응")

# ---- 가운데: 막대그래프 높이 줄이기
chart = by_name("차트 25")
chart.find("p:xfrm/a:ext", NS).set("cy", str(int(1.72 * E)))

add = []
X0, X1 = 4.80, 8.53                      # 40 dB, 90 dB
dbx = lambda d: X0 + (d - 40) / 50 * (X1 - X0)
add.append(rect(4.72, 5.53, 0.055, 0.185, "002060"))
add.append(textbox(4.87, 5.50, 3.75, 0.23, [para("소음 크기 비교 (dB)", 13.5, True)]))
yb = 6.04
add.append(rect(X0, yb + 0.03, X1 - X0, 0.05, "D9D9D9"))
add.append(rect(dbx(67), yb, dbx(76) - dbx(67), 0.11, "002060"))
add.append(textbox(dbx(67) - 0.45, 5.83, dbx(76) - dbx(67) + 0.9, 0.17, [para("정동관 주변 67~76", 8, True, "002060", "ctr")], anchor="b"))
REF = [(40, "도서관"), (50, "조용한 사무실"), (60, "보통 대화"), (70, "전화벨"), (80, "지하철 소음"), (90, "공장 안")]
for d, lab in REF:
    add.append(rect(dbx(d) - 0.006, yb - 0.02, 0.012, 0.15, "7F7F7F"))
    w = 0.76
    x = dbx(d) - w / 2; al = "ctr"
    if d == 40: x, al = X0 - 0.04, "l"
    if d == 90: x, al = X1 - w + 0.04, "r"
    add.append(textbox(x, yb + 0.16, w, 0.30, [para(str(d), 8, True, "404040", al), para(lab, 8, False, "595959", al)]))
add.append(textbox(4.72, 6.52, 3.89, 0.30, [para("북측 76 dB는 도로변 기준 70 dB보다 6 dB 높음. 소리 에너지는 약 4배, 귀로는 약 1.5배 크게 들림", 9.5, False, "000000")]))

# ---- 오른쪽: 소음원과 대응 표
src = by_name("표 13")
tbl_el = copy.deepcopy(src); new_id(tbl_el, "표")
nv = tbl_el.find("p:nvGraphicFramePr/p:nvPr", NS)
for e in list(nv): nv.remove(e)
tbl = tbl_el.find(".//a:tbl", NS)
rows = tbl.findall("a:tr", NS)
h_cell, b_left, b_ctr = rows[0].findall("a:tc", NS)[0], rows[1].findall("a:tc", NS)[0], rows[1].findall("a:tc", NS)[1]
b_left2, b_ctr2 = rows[2].findall("a:tc", NS)[0], rows[2].findall("a:tc", NS)[1]
grid = tbl.find("a:tblGrid", NS)
gtmp = grid.findall("a:gridCol", NS)[0]
for g in grid.findall("a:gridCol", NS): grid.remove(g)
COLS = [1.06, 0.68, 2.15]
for i, w in enumerate(COLS):
    g = copy.deepcopy(gtmp); g.set("w", str(int(w * E)))
    ext = g.find(".//{http://schemas.microsoft.com/office/drawing/2014/main}colId")
    if ext is not None: ext.set("val", str(30000 + i))
    grid.append(g)
for r in rows: tbl.remove(r)
def cell(tpl, text, algn=None):
    c = copy.deepcopy(tpl); set_text(c, text)
    if algn: c.find(".//a:pPr", NS).set("algn", algn)
    return c
EXT = [("북·서전로", "76", "6F 홀 북 면을 막고, 1층 북쪽은 차량 출구로만 씀"),
       ("서·전포대로", "72", "6F 홀 서 면을 막고 5F는 이중창, 1층 카페가 완충"),
       ("남·224번길", "70", "서·북보다 조용해 광장과 홀을 남쪽으로 엶"),
       ("동·이면도로", "67~69", "하역·이륜차 운영시간 제한, 동쪽엔 5F 사무 공간")]
INT = [("지하 공연장", "-", "박스인박스와 방진 바닥, 선큰 마당 쪽 로비가 완충"),
       ("6F 가변홀", "-", "이중 차음 지붕, 서·북은 막고 남쪽 광장으로만 엶"),
       ("소로·램프", "-", "2층 바닥이 덮은 7m 통로, 공연장은 방진 바닥")]
H_HDR, H_GRP, H_ROW = 0.30, 0.28, 0.56
hdr = etree.SubElement(tbl, A + "tr", h=str(int(H_HDR * E)))
for t, al in [("소음원", "l"), ("dB", "ctr"), ("대응", "l")]: hdr.append(cell(h_cell, t, al))
def group(title):
    tr = etree.SubElement(tbl, A + "tr", h=str(int(H_GRP * E)))
    c = cell(b_left, title); c.set("gridSpan", "3")
    r = c.find(".//a:rPr", NS); r.set("b", "1"); r.set("sz", "1000"); r.find("a:solidFill/a:srgbClr", NS).set("val", "002060")
    c.find("a:tcPr/a:solidFill/a:srgbClr", NS).set("val", "DAE3F3")
    tr.append(c)
    for _ in range(2):
        m = copy.deepcopy(b_left); m.set("hMerge", "1"); tr.append(m)
def rowsof(data):
    for i, (a_, b_, c_) in enumerate(data):
        L, C = (b_left, b_ctr) if i % 2 == 0 else (b_left2, b_ctr2)
        tr = etree.SubElement(tbl, A + "tr", h=str(int(H_ROW * E)))
        tr.append(cell(L, a_)); tr.append(cell(C, b_)); tr.append(cell(L, c_))
group("외부 소음원 (주간 추정치)"); rowsof(EXT)
group("건물 안 소음원"); rowsof(INT)
total_h = H_HDR + 2 * H_GRP + H_ROW * (len(EXT) + len(INT))
place(tbl_el, 8.94, 1.49, sum(COLS), total_h)
add.append(tbl_el)

# 출처 · 노트
src_box = by_name("TextBox 11")
for t in src_box.iter(A + "t"):
    if t.text and "별표, " in t.text:
        t.text = t.text.replace("별표, ", "별표, 국가소음정보시스템(소음 크기 비교), ", 1).replace("Petr Meissner", "Petr\xa0Meissner")
ext_lst = spTree.find("p:extLst", NS)
for el in add:
    if ext_lst is not None: ext_lst.addprevious(el)
    else: spTree.append(el)
tree.write(f, xml_declaration=True, encoding="UTF-8", standalone=True)

# 노트
rels = open(os.path.join(U, "ppt/slides/_rels/slide9.xml.rels"), encoding="utf8").read()
nf = re.search(r'notesSlides/(notesSlide\d+\.xml)', rels).group(1)
nt = etree.parse(os.path.join(U, "ppt/notesSlides", nf))
body = [s for s in nt.getroot().iter(P + "sp") if s.find(".//p:ph", NS) is not None and s.find(".//p:ph", NS).get("type") == "body"][0]
ts = list(body.iter(A + "t"))
ts[-1].text = (ts[-1].text or "") + (" 소음 크기 비교의 예시는 국가소음정보시스템의 소음도 비교 예시이며 거리·조건에 따라 다름."
                                     " 10 dB이 커지면 귀로는 약 2배, 6 dB이면 약 1.5배 크게 들림(소리 에너지는 약 4배).")
nt.write(os.path.join(U, "ppt/notesSlides", nf), xml_declaration=True, encoding="UTF-8", standalone=True)
print("ok", nid[0])
