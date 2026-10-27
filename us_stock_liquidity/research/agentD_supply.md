# 事实清单：股票供给与市场结构（agentD）
> 为《美股为何持续上涨——资金与流动性从哪里来》"股票供给与市场结构"一节核实。
> 核实执行日：**2026-10-15**（美国时间）。下文所有数字与引语均为本次会话实际抓取所得，非记忆。
> 抓取方法说明：本环境 WebFetch 被安全策略拦截，全部改用 `curl`（含 `--http1.1`）。未能访问的站点在各条目"未找到"处注明。
> 证据等级：【官方】政府/交易所/监管机构原始数据；【媒体】主流财经媒体报道；【分析师】券商/研究机构/学术论文（学术另注明）；【传闻】未经证实。

---

## 1. 美国上市公司数量

### 1.1 最新值与趋势 ——【官方】World Bank（WDI API）
- 数据源 URL：`https://api.worldbank.org/v2/country/US/indicator/CM.MKT.LDOM.NO?format=json&per_page=100`
- 抓取于 2026-10-15；响应头字段显示 `"lastupdated":"2026-10-08"`（World Bank 数据库更新日期）
- 指标原名（原句）：`"indicator":{"value":"Listed domestic companies, total"}`；国家 `"United States"`
- 年末值（家）：

| 年份 | 1979 | 1980 | 1985 | 1990 | 1995 | **1996（峰值）** | 1997 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | **2025（最新）** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 家数 | 2,401* | 5,164 | 6,260 | 6,429 | 7,487 | **8,090** | 7,905 | 3,910 | 4,104 | 4,774 | 4,642 | 4,317 | 4,010 | **3,908** |

\* 1979 为 World Bank 该序列起点，数值异常低（可能为口径切换），引用时建议从 1980 起用。
- **可用结论**：2025 年 3,908 家为 1980 年（5,164 家）以来最低；相对 1996 年峰值 8,090 家约腰斩（-51.7%，据官方数据计算）。
- 注：World Bank 原始数据源自 WFE（世界交易所联合会），反映在美上市本土公司总数。个人在正文引用时标注"世界银行 WDI，2025 年值，2026-10-08 更新"即可。

---

## 2. IPO 规模、SPAC 与回购对比

### 2.1 IPO 数量与募资 ——【分析师】stockanalysis.com
- URL：`https://stockanalysis.com/ipos/statistics/`（抓取 2026-10-15，页面标注 "As of October 14, 2026"）
- 原句：
  - "There have been **255 IPOs so far in 2026**."（2026 年至今 255 家）
  - "There were **350 IPOs in 2025**."（2024 年 226 家；2021 年 1,035 家为纪录；2008 年 62 家为最少）
  - 该页 2000–2026 年 IPO 累计 6,893 家。
- 口径提示：stockanalysis.com 口径较宽（含小市值/OTC 升板），与 Renaissance 口径差异大（见下）。

### 2.2 IPO 数量与募资 ——【分析师】Renaissance Capital（口径：≥$50mm 市值 IPO）
- 统计页 URL：`https://www.renaissancecapital.com/IPO-Center/Stats`（抓取 2026-10-15）
- 原句（2026 年至今）："There have been **114 IPOs priced this year**, a -33.7% change from last year... Total proceeds raised were **$147.6 bil this year**, a +360.9% change from last year... 203 IPOs filed this year, a -10.6%..."；同一页面另句："There have been **155 SPAC IPOs**, the most in any sector."（SPAC 为分板块口径中数量最多者）
- 2025 年度 PDF《2025 US Review》（`https://www.renaissancecapital.com/review/2025USReview_Public.pdf`，2026-01-02）原句：
  - "new issuance reached a **four-year high**, with **202 IPOs raising a combined $44.0 billion**"；"71 IPOs raising $100 million or more"；最大单为 Medline $6.3B
  - "The **SPAC market ramped up its recovery in 2025, with new issuance more than doubling from 2024**"
  - 年度对比：2022 年 $7.7B/71 家、2023 年 $19.5B/109 家、2024 年 $29.6B/150 家、2025 年 $44.0B/202 家；2025 年 Renaissance IPO Index +5% vs S&P 500 +18%
- 3Q26 季报 PDF（`https://www.renaissancecapital.com/review/3Q26USReview_Public.pdf`，2026-10-01）原句：
  - "**30 IPOs Raise Nearly $33 Billion Driven by SK hynix**"（SK hynix 单笔 $26.5B；剔除后 3Q26 仅 $6.2B）
  - 季度拆解：1Q26 $9.9B/41 家；2Q26 $104.8B/34 家；3Q26 $32.8B/30 家
  - "**Anthropic**, which is currently expected to headline the 4Q26, and **OpenAI**, now waiting until 2027 to list"
- 注：Renaissance 行业细分表在页面中被付费墙锁定（"Locked - Pro subscription required"），未能取用。

### 2.3 超大型 IPO 个案 ——【媒体】CNBC
- SpaceX：`https://www.cnbc.com/2026/06/12/spacex-coo-gwynne-shotwell-spcx-ipo.html`（2026-06-12）原句："**SpaceX is hitting the Nasdaq on Friday after a record-setting $75 billion initial share sale**"（目标估值 $1.75T）。这是 2026 年 IPO 募资额同比暴增（+360.9%）的主因。

### 2.4 2026 IPO 全年预测 ——【媒体】CNBC 引 Goldman Sachs
- URL：`https://www.cnbc.com/2026/07/23/us-ipo-activity-bubble-goldman.html`（2026-07-23）
- 原句："**U.S. IPO volumes are set to cross $200 billion this year to set a new record**"（Goldman 预测全年破 $200B 纪录）
- Goldman 的 Ben Snider 原句："The current reopening looks more like a **normalization of IPO activity — amplified by a few very large deals — than the broad-based surge** investors typically associate with an IPO boom."（同文对比：今年约 60 家美国 IPO，1999 年近 400 家、2021 年超 250 家——数量并未回到历史狂热水平）

### 2.5 回购规模（用于与 IPO 对比）
- 【媒体】CNBC 引 S&P DJI/Silverblatt（2025-08-06，`https://www.cnbc.com/2025/08/06/the-stock-markets-secret-sauce-buybacks-on-pace-for-a-record-in-2025.html`）原句：
  - "In 2024, **S&P 500 buybacks totaled $942.5 billion**."
  - "In July, companies announced buybacks totaling **$165.63 billion, a record for the month**, according to data from Birinyi Associates. Year to date, that puts buybacks at some **$926.1 billion**, Birinyi Associates' data showed."
  - Silverblatt 原句："I expect the second half to increase to and set a record for 2025."（即 2025 年 S&P 500 回购预计超过 2024 年的 $942.5B）
- 【媒体】CNBC（2026-07-23，同上 Goldman 文）引佛罗里达大学 Jay Ritter 原句："He said that **U.S. public companies return roughly $1.6 trillion to investors annually through dividends and stock buybacks**."（分红+回购合计约 $1.6T/年，即远大于 IPO 抽水规模）
- 【媒体】个案：Nvidia 追加 $150B 回购授权、总额达 $235B（CNBC 2026-09-28，`https://www.cnbc.com/2026/09/28/nvidia-share-buyback-plan-gets-150-billion-boost.html`，原句 "largest share repurchase authorization increase in history"）。
- **未找到**：2025/2026 全年 S&P 500 回购总额的官方口径（S&P Dow Jones Indices 站点 spglobal.com 全部返回 403）。上文 $942.5B 为 2024 年实值（媒体转引 S&P DJI），2025 年仅有"将创纪录"的表述与 Birinyi 截至 2025-07 的 YTD 数，请勿当作 2025 全年数使用。
- 可用的量级对比（据以上数据，媒体口径）：2026 年至今 IPO 募资 $147.6B（Renaissance 口径）vs 回购年化约 $1T 量级（2024 年 $942.5B），回购仍是股票净供给的主要负项。

---

## 3. 净股票发行（net equity issuance）——【官方】美联储 Z.1 资金流量表

- 数据源：美联储《Financial Accounts of the United States (Z.1)》当前版本，**发布日 2026-09-11**（最新季度 2026:Q2）。
- 表：**F51.1.t "Corporate equities"**（transactions, SAAR；单位 $ millions）
  - 表页 URL：`https://www.federalreserve.gov/releases/z1/current/html/F51_1_t.htm`（本次核实返回 200，页面标题 "The Fed - Financial Accounts of the United States - Z.1 - table F51.1.t"）
  - 原始数据文件：`https://www.federalreserve.gov/releases/z1/current/z1_csv_files.zip` → `csv/F51_1_t.csv`；字段说明 `data_dictionary/F51_1_t.txt`
  - 数据字典原句（口径）：`"Millions of dollars; transactions at a seasonally adjusted annual rate"`
- 使用行：**Line 2 "Nonfinancial corporate business; corporate equities; liability"**（非金融企业股票净发行；正=净发行，负=净回购）
- 值（把 SAAR $M 换算为 $B）：

| 期间 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026H1 |
|---|---|---|---|---|---|---|---|
| 年度均值（4 季 SAAR 平均） | **-74** | **-54** | **-553** | **-603** | **-397** | **-348** | **+409** |

| 季度（SAAR，$B） | 2024Q1 | 2024Q2 | 2024Q3 | 2024Q4 | 2025Q1 | 2025Q2 | 2025Q3 | 2025Q4 | 2026Q1 | 2026Q2 |
|---|---|---|---|---|---|---|---|---|---|---|
| 非金融企业净发行 | -636 | -503 | -349 | -99 | -324 | -373 | -431 | -264 | **+205** | **+613** |

- **可用结论**：非金融企业股票净发行 2005–2025 连续为负（净回购主导股票供给），2026 年上半年首次转正（2026Q2 +$613B SAAR），为多年罕见的供给转向，值得在报告中作为"供给端变化"的警示点。
- 口径提醒（重要，防止误用）：
  - 表内 Line 1/17 "All sectors; corporate equities; asset"（2024Q4 +$1,683B；2025Q4 +$1,890B；2026Q2 +$2,953B SAAR）**不等于**各负债行加总（2025Q4：1,890,359 vs 3,885,539，单位 $M），因其含 ETF/基金份额等金融部门负债项、外国股票与估值口径差异——请勿把 Line 1 当"净发行"引用。
  - 其中 Line 8 "Exchange-traded funds; total financial assets"（ETF 份额发行）2025Q4 高达 +$2,076B SAAR，说明"净供给"讨论需区分企业融资与基金份额创设两类口径。
- 【媒体】交叉印证：CNBC/Goldman（2026-07-23，URL 同 2.4）原句提示欧洲"net equity issuance, after accounting for redemptions and buybacks, remains slightly negative at **-0.2% of market capitalization**"（欧洲；可对比说明美国同样存在净发行收缩）。

---

## 4. 并购（M&A）——【媒体】CNBC 引 PitchBook / PwC

- 2025 年美国并购（PitchBook）：CNBC 2025-12-19（`https://www.cnbc.com/2025/12/19/wall-street-deals-2025-trump-tariffs-uncertainty.html`）原句：
  - "Through Dec. 15 this year, there were roughly **13,900 transactions in the U.S.**, compared with 15,940 deals during the same period in 2024"（笔数下降）
  - "The 2025 deals tracked by PitchBook totaled roughly **$2.4 trillion in value**, compared with roughly $1.83 trillion in 2024"（金额上升）
  - 巨型交易：Union Pacific/Norfolk Southern $85B；Netflix/WBD $72B；EA 约 $50B
- 2025 年全球并购（PitchBook）：CNBC 2026-02-25（`https://www.cnbc.com/2026/02/25/global-ma-boom-surges-2026-ai-mega-deals-capital-squeeze-merger-and-acquisition.html`）原句："the total value of deal-making activity **surged nearly 40% to a record of $4.9 trillion in 2025**... It surpassed the previous high of $4.86 trillion set in 2021."
- 2026 年（PwC）：CNBC 2026-06-23（`https://www.cnbc.com/2026/06/23/global-ma-deal-value-on-track-to-reach-4-trillion-this-year-pwc-.html`）原句："global deal value... **on track to reach $4 trillion in 2026**, making it the strongest year since 2021"；"Transactions above $5 billion now account for **48% of global deal value**, compared with 39% in 2025 and 26% in 2024"；个案：SpaceX 收购 Cursor 约 $60B。
- 可用结论：并购活跃度（尤其巨型交易占比）处于历史高位，是股票需求端"接管股票"的重要来源。

---

## 5. 被动/指数持有占比——【官方】ICI（data.ici.org）

- 数据源：ICI 官方数据平台 `https://data.ici.org/`（Dash 应用；本环境通过其 `/_dash-update-component` 回调实际取数，抓取 2026-10-15；原始响应留存于 /tmp/ici_fig42.json、/tmp/ici_fig4.json）。
- 图一（fig42）原句标题："**Index Mutual Funds: Total Net Assets**"；副标题："Millions of dollars, year-end"；数据范围 2016–2025。
- 指数共同基金 TNA（年末，$ 百万）：S&P 500 指数基金 2025=**2,284,816**（2016=763,748）；其他美国国内股票指数基金 2025=**3,146,265**；全球股票指数基金 2025=**1,017,421**；混合 62,796；债券 1,144,674。**指数股票类合计 = 6,448,502（约 $6.45T）**。
- 图二（fig4）"股票型共同基金按投资目标合计（$B，年末）"：2025 年 Capital appreciation 3,330.75 + World 3,715.00 + Total return 9,328.66 = **16,374.41（约 $16.37T）**（2016 年合计 8,567.04）。
- **计算（据上述官方数据的推导，非 ICI 直接发布）**：指数股票共同基金占股票型共同基金资产 = **39.4%（2025）**，2016 年为 **25.0%**（2,144,633/8,567,040）。
- 口径提醒：以上为**共同基金**（不含 ETF）。ICI 官网 ici.org 与 icifactbook.org 均 403，无法直接读取 Fact Book 的"指数基金（含 ETF）占股票基金资产"官方头版数字，**未找到**该含 ETF 的口径。若报告使用 39.4%，请标注"仅共同基金口径，据 ICI 官数据计算"。

---

## 6. 市场微观结构：0DTE、成交量、ETF 成交占比

### 6.1 0DTE 占比 ——【官方】Cboe
- URL：`https://www.cboe.com/tradable-products/0dte`（抓取 2026-10-15；页面未标注统计截止日期）
- 原句："**59% of SPX® volume traded 0DTE**"；"48% of XSP® volume traded 0DTE"；"54% annual increase in SPX® 0DTE volume since 2016"。

### 6.2 期权成交热度 ——【媒体】CNBC
- URL：`https://www.cnbc.com/2026/08/08/record-breaking-week-for-options-powers-sp-500-surge.html`（2026-08-08 发布，指 2026-08-04 周二）
- 原句：
  - "Stock market bulls got some huge affirmation this week as **the S&P 500 made all-time highs, options volumes set records**..."
  - "**More than four million S&P 500 index calls traded on Cboe Global Markets Tuesday** as the benchmark gauge surged above 7,700 for the first time in history. That topped the previous record for call trading in May by 10%, according to exchange data."
  - "**Zero-day-to-expiry call options accounted for 2.4 million trades in the S&P 500 on Tuesday, also a record.**"
  - "Total open interest in the S&P 500 ended the week at 27.4 million contracts, in the 93rd percentile over the past year, according to Cboe."

### 6.3 美股整体成交额趋势 ——【官方】Cboe 历史市场成交量文件（本次新发现）
- 页面 URL：`https://www.cboe.com/us/equities/market_statistics/historical_market_volume/`
- 页面原句（口径，逐字）："Cboe is a leading source of market data for the industry providing comprehensive market share and volume statistics for the U.S. equities markets. **The following files contain historical market data for all of the U.S. equities exchanges and trade-reporting facilities (TRFs)**, dating back to January 2009. The historical market volume files include the following data for each market center, broken down by Tape (Tape A, B, C): **Total shares traded daily; Total notional value traded daily; Total number of trades occurring daily.**"
- 数据文件（官方 CSV，逐月 × 市场中心）：
  - `https://cdn.cboe.com/resources/us/equities/market-statistics/historical-market-volume/market_history_monthly_2026.csv`（至 2026-09）
  - `.../market_history_monthly_2025.csv`、`.../market_history_monthly_2024.csv`
- CSV 表头原句："Month,Market Participant,Tape A Shares,Tape B Shares,Tape C Shares,Total Shares,Tape A Notional,Tape B Notional,Tape C Notional,Total Notional,Tape A Trade Count,Tape B Trade Count,Tape C Trade Count,Total Trade Count"
- 该文件覆盖当月在美全部交易所与 TRF（2026-09 当月列示 21 家市场中心：NYSE/Nasdaq/Arca/MEMX/IEX/TRF 等），对全部市场中心求和即为**全美股票总成交量**（据官方数据汇总计算）：

| 月份 | 总名义额($T) | 总股数(十亿股) | Cboe四场所份额(%) |
|---|---|---|---|
| 2024-01 | 12.29 | 242.6 | 11.8 |
| 2024-06 | 11.53 | 225.7 | 9.8 |
| 2024-12 | 14.13 | 308.9 | 9.5 |
| 2025-03 | 16.34 | 336.2 | 9.5 |
| 2025-06 | 15.95 | 364.9 | 9.6 |
| 2025-10 | 21.94 | 482.9 | 10.2 |
| 2025-12 | 18.82 | 349.3 | 8.6 |
| 2026-03 | 24.24 | 450.4 | 9.9 |
| 2026-06（区间最高） | 27.12 | 491.0 | 8.7 |
| 2026-09（最新） | 20.42 | 356.8 | 8.3 |

- 汇总（据官方数据计算）：
  - 2024 全年合计 **$153.15T / 3,064 十亿股**；2025 全年 **$206.07T / 4,396 十亿股**，名义额同比 **+34.6%**。
  - 2026 前 9 月 **$197.33T**，2025 同期 $146.79T，同比 **+34.4%**；2026 年以来月均约 $21.9T（2025 年月均 $17.2T）。
  - Cboe 四家交易所（BZX/BYX/EDGA/EDGX）合计份额由 2024-01 的 **11.8%** 降至 2026-09 的 **8.3%**（更多成交向 TRF/其他场所迁移，可作为"成交场所结构变化"的官方数据点）。
- **未找到**：全美官方口径的**日均**成交额趋势（SIFMA 站点 000 超时、Cboe 页面日度数据为 JS 动态加载未取得）。Cboe 文件为月度合计，日均需除以当月交易日数，**按规则不估算**；建议报告直接使用"月度总名义额"或"年同比 +34%"表述。
- **未找到**：ETF 占美股成交量的比例（无可核实来源，ICI 相关页面 403）。

---

## 7. 学术/权威研究（被动流入、价格弹性、指数纳入）——【分析师/学术】NBER

1. **Gabaix & Koijen, "In Search of the Origins of Financial Fluctuations: The Inelastic Markets Hypothesis"**, NBER Working Paper **w28967**，2021-06-28。
   - 链接：`https://www.nber.org/papers/w28967`（PDF：`https://www.nber.org/system/files/working_papers/w28967/w28967.pdf`）
   - 摘要原句："the price elasticity of demand of the aggregate stock market is small, and flows in and out of the stock market have large impacts on prices. Using the recent method of granular instrumental variables, we find that **investing $1 in the stock market increases the market's aggregate value by about $5**."
   - 用途：被动/整体资金流入对价格的非比例放大效应（资金流弹性 ~5 倍）。
2. **Jiang, Vayanos & Zheng, "Passive Investing and the Rise of Mega-Firms"**, NBER Working Paper **w28253**，2020-12-28。
   - 链接：`https://www.nber.org/papers/w28253`
   - 摘要原句："**Flows into passive funds raise disproportionately the stock prices of the economy's largest firms**, and especially those large firms that the market overvalues. These effects are sufficiently strong to cause the aggregate market to rise even when flows are entirely due to investors switching from active to passive."
   - 用途：被动化对大盘股/指数权重的推力（解释"少数大市值股票拉动指数"）。
3. **Greenwood & Sammon, "The Disappearing Index Effect"**, NBER Working Paper **w30748**，2022-12-12。
   - 链接：`https://www.nber.org/papers/w30748`
   - 结论：指数纳入的短期价格效应基本消失——**反向证据**，用于平衡"指数纳入必然推价"的论断。
- **未找到**：BIS 与 IMF 的具体工作论文（bis.org 站内搜索无结果、imf.org 403）。以上 3 篇 NBER 论文均为本次逐篇打开 PDF/摘要核实。

---

## 8. 未找到清单（已尽力尝试）
| 项 | 结论 | 已尝试 |
|---|---|---|
| 2025/2026 全年 S&P 500 回购总额（官方口径） | **未找到**（仅有 2024 年 $942.5B 与 2025 年"将创纪录"表述） | spglobal.com 403；S&P DJI 站点不可达 |
| 美股官方口径**日均**成交额趋势 | **未找到**（获得月度官方合计，见 6.3） | SIFMA 000；Cboe 日度数据为 JS 动态 |
| ETF 占美股成交量比例 | **未找到** | ICI 403；无可核实来源 |
| 指数基金（含 ETF）占股票基金资产官方头版比例 | **未找到**（已给出仅共同基金口径的官方数据+推导 39.4%） | ici.org / icifactbook.org 均 403 |
| BIS/IMF 相关论文 | **未找到** | bis.org 搜索空结果；imf.org 403 |
| Renaissance 行业细分数据 | 付费墙 | 页面显示 "Locked - Pro subscription required" |

> 存储说明：本清单核对过程中下载/生成的佐证文件位于 /tmp（wb_us_listed.json、cboe_m_2024/2025/2026.csv、ici_fig42.json、ici_fig4.json、w28967.pdf、w28253.pdf、rena_2025.pdf、rena_3q26.pdf、z1ext/ 等），如需复核可在同机访问。
