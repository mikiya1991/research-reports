# -*- coding: utf-8 -*-
"""Is the market at an ATH? And: does a strong run INTO the midterm predict the post-election year?"""
import json, os, csv, statistics as st, math, datetime as dt

D = os.path.dirname(os.path.abspath(__file__))
M = json.load(open(os.path.join(D, 'data', 'sp500_monthly_multpl.json')))
idx = {(int(d[:4]), int(d[5:7])): float(v) for d, v in M}
rows = [(d, float(v)) for d, v in list(csv.reader(open(os.path.join(D,'..','us_stock_liquidity','data','SP500.csv'))))[1:] if v]

print("=" * 96)
print("IS 2026 AT AN ALL-TIME HIGH? (FRED daily, 2016-10 .. 2026-10-13)")
print("=" * 96)
mx = max(rows, key=lambda x: x[1])
print(f"  series max: {mx[1]:.2f} on {mx[0]}   (n={len(rows)} obs)")
yr26 = [r for r in rows if r[0].startswith('2026')]
print(f"  2026 max  : {max(yr26, key=lambda x:x[1])[1]:.2f} on {max(yr26, key=lambda x:x[1])[0]}")
print(f"  last      : {rows[-1][1]:.2f} on {rows[-1][0]}")
print(f"  monthly(AVG) series all-time max: {max(idx.values()):.2f} at {max(idx, key=idx.get)}")

print()
print("=" * 96)
print("MEAN-REVERSION TEST: midterm-year Jan->Oct run vs the following 12 months (Oct->Oct+1)")
print("=" * 96)
print(f"{'year':<7}{'Jan->Oct':>10}{'Oct->Oct+1':>13}{'quartile':>10}")
data = []
for y in range(1950, 2023):
    if (y - 2) % 4: continue
    if (y,1) not in idx or (y,10) not in idx or (y+1,10) not in idx: continue
    pre = idx[(y,10)]/idx[(y,1)] - 1
    post = idx[(y+1,10)]/idx[(y,10)] - 1
    data.append((y, pre*100, post*100))
data.sort(key=lambda r: r[1])
for i,(y,pre,post) in enumerate(data):
    q = 'weak' if i < len(data)/3 else ('strong' if i >= 2*len(data)/3 else 'mid')
    mark = '  <-- 2026 is here (+14.0%)' if False else ''
    print(f"{y:<7}{pre:>+9.1f}%{post:>+12.1f}%{q:>10}")
n=len(data); w=data[:n//3]; s=data[-(n//3):]
print(f"\n  weakest third  pre-run mean {st.mean([r[1] for r in w]):+6.1f}%  ->  post 12m mean {st.mean([r[2] for r in w]):+6.1f}%")
print(f"  strongest third pre-run mean {st.mean([r[1] for r in s]):+6.1f}%  ->  post 12m mean {st.mean([r[2] for r in s]):+6.1f}%")
allpre=[r[1] for r in data]; allpost=[r[2] for r in data]
mp, mq = st.mean(allpre), st.mean(allpost)
cov = sum((a-mp)*(b-mq) for a,b in zip(allpre,allpost))/(len(data)-1)
r = cov/(st.stdev(allpre)*st.stdev(allpost))
print(f"  correlation(Jan->Oct run, next 12m) = {r:+.2f}   (n={len(data)})")
print(f"  ALL midterm years: pre mean {mp:+.1f}%  post mean {mq:+.1f}%")

print()
print("-- how many midterm years had a Jan->Oct run >= +10%? --")
hi = [r for r in data if r[1] >= 10]
print(f"  n={len(hi)}: " + ', '.join(f"{y}({pre:+.0f}%->{post:+.0f}%)" for y,pre,post in hi))
if hi: print(f"  their post-election 12m: mean {st.mean([r[2] for r in hi]):+.1f}%  min {min(r[2] for r in hi):+.1f}%  win {sum(1 for r in hi if r[2]>0)}/{len(hi)}")
