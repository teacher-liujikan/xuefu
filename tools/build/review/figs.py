# -*- coding: utf-8 -*-
"""Shared builders for the scaffolded A4 worksheets (作答單)."""
import io, base64, math, qrcode


def qr_data(txt):
    q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=8, border=1)
    q.add_data(txt.encode('utf-8')); q.make(fit=True)
    b = io.BytesIO(); q.make_image().save(b, format='PNG')
    return base64.b64encode(b.getvalue()).decode(), q.version

# ---------- inline pieces ----------
B = '<span class="bx"></span>'            # write-in box
BS = '<span class="bx s"></span>'         # small box (digits)
O = '<span class="op"></span>'            # operator circle (fill + − × ＞ ＜ ＝)
def L(w=None): return f'<span class="ln"{f" style=\"min-width:{w}mm\"" if w else ""}></span>'
def H(t): return f'<span class="hint">{t}</span>'
def CH(*opts): return '<span class="choice">' + ''.join(f'<span>{o}</span>' for o in opts) + '</span>'
def row(tag, body): return f'<div class="row"><span class="tagc">{tag}</span>{body}</div>'
def prob(q, rows, fig=''):
    return f'<div class="prob"><div class="q">{q}</div>{fig}{"".join(rows)}</div>'
def two(*probs): return '<div class="two">' + ''.join(probs) + '</div>'
def three(*probs): return '<div class="three">' + ''.join(probs) + '</div>'
def lvl(n, title, note): return f'<div class="lvl"><i>{n}</i>{title} <small>{note}</small></div>'
def steps(*s): return '<div class="steps">' + ''.join(f'<div class="st"><b>{a}</b>{b}</div>' for a, b in s) + '</div>'
def example(*lines): return '<div class="ex">' + ''.join(f'<div{" class=\"q\"" if i == 0 else ""}>{l}</div>' for i, l in enumerate(lines)) + '</div>'
def check(*items): return '<div class="check"><div class="ck-h">寫完自己檢查，做到了就打勾：</div>' + ''.join(f'<div>{i}</div>' for i in items) + '</div>'
def drawbox(label, h=40): return f'<div class="draw" style="height:{h}mm"><span>{label}</span></div>'

# ---------- figures (SVG, sized in mm so they print at true scale) ----------
def svg(w, h, body, cls='fig'):
    return f'<svg class="{cls}" style="max-width:100%;height:auto" width="{w}mm" height="{h}mm" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">{body}</svg>'
T = lambda x, y, t, s=4, a='middle', w='600', fill='#1b2a30': f'<text x="{x}" y="{y}" font-size="{s}" text-anchor="{a}" font-weight="{w}" fill="{fill}" font-family="Noto Sans CJK TC, sans-serif">{t}</text>'

def blocks(h, t, o):
    """base-ten blocks: h flats, t rods, o units"""
    parts = []; x = 2
    for _ in range(h):
        g = ''.join(f'<line x1="{x}" y1="{2+i*1.4}" x2="{x+14}" y2="{2+i*1.4}" stroke="#7a8c90" stroke-width=".15"/><line x1="{x+i*1.4}" y1="2" x2="{x+i*1.4}" y2="16" stroke="#7a8c90" stroke-width=".15"/>' for i in range(11))
        parts.append(f'<rect x="{x}" y="2" width="14" height="14" fill="#cfe0ff" stroke="#1b2a30" stroke-width=".35"/>' + g); x += 16
    x += 3
    for _ in range(t):
        g = ''.join(f'<line x1="{x}" y1="{2+i*1.4}" x2="{x+1.6}" y2="{2+i*1.4}" stroke="#7a8c90" stroke-width=".15"/>' for i in range(11))
        parts.append(f'<rect x="{x}" y="2" width="1.6" height="14" fill="#ffd3a6" stroke="#1b2a30" stroke-width=".3"/>' + g); x += 2.6
    x += 3
    for k in range(o):
        parts.append(f'<rect x="{x+(k%5)*2.4}" y="{12.4-(k//5)*2.4}" width="1.6" height="1.6" fill="#fff" stroke="#1b2a30" stroke-width=".3"/>')
    x += 13
    return svg(max(x, 30), 18, ''.join(parts))

def clock(h=None, m=None, size=34):
    c = size / 2; r = c - 1.2; out = [f'<circle cx="{c}" cy="{c}" r="{r}" fill="#fff" stroke="#1b2a30" stroke-width=".8"/>']
    for i in range(60):
        a = math.radians(i * 6); big = i % 5 == 0; r1 = r - (2.2 if big else 1.1)
        out.append(f'<line x1="{c+r1*math.sin(a):.2f}" y1="{c-r1*math.cos(a):.2f}" x2="{c+r*math.sin(a):.2f}" y2="{c-r*math.cos(a):.2f}" stroke="#1b2a30" stroke-width="{.45 if big else .2}"/>')
    for n in range(1, 13):
        a = math.radians(n * 30); rr = r - 5
        out.append(T(f'{c+rr*math.sin(a):.2f}', f'{c-rr*math.cos(a)+1.4:.2f}', n, size * 0.11))
    if h is not None:
        ha = math.radians(((h % 12) + m / 60) * 30); ma = math.radians(m * 6)
        out.append(f'<line x1="{c}" y1="{c}" x2="{c+r*0.5*math.sin(ha):.2f}" y2="{c-r*0.5*math.cos(ha):.2f}" stroke="#1b2a30" stroke-width="1.6" stroke-linecap="round"/>')
        out.append(f'<line x1="{c}" y1="{c}" x2="{c+r*0.82*math.sin(ma):.2f}" y2="{c-r*0.82*math.cos(ma):.2f}" stroke="#0B8577" stroke-width=".9" stroke-linecap="round"/>')
    out.append(f'<circle cx="{c}" cy="{c}" r="1" fill="#1b2a30"/>')
    return svg(size, size, ''.join(out))

def ruler(a, b, label='', length=12):
    """object bar from a cm to b cm drawn above a true-scale ruler (1 cm = 10 mm)"""
    W = length * 10 + 10; X = lambda cm: 5 + cm * 10
    out = []
    if b is not None:
        out.append(f'<rect x="{X(a)}" y="2" width="{(b-a)*10}" height="5" rx="1" fill="#9fd9cc" stroke="#1b2a30" stroke-width=".35"/>')
        if label: out.append(T(X(a) + (b - a) * 5, 6, label, 3.2))
        out.append(f'<line x1="{X(a)}" y1="7" x2="{X(a)}" y2="10" stroke="#5c6e74" stroke-width=".25" stroke-dasharray=".8 .6"/><line x1="{X(b)}" y1="7" x2="{X(b)}" y2="10" stroke="#5c6e74" stroke-width=".25" stroke-dasharray=".8 .6"/>')
    out.append(f'<rect x="1" y="10" width="{W-2}" height="12" fill="#fbf1cf" stroke="#1b2a30" stroke-width=".35"/>')
    for i in range(length * 10 + 1):
        x = 5 + i; big = i % 10 == 0; mid = i % 5 == 0
        out.append(f'<line x1="{x}" y1="10" x2="{x}" y2="{10+(4.5 if big else 3 if mid else 1.8)}" stroke="#1b2a30" stroke-width="{.3 if big else .15}"/>')
        if big: out.append(T(x, 20, i // 10, 3.2))
    return svg(W, 23, ''.join(out))

def line_cm(cm, label=''):
    w = cm * 10 + 30
    return svg(w, 8, f'<line x1="5" y1="4" x2="{5+cm*10}" y2="4" stroke="#1b2a30" stroke-width=".7"/><line x1="5" y1="1.5" x2="5" y2="6.5" stroke="#1b2a30" stroke-width=".5"/><line x1="{5+cm*10}" y1="1.5" x2="{5+cm*10}" y2="6.5" stroke="#1b2a30" stroke-width=".5"/>' + (T(12 + cm * 10, 5.5, label, 3.4, 'start') if label else ''))

def balance(left, right, tilt):
    """tilt: -1 left heavier (left low), 1 right low, 0 level"""
    a = tilt * 10; C = 35
    def side(dx, name):
        rad = math.radians(a); x = C + dx * math.cos(rad); y = 10 + dx * math.sin(rad)
        return (f'<line x1="{x:.2f}" y1="{y:.2f}" x2="{x:.2f}" y2="{y+7:.2f}" stroke="#1b2a30" stroke-width=".3"/>'
                f'<path d="M{x-9:.2f} {y+7:.2f} H{x+9:.2f} L{x+7:.2f} {y+9:.2f} H{x-7:.2f} Z" fill="#eef3f2" stroke="#1b2a30" stroke-width=".35"/>'
                + T(f'{x:.2f}', f'{y+5:.2f}', name, 3.2))
    return svg(70, 30, f'<path d="M{C} 10 L{C-6} 29 H{C+6} Z" fill="#eef3f2" stroke="#1b2a30" stroke-width=".4"/>'
               f'<g transform="rotate({a} {C} 10)"><rect x="{C-27}" y="9" width="54" height="2" rx="1" fill="#5c6e74"/></g><circle cx="{C}" cy="10" r="1.1" fill="#1b2a30"/>'
               + side(-25, left) + side(25, right))

def cups(levels, widths=None, labels=None, h=26):
    widths = widths or [14] * len(levels); labels = labels or ['甲', '乙', '丙'][:len(levels)]
    out = []; x = 4
    for lv, w, lab in zip(levels, widths, labels):
        y = 3; wy = y + h * (1 - lv)
        out.append(f'<rect x="{x}" y="{wy:.2f}" width="{w}" height="{y+h-wy:.2f}" fill="#bfe1f7"/><path d="M{x} {y} V{y+h} H{x+w} V{y}" fill="none" stroke="#1b2a30" stroke-width=".55"/>' + T(x + w / 2, y + h + 5, lab, 3.6))
        x += w + 10
    return svg(x, h + 9, ''.join(out))

def smallcups(n, label):
    out = [T(3, 6, label, 3.6, 'start')]
    for i in range(n):
        x = 12 + i * 7
        out.append(f'<path d="M{x} 1.5 L{x+1} 8 H{x+4.5} L{x+5.5} 1.5" fill="#bfe1f7" stroke="#1b2a30" stroke-width=".35"/>')
    return svg(14 + n * 7, 10, ''.join(out))

def money(items):
    """items: list of denominations; notes as rectangles, coins as circles (labelled, not real designs)"""
    out = []; x = 2
    for d in items:
        if d >= 100:
            out.append(f'<rect x="{x}" y="2" width="18" height="10" rx="1" fill="{ {1000:"#c9dcf5",500:"#e6cfb3",100:"#f5c6c1"}[d] }" stroke="#1b2a30" stroke-width=".35"/>' + T(x + 9, 8.6, d, 3.6)); x += 20
        else:
            r = {50: 5.2, 10: 4.6, 5: 4, 1: 3.4}[d]
            out.append(f'<circle cx="{x+r}" cy="7" r="{r}" fill="{ {50:"#f2d27a",10:"#e9cf8a",5:"#dfe3e6",1:"#e0b391"}[d] }" stroke="#1b2a30" stroke-width=".35"/>' + T(x + r, 8.3, d, 3)); x += 2 * r + 2
    return svg(x + 2, 14, ''.join(out))

def bar(whole, a, b):
    """bar model: whole on top, two parts below; pass '( )' for the unknown"""
    W = 120
    pa = 0.45
    return svg(W, 26, f'<path d="M5 7 V4 H{W-5} V7" fill="none" stroke="#5c6e74" stroke-width=".35"/>' + T(W / 2, 3.2, whole, 3.8)
               + f'<rect x="5" y="9" width="{(W-10)*pa}" height="6" fill="#cfeee6" stroke="#1b2a30" stroke-width=".4"/><rect x="{5+(W-10)*pa}" y="9" width="{(W-10)*(1-pa)}" height="6" fill="#fde3c4" stroke="#1b2a30" stroke-width=".4"/>'
               + f'<path d="M5 17 V19 H{5+(W-10)*pa-1} V17 M{5+(W-10)*pa+1} 17 V19 H{W-5} V17" fill="none" stroke="#5c6e74" stroke-width=".35"/>'
               + T(5 + (W - 10) * pa / 2, 24, a, 3.8) + T(5 + (W - 10) * pa + (W - 10) * (1 - pa) / 2, 24, b, 3.8))

def shape(kind, labels=None, w=40, h=30, marks=None):
    labels = labels or []
    if kind == 'tri': pts = [(w/2, 3), (w-3, h-3), (3, h-3)]
    elif kind == 'eqtri': pts = [(w/2, 3), (w-4, h-3), (4, h-3)]
    elif kind == 'rect': pts = [(4, 4), (w-4, 4), (w-4, h-4), (4, h-4)]
    elif kind == 'square': pts = [(4, 4), (h-4, 4), (h-4, h-4), (4, h-4)]
    elif kind == 'pent': pts = [(w/2, 3), (w-4, h*0.42), (w-9, h-3), (9, h-3), (4, h*0.42)]
    elif kind == 'quad': pts = [(8, 5), (w-4, 3), (w-10, h-4), (4, h-8)]
    else: pts = kind
    mx = max(p[0] for p in pts) + 4; my = max(p[1] for p in pts) + 4
    cx = sum(p[0] for p in pts) / len(pts); cy = sum(p[1] for p in pts) / len(pts)
    out = [f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x,y in pts)}" fill="#fff4d9" stroke="#1b2a30" stroke-width=".55"/>']
    for i, t in labels:
        (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % len(pts)]
        mxp, myp = (x1 + x2) / 2, (y1 + y2) / 2; dx, dy = mxp - cx, myp - cy; d = math.hypot(dx, dy) or 1
        k = 4.5 + abs(dx / d) * 5; out.append(T(f'{mxp+dx/d*k:.1f}', f'{myp+dy/d*k+1.2:.1f}', t, 3.2))
    if marks: out.append(marks)
    pad = 12 if labels else 0
    return svg(mx + 8 + 2 * pad, my + 4 + pad * 1.2, f'<g transform="translate({pad},{pad*0.6})">' + ''.join(out) + '</g>')

def vgrid(a=None, op='+', b=None):
    """vertical calculation grid: 百 十 一 columns, carry boxes on top, answer boxes at bottom"""
    def digits(n):
        if n is None: return ['', '', '']
        s = str(n).rjust(3); return [c.strip() for c in s]
    A, Bd = digits(a), digits(b)
    cell = lambda v, cls='': f'<td class="{cls}">{v}</td>'
    return ('<table class="vg"><tr class="hd"><td></td><td>百</td><td>十</td><td>一</td></tr>'
            '<tr class="cy"><td></td>' + ''.join(cell('<span class="cbx"></span>') for _ in range(3)) + '</tr>'
            '<tr><td></td>' + ''.join(cell(d, 'w' if a is None else '') for d in A) + '</tr>'
            f'<tr><td class="o">{"＋" if op=="+" else "－" if op=="-" else ""}</td>' + ''.join(cell(d, 'w' if b is None else '') for d in Bd) + '</tr>'
            '<tr class="ans"><td></td>' + ''.join(cell('') for _ in range(3)) + '</tr></table>')

def pvt(n=None):
    d = [c for c in str(n)] if n else ['', '', '']
    return ('<table class="pv"><tr><th>百位</th><th>十位</th><th>個位</th></tr>'
            '<tr class="sym"><td>100</td><td>⑩</td><td>①</td></tr><tr class="w"><td></td><td></td><td></td></tr></table>')

def page(blocks_html, first=False, meta='', title='', qr=None, header=''):
    if first:
        head = (f'<div class="head"><div><div class="meta">{meta}</div><h1>{title}</h1></div>'
                f'<div class="hr"><div class="fields col"><div>姓名 <span></span></div><div>日期 <span></span></div></div>'
                f'<figure class="qr"><img src="data:image/png;base64,{qr}" alt="解答 QR code"><figcaption>老師掃描看解答</figcaption></figure></div></div>')
    else:
        head = f'<div class="head"><div><div class="meta">{meta}</div><h1>{header}</h1></div><div class="fields">姓名 <span></span></div></div>'
    return f'<section class="page">{head}{"".join(blocks_html)}</section>'

def doc(title, pages):
    return f'<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><title>{title}</title><style>{CSS}</style></head><body>{"".join(pages)}</body></html>'
