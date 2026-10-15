"""PowerPoint 줄바꿈 근사: v11 PDF에서 맑은 고딕 글자 폭을 뽑고, pptx 문단을 어절 단위로 배치."""
import re, os, json, collections
from lxml import etree
import pdfplumber

NS = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main",
      "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}
A = "{%s}" % NS["a"]
EMU = 914400
FINAL = "/home/user/cloud/jeongdonggwan/pptx/final/"
PDFS = [FINAL + "261002-전포동주차타워사업계획서-건물주변구체화-정성윤.pdf", FINAL + "전포정동관_최종본_v9.pdf"]

# ---------------------------------------------------------------- metrics
def build_metrics(cache="metrics.json"):
    if os.path.exists(cache): return json.load(open(cache))
    W = {"r": collections.defaultdict(list), "b": collections.defaultdict(list)}
    space = {"r": [], "b": []}
    for path in PDFS:
        with pdfplumber.open(path) as pdf:
            for pg in pdf.pages:
                cs = pg.chars
                for i, c in enumerate(cs):
                    if "Malgun" not in c["fontname"] or c["size"] < 5: continue
                    k = "b" if "Bold" in c["fontname"] else "r"
                    W[k][c["text"]].append((c["x1"] - c["x0"]) / c["size"])
                    if i + 1 < len(cs):
                        d = cs[i + 1]
                        if abs(d["top"] - c["top"]) < 0.5 and abs(d["size"] - c["size"]) < 0.05 and d["fontname"] == c["fontname"]:
                            g = (d["x0"] - c["x1"]) / c["size"]
                            if 0.2 < g < 0.45: space[k].append(g)
    out = {k: {ch: sorted(v)[len(v) // 2] for ch, v in W[k].items()} for k in W}
    for k in space:
        v = sorted(space[k]); out[k][" "] = v[len(v) // 2] if v else 0.3
    json.dump(out, open(cache, "w"), ensure_ascii=False)
    return out

M = build_metrics()
SCALE = {"k": 1.0}
def cw(ch, bold):
    t = M["b" if bold else "r"]
    if ch in t: return t[ch]
    o = M["r"] if bold else M["b"]
    if ch in o: return o[ch]
    if "가" <= ch <= "힣" or "一" <= ch <= "鿿": return 1.0
    if ch == "\xa0": return t.get(" ", 0.3)
    if ch.isdigit(): return t.get("0", 0.55)
    return 0.55

# ---------------------------------------------------------------- pptx paragraphs
def runs_of(p, default_sz=18.0):
    out = []
    for r in p:
        tag = etree.QName(r).localname
        if tag in ("r", "fld"):
            rp = r.find("a:rPr", NS); t = r.find("a:t", NS)
            sz = int(rp.get("sz")) / 100 if rp is not None and rp.get("sz") else default_sz
            b = rp is not None and rp.get("b") == "1"
            spc = int(rp.get("spc")) / 100 if rp is not None and rp.get("spc") else 0.0
            out.append((t.text or "" if t is not None else "", sz, b, spc))
        elif tag == "br":
            out.append(("\n", default_sz, False, 0.0))
    return out

def layout(runs, w_first, w_rest):
    """어절(공백) 단위 줄바꿈. NBSP는 붙여 둠. 한 어절이 줄보다 길면 글자 단위로 자름."""
    toks = []   # (text, width, is_space)
    for text, sz, b, spc in runs:
        em = sz / 72
        for ch in text:
            w = cw(ch, b) * em * SCALE["k"] + spc / 72
            if ch == "\n": toks.append(("\n", 0, "br")); continue
            kind = "sp" if ch == " " else "ch"
            if toks and toks[-1][2] == kind == "ch":
                toks[-1] = (toks[-1][0] + ch, toks[-1][1] + w, "ch")
            elif toks and toks[-1][2] == kind == "sp":
                toks[-1] = (toks[-1][0] + ch, toks[-1][1] + w, "sp")
            else: toks.append((ch, w, kind))
    lines, cur, curw = [], "", 0.0
    limit = w_first
    # 단어 폭은 원래 토큰 기준 비례로 나눔
    flat = []
    for t in toks:
        if t[2] != "ch": flat.append(t); continue
        parts = re.findall(r"[^\-/–~]*[\-/–~]|[^\-/–~]+", t[0])
        tot = len(t[0]) or 1
        for pt in parts: flat.append((pt, t[1] * len(pt) / tot, "ch"))
    pend_sp = ("", 0.0)
    for text, w, kind in flat:
        if kind == "br":
            lines.append(cur); cur, curw, pend_sp, limit = "", 0.0, ("", 0.0), w_rest; continue
        if kind == "sp":
            pend_sp = (pend_sp[0] + text, pend_sp[1] + w); continue
        need = curw + pend_sp[1] + w
        if cur and need > limit + 1e-4:
            lines.append(cur); cur, curw, limit = "", 0.0, w_rest; pend_sp = ("", 0.0)
            need = w
        if not cur and w > limit:     # 긴 어절은 글자 단위
            for ch in text:
                cwid = w / max(len(text), 1)
                if cur and curw + cwid > limit + 1e-4:
                    lines.append(cur); cur, curw, limit = "", 0.0, w_rest
                cur += ch; curw += cwid
            pend_sp = ("", 0.0); continue
        cur += pend_sp[0] + text; curw = need; pend_sp = ("", 0.0)
    lines.append(cur)
    return lines

def body_props(txBody):
    bp = txBody.find("a:bodyPr", NS)
    g = lambda k, d: int(bp.get(k)) if bp is not None and bp.get(k) is not None else d
    return {"l": g("lIns", 91440), "r": g("rIns", 91440), "t": g("tIns", 45720), "b": g("bIns", 45720),
            "wrap": (bp.get("wrap") if bp is not None else None) or "square",
            "autofit": None if bp is None else ("norm" if bp.find("a:normAutofit", NS) is not None else ("sp" if bp.find("a:spAutoFit", NS) is not None else None))}

def para_info(p):
    pPr = p.find("a:pPr", NS)
    marL = int(pPr.get("marL")) if pPr is not None and pPr.get("marL") else 0
    ind = int(pPr.get("indent")) if pPr is not None and pPr.get("indent") else 0
    ln = pPr.find("a:lnSpc", NS) if pPr is not None else None
    lnspc = None
    if ln is not None:
        pc = ln.find("a:spcPct", NS); pt = ln.find("a:spcPts", NS)
        lnspc = ("pct", int(pc.get("val")) / 1000) if pc is not None else ("pts", int(pt.get("val")) / 100)
    def sp(tag):
        e = pPr.find(f"a:{tag}", NS) if pPr is not None else None
        if e is None: return 0.0
        pt = e.find("a:spcPts", NS); pc = e.find("a:spcPct", NS)
        return int(pt.get("val")) / 100 if pt is not None else ("pct", int(pc.get("val")) / 1000)
    algn = pPr.get("algn") if pPr is not None else None
    return marL, ind, lnspc, sp("spcBef"), sp("spcAft"), algn

def iter_text_shapes(tree):
    """(이름, 종류, 내부폭EMU, 높이EMU, txBody, extra) — 표는 셀마다."""
    root = tree.getroot()
    for sp in root.iter("{%s}sp" % NS["p"]):
        tb = sp.find("p:txBody", NS)
        if tb is None: continue
        name = sp.find("p:nvSpPr/p:cNvPr", NS).get("name")
        ext = sp.find("p:spPr/a:xfrm/a:ext", NS); off = sp.find("p:spPr/a:xfrm/a:off", NS)
        if ext is None: continue
        bp = body_props(tb)
        yield name, "sp", int(ext.get("cx")) - bp["l"] - bp["r"], int(ext.get("cy")) - bp["t"] - bp["b"], tb, \
              {"bp": bp, "x": int(off.get("x")), "y": int(off.get("y")), "cx": int(ext.get("cx")), "cy": int(ext.get("cy")), "sp": sp}
    for gf in root.iter("{%s}graphicFrame" % NS["p"]):
        tbl = gf.find(".//a:tbl", NS)
        if tbl is None: continue
        name = gf.find("p:nvGraphicFramePr/p:cNvPr", NS).get("name")
        cols = [int(c.get("w")) for c in tbl.find("a:tblGrid", NS)]
        for ri, tr in enumerate(tbl.findall("a:tr", NS)):
            ci = 0
            for tc in tr.findall("a:tc", NS):
                span = int(tc.get("gridSpan", "1"))
                if tc.get("hMerge") == "1" or tc.get("vMerge") == "1": ci += 1; continue
                tcPr = tc.find("a:tcPr", NS)
                l = int(tcPr.get("marL", 91440)) if tcPr is not None else 91440
                r_ = int(tcPr.get("marR", 91440)) if tcPr is not None else 91440
                w = sum(cols[ci:ci + span]) - l - r_
                yield f"{name}[{ri},{ci}]", "tc", w, int(tr.get("h")), tc.find("a:txBody", NS), {"tc": tc}
                ci += span

def paragraphs(tb, inner_w):
    out = []
    for p in tb.findall("a:p", NS):
        runs = runs_of(p)
        text = "".join(r[0] for r in runs)
        marL, ind, lnspc, bef, aft, algn = para_info(p)
        if not text.strip():
            out.append({"p": p, "text": text, "lines": [""], "sz": max([r[1] for r in runs] or [0]), "empty": True,
                        "lnspc": lnspc, "bef": bef, "aft": aft, "marL": marL, "ind": ind}); continue
        wf = (inner_w - marL - ind) / EMU; wr = (inner_w - marL) / EMU
        lines = layout(runs, wf, wr)
        out.append({"p": p, "text": text, "lines": lines, "sz": max(r[1] for r in runs if r[0].strip()),
                    "b": any(r[2] for r in runs if r[0].strip()), "spc": sorted({r[3] for r in runs if r[0].strip()}),
                    "lnspc": lnspc, "bef": bef, "aft": aft, "marL": marL, "ind": ind, "algn": algn, "empty": False})
    return out

def slide_files(u):
    pres = etree.parse(os.path.join(u, "ppt/presentation.xml"))
    rels = etree.parse(os.path.join(u, "ppt/_rels/presentation.xml.rels"))
    m = {e.get("Id"): e.get("Target") for e in rels.getroot()}
    return [os.path.join(u, "ppt", m[e.get("{%s}id" % NS["r"])]) for e in pres.getroot().find("p:sldIdLst", NS)]
