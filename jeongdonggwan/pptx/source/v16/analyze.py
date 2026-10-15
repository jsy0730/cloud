import sys, re, collections
sys.path.insert(0, ".")
from typo import *
from lxml import etree
U = sys.argv[1]
import typo; typo.SCALE["k"] = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
nows = lambda s: re.sub(r"[\s\xa0]", "", s)
issues = []
def lh(p):
    k = 1.0
    if p["lnspc"] and p["lnspc"][0] == "pct": k = p["lnspc"][1] / 100
    return p["sz"] * 1.2 * k / 72
def para_h(ps):
    h = 0
    for i, p in enumerate(ps):
        if p["empty"]: h += (p["sz"] or 0) * 1.2 / 72; continue
        h += len(p["lines"]) * lh(p)
        if isinstance(p["aft"], float) and i < len(ps) - 1: h += p["aft"] / 72
        if isinstance(p["bef"], float) and i > 0: h += p["bef"] / 72
    return h
UNITS = r"^(대|명|석|면|곳|층|m|㎡|%|km|h|dB|년|월|회|주|평|원)"
for si, f in enumerate(slide_files(U), 1):
    t = etree.parse(f)
    tables = collections.defaultdict(dict)
    for name, kind, w, h, tb, ex in iter_text_shapes(t):
        if kind == "sp" and ex["bp"]["wrap"] == "none": continue
        ps = paragraphs(tb, w)
        for p in ps:
            if p["empty"] or len(p["lines"]) < 2: continue
            L = p["lines"]; last = nows(L[-1]); words = L[-1].split()
            if len(last) <= 3 or (len(words) == 1 and len(last) <= 4):
                issues.append((si, name, "끝줄 짧음", L))
            for a, b in zip(L, L[1:]):
                a_ = a.rstrip(); b_ = b.lstrip()
                if re.search(r"(^|\s)(약|총|및|→|·)$", a_) or re.search(r"\d$", a_) and re.match(UNITS, b_):
                    issues.append((si, name, "어색한 끊김", [a_[-12:], b_[:12]]))
                if a_.count("(") > a_.count(")") and len(nows(b_.split(")")[0])) <= 6:
                    issues.append((si, name, "괄호 끊김", [a_[-14:], b_[:14]]))
        if kind == "sp":
            need = para_h(ps); have = h / EMU
            if ex["bp"]["autofit"] != "sp" and need > have + 0.04 and any(not p["empty"] for p in ps):
                issues.append((si, name, f"넘침 {need:.2f}>{have:.2f}in", [p["text"][:30] for p in ps if not p["empty"]][:2]))
        else:
            tname, rc = name.split("[")
            r_, c_ = map(int, rc.rstrip("]").split(","))
            tc = ex["tc"]; pr = tc.find("a:tcPr", NS)
            mt = int(pr.get("marT", 45720)) if pr is not None else 45720
            mb = int(pr.get("marB", 45720)) if pr is not None else 45720
            span = int(tc.get("rowSpan", "1"))
            tables[tname][(r_, c_)] = ((para_h(ps) + (mt + mb) / EMU) / span, h / EMU)
    for tname, cells in tables.items():
        rows = collections.defaultdict(lambda: [0, 0])
        for (r_, c_), (need, have) in cells.items():
            rows[r_][0] = max(rows[r_][0], need); rows[r_][1] = have
        grow = sum(max(0, n - hv) for n, hv in rows.values())
        if grow > 0.05: issues.append((si, tname, f"표 행 늘어남 +{grow:.2f}in", [f"r{r}:{n:.2f}/{hv:.2f}" for r, (n, hv) in rows.items() if n > hv + 0.01]))
for x in issues: print(x)
print(len(issues))
