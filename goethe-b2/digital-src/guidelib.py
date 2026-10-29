"""Goethe B2 가이드 페이지(schreiben-guide.html, sprechen-guide.html)가 함께 쓰는 헬퍼와 기본 CSS."""
import html
import os
import re
import subprocess
import sys

ARROW = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
BACK = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 12H5M11 6l-6 6 6 6"/></svg>'
NUMS = "❶❷❸❹❺❻❼❽❾❿"
HANGUL = re.compile("[\uac00-\ud7a3]")


def e(s):
    return html.escape(s, quote=True)


def words(s):
    return len(s.split())


def de(s):
    """독일어 조각에 lang 속성을 붙입니다."""
    return f'<span lang="de">{e(s)}</span>'


def table(head, rows, cls="", de_cols=()):
    """표. 좁은 화면에서는 열 이름을 앞에 붙여 한 줄씩 쌓습니다.

    de_cols="auto"이면 한글이 없는 칸을 독일어(lang="de")로 표시합니다."""
    out = [f'<div class="tw"><table class="tbl {cls}"><thead><tr>' + "".join(f"<th>{e(h)}</th>" for h in head) + "</tr></thead><tbody>"]
    for r in rows:
        tds = []
        for i, c in enumerate(r):
            is_de = (not HANGUL.search(c) and any(ch.isalpha() for ch in c)) if de_cols == "auto" else i in de_cols
            cell = de(c) if is_de else e(c)
            tds.append(f'<td data-label="{e(head[i])}">{cell}</td>')
        out.append("<tr>" + "".join(tds) + "</tr>")
    out.append("</tbody></table></div>")
    return "".join(out)


def section(sid, eyebrow, title, inner, lead=""):
    lead_html = f'<p class="slead">{lead}</p>' if lead else ""
    return (f'<section class="sec" id="{sid}" aria-labelledby="{sid}-h">'
            f'<p class="eyebrow">{e(eyebrow)}</p><h2 id="{sid}-h">{e(title)}</h2>{lead_html}{inner}</section>')



def page(skill, d, nav, secs, css_extra=""):
    """가이드 한 쪽의 HTML 틀(머리, 로고, 목차 칩, 본문, 출처, 바닥).

    skill   머리말에 쓰는 영역 이름(Schreiben, Sprechen)
    nav     [(섹션 id, 칩 글자), ...]
    secs    section()으로 만든 HTML 조각의 목록
    """
    chips = "".join(f'<a href="#{i}">{e(t)}</a>' for i, t in nav)
    src = "".join(f'<li><a href="{e(u)}" target="_blank" rel="noopener">{e(t)}</a></li>' for t, u in d["sources"])
    return f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="color-scheme" content="light">
<meta name="robots" content="noindex,nofollow">
<title>Goethe B2 {skill} · {e(d["title"])} — Sophia Deutsch Akademie</title>
<link rel="icon" href="../assets/apple-touch-icon.png">
<link rel="stylesheet" href="../assets/pretendard.css">
<style>
{CSS}{css_extra}</style>
</head>
<body>
<main class="wrap">
  <div class="brand"><img src="../assets/logo.png" alt="Sophia Deutsch Akademie 로고" width="40"><b>Sophia Deutsch Akademie</b></div>
  <header class="hero">
    <p class="eyebrow">{e(d["eyebrow"])}</p>
    <h1>{e(d["title"])}</h1>
    <p class="lead">{e(d["lead"])}</p>
    <nav class="chips" aria-label="가이드 목차">{chips}</nav>
  </header>
  {"".join(secs)}
  <p class="closing" lang="de">{e(d["closing"])}</p>
  <aside class="src"><h2>{e(d["sources_title"])}</h2><ul>{src}</ul></aside>
  <footer class="foot"><a href="index.html#mode">{BACK} Goethe B2 모의고사</a><span>© 2026 Sophia Deutsch Akademie</span></footer>
</main>
</body>
</html>
'''


CSS = """:root{--navy:#2E3A55;--navy-2:#3B4863;--ivory:#FBF8F1;--mist:#F5F2E9;--line:#E4DFD3;--ochre:#B87830;--ochre-ink:#85571F;--red:#AA483C;--ink:#2E3A55;--ink-2:#4A5570;--ink-3:#626C80;--card:#FFFFFF;
--sans:"Pretendard Variable",Pretendard,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Apple SD Gothic Neo","Malgun Gothic","Noto Sans KR",sans-serif}
html[data-theme="dark"]{--card:#1B2028}
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth}
body{margin:0;background:var(--ivory);color:var(--ink);font-family:var(--sans);font-size:16px;line-height:1.7;word-break:keep-all;overflow-wrap:break-word;-webkit-font-smoothing:antialiased}
h1,h2,h3,p,ol,ul,dl,dd{margin:0}
ol,ul{padding:0;list-style:none}
a{color:inherit}
:focus-visible{outline:2px solid var(--ochre);outline-offset:3px;border-radius:4px}
.wrap{max-width:900px;margin:0 auto;padding:28px clamp(20px,5vw,40px) 40px}
.brand{display:flex;align-items:center;gap:14px}
.brand img{width:40px;height:auto;display:block}
.brand b{font-size:19px;font-weight:700;line-height:1.2}
@media (max-width:380px){.brand{gap:10px;max-width:calc(100% - 130px)}.brand img{width:34px}.brand b{font-size:15px}}
.eyebrow{font-size:13px;letter-spacing:.18em;text-transform:uppercase;color:var(--ochre-ink);font-weight:700}
.hero{padding:clamp(40px,8vh,72px) 0 8px}
h1{font-weight:800;font-size:clamp(34px,6.4vw,60px);line-height:1.12;letter-spacing:-.03em;margin:14px 0 0}
.lead{margin-top:18px;font-size:clamp(16px,2.3vw,18px);color:var(--ink-3);max-width:640px}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:28px}
.chips a{display:inline-block;text-decoration:none;font-size:13.5px;font-weight:600;color:var(--ink-2);background:var(--card);border:1px solid var(--line);border-radius:999px;padding:6px 14px;transition:border-color .15s,background-color .15s}
.chips a:hover{border-color:var(--navy);background:var(--mist)}
.sec{margin-top:clamp(48px,8vh,72px);scroll-margin-top:24px}
h2{font-weight:800;font-size:clamp(26px,4.4vw,38px);line-height:1.2;letter-spacing:-.02em;margin:8px 0 0;padding-bottom:10px;border-bottom:2px solid var(--navy)}
.slead{margin-top:12px;font-size:15.5px;color:var(--ink-3)}
.sub{font-size:19px;font-weight:800;letter-spacing:-.01em;margin:30px 0 10px}
.kv{margin-top:6px}
.kv>div{display:grid;grid-template-columns:104px minmax(0,1fr);column-gap:16px;padding:14px 2px;border-bottom:1px solid var(--line)}
.kv dt{font-weight:700;color:var(--ochre-ink)}
.kv dd{font-size:15.5px}
.tw{margin-top:14px;overflow-x:auto}
.tbl{width:100%;border-collapse:collapse;font-size:15px}
.tbl th{text-align:left;font-size:13px;font-weight:700;color:var(--ink-3);padding:9px 12px;border-bottom:1.5px solid var(--navy);white-space:nowrap}
.tbl td{padding:11px 12px;border-bottom:1px solid var(--line);vertical-align:top}
.tbl tbody tr:hover td{background:var(--mist)}
.tbl.crit td:first-child,.tbl.lvl td:first-child{font-weight:700}
.tbl.crit td:nth-child(2),.tbl.lvl td:nth-child(2){white-space:nowrap;font-weight:700;color:var(--ochre-ink)}
.tbl.lvl td:first-child{width:56px}
.tbl.mis td:first-child{color:var(--red)}
.tbl.mis td:nth-child(2){font-weight:600}
.tbl.phr td:first-child{font-weight:700;white-space:nowrap}
.tbl.phr td:nth-child(2){color:var(--ink-3);font-size:13.5px;white-space:nowrap}
.tbl.phr td:nth-child(3){color:var(--ink-3)}
.tbl.phr td:nth-child(4){font-weight:600}
.note{margin-top:12px;font-size:14px;color:var(--ink-3)}
.warn{margin-top:18px;padding:14px 18px;border-radius:12px;background:var(--card);border:1.5px solid var(--ochre);font-size:15px}
.warn b{display:block;font-size:13px;letter-spacing:.14em;color:var(--ochre-ink);margin-bottom:2px}
.bul{margin-top:2px}
.bul li{position:relative;padding:9px 0 9px 20px;border-bottom:1px solid var(--line);font-size:15.5px}
.bul li::before{content:"";position:absolute;left:3px;top:20px;width:6px;height:6px;border-radius:50%;background:var(--ochre)}
.num{margin-top:6px}
.num li{display:grid;grid-template-columns:40px minmax(0,1fr);column-gap:10px;align-items:baseline;padding:13px 2px;border-bottom:1px solid var(--line)}
.num .n{font-weight:800;color:var(--ochre-ink);font-size:17px}
.chk{margin-top:6px}
.chk li{display:grid;grid-template-columns:30px minmax(0,1fr);column-gap:10px;align-items:start;padding:12px 2px;border-bottom:1px solid var(--line)}
.chk .bx{width:20px;height:20px;margin-top:4px;border:2px solid var(--navy);border-radius:5px}
.chk b{display:inline-block;min-width:22px;color:var(--ochre-ink);font-weight:800}
.lts{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;margin-top:6px}
.lt{display:flex;flex-direction:column;background:var(--card);border:1px solid var(--line);border-radius:16px;padding:18px 20px 14px}
.lt-h{display:grid;grid-template-columns:34px minmax(0,1fr);column-gap:8px;align-items:start}
.lt-n{font-size:24px;line-height:1.2;color:var(--ochre-ink)}
.lt-h h3{font-size:17px;font-weight:800;line-height:1.35}
.lt-p{font-size:12.5px;color:var(--ink-3);line-height:1.5;margin-top:2px}
.lt-b{margin-top:14px;padding:12px 14px;background:var(--mist);border-radius:10px;font-size:14.5px;line-height:1.65;word-break:normal;flex:1}
.lt-b p{margin:0}
.lt-t{margin:8px 0 !important}
.lt-g{margin-top:8px}
.lt-c{margin-top:12px;font-size:13px;color:var(--ink-3);display:flex;align-items:baseline;gap:6px;flex-wrap:wrap}
.lt-c b{font-size:16px;color:var(--navy);font-weight:800}
.lt-c span{font-size:12px}
.closing{margin-top:clamp(48px,8vh,72px);font-size:clamp(18px,3vw,22px);font-weight:700;color:var(--ink-2);text-align:center;line-height:1.6;word-break:normal}
.src{margin-top:40px;padding-top:18px;border-top:1px solid var(--line)}
.src h2{font-size:14px;letter-spacing:.14em;border:0;padding:0;margin:0 0 6px;color:var(--ink-3);font-weight:700}
.src li{padding:3px 0;font-size:13px;color:var(--ink-3);word-break:normal}
.src a{text-decoration:underline;text-underline-offset:3px}
.src a:hover{color:var(--ink)}
.foot{display:flex;justify-content:space-between;align-items:center;gap:16px;flex-wrap:wrap;margin-top:36px;font-size:12.5px;color:var(--ink-3)}
.foot a{display:inline-flex;align-items:center;gap:6px;text-decoration:none;font-weight:600;color:var(--ink-2);font-size:13.5px}
.foot a:hover{color:var(--ink);text-decoration:underline}
html[data-theme="dark"] .tbl tbody tr:hover td{background:#222831}
@media (max-width:760px){.lts{grid-template-columns:1fr}}
@media (max-width:640px){
  .kv>div{grid-template-columns:1fr;row-gap:2px}
  .tw{overflow:visible}
  .tbl,.tbl thead,.tbl tbody,.tbl tr,.tbl td{display:block;width:100%}
  .tbl thead{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
  .tbl tr{padding:12px 2px;border-bottom:1px solid var(--line)}
  .tbl td{border:0;padding:2px 10px;white-space:normal !important}
  .tbl td::before{content:attr(data-label);display:block;font-size:11.5px;font-weight:700;letter-spacing:.06em;color:var(--ink-3)}
  .tbl td:first-child::before{display:none}
  .tbl.lvl tr{display:grid;grid-template-columns:auto auto minmax(0,1fr);column-gap:10px;align-items:baseline}
  .tbl.lvl td{padding:2px 0}
  .tbl.lvl td::before{display:none}
  .tbl.lvl td:first-child{width:auto}
  .tbl tbody tr:hover td{background:none}
}
@media (max-width:560px){.wrap{padding:22px 20px 32px}.brand{padding-right:96px}}
@media print{.chips,.foot a{display:none}.sec{break-inside:avoid-page}.lt{break-inside:avoid}body{background:#fff}}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
"""


def finish(out, app):
    """파일을 쓴 뒤 다크 모드 스위치와 목차 버튼을 넣습니다."""
    theme = os.path.join(app, "..", "tools", "soda-theme.py")
    if os.path.exists(theme):
        subprocess.run([sys.executable, theme, out, "--kind", "index"], check=True)
