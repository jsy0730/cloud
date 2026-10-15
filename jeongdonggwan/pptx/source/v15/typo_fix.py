"""v15 조판 보정: 줄바꿈 묶음(NBSP), 머리글 줄 정렬, 차트 항목 구분자. usage: python3 -I typo_fix.py <unpacked>"""
import sys, os, re, io, zipfile, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from typo import *
from lxml import etree
U = sys.argv[1]
NB = "\xa0"
P = "{%s}" % NS["p"]
log = []

# 1) 문단 단위 치환: (쪽, 원문 일부, 바꿀 글) — 공백 대신 NBSP로 어절을 묶음
BIND = {
    4: [("없음(지하 라이브클럽 1곳)", f"없음 (지하{NB}라이브클럽{NB}1곳)")],
    5: [("충당(사업성은 별도 검토)", f"충당 (사업성은{NB}별도{NB}검토)")],
    8: [("주거 경계에 이름", f"주거 경계에{NB}이름")],
    9: [("에너지는 약 4배, 귀로는 약 1.5배", f"에너지는 약{NB}4배, 귀로는 약{NB}1.5배")],
    13: [("(다목적체육관 1,394㎡)", f"(다목적체육관{NB}1,394㎡)")],
    19: [("블록 밑면에서 내려감", f"블록 밑면에서{NB}내려감")],
    20: [("차가 드나들지 않게 함", f"차가 드나들지{NB}않게{NB}함")],
    23: [("지하 공연장 30m)", f"지하{NB}공연장{NB}30m)")],
}
files = slide_files(U)
for pg, pairs in BIND.items():
    f = files[pg - 1]; t = etree.parse(f); hit = set()
    for p in t.iter(A + "p"):
        ts = list(p.iter(A + "t"))
        for old, new in pairs:
            for x in ts:
                s = (x.text or "")
                if old in s.replace(NB, " "):
                    # 원문 위치를 NBSP 무시하고 찾아 교체
                    norm = s.replace(NB, " "); i = norm.index(old)
                    x.text = s[:i] + new + s[i + len(old):]; hit.add(old); log.append(f"p{pg}: {old!r}")
    miss = [o for o, _ in pairs if o not in hit]
    if miss: print("MISS", pg, miss)
    t.write(f, xml_declaration=True, encoding="UTF-8", standalone=True)

# 2) 머리글 줄: 제목 → 막대 → 소제목 → 선
def mw(sp):
    runs = []
    for p in sp.find("p:txBody", NS).findall("a:p", NS): runs += runs_of(p)
    return sum(cw(ch, b) * sz / 72 + spc / 72 for tx, sz, b, spc in runs for ch in tx)
def geo(sp):
    o = sp.find("p:spPr/a:xfrm/a:off", NS); e = sp.find("p:spPr/a:xfrm/a:ext", NS)
    return o, e
for pg, f in enumerate(files, 1):
    if pg in (1, 2): continue
    t = etree.parse(f); r = t.getroot()
    title = bar = sub = line = None
    for sp in r.find("p:cSld/p:spTree", NS).findall("p:sp", NS):
        o, e = geo(sp)
        if o is None: continue
        x, y, w = int(o.get("x")) / EMU, int(o.get("y")) / EMU, int(e.get("cx")) / EMU
        rp = sp.find(".//a:rPr", NS); g = sp.find(".//a:prstGeom", NS)
        if abs(y - 0.2) < 0.02 and rp is not None and rp.get("sz") == "1700": title = sp
        elif abs(y - 0.2) < 0.02 and rp is not None and rp.get("sz") == "1200" and x > 1.5: sub = sp
        elif g is not None and g.get("prst") == "rect" and abs(y - 0.36) < 0.03 and w < 0.06: bar = sp
        elif g is not None and g.get("prst") == "line" and abs(y - 0.51) < 0.03 and x < 9.1: line = sp
    if not (title is not None and bar is not None and sub is not None): continue
    to, te = geo(title); bo, be = geo(bar); so, se = geo(sub)
    gap_bar = int(bo.get("x")) - (int(to.get("x")) + int(te.get("cx")))
    gap_sub = int(so.get("x")) - int(bo.get("x"))
    tw = int((mw(title) + 0.20) * EMU); sw = int((mw(sub) + 0.146) * EMU)
    gap_bar = int(0.08 * EMU)
    te.set("cx", str(tw))
    bx = int(to.get("x")) + tw + gap_bar; bo.set("x", str(bx))
    sx = bx + int(0.15 * EMU); so.set("x", str(sx)); se.set("cx", str(sw))
    if line is not None:
        lo, le = geo(line); right = int(lo.get("x")) + int(le.get("cx"))
        lx = sx + sw + int(0.2 * EMU); lo.set("x", str(lx)); le.set("cx", str(max(right - lx, int(0.3 * EMU))))
        if right - lx < 0.4 * EMU: log.append(f"p{pg}: 선 짧음 {(right-lx)/EMU:.2f}")
    t.write(f, xml_declaration=True, encoding="UTF-8", standalone=True)

# 3) 차트 항목 이름의 ' · '
for cf in glob.glob(os.path.join(U, "ppt/charts/chart*.xml")):
    s = open(cf, encoding="utf8").read()
    s2 = re.sub(r"(<c:v>[^<]*?) · ([^<]*</c:v>)", lambda m: m.group(1) + "·" + m.group(2), s)
    while s2 != s:
        s = s2; s2 = re.sub(r"(<c:v>[^<]*?) · ([^<]*</c:v>)", lambda m: m.group(1) + "·" + m.group(2), s)
    open(cf, "w", encoding="utf8").write(s2)
for xf in glob.glob(os.path.join(U, "ppt/embeddings/*.xlsx")):
    zin = zipfile.ZipFile(xf); buf = io.BytesIO(); zout = zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED)
    for it in zin.infolist():
        d = zin.read(it.filename)
        if it.filename == "xl/sharedStrings.xml": d = d.replace(" · ".encode(), "·".encode())
        zout.writestr(it, d)
    zout.close(); zin.close(); open(xf, "wb").write(buf.getvalue())
print("\n".join(log))
