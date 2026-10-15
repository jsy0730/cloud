"""v16: 09 실별 면적 쪽 — 층별 면적을 실 단위 표(지상 · 지하 · 합계)로. usage: python3 -I area_slide.py <unpacked>"""
import sys, os, copy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from typo import slide_files, NS
from lxml import etree
U = sys.argv[1]
A = "{%s}" % NS["a"]; P = "{%s}" % NS["p"]
E = 914400
f = slide_files(U)[10]
tree = etree.parse(f); root = tree.getroot()
spTree = root.find("p:cSld/p:spTree", NS)
def by_name(n):
    for el in spTree:
        c = el.find(".//p:cNvPr", NS)
        if c is not None and c.get("name") == n: return el
    raise KeyError(n)
nid = [max(int(c.get("id")) for c in root.iter(P + "cNvPr"))]
def new_id(el, prefix):
    nid[0] += 1; c = el.find(".//p:cNvPr", NS); c.set("id", str(nid[0])); c.set("name", f"{prefix} {nid[0]-1}"); return el
def place(el, x, y, w, h):
    off = el.find(".//a:off", NS); ext = el.find(".//a:ext", NS)
    off.set("x", str(int(x * E))); off.set("y", str(int(y * E))); ext.set("cx", str(int(w * E))); ext.set("cy", str(int(h * E))); return el
def set_text(el, text):
    ts = list(el.iter(A + "t")); ts[0].text = text
    for t in ts[1:]:
        r = t.getparent(); r.getparent().remove(r)
    return el

# ---------------------------------------------------------------- 데이터 (기존 표와 같은 값)
CAT = {"주차": ("08205E", "FFFFFF"), "문화": ("4272C4", "FFFFFF"), "상업": ("7F9DCF", "FFFFFF"),
       "코어": ("ABBDE0", "000000"), "설비": ("DBE2F5", "000000")}
ABOVE = [("6F", "3,000.0", [("체육·공연 가변홀", "문화", 1500.0), ("다목적·연습실", "문화", 700.0), ("공연 지원", "문화", 650.0), ("코어", "코어", 150.0)]),
         ("5F", "4,322.1", [("상인회·공유오피스", "상업", 1200.0), ("주차 (전환 가능)", "주차", 2972.1), ("코어", "코어", 150.0)]),
         ("2~4F", "4,322.1×3", [("주차 (층당)", "주차", 4172.1), ("코어 (층당)", "코어", 150.0)]),
         ("1F", "3,635.3", [("서점", "상업", 400.0), ("카페", "상업", 400.0), ("공연 로비", "문화", 300.0), ("근린생활시설", "상업", 600.0),
                            ("램프", "주차", 900.0), ("정산", "주차", 100.0), ("이륜차", "주차", 200.0), ("하역", "설비", 150.0),
                            ("기타", "설비", 435.3), ("코어", "코어", 150.0)])]
BELOW = [("B1", "4,806.5", [("공연장 로비", "문화", 500.0), ("객석 상부", "문화", 300.0), ("주차", "주차", 3856.5), ("코어", "코어", 150.0)]),
         ("B2", "4,964.5", [("공연장 200석", "문화", 800.0), ("분장·창고", "문화", 300.0), ("주차", "주차", 3714.5), ("코어", "코어", 150.0)]),
         ("B3", "4,964.5", [("전기·기계실", "설비", 300.0), ("주차", "주차", 4514.5), ("코어", "코어", 150.0)]),
         ("B4", "4,964.5", [("펌프·저수조", "설비", 600.0), ("주차", "주차", 4214.5), ("코어", "코어", 150.0)])]
PY = 3.3058
# 검산
def tot(fl): return sum(a for _, _, a in fl[2]) * (3 if fl[0] == "2~4F" else 1)
up, dn = sum(tot(x) for x in ABOVE), sum(tot(x) for x in BELOW)
assert abs(up - 23923.7) < 0.05 and abs(dn - 19700.0) < 0.05, (up, dn)
for fl in ABOVE + BELOW:
    s = sum(a for _, _, a in fl[2]); assert abs(s - float(fl[1].split("×")[0].replace(",", ""))) < 0.05, fl[0]
cats = {}
for fl in ABOVE + BELOW:
    for _, c, a in fl[2]: cats[c] = cats.get(c, 0) + a * (3 if fl[0] == "2~4F" else 1)
assert abs(cats["주차"] - 32988.4) < 0.05 and abs(cats["문화"] - 5050) < 0.05 and abs(cats["상업"] - 2600) < 0.05, cats

# ---------------------------------------------------------------- 표 틀(기존 표의 서식 복제)
src = by_name("표 21")
tpl = src.find(".//a:tbl", NS); trs = tpl.findall("a:tr", NS)
H = trs[0].findall("a:tc", NS)[0]
B1L, B1R = trs[1].findall("a:tc", NS)[0], trs[1].findall("a:tc", NS)[-1]
B2L, B2R = trs[2].findall("a:tc", NS)[0], trs[2].findall("a:tc", NS)[-1]
TOTL, TOTR = trs[-1].findall("a:tc", NS)[0], trs[-1].findall("a:tc", NS)[-1]
gtmp = tpl.find("a:tblGrid", NS).findall("a:gridCol", NS)[0]

def run_fmt(c, sz=None, bold=None, color=None):
    for r in c.iter(A + "rPr"):
        if sz: r.set("sz", str(int(sz * 100)))
        if bold is not None:
            if bold: r.set("b", "1")
            elif "b" in r.attrib: del r.attrib["b"]
        if color:
            sf = r.find("a:solidFill/a:srgbClr", NS)
            if sf is not None: sf.set("val", color)
    for r in c.iter(A + "endParaRPr"):
        if sz: r.set("sz", str(int(sz * 100)))
def cell(tpl_c, text, algn=None, sz=9.5, bold=None, color=None, fill=None, mar=0.06):
    c = copy.deepcopy(tpl_c); set_text(c, text)
    if algn: c.find(".//a:pPr", NS).set("algn", algn)
    run_fmt(c, sz, bold, color)
    pr = c.find("a:tcPr", NS); pr.set("marL", str(int(mar * E))); pr.set("marR", str(int(mar * E)))
    pr.set("marT", "27432"); pr.set("marB", "27432")
    if fill: pr.find("a:solidFill/a:srgbClr", NS).set("val", fill)
    return c
def add_line(c, text, sz, color, bold=False):
    p0 = c.find("a:txBody/a:p", NS); p = copy.deepcopy(p0)
    ts = list(p.iter(A + "t")); ts[0].text = text
    for r in p.iter(A + "rPr"):
        r.set("sz", str(int(sz * 100)))
        if not bold and "b" in r.attrib: del r.attrib["b"]
        sf = r.find("a:solidFill/a:srgbClr", NS)
        if sf is not None: sf.set("val", color)
    c.find("a:txBody", NS).findall("a:p", NS)[-1].addnext(p)
def new_table(cols, x, y):
    el = copy.deepcopy(src); new_id(el, "표")
    nv = el.find("p:nvGraphicFramePr/p:nvPr", NS)
    for e in list(nv): nv.remove(e)
    tbl = el.find(".//a:tbl", NS)
    grid = tbl.find("a:tblGrid", NS)
    for g in grid.findall("a:gridCol", NS): grid.remove(g)
    for i, w in enumerate(cols):
        g = copy.deepcopy(gtmp); g.set("w", str(int(w * E)))
        cid = g.find(".//{http://schemas.microsoft.com/office/drawing/2014/main}colId")
        if cid is not None: cid.set("val", str(40000 + nid[0] * 10 + i))
        grid.append(g)
    for r in tbl.findall("a:tr", NS): tbl.remove(r)
    return el, tbl

COLS = [0.74, 1.55, 0.50, 0.66, 0.48]
RH, HH = 0.245, 0.27
RS = 0.235
def schedule(floors, x, y):
    el, tbl = new_table(COLS, x, y)
    tr = etree.SubElement(tbl, A + "tr", h=str(int(HH * E)))
    for t, al in [("층", "ctr"), ("실", "l"), ("분류", "ctr"), ("면적㎡", "r"), ("평", "r")]:
        tr.append(cell(H, t, al, sz=9.5))
    n = 0; h = HH
    for fl, sub, rooms in floors:
        L, R = (B1L, B1R) if n % 2 == 0 else (B2L, B2R); n += 1
        for i, (room, cat, area) in enumerate(rooms):
            tr = etree.SubElement(tbl, A + "tr", h=str(int(RH * E))); h += RH
            if i == 0:
                fc = cell(L, fl, "ctr", sz=10.5, bold=True); fc.set("rowSpan", str(len(rooms)))
                fc.find("a:tcPr", NS).set("anchor", "ctr")
                add_line(fc, sub, 8.5, "595959")
                tr.append(fc)
            else:
                m = cell(L, "", "ctr"); m.set("vMerge", "1"); tr.append(m)
            tr.append(cell(L, room, "l"))
            bg, fg = CAT[cat]
            tr.append(cell(L, cat, "ctr", sz=8.5, bold=True, color=fg, fill=bg))
            tr.append(cell(R, f"{area:,.1f}", "r"))
            tr.append(cell(R, f"{area / PY:,.0f}", "r", color="595959"))
    place(el, x, y, sum(COLS), h)
    return el, h

add = []
XL, XR, Y = 0.5, 4.68, 1.49
t_up, h_up = schedule(ABOVE, XL, Y); add.append(t_up)
t_dn, h_dn = schedule(BELOW, XR, Y); add.append(t_dn)

# 합계 표
SC = [1.21, 1.56, 1.16]
el, tbl = new_table(SC, XR, 0)
tr = etree.SubElement(tbl, A + "tr", h=str(int(HH * E)))
for t, al in [("구분", "l"), ("면적㎡", "r"), ("평", "r")]: tr.append(cell(H, t, al))
rows = [("지상", 23923.7), ("지하", 19700.0)]
for i, (k, v) in enumerate(rows):
    L, R = (B1L, B1R) if i % 2 == 0 else (B2L, B2R)
    tr = etree.SubElement(tbl, A + "tr", h=str(int(RS * E)))
    tr.append(cell(L, k, "l")); tr.append(cell(R, f"{v:,.1f}", "r")); tr.append(cell(R, f"{v / PY:,.0f}", "r", color="595959"))
tr = etree.SubElement(tbl, A + "tr", h=str(int(RS * E)))
tr.append(cell(TOTL, "연면적", "l", bold=True)); tr.append(cell(TOTR, "43,623.7", "r", bold=True)); tr.append(cell(TOTR, f"{43623.7 / PY:,.0f}", "r", bold=True))
sum_h = HH + 3 * RS
sum_y = 6.80 - sum_h
place(el, XR, sum_y, sum(SC), sum_h); add.append(el)

# 머리글
head = by_name("TextBox 14"); set_text(head, "지상층 실별 면적")
head.find(".//a:ext", NS).set("cx", str(int(3.78 * E)))
def heading(x, y, text):
    bar = copy.deepcopy(by_name("직사각형 13")); new_id(bar, "직사각형")
    bo = bar.find(".//a:off", NS); bo.set("x", str(int(x * E))); bo.set("y", str(int((y + 0.03) * E)))
    tb = copy.deepcopy(head); new_id(tb, "TextBox"); set_text(tb, text)
    to = tb.find(".//a:off", NS); to.set("x", str(int((x + 0.15) * E))); to.set("y", str(int(y * E)))
    return [bar, tb]
add += heading(XR, 1.14, "지하층 실별 면적")
add += heading(XR, sum_y - 0.35, "면적 합계")
assert Y + h_dn + 0.12 < sum_y - 0.35, (Y + h_dn, sum_y)
assert Y + h_up <= 6.81, Y + h_up

spTree.remove(src)
ext_lst = spTree.find("p:extLst", NS)
for el in add:
    (ext_lst.addprevious(el) if ext_lst is not None else spTree.append(el))
tree.write(f, xml_declaration=True, encoding="UTF-8", standalone=True)
print("ok", round(Y + h_up, 2), round(Y + h_dn, 2), round(sum_y, 2))
