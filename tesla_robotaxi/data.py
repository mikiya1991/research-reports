# -*- coding: utf-8 -*-
"""Tesla Robotaxi report dataset. All figures from primary filings unless noted.
Sources: SEC EDGAR CIK 0001318605 (Q1'25-Q3'26 shareholder updates, 10-K FY2025, 10-Q Q2'26),
8-K 2026-10-02 (Q3'26 production & deliveries), California DMV permit lists.
"""

# ---- Quarterly P&L (USD millions). Source: Tesla shareholder updates Q1'25..Q2'26 ----
Q = ['Q1-25','Q2-25','Q3-25','Q4-25','Q1-26','Q2-26']
P = {
 'auto_rev':   [13967,16661,21205,17693,16234,20516],
 'energy_rev': [ 2730, 2789, 3415, 3837, 2408, 3139],
 'svc_rev':    [ 2638, 3046, 3475, 3371, 3745, 4581],
 'total_rev':  [19335,22496,28095,24901,22387,28236],
 'auto_cost':  [None, 13795,17590,14080,12812,17053],
 'energy_cost':[None,  1943, 2342, 2739, 1456, 2499],
 'svc_cost':   [None,  2880, 3109, 3073, 3399, 3933],
 'reg_credits':[  None, 439, 417, 542, 380, 146],
 'gross_profit':[3153,3878,5054,5009,4720,4751],
 'gm':         [16.3,17.2,18.0,20.1,21.1,16.8],
 'opex':       [2754,2955,3430,3600,3779,4353],
 'rd':         [None,1589,1630,1783,1946,2371],
 'sga':        [None,1366,1562,1655,1833,1982],
 'sbc':        [None, 635, 663, 954,1030,1151],
 'op_income':  [ 399, 923,1624,1409, 941, 398],
 'op_margin':  [ 2.1, 4.1, 5.8, 5.7, 4.2, 1.4],
 'adj_ebitda': [2814,3401,4227,4154,3668,3273],
 'net_income': [ 409,1172,1373, 840, 477,1114],
 'ocf':        [2156,2540,6238,3813,3937,4697],
 'capex':      [1492,2394,2248,2393,2493,5789],
 'fcf':        [ 664, 146,3990,1420,1444,-1092],
}
CASH = [('Q2-25',36782),('Q3-25',41647),('Q4-25',44059),('Q1-26',44743),('Q2-26',43524)]
DEBT_NONRECOURSE = [('Q2-25',6953),('Q3-25',7458),('Q4-25',8150),('Q1-26',9017),('Q2-26',9059)]

# ---- Annual (USD millions). Source: Q4'25 shareholder update ----
YRS = [2021,2022,2023,2024,2025]
ANN = {
 'auto_rev':  [47232,71462,82419,77070,69526],
 'energy_rev':[ 2789, 3909, 6035,10086,12771],
 'svc_rev':   [ 3802, 6091, 8319,10534,12530],
 'total_rev': [53823,81462,96773,97690,94827],
 'gm':        [25.3,25.6,18.2,17.9,18.0],
 'op_income': [ 6523,13656, 8891, 7076, 4355],
 'op_margin': [12.1,16.8,9.2,7.2,4.6],
 'adj_ebitda':[11722,19390,16631,16056,14596],
 'net_income':[ 5519,12556,14997, 7091, 3794],
 'capex':     [ 6514, 7163, 8899,11342, 8527],
 'fcf':       [ 4983, 7561, 4357, 3581, 6220],
 'cash':      [17707,22185,29094,36563,44059],
}
ANN_OPS = {  # operational
 'deliveries':[936222,1313851,1808581,1789226,1636129],
 'prod':      [930422,1369611,1845985,1773443,1654667],
 'cum_deliv': [2.3,3.7,5.5,7.3,8.9],
 'fsd_subs':  [0.4,0.5,0.6,0.8,1.1],   # millions
 'storage':   [4.0,6.5,14.7,31.4,46.7], # GWh
 'supercharger_conn':[31498,42419,54892,65495,77682],
}

# FSD active subscriptions (millions) by quarter
FSD_Q = [('Q2-25',0.95),('Q3-25',1.04),('Q4-25',1.10),('Q1-26',1.28),('Q2-26',1.48)]

# Storage deployed GWh by quarter
STORAGE_Q = [('Q1-25',10.4),('Q2-25',9.6),('Q3-25',12.5),('Q4-25',14.2),('Q1-26',8.8),('Q2-26',13.5),('Q3-26',13.7)]

# Q3-2026 production & deliveries (8-K filed 2026-10-02)
Q3_26 = {'production':464391,'deliveries':486532,'m3y_prod':457387,'m3y_deliv':478237,
         'other_prod':7004,'other_deliv':8295,'storage_gwh':13.7}

# ---- Robotaxi rollout timeline (Tesla filings) ----
ROBOTAXI_TIMELINE = [
 ('2025-06','Austin, TX','首发（配安全员）','Tesla Q4\'25 & 10-K'),
 ('2025-10','Bay Area, CA','开始服务圣何塞机场；始终配安全员（TCP许可）','Tesla Q4\'25'),
 ('2025-12','Austin, TX','开始无人驾驶测试（无乘客）','Tesla Q4\'25'),
 ('2026-01','Austin, TX','有限度撤除车内安全员','Tesla Q4\'25'),
 ('2026-04','Dallas & Houston, TX','无人监督付费载客上线','Tesla Q1\'26'),
 ('2026-07','Miami/Orlando/Tampa, FL','无人监督载客上线','Tesla Q2\'26'),
 ('进行中','Phoenix, AZ','筹备中（测试/许可/应急培训）','Tesla Q2\'26'),
 ('进行中','Las Vegas, NV','筹备中','Tesla Q2\'26'),
]

# ---- California DMV permits (primary source, as of dates noted) ----
CA_DMV = {
 'testing_with_driver_asof':'2026-09-17',
 'testing_with_driver':['AIMOTIVE','AUDI','AURORA','AutoMo USA','GATIK AI','HELM.AI','IMAGRY','KODIAK AI',
   'MAY MOBILITY','MERCEDES-BENZ RDNA','MOIA America','NISSAN','NURO','NVIDIA','OHMIO','PLUSAI','PONY.AI',
   'QUALCOMM','TELENAV','TENSOR AUTO','TESLA ROBOTAXI LLC','VUERON','WAYMO','WeRide AI','WOVEN BY TOYOTA','ZOOX'],
 'driverless_testing_asof':'2026-04-03',
 'driverless_testing':['AutoMo USA','Nuro','Tensor Auto','Waymo','WeRide AI','Zoox'],
 'deployment_asof':'2025-11-21',
 'deployment':['Mercedes-Benz RDNA','Nuro','Waymo'],
 'tesla_driverless':False,
 'tesla_deployment':False,
}

# ---- CEO Performance Award 2025 (DEF 14A 2025-09-17) ----
CEO_AWARD_MKTCAP = [2.0,2.5,3.0,3.5,4.0,4.5,5.0,5.5,6.0,6.5,7.5,8.5]  # $ trillions
CEO_AWARD_OPS = ['20M vehicles delivered','10M active FSD subscriptions','1M bots delivered',
 '1M robotaxis in commercial operation','$50B Adj. EBITDA','$80B Adj. EBITDA','$130B Adj. EBITDA',
 '$210B Adj. EBITDA','$300B Adj. EBITDA','$400B Adj. EBITDA','$400B Adj. EBITDA','$400B Adj. EBITDA']
