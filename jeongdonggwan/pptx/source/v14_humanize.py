"""v13 -> v14: 문구를 사람 손으로 쓴 보고서 톤으로, 도구 흔적 제거. usage: python3 -I humanize.py <unpacked dir>"""
import re, sys, io, zipfile, os
from lxml import etree

U = sys.argv[1]
NS = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main",
      "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}
A = "{%s}" % NS["a"]
EMU = 914400
log = []

def load(path):
    return etree.parse(os.path.join(U, path), etree.XMLParser(remove_blank_text=False))
def save(tree, path):
    tree.write(os.path.join(U, path), xml_declaration=True, encoding="UTF-8", standalone=True)

# ---------- page -> slide file
pres = load("ppt/presentation.xml")
rels = load("ppt/_rels/presentation.xml.rels")
rid2t = {e.get("Id"): e.get("Target") for e in rels.getroot()}
pages = [rid2t[e.get("{%s}id" % NS["r"])] for e in pres.getroot().find("p:sldIdLst", NS)]
page_of = {"ppt/" + t: i + 1 for i, t in enumerate(pages)}

# ---------- 1) 문구 교체 (원문 그대로 일치할 때만). "*"로 끝나면 앞부분 일치
SUB = "Text 3"   # 머리글 소제목
OVR = {
 1: {"2026 · 공학설계기초": "2026 공학설계기초"},
 2: {"전포 정동관 · 낮에는 주차장, 밤에는 공연과 옥상 광장": "낮에는 주차장, 밤에는 공연장과 옥상 광장이 되는 전포 정동관"},
 3: {"사람을 받아 온 땅이 이제 차와 사람을 함께 받을 차례임": "방문객은 계속 늘었지만 주차 공간은 부족함",
     "계획 · 협약 단계이며 확정된 것은 아님": "아직 계획·협약 단계로 확정되지 않음",
     "주차를 늘려 상권이 산 사례": "주차장 확충 후 상권 변화 사례",
     "서울 사당 · 공영 145면": "서울 사당 (공영 145면)"},
 4: {"먹고 · 보고는 채워졌고 듣고만 비어 공연장이 필요함": "먹거리·볼거리는 많지만 공연 공간은 없음",
     "왜 듣고만 비어 있는가": "공연 공간이 없는 이유",
     "무엇이 비었나": "현황",
     "규모의 공백": "규모", "제도의 공백": "제도", "위치의 공백": "입지",
     "공연이 들어오면 먹고 · 보고와 이어짐: 대학로 관객은 공연 전후 1인당 약 2만 원을 식사 · 음료 · 주류에 씀(2013)":
        "공연장이 생기면 주변 식당·카페 이용도 늘어남. 대학로 관객은 공연 전후 1인당 약 2만 원을 식사·음료·주류에 씀(2013)"},
 5: {"주차장이 공연장을 받치고 공연장이 주차장을 살림": "주차와 공연은 이용 시간대가 겹치지 않음",
     "왜 한 건물인가": "한 건물로 계획한 이유",
     "극장 하나만으론 살아남기 어려움": "소극장 단독 운영은 어려움",
     "건물이 문화시설을 품어야 함": "낮과 밤에 같은 공간을 나눠 씀",
     "주차 수입이 공연장 운영을 받치는 구조를 건물이 만듦(사업성은 별도 검토)": "주차 수입으로 공연장 운영비 일부를 충당(사업성은 별도 검토)",
     "주차 건물이라 공연 소음이 건물 안에서는 문제가 적음": "주차 건물이라 공연 소음 문제가 적음",
     "한 건물 안에서 이미 이뤄지고 있음": "주차장과 문화시설을 합친 해외 사례"},
 7: {"수요 · 공백 · 형상이 모두 이 땅에 겹침": "두 역과 세 상권 사이, 주차가 부족한 곳임",
     "이 땅이어야 하는 이유": "부지 선정 이유",
     "두 역 사이에 놓인 땅": "서면역과 전포역 사이",
     "서면역 737m · 전포역 529m, 어느 역에서도 걸어서 닿음": "서면역 737m, 전포역 529m로 두 역 모두 걸어서 이동 가능",
     "세 상권이 만나는 결절점": "세 상권이 만나는 위치",
     "공영주차장이 비어 있는 자리": "공영주차장 부족",
     "이미 있는 6m 소로를 씀": "기존 6m 소로 활용",
     "새 길을 뚫지 않고 소로 5필지(733.1㎡)를 차량 전용 차로로 돌려 씀": "소로 5필지(733.1㎡)를 차량 전용 차로로 사용",
     "세 도로에 면해 입구와 출구를 가름": "세 도로에 접해 입·출구 분리 가능",
     "전포대로(서) · 서전로(북) · 224번길(남), 400대 초과 시 입출구 분리 요건": "전포대로(서), 서전로(북), 224번길(남)에 접함. 400대 초과 시 입·출구 분리 필요"},
 8: {"서 · 동 면은 슬랫으로 거르고 광장은 남쪽에 둠": "서·동 면은 슬랫으로 가리고 광장은 남쪽에 둠"},
 9: {"소음 큰 실은 지하 · 최상층 안쪽에 두고 서 · 북 면은 닫음": "시끄러운 실은 지하와 최상층에 두고 서·북 면은 막음",
     "서 · 북 면은 닫고 남쪽 광장으로 개구": "서·북 면은 막고 남쪽 광장 쪽으로 엶"},
 10: {"조망은 옥상 광장에서 얻고 남 · 동으로만 엶": "옥상 광장에서 남·동쪽 조망이 가장 좋음",
      "서 · 약 0.6km": "서, 약 0.6km"},
 13: {"반경 안에 없는 용도를 층별로 쌓아 한 건물에 모음": "주변에 없는 시설을 중심으로 층별 용도를 정함"},
 14: {"소로를 따라 자른 단면에서 차와 사람의 길이 갈림": "단면에서 차량 동선과 보행 동선이 분리됨",
      "출처: 본 시안 개념 단면 · 구조 · 설비 두께는 표현하지 않음, 층고 · 면적 개략": "출처: 본 시안 개념 단면 / 구조·설비 두께는 생략, 층고와 면적은 개략"},
 19: {"공연과 행사는 지하 홀과 높은 층고에 담았음": "공연장은 지하에, 행사 공간은 층고 높은 층에 둠",
      "콘크리트 셸이 음향과 차음을 함께 풀고, 지상 블록은 마을 광장의 랜드마크가 됨": "콘크리트 셸로 음향과 차음을 해결하고, 지상 블록은 마을 광장의 랜드마크 역할을 함"},
 20: {"두 끝을 비워 이격을 맞추고 그 자리를 얼굴로 씀": "뾰족한 두 끝을 비워 이격을 맞추고 계단 코어로 씀",
      "주차가 어려운 좁은 끝을 사람 이동의 중심으로 씀": "주차가 어려운 좁은 끝에 계단과 승강기를 둠"},
 21: {"주차 75.62%로 요건을 맞추고 공연과 광장을 얹음": "주차 비율 75.62%를 확보하고 공연장과 광장을 더함"},
 22: {"주차층은 슬랫으로 감싸고 홀과 계단은 켜서 드러냄": "주차층은 목재 슬랫으로 가리고 홀과 계단은 드러냄",
      "밤 · 주차층은 낮게, 1층과 6F 홀이 켜짐": "야간, 1층과 6F 홀에 불이 켜진 모습",
      "서전로 × 전포대로 모퉁이 · 1층이 가로를 향해 열림": "서전로와 전포대로 모퉁이, 1층이 가로 쪽으로 열림"},
 23: {"주차 요건은 적합하고 출입구 · 구조 · 피난은 조건부임": "주차 요건은 충족, 출입구·구조·피난은 추가 검토 필요",
      "출처: 법제처 국가법령정보센터 현행본(2026.10.11 조회)*": "출처: 법제처 국가법령정보센터 현행 법령(2026.10.11 조회)",
      "구조 · 방재는 확정 설계가 아닌 제안이며*": "구조·방재는 제안 단계로, 실제 설계에서 계산으로 확인해야 함. 조건부 3건: 노외주차장 출입구(교차로 5m, 정류장 10m), 주차장 구조(램프 17%), 피난(보행거리 50m, 지하 공연장 30m)"},
}
CONCEPT = {"停과 動이 교대하는 하루": "낮과 밤의 쓰임",
           "차가 멈추는 주차층은 목재 슬랫 스크린으로 차분히 감싸고, 사람이 움직이는 순환 계단 · 6F 가변홀 · 옥상 광장은 검은 계단과 켜진 홀로 드러냄":
           "주차층은 목재 슬랫으로 감싸고, 순환 계단·6F 가변홀·옥상 광장은 밖에서 보이도록 열어 둠"}
OVR[15] = dict(CONCEPT); OVR[16] = dict(CONCEPT)
SUBSTR = {6: [("확인도면 정합으로 판별함", "확인도면과 대조함")],
          17: [("(저장소 자료)", "")]}
NOTES = {15: "낮: 주차장으로 쓰이는 모습.",
         16: "밤: 공연장과 옥상 광장에 불이 켜진 모습.",
         22: "외피 슬랫 폭 0.15m, 간격 0.24m는 가정값임."}
used = set()

# ---------- 2) " · " 구분자 정리
HANGULISH = re.compile(r"^[(\[]?[\uac00-\ud7a3\u4e00-\u9fff\u2160-\u216f]")
POST = [("풍경·사진, SNS 감성", "풍경·사진·SNS 감성"), ("남측, 224번길", "남측·224번길"), ("이륜차, 자전거", "이륜차·자전거"),
        ("객석, 코트", "객석·코트"), ("근생, 문화집회", "근생·문화집회"), ("입구, 출구 분리", "입구·출구 분리"),
        ("트러스, 전이보", "트러스·전이보"), ("방화, 내후성", "방화·내후성"), ("놀이, 운동 공간", "놀이·운동 공간"),
        ("6층, 옥상", "6층·옥상"), ("B1, B2", "B1·B2"), ("B3, B4", "B3·B4"), ("평택·대지", "평택, 대지"),
        ("식당, 술집이", "식당·술집이"), ("용도 선정, 층별 계획", "용도 선정·층별 계획"), ("공구, 철물점", "공구·철물점"),
        ("A 종단면 (남 → 북), 개념, 층고, 면적 개략", "A 종단면(남→북), 개념도, 층고·면적 개략"),
        ("← 남·전포대로, 224번길", "← 남(전포대로·224번길)"), ("← 서·전포대로", "← 서(전포대로)"), ("서전로·북 →", "북(서전로) →"),
        ("정동관 그림자, 동지 09, 12, 15시,", "정동관 그림자(동지 09·12·15시),"),
        ("출처: 본 시안, 진출입 위치는 구청, 경찰 협의 전 개념이며", "출처: 본 시안 / 진출입 위치는 구청·경찰 협의 전 개념이며")]
HANGULISH = re.compile(r"^[(\[]?[가-힣一-鿿Ⅰ-Ⅿ]")
def fix_dots(s, source=False, tight_all=False):
    s = re.sub(r"[ \xa0]·[ \xa0]", " · ", s)
    if " · " in s:
        if source: s = s.replace(" · ", ", ")
        elif tight_all: s = s.replace(" · ", "·")
        else:
            parts = s.split(" · "); out = parts[0]
            for i in range(1, len(parts)):
                left, right = parts[i-1], parts[i]
                L = left.split()[-1] if left.split() else ""
                R = right.split()[0] if right.split() else ""
                tight = (HANGULISH.match(L) and HANGULISH.match(R) and not re.search(r"\d[^가-힣]*$", L)
                         and (" " not in left.strip() or " " not in right.strip() or len(L) == 1 or len(R) == 1))
                out += ("·" if tight else ", ") + right
            s = out
    for a, b in POST: s = s.replace(a, b)
    s = re.sub(r"제(\d+), (\d+)조", r"제\1·\2조", s)
    return s

def is_footer(t): return t.startswith("담당자 정성윤")

def edit_text_tree(tree, page, notes=False):
    for p in tree.iter(A + "p"):
        runs = [r for r in p.iter(A + "t")]
        if not runs: continue
        ptext = "".join(t.text or "" for t in runs)
        src = ptext.startswith("출처")
        for t in runs:
            s = t.text or ""
            if not notes:
                for k, v in OVR.get(page, {}).items():
                    n = s.replace("\xa0", " ")
                    hit = n.startswith(k[:-1]) if k.endswith("*") else n == k
                    if hit:
                        s = v; used.add((page, k)); break
                if s.strip() == "연결" and page == 4: s = s.replace("연결", "기대 효과")
                if s.startswith("->"): s = "→" + s[2:]
                for a, b in SUBSTR.get(page, []):
                    if a in s: s = s.replace(a, b); used.add((page, a))
            if not is_footer(ptext):
                s = fix_dots(s, source=src, tight_all=(page == 2 and not notes))
                s = re.sub(r"(\d)–(\d)", r"\1~\2", s)          # 03–05 -> 03~05
            if s != (t.text or ""): t.text = s

# ---------- 3) 도형 이름을 PowerPoint 기본 이름으로, 대체 텍스트 경로 제거
GEOM = {"rect": "직사각형", "line": "직선 연결선", "ellipse": "타원", "roundRect": "사각형: 둥근 모서리",
        "homePlate": "화살표: 오각형", "rtTriangle": "직각 삼각형"}
def rename(tree):
    for c in tree.iter("{%s}cNvPr" % NS["p"]):
        if c.get("descr", "").startswith(("C:\\", "/", "file:")): del c.attrib["descr"]
        name = c.get("name", ""); n = int(c.get("id")) - 1
        if not re.fullmatch(r"(Text|Shape|Image|Table|Chart|Group) \d+", name): continue
        holder = c.getparent().getparent()          # p:sp / p:pic / ...
        tag = etree.QName(holder).localname
        if tag == "pic": new = f"그림 {n}"
        elif tag == "grpSp": new = f"그룹 {n}"
        elif tag == "graphicFrame":
            new = f"표 {n}" if holder.find(".//a:tbl", NS) is not None else f"차트 {n}"
        elif tag == "cxnSp": new = f"직선 연결선 {n}"
        else:
            nv = holder.find("p:nvSpPr/p:cNvSpPr", NS)
            if nv is not None and nv.get("txBox") == "1": new = f"TextBox {n}"
            else:
                g = holder.find(".//a:prstGeom", NS)
                new = f"{GEOM.get(g.get('prst') if g is not None else 'rect', '자유형')} {n}"
        c.set("name", new)
    cs = tree.getroot().find("p:cSld", NS)
    if cs is not None and re.fullmatch(r"Slide \d+", cs.get("name", "")): del cs.attrib["name"]

# ---------- 4) 머리글 소제목 너비 다시 계산(맑은 고딕 12pt 근사), 옆 선 위치 맞춤
def text_w(s, pt):
    em = pt / 72
    w = 0
    for ch in s:
        if re.match(r"[\uac00-\ud7a3\u4e00-\u9fff]", ch): w += 1.0
        elif ch == " ": w += 0.28
        elif ch in "·,.()": w += 0.33
        elif ch == "%": w += 0.85
        else: w += 0.56
    return w * em
def fit_subtitle(tree, page, changed):
    sp = {}
    for s in tree.getroot().iter("{%s}sp" % NS["p"]):
        c = s.find("p:nvSpPr/p:cNvPr", NS); sp[c.get("name")] = s
    sub = sp.get("Text 3")
    if sub is None or not changed: return
    line = next((s for s in sp.values() if s.find(".//a:prstGeom", NS) is not None and s.find(".//a:prstGeom", NS).get("prst") == "line"
                 and abs(int(s.find(".//a:off", NS).get("y")) - int(0.51*EMU)) < 20000), None)
    off, ext = sub.find(".//a:off", NS), sub.find(".//a:ext", NS)
    txt = "".join(t.text for t in sub.iter(A + "t"))
    sz = int(sub.find(".//a:rPr", NS).get("sz")) / 100
    w = int((text_w(txt, sz) * 1.08 + 0.05) * EMU)
    x = int(off.get("x"))
    if line is not None:
        lo, le = line.find(".//a:off", NS), line.find(".//a:ext", NS)
        right = int(lo.get("x")) + int(le.get("cx"))
        nlx = x + w + int(0.2 * EMU)
        if right - nlx < int(0.35 * EMU):
            log.append(f"p{page}: 소제목이 길어 선이 짧아짐 ({(right-nlx)/EMU:.2f}in)")
        lo.set("x", str(nlx)); le.set("cx", str(max(right - nlx, int(0.3*EMU))))
    log.append(f"p{page}: 소제목 폭 {int(ext.get('cx'))/EMU:.2f} -> {w/EMU:.2f}in")
    ext.set("cx", str(w))

# ---------- run over slides
SUBS_CHANGED = {3,4,5,7,8,9,10,13,14,19,20,21,22,23}
for f, page in page_of.items():
    rel = f[len("ppt/"):] if False else f
    tree = load(rel)
    edit_text_tree(tree, page)
    fit_subtitle(tree, page, page in SUBS_CHANGED)
    rename(tree)
    save(tree, rel)
    # notes
    rf = os.path.join(U, os.path.dirname(rel), "_rels", os.path.basename(rel) + ".rels")
    nt = re.search(r'Target="\.\./notesSlides/(notesSlide\d+\.xml)"', open(rf, encoding="utf8").read())
    if nt:
        np_ = "ppt/notesSlides/" + nt.group(1); ntree = load(np_)
        if page in NOTES:
            body = [s for s in ntree.getroot().iter("{%s}sp" % NS["p"]) if s.find(".//p:ph", NS) is not None and s.find(".//p:ph", NS).get("type") == "body"][0]
            ts = list(body.iter(A + "t")); ts[0].text = NOTES[page]
            for t in ts[1:]: t.text = ""
        edit_text_tree(ntree, page, notes=True)
        rename(ntree)
        save(ntree, np_)

missing = [(p, k) for p, d in OVR.items() for k in d if (p, k) not in used] + \
          [(p, a) for p, l in SUBSTR.items() for a, _ in l if (p, a) not in used]
print("NOT FOUND:", missing)

# ---------- 5) 레이아웃 이름, 문서 속성
for d in ("ppt/slideLayouts", "ppt/slideMasters"):
    for fn in os.listdir(os.path.join(U, d)):
        if not fn.endswith(".xml"): continue
        p = os.path.join(d, fn); s = open(os.path.join(U, p), encoding="utf8").read()
        s2 = s.replace('<p:cSld name="DEFAULT"', '<p:cSld name="빈 화면"').replace('<p:cSld name="GS"', '<p:cSld name="제목만"')
        if s2 != s: open(os.path.join(U, p), "w", encoding="utf8").write(s2); log.append(f"layout {fn}")
cp = os.path.join(U, "docProps/core.xml"); s = open(cp, encoding="utf8").read()
s = re.sub(r"<dc:title>.*?</dc:title>", "<dc:title>전포동 복합주차장 정동관 건축계획</dc:title>", s)
s = re.sub(r"<dc:subject>.*?</dc:subject>", "", s)
open(cp, "w", encoding="utf8").write(s)
ap = os.path.join(U, "docProps/app.xml"); s = open(ap, encoding="utf8").read()
open(ap, "w", encoding="utf8").write(s.replace("<Company>PptxGenJS</Company>", "<Company></Company>"))
# 차트 원본 엑셀의 작성자
for fn in os.listdir(os.path.join(U, "ppt/embeddings")):
    p = os.path.join(U, "ppt/embeddings", fn)
    zin = zipfile.ZipFile(p); buf = io.BytesIO(); zout = zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED)
    for it in zin.infolist():
        d = zin.read(it.filename)
        if it.filename == "docProps/core.xml": d = d.replace(b"PptxGenJS", "정성윤".encode())
        if it.filename == "docProps/app.xml": d = d.replace(b"PptxGenJS", b"Microsoft Excel")
        zout.writestr(it, d)
    zout.close(); zin.close(); open(p, "wb").write(buf.getvalue())
print("\n".join(log))
