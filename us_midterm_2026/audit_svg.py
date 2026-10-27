# -*- coding: utf-8 -*-
"""Geometry audit of every inline SVG in the built report.

Two checks, both mechanical:
  1. spill   - any text element whose estimated box falls outside the viewBox
  2. collide - any two text elements in the same chart whose boxes overlap

Text width is estimated from the glyph mix: CJK is ~1.0em, latin/digits ~0.55em.
The attributes are matched in the exact order charts.t() emits them, because a
lazy pattern that makes text-anchor optional silently fails to capture it and
reports phantom spills.
"""
import io
import re
import sys

LAT = 0.55
CJK = 1.0

SVG_RE = re.compile(r"<svg[^>]*viewBox='0 0 (\d+) (\d+)'[^>]*>(.*?)</svg>", re.S)
TXT_RE = re.compile(
    r"<text x='([-\d.]+)' y='([-\d.]+)' font-size='([\d.]+)' fill='[^']*' "
    r"text-anchor='(\w+)' font-weight='([\w]+)'(?: transform='rotate\(([-\d.]+))?[^>]*>([^<]*)</text>"
)


def width(s, size):
    return sum(size * (CJK if ord(c) > 0x2E7F else LAT) for c in s)


def main(path):
    doc = io.open(path, encoding='utf-8').read()
    caps = re.findall(r"""class=['"]ft['"]>([^<]*)<""", doc)
    spills, collisions, total = [], [], 0
    for ci, (w, h, body) in enumerate(SVG_RE.findall(doc)):
        W, H = int(w), int(h)
        boxes = []
        for m in TXT_RE.finditer(body):
            x, y, size, anchor, weight, rot, s = m.groups()
            x, y, size = float(x), float(y), float(size)
            total += 1
            tw = width(s, size)
            if anchor == 'end':
                x0 = x - tw
            elif anchor == 'start':
                x0 = x
            else:
                x0 = x - tw / 2
            x1 = x0 + tw
            # y is the baseline; ascender ~0.78em, descender ~0.22em
            y0, y1 = y - size * 0.78, y + size * 0.22
            tag = caps[ci] if ci < len(caps) else f'svg{ci + 1}'
            if x0 < -1 or x1 > W + 1 or y0 < -1 or y1 > H + 1:
                spills.append((tag, s[:40], round(x0, 1), round(x1, 1), round(y0, 1),
                               round(y1, 1), W, H))
            boxes.append((x0, y0, x1, y1, s, tag))
        boxes.sort()
        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                a, b = boxes[i], boxes[j]
                if b[0] >= a[2] or b[1] >= a[3]:
                    continue
                ox = min(a[2], b[2]) - max(a[0], b[0])
                oy = min(a[3], b[3]) - max(a[1], b[1])
                if ox > 2.0 and oy > 2.0:
                    collisions.append((a[5], a[4][:26], b[4][:26], round(ox, 1), round(oy, 1)))
    print(f"图 {len(caps)} 张，SVG {len(SVG_RE.findall(doc))} 个，文本元素 {total} 个")
    print(f"越界  {len(spills)} 个")
    for s in spills[:25]:
        print("   ", s)
    print(f"重叠  {len(collisions)} 对")
    for c in collisions[:25]:
        print("   ", c)
    return 0 if not spills and not collisions else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else 'us_midterm_2026_report.html'))
