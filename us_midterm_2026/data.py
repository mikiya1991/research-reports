# -*- coding: utf-8 -*-
"""Loads computed datasets for the 2026 midterm report.

Series note: data/sp500_monthly_multpl.json is the multpl monthly series, which
cross-validates against the FRED daily month-AVERAGE (mean abs dev 0.021%), NOT
the month-end close (1.823%). Every long-history figure in this report is built
on month averages; label charts accordingly.
"""
import json, os, csv, datetime as dt

D = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(D, 'data')

MIDTERM = json.load(open(os.path.join(DATA, 'midterm_stats.json')))
PATHS = json.load(open(os.path.join(DATA, 'election_year_paths.json')))
SP500_M = json.load(open(os.path.join(DATA, 'sp500_monthly_multpl.json')))

# daily S&P (FRED SP500, re-pulled 2026-10-17; spans 2016-10-17 .. 2026-10-15)
_liq = os.path.join(DATA, 'SP500_fresh.csv')
SP500_D = [(d, float(v)) for d, v in list(csv.reader(open(_liq)))[1:] if v]

# --- 2026 market state, verified against the raw FRED daily series -----------
LAST_DATE, LAST_CLOSE = SP500_D[-1]          # 2026-10-15, 7744.06
Y2025_CLOSE = dict(SP500_D)['2025-12-31']    # 6845.50  (was wrongly 6929.12)
YTD_2026 = LAST_CLOSE / Y2025_CLOSE - 1      # +13.13%
D_2026 = [(d, v) for d, v in SP500_D if d >= '2026-01-01']
HIGH_2026 = max(D_2026, key=lambda x: x[1])  # 2026-10-06, 7818.93 = record close
LOW_2026 = min(D_2026, key=lambda x: x[1])   # 2026-03-30, 6343.72
DD_FROM_ATH = LAST_CLOSE / HIGH_2026[1] - 1  # -0.96%
_jan_hi = max([r for r in D_2026 if r[0] < '2026-02-01'], key=lambda x: x[1])
Q1_DD_2026 = LOW_2026[1] / _jan_hi[1] - 1    # Jan peak -> Mar trough
RALLY_OFF_LOW = HIGH_2026[1] / LOW_2026[1] - 1

# --- month-average indexed series ------------------------------------------
MIDX = {(int(d[:4]), int(d[5:7])): float(v) for d, v in SP500_M}
MIDTERM_YEARS = [y for y in range(1950, 2023) if (y - 2) % 4 == 0 and (y, 1) in MIDX]

ELECTION_2026 = '2026-11-03'
# Each midterm's own election day. 图 4 cuts every path here so the three curves
# are read at the same point in the cycle rather than at three different ones.
ELECTION_DAY = {'2018': '2018-11-06', '2022': '2022-11-08', '2026': '2026-11-03'}
# index value (year's first trading day = 100) on / before that day
ENTER = {y: max((p for p in PATHS[y] if p[0] <= d), key=lambda p: p[0])
         for y, d in ELECTION_DAY.items()}
ENTER_PCT = {y: v - 100 for y, (_, v) in ENTER.items()}
REPORT_DATE = '2026-10-17'
DAYS_TO_ELECTION = (dt.date(2026, 11, 3) - dt.date(2026, 10, 17)).days


def fwd12(y):
    """Oct(midterm y) -> Oct(y+1), month-average series."""
    return MIDX[(y + 1, 10)] / MIDX[(y, 10)] - 1


def maxdd_post(y, k=12):
    """max peak-to-trough drawdown within the k months after the midterm Oct."""
    s = []
    for i in range(k + 1):
        yy, mm = y, 10 + i
        while mm > 12: mm -= 12; yy += 1
        if (yy, mm) in MIDX: s.append(MIDX[(yy, mm)])
    if len(s) < 2: return None
    peak, w = s[0], 0.0
    for v in s:
        peak = max(peak, v); w = min(w, v / peak - 1)
    return w


# --- outcome typology: modern midterms classified by RESULT TYPE ------------
# Control facts (House/Senate winners) are standard, well-documented history.
OUTCOME_ROWS = [
    (1990, 'R', 'pres_party_holds',  '执政党保住两院',            'D', 'D'),
    (1994, 'D', 'opposition_sweep',  '在野党拿下两院',            'R', 'R'),
    (1998, 'D', 'no_flip',           '未翻盘（执政党还小赢）',    'R', 'R'),
    (2002, 'R', 'no_flip',           '未翻盘（执政党还小赢）',    'R', 'R'),
    (2006, 'R', 'opposition_sweep',  '在野党拿下两院',            'D', 'D'),
    (2010, 'D', 'split',             '分裂：在野党只拿众议院',    'R', 'D'),
    (2014, 'D', 'opposition_sweep',  '在野党拿下两院',            'R', 'R'),
    (2018, 'R', 'split',             '分裂：在野党只拿众议院',    'D', 'R'),
    (2022, 'D', 'split',             '分裂：在野党只拿众议院',    'R', 'D'),
]
OUTCOME_TYPES = ['no_flip', 'pres_party_holds', 'opposition_sweep', 'split']
TYPE_LABEL = {
    'no_flip':          '未翻盘 · 执政党保住两院',
    'pres_party_holds': '维持现状 · 执政党保住两院',
    'opposition_sweep': '在野党拿下两院',
    'split':            '分裂国会 · 在野党只拿众议院',
}
# Colours follow the MERGED three-way grouping used in 图 5 (no_flip and
# pres_party_holds are the same outcome: the president's party keeps both
# chambers). Validated as a set: #0A9960/#2F6FB8/#C0392B PASSES the normal-vision
# floor; adding ACCENT2 orange alongside ACCENT4 red is a hard FAIL (ΔE 14.9).
TYPE_COLOR = {
    'no_flip': '#2F6FB8', 'pres_party_holds': '#2F6FB8',
    'opposition_sweep': '#0A9960', 'split': '#C0392B',
}
OUTCOME_DATA = {t: [(y, fwd12(y) * 100, maxdd_post(y) * 100)
                    for y, _, k, _, _, _ in OUTCOME_ROWS if k == t]
                for t in OUTCOME_TYPES}

# --- era split: does the midterm edge survive? ------------------------------
ERAS = [('1950–1986', 1950, 1987), ('1990–2006', 1990, 2007), ('2010–2022', 2010, 2023)]


def era_excess(lo, hi):
    """midterm-year fwd12m minus the mean of its two neighbouring cycle years."""
    out = []
    for y in MIDTERM_YEARS:
        if not (lo <= y < hi): continue
        nb = [MIDX[(y, 10)] / MIDX[(y - 1, 10)] - 1, MIDX[(y + 2, 10)] / MIDX[(y + 1, 10)] - 1]
        out.append((y, (fwd12(y) - sum(nb) / 2) * 100))
    return out


ERA_EXCESS = [(lab, era_excess(lo, hi)) for lab, lo, hi in ERAS]

# --- seasonal: mean monthly return, midterm years vs all years --------------
def _prev(y, m):
    """the calendar month immediately before (y, m)."""
    return (y - 1, 12) if m == 1 else (y, m - 1)


def month_means(years):
    out = {}
    for m in range(1, 13):
        rs = []
        for y in years:
            p = _prev(y, m)
            if (y, m) in MIDX and p in MIDX:
                rs.append(MIDX[(y, m)] / MIDX[p] - 1)
        out[m] = (sum(rs) / len(rs) * 100, sum(1 for r in rs if r > 0) / len(rs) * 100)
    return out


SEASON_MID = month_means(MIDTERM_YEARS)
SEASON_ALL = month_means([y for y in range(1950, 2026) if (y, 1) in MIDX])

# --- headline aggregates ----------------------------------------------------
POST12 = [fwd12(y) * 100 for y in MIDTERM_YEARS]
POST12_MEAN = sum(POST12) / len(POST12)
POST12_MED = sorted(POST12)[len(POST12) // 2]
POST12_POS = sum(1 for x in POST12 if x > 0)
POSTDD = [maxdd_post(y) * 100 for y in MIDTERM_YEARS]
POSTDD_MEAN = sum(POSTDD) / len(POSTDD)
POSTDD_WORST = min(POSTDD)
POSTDD_GT5 = sum(1 for x in POSTDD if x <= -5)
BASE_NOV = MIDTERM['baseline_nov_nov']
POST_YR = [r['post_yr'] for r in MIDTERM['rows']]
POST_YR_MEAN = sum(POST_YR) / len(POST_YR)

# --- election-year calendar return ------------------------------------------
CAL = {y: MIDX[(y, 12)] / MIDX[(y - 1, 12)] - 1
       for y in MIDTERM_YEARS if (y, 12) in MIDX and (y - 1, 12) in MIDX}
