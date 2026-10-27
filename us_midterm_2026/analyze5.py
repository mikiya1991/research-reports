# -*- coding: utf-8 -*-
"""Risk side: drawdowns in the 12 months AFTER a midterm, and the 'when does the year peak' question."""
import json, os, csv, statistics as st, datetime as dt

D = os.path.dirname(os.path.abspath(__file__))
M = json.load(open(os.path.join(D, 'data', 'sp500_monthly_multpl.json')))
idx = {(int(d[:4]), int(d[5:7])): float(v) for d, v in M}
MIDTERM = [y for y in range(1950, 2023) if (y - 2) % 4 == 0 and (y, 1) in idx]

def seq(y, k0, k1):
    """month-end(AVG) sequence from Oct+y k0 .. Oct+y k1"""
    out = []
    for k in range(k0, k1 + 1):
        yy, mm = y, 10 + k
        while mm > 12: mm -= 12; yy += 1
        while mm < 1: mm += 12; yy -= 1
        if (yy, mm) in idx: out.append(((yy, mm), idx[(yy, mm)]))
    return out

print("=" * 100)
print("MAX DRAWDOWN inside the 12 months AFTER the midterm (monthly avg series)")
print("=" * 100)
dds = []
for y in MIDTERM:
    s = seq(y, 0, 12)
    if len(s) < 13: continue
    peak = s[0][1]; worst = 0.0; wm = None
    for (k, v) in s:
        if v > peak: peak = v
        dd = v / peak - 1
        if dd < worst: worst, wm = dd, k
    dds.append((y, worst * 100, wm))
    print(f"  {y}  max DD {worst*100:+7.2f}%   trough at month +{wm}   (12m total {s[-1][1]/s[0][1]-1:+6.1%})")
v = [d for _, d, _ in dds]
print(f"\n  n={len(v)}  mean={st.mean(v):+6.2f}%  median={st.median(v):+6.2f}%  worst={min(v):+6.2f}%")
print(f"  cycles with a >10% drawdown: {sum(1 for x in v if x <= -10)}/{len(v)}")
print(f"  cycles with a >5% drawdown : {sum(1 for x in v if x <= -5)}/{len(v)}")

print()
print("=" * 100)
print("WHEN DOES THE MIDTERM YEAR PEAK? (is the high before or after election day?)")
print("=" * 100)
before = after = 0
for y in MIDTERM:
    s = [(m, idx[(y, m)]) for m in range(1, 13) if (y, m) in idx]
    if len(s) < 12: continue
    m = max(s, key=lambda x: x[1])[0]
    tag = 'BEFORE election' if m <= 10 else 'AFTER election'
    if m <= 10: before += 1
    else: after += 1
    print(f"  {y}  year high in month {m:>2}  -> {tag}")
print(f"\n  peaks before/at Oct: {before}   peaks in Nov-Dec: {after}  (n={before+after})")

print()
print("=" * 100)
print("SAME TEST IN THE MODERN ERA ONLY (1990+) + what it means sizing-wise")
print("=" * 100)
mod = [d for y, d, _ in dds if y >= 1990]
print(f"  1990+ max DD: n={len(mod)} mean={st.mean(mod):+6.2f}% med={st.median(mod):+6.2f}% worst={min(mod):+6.2f}%")
