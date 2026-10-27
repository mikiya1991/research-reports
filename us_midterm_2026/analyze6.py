# -*- coding: utf-8 -*-
"""Analogue mapping: classify modern midterms by OUTCOME TYPE, then look at the market response.
Seat/control facts below are well-documented; they are hand-entered, not derived."""
import json, os, statistics as st

D = os.path.dirname(os.path.abspath(__file__))
M = json.load(open(os.path.join(D, 'data', 'sp500_monthly_multpl.json')))
idx = {(int(d[:4]), int(d[5:7])): float(v) for d, v in M}

def fwd(y, k=12):
    yy, mm = y, 10 + k
    while mm > 12: mm -= 12; yy += 1
    return idx[(yy, mm)] / idx[(y, 10)] - 1

def dd(y, k=12):
    s = []
    for i in range(k + 1):
        yy, mm = y, 10 + i
        while mm > 12: mm -= 12; yy += 1
        if (yy, mm) in idx: s.append(idx[(yy, mm)])
    peak = s[0]; w = 0
    for v in s:
        peak = max(peak, v); w = min(w, v / peak - 1)
    return w

# (year, president party, outcome label, who controls House after, who controls Senate after)
OUT = [
 (1990, 'R', 'status quo: pres party keeps both',            'D', 'D'),
 (1994, 'D', 'opposition wins BOTH chambers',                'R', 'R'),
 (1998, 'D', 'no flip: pres party holds, even gains seats',  'R', 'R'),
 (2002, 'R', 'no flip: pres party holds and gains',          'R', 'R'),
 (2006, 'R', 'opposition wins BOTH chambers',                'D', 'D'),
 (2010, 'D', 'SPLIT: opposition wins House only',            'R', 'D'),
 (2014, 'D', 'opposition wins BOTH chambers',                'R', 'R'),
 (2018, 'R', 'SPLIT: opposition wins House only',            'D', 'R'),
 (2022, 'D', 'SPLIT: opposition wins House only',            'R', 'D'),
]
print("=" * 104)
print("MODERN MIDTERMS (1990-2022) BY OUTCOME TYPE  |  fwd = Oct(midterm) -> Oct(+1), month-avg series")
print("=" * 104)
print(f"{'yr':<6}{'pres':<6}{'outcome':<45}{'House':<7}{'Sen':<5}{'fwd12m':>9}{'maxDD':>9}")
rows = []
for y, pp, lab, h, s in OUT:
    f = fwd(y) * 100; d = dd(y) * 100
    rows.append((y, lab, f, d))
    print(f"{y:<6}{pp:<6}{lab:<45}{h:<7}{s:<5}{f:>+8.1f}%{d:>+8.1f}%")

print()
print("-- grouped by outcome TYPE --")
from collections import defaultdict
g = defaultdict(list)
for y, lab, f, d in rows: g[lab].append((y, f, d))
for lab, v in sorted(g.items(), key=lambda kv: -st.mean([x[1] for x in kv[1]])):
    fs = [x[1] for x in v]; ds = [x[2] for x in v]
    yrs = ','.join(str(x[0]) for x in v)
    print(f"  {lab:<45} n={len(v)} [{yrs}]  fwd mean {st.mean(fs):+6.1f}%  (range {min(fs):+.1f}..{max(fs):+.1f})  "
          f"maxDD mean {st.mean(ds):+6.1f}%  worst {min(ds):+.1f}%")

print()
print("-- the two 'no flip' cycles vs the two 'opposition sweep' cycles --")
nf = [f for y, lab, f, d in rows if lab.startswith('no flip')]
sw = [f for y, lab, f, d in rows if 'BOTH chambers' in lab]
sp = [f for y, lab, f, d in rows if lab.startswith('SPLIT')]
print(f"  no flip (1998,2002)          n=2  mean fwd {st.mean(nf):+6.1f}%")
print(f"  opposition sweep of both     n=3  mean fwd {st.mean(sw):+6.1f}%   [1994,2006,2014]")
print(f"  split Congress (2010,18,22)  n=3  mean fwd {st.mean(sp):+6.1f}%   <- the 2026 modal case")
