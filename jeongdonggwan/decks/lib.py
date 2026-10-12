# -*- coding: utf-8 -*-
# slide HTML component library (공설기 v1.2 look) for the Slides artifact subset
import json, html
NAVY = '#002060'; GRAY = '#595959'; LINE = '#a0a2a5'; PANEL = '#f2f2f2'; HEAD = '#767171'; BAND1 = '#e7e6e6'; BAND2 = '#f0f3f7'
RED = '#ff0000'; GOLD = '#ffc000'; DARK = '#323232'
REG = "font-family:'Pretendard', Arial, sans-serif;"
BOLD = "font-family:'Pretendard Bold', Arial, sans-serif;"
XB = "font-family:'Pretendard ExtraBold', Arial, sans-serif;"
SERIF = "font-family:'Noto Serif KR', Georgia, serif;"
ASSET = {}
def esc(t): return html.escape(t, quote=False)
def blob(k): return '/_blob/' + ASSET[k]
SECTIONS = ['INTRODUCTION', 'MAIN SUBJECT', 'CONCLUSION']
def tabs(active):
    out = []
    for i, s in enumerate(SECTIONS):
        on = i == active
        out.append(f'<p style="{BOLD}font-size:24px;line-height:1.2;background:{NAVY if on else "#f2f2f2"};color:{"#ffffff" if on else "#8c8c8c"};padding:8px 24px">{s}</p>')
    return '<div style="display:flex;flex-direction:row;gap:6px">' + ''.join(out) + '</div>'
def header(n, title, sub, active, gap=8):
    return (f'<div style="display:flex;flex-direction:column;gap:{gap}px">'
            f'<div style="display:flex;flex-direction:row;align-items:center;gap:18px">'
            f'<p style="{XB}font-size:60px;line-height:1.1;color:{NAVY}">{n}</p>'
            f'<p style="{XB}font-size:36px;line-height:1.2;color:#000000">{esc(title)}</p>'
            f'<div style="width:9px;height:38px;background:{NAVY}"></div>'
            f'<p style="font-size:27px;line-height:1.3;color:{GRAY}">{esc(sub)}</p>'
            f'<div style="flex:1"></div>{tabs(active)}</div>'
            f'<div style="height:2px;background:{LINE}"></div></div>')
def footer(src, pg, tag='전포 정동관'):
    return (f'<hr style="position:absolute;left:72px;top:984px;width:1776px;border-top:2px solid {LINE}">'
            f'<p style="position:absolute;left:72px;top:996px;width:150px;{SERIF}font-size:36px;line-height:1.2;color:{NAVY}">停動館</p>'
            f'<p style="position:absolute;left:240px;top:996px;width:1290px;font-size:24px;line-height:1.3;color:{GRAY}">{esc(src)}</p>'
            f'<p style="position:absolute;left:1560px;top:996px;width:288px;font-size:24px;line-height:1.3;text-align:right;color:{GRAY}">{tag} · {pg}</p>')
def slide(sid, body, pad='48px 72px 120px', gap=20, bg='#ffffff', section=None, notes=None, extra_attr=''):
    d = f' data-section="{esc(section)}"' if section else ''
    a = f'<aside>{esc(notes)}</aside>' if notes else ''
    return (f'<section id="{sid}"{d}{extra_attr} style="background:{bg};color:#000000;{REG}padding:{pad};display:flex;flex-direction:column;gap:{gap}px">\n'
            f'{body}\n{a}</section>\n')
def ptitle(t, size=33, color=NAVY):
    return f'<p style="{BOLD}font-size:{size}px;line-height:1.3;border-left:9px solid {color};padding:0px 0px 0px 16px">{esc(t)}</p>'
def ptext(t, size=26, color='#000000', bold=False, lh=1.4, extra=''):
    return f'<p style="{BOLD if bold else ""}font-size:{size}px;line-height:{lh};color:{color};{extra}">{t}</p>'
def table(heads, widths, rows, size=24, aligns=None, bold_rows=(), lh=1.3, bands=(BAND1, BAND2), band_by=None, color_cols=None, pad=None):
    aligns = aligns or ['left'] * len(heads)
    pd = f';padding:{pad}' if pad else ''
    th = ''.join(f'<th style="width:{w}%;text-align:{a};color:#ffffff{pd}">{esc(h)}</th>' for h, w, a in zip(heads, widths, aligns))
    trs = [f'<tr style="background:{HEAD}">{th}</tr>']
    for i, r in enumerate(rows):
        bg = bands[(band_by[i] if band_by else i) % 2]
        tds = []
        for j, (c, a) in enumerate(zip(r, aligns)):
            st = f'text-align:{a}'
            if (i in bold_rows): st += ';font-weight:700'
            if pad: st += ';padding:' + pad
            tds.append(f'<td style="{st}">{c}</td>')
        trs.append(f'<tr style="background:{bg}">' + ''.join(tds) + '</tr>')
    return f'<table style="font-size:{size}px;line-height:{lh};color:#000000">' + ''.join(trs) + '</table>'
def box(label, lines, color=NAVY, size=26, title=None, bg=PANEL, lh=1.45, pad='16px 26px 18px', w=None):
    st = f'width:{w}px;' if w else ''
    parts = [f'<div style="display:flex;flex-direction:column;gap:7px;background:{bg};padding:{pad};{st}">']
    if label: parts.append(f'<div style="display:flex;flex-direction:row"><p style="{BOLD}font-size:{size + 1}px;line-height:1.3;background:{color};color:#ffffff;padding:3px 22px">{esc(label)}</p></div>')
    if title: parts.append(f'<p style="{BOLD}font-size:{size + 1}px;line-height:1.4">{title}</p>')
    for l in lines: parts.append(f'<p style="font-size:{size}px;line-height:{lh}">{l}</p>')
    parts.append('</div>'); return ''.join(parts)
def check(text, label='Check', size=26):
    return (f'<div style="display:flex;flex-direction:column;gap:6px;background:{DARK};padding:16px 26px 20px">'
            f'<p style="{BOLD}font-size:{size + 1}px;line-height:1.3;color:#ffffff">{label}</p>'
            f'<p style="font-size:{size}px;line-height:1.45;color:#ffffff">{text}</p></div>')
def take(text, size=27, w=None):
    st = f'width:{w}px;' if w else ''
    return f'<p style="{st}font-size:{size}px;line-height:1.4;color:{RED};font-weight:700">→ {text}</p>'
def img(k, w, h, fit='cover', alt='', bg=None, extra=''):
    b = f'background:{bg};' if bg else ''
    return f'<img src="{blob(k)}" alt="{esc(alt)}" style="width:{w}px;height:{h}px;object-fit:{fit};{b}{extra}">'
def cap(t, w=None, align='right'):
    st = f'width:{w}px;' if w else ''
    return f'<p style="{st}font-size:24px;line-height:1.4;font-style:italic;color:{GRAY};text-align:{align}">{esc(t)}</p>'
def row(children, gap=24, align=None, extra=''):
    a = f'align-items:{align};' if align else ''
    return f'<div style="display:flex;flex-direction:row;gap:{gap}px;{a}{extra}">' + ''.join(children) + '</div>'
def col(children, gap=14, extra=''):
    return f'<div style="display:flex;flex-direction:column;gap:{gap}px;{extra}">' + ''.join(children) + '</div>'
def grid(cols, children, gap=24, extra=''):
    return f'<div style="display:grid;grid-template-columns:{cols};gap:{gap}px;{extra}">' + ''.join(children) + '</div>'
def pill(t, bg=NAVY, color='#ffffff', size=26):
    return f'<p style="{BOLD}font-size:{size}px;line-height:1.3;background:{bg};color:{color};padding:3px 20px">{esc(t)}</p>'
def divider(sid, active, items, bg_img, section_desc):
    # progress page: three numbered chapters with the current one highlighted
    out = []
    for i, (name, lines) in enumerate(items):
        on = i == active
        op = '' if on else 'opacity:0.3;'
        stroke = NAVY if on else '#8c8c8c'
        ls = ''.join(f'<p style="font-size:30px;line-height:1.55">- {esc(l)}</p>' for l in lines)
        out.append(f'<div style="display:flex;flex-direction:row;gap:30px;align-items:flex-start;width:1180px;{op}">'
                   f'<p style="{XB}font-size:96px;line-height:1;width:170px;flex:none;color:#ffffff;-webkit-text-stroke:3px {stroke}">0{i + 1}</p>'
                   f'<div style="display:flex;flex-direction:column;gap:8px;padding:6px 0px 0px"><p style="{XB}font-size:44px;line-height:1.2;letter-spacing:-1px;color:{NAVY}">{name}</p>{ls}</div></div>')
    body = (f'<img src="{blob(bg_img)}" alt="" style="position:absolute;left:1320px;top:0px;width:600px;height:1080px;object-fit:cover">'
            f'<p style="position:absolute;left:1320px;top:900px;width:560px;{SERIF}font-size:150px;line-height:1;text-align:right;white-space:nowrap;color:#ffffff;opacity:0.7">停動館</p>' + ''.join(out))
    return (f'<section id="{sid}" data-section="{esc(section_desc)}" style="background:#ffffff;color:#000000;{REG}padding:150px 0px 0px 96px;display:flex;flex-direction:column;gap:46px">\n{body}\n</section>\n')
def barchart(items, w=700, h=300, maxv=150, ref=130, color_main=NAVY, color_alt='#8493b2'):
    # items: (label, value, color) ; returns relative-positioned div
    n = len(items); bw = int((w - 120) / n * 0.62); gap = int((w - 120) / n)
    y = lambda v: int(h - v / maxv * h)
    parts = [f'<div style="position:relative;width:{w}px;height:{h + 62}px">']
    parts.append(f'<div style="position:absolute;left:100px;top:{y(ref)}px;width:{w - 110}px;height:2px;background:#595959"></div>')
    parts.append(f'<p style="position:absolute;left:0px;top:{y(ref) - 14}px;width:96px;font-size:24px;line-height:1.2;text-align:right;color:{GRAY}">{ref}%</p>')
    for i, (lab, v, c) in enumerate(items):
        x = 110 + i * gap + int((gap - bw) / 2)
        parts.append(f'<div style="position:absolute;left:{x}px;top:{y(v)}px;width:{bw}px;height:{h - y(v)}px;background:{c}"></div>')
        parts.append(f'<p style="position:absolute;left:{x - 10}px;top:{y(v) + 10}px;width:{bw + 20}px;{BOLD}font-size:30px;line-height:1.2;text-align:center;color:#ffffff">{v}%</p>')
        parts.append(f'<p style="position:absolute;left:{x - 24}px;top:{h + 8}px;width:{bw + 48}px;font-size:24px;line-height:1.25;text-align:center">{esc(lab)}</p>')
    parts.append('</div>'); return ''.join(parts)
