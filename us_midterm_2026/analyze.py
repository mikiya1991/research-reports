# -*- coding: utf-8 -*-
"""Extract the electoral-cycle seasonal + distributional facts from multpl monthly S&P."""
import json, os, statistics as st, datetime as dt

D = os.path.dirname(os.path.abspath(__file__))
M = json.load(open(os.path.join(D, 'data', 'sp500_monthly_multpl.json')))
# month-end index: date -> level
idx = {}
for d, v in M:
    y, m = int(d[:4]), int(d[5:7])
    idx[(y, m)] = float(v)

years = sorted({y for y, m in idx})
MIDTERM = [y for y in years if (y - 2) % 4 == 0 and y >= 1950 and y <= 2022]

def ret(y, m, back=12):
    """return over `back` months ending at (y,m)"""
    ty, tm = y, m - back
    while tm <= 0:
        tm += 12; ty -= 1
    if (ty, tm) not in idx or (y, m) not in idx: return None
    return idx[(y, m)] / idx[(ty, tm)] - 1

# ---- 1. post-midterm 12m (Nov of midterm year -> Nov of year+1) -----------------
post_nov = []
for y in MIDTERM:
    r = ret(y + 1, 11, 12)
    if r is not None: post_nov.append((y, r))

# ---- 2. calendar year of the midterm -------------------------------------------
cal = []
for y in MIDTERM:
    r = ret(y, 12, 12)
    if r is not None: cal.append((y, r))

# ---- 3. sector-free monthly seasonal: avg return by month in midterm vs other yrs
def month_stats(pool):
    out = {}
    for m in range(1, 13):
        rs = [ret(y, m, 1) for y in pool]
        rs = [r for r in rs if r is not None]
        if rs: out[m] = (st.mean(rs), st.median(rs), sum(1 for r in rs if r > 0) / len(rs), len(rs))
    return out

mt_season = month_stats(MIDTERM)
all_season = month_stats([y for y in years if y >= 1950])
pre4 = [y for y in years if (y - 3) % 4 == 0 and y >= 1950]   # year before midterm (yr3)
pre1 = [y for y in years if (y - 1) % 4 == 0 and y >= 1950]   # year before midterm? adjust

# ---- 4. window around election day ---------------------------------------------
def window(y, a, b):
    """cumulative return from month a to month b (inclusive), same year+offset"""
    def shift(yr, mo, k):
        mo2 = mo + k
        while mo2 > 12: mo2 -= 12; yr += 1
        while mo2 < 1: mo2 += 12; yr -= 1
        return yr, mo2
    s = shift(y, 10, a); e = shift(y, 10, b)
    if s not in idx or e not in idx: return None
    return idx[e] / idx[s] - 1

pre6 = [(y, window(y, -6, 0)) for y in MIDTERM]
post6 = [(y, window(y, 0, 6)) for y in MIDTERM]
post12 = [(y, window(y, 0, 12)) for y in MIDTERM]

def summarize(name, pairs, unit='%'):
    v = [r * 100 for _, r in pairs if r is not None]
    if not v: return
    print(f"{name:<34} n={len(v):>3}  mean={st.mean(v):+7.2f}{unit}  med={st.median(v):+7.2f}  "
          f"min={min(v):+7.2f}  max={max(v):+7.2f}  win={sum(1 for x in v if x>0)}/{len(v)}"
          f" ({sum(1 for x in v if x>0)/len(v)*100:.0f}%)")

print("=" * 118)
print("MIDTERM CYCLE: 1950–2022 (19 elections), month-end S&P (multpl), election = Oct month-end")
print("=" * 118)
summarize("election-year calendar return", cal)
summarize("6m pre-election (May->Oct)", pre6)
summarize("6m post-election (Oct->Apr)", post6)
summarize("12m post-election (Oct->Oct+1)", post12)
summarize("12m post-election (Nov->Nov)", post_nov)

print()
print("-- monthly mean return, midterm years vs ALL years since 1950 --")
print(f"{'mon':<6}{'midterm mean':>14}{'midterm med':>13}{'mt win%':>9}   {'all mean':>10}{'all med':>10}{'all win%':>10}")
for m in range(1, 13):
    a = mt_season[m]; b = all_season[m]
    tag = '  <-- election' if m == 10 or m == 11 else ''
    print(f"{m:<6}{a[0]*100:>13.2f}%{a[1]*100:>12.2f}%{a[2]*100:>8.0f}%   {b[0]*100:>9.2f}%{b[1]*100:>9.2f}%{b[2]*100:>9.0f}%{tag}")

# ---- 5. worst drawdown in the 3 months around the election ---------------------
print()
print("-- intra-window worst drawdown (peak-to-trough, month-end) --")
for lab, (a, b) in {'pre 3m': (-3, 0), 'post 3m': (0, 3), 'post 6m': (0, 6)}.items():
    def shift(yr, mo, k):
        mo2 = mo + k
        while mo2 > 12: mo2 -= 12; yr += 1
        while mo2 < 1: mo2 += 12; yr -= 1
        return yr, mo2
    dds = []
    for y in MIDTERM:
        pts = []
        for k in range(a, b + 1):
            yy, mm = shift(y, 10, k)
            if (yy, mm) in idx: pts.append(idx[(yy, mm)])
        if len(pts) >= 2:
            peak = pts[0]; dd = 0
            for v in pts:
                peak = max(peak, v); dd = min(dd, v / peak - 1)
            dds.append(dd * 100)
    print(f"  {lab:<8} n={len(dds)}  mean={st.mean(dds):+6.2f}%  med={st.median(dds):+6.2f}%  worst={min(dds):+6.2f}%")

# ---- 6. where 2026 sits --------------------------------------------------------
print()
print("-- 2026 context --")
last = M[-1]
print("  last monthly obs:", last)
