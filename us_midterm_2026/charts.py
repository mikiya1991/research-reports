# -*- coding: utf-8 -*-
"""Hand-rolled SVG chart library (stdlib only). All charts are inline <svg>, viewBox width 1120."""
import math, datetime as dt

INK = '#101820'; INK2 = '#3A4750'; INK3 = '#5A6672'; MUTED = '#8B95A3'; GRID = '#E8EDEF'
# --- validated palette (dataviz validate_palette.js, light) ---
ACCENT = '#0A9960'    # green  - primary series
ACCENT3 = '#2F6FB8'   # blue   - second series / Democratic party color
ACCENT2 = '#CC7A00'   # orange - third series
ACCENT4 = '#C0392B'   # red    - negative / Republican party color
ACCENT5 = '#7A4FD6'   # violet - 4th series ONLY when blue absent from chart
MAGENTA = '#C2418F'   # 4th series ONLY when red absent from chart
GREY = '#9AA6B2'
# categorical core (all-pairs validated): green / blue / orange. Never add a 4th
# categorical hue to one chart without re-validating; prefer small multiples.
SERIES = [ACCENT, ACCENT3, ACCENT2]
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


def ticks(lo, hi, target=6):
    """Round tick values inside [lo, hi] on a 1/2/2.5/5/10 x 10^k step.

    Deriving ticks as lo + i*(hi-lo)/n (the obvious loop) produces labels like
    -31% / 51% or 14% / 23% / 33%, because the padded data range is rarely round.
    Snap the STEP to a round number first, then walk it across the range.
    """
    span = hi - lo
    if span <= 0:
        return [lo]
    e = math.floor(math.log10(span / max(target, 1)))
    for m in (1, 2, 2.5, 5, 10):
        step = m * 10 ** e
        if span / step <= target + 1e-9:
            break
    start = math.ceil(lo / step - 1e-9) * step
    out, k = [], 0
    while k < 60:
        v = start + k * step
        if v > hi + 1e-9:
            break
        out.append(0.0 if abs(v) < step * 0.02 else v)   # no signed zero
        k += 1
    return out


def pfmt(v, unit='', dec=0, plus=False):
    """Axis-tick number. Never prints a signed zero ('-0%'), and uses a real minus."""
    if abs(v) < 10 ** -(dec + 1) / 2:
        return f'{0:.{dec}f}{unit}'
    s = f'{v:+.{dec}f}' if plus else f'{v:.{dec}f}'
    return s.replace('-', '−') + unit


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
                 xpad_frac=0.015, x_include=None):
        self.pad = pad
        self.x0, self.x1 = pad[0], w - pad[1]
        self.ytop, self.ybot = pad[3], h - pad[2]
        self.w, self.h = w, h
        allpts = [p for s in series for p in s['pts']]
        t0 = min(dt.date.fromisoformat(d) for d, _ in allpts)
        t1 = max(dt.date.fromisoformat(d) for d, _ in allpts)
        # Dates that must fit on the axis but carry no value of their own - a
        # vline for election day sits past the last observation, and without
        # this the axis stops short and the marker is drawn off the canvas.
        for d in (x_include or []):
            dd = dt.date.fromisoformat(d)
            t0, t1 = min(t0, dd), max(t1, dd)
        span = (t1 - t0).days
        self.o0 = t0.toordinal() - span * xpad_frac
        self.o1 = t1.toordinal() + span * xpad_frac
        vals = [v for _, v in allpts]
        vmin = min(vals) if ymin is None else ymin
        vmax = max(vals) if ymax is None else ymax
        self.vmin = 0 if (ymin is None and vmin > 0) else vmin
        # An explicit ymax is a statement about the data's ceiling (a probability
        # axis ends at 100%), so it must not be rounded up: nice(100) is 120,
        # which leaves a fifth of the plot empty above the top gridline.
        self.vmax = nice(vmax) if ymax is None else vmax
        self.nticks = nticks
        self.yfmt = yfmt or (lambda v: nfmt(v))
        self.tickfmt = tickfmt

    def x(self, date):
        o = dt.date.fromisoformat(date).toordinal()
        return self.x0 + (o - self.o0) / (self.o1 - self.o0) * (self.x1 - self.x0)

    def y(self, v):
        return self.ybot - (v - self.vmin) / (self.vmax - self.vmin) * (self.ybot - self.ytop)

    def grid(self):
        # Round tick values, not vmin + i*(vmax-vmin)/n: with an explicit range
        # like 20..100 the even split labels the gridlines 20 / 36 / 52 / 68 / 84.
        out = []
        for v in ticks(self.vmin, self.vmax, self.nticks):
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
               line_w=2.2, dash_after=None, xaxis_years=True, x_include=None):
    """series: list of dict(name=..., pts=[(date, val), ...], color=..., dash=None, width=None)
       vlines: list of (date, label, color)  notes: list of dict(date,val,text,dx,dy,color,anchor)"""
    colors = colors or SERIES
    ax = Ax(series, w=w, h=h, pad=pad, ymin=ymin, ymax=ymax, nticks=nticks, yfmt=yfmt,
            x_include=x_include)
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
            # last_dy lets two series that converge at the right edge keep their
            # end labels apart; without it the labels overlap whenever the final
            # values are within a point or two of each other.
            o.append(t(min(x + 8, ax.x1), y + s.get('last_dy', -8),
                       s.get('last_label') or nfmt(last_v), 12, col,
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
    # Round ticks, not vmin + i*(vmax-vmin)/n: with an explicit asymmetric ymin
    # (e.g. -7..12) the even split yields -7 / -2 / 3 / 7 / 12.
    tk = ticks(vmin, vmax, max(nticks, 4))
    tdec = dec if (len(tk) < 2 or tk[1] - tk[0] < 1) else 0
    yfmt = yfmt or (lambda v: pfmt(v, unit, tdec))
    o = [svg_open(w, h)]
    for v in tk:
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
            # Bars encode MAGNITUDE, so they are measured from zero - not from the
            # axis floor. With ymin=-3 a -0.22% bar drawn from -3 is 2.78 units long
            # and reads as a gain. `base` is the zero line whenever the scale dips
            # below it, so a month of 0.00% draws nothing rather than a tall bar.
            base = 0.0 if vmin < 0 else vmin
            yb = ybot - (base - vmin) / (vmax - vmin) * (ybot - ytop)
            start = cx - (bw * len(series)) / 2
            for si, (nm, vs) in enumerate(series):
                v = vs[i] or 0
                yv = ybot - (v - vmin) / (vmax - vmin) * (ybot - ytop)
                hh = abs(yv - yb)
                if v == 0 and base == 0:
                    hh = 2.0                       # keep a zero bar visible
                o.append(rc(start + si * bw, min(yv, yb), bw, hh,
                            colors[si % len(colors)], 3, op=0.9))
                if value_labels and v:
                    o.append(t(start + si * bw + bw / 2,
                               (yv - 6) if v >= 0 else (yv + 15), nfmt(v, dec), val_size,
                               INK2, weight='650'))
    for nt in (notes or []):
        ti = nt['i'] if isinstance(nt['i'], int) else labels.index(nt['i'])
        cx = x0 + step * (ti + 0.5)
        yv = nt.get('val') if nt.get('val') is not None else tops[ti]
        y = ybot - (yv - vmin) / (vmax - vmin) * (ybot - ytop) + nt.get('dy', -26)
        o.append(t(cx + nt.get('dx', 0), y, nt['text'], 11.5, nt.get('color', ACCENT4), weight='700'))
    return ''.join(o) + '</svg>'


def hbars(labels, values, w=W, h=None, pad=(230, 120, 52, 40), color=ACCENT,
          val_fmt=None, vmax=None, colors=None, ref=None, ref_lab='', ref_top=None,
          step_h=34, sublabels=None, unit=''):
    """horizontal bars; labels left, values printed right of bar, value axis below.

    `ref` draws a vertical reference line - the value a bar must clear to mean
    something (50% in a two-way race). Without it, a bar chart of probabilities
    has no way to show which side of "even" each row falls on. Its caption sits
    ABOVE the plot: drawn inside, it lands on the top row's bar.
    `vmax` overrides nice(max(values)) so a 0-100% axis is not rescaled to 110.
    """
    n = len(labels)
    h = h or (pad[3] + pad[2] + n * step_h)
    x0, x1 = pad[0], w - pad[1]
    ytop, ybot = pad[3], h - pad[2]
    vmax = vmax or nice(max(values))
    step = (ybot - ytop) / n
    o = [svg_open(w, h)]
    for v in ticks(0, vmax, 6):
        x = x0 + v / vmax * (x1 - x0)
        if x > x1 + 0.5:
            continue
        o.append(ln(x, ytop, x, ybot, GRID, 1))
        o.append(t(x, ybot + 21, pfmt(v, unit), 11.5, MUTED))
    o.append(ln(x0, ybot, x1, ybot, '#D5DCE1', 1.5))
    if ref is not None:
        rx = x0 + ref / vmax * (x1 - x0)
        o.append(ln(rx, (ytop if ref_top is None else ref_top), rx, ybot,
                    '#B9C3CB', 1.6, dash='5 4'))
        if ref_lab:
            o.append(t(rx, ytop - 12, ref_lab, 11.5, MUTED))
    for i, (lab, v) in enumerate(zip(labels, values)):
        cy = ytop + step * (i + 0.5)
        bw = v / vmax * (x1 - x0)
        col = (colors[i] if colors else color)
        # The two-line block is centred on the bar. Hanging the sublabel below
        # the bar instead puts it closer to the next row's title than to its own.
        o.append(t(x0 - 12, cy + (-2 if sublabels else 4), lab, 12.5, INK2, 'end'))
        if sublabels:
            o.append(t(x0 - 12, cy + 14, sublabels[i], 10.5, MUTED, 'end'))
        o.append(rc(x0, cy - 10, bw, 20, col, 5, op=0.88))
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


def stack_bar1(segments, w=W, h=150, pad=(0, 0, 46, 30), gap=2.0, unit='', show_pct=True,
               label_size=13):
    """one horizontal stacked bar. segments=[(label, value, color, sub), ...]
    sub = optional second line inside segment (small). Values are raw counts or %."""
    x0, x1 = pad[0], w - pad[1]
    ytop, ybot = pad[3], h - pad[2]
    total = sum(s[1] for s in segments) or 1
    bw = x1 - x0
    o = [svg_open(w, h)]
    cx = x0
    for seg in segments:
        lab, v, col = seg[0], seg[1], seg[2]
        sub = seg[3] if len(seg) > 3 else ''
        frac = v / total
        segw = frac * bw - (gap if cx + frac * bw < x1 - 0.5 else 0)
        bh = ybot - ytop
        o.append(rc(cx, ytop, segw, bh, col, 6, op=0.92))
        if segw > 46:
            pct = f'{frac*100:.0f}%' if show_pct else ''
            txt = f'{lab}'
            if pct:
                o.append(t(cx + segw / 2, ytop + bh / 2 - 2, txt, label_size, '#fff', weight='700'))
                o.append(t(cx + segw / 2, ytop + bh / 2 + 16, pct, label_size - 1, '#fff', op=0.92))
                if sub:
                    o.append(t(cx + segw / 2, ytop + bh / 2 + 33, sub, label_size - 2.5, '#fff', op=0.85))
        else:
            o.append(t(cx + segw / 2, ytop - 8, lab, label_size - 1.5, col, weight='650'))
        cx += frac * bw
    o.append('</svg>')
    return ''.join(o)


def rangeline(rows, w=W, h=None, pad=(210, 90, 40, 26), lo=0, hi=100, unit='%',
              tick_at=None, ref=None):
    """probability range chart: rows=[(label, lo_v, hi_v, point_v, color, note), ...]
    draws a thin bar for [lo,hi] with a dot at point estimate; x axis in %."""
    n = len(rows)
    h = h or (pad[3] + pad[2] + n * 44)
    x0, x1 = pad[0], w - pad[1]
    ytop, ybot = pad[3], h - pad[2]

    def X(v):
        return x0 + (v - lo) / (hi - lo) * (x1 - x0)

    o = [svg_open(w, h)]
    step = 10 if (hi - lo) > 40 else 5
    v = lo
    while v <= hi + 1e-9:
        x = X(v)
        o.append(ln(x, ytop, x, ybot, GRID, 1))
        o.append(t(x, ybot + 20, f'{v:g}{unit}', 11.5, MUTED))
        v += step
    o.append(ln(x0, ybot, x1, ybot, '#D5DCE1', 1.5))
    for r in (ref or []):
        x = X(r[0])
        o.append(ln(x, ytop, x, ybot, r[2] if len(r) > 2 else ACCENT4, 1.2, dash='4 4', op=0.8))
        o.append(t(x, ytop - 6, r[1], 11, r[2] if len(r) > 2 else ACCENT4, weight='650'))
    rowstep = (ybot - ytop) / n if n else 1
    for i, r in enumerate(rows):
        lab, a, b, pt, col = r[0], r[1], r[2], r[3], r[4]
        cy = ytop + rowstep * (i + 0.5)
        o.append(t(x0 - 14, cy + 4, lab, 12.5, INK2, 'end'))
        o.append(rc(X(a), cy - 7, X(b) - X(a), 14, col, 7, op=0.30))
        o.append(circ(X(pt), cy, 6, col, '#fff', 2))
        o.append(t(X(b) + 8, cy + 4, f'{pt:g}{unit}', 12.5, col, 'start', weight='700'))
        if len(r) > 5 and r[5]:
            o.append(t(x1 + 4, cy + 4, '', 11, MUTED, 'start'))
    o.append('</svg>')
    return ''.join(o)


def midterm_bars(rows, w=W, h=430, pad=(64, 26, 58, 20), mean=None, baseline=None):
    """rows=[(year, pct), ...]; diverging green/red by sign, value labels, ref lines."""
    x0, x1 = pad[0], w - pad[1]
    ytop, ybot = pad[3], h - pad[2]
    vals = [r[1] for r in rows]
    vmin = min(0, min(vals))
    vmax = nice(max(vals) * 1.12)
    n = len(rows)
    step = (x1 - x0) / n
    bw = step * 0.62

    def Y(v):
        return ybot - (v - vmin) / (vmax - vmin) * (ybot - ytop)

    o = [svg_open(w, h)]
    v = 0
    tick = 10 if (vmax - vmin) > 25 else 5
    vv = 0
    while vv <= vmax + 1e-9:
        y = Y(vv)
        o.append(ln(x0, y, x1, y, GRID, 1))
        o.append(t(x0 - 10, y + 4, f'{vv:g}%', 11.5, MUTED, 'end'))
        vv += tick
    o.append(ln(x0, Y(0), x1, Y(0), '#D5DCE1', 1.5))
    for i, (yr, pct) in enumerate(rows):
        cx = x0 + step * (i + 0.5)
        col = ACCENT if pct >= 0 else ACCENT4
        y = Y(pct)
        hh = abs(Y(pct) - Y(0))
        o.append(rc(cx - bw / 2, min(y, Y(0)), bw, hh, col, 4, op=0.9))
        ty = y - 7 if pct >= 0 else y + 16
        o.append(t(cx, ty, f'{pct:+.1f}', 11, INK2 if pct >= 0 else ACCENT4, weight='650'))
        o.append(t(cx, ybot + 20, str(yr), 10.5, MUTED, rot=-45 if i % 2 == 0 else 0,
                   anchor='end' if i % 2 == 0 else 'middle'))
    if mean is not None:
        y = Y(mean)
        o.append(ln(x0, y, x1, y, ACCENT3, 1.6, dash='6 4', op=0.85))
        o.append(t(x1, y - 8, f'19 次平均 {mean:+.1f}%', 11.5, ACCENT3, 'end', weight='650'))
    if baseline is not None:
        y = Y(baseline)
        o.append(ln(x0, y, x1, y, GREY, 1.4, dash='2 4', op=0.9))
        o.append(t(x1, y + 15, f'任意年份同窗口基线 {baseline:+.1f}%', 11.5, GREY, 'end', weight='650'))
    o.append('</svg>')
    return ''.join(o)


# ============================================================ midterm report additions
def dot_strip(groups, w=W, h=None, pad=(196, 118, 46, 22), lo=None, hi=None, unit='%',
              ref=0, colors=None, mean_label='均值'):
    """Per-group dot strip: every sample shown as a dot, plus a mean bar. Never hides n.

    groups = [(label, [v1, v2, ...], color, note), ...]
    """
    n = len(groups)
    h = h or (pad[3] + pad[2] + n * 62)
    x0, x1 = pad[0], w - pad[1]
    ytop, ybot = pad[3], h - pad[2]
    allv = [v for _, vs, _, _ in groups for v in vs]
    lo = min(allv + [ref]) if lo is None else lo
    hi = max(allv + [ref]) if hi is None else hi
    span = (hi - lo) or 1
    lo, hi = lo - span * 0.08, hi + span * 0.08

    def X(v):
        return x0 + (v - lo) / (hi - lo) * (x1 - x0)

    o = [svg_open(w, h)]
    for v in ticks(lo, hi, 9 if (hi - lo) > 40 else 5):
        x = X(v)
        o.append(ln(x, ytop, x, ybot, GRID, 1))
        o.append(t(x, ybot + 20, pfmt(v, unit), 11.5, MUTED))
    if ref is not None:
        o.append(ln(X(ref), ytop, X(ref), ybot, '#D5DCE1', 1.5))
    step = (ybot - ytop) / n
    for i, (lab, vs, col, note) in enumerate(groups):
        cy = ytop + step * (i + 0.5)
        o.append(t(x0 - 14, cy + 4, lab, 12.5, INK2, 'end'))
        if note:
            o.append(t(x0 - 14, cy + 20, note, 10.5, MUTED, 'end'))
        if vs:
            m = sum(vs) / len(vs)
            o.append(rc(X(min(vs)), cy - 3, X(max(vs)) - X(min(vs)), 6, col, 3, op=0.16))
            o.append(ln(X(m), cy - 11, X(m), cy + 11, col, 2.6))
            for v in vs:
                o.append(circ(X(v), cy, 5.2, col, '#fff', 1.6, op=0.95))
            o.append(t(X(max(vs)) + 12, cy + 4, f'{mean_label} {m:+.1f}{unit}', 11.5, col,
                       'start', weight='700'))
    o.append('</svg>')
    return ''.join(o)


def diverging_matrix(rows, cols, data, w=W, h=None, pad=(150, 26, 30, 74), cell=None,
                     lo=-2, hi=2, unit='', row_note=None):
    """scenario x sector impact matrix. data[r][c] = float in [lo,hi] or None.

    Cells are ALWAYS text-labelled, so colour is redundant encoding, not the only one.
    Diverging scale: two hues + a neutral grey midpoint (dataviz rule).
    """
    nr, nc = len(rows), len(cols)
    ch = cell or 46
    h = h or (pad[3] + pad[2] + nr * (ch + 4) + 14)
    x0 = pad[0]
    cw = (w - pad[0] - pad[1]) / nc
    ytop = pad[3]

    def col(v):
        if v is None: return '#F2F5F7'
        if v == 0:    return '#E6EBEF'
        a = min(abs(v) / max(abs(lo), abs(hi)), 1.0) * 0.82 + 0.12
        return ACCENT4 if v < 0 else ACCENT

    o = [svg_open(w, h)]
    for j, c in enumerate(cols):
        o.append(t(x0 + cw * (j + 0.5), ytop - 12, c, 11.5, INK2, weight='650'))
    for i, r in enumerate(rows):
        cy = ytop + i * (ch + 4)
        o.append(t(x0 - 14, cy + ch / 2 + 4, r, 12.5, INK2, 'end'))
        if row_note:
            o.append(t(x0 - 14, cy + ch / 2 + 20, row_note[i], 10.5, MUTED, 'end'))
        for j in range(nc):
            v = data[i][j]
            fill = col(v)
            op = 0.16 + min(abs(v) / 2, 1.0) * 0.72 if v else 0.0
            o.append(rc(x0 + cw * j + 2, cy, cw - 4, ch, fill, 6, op=op))
            lab = '—' if v is None else (f'{v:+.0f}' if v else '0')
            txt = '#fff' if (v and abs(v) >= 1) else (INK3 if v is None else INK2)
            o.append(t(x0 + cw * (j + 0.5), cy + ch / 2 + 5, lab, 12.5, txt, weight='700'))
    o.append('</svg>')
    return ''.join(o)


def scenario_grid(cells, w=W, h=300, pad=(20, 20, 34, 30), gap=10):
    """2x2 outcome grid. cells = [tl, tr, bl, br], each = (title, pct, color, lines[])."""
    x0, x1 = pad[0], w - pad[1]
    ytop, ybot = pad[3], h - pad[2]
    cw = (x1 - x0 - gap) / 2
    chh = (ybot - ytop - gap) / 2
    o = [svg_open(w, h)]
    for k, cell in enumerate(cells):
        cx = x0 + (k % 2) * (cw + gap)
        cy = ytop + (k // 2) * (chh + gap)
        title, pct, col, lines = cell
        o.append(rc(cx, cy, cw, chh, col, 10, op=0.07))
        o.append(rc(cx, cy, cw, chh, 'none', 10, stroke=col, sw=1.4))
        o.append(t(cx + 18, cy + 30, title, 14, INK, 'start', weight='700'))
        o.append(t(cx + cw - 18, cy + 34, f'{pct:.0f}%', 26, col, 'end', weight='700'))
        for i, ln_ in enumerate(lines):
            o.append(t(cx + 18, cy + 56 + i * 18, ln_, 11.5, INK2, 'start'))
    o.append('</svg>')
    return ''.join(o)


def dot_rows(rows, w=W, h=None, pad=(238, 106, 46, 30), lo=0, hi=100, unit='%',
             row_gap=52):
    """One row per forecaster, one dot per question. Every dot carries its number,
    so colour is a redundant encoding, not the only one.

    rows = [(label, sublabel, [(value, colour, tag), ...], right_note?), ...]
    A method that did not publish a number is simply absent from its list - the
    row shows what exists rather than a zero. `right_note` carries the explanation
    for a row that is deliberately empty, so it does not read as missing data.
    """
    n = len(rows)
    h = h or (pad[3] + pad[2] + n * row_gap)
    x0, x1 = pad[0], w - pad[1]
    ytop, ybot = pad[3], h - pad[2]

    def X(v):
        return x0 + (v - lo) / (hi - lo) * (x1 - x0)

    o = [svg_open(w, h)]
    for v in ticks(lo, hi, 6):
        x = X(v)
        o.append(ln(x, ytop, x, ybot, GRID, 1))
        o.append(t(x, ybot + 20, pfmt(v, unit), 11.5, MUTED))
    o.append(ln(x0, ybot, x1, ybot, '#D5DCE1', 1.5))
    step = (ybot - ytop) / n
    for i, r in enumerate(rows):
        lab, sub, pts = r[0], r[1], r[2]
        note = r[3] if len(r) > 3 else ''
        cy = ytop + step * (i + 0.5)
        if i % 2 == 0:
            o.append(rc(x0, cy - step / 2 + 4, x1 - x0, step - 8, '#F7F9FA', 6))
        o.append(t(x0 - 14, cy + 4, lab, 12.5, INK2, 'end', weight='650'))
        if sub:
            o.append(t(x0 - 14, cy + 20, sub, 10.5, MUTED, 'end'))
        if note:
            o.append(t(x1 - 8, cy + 4, note, 11.5, MUTED, 'end'))
        for v, col, tag in sorted(pts):
            x = X(v)
            o.append(circ(x, cy, 6.5, col, '#fff', 2))
            o.append(t(x, cy - 13, f'{v:g}{unit}', 12, col, weight='700'))
            if tag:
                o.append(t(x, cy + 22, tag, 10.5, MUTED))
    o.append('</svg>')
    return ''.join(o)


def threshold_axis(bands, marks, w=W, h=236, pad=(56, 56, 40, 44),
                   lo=0, hi=16, unit='', band_y=0.74):
    """A single number line showing where a decision flips.

    bands = [(x0, x1, colour, label)]   decisive zones, shaded and named
    marks = [(x, colour, label, sub, above[, hollow])]   values on the axis
    `hollow` draws a white-cored marker: the same measurement, hypothetical status.
    Vertical stems from each mark to its label. Bands always carry a written
    label, so the shaded colour is a redundancy rather than the encoding.
    """
    x0, x1 = pad[0], w - pad[1]
    ytop, ybot = pad[3], h - pad[2]
    ymid = ytop + (ybot - ytop) * band_y

    def X(v):
        return x0 + (v - lo) / (hi - lo) * (x1 - x0)

    o = [svg_open(w, h)]
    # Zones are full-height washes with their names at the top; the axis line and
    # the marks then sit on a clean field instead of on top of the zone captions.
    o.append(f"<rect x='{X(lo):.1f}' y='{ytop:.1f}' width='{X(hi)-X(lo):.1f}' "
             f"height='{ybot-ytop:.1f}' rx='10' fill='#F7F9FA'/>")
    for xa, xb, col, lab in bands:
        o.append(rc(X(xa), ytop, X(xb) - X(xa), ybot - ytop, col, 0, op=0.13))
        o.append(ln(X(xa), ytop, X(xa), ybot, col, 1.2, dash='4 4', op=0.55))
        o.append(t((X(xa) + X(xb)) / 2, ytop - 12, lab, 12, col, weight='700'))
    o.append(ln(x0, ymid, x1, ymid, '#C3CCD3', 2))
    for v in ticks(lo, hi, 8):
        x = X(v)
        o.append(ln(x, ymid, x, ymid + 6, '#C3CCD3', 1))
        o.append(t(x, ybot + 22, f'D+{v:g}{unit}' if v else 'D+0', 11.5, MUTED))
    for mk in marks:
        v, col, lab, sub, above = mk[0], mk[1], mk[2], mk[3], mk[4]
        hollow = mk[5] if len(mk) > 5 else False
        x = X(v)
        yy = ymid - 22 if above else ymid + 22
        o.append(circ(x, ymid, 7, '#fff' if hollow else col, col, 2.4))
        o.append(ln(x, ymid, x, yy, col, 1.6, op=0.7))
        d = -1 if above else 1
        o.append(t(x, yy + d * 12, f'D+{v:g}', 13.5, col, weight='700'))
        o.append(t(x, yy + d * 28, lab, 11.5, INK2, weight='650'))
        if sub:
            # INK3 rather than MUTED: this line sits on a tinted zone wash,
            # where the muted grey loses the contrast it has on white.
            o.append(t(x, yy + d * 43, sub, 10.5, INK3))
    o.append('</svg>')
    return ''.join(o)


def diverging_bars(labels, values, w=W, h=340, pad=(210, 120, 54, 26), unit='pp',
                   neg=ACCENT4, pos=ACCENT3, dec=1, ref_label=''):
    """Signed bars around a zero line. values[i] > 0 draws right in `pos` colour.

    One axis, one scale: the sign carries the direction, the bar the magnitude.
    """
    x0, x1 = pad[0], w - pad[1]
    ytop, ybot = pad[3], h - pad[2]
    n = len(labels)
    mx = max([abs(v) for v in values] + [1]) * 1.22
    step = (ybot - ytop) / n
    bx0 = x0 + (x1 - x0) * 0.42          # zero line sits left-of-centre
    bw = (x1 - x0) * 0.54

    def X(v):
        return bx0 + v / mx * bw

    o = [svg_open(w, h)]
    tk = ticks(-mx / 2, mx / 2, 4)               # -mx/2..mx/2, not the full width
    tdec = 0 if len(tk) < 2 or tk[1] - tk[0] >= 1 else 1
    for v in tk:
        x = X(v)
        if x0 <= x <= x1:
            o.append(ln(x, ytop, x, ybot, GRID, 1))
            o.append(t(x, ybot + 20, pfmt(v, unit, tdec), 11, MUTED))
    o.append(ln(bx0, ytop, bx0, ybot, '#C3CCD3', 2))
    for i, (lab, v) in enumerate(zip(labels, values)):
        cy = ytop + step * i
        bh = min(step * 0.56, 30)
        by = cy + (step - bh) / 2
        xa, xb = (bx0, X(v)) if v >= 0 else (X(v), bx0)
        o.append(rc(xa, by, xb - xa, bh, pos if v >= 0 else neg, 4, op=0.9))
        o.append(t(x0 - 14, cy + step / 2 + 4, lab, 12, INK2, 'end'))
        tx = X(v) + (10 if v >= 0 else -10)
        o.append(t(tx, cy + step / 2 + 4, f'{v:+.1f}', 11.5,
                   pos if v >= 0 else neg, 'start' if v >= 0 else 'end', weight='700'))
    o.append('</svg>')
    return ''.join(o)


def _txt_w(s, size):
    """Rough advance width: CJK glyphs are ~1.0em, latin/digits ~0.55em."""
    return sum(size * (1.0 if ord(c) > 0x2E7F else 0.55) for c in str(s))


def timeline(events, w=W, h=300, pad=(46, 46, 60, 40), lo=None, hi=None,
             axis_lab=''):
    """events = [(date_str, label, detail, color, above_bool), ...] on a date axis.

    Dots sit at their true date. Labels are packed into two lanes (above / below)
    and pushed apart horizontally until they stop colliding, then joined back to
    their dot with an elbow leader. Clustered dates are the normal case - a
    presidential election, a runoff and a funding deadline can land inside six
    weeks - so a layout that simply centres each label on its own dot overlaps.
    """
    ev = []
    for e in events:
        d = dt.date.fromisoformat(e[0])
        det = e[2] if len(e) > 2 else ''
        col = e[3] if len(e) > 3 else ACCENT
        above = e[4] if len(e) > 4 else False
        bwid = max(_txt_w(e[1], 12.5), _txt_w(d.isoformat(), 10.5),
                   _txt_w(det, 10.5)) + 28
        ev.append(dict(d=d, lab=e[1], det=det, col=col, above=above,
                       bw=bwid, x=0.0, cx=0.0))
    ds = [e['d'] for e in ev]
    t0 = min(ds) if lo is None else dt.date.fromisoformat(lo)
    t1 = max(ds) if hi is None else dt.date.fromisoformat(hi)
    x0, x1 = pad[0], w - pad[1]
    ymid = h / 2
    span = (t1 - t0).days or 1

    for e in ev:
        e['x'] = x0 + (e['d'].toordinal() - t0.toordinal()) / span * (x1 - x0)

    # --- pack each lane ---------------------------------------------------
    for lane in (True, False):
        row = sorted([e for e in ev if e['above'] is lane], key=lambda e: e['x'])
        for i, e in enumerate(row):
            e['cx'] = e['x'] if i == 0 else max(
                e['x'], row[i - 1]['cx'] + (row[i - 1]['bw'] + e['bw']) / 2)
        if row:
            over = (row[-1]['cx'] + row[-1]['bw'] / 2) - x1
            if over > 0:
                for e in row:
                    e['cx'] -= over
            under = x0 - (row[0]['cx'] - row[0]['bw'] / 2)
            if under > 0:
                for e in row:
                    e['cx'] += under

    o = [svg_open(w, h)]
    o.append(ln(x0, ymid, x1, ymid, '#C3CCD3', 2))
    if axis_lab:
        # bottom-left, clear of both label lanes
        o.append(t(x0, h - 10, axis_lab, 11, MUTED, 'start'))
    for e in ev:
        x, cx, col, above = e['x'], e['cx'], e['col'], e['above']
        top = ymid - 34 if above else ymid + 34          # label block edge
        o.append(circ(x, ymid, 5.5, col, '#fff', 2))
        o.append(path([(x, ymid), (x, top), (cx, top)], col, 1.4, op=0.7))
        if above:   # block grows upward from `top`
            o.append(t(cx, top - 40, e['lab'], 12.5, col, weight='700'))
            o.append(t(cx, top - 25, e['d'].isoformat(), 10.5, MUTED))
            if e['det']:
                o.append(t(cx, top - 10, e['det'], 10.5, INK2))
        else:       # block grows downward from `top`
            o.append(t(cx, top + 14, e['lab'], 12.5, col, weight='700'))
            o.append(t(cx, top + 29, e['d'].isoformat(), 10.5, MUTED))
            if e['det']:
                o.append(t(cx, top + 44, e['det'], 10.5, INK2))
    o.append('</svg>')
    return ''.join(o)
