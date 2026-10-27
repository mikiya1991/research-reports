# -*- coding: utf-8 -*-
"""Control test: is the post-midterm window special, or is it just drift?
Group every Oct->Oct+1 12m window 1950-2025 by position in the presidential cycle."""
import json, os, statistics as st

D = os.path.dirname(os.path.abspath(__file__))
M = json.load(open(os.path.join(D, 'data', 'sp500_monthly_multpl.json')))
idx = {(int(d[:4]), int(d[5:7])): float(v) for d, v in M}

def ret(y, m, y2, m2):
    return idx[(y2, m2)] / idx[(y, m)] - 1 if (y, m) in idx and (y2, m2) in idx else None

def shift(yr, mo, k):
    mo2 = mo + k
    while mo2 > 12: mo2 -= 12; yr += 1
    while mo2 < 1: mo2 += 12; yr -= 1
    return yr, mo2

# presidential cycle position: year ending in 2 = midterm (position 2)
groups = {1: [], 2: [], 3: [], 4: []}
for y in range(1950, 2026):
    pos = ((y - 2) % 4) + 1          # 1=post-election yr, 2=midterm, 3=pre-election yr, 4=election yr
    r = ret(y, 10, y + 1, 10)
    if r is not None:
        groups[pos].append((y, r * 100))

NAME = {1: 'Yr1 post-elex  (e.g. 2023)', 2: 'Yr2 MIDTERM   (e.g. 2026)',
        3: 'Yr3 pre-elex   (e.g. 2027)', 4: 'Yr4 election   (e.g. 2028)'}
print("=" * 100)
print("CONTROL: every Oct->Oct+1 12-month window 1950-2025, grouped by presidential-cycle position")
print("=" * 100)
for p in (1, 2, 3, 4):
    v = [r for _, r in groups[p]]
    print(f"{NAME[p]:<30} n={len(v):>3}  mean={st.mean(v):+6.2f}%  med={st.median(v):+6.2f}%  "
          f"min={min(v):+7.2f}  max={max(v):+7.2f}  win={sum(1 for x in v if x>0)}/{len(v)}"
          f" ({sum(1 for x in v if x>0)/len(v)*100:.0f}%)")

# pair each midterm year against the SAME calendar year's yr1/yr3 to isolate the cycle
print()
print("-- paired: midterm-year window minus the average of its neighbouring cycle years --")
pair = []
for y in range(1950, 2025):
    if (y - 2) % 4: continue
    a = ret(y, 10, y + 1, 10)
    nb = [ret(y - 1, 10, y, 10), ret(y + 1, 10, y + 2, 10)]
    nb = [x for x in nb if x is not None]
    if a is not None and nb:
        pair.append((y, (a - st.mean(nb)) * 100, a * 100, st.mean(nb) * 100))
d = [p[1] for p in pair]
print(f"  n={len(d)}  mean excess={st.mean(d):+6.2f}pp  med={st.median(d):+6.2f}pp  "
      f"midterm outperformed in {sum(1 for x in d if x>0)}/{len(d)} cycles")
for y, e, a, n in pair:
    print(f"    {y}  midterm={a:+7.1f}%  neighbours={n:+7.1f}%  excess={e:+7.1f}pp")

# Where is the midterm-year low? month of the minimum in the daily-ish monthly series
print()
print("-- month of the midterm-year low (month-end series) --")
from collections import Counter
c = Counter()
for y in range(1950, 2023):
    if (y - 2) % 4: continue
    pts = [(m, idx[(y, m)]) for m in range(1, 13) if (y, m) in idx]
    if len(pts) == 12:
        c[min(pts, key=lambda x: x[1])[0]] += 1
for m in range(1, 13):
    if c[m]: print(f"    month {m:>2}: {'#'*c[m]} {c[m]}")
print("    (Sep-Oct lows:", c[9] + c[10], "of", sum(c.values()), ")")

# 2026 YTD position
print()
print("-- 2026 YTD --")
print(f"  2025-12 close = {idx[(2025,12)]:.2f}")
print(f"  2026-10 close = {idx[(2026,10)]:.2f}   ->  YTD {idx[(2026,10)]/idx[(2025,12)]-1:+.2%}")
