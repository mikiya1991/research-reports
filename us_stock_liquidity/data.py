# -*- coding: utf-8 -*-
"""Loads prepped FRED series and exposes chart-ready structures."""
import json, os, datetime as dt

D = os.path.dirname(os.path.abspath(__file__))
RAW = json.load(open(os.path.join(D, 'data', 'prepped.json')))


def monthly(rows):
    """keep last observation of each calendar month -> [(YYYY-MM-DD, v)]"""
    out = {}
    for d, v in rows:
        out[d[:7]] = (d, v)
    return [out[k] for k in sorted(out)]


def weekly(rows, k=4):
    """thin to ~every k-th observation, always keep last"""
    th = rows[::k]
    if th[-1] != rows[-1]:
        th = th + [rows[-1]]
    return th


def year_end(rows, y):
    c = [r for r in rows if r[0] <= f'{y}-12-31']
    return c[-1] if c else None


def last(rows):
    return rows[-1]


def first_after(rows, date):
    for r in rows:
        if r[0] >= date:
            return r
    return None


# ---- base series (dates ascending) ----
SP500_DAILY = [(d, v) for d, v in RAW['sp500_daily']]
SP500_WEEK = weekly(SP500_DAILY, 5)
WALCL = [(d, v) for d, v in RAW['walcl_week']]
RRP = [(d, v) for d, v in RAW['rrp_thin']]
RESERVES = [(d, v) for d, v in RAW['reserves_week']]
M2 = [(d, v) for d, v in RAW['m2_month']]
DGS10 = [(d, v) for d, v in RAW['dgs10_daily']]
FFR = [(d, v) for d, v in RAW['fedfunds_month']]
DGS10_MONTH = monthly(DGS10)

M2_YOY = []
for i in range(12, len(M2)):
    M2_YOY.append((M2[i][0], (M2[i][1] / M2[i - 12][1] - 1) * 100))


def since(rows, date):
    return [r for r in rows if r[0] >= date]


def stat(rows):
    """returns dict with last, max, max_date, min, min_date"""
    mx = max(rows, key=lambda r: r[1]); mn = min(rows, key=lambda r: r[1])
    return dict(last=rows[-1][1], last_date=rows[-1][0], max=mx[1], max_date=mx[0],
                min=mn[1], min_date=mn[0])
