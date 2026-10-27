# -*- coding: utf-8 -*-
"""CSS for the US equity liquidity report. Keep in sync with classes used in content*.py."""

CSS = """
  :root{
    --ink:#101820; --ink2:#3A4750; --ink3:#697683; --line:#E2E7EC; --bg:#F6F8FA;
    --card:#FFFFFF; --accent:#0E7C66; --accent2:#B8860B; --ok:#0F9D58; --warn:#F4B400;
    --bad:#DB4437; --neu:#7B8794; --gold:#C08A2E;
  }
  *{box-sizing:border-box;}
  body{
    margin:0; background:var(--bg); color:var(--ink);
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;
    font-size:15px; line-height:1.75; -webkit-font-smoothing:antialiased;
  }
  .wrap{max-width:1180px;margin:0 auto;padding:0 24px 100px;}

  .hero{background:linear-gradient(135deg,#0A1F1B 0%,#0D3B33 55%,#0E7C66 100%);color:#fff;padding:56px 0 44px;margin-bottom:30px;}
  .hero .wrap{padding-bottom:0;}
  .hero .kicker{font-size:12.5px;letter-spacing:.22em;text-transform:uppercase;color:#8FD8C4;font-weight:600;margin-bottom:14px;}
  .hero h1{font-size:38px;line-height:1.25;margin:0 0 16px;font-weight:700;letter-spacing:-.01em;}
  .hero p.sub{font-size:16.5px;color:#C9E8DE;margin:0 0 26px;max-width:880px;}
  .hero-meta{display:flex;flex-wrap:wrap;gap:10px;}
  .chip{background:rgba(255,255,255,.10);border:1px solid rgba(255,255,255,.22);border-radius:999px;padding:6px 15px;font-size:13px;color:#E6F5F0;backdrop-filter:blur(4px);}
  .chip b{color:#fff;}

  .toc{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px 22px;margin:26px 0 8px;display:flex;flex-wrap:wrap;gap:8px 22px;font-size:13.5px;}
  .toc a{color:var(--ink2);text-decoration:none;border-bottom:1px dashed transparent;}
  .toc a:hover{color:var(--accent);border-bottom-color:var(--accent);}
  .toc .n{color:var(--ink3);margin-right:6px;font-variant-numeric:tabular-nums;}

  h2{font-size:24px;margin:56px 0 6px;padding-top:22px;font-weight:700;letter-spacing:-.01em;border-top:3px solid var(--ink);display:inline-block;}
  h2 + .lede{color:var(--ink3);font-size:14px;margin:0 0 26px;max-width:940px;}
  h3{font-size:18px;margin:36px 0 12px;font-weight:650;}
  h4{font-size:15.5px;margin:24px 0 8px;font-weight:650;color:var(--ink2);}
  p{margin:12px 0;}
  ul,ol{margin:12px 0;padding-left:22px;}
  li{margin:6px 0;}
  code{background:#EEF2F6;padding:1px 6px;border-radius:4px;font-size:13px;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;}
  .muted{color:var(--ink3);}
  .small{font-size:13.5px;}
  .quote{border-left:3px solid var(--accent);background:#F2F9F7;padding:9px 14px;font-style:italic;color:var(--ink2);border-radius:0 8px 8px 0;font-size:14.5px;}

  .card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:26px 28px;margin:22px 0;box-shadow:0 1px 2px rgba(16,24,40,.04),0 8px 24px -16px rgba(16,24,40,.14);}
  .grid2{display:grid;grid-template-columns:1fr 1fr;gap:20px;}
  .grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;}
  .grid4{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;}
  @media(max-width:900px){.grid2,.grid3,.grid4{grid-template-columns:1fr;}}

  .kpi{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px 18px;}
  .kpi .lab{font-size:12px;color:var(--ink3);letter-spacing:.04em;margin-bottom:6px;}
  .kpi .val{font-size:24px;font-weight:700;line-height:1.15;letter-spacing:-.02em;}
  .kpi .sub{font-size:12.5px;color:var(--ink3);margin-top:5px;}
  .up{color:var(--ok);} .down{color:var(--bad);} .flat{color:var(--neu);}

  table{width:100%;border-collapse:collapse;margin:18px 0;font-size:13.8px;}
  th{background:#EDF3F1;text-align:left;padding:11px 13px;font-weight:650;color:var(--ink2);border-bottom:2px solid #D6E2DE;white-space:nowrap;}
  td{padding:10px 13px;border-bottom:1px solid var(--line);vertical-align:top;}
  tr:last-child td{border-bottom:none;}
  tbody tr:hover{background:#FAFCFB;}
  .num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap;}
  tr.hi td{background:#F2F8F6;}

  .b{display:inline-block;padding:2px 9px;border-radius:999px;font-size:11.5px;font-weight:650;line-height:1.7;white-space:nowrap;}
  .b-ok{background:#E4F5EA;color:#0B7A45;}
  .b-news{background:#E7EEF8;color:#2F5FA8;}
  .b-analyst{background:#F3E8FB;color:#7A2FA8;}
  .b-rumor{background:#FEF3D7;color:#9A6C00;}
  .b-est{background:#EDEFF2;color:#5A6570;}

  .call{border-left:4px solid var(--accent);background:#F1F8F6;border-radius:0 10px 10px 0;padding:16px 20px;margin:20px 0;}
  .call.warn{border-color:var(--warn);background:#FFF9EA;}
  .call.bad{border-color:var(--bad);background:#FDF2F1;}
  .call.ok{border-color:var(--ok);background:#EFFAF3;}
  .call .t{font-weight:700;margin-bottom:6px;font-size:14.5px;}

  .fig{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:24px 26px 18px;margin:24px 0;}
  .fig .ft{font-size:15px;font-weight:700;margin-bottom:4px;}
  .fig .fs{font-size:12.5px;color:var(--ink3);margin-bottom:18px;}
  .fig svg{display:block;width:100%;height:auto;overflow:visible;}
  .note{font-size:12px;color:var(--ink3);margin-top:14px;padding-top:12px;border-top:1px dashed var(--line);}
  .legend{display:flex;flex-wrap:wrap;gap:16px;margin:14px 0 0;font-size:12.5px;color:var(--ink2);}
  .legend i{display:inline-block;width:11px;height:11px;border-radius:3px;margin-right:6px;vertical-align:-1px;}
  text{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;}

  .foot{margin-top:70px;padding-top:24px;border-top:1px solid var(--line);color:var(--ink3);font-size:12.5px;}
  .disclaimer{background:#FBFCFD;border:1px solid var(--line);border-radius:12px;padding:18px 22px;margin-top:40px;font-size:12.5px;color:var(--ink3);}
"""
