# -*- coding: utf-8 -*-
"""Assemble the self-contained HTML report, then verify it."""

import io, re, sys
from html.parser import HTMLParser

import style
import content1 as c1
import content2 as c2
import content3 as c3

VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link',
        'meta', 'param', 'source', 'track', 'wbr', 'path', 'rect', 'circle',
        'line', 'polyline', 'polygon', 'use', 'stop'}

TOC = [
    ("s0", "摘要", "核心判断"),
    ("s1", "第一章", "投资判断与情景框架"),
    ("s2", "第二章", "技术底座：Tesla 到底在造什么"),
    ("s3", "第三章", "运营现状：7 个都市圈，两种法律结构"),
    ("s4", "第四章", "监管与安全：真正的约束条件"),
    ("s5", "第五章", "单位经济学：一个必须承认无知的模型"),
    ("s6", "第六章", "财务现实：利润率 1.4% 的公司"),
    ("s7", "第七章", "竞争格局：Tesla 是挑战者"),
    ("s8", "第八章", "催化剂与时间表"),
    ("s9", "第九章", "估值：市场为未发生的事付了多少钱"),
    ("s10", "第十章", "风险清单"),
    ("s11", "第十一章", "证据分级、已剔除项与已知错误"),
]


def build():
    M = {}
    body = []
    body.append(c1.section_summary(M))
    body.append(c1.section_thesis(M))
    body.append(c1.section_tech(M))
    body.append(c1.section_ops(M))
    body.append(c1.section_reg(M))
    body.append(c2.section_unit(M))
    body.append(c2.fig_unit_waterfall(M))
    body.append(c2.fig_sens(M))
    body.append(c2.section_fin(M))
    body.append(c2.section_ops_metrics(M))
    body.append(c3.section_competition(M))
    body.append(c2.section_catalysts(M))
    body.append(c2.tbl_catalysts(M))
    body.append(c3.section_valuation(M))
    body.append(c3.section_risk(M))
    body.append(c3.section_evidence(M))
    content = "\n".join(body)

    toc = "\n".join(f"<a href='#{i}'><span class='n'>{n}</span>{t}</a>" for i, n, t in TOC)

    doc = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Tesla Robotaxi 投资研究报告 · 2026年10月</title>
<style>{style.CSS}</style>
</head>
<body>
<header class="hero"><div class="wrap">
  <div class="kicker">Investment Research · 独立研究</div>
  <h1>Tesla Robotaxi 投资研究报告</h1>
  <p class="subtitle">把「无人驾驶的未来」翻译成可以核对的数字：车队规模、监管状态、单位经济、
  现金流，以及市场当前为尚未发生的事付了多少钱。</p>
  <div class="meta-row">
    <span>发布日期 <b>2026-10-08</b></span>
    <span>数据截止 <b>2026-10-08</b></span>
    <span>标的 <b>TSLA · NASDAQ</b></span>
    <span>参考价 <b>${c3.MKT['price']:.2f}</b>（2026-10-07）</span>
    <span>市值 <b>1.49 万亿美元</b></span>
    <span>证据等级 <b>A / B / C / D / X</b> 逐条标注</span>
  </div>
</div></header>

<div class="wrap">
<div class="toc">{toc}</div>
{content}

<div class="disclaimer">
<b>免责声明与阅读约定。</b>本报告为独立研究文档，不构成任何证券的买卖建议，也不构成投资顾问服务。
报告中的所有估值、情景与参数均为本报告作者的假设与推算，已在正文中标为证据等级 C；
所有来自公司文件与政府名单的数据已标为等级 A 并可在原始出处复核。
本报告作者不持有文中提及证券的头寸，与文中提及的任何公司无业务关系。
投资涉及本金损失风险，历史数据与情景推演均不代表未来结果。
</div>

<div class="footer">
Tesla Robotaxi 投资研究报告 · 2026-10-08 · 全部图表为内嵌 SVG，由本报告数据直接生成，无外部依赖。<br>
一手来源：SEC EDGAR（Tesla CIK 0001318605）10-K / 10-Q / 8-K / DEF 14A；加州 DMV 自动驾驶许可名单；
德州机动车管理局商用授权公开记录（经 CNBC 2026-10-03 报道引用）。<br>
二手来源：CNBC、The Verge、TechCrunch、stockanalysis.com、Waymo 官方网站。<br>
本报告中凡未能一手核验的事项，已在第十一章 11.4 节逐条列出。
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

    figs = re.findall(r"图\s*(\d+)\s*·", doc)
    nums = [int(x) for x in figs]
    if nums == list(range(1, len(nums) + 1)):
        print(f"✓ 图表编号连续：图 1 – 图 {len(nums)}，共 {len(nums)} 张")
    else:
        ok = False
        print("!! 图表编号不连续:", nums)

    n_svg = doc.count("<svg")
    n_cap = len(re.findall(r"""class=['"]ftitle['"]""", doc))
    if n_svg < n_cap:
        ok = False
        print(f"!! SVG 数量({n_svg}) 少于图表标题数({n_cap})")
    else:
        print(f"✓ 图表完整：{n_cap} 张图，共 {n_svg} 个 SVG"
              f"（{n_svg-n_cap} 张为双面板图）")

    n_h2 = len(re.findall(r"<h2 ", doc))
    print(f"✓ 章节数（h2）：{n_h2}；目录条目：{len(TOC)}")
    for i, n, _ in TOC:
        if (f'id="{i}"' not in doc) and (f"id='{i}'" not in doc):
            ok = False
            print(f"!! 目录锚点缺失: {i}")

    css = style.CSS
    defined = set(re.findall(r"\.([a-zA-Z][\w-]*)", css))
    used = {c for c in p.classes if c}
    missing = sorted(used - defined)
    if missing:
        ok = False
        print("!! 使用了未在 CSS 中定义的 class:", missing)
    else:
        print(f"✓ 样式覆盖：用到的 {len(used)} 个 class 全部在 CSS 中有定义")

    leak = re.findall(r"<(module|function|class) [^>]*>", doc)
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
    badges = {b: len(re.findall(f'badge b-{b}', doc)) for b in 'abcdx'}
    print("✓ 证据徽章分布：", badges, "合计", sum(badges.values()))
    return ok


if __name__ == '__main__':
    d = build()
    out = 'tesla_robotaxi_report.html'
    io.open(out, 'w', encoding='utf-8').write(d)
    print(f"已写入 {out}\n")
    sys.exit(0 if verify(d) else 1)
