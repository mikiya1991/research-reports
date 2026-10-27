# -*- coding: utf-8 -*-
"""Preprocess FRED CSVs into trimmed series for charting + print key stats."""
import csv, json, os, datetime as dt

D = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(D, 'data')


def load(fn):
    rows = []
    with open(os.path.join(DATA, fn), newline='') as f:
        r = csv.reader(f)
        next(r, None)
        for row in r:
            if len(row) < 2 or row[1] in ('.', ''):
                continue
            try:
                rows.append((row[0], float(row[1])))
            except ValueError:
                continue
    return rows


def val_on_or_before(rows, date_str):
    d = dt.date.fromisoformat(date_str)
    out = None
    for ds, v in rows:
        dd = dt.date.fromisoformat(ds)
        if dd <= d:
            out = (ds, v)
        else:
            break
    return out


sp = load('SP500.csv')
wal = load('WALCL.csv')
rrp = load('RRPONTSYD.csv')
res = load('WRESBAL.csv')
m2 = load('M2SL.csv')
ffr = load('FEDFUNDS.csv')
d10 = load('DGS10.csv')
hh = load('BOGZ1FL153064486Q.csv')

print('=== SP500 ===')
for y in range(2019, 2027):
    print(y, 'year-end:', val_on_or_before(sp, f'{y}-12-31'))
print('latest:', sp[-1], 'max:', max(sp, key=lambda x: x[1]))

print('\n=== WALCL (Fed assets, $mn) ===')
print('peak:', max(wal, key=lambda x: x[1]))
print('2019-12-31:', val_on_or_before(wal, '2019-12-31'))
print('2022-04-30:', val_on_or_before(wal, '2022-04-30'))
print('latest:', wal[-1])

print('\n=== RRP ($bn) ===')
print('peak:', max(rrp, key=lambda x: x[1]))
for d in ('2022-12-30', '2023-12-29', '2024-12-31', '2025-06-30', '2025-12-31'):
    print(d, val_on_or_before(rrp, d))
print('latest:', rrp[-1])

print('\n=== WRESBAL (reserves, $mn) ===')
print('2019-09-30:', val_on_or_before(res, '2019-09-30'))
print('2022-04-30:', val_on_or_before(res, '2022-04-30'))
print('peak:', max(res, key=lambda x: x[1]))
print('latest:', res[-1])

print('\n=== M2 (monthly, $bn) ===')
print('latest:', m2[-1])
i = len(m2) - 1
print('yoy latest %:', round((m2[-1][1] / m2[i-12][1] - 1) * 100, 2))
for y in (2020, 2021, 2022, 2023, 2024, 2025):
    a = val_on_or_before(m2, f'{y}-01-31'); b = val_on_or_before(m2, f'{y}-12-31')
    print(y, 'yoy %:', round((b[1] / a[1] - 1) * 100, 1))

print('\n=== FEDFUNDS (monthly %) ===')
for d in ('2023-07-31', '2024-09-30', '2025-01-31', '2025-12-31', '2026-09-30'):
    print(d, val_on_or_before(ffr, d))
print('latest:', ffr[-1])

print('\n=== DGS10 (daily %) ===')
for d in ('2024-12-31', '2025-12-31'):
    print(d, val_on_or_before(d10, d))
print('latest:', d10[-1], 'max2026:', max([x for x in d10 if x[0] >= '2026-01-01'], key=lambda x: x[1]))

print('\n=== Household corporate equities (BOGZ1FL153064486Q) ===')
for y in (2000, 2007, 2013, 2020, 2021, 2022, 2023, 2024, 2025):
    print(y, 'Q4:', val_on_or_before(hh, f'{y}-12-31'))
print('latest:', hh[-1])

# ---- trimmed series for charts ----
def thin_daily(rows, k=5):
    return rows[::k] if rows[-1] == rows[::k][-1] else rows[::k] + [rows[-1]]

out = {
    'sp500_daily': [[d, v] for d, v in sp],
    'sp500_month': [[d, v] for d, v in sp if d.endswith(('-01', '-02', '-03', '-04', '-05', '-06',
                                                          '-07', '-08', '-09', '-10', '-11', '-12'))][0::1][-0:] ,
    'walcl_week': [[d, v] for d, v in wal],
    'rrp_thin': [[d, v] for d, v in thin_daily(rrp, 5)],
    'reserves_week': [[d, v] for d, v in res],
    'm2_month': [[d, v] for d, v in m2],
    'dgs10_daily': [[d, v] for d, v in d10],
    'fedfunds_month': [[d, v] for d, v in ffr],
}
with open(os.path.join(DATA, 'prepped.json'), 'w') as f:
    json.dump(out, f)
print('\nwrote prepped.json',
      {k: len(v) for k, v in out.items()})
