# -*- coding: utf-8 -*-
"""Minimal hand-rolled SVG chart library for the Tesla Robotaxi report.
No external deps. Every chart returns an inline <svg> string."""

import math

# ---- design tokens (mirrored in CSS) ----
INK      = '#12161c'
INK_SOFT = '#4a5462'
MUTED    = '#8b95a3'
GRID     = '#e4e8ee'
PANEL    = '#ffffff'
ACCENT   = '#c8452d'   # tesla-ish red
ACCENT2  = '#1f6feb'   # blue
ACCENT3  = '#0f9d58'   # green
ACCENT4  = '#b8860b'   # amber
ACCENT5  = '#7b4fd6'   # violet
GREY     = '#b6bec9'
SERIES   = [ACCENT, ACCENT2, ACCENT3, ACCENT4, ACCENT5, '#0d8a9e', '#d1477a']

FONT = "font-family='-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica Neue,Helvetica,Arial,PingFang SC,Hiragino Sans GB,Microsoft YaHei,sans-serif'"


def esc(s):
    return (str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))


def _nice(v):
    """nice axis maximum"""
    if v <= 0:
        return 1.0
    e = math.floor(math.log10(v))
    f = v / (10 ** e)
    for m in (1, 1.2, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10):
        if f <= m:
            return m * (10 ** e)
    return 10 ** (e + 1)


def _fmt(v, dec=0):
    s = f'{v:,.{dec}f}'
    return s


def svg_open(w, h, cls='chart'):
    return (f"<svg class='{cls}' viewBox='0 0 {w} {h}' width='100%' "
            f"preserveAspectRatio='xMidYMid meet' role='img' {FONT}>")


def defs():
    """shared defs: subtle grid pattern + arrow"""
    return ("<defs>"
            "<linearGradient id='gA' x1='0' y1='0' x2='0' y2='1'>"
            f"<stop offset='0%' stop-color='{ACCENT}' stop-opacity='0.95'/>"
            f"<stop offset='100%' stop-color='{ACCENT}' stop-opacity='0.55'/></linearGradient>"
            "<linearGradient id='gB' x1='0' y1='0' x2='0' y2='1'>"
            f"<stop offset='0%' stop-color='{ACCENT2}' stop-opacity='0.95'/>"
            f"<stop offset='100%' stop-color='{ACCENT2}' stop-opacity='0.55'/></linearGradient>"
            "</defs>")


def axis_text(x, y, s, size=12, fill=None, anchor='middle', weight='400', rot=None):
    fill = fill or MUTED
    tr = f" transform='rotate({rot} {x} {y})'" if rot else ''
    return (f"<text x='{x:.1f}' y='{y:.1f}' font-size='{size}' fill='{fill}' "
            f"text-anchor='{anchor}' font-weight='{weight}'{tr}>{esc(s)}</text>")


def ygrid(x0, x1, y_top, y_bot, vmax, ticks=5, unit='', dec=0, fmt=None):
    out = []
    for i in range(ticks + 1):
        v = vmax * i / ticks
        y = y_bot - (y_bot - y_top) * i / ticks
        out.append(f"<line x1='{x0:.1f}' y1='{y:.1f}' x2='{x1:.1f}' y2='{y:.1f}' "
                   f"stroke='{GRID}' stroke-width='1'/>")
        lab = fmt(v) if fmt else _fmt(v, dec) + unit
        out.append(axis_text(x0 - 10, y + 4, lab, 11, MUTED, 'end'))
    return ''.join(out)


def xlabels(x0, x1, labels, y, size=11, rot=None, anchor='middle'):
    n = len(labels)
    step = (x1 - x0) / n
    out = []
    for i, l in enumerate(labels):
        cx = x0 + step * (i + 0.5)
        out.append(axis_text(cx, y, l, size, MUTED, anchor, rot=rot))
    return ''.join(out)


# ------------------------------------------------------------------ bars
def bars(labels, series, w=1120, h=390, pad=(64, 24, 54, 16), colors=None,
         unit='', dec=0, stack=False, legend=True, ymax=None, annots=None,
         ylab=None, value_labels=False, val_fmt=None):
    """series: list of (name, [values]). stack=True stacks them."""
    x0, x1 = pad[0], w - pad[1]
    ytop, ybot = pad[3], h - pad[2]
    colors = colors or SERIES
    n = len(labels)
    step = (x1 - x0) / n
    if stack:
        tot = [sum(s[1][i] for s in series) for i in range(n)]
        vmax = ymax or _nice(max(tot) * 1.12)
    else:
        vmax = ymax or _nice(max(max(s[1]) for s in series) * 1.18)
    sc = (ybot - ytop) / vmax
    o = [svg_open(w, h), defs()]
    o.append(ygrid(x0, x1, ytop, ybot, vmax, 5, unit, dec))
    if ylab:
        o.append(axis_text(pad[0] - 48, ytop - 12, ylab, 11, MUTED, 'start'))
    bw = step * (0.62 if not stack else 0.5)
    if not stack:
        bw = step * 0.66 / len(series)
    for i in range(n):
        cx = x0 + step * (i + 0.5)
        if stack:
            acc = 0.0
            for si, (nm, vs) in enumerate(series):
                v = vs[i] or 0
                hh = v * sc
                y = ybot - (acc + v) * sc
                o.append(f"<rect x='{cx-bw/2:.1f}' y='{y:.1f}' width='{bw:.1f}' height='{max(hh,0):.1f}' "
                         f"fill='{colors[si % len(colors)]}' fill-opacity='{0.92 if si==0 else 0.86}'/>")
                acc += v
        else:
            start = cx - (bw * len(series)) / 2
            for si, (nm, vs) in enumerate(series):
                v = vs[i] or 0
                hh = v * sc
                x = start + si * bw
                o.append(f"<rect x='{x:.1f}' y='{ybot-hh:.1f}' width='{bw*0.86:.1f}' height='{max(hh,0):.1f}' "
                         f"fill='{colors[si % len(colors)]}' fill-opacity='0.9'/>")
                if value_labels and v:
                    lab = val_fmt(v) if val_fmt else _fmt(v, dec)
                    o.append(axis_text(x + bw * 0.43, ybot - hh - 6, lab, 10, INK_SOFT, 'middle', '600'))
    o.append(f"<line x1='{x0:.1f}' y1='{ybot:.1f}' x2='{x1:.1f}' y2='{ybot:.1f}' stroke='{GREY}' stroke-width='1.2'/>")
    o.append(xlabels(x0, x1, labels, ybot + 20))
    if legend and len(series) > 1:
        lx = x0
        ly = h - 12
        for si, (nm, _) in enumerate(series):
            o.append(f"<rect x='{lx:.1f}' y='{ly-9:.1f}' width='11' height='11' rx='2' fill='{colors[si % len(colors)]}' fill-opacity='0.9'/>")
            o.append(axis_text(lx + 16, ly, nm, 11, INK_SOFT, 'start'))
            lx += 22 + len(nm) * 12.2
    if annots:
        for (ax, ay, txt, col) in annots:
            o.append(axis_text(ax, ay, txt, 11, col or ACCENT, 'start', '600'))
    o.append('</svg>')
    return ''.join(o)


# ------------------------------------------------------------------ lines
def lines(labels, series, w=1120, h=380, pad=(64, 24, 54, 16), colors=None,
          unit='', dec=1, ymax=None, ymin=None, legend=True, markers=True,
          fill_first=False, band=None, annots=None, dash_for=(), ylab=None):
    x0, x1 = pad[0], w - pad[1]
    ytop, ybot = pad[3], h - pad[2]
    colors = colors or SERIES
    allv = [v for _, vs in series for v in vs if v is not None]
    hi = max(allv)
    lo = min(0 if ymin is None else ymin, min(allv))
    vmax = ymax or _nice(hi * 1.12)
    vmin = ymin if ymin is not None else 0
    sc = (ybot - ytop) / (vmax - vmin)
    n = len(labels)
    def X(i): return x0 + (x1 - x0) * (i / (n - 1) if n > 1 else 0.5)
    def Y(v): return ybot - (v - vmin) * sc
    o = [svg_open(w, h), defs()]
    o.append(ygrid(x0, x1, ytop, ybot, vmax - vmin, 5, unit, dec))
    if ymin is not None and ymin < 0:
        o.append(f"<line x1='{x0:.1f}' y1='{Y(0):.1f}' x2='{x1:.1f}' y2='{Y(0):.1f}' stroke='{GREY}' stroke-width='1.3'/>")
    if ylab:
        o.append(axis_text(pad[0] - 48, ytop - 12, ylab, 11, MUTED, 'start'))
    for si, (nm, vs) in enumerate(series):
        pts = [(X(i), Y(v)) for i, v in enumerate(vs) if v is not None]
        d = ' '.join(f"{'M' if k==0 else 'L'}{x:.1f},{y:.1f}" for k, (x, y) in enumerate(pts))
        dash = " stroke-dasharray='6 4'" if nm in dash_for else ''
        if fill_first and si == 0 and pts:
            area = d + f" L{pts[-1][0]:.1f},{Y(vmin):.1f} L{pts[0][0]:.1f},{Y(vmin):.1f} Z"
            o.append(f"<path d='{area}' fill='{colors[si]}' fill-opacity='0.10'/>")
        o.append(f"<path d='{d}' fill='none' stroke='{colors[si % len(colors)]}' stroke-width='2.6'{dash} "
                 f"stroke-linejoin='round' stroke-linecap='round'/>")
        if markers:
            for x, y in pts:
                o.append(f"<circle cx='{x:.1f}' cy='{y:.1f}' r='3.4' fill='{PANEL}' stroke='{colors[si % len(colors)]}' stroke-width='2.2'/>")
    o.append(f"<line x1='{x0:.1f}' y1='{ybot:.1f}' x2='{x1:.1f}' y2='{ybot:.1f}' stroke='{GREY}' stroke-width='1.2'/>")
    o.append(xlabels(x0, x1, labels, ybot + 20, 11))
    if legend and len(series) > 1:
        lx = x0; ly = h - 12
        for si, (nm, _) in enumerate(series):
            o.append(f"<line x1='{lx:.1f}' y1='{ly-4:.1f}' x2='{lx+14:.1f}' y2='{ly-4:.1f}' stroke='{colors[si % len(colors)]}' stroke-width='3'/>")
            o.append(axis_text(lx + 19, ly, nm, 11, INK_SOFT, 'start'))
            lx += 40 + len(nm) * 12.2
    if band:
        y1, y2, lab, col = band
        o.append(f"<rect x='{x0:.1f}' y='{Y(y2):.1f}' width='{x1-x0:.1f}' height='{abs(Y(y1)-Y(y2)):.1f}' "
                 f"fill='{col}' fill-opacity='0.10'/>")
        o.append(axis_text(x1 - 6, Y(y2) - 6, lab, 11, col, 'end', '600'))
    if annots:
        for (i, v, txt, col, dx, dy) in annots:
            o.append(axis_text(X(i) + dx, Y(v) + dy, txt, 11, col, 'middle', '600'))
    o.append('</svg>')
    return ''.join(o)


# ------------------------------------------------------------------ waterfall
def waterfall(items, w=1120, h=420, pad=(70, 30, 60, 20), unit='$B'):
    """items: list of (label, value, kind) kind in {start,pos,neg,total}"""
    x0, x1 = pad[0], w - pad[1]
    ytop, ybot = pad[3], h - pad[2]
    tops, bots = [], []
    run = 0.0
    bars_ = []
    for lab, v, kind in items:
        if kind in ('start', 'total'):
            bars_.append((lab, 0, v, kind)); tops.append(v); bots.append(0)
            run = v
        else:
            bars_.append((lab, run, run + v, kind)); tops.append(max(run, run + v)); bots.append(min(run, run + v))
            run += v
    vmax = _nice(max(tops) * 1.15)
    sc = (ybot - ytop) / vmax
    n = len(bars_)
    step = (x1 - x0) / n
    bw = step * 0.56
    o = [svg_open(w, h), defs()]
    o.append(ygrid(x0, x1, ytop, ybot, vmax, 5, '', 0))
    for i, (lab, b, t, kind) in enumerate(bars_):
        cx = x0 + step * (i + 0.5)
        col = ACCENT2 if kind == 'total' else (ACCENT if kind == 'neg' else (ACCENT3 if kind == 'pos' else GREY))
        y = ybot - t * sc
        hh = max((t - b) * sc, 3)
        op = 0.9 if kind != 'start' else 0.55
        o.append(f"<rect x='{cx-bw/2:.1f}' y='{y:.1f}' width='{bw:.1f}' height='{hh:.1f}' rx='2' fill='{col}' fill-opacity='{op}'/>")
        val = t if kind in ('start', 'total') else (t - b)
        sign = '' if kind in ('start', 'total') else ('+' if kind == 'pos' else '−')
        o.append(axis_text(cx, y - 7, f"{sign}{_fmt(abs(val),0)}", 11, INK_SOFT, 'middle', '600'))
        for k, ln in enumerate(lab.split('|')):
            o.append(axis_text(cx, ybot + 18 + k * 13, ln, 10.5, MUTED, 'middle'))
    o.append(f"<line x1='{x0:.1f}' y1='{ybot:.1f}' x2='{x1:.1f}' y2='{ybot:.1f}' stroke='{GREY}' stroke-width='1.2'/>")
    o.append('</svg>')
    return ''.join(o)


# ------------------------------------------------------------------ gantt / timeline
def timeline(rows, w=1120, pad_left=250, pad_right=40, row_h=34, top_pad=54, bottom_pad=26,
             xmin=0, xmax=1, ticks=None):
    """rows: list of dict(name, segs=[(start,end,label,status)], note)"""
    h = top_pad + row_h * len(rows) + bottom_pad
    x0, x1 = pad_left, w - pad_right
    def X(v): return x0 + (x1 - x0) * (v - xmin) / (xmax - xmin)
    o = [svg_open(w, h), defs()]
    if ticks:
        for tv, tl in ticks:
            xx = X(tv)
            o.append(f"<line x1='{xx:.1f}' y1='{top_pad-22:.1f}' x2='{xx:.1f}' y2='{top_pad+row_h*len(rows):.1f}' stroke='{GRID}' stroke-width='1'/>")
            o.append(axis_text(xx, top_pad - 28, tl, 11, MUTED, 'middle', '600'))
    for ri, r in enumerate(rows):
        yc = top_pad + row_h * ri + row_h / 2
        o.append(axis_text(pad_left - 14, yc + 4, r['name'], 12, INK, 'end', '600'))
        for (a, b, lab, status) in r['segs']:
            col = {'done': ACCENT3, 'live': ACCENT, 'prep': ACCENT4, 'blocked': MUTED}.get(status, GREY)
            xx, ww = X(a), max(X(b) - X(a), 8)
            o.append(f"<rect x='{xx:.1f}' y='{yc-10:.1f}' width='{ww:.1f}' height='20' rx='10' fill='{col}' fill-opacity='0.88'/>")
            if lab:
                o.append(axis_text(xx + ww + 9, yc + 4, lab, 11, INK_SOFT, 'start'))
        if r.get('note'):
            o.append(axis_text(pad_left - 14, yc + 17, r['note'], 10, MUTED, 'end'))
    o.append('</svg>')
    return ''.join(o)


# ------------------------------------------------------------------ heatmap / matrix
def matrix(rows, cols, vals, w=1120, h=None, pad=(200, 30, 60, 20), colors=None,
           fmt=None, legend=None, colw=None):
    """vals: rows x cols of numbers 0..1 for intensity (or -1 for none)"""
    row_h = 34
    h = h or pad[3] + row_h * len(rows) + pad[2]
    x0 = pad[0]; x1 = w - pad[1]
    cw = (x1 - x0) / len(cols)
    o = [svg_open(w, h), defs()]
    for j, c in enumerate(cols):
        for k, ln in enumerate(str(c).split('|')):
            o.append(axis_text(x0 + cw * (j + 0.5), pad[3] - 12 + k * 13, ln, 11, INK_SOFT, 'middle', '600'))
    for i, r in enumerate(rows):
        yc = pad[3] + row_h * i
        o.append(axis_text(x0 - 12, yc + row_h / 2 + 4, r, 11.5, INK, 'end', '500'))
        for j in range(len(cols)):
            v = vals[i][j]
            xx = x0 + cw * j
            if v is None or v < 0:
                o.append(f"<rect x='{xx+2:.1f}' y='{yc+3:.1f}' width='{cw-4:.1f}' height='{row_h-6}' rx='4' fill='#f2f4f7'/>")
                o.append(axis_text(xx + cw / 2, yc + row_h / 2 + 4, '—', 12, MUTED, 'middle'))
                continue
            col = colors(v) if callable(colors) else GREY
            txt = fmt(v) if fmt else f'{v:.0%}'
            lum = 0.0
            if isinstance(col, tuple):
                col, lum = col
            o.append(f"<rect x='{xx+2:.1f}' y='{yc+3:.1f}' width='{cw-4:.1f}' height='{row_h-6}' rx='4' fill='{col}'/>")
            o.append(axis_text(xx + cw / 2, yc + row_h / 2 + 4, txt, 11.5,
                               '#fff' if lum > 0.55 else INK, 'middle', '600'))
    if legend:
        o.append(axis_text(x0, h - 14, legend, 10.5, MUTED, 'start'))
    o.append('</svg>')
    return ''.join(o)


# ------------------------------------------------------------------ horiz bars
def hbars(items, w=1120, label_w=250, pad_right=30, row_h=30, top_pad=26, bottom_pad=20,
          colors=None, unit='', dec=1, fmt=None, vmax=None):
    """items: list of (label, value) or (label, value, color)"""
    h = top_pad + row_h * len(items) + bottom_pad
    x0 = label_w; x1 = w - pad_right
    vm = vmax or _nice(max(i[1] for i in items) * 1.15)
    def X(v): return x0 + (x1 - x0) * v / vm
    o = [svg_open(w, h), defs()]
    for i, it in enumerate(items):
        lab, v = it[0], it[1]
        col = it[2] if len(it) > 2 else (colors or SERIES)[0]
        yc = top_pad + row_h * i
        o.append(axis_text(x0 - 12, yc + row_h / 2 + 4, lab, 11.5, INK, 'end', '500'))
        o.append(f"<rect x='{x0:.1f}' y='{yc+5:.1f}' width='{max(X(v)-x0,2):.1f}' height='{row_h-12:.1f}' rx='3' fill='{col}' fill-opacity='0.9'/>")
        txt = fmt(v) if fmt else _fmt(v, dec) + unit
        o.append(axis_text(X(v) + 8, yc + row_h / 2 + 4, txt, 11, INK_SOFT, 'start', '600'))
    o.append('</svg>')
    return ''.join(o)


# ------------------------------------------------------------------ scatter
def scatter(points, w=1120, h=430, pad=(70, 30, 60, 22), xlab='', ylab='',
            xlog=False, annot=True, size_by=None, quadrant=None):
    """points: list of dict(x,y,label,color,r)"""
    x0, x1 = pad[0], w - pad[1]
    ytop, ybot = pad[3], h - pad[2]
    xs = [p['x'] for p in points]; ys = [p['y'] for p in points]
    xmax = _nice(max(xs) * 1.25); ymax = _nice(max(ys) * 1.2)
    def X(v): return x0 + (x1 - x0) * v / xmax
    def Y(v): return ybot - (ybot - ytop) * v / ymax
    o = [svg_open(w, h), defs()]
    for i in range(6):
        v = ymax * i / 5; y = Y(v)
        o.append(f"<line x1='{x0:.1f}' y1='{y:.1f}' x2='{x1:.1f}' y2='{y:.1f}' stroke='{GRID}'/>")
        o.append(axis_text(x0 - 10, y + 4, _fmt(v, 0), 11, MUTED, 'end'))
    for i in range(6):
        v = xmax * i / 5; x = X(v)
        o.append(f"<line x1='{x:.1f}' y1='{ytop:.1f}' x2='{x:.1f}' y2='{ybot:.1f}' stroke='{GRID}'/>")
        o.append(axis_text(x, ybot + 20, _fmt(v, 0), 11, MUTED, 'middle'))
    if quadrant:
        qx, qy = X(quadrant[0]), Y(quadrant[1])
        o.append(f"<line x1='{qx:.1f}' y1='{ytop:.1f}' x2='{qx:.1f}' y2='{ybot:.1f}' stroke='{GREY}' stroke-dasharray='5 4'/>")
        o.append(f"<line x1='{x0:.1f}' y1='{qy:.1f}' x2='{x1:.1f}' y2='{qy:.1f}' stroke='{GREY}' stroke-dasharray='5 4'/>")
    for p in points:
        r = p.get('r', 9)
        o.append(f"<circle cx='{X(p['x']):.1f}' cy='{Y(p['y']):.1f}' r='{r}' fill='{p.get('color',ACCENT)}' fill-opacity='0.78' stroke='#fff' stroke-width='1.5'/>")
        if annot:
            o.append(axis_text(X(p['x']), Y(p['y']) - r - 6, p['label'], 11, INK, 'middle', '600'))
    o.append(axis_text((x0 + x1) / 2, h - 8, xlab, 11.5, INK_SOFT, 'middle', '600'))
    o.append(axis_text(x0 - 52, ytop - 10, ylab, 11.5, INK_SOFT, 'start', '600'))
    o.append('</svg>')
    return ''.join(o)


# ------------------------------------------------------------------ football field
def football(items, w=1120, h=None, label_w=250, row_h=46, top_pad=44, bottom_pad=34, marker=None):
    """items: list of (label, low, high, mid, color)"""
    row_h = row_h
    h = h or top_pad + row_h * len(items) + bottom_pad
    x0 = label_w; x1 = w - 60
    lo = min(i[1] for i in items); hi = max(i[2] for i in items)
    lo = min(lo, marker or lo); hi = max(hi, marker or hi)
    span = hi - lo
    lo -= span * 0.06; hi += span * 0.06
    def X(v): return x0 + (x1 - x0) * (v - lo) / (hi - lo)
    o = [svg_open(w, h), defs()]
    ticks = 6
    for i in range(ticks + 1):
        v = lo + (hi - lo) * i / ticks
        x = X(v)
        o.append(f"<line x1='{x:.1f}' y1='{top_pad-24:.1f}' x2='{x:.1f}' y2='{h-bottom_pad+4:.1f}' stroke='{GRID}'/>")
        o.append(axis_text(x, top_pad - 30, _fmt(v, 0), 11, MUTED, 'middle'))
    for i, (lab, low, high, mid, col) in enumerate(items):
        yc = top_pad + row_h * i + row_h / 2
        o.append(axis_text(x0 - 12, yc + 4, lab, 11.5, INK, 'end', '500'))
        o.append(f"<rect x='{X(low):.1f}' y='{yc-9:.1f}' width='{max(X(high)-X(low),3):.1f}' height='18' rx='9' fill='{col}' fill-opacity='0.30'/>")
        o.append(f"<line x1='{X(low):.1f}' y1='{yc:.1f}' x2='{X(high):.1f}' y2='{yc:.1f}' stroke='{col}' stroke-width='2.4'/>")
        if mid:
            o.append(f"<circle cx='{X(mid):.1f}' cy='{yc:.1f}' r='6' fill='{col}' stroke='#fff' stroke-width='2'/>")
    if marker:
        x = X(marker)
        o.append(f"<line x1='{x:.1f}' y1='{top_pad-24:.1f}' x2='{x:.1f}' y2='{h-bottom_pad+4:.1f}' stroke='{INK}' stroke-width='2' stroke-dasharray='6 4'/>")
        o.append(axis_text(x, h - bottom_pad + 20, f'现价 {_fmt(marker,0)}', 11, INK, 'middle', '700'))
    o.append('</svg>')
    return ''.join(o)


# ------------------------------------------------------------------ sensitivity heat
def sens(rows, cols, vals, w=1120, pad=(190, 26, 70, 20), cell=None, fmt=None,
         cmin=None, cmax=None, title=''):
    """vals[i][j] numeric; color scale red->green"""
    row_h = 52
    h = pad[3] + row_h * len(rows) + pad[2]
    x0 = pad[0]; x1 = w - pad[1]
    cw = (x1 - x0) / len(cols)
    flat = [v for r in vals for v in r if v is not None]
    lo = cmin if cmin is not None else min(flat)
    hi = cmax if cmax is not None else max(flat)
    def col(v):
        t = 0 if hi == lo else (v - lo) / (hi - lo)
        # red (bad) -> amber -> green (good)
        if t < 0.5:
            u = t / 0.5
            r = int(200 + (232 - 200) * u); g = int(72 + (170 - 72) * u); b = int(45 + (40 - 45) * u)
        else:
            u = (t - 0.5) / 0.5
            r = int(232 + (22 - 232) * u); g = int(170 + (140 - 170) * u); b = int(40 + (80 - 40) * u)
        return f'rgb({r},{g},{b})', t
    o = [svg_open(w, h), defs()]
    if title:
        o.append(axis_text(x0, 14, title, 11.5, INK_SOFT, 'start', '600'))
    for j, c in enumerate(cols):
        o.append(axis_text(x0 + cw * (j + 0.5), h - pad[2] + 40, c, 11.5, INK_SOFT, 'middle', '600'))
    for i, r in enumerate(rows):
        yc = pad[3] + row_h * i
        o.append(axis_text(x0 - 12, yc + row_h / 2 + 4, r, 11.5, INK, 'end', '500'))
        for j in range(len(cols)):
            v = vals[i][j]
            xx = x0 + cw * j
            if v is None:
                o.append(f"<rect x='{xx+2:.1f}' y='{yc+3:.1f}' width='{cw-4:.1f}' height='{row_h-6}' rx='4' fill='#f2f4f7'/>")
                continue
            (c_, t) = col(v)
            o.append(f"<rect x='{xx+2:.1f}' y='{yc+3:.1f}' width='{cw-4:.1f}' height='{row_h-6}' rx='4' fill='{c_}' fill-opacity='0.88'/>")
            lab = fmt(v) if fmt else _fmt(v, 0)
            o.append(axis_text(xx + cw / 2, yc + row_h / 2 + 5, lab, 13, '#fff' if (t < 0.25 or t > 0.72) else INK, 'middle', '700'))
    o.append('</svg>')
    return ''.join(o)


# ------------------------------------------------------------------ stacked area (fleet ramp scenarios)
def area(labels, series, w=1120, h=400, pad=(70, 30, 60, 20), colors=None, unit='', legend=True, ymax=None):
    x0, x1 = pad[0], w - pad[1]
    ytop, ybot = pad[3], h - pad[2]
    colors = colors or SERIES
    n = len(labels)
    vmax = ymax or _nice(max(max(vs) for _, vs in series) * 1.15)
    sc = (ybot - ytop) / vmax
    def X(i): return x0 + (x1 - x0) * (i / (n - 1) if n > 1 else 0.5)
    def Y(v): return ybot - v * sc
    o = [svg_open(w, h), defs()]
    o.append(ygrid(x0, x1, ytop, ybot, vmax, 5, unit, 0))
    for si, (nm, vs) in enumerate(series):
        d = ' '.join(f"{'M' if k==0 else 'L'}{X(k):.1f},{Y(v):.1f}" for k, v in enumerate(vs))
        area_d = d + f" L{X(n-1):.1f},{ybot:.1f} L{X(0):.1f},{ybot:.1f} Z"
        o.append(f"<path d='{area_d}' fill='{colors[si % len(colors)]}' fill-opacity='0.16'/>")
        o.append(f"<path d='{d}' fill='none' stroke='{colors[si % len(colors)]}' stroke-width='2.6' stroke-linejoin='round'/>")
        for k, v in enumerate(vs):
            if k == n - 1 or k == 0:
                o.append(f"<circle cx='{X(k):.1f}' cy='{Y(v):.1f}' r='3.2' fill='#fff' stroke='{colors[si % len(colors)]}' stroke-width='2'/>")
    o.append(xlabels(x0, x1, labels, ybot + 20, 11))
    o.append(f"<line x1='{x0:.1f}' y1='{ybot:.1f}' x2='{x1:.1f}' y2='{ybot:.1f}' stroke='{GREY}'/>")
    if legend:
        lx = x0; ly = h - 12
        for si, (nm, _) in enumerate(series):
            o.append(f"<line x1='{lx:.1f}' y1='{ly-4:.1f}' x2='{lx+14:.1f}' y2='{ly-4:.1f}' stroke='{colors[si % len(colors)]}' stroke-width='3'/>")
            o.append(axis_text(lx + 19, ly, nm, 11, INK_SOFT, 'start'))
            lx += 40 + len(nm) * 12.2
    o.append('</svg>')
    return ''.join(o)


# ------------------------------------------------------------------ small multiples / stat bar
def gauge(value, target, w=300, h=110, label='', unit=''):
    o = [svg_open(w, h), defs()]
    t = min(value / target, 1.0) if target else 0
    o.append(f"<rect x='6' y='58' width='{w-12}' height='16' rx='8' fill='{GRID}'/>")
    o.append(f"<rect x='6' y='58' width='{(w-12)*t:.1f}' height='16' rx='8' fill='{ACCENT}'/>")
    o.append(axis_text(6, 40, label, 11.5, INK_SOFT, 'start', '600'))
    o.append(axis_text(6, 96, f'{value:,.1f}{unit} / {target:,.1f}{unit}', 11, MUTED, 'start'))
    o.append(axis_text(w - 6, 96, f'{t:.1%}', 11, INK, 'end', '700'))
    o.append('</svg>')
    return ''.join(o)
