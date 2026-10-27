# -*- coding: utf-8 -*-
"""Corrected cycle labels + subperiod split + source cross-validation."""
import json, os, csv, statistics as st, datetime as dt, math
from collections import defaultdict

D = os.path.dirname(os.path.abspath(__file__))
M = json.load(open(os.path.join(D, 'data', 'sp500_monthly_multpl.json')))
idx = {(int(d[:4]), int(d[5:7])): float(v) for d, v in M}

# ---------- 1. cross-validate multpl monthly against FRED daily month-ends ----------
liq = os.path.join(D, '..', 'us_stock_liquidity', 'data', 'SP500.csv')
daily = [(dt.date.fromisoformat(d), float(v)) for d, v in list(csv.reader(open(liq)))[1:] if v]
by_ym = defaultdict(list)
for d, v in daily: by_ym[(d.year, d.month)].append((d, v))
print("=" * 104)
print("SOURCE CHECK: multpl 'monthly' vs FRED daily month-end close (overlap 2016-10 .. 2026-09)")
print("=" * 104)
print(f"{'month':<10}{'multpl':>11}{'FRED last':>11}{'FRED mean':>11}{'d vs last':>11}{'d vs mean':>11}")
dl, dm = [], []
for k in sorted(by_ym):
    if k not in idx: continue
    rows = sorted(by_ym[k]); lastv = rows[-1][1]; meanv = st.mean([v for _, v in rows])
    dl.append(idx[k] / lastv - 1); dm.append(idx[k] / meanv - 1)
    if k >= (2024, 1) or k <= (2017, 3):
        print(f"{k[0]}-{k[1]:02d}  {idx[k]:>10.2f}{lastv:>11.2f}{meanv:>11.2f}"
              f"{idx[k]/lastv-1:>10.2%}{idx[k]/meanv-1:>11.2%}")
print(f"\n  mean |multpl - FRED month-end close| = {st.mean([abs(x) for x in dl]):.3%}")
print(f"  mean |multpl - FRED month-average|   = {st.mean([abs(x) for x in dm]):.3%}")
print(f"  -> multpl series is the {'MONTH-END CLOSE' if st.mean([abs(x) for x in dl]) < st.mean([abs(x) for x in dm]) else 'MONTH AVERAGE'}")

# ---------- 2. corrected cycle labels ----------
def ret(y, m, y2, m2):
    return idx[(y2, m2)] / idx[(y, m)] - 1 if (y, m) in idx and (y2, m2) in idx else None

print()
print("=" * 104)
print("FORWARD 12-MONTH RETURN (Oct -> Oct+1), grouped by the cycle position of the STARTING year")
print("=" * 104)
groups = defaultdict(list)
for y in range(1950, 2026):
    pos = (y - 2) % 4          # 0 = midterm year (2022,2026); 1 = pre-election yr; 2 = election yr; 3 = post-elex yr1
    r = ret(y, 10, y + 1, 10)
    if r is not None: groups[pos].append((y, r * 100))
LABEL = {0: 'MIDTERM year        (2018,2022,2026)',
         1: 'pre-election year   (2019,2023,2027)',
         2: 'election year       (2020,2024)',
         3: 'post-election yr 1  (2021,2025)'}
for p in (0, 1, 2, 3):
    v = [r for _, r in groups[p]]
    sd = st.stdev(v)
    t = st.mean(v) / (sd / math.sqrt(len(v)))
    print(f"{LABEL[p]:<36} n={len(v):>3}  mean={st.mean(v):+6.2f}%  med={st.median(v):+6.2f}%  sd={sd:>5.1f}  "
          f"win={sum(1 for x in v if x>0):>2}/{len(v)}  t={t:>4.2f}")

print()
print("-- MIDTERM-year forward 12m, split by era --")
for lab, lo, hi in [('1950-1986', 1950, 1987), ('1990-2006', 1990, 2007), ('2010-2022', 2010, 2023)]:
    v = [r for y, r in groups[0] if lo <= y < hi]
    print(f"   {lab}  n={len(v)}  mean={st.mean(v):+7.2f}%  med={st.median(v):+7.2f}%  "
          f"min={min(v):+6.2f}%  win={sum(1 for x in v if x>0)}/{len(v)}")

print()
print("-- paired excess vs neighbouring cycle years, by era --")
pair = defaultdict(list)
for y in range(1950, 2025):
    if (y - 2) % 4: continue
    a = ret(y, 10, y + 1, 10)
    nb = [x for x in (ret(y - 1, 10, y, 10), ret(y + 1, 10, y + 2, 10)) if x is not None]
    if a is not None and nb: pair['all'].append((y, (a - st.mean(nb)) * 100))
for lab, lo, hi in [('1950-1986', 1950, 1987), ('1990-2006', 1990, 2007), ('2010-2022', 2010, 2023)]:
    v = [e for y, e in pair['all'] if lo <= y < hi]
    sd = st.stdev(v); t = st.mean(v) / (sd / math.sqrt(len(v)))
    print(f"   {lab}  n={len(v)}  mean excess={st.mean(v):+7.2f}pp  med={st.median(v):+7.2f}pp  "
          f"beat neighbours {sum(1 for x in v if x>0)}/{len(v)}  t={t:>4.2f}")

# ---------- 3. the short window around election day, daily (2016+) ----------
print()
print("=" * 104)
print("ELECTION-DAY WINDOW, daily (only 2018 & 2022 available pre-2026)")
print("=" * 104)
P = json.load(open(os.path.join(D, 'data', 'election_year_paths.json')))
for y in ('2018', '2022', '2026'):
    s = P[y]; dates = [dt.date.fromisoformat(d) for d, _ in s]; lv = [v for _, v in s]
    ed = dt.date(int(y), 11, 3)
    def near(k):
        tgt = ed + dt.timedelta(days=k)
        best = min(range(len(dates)), key=lambda i: abs((dates[i] - tgt).days))
        return lv[best]
    if dates[-1] < ed: 
        print(f"  {y}: series ends {dates[-1]} (pre-election)"); continue
    print(f"  {y}: 4w before={near(-28):.2f}  election day={near(0):.2f}  4w after={near(28):.2f}  "
          f"8w after={near(56):.2f}  |  -4w->+4w {near(28)/near(-28)-1:+.2%}  -4w->+8w {near(56)/near(-28)-1:+.2%}")
