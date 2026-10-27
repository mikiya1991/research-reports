# -*- coding: utf-8 -*-
"""Hand-rolled SVG chart library (stdlib only). All charts are inline <svg>, viewBox width 1120."""
import math, datetime as dt

INK = '#101820'; INK2 = '#3A4750'; MUTED = '#8B95A3'; GRID = '#E8EDEF'
ACCENT = '#0E7C66'    # primary green
ACCENT2 = '#B8860B'   # gold
ACCENT3 = '#2F6FB8'   # blue
ACCENT4 = '#C0392B'   # red
ACCENT5 = '#7A4FD6'   # violet
GREY = '#9AA6B2'
SERIES = [ACCENT, ACCENT3, ACCENT2, ACCENT4, ACCENT5, '#0D8A9E', '#D1477A']
FONT = ("font-family='-apple-system,BlinkMacSystemFont,Segoe UI,PingFang SC,"
        "Hiragino Sans GB,Microsoft YaHei,sans-serif'")

W = 1120


def esc(s):
    return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def nfmt(v, dec=0):
    return f'{v:,.{dec}f}'


def nice(v, up=1.10):
    if v <= 0:
        return 1.0
    v = v * up
    e = math.floor(math.log10(v))
    f = v / 10 ** e
    for m in (1, 1.2, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10):
        if f <= m + 1e-9:
            return m * 10 ** e
    return 10 ** (e + 1)


def svg_open(w, h, cls='chart'):
    return (f"<svg class='{cls}' viewBox='0 0 {w} {h}' width='100%' "
            f"preserveAspectRatio='xMidYMid meet' role='img' {FONT}>")


def t(x, y, s, size=12, fill=MUTED, anchor='middle', weight='400', rot=None, op=None):
    tr = f" transform='rotate({rot} {x:.1f} {y:.1f})'" if rot else ''
    o = f" opacity='{op}'" if op else ''
    return (f"<text x='{x:.1f}' y='{y:.1f}' font-size='{size}' fill='{fill}' "
            f"text-anchor='{anchor}' font-weight='{weight}'{tr}{o}>{esc(s)}</text>")


def ln(x1, y1, x2, y2, stroke=GRID, w=1, dash=None, op=None):
    d = f" stroke-dasharray='{dash}'" if dash else ''
    o = f" opacity='{op}'" if op else ''
    return (f"<line x1='{x1:.1f}' y1='{y1:.1f}' x2='{x2:.1f}' y2='{y2:.1f}' "
            f"stroke='{stroke}' stroke-width='{w}'{d}{o}/>")


def rc(x, y, w_, h_, fill, rx=4, op=None, stroke=None, sw=1):
    o = f" opacity='{op}'" if op else ''
    st = f" stroke='{stroke}' stroke-width='{sw}'" if stroke else ''
    return (f"<rect x='{x:.1f}' y='{y:.1f}' width='{max(w_,0):.1f}' height='{max(h_,0):.1f}' "
            f"rx='{rx}' fill='{fill}'{o}{st}/>")


def path(pts, stroke, w=2, fill='none', dash=None, op=None):
    if len(pts) < 2:
        return ''
    d = 'M ' + ' L '.join(f'{x:.1f} {y:.1f}' for x, y in pts)
    da = f" stroke-dasharray='{dash}'" if dash else ''
    o = f" opacity='{op}'" if op else ''
    return (f"<path d='{d}' fill='{fill}' stroke='{stroke}' stroke-width='{w}' "
            f"stroke-linejoin='round' stroke-linecap='round'{da}{o}/>")


def area(pts, base_y, fill, op=0.12):
    if len(pts) < 2:
        return ''
    d = 'M ' + f'{pts[0][0]:.1f} {base_y:.1f} L ' + ' L '.join(
        f'{x:.1f} {y:.1f}' for x, y in pts) + f' L {pts[-1][0]:.1f} {base_y:.1f} Z'
    return f"<path d='{d}' fill='{fill}' opacity='{op}'/>"


def circ(x, y, r, fill, stroke=None, sw=2, op=None):
    st = f" stroke='{stroke}' stroke-width='{sw}'" if stroke else ''
    o = f" opacity='{op}'" if op else ''
    return f"<circle cx='{x:.1f}' cy='{y:.1f}' r='{r}' fill='{fill}'{st}{o}/>"


def arrow(x1, y1, x2, y2, color=ACCENT, w=2.4, dash=None, head=9):
    """straight arrow with triangular head"""
    ang = math.atan2(y2 - y1, x2 - x1)
    hx, hy = x2 - head * math.cos(ang), y2 - head * math.sin(ang)
    da = f" stroke-dasharray='{dash}'" if dash else ''
    p1 = f"{hx + head*0.45*math.sin(ang):.1f} {hy - head*0.45*math.cos(ang):.1f}"
    p2 = f"{hx - head*0.45*math.sin(ang):.1f} {hy + head*0.45*math.cos(ang):.1f}"
    return (ln(x1, y1, hx, hy, color, w, da) +
            f"<polygon points='{x2:.1f},{y2:.1f} {p1} {p2}' fill='{color}'/>")


def legend_row(items, x, y, size=12.5):
    """items: list of (color, text). laid out horizontally"""
    out, cx = [], x
    for color, text in items:
        out.append(rc(cx, y - 9, 11, 11, color, 3))
        out.append(t(cx + 16, y, text, size, INK2, 'start'))
        cx += 24 + len(text) * (size * 0.95)
    return ''.join(out)


# ---------------------------------------------------------------- cartesian helpers
class Ax:
    """maps (date,value) -> pixel; handles nice ticks + date axis."""
    def __init__(self, series, w=W, h=420, pad=(74, 30, 46, 22),
                 ymin=None, ymax=None, nticks=5, yfmt=None, tickfmt=None,
                 xpad_frac=0.015):
        self.pad = pad
        self.x0, self.x1 = pad[0], w - pad[1]
        self.ytop, self.ybot = pad[3], h - pad[2]
        self.w, self.h = w, h
        allpts = [p for s in series for p in s['pts']]
        t0 = min(dt.date.fromisoformat(d) for d, _ in allpts)
        t1 = max(dt.date.fromisoformat(d) for d, _ in allpts)
        span = (t1 - t0).days
        self.o0 = t0.toordinal() - span * xpad_frac
        self.o1 = t1.toordinal() + span * xpad_frac
        vals = [v for _, v in allpts]
        vmin = min(vals) if ymin is None else ymin
        vmax = max(vals) if ymax is None else ymax
        self.vmin = 0 if (ymin is None and vmin > 0) else vmin
        self.vmax = nice(vmax)
        self.nticks = nticks
        self.yfmt = yfmt or (lambda v: nfmt(v))
        self.tickfmt = tickfmt

    def x(self, date):
        o = dt.date.fromisoformat(date).toordinal()
        return self.x0 + (o - self.o0) / (self.o1 - self.o0) * (self.x1 - self.x0)

    def y(self, v):
        return self.ybot - (v - self.vmin) / (self.vmax - self.vmin) * (self.ybot - self.ytop)

    def grid(self):
        out = []
        for i in range(self.nticks + 1):
            v = self.vmin + (self.vmax - self.vmin) * i / self.nticks
            y = self.y(v)
            out.append(ln(self.x0, y, self.x1, y, GRID, 1))
            out.append(t(self.x0 - 10, y + 4, self.yfmt(v), 11.5, MUTED, 'end'))
        return ''.join(out)

    def xaxis(self, years=None, months_every=None, fmt='%Y'):
        out = [ln(self.x0, self.ybot, self.x1, self.ybot, '#D5DCE1', 1.5)]
        o0 = int(self.o0); o1 = int(self.o1)
        if years:
            ystart = dt.date.fromordinal(o0).year + 1
            for yy in range(ystart, dt.date.fromordinal(o1).year + 1):
                for mm in (years if isinstance(years, (list, tuple)) else [1]):
                    d = dt.date(yy, mm, 1)
                    if o0 <= d.toordinal() <= o1:
                        x = self.x(d.isoformat())
                        out.append(ln(x, self.ybot, x, self.ybot + 5, '#C3CCD3', 1))
                        out.append(t(x, self.ybot + 19, d.strftime(fmt), 11.5, MUTED))
        if months_every:
            d = dt.date.fromordinal(o0)
            d = dt.date(d.year, d.month, 1)
            while d.toordinal() <= o1:
                if d.month % months_every == 1 and d.day == 1:
                    x = self.x(d.isoformat())
                    out.append(t(x, self.ybot + 19, d.strftime('%y/%m'), 10.5, MUTED, rot=-38))
                d = dt.date(d.year + (1 if d.month == 12 else 0), 1 if d.month == 12 else d.month + 1, 1)
        return ''.join(out)


def line_chart(series, w=W, h=420, pad=(74, 30, 46, 22), ymin=None, ymax=None,
               nticks=5, yfmt=None, colors=None, ylab=None,
               area_first=False, vlines=None, notes=None, dots_last=False,
               line_w=2.2, dash_after=None, xaxis_years=True):
    """series: list of dict(name=..., pts=[(date, val), ...], color=..., dash=None, width=None)
       vlines: list of (date, label, color)  notes: list of dict(date,val,text,dx,dy,color,anchor)"""
    colors = colors or SERIES
    ax = Ax(series, w=w, h=h, pad=pad, ymin=ymin, ymax=ymax, nticks=nticks, yfmt=yfmt)
    o = [svg_open(w, h), ax.grid(), ax.xaxis(years=xaxis_years)]
    if ylab:
        o.append(t(pad[0] - 56, ax.ytop - 10, ylab, 11.5, MUTED, 'start'))
    for vl in (vlines or []):
        date, label, color = vl[0], vl[1], (vl[2] if len(vl) > 2 else ACCENT4)
        x = ax.x(date)
        o.append(ln(x, ax.ytop, x, ax.ybot, color, 1.4, dash='4 4', op=0.75))
        if label:
            o.append(t(x + 4, ax.ytop + 12, label, 11.5, color, 'start', weight='650'))
    for i, s in enumerate(series):
        col = s.get('color') or colors[i % len(colors)]
        dash = s.get('dash')
        pts = [(ax.x(d), ax.y(v)) for d, v in s['pts']]
        if area_first and i == 0:
            o.append(area(pts, ax.ybot, col, 0.14))
        o.append(path(pts, col, s.get('width', line_w), dash=dash))
        if dots_last:
            x, y = pts[-1]
            o.append(circ(x, y, 4.5, '#fff', stroke=col, sw=2.6))
            last_v = s['pts'][-1][1]
            o.append(t(min(x + 8, ax.x1), y - 8, s.get('last_label') or nfmt(last_v), 12, col,
                       'end' if x > ax.x1 - 80 else 'start', weight='700'))
    for nt in (notes or []):
        x, y = ax.x(nt['date']), ax.y(nt['val']) if nt.get('val') is not None else ax.ytop + 30
        dx, dy = nt.get('dx', 0), nt.get('dy', -14)
        col = nt.get('color', INK2)
        if nt.get('dot', False):
            o.append(circ(x, y, 4.5, col))
        if nt.get('arrow', False):
            o.append(ln(x, y, x + dx * 0.72, y + dy * 0.72, col, 1.2, dash='3 3'))
        tx_, ty_ = x + dx, y + dy
        anchor = nt.get('anchor', 'middle')
        for li, line in enumerate(nt['text'].split('|')):
            o.append(t(tx_, ty_ + li * 15, line, nt.get('size', 11.5), col, anchor,
                       weight=nt.get('weight', '600')))
    return ''.join(o) + '</svg>'


def bars(labels, series, w=W, h=380, pad=(74, 26, 52, 18), colors=None, unit='',
         dec=0, stack=False, ymax=None, nticks=5, yfmt=None, value_labels=True,
         val_size=11, xlab_size=11.5, gap=0.66, ymin=None, notes=None, label_rot=None):
    """series: list of (name, values) aligned with labels (categorical x)."""
    colors = colors or SERIES
    x0, x1 = pad[0], w - pad[1]
    ytop, ybot = pad[3], h - pad[2]
    n = len(labels)
    step = (x1 - x0) / n
    if stack:
        tops = [sum(s[1][i] or 0 for s in series) for i in range(n)]
    else:
        tops = [max((s[1][i] or 0) for s in series) for i in range(n)]
    vmax = ymax or nice(max(tops) * 1.16)
    vmin = ymin if ymin is not None else 0
    yfmt = yfmt or (lambda v: nfmt(v, dec) + unit)
    o = [svg_open(w, h)]
    for i in range(nticks + 1):
        v = vmin + (vmax - vmin) * i / nticks
        y = ybot - (v - vmin) / (vmax - vmin) * (ybot - ytop)
        o.append(ln(x0, y, x1, y, GRID, 1))
        o.append(t(x0 - 10, y + 4, yfmt(v), 11.5, MUTED, 'end'))
    o.append(ln(x0, ybot, x1, ybot, '#D5DCE1', 1.5))
    bw = step * gap if stack else step * gap / len(series)
    for i in range(n):
        cx = x0 + step * (i + 0.5)
        if label_rot:
            o.append(t(cx, ybot + 20, labels[i], xlab_size, MUTED, 'end', rot=label_rot))
        else:
            o.append(t(cx, ybot + 20, labels[i], xlab_size, MUTED))
        if stack:
            acc = 0.0
            for si, (nm, vs) in enumerate(series):
                v = vs[i] or 0
                y = ybot - (acc + v - vmin) / (vmax - vmin) * (ybot - ytop)
                hh = v / (vmax - vmin) * (ybot - ytop)
                o.append(rc(cx - bw / 2, y, bw, hh, colors[si % len(colors)], 3, op=0.9))
                if value_labels and v and hh > 18:
                    o.append(t(cx, y + 16, nfmt(v, dec), val_size, '#fff', weight='650'))
                acc += v
        else:
            start = cx - (bw * len(series)) / 2
            for si, (nm, vs) in enumerate(series):
                v = vs[i] or 0
                hh = max(v - vmin, 0) / (vmax - vmin) * (ybot - ytop)
                y = ybot - hh
                o.append(rc(start + si * bw, y, bw, hh, colors[si % len(colors)], 3, op=0.9))
                if value_labels and v:
                    o.append(t(start + si * bw + bw / 2, y - 6, nfmt(v, dec), val_size,
                               INK2, weight='650'))
    for nt in (notes or []):
        ti = nt['i'] if isinstance(nt['i'], int) else labels.index(nt['i'])
        cx = x0 + step * (ti + 0.5)
        yv = nt.get('val') if nt.get('val') is not None else tops[ti]
        y = ybot - (yv - vmin) / (vmax - vmin) * (ybot - ytop) + nt.get('dy', -26)
        o.append(t(cx + nt.get('dx', 0), y, nt['text'], 11.5, nt.get('color', ACCENT4), weight='700'))
    return ''.join(o) + '</svg>'


def hbars(labels, values, w=W, h=None, pad=(230, 120, 30, 14), color=ACCENT,
          val_fmt=None, note_all=None):
    """horizontal bars; labels left, values printed right of bar."""
    n = len(labels)
    h = h or (pad[3] + pad[2] + n * 34)
    x0, x1 = pad[0], w - pad[1]
    ytop, ybot = pad[3], h - pad[2]
    vmax = nice(max(values))
    step = (ybot - ytop) / n
    o = [svg_open(w, h)]
    for i, (lab, v) in enumerate(zip(labels, values)):
        cy = ytop + step * (i + 0.5)
        bw = v / vmax * (x1 - x0)
        o.append(t(x0 - 12, cy + 4, lab, 12.5, INK2, 'end'))
        o.append(rc(x0, cy - 11, bw, 22, color, 5, op=0.88))
        o.append(t(x0 + bw + 8, cy + 4, val_fmt(v) if val_fmt else f'{v:g}', 12.5, INK2, 'start',
                   weight='650'))
    return ''.join(o) + '</svg>'


def waterfall(labels, base_label, base, deltas, end_label, w=W, h=420,
              pad=(74, 30, 46, 18), dec=0, unit='', up_color=ACCENT3, down_color=ACCENT4):
    """classic waterfall: base bar, then deltas, then total."""
    n = len(deltas) + 2  # base + deltas + end
    x0, x1 = pad[0], w - pad[1]
    ytop, ybot = pad[3], h - pad[2]
    vals = [base]
    run = base
    for _, d in deltas:
        run += d
        vals.append(run)
    total = run
    lo = min(0, min(vals + [total]))
    hi = max(vals + [total])
    vmin = 0 if lo >= 0 else -nice(-lo)
    vmax = nice(hi * 1.15)
    yfmt = lambda v: nfmt(v, dec) + unit
    o = [svg_open(w, h)]
    for i in range(6):
        v = vmin + (vmax - vmin) * i / 5
        y = ybot - (v - vmin) / (vmax - vmin) * (ybot - ytop)
        o.append(ln(x0, y, x1, y, GRID, 1))
        o.append(t(x0 - 10, y + 4, yfmt(v), 11.5, MUTED, 'end'))
    o.append(ln(x0, ybot, x1, ybot, '#D5DCE1', 1.5))
    step = (x1 - x0) / n
    bw = step * 0.56
    Y = lambda v: ybot - (v - vmin) / (vmax - vmin) * (ybot - ytop)
    # base
    cx = x0 + step * 0.5
    o.append(rc(cx - bw / 2, Y(base), bw, Y(vmin) - Y(base) if vmin < 0 else Y(0) - Y(base),
                ACCENT, 4, op=0.85))
    o.append(t(cx, Y(base) - 8, nfmt(base, dec), 12, INK2, weight='700'))
    o.append(t(cx, ybot + 20, base_label, 11.5, MUTED))
    run = base
    for i, (lab, d) in enumerate(deltas):
        cx = x0 + step * (i + 1.5)
        y1, y2 = Y(run), Y(run + d)
        col = up_color if d >= 0 else down_color
        o.append(rc(cx - bw / 2, min(y1, y2), bw, abs(y2 - y1), col, 4, op=0.9))
        o.append(t(cx, min(y1, y2) - 8, ('+' if d >= 0 else '') + nfmt(d, dec), 12, col, weight='700'))
        o.append(t(cx, ybot + 20, lab, 11, MUTED, rot=-24 if len(lab) > 8 else 0))
        if i > 0 or True:
            o.append(ln(x0 + step * (i + 0.5) + bw / 2, y1, cx - bw / 2, y1, '#C3CCD3', 1, dash='3 3'))
        run += d
    cx = x0 + step * (n - 0.5)
    o.append(rc(cx - bw / 2, Y(total), bw, Y(0) - Y(total), ACCENT, 4, op=0.85))
    o.append(t(cx, Y(total) - 8, nfmt(total, dec), 12, INK2, weight='700'))
    o.append(t(cx, ybot + 20, end_label, 11.5, MUTED))
    o.append(ln(x0 + step * (n - 1.5) + bw / 2, Y(total), cx - bw / 2, Y(total), '#C3CCD3', 1, dash='3 3'))
    return ''.join(o) + '</svg>'


def box(x, y, w_, h_, title, lines=None, color=ACCENT, fill_op=0.07, tsize=13.5, lsize=11.5):
    o = [rc(x, y, w_, h_, color, 10, op=fill_op),
         rc(x, y, w_, h_, 'none', 10, stroke=color, sw=1.4)]
    o.append(t(x + w_ / 2, y + (24 if lines else h_ / 2 + 5), title, tsize, INK, weight='700'))
    for i, line in enumerate(lines or []):
        o.append(t(x + w_ / 2, y + 44 + i * 16, line, lsize, INK2))
    return ''.join(o)
