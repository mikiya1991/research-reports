# -*- coding: utf-8 -*-
"""Assemble the self-contained HTML report, then verify it."""

import io, re, sys
from html.parser import HTMLParser

import style
import data as D
import content1 as c1
import content2 as c2
import content3 as c3

VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link',
        'meta', 'param', 'source', 'track', 'wbr', 'path', 'rect', 'circle',
        'line', 'polyline', 'polygon', 'use', 'stop'}

TOC = [
    ("s0", "摘要", "核心判断"),
    ("s1", "第一章", "事实基础：选什么、什么时候、现在什么赔率"),
    ("s2", "第二章", "市场是在什么状态下走进这场选举的"),
    ("s3", "第三章", "历史基准率，以及它为什么现在不可靠"),
    ("s4", "第四章", "换个切法：按结果类型分组"),
    ("s5", "第五章", "情景推演：四种结果与概率"),
    ("s6", "第六章", "预测市场：它知道什么，不知道什么"),
    ("s7", "第七章", "传导渠道与板块影响"),
    ("s8", "第八章", "选情的基本面：选民在投什么"),
    ("s9", "第九章", "比选举更重要的事"),
    ("s10", "第十章", "操作含义与政策日历"),
    ("s11", "第十一章", "证据分级、已剔除项与已知错误"),
]


def build():
    M = {}
    body = []
    # -- 第一章：事实 --------------------------------------------------------
    body.append(c1.section_summary(M))
    body.append(c1.section_facts(M))
    body.append(c1.fig_odds(M))
    # -- 第二、三章：起点与历史基准率 ---------------------------------------
    body.append(c1.section_market(M))
    body.append(c1.section_history(M))
    body.append(c1.fig_hist_bars(M))
    body.append(c1.fig_era_debunk(M))
    body.append(c1.fig_2026_path(M))
    # -- 第四章：结果类型 ---------------------------------------------------
    body.append(c2.section_typology(M))
    body.append(c2.fig_outcome_types(M))
    body.append(c2.fig_drawdown(M))
    # -- 第五章：情景推演 ---------------------------------------------------
    body.append(c2.section_scenarios(M))
    body.append(c2.fig_scenario_grid(M))
    body.append(c2.section_transmission(M))
    body.append(c2.section_polling(M))
    body.append(c2.fig_poll_error(M))
    body.append(c2.section_polling2(M))
    body.append(c2.section_structural(M))
    # -- 第六章：预测市场 ---------------------------------------------------
    body.append(c2.section_predmkt(M))     # 6.1 市场现在说什么
    body.append(c2.section_odyssey(M))     # 6.2 价格是怎么走到这里的
    body.append(c2.fig_odds_path(M))       # 图 9
    body.append(c2.section_predmkt2(M))    # 6.3 六个来源六个数字（引用图 1）
    body.append(c2.section_senate(M))      # 6.4 62% 由哪些席位构成
    body.append(c2.fig_race_map(M))        # 图 10
    body.append(c2.section_predmkt3(M))    # 6.5 谁在定价
    body.append(c2.section_predmkt4(M))    # 6.6 历史成绩单
    body.append(c2.section_predmkt5(M))    # 6.7 为什么它不是民调的独立证据
    body.append(c2.fig_threshold(M))       # 图 11
    body.append(c2.section_predmkt6(M))    # 6.8 本章结论
    # -- 第七章：传导与板块 -------------------------------------------------
    body.append(c2.section_sectors(M))
    body.append(c2.fig_impact_matrix(M))
    # -- 第八、九章：选情基本面与真正的主导变量 -----------------------------
    body.append(c3.section_issues(M))
    body.append(c3.section_bigger(M))
    body.append(c3.fig_2026_months(M))
    body.append(c3.section_bigger2(M))
    # -- 第十章：操作含义与日历 ---------------------------------------------
    body.append(c3.section_play(M))
    body.append(c3.fig_seasonal(M))
    body.append(c3.fig_calendar(M))
    # -- 第十一章：证据 -----------------------------------------------------
    body.append(c3.section_evidence(M))
    content = "\n".join(body)

    toc = "\n".join(f"<a href='#{i}'><span class='n'>{n}</span>{t}</a>" for i, n, t in TOC)

    doc = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>2026 美国中期选举 · 情景推演与股市影响</title>
<style>{style.CSS}</style>
</head>
<body>
<header class="hero"><div class="wrap">
  <div class="kicker">Scenario Analysis · 独立研究</div>
  <h1>2026 美国中期选举：情景推演与股市影响</h1>
  <p class="sub">选举日是 11 月 3 日。这份报告回答三个问题：可能的结果有哪些、各自概率多少、
  对市场意味着什么——以及为什么这次选举可能不是当前最重要的变量。</p>
  <div class="hero-meta">
    <span class="chip">报告日期 <b>{D.REPORT_DATE}</b></span>
    <span class="chip">数据截止 <b>2026-10-15 收盘</b></span>
    <span class="chip">选举日 <b>2026-11-03</b></span>
    <span class="chip">距今 <b>{D.DAYS_TO_ELECTION} 天</b></span>
    <span class="chip">标普 500 <b>{D.LAST_CLOSE:,.2f}</b></span>
    <span class="chip">全部图表 <b>内嵌 SVG</b></span>
  </div>
</div></header>

<div class="wrap">
<div class="toc">{toc}</div>
{content}

<div class="disclaimer">
<b>免责声明与阅读约定。</b>本报告为独立研究文档，不构成任何证券的买卖建议，也不构成投资顾问服务。
报告中的所有情景概率、板块评分与历史统计均为本报告作者的推算，已在正文中标为「估算」；
来自民调、媒体报道与机构研究的数据已逐条标注机构与时间窗口，可回到原始出处复核。
本报告作者不持有文中提及证券的头寸，与文中提及的任何机构无业务关系。
投资涉及本金损失风险，历史数据与情景推演均不代表未来结果。
</div>

<div class="foot">
2026 美国中期选举情景推演 · {D.REPORT_DATE} · 全部图表为内嵌 SVG，由本报告数据直接生成，无外部依赖。<br>
一手数据：FRED（SP500 日线序列，本报告自行下载并计算全部行情指标）。<br>
历史数据：multpl 标普 500 月度序列（经交叉验证为<b>月平均值</b>，非月末收盘）。<br>
选举与民调数据：Pew Research Center、AP-NORC、Fox News、Economist/YouGov、Reuters/Ipsos、
Gallup、Quinnipiac、NBC News、KFF、CBS/YouGov、Decision Desk HQ、Silver Bulletin、
Sabato's Crystal Ball、Ballotpedia、Polymarket、Kalshi。<br>
本报告中未能一手核验或已主动剔除的事项，已在第十一章逐条列出。
</div>
</div>
</body>
</html>"""
    return doc


# ------------------------------------------------------------------ verification
class Check(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.errors = []
        self.classes = set()
        self.ids = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if 'class' in d:
            for cl in d['class'].split():
                self.classes.add(cl)
        if 'id' in d:
            self.ids.append(d['id'])
        if tag not in VOID:
            self.stack.append((tag, self.getpos()))

    def handle_startendtag(self, tag, attrs):
        d = dict(attrs)
        if 'class' in d:
            for cl in d['class'].split():
                self.classes.add(cl)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            self.errors.append(f"多余的结束标签 </{tag}> at {self.getpos()}")
            return
        top, pos = self.stack.pop()
        if top != tag:
            self.errors.append(f"标签不匹配: <{top}> (开于 {pos}) 被 </{tag}> 关闭 at {self.getpos()}")


def verify(doc):
    ok = True
    p = Check()
    p.feed(doc)
    if p.errors:
        ok = False
        print("!! 标签错误:")
        for e in p.errors[:20]:
            print("   ", e)
    if p.stack:
        ok = False
        print("!! 未闭合的标签:", [(t, pos) for t, pos in p.stack][:20])
    if not p.errors and not p.stack:
        print("✓ 标签平衡：通过（HTMLParser 解析，含 SVG 空元素处理）")

    nums = [int(x) for x in re.findall(r"图\s*(\d+)\s*·", doc)]
    if nums == list(range(1, len(nums) + 1)):
        print(f"✓ 图表编号连续：图 1 – 图 {len(nums)}，共 {len(nums)} 张")
    else:
        ok = False
        print("!! 图表编号不连续:", nums)

    n_svg = doc.count("<svg")
    n_cap = len(re.findall(r"""class=['"]ft['"]""", doc))
    if n_svg < n_cap:
        ok = False
        print(f"!! SVG 数量({n_svg}) 少于图表标题数({n_cap})")
    else:
        print(f"✓ 图表完整：{n_cap} 张图，共 {n_svg} 个 SVG")

    n_h2 = len(re.findall(r"<h2 ", doc))
    print(f"✓ 章节数（h2）：{n_h2}；目录条目：{len(TOC)}")
    for i, n, _ in TOC:
        if (f'id="{i}"' not in doc) and (f"id='{i}'" not in doc):
            ok = False
            print(f"!! 目录锚点缺失: {i}")

    defined = set(re.findall(r"\.([a-zA-Z][\w-]*)", style.CSS))
    used = {c for c in p.classes if c}
    missing = sorted(used - defined)
    if missing:
        ok = False
        print("!! 使用了未在 CSS 中定义的 class:", missing)
    else:
        print(f"✓ 样式覆盖：用到的 {len(used)} 个 class 全部在 CSS 中有定义")

    leak = re.findall(r"<(module|function|class|object) [^>]*>", doc)
    if leak:
        ok = False
        print("!! Python 对象被插值进 HTML:", leak[:5])
    else:
        print("✓ 无未替换的 Python 对象 repr")

    if re.search(r"https?://[^\"'\s>]+\.(css|js|png|jpg|svg|woff2?)", doc):
        ok = False
        print("!! 存在外部资源引用")
    else:
        print("✓ 自包含：无外部 CSS/JS/图片/字体引用")

    print(f"✓ 文档大小：{len(doc.encode('utf-8'))/1024:.0f} KB")
    badges = {b: len(re.findall(f'b-{b}', doc)) for b in
              ('ok', 'news', 'analyst', 'est', 'rumor')}
    print("✓ 证据徽章分布：", badges, "合计", sum(badges.values()))
    if not all(badges.values()):
        print("   (提示：有证据等级未被使用)")
    return ok


if __name__ == '__main__':
    d = build()
    out = 'us_midterm_2026_report.html'
    io.open(out, 'w', encoding='utf-8').write(d)
    print(f"已写入 {out}\n")
    sys.exit(0 if verify(d) else 1)
