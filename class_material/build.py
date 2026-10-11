"""Re-layout a 16:9 slide PDF onto A4: drop title bar / footer / chapter covers,
crop each slide to its content and flow the tiles in columns.
Pages are placed as vector form XObjects, so photos are not re-encoded."""
import sys
import numpy as np
import pymupdf

SRC, OUT, MODE = sys.argv[1], sys.argv[2], sys.argv[3]
DIVIDERS = {0, 14, 39, 59, 82, 111}      # title-only chapter covers
BROKEN = {128, 129}                      # source slides are a blank white / solid black box
BAR_BOTTOM = 58                          # blue title bar ends here (pt)
PAD_BOTTOM = 8
MIN_H = 60
X0, X1 = 30, 860                         # side trim (pt): real content spans ~37-850

LAYOUT = {
    # name: (page w, page h, margin, gutter, columns)
    "landscape2": (842, 595, 18, 8, 2),
    "portrait2": (595, 842, 14, 6, 2),
}[MODE]
PW, PH, M, G, NCOL = LAYOUT
COLW = (PW - 2 * M - (NCOL - 1) * G) / NCOL
SCALE = COLW / (X1 - X0)
GAP = 5

def is_footer(x0, y0, x1, y1):
    # lab logo / caption at bottom-left, speaker icon (~48pt square, any x) at the bottom
    return y0 >= 470 and (x1 <= 215 or ((x1 - x0) <= 60 and (y1 - y0) <= 60))


src = pymupdf.open(SRC)

# drop footer logo / speaker icons (shared or per-page xrefs) from the in-memory copy
for p in src:
    for im in p.get_image_info(xrefs=True):
        if is_footer(*im["bbox"]) and im["xref"]:
            p.delete_image(im["xref"])
    spans = [pymupdf.Rect(sp["bbox"]) for b in p.get_text("dict")["blocks"] for l in b.get("lines", [])
             for sp in l["spans"] if is_footer(*sp["bbox"])]
    for r in spans:
        p.add_redact_annot(r, fill=False)
    if spans:
        p.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE)


def has_bar(p):
    pm = p.get_pixmap(dpi=72, clip=pymupdf.Rect(870, 40, 890, 50))
    a = np.frombuffer(pm.samples, np.uint8).reshape(pm.h, pm.w, pm.n)[:, :, :3].astype(int).mean(axis=(0, 1))
    return a[2] - a[0] > 60 and a[0] < 90


def content_box(p):
    top_floor = BAR_BOTTOM if has_bar(p) else 0
    ys0, ys1 = [], []
    full = p.rect
    for b in p.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                if not s["text"].strip():
                    continue
                x0, y0, x1, y1 = s["bbox"]
                if y1 <= top_floor or is_footer(x0, y0, x1, y1) or y0 > 525:
                    continue
                ys0.append(y0); ys1.append(y1)
    for im in p.get_image_info():
        x0, y0, x1, y1 = im["bbox"]
        if (x1 - x0) > 900 and (y1 - y0) > 500:      # full-page background
            continue
        if is_footer(x0, y0, x1, y1) or y1 <= top_floor:
            continue
        ys0.append(y0); ys1.append(y1)
    for d in p.get_drawings():
        r = d["rect"]
        if r.width > 900 and r.height > 450:
            continue
        if is_footer(r.x0, r.y0, r.x1, r.y1) or r.y1 <= top_floor or r.y0 > 525:
            continue
        ys0.append(r.y0); ys1.append(r.y1)
    if not ys1:
        return None
    top = max(top_floor, min(ys0) - 6)
    bottom = min(max(ys1) + PAD_BOTTOM, 530)
    bottom = max(bottom, top + MIN_H)
    return pymupdf.Rect(X0, top, X1, bottom)


tiles = []
for i, p in enumerate(src):
    if i in DIVIDERS or i in BROKEN:
        continue
    box = content_box(p)
    if box is None:
        print("skip empty", i)
        continue
    tiles.append((i, box))

out = pymupdf.open()
page = None
col = 0
y = M


def new_page():
    global page, col, y
    page = out.new_page(width=PW, height=PH)
    col, y = 0, M


new_page()
placed = 0
for i, box in tiles:
    h = box.height * SCALE
    if y + h > PH - M + 0.01:
        col += 1
        y = M
        if col >= NCOL:
            new_page()
    x = M + col * (COLW + G)
    rect = pymupdf.Rect(x, y, x + COLW, y + h)
    page.show_pdf_page(rect, src, i, clip=box)
    page.draw_rect(rect, color=(0.6, 0.6, 0.6), width=0.4)
    y += h + GAP
    placed += 1

out.save(OUT, garbage=4, deflate=True, clean=True)
print(f"{MODE}: {placed} slides -> {len(out)} pages, scale {SCALE:.3f}, "
      f"body text ~{18 * SCALE:.1f}pt, size {round(__import__('os').path.getsize(OUT) / 1e6, 2)}MB")
