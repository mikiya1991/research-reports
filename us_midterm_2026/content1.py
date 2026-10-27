# -*- coding: utf-8 -*-
"""摘要 + 第一章（事实基础）+ 第二章（市场状态）+ 第三章（历史基准率）"""
import charts as C
import data as D

OK = "<span class='b b-ok'>已证实</span>"
NEWS = "<span class='b b-news'>媒体报道</span>"
AN = "<span class='b b-analyst'>机构观点</span>"
EST = "<span class='b b-est'>估算</span>"
RUM = "<span class='b b-rumor'>未核实</span>"


def section_summary(M):
    return f"""
<h2 id="s0">摘要 · 核心判断</h2>
<p class="lede">一句话结论：这场选举的结果本身大概率已被定价；它真正危险的地方，不是谁赢，
而是它恰好落在了一个「高估值 + 加息周期 + 油价冲击 + AI 信用紧张」的基本面上。</p>

<div class="card">
<ol>
<li><b>时间：2026 年 11 月 3 日（周二），距今 {D.DAYS_TO_ELECTION} 天。</b>
全部 435 个众议院席位、35 个参议院席位（33 个常规 + 佛罗里达、俄亥俄两个补选）、36 个州长，
以及数千个州议席同时改选。{OK}</li>

<li><b>众议院翻盘几乎已成定局，参议院才是真变量。</b>
预测市场给民主党拿下众议院的概率约 90%，参议院约 61–65%；模型端分歧更大
（Decision Desk HQ 参议院 56%，Silver Bulletin 75%）。参议院算术很硬：共和党 53–47 领先，
民主党需要净赢 4 席。{NEWS}</li>

<li><b>「民调不准就看预测市场」这个想法只对一半。</b>
对众议院不对：市场给 91%，但它的边际定价者读的就是同一批民调，
民调错它就错得一样。对参议院对：参议院市场在 2026 年 1–10 月移动了 27 个百分点，
而同期全国普选民调只动了约 1.5 个百分点——那 27 个百分点里装的是战争、
候选人质量、筹款与州级信息，是民调不直接测量的东西。
<b>所以用法是：众议院看民调（并记住安全垫只有 3.5 个百分点），参议院看市场。</b>
另需知道，这个「市场」实际是几十个钱包——前 1% 的账户占了约七成交易量（见第六章）。{EST}</li>

<li><b>不要用「中期选举后必涨」这条历史规律做交易。</b>
1950–2022 的 19 次中期选举，选举后 12 个月标普 19/19 为正、均值 +18.2%，看起来无懈可击。
但把它和相邻周期年份对照后，这个超额优势在最近四个周期（2010/2014/2018/2022）已经变成
<b>−4.1 个百分点</b>，四次里只有一次跑赢。这条规律主要是 2000 年以前的现象。{EST}</li>

<li><b>真正有区分度的发现：按「结果类型」分组，本次最可能的分裂国会是历史上最差的一类。</b>
1990 年以来，参众两院分裂（在野党只拿众议院）的三次——2010、2018、2022——选举后 12 个月
平均 +8.1%，且平均要经历 −8.5% 的最大回撤，为四类结果中最差。样本只有 3 个，
只能当机制参考，不能当统计结论。{EST}</li>

<li><b>整套概率最可能错在哪里：2025 年民调系统性地低估了民主党约 6 个百分点。</b>
Silver Bulletin 的 2025 年民调评分卡显示，平均偏差方向是 6.1 个百分点、偏向共和党，
新泽西州长选举的民调误差接近 10 个百分点。如果这个偏差在 2026 年重现，
当前的 D+8 至 D+9 全国普选民调对应的实际结果会强得多。
但 2025 年 12 月的田纳西第 7 选区补选与纽约市长选举中，
民调是<b>高估</b>而非低估民主党——<b>两个方向的误差都是活的，这是本次预测最大的不确定来源。</b>{NEWS} {EST}</li>

<li><b>市场进入选举时并不便宜。</b>
标普 500 在 10 月 6 日创下 7,818.93 的收盘纪录，10 月 15 日收 7,744.06（YTD +13.1%）。
但滚动市盈率 25.8 倍、席勒 CAPE 40.8 倍（155 年历史第二高，仅次于 2000 年）、
<b>股权风险溢价已归零</b>——这是 2002 年以来的第一次。{NEWS}</li>

<li><b>选举不是当前的主导变量。</b>
真正在驱动盘面的是三件事：AI 资本开支的信用压力（CoreWeave 的 CDS 突破 1,000bp）、
伊朗战争的能源冲击（布伦特约 $105，9 月 CPI 3.7%）、以及沃什接任后美联储转入
<b>加息周期</b>（9 月 16 日加息 25bp 至 3.75–4.00%，年底前至少再加一次的概率约 93%）。{NEWS}</li>

<li><b>因此，各情景的市场影响应当理解为「叠加在脆弱基本面上的扰动」，不是独立驱动力。</b>
选举能改变的，主要是政策尾部风险与不确定性溢价；它改不了油价、改不了 AI 的资本回报、
也改不了美联储的双重使命（美联储主席不在选票上）。{EST}</li>

<li><b>被低估的尾部不在民主党横扫，而在另外两处：</b>
(a) 共和党守住两院——预测市场只给 8–11%，一旦发生是最大的预期差；
(b) 结果被质疑或延迟认证——这会推高波动率，而不是决定方向。{EST}</li>

<li><b>操作含义：不要为选举方向建仓，要为波动率建仓。</b>
历史上选举后 12 个月平均要吃 −5.6% 的回撤，11/19 次回撤超过 5%。
在股权风险溢价为零、且选举后紧接着 12 月 11 日拨款截止日的组合下，
用期权而非现货表达观点，性价比明显更高。{EST}</li>
</ol>
</div>

<div class="call warn">
<div class="t">阅读这份报告前需要知道的三件事</div>
<b>第一，数据截止 2026-10-15。</b>标普点位与涨跌幅来自 FRED 原始日线序列（本报告自行计算），
其余宏观与选情数据来自公开报道，逐条标注来源与证据等级。10 月 16 日盘中有报道称
美股因 AI 信用问题进一步下跌，但该日收盘数据未能核实，本报告不予采用。<br>
<b>第二，历史统计全部基于月均序列。</b>本报告使用的 multpl 月度标普序列经交叉验证为
<b>月平均值</b>而非月末收盘（与 FRED 日线月均偏差仅 0.02%，与月末收盘偏差 1.82%）。
所有长周期回报因此按「月均价到月均价」计算，与常见的「收盘到收盘」口径会有小幅差异。<br>
<b>第三，情景概率是本报告基于公开赔率与模型的主观合成</b>，不是任何机构的官方预测，
已全部标为 {EST}。请把它当作一组有内部一致性的假设，而不是事实。
</div>
"""


def section_facts(M):
    return f"""
<h2 id="s1">第一章 · 事实基础：选什么、什么时候、现在什么赔率</h2>
<p class="lede">在做任何推演之前，先把可核对的事实钉死。本章的全部数字都可以回到原始出处。</p>

<h3>1.1 时间与标的</h3>
<div class="grid4">
  <div class="kpi"><div class="lab">选举日</div><div class="val">11 月 3 日</div>
    <div class="sub">2026 年，周二 · 距今 {D.DAYS_TO_ELECTION} 天</div></div>
  <div class="kpi"><div class="lab">众议院</div><div class="val">435 席</div>
    <div class="sub">过半需 218 席</div></div>
  <div class="kpi"><div class="lab">参议院</div><div class="val">35 席</div>
    <div class="sub">33 常规 + FL/OH 补选</div></div>
  <div class="kpi"><div class="lab">州长</div><div class="val">36 个</div>
    <div class="sub">另有数千州议席</div></div>
</div>

<p><b>参议院的算术是这个周期里最硬的一条约束。</b>共和党目前以 53–47 领先，
由于 50–50 时副总统 JD·万斯可以投下打破平局的一票，民主党必须<b>净赢 4 席</b>才能真正控制参议院。
35 个改选席位中有 22 个是共和党持有的——这意味着地图理论上对民主党有利，
但其中多数位于特朗普在 2024 年以两位数优势拿下的州，这也是为什么各家的参议院预测差异远大于众议院。{NEWS}</p>

<h3>1.2 各家预测的差异本身就是信息</h3>
<p>众议院方面，所有来源高度一致；参议院方面分歧显著。这种分歧结构告诉我们：
<b>市场对众议院的定价是坚实的，对参议院的定价是脆弱的</b>——而脆弱的那一端，才是可能产生预期差的地方。</p>
"""


def fig_odds(M):
    # One row per forecaster, sorted by value. This is the report's only
    # source-comparison chart: chapter 6's argument cites it rather than
    # repeating it, because two charts of the same six numbers with slightly
    # different rounding is a contradiction a reader will find.
    rows = [
        ("众议院 · Decision Desk HQ", 76, 76, 76, C.ACCENT3, ""),
        ("众议院 · Quantus Insights", 85, 85, 85, C.ACCENT3, ""),
        ("众议院 · Polymarket", 91, 91, 91, C.ACCENT3, ""),
        ("众议院 · Kalshi", 92, 92, 92, C.ACCENT3, ""),
        ("众议院 · Silver Bulletin", 93, 93, 93, C.ACCENT3, ""),
        ("众议院 · FiftyPlusOne", 98, 98, 98, C.ACCENT3, ""),
        ("参议院 · Call the Map", 55, 55, 55, C.ACCENT4, ""),
        ("参议院 · Decision Desk HQ", 56, 56, 56, C.ACCENT4, ""),
        ("参议院 · Kalshi", 61, 61, 61, C.ACCENT4, ""),
        ("参议院 · Polymarket", 63, 63, 63, C.ACCENT4, ""),
        ("参议院 · Silver Bulletin", 75, 75, 75, C.ACCENT4, ""),
    ]
    svg = C.rangeline(rows, lo=40, hi=100, unit="%", ref=[(50, "五五开", C.GREY)],
                      pad=(250, 96, 44, 26))
    return f"""
<div class="fig">
  <div class="ft">图 1 · 民主党赢得两院的概率：模型与预测市场，2026 年 10 月中旬</div>
  <div class="fs">众议院 76% 到 98%，参议院 55% 到 75%——
  两院的分歧都比任何一家机构自称的置信区间大得多</div>
  {svg}
  <div class="legend">
    <span><i style="background:{C.ACCENT3}"></i>众议院</span>
    <span><i style="background:{C.ACCENT4}"></i>参议院</span>
  </div>
  <div class="note">来源：Decision Desk HQ、Quantus Insights（2026-10-06/07）、Call the Map、
  Silver Bulletin FLIPR（2026-10-08）、FiftyPlusOne、Polymarket（2026-10-09/11）、Kalshi（2026-10-09/11）。{NEWS}
  <b>专家评级机构（Cook、Inside Elections、Sabato）不在图上——它们不发布概率数字，
  只做逐选区定级，而它们对众议院的判断是「接近五五开」。</b>本报告不给它们编一个百分比，
  这一点在 6.3 节展开。{EST}
  <br>预测市场成交额合计超过 2.2 亿美元（截至 2026-09-30），是 2024 年整个国会周期
  （9,240 万美元）的两倍以上。但要注意 ACDC 的同口径警告：
  <b>Polymarket 上约 68%–70% 的国会交易额来自前 1% 的钱包</b>，
  因此这些价格未必是干净的共识读数。详见 6.5 节。{NEWS}</div>
</div>
"""


def section_market(M):
    return f"""
<h2 id="s2">第二章 · 市场是在什么状态下走进这场选举的</h2>
<p class="lede">同一个选举结果，在不同的估值与流动性起点上，市场含义完全不同。所以起点必须先说清楚。</p>

<div class="grid4">
  <div class="kpi"><div class="lab">标普 500</div><div class="val">{D.LAST_CLOSE:,.0f}</div>
    <div class="sub">{D.LAST_DATE} 收盘 · 距 10/6 纪录高点 {D.DD_FROM_ATH*100:+.2f}%</div></div>
  <div class="kpi"><div class="lab">2026 年内涨幅</div><div class="val up">{D.YTD_2026*100:+.1f}%</div>
    <div class="sub">自 2025-12-31 的 {D.Y2025_CLOSE:,.0f}</div></div>
  <div class="kpi"><div class="lab">滚动市盈率</div><div class="val">25.8×</div>
    <div class="sub">远期 12 个月约 19.1×</div></div>
  <div class="kpi"><div class="lab">席勒 CAPE</div><div class="val down">40.8</div>
    <div class="sub">155 年第二高，仅次于 2000 年</div></div>
</div>

<div class="grid4" style="margin-top:14px">
  <div class="kpi"><div class="lab">联邦基金利率</div><div class="val">3.75–4.00%</div>
    <div class="sub">9/16 加息 25bp，12–0 全票</div></div>
  <div class="kpi"><div class="lab">10 年期美债</div><div class="val">~5.1%</div>
    <div class="sub">10/5 触及 5.31%，2002 年来最高</div></div>
  <div class="kpi"><div class="lab">股权风险溢价</div><div class="val down">≈ 0</div>
    <div class="sub">2002 年以来首次归零</div></div>
  <div class="kpi"><div class="lab">布伦特原油</div><div class="val">~$105</div>
    <div class="sub">9 月中曾达 $131</div></div>
</div>

<div class="call bad">
<div class="t">最重要的一点：这次选举不是 2018 年的重演</div>
2018 年中期选举时，市场刚从第四季度急跌中走出，估值被压缩，美联储还在加息路径的末端。
2026 年的起点完全不同：<b>标普在选举前一个月刚创下历史新高，而股权风险溢价恰好归零</b>——
这意味着股票相对债券没有任何估值补偿。历史上这个指标上一次归零是 2002 年。
在一个没有风险补偿的起点上，任何一类尾部风险的定价都不充分。{NEWS}
</div>

<h3>2.1 当前真正在驱动盘面的，不是选举</h3>
<p>美国银行 10 月全球基金经理调查（10 月 2–8 日执行，10 月 13 日发布，样本约 161–185 位经理、
管理规模约 4,500–5,120 亿美元）给出的尾部风险排序，可以作为市场注意力的直接读数：{AN}</p>

<div class="card">
<table>
<thead><tr><th>排序</th><th>尾部风险</th><th class="num">受访占比</th><th>与本次选举的关系</th></tr></thead>
<tbody>
<tr class="hi"><td>1</td><td>债券收益率无序上行</td><td class="num">约 31%</td>
  <td>选举只能间接影响（财政赤字路径）</td></tr>
<tr><td>2</td><td>AI 泡沫破裂</td><td class="num">约 23%</td><td><b>与选举无关</b></td></tr>
<tr><td>3</td><td>通胀重燃</td><td class="num">约 20%</td><td>主要来自伊朗战争能源冲击</td></tr>
<tr><td>4</td><td>超大规模云厂商引发信用事件</td><td class="num">约 11%</td><td><b>与选举无关</b></td></tr>
</tbody>
</table>
</div>

<p>值得注意的是，调查中基金经理表示<b>在 10 年期收益率达到约 5.9% 之前不会从股票轮换到债券</b>——
而当前是 5.1%。最拥挤的交易是做多全球半导体（45%）和做空美债（27%）；
科技板块净超配 +37%，为 2020 年 8 月以来最高；可选消费净低配 −34%，为 2008 年 7 月以来最悲观。{AN}</p>

<div class="call">
<div class="t">这对选举推演意味着什么</div>
拥挤的科技多头 + 极度悲观的消费空头 + 归零的风险溢价，共同构成一个特征：
<b>市场对「坏消息」的敏感度高于对「好消息」的敏感度</b>。
在这种结构下，同一份选举结果，负面解读的传导速度会快于正面解读。
本报告第七章的情景影响评估已经内生地反映了这一非对称性。
</div>
"""


def section_history(M):
    return f"""
<h2 id="s3">第三章 · 历史基准率，以及它为什么现在不可靠</h2>
<p class="lede">关于中期选举与股市，流传最广的一句话是「选举后一年必涨」。这句话有数据支撑，
但支撑它的数据主要来自 2000 年以前。本章把这条规律拆开检验。</p>

<h3>3.1 原始规律：看起来无懈可击</h3>
<p>以选举年 10 月到次年 10 月为窗口，1950–2022 年的 19 次中期选举中，
标普 500 的 12 个月回报<b>全部为正</b>，均值 +18.2%，中位数 +18.0%，最低 +3.0%。{EST}</p>
"""


def fig_hist_bars(M):
    rows = [(y, D.fwd12(y) * 100) for y in D.MIDTERM_YEARS]
    svg = C.midterm_bars(rows, mean=D.POST12_MEAN)
    return f"""
<div class="fig">
  <div class="ft">图 2 · 中期选举后 12 个月标普 500 回报（1950–2022，共 19 次）</div>
  <div class="fs">窗口为选举年 10 月月均 → 次年 10 月月均。19 次全部为正，均值 +18.2%，最差 +3.0%</div>
  {svg}
  <div class="note">数据来源：multpl 标普 500 月度序列（经交叉验证为<b>月平均值</b>），本报告计算。{EST}
  这张图是「中期选举后必涨」这一说法的原始证据。下一张图说明它为什么不能直接用。</div>
</div>
"""


def fig_era_debunk(M):
    groups = []
    for lab, rows in D.ERA_EXCESS:
        vals = [v for _, v in rows]
        col = C.ACCENT if sum(vals) / len(vals) > 0 else C.ACCENT4
        groups.append((lab, vals, col, f"n={len(vals)} · {sum(1 for v in vals if v>0)}/{len(vals)} 跑赢邻年"))
    svg = C.dot_strip(groups, lo=-25, hi=45, ref=0, pad=(196, 150, 46, 22))
    return f"""
<div class="fig">
  <div class="ft">图 3 · 中期选举年的「超额回报」：扣掉相邻周期年份之后</div>
  <div class="fs">纵轴 = 中期选举年 12 个月回报 − 相邻两个周期年份 12 个月回报的均值，单位为百分点。每一个点是一个选举周期</div>
  {svg}
  <div class="legend">
    <span><i style="background:{C.ACCENT}"></i>均值跑赢相邻年份</span>
    <span><i style="background:{C.ACCENT4}"></i>均值跑输相邻年份</span>
  </div>
  <div class="note">方法与含义：股票长期是上涨的，所以「选举后一年上涨」本身不构成任何证据。
  必须扣掉同期其他年份的涨幅。扣完之后：1950–1986 年平均超额 +14.1pp（10 次中 9 次跑赢），
  1990–2006 年 +22.9pp（5 次全部跑赢），而 <b>2010–2022 年变成 −4.1pp（4 次中只有 1 次跑赢）</b>。{EST}
  <br>结论：这条规律在最近四个周期已经失效。它可能是被数据挖掘出来的历史巧合，
  也可能曾经真实存在但已被市场学习套利掉。无论哪种解释，都不应该拿它作为 2026 年的交易依据。</div>
</div>
"""


def fig_2026_path(M):
    # Each curve is CUT AT ITS OWN ELECTION DAY. Running 2018 and 2022 through to
    # Dec 31 while 2026 stops in October compares a full year against ten months
    # and reverses the picture for 2022 (it closed the year at -20.0% but stood at
    # -20.2% on election day, whereas October alone was -23.6%).
    series = []
    # green/blue/grey, not green/orange/grey: the validated set separates under
    # protanopia at ΔE 12.2, where green↔orange only manages 6.8 (warn band).
    for y, col, nm in (('2026', C.ACCENT, '2026 年'), ('2018', C.GREY, '2018 年'),
                       ('2022', C.ACCENT3, '2022 年')):
        pts = [(d, v) for d, v in D.PATHS[y] if d <= D.ELECTION_DAY[y]]
        series.append({'name': nm, 'pts': pts, 'color': col})
    svg = C.line_chart(series, h=400, yfmt=lambda v: f'{v:.0f}', ylab='指数（各年首个交易日 = 100）',
                       vlines=[('2026-11-03', '选举日', C.INK2)], dots_last=True)
    return f"""
<div class="fig">
  <div class="ft">图 4 · 2026 年与最近两次中期选举年的路径对比（归一化，1 月首个交易日 = 100）</div>
  <div class="fs">进入选举日当天的累计涨幅：2026 年 {D.ENTER_PCT['2026']:+.1f}%、2018 年 {D.ENTER_PCT['2018']:+.1f}%、2022 年 {D.ENTER_PCT['2022']:+.1f}%。这是完全不同的一种起点</div>
  {svg}
  <div class="legend">
    <span><i style="background:{C.ACCENT}"></i>2026 年</span>
    <span><i style="background:{C.GREY}"></i>2018 年</span>
    <span><i style="background:{C.ACCENT3}"></i>2022 年</span>
  </div>
  <div class="note">数据来源：FRED SP500 日线，本报告归一化计算。{EST}
  三条曲线都在<b>各自的选举日截止</b>（2018-11-06、2022-11-08、2026-11-03）；
  2026 年的数据实际只到 10 月 15 日，距其选举日还有 {D.DAYS_TO_ELECTION} 天——
  绿线右端到虚线之间空出的这一段<b>就是尚未走完的路</b>，本报告不对它做任何外推。
  <br>读法：2018 与 2022 两个中期选举年，市场都是在年内先跌、带着亏损进入 11 月；
  2026 年则是带着可观盈利、且在选举前一个月刚创历史新高进入。所以
  「历史上中期选举后一年都涨」这句统计描述，其样本中的绝大部分起点是<b>跌下来的市场</b>，
  而 2026 的起点是<b>涨上去的市场</b>。这一点在做类比时必须显式扣掉。</div>
</div>
"""
