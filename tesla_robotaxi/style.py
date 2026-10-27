# -*- coding: utf-8 -*-
"""CSS for the report — every class used in the document is defined here."""

CSS = """
:root{
  --ink:#12161c; --ink-soft:#3d4753; --muted:#77818f; --line:#e4e8ee; --line-soft:#eef1f5;
  --bg:#f7f8fa; --panel:#ffffff; --accent:#c8452d; --accent2:#1f6feb; --accent3:#0f9d58;
  --accent4:#b8860b; --accent5:#7b4fd6; --shadow:0 1px 2px rgba(18,22,28,.05),0 8px 24px rgba(18,22,28,.06);
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{
  margin:0; background:var(--bg); color:var(--ink);
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Helvetica Neue",Helvetica,Arial,
    "PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;
  font-size:15px; line-height:1.75; letter-spacing:.01em;
}
.wrap{max-width:1180px; margin:0 auto; padding:0 28px 96px}
header.hero{
  background:linear-gradient(160deg,#151a21 0%,#232c38 55%,#2f3a48 100%);
  color:#fff; padding:56px 0 44px; margin-bottom:34px;
}
header.hero .wrap{padding-bottom:0}
.kicker{font-size:12.5px; letter-spacing:.22em; text-transform:uppercase; color:#9fb0c4; font-weight:600}
h1{font-size:38px; line-height:1.22; margin:14px 0 10px; font-weight:700; letter-spacing:-.01em}
.subtitle{font-size:16.5px; color:#c3cddb; max-width:820px; margin:0 0 26px}
.meta-row{display:flex; flex-wrap:wrap; gap:10px 28px; font-size:13px; color:#a9b7c8; border-top:1px solid rgba(255,255,255,.14); padding-top:18px}
.meta-row b{color:#fff; font-weight:600}
h2{
  font-size:24px; margin:52px 0 6px; padding-bottom:12px; border-bottom:2px solid var(--ink);
  display:flex; align-items:baseline; gap:12px; font-weight:700; letter-spacing:-.01em;
}
h2 .num{font-size:13px; color:var(--accent); font-weight:700; letter-spacing:.12em}
h3{font-size:17.5px; margin:34px 0 8px; font-weight:650}
h4{font-size:15px; margin:22px 0 4px; font-weight:650; color:var(--ink-soft)}
p{margin:12px 0; color:var(--ink-soft)}
ul,ol{margin:12px 0 12px 4px; padding-left:22px; color:var(--ink-soft)}
li{margin:7px 0}
li::marker{color:var(--muted)}
strong{color:var(--ink); font-weight:650}
code{background:#eef1f5; padding:1.5px 6px; border-radius:4px; font-size:13px;
  font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
a{color:var(--accent2); text-decoration:none; border-bottom:1px solid rgba(31,111,235,.28)}
a:hover{border-bottom-color:var(--accent2)}

/* ---------- KPI grid ---------- */
.kpis{display:grid; grid-template-columns:repeat(auto-fit,minmax(196px,1fr)); gap:14px; margin:26px 0 8px}
.kpi{background:var(--panel); border:1px solid var(--line); border-radius:12px; padding:16px 18px; box-shadow:var(--shadow)}
.kpi .lab{font-size:12px; color:var(--muted); letter-spacing:.02em; margin-bottom:6px; min-height:32px}
.kpi .val{font-size:26px; font-weight:700; letter-spacing:-.02em; line-height:1.15}
.kpi .val small{font-size:13.5px; font-weight:600; color:var(--muted); margin-left:3px; letter-spacing:0}
.kpi .note{font-size:11.5px; color:var(--muted); margin-top:6px}
.up{color:var(--accent3)} .down{color:var(--accent)} .flat{color:var(--muted)}

/* ---------- callouts ---------- */
.callout{border-radius:12px; padding:16px 20px; margin:22px 0; border:1px solid var(--line);
  background:var(--panel); border-left:4px solid var(--accent2); box-shadow:var(--shadow)}
.callout .t{font-weight:700; font-size:14px; margin-bottom:6px; color:var(--ink)}
.callout p{margin:6px 0}
.callout.warn{border-left-color:var(--accent4); background:#fffdf6}
.callout.risk{border-left-color:var(--accent); background:#fff8f7}
.callout.ok{border-left-color:var(--accent3); background:#f6fdf9}
.callout.key{border-left-color:var(--accent5); background:#faf8ff}

/* ---------- figures ---------- */
figure{margin:30px 0 34px; background:var(--panel); border:1px solid var(--line);
  border-radius:14px; padding:20px 22px 12px; box-shadow:var(--shadow)}
figure .ftitle{font-size:15px; font-weight:700; margin:0 0 2px; color:var(--ink)}
figure .fsub{font-size:12.5px; color:var(--muted); margin:0 0 14px; line-height:1.6}
figure .fsrc{font-size:11.5px; color:var(--muted); margin:10px 0 4px; border-top:1px dashed var(--line);
  padding-top:9px; line-height:1.6}
figcaption{font-size:12.5px; color:var(--muted); margin-top:8px}
svg.chart{display:block; width:100%; height:auto; overflow:visible}

/* ---------- tables ---------- */
table{width:100%; border-collapse:collapse; margin:20px 0; font-size:13.5px; background:var(--panel);
  border:1px solid var(--line); border-radius:12px; overflow:hidden}
th{background:#f2f5f9; text-align:left; padding:11px 13px; font-weight:650; font-size:12.5px;
  color:var(--ink); border-bottom:1px solid var(--line); white-space:nowrap}
td{padding:10px 13px; border-bottom:1px solid var(--line-soft); color:var(--ink-soft); vertical-align:top}
tr:last-child td{border-bottom:none}
tbody tr:hover{background:#fafbfd}
td.num,th.num{text-align:right; font-variant-numeric:tabular-nums}
td.pos{color:var(--accent3); font-weight:600} td.neg{color:var(--accent); font-weight:600}
.tbl-note{font-size:11.5px; color:var(--muted); margin:-12px 0 22px; line-height:1.6}

/* ---------- evidence badges ---------- */
.badge{display:inline-block; font-size:10.5px; font-weight:700; letter-spacing:.05em; padding:1.5px 7px;
  border-radius:5px; vertical-align:1.5px; margin-left:5px; white-space:nowrap; line-height:1.6}
.b-a{background:#e6f4ea; color:#0b6b3a; border:1px solid #bfe3cb}
.b-b{background:#e8f0fe; color:#1653b8; border:1px solid #c6dafb}
.b-c{background:#fff4e0; color:#8a5a00; border:1px solid #f3ddb0}
.b-d{background:#f2f4f7; color:#5b6472; border:1px solid #dfe3ea}
.b-x{background:#fdeceb; color:#a3261a; border:1px solid #f6c9c4}

/* ---------- rating block ---------- */
.rating{display:grid; grid-template-columns:repeat(auto-fit,minmax(230px,1fr)); gap:16px; margin:26px 0}
.rating .box{background:var(--panel); border:1px solid var(--line); border-radius:12px; padding:18px;
  box-shadow:var(--shadow)}
.rating .box .h{font-size:12px; color:var(--muted); letter-spacing:.04em; text-transform:uppercase; font-weight:650}
.rating .box .big{font-size:30px; font-weight:700; margin:6px 0 2px; letter-spacing:-.02em}

/* ---------- misc ---------- */
.two-col{display:grid; grid-template-columns:1fr 1fr; gap:26px}
@media (max-width:820px){.two-col{grid-template-columns:1fr}}
.toc{background:var(--panel); border:1px solid var(--line); border-radius:12px; padding:18px 22px;
  box-shadow:var(--shadow); columns:2; column-gap:34px; font-size:13.5px; margin:26px 0}
@media (max-width:820px){.toc{columns:1}}
.toc a{display:block; padding:4px 0; border:none; color:var(--ink-soft)}
.toc a:hover{color:var(--accent2)}
.toc .n{color:var(--muted); font-variant-numeric:tabular-nums; display:inline-block; width:26px}
hr{border:none; border-top:1px solid var(--line); margin:40px 0}
.tagrow{display:flex; flex-wrap:wrap; gap:8px; margin:14px 0}
.tag{font-size:12px; padding:3px 10px; border-radius:20px; background:#eef1f5; color:var(--ink-soft); border:1px solid var(--line)}
.tag.r{background:#fdeceb; color:#a3261a; border-color:#f6c9c4}
.tag.g{background:#e6f4ea; color:#0b6b3a; border-color:#bfe3cb}
.tag.a{background:#fff4e0; color:#8a5a00; border-color:#f3ddb0}
.footer{margin-top:60px; padding-top:22px; border-top:1px solid var(--line); font-size:12px; color:var(--muted); line-height:1.8}
.disclaimer{background:#f2f5f9; border:1px solid var(--line); border-radius:12px; padding:16px 20px;
  font-size:12.5px; color:var(--ink-soft); margin:30px 0}
.scroll{overflow-x:auto}
"""
