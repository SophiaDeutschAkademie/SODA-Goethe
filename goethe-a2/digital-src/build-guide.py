#!/usr/bin/env python3
"""Goethe A2 쓰기 시험 대비 가이드(schreiben-guide.html)를 만듭니다.

입력  guide-data.json   가이드의 모든 글과 모범 답안
출력  ../schreiben-guide.html (이 앱 폴더)

모범 답안의 단어 수는 이 스크립트가 직접 세고, 범위를 벗어나면 멈춥니다.
  Teil 1  20~30단어, Teil 2  30~40단어 (Anrede + 본문 + Gruß + 이름을 모두 센 값)
글꼴은 저장소 루트의 assets/pretendard.css를 씁니다(../../assets/ 가 아니라 앱 폴더 기준 ../assets/).
파일을 쓴 뒤 ../../tools/soda-theme.py 로 다크 모드 스위치를 넣습니다.

사용법 (앱 폴더에서)
  python3 digital-src/build-guide.py
"""
import html
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(HERE)
OUT = os.path.join(APP, "schreiben-guide.html")

ARROW = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
BACK = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 12H5M11 6l-6 6 6 6"/></svg>'
NUMS = "❶❷❸❹❺❻❼❽❾❿"


def e(s):
    return html.escape(s, quote=True)


def words(s):
    return len(s.split())


def de(s):
    """독일어 조각에 lang 속성을 붙입니다."""
    return f'<span lang="de">{e(s)}</span>'


def table(head, rows, cls="", de_cols=()):
    """표. 좁은 화면에서는 열 이름을 앞에 붙여 한 줄씩 쌓습니다."""
    out = [f'<div class="tw"><table class="tbl {cls}"><thead><tr>' + "".join(f"<th>{e(h)}</th>" for h in head) + "</tr></thead><tbody>"]
    for r in rows:
        tds = []
        for i, c in enumerate(r):
            cell = de(c) if i in de_cols else e(c)
            tds.append(f'<td data-label="{e(head[i])}">{cell}</td>')
        out.append("<tr>" + "".join(tds) + "</tr>")
    out.append("</tbody></table></div>")
    return "".join(out)


def section(sid, eyebrow, title, inner, lead=""):
    lead_html = f'<p class="slead">{lead}</p>' if lead else ""
    return (f'<section class="sec" id="{sid}" aria-labelledby="{sid}-h">'
            f'<p class="eyebrow">{e(eyebrow)}</p><h2 id="{sid}-h">{e(title)}</h2>{lead_html}{inner}</section>')


def letters(part):
    lo, hi = part["range"]
    cards = []
    for i, a in enumerate(part["answers"]):
        body_n = words(a["body"])
        total = words(a["anrede"]) + body_n + words(a["gruss"])
        if not (lo <= total <= hi):
            sys.exit(f'{part["no"]} 모범 답안 {i + 1} "{a["title"]}": 전체 {total}단어, 범위 {lo}~{hi}를 벗어났습니다')
        if body_n * 2 < lo:  # 본문만 세어도 요구량의 절반 이상이어야 합니다
            sys.exit(f'{part["no"]} 모범 답안 {i + 1} "{a["title"]}": 본문 {body_n}단어, 요구량의 50% 미만입니다')
        gruss = "".join(f'<p lang="de">{e(l)}</p>' for l in a["gruss"].split("\n"))
        cards.append(
            f'<article class="lt"><header class="lt-h"><span class="lt-n" aria-hidden="true">{NUMS[i]}</span>'
            f'<div><h3>{e(a["title"])}</h3><p class="lt-p" lang="de">{e(a["points"])}</p></div></header>'
            f'<div class="lt-b"><p lang="de">{e(a["anrede"])}</p><p lang="de" class="lt-t">{e(a["body"])}</p>'
            f'<div class="lt-g">{gruss}</div></div>'
            f'<p class="lt-c"><b>{total}</b> Wörter <span>본문 {body_n} · 인사말·맺음말·이름 포함 {total}</span></p></article>')
    return f'<div class="lts">{"".join(cards)}</div>'


def build(d):
    ov, sc, st, dy, ck, mi, sg = (d[k] for k in ("overview", "scoring", "steps", "dayof", "checklist", "mistakes", "strategies"))
    t1, t2 = d["teil1"], d["teil2"]

    nav = [("uebersicht", "시험 구조"), ("bewertung", "채점"), ("schritte", "준비 5단계"), ("pruefungstag", "시험 당일"),
           ("checkliste", "체크리스트"), ("fehler", "실수"), ("strategie", "고득점"), ("teil1", "Teil 1 SMS"), ("teil2", "Teil 2 E-Mail")]
    chips = "".join(f'<a href="#{i}">{e(t)}</a>' for i, t in nav)

    secs = []
    secs.append(section(ov["id"], "Überblick", ov["title"],
                        '<dl class="kv">' + "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in ov["rows"]) + "</dl>"))

    inner = (table(["기준", "배점", "보는 것"], sc["criteria"], "crit") +
             f'<h3 class="sub">{e(sc["levels_title"])}</h3>' + table(["단계", "점수", "Leitpunkt 수행"], sc["levels"], "lvl") +
             f'<p class="note">{e(sc["levels_note"])}</p>'
             f'<p class="warn"><b>0점 규칙</b>{e(sc["zero"])}</p>'
             f'<h3 class="sub">{e(sc["rules_title"])}</h3><ul class="bul">' + "".join(f"<li>{e(r)}</li>" for r in sc["rules"]) + "</ul>")
    secs.append(section(sc["id"], "Bewertung", sc["title"], inner, e(sc["intro"])))

    secs.append(section(st["id"], "Vorbereitung", st["title"], '<ol class="num">' + "".join(
        f'<li><span class="n">{e(n)}</span><span>{e(t)}</span></li>' for n, t in st["rows"]) + "</ol>"))

    secs.append(section(dy["id"], "Prüfungstag", dy["title"], '<ol class="num circ">' + "".join(
        f'<li><span class="n">{"①②③④"[i]}</span><span>{e(t)}</span></li>' for i, t in enumerate(dy["items"])) + "</ol>"))

    secs.append(section(ck["id"], "Checkliste", ck["title"], '<ul class="chk">' + "".join(
        f'<li><span class="bx" aria-hidden="true"></span><span><b>{i + 1}</b>{e(t)}</span></li>' for i, t in enumerate(ck["items"])) + "</ul>"))

    secs.append(section(mi["id"], "Fehler", mi["title"], table(["✗ 실수", "✓ 올바른 표현", "설명"], mi["rows"], "mis", de_cols=(0, 1))))

    secs.append(section(sg["id"], "Strategie", sg["title"], '<ol class="num">' + "".join(
        f'<li><span class="n">{e(n)}</span><span>{e(t)}</span></li>' for n, t in sg["rows"]) + "</ol>"))

    for part in (t1, t2):
        inner = (f'<h3 class="sub">{e(part["phrases_title"])}</h3>' +
                 table(["기능", "문법", "기본", "고득점 문장"], part["phrases"], "phr", de_cols=(2, 3)) +
                 (f'<p class="note">{e(part["reasons"])}</p>' if part["reasons"] else "") +
                 f'<h3 class="sub">{e(part["answers_title"])}</h3>' + letters(part))
        secs.append(section(part["id"], part["no"], part["title"], inner, e(part["lead"])))

    src = "".join(f'<li><a href="{e(u)}" target="_blank" rel="noopener">{e(t)}</a></li>' for t, u in d["sources"])
    page = f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="color-scheme" content="light">
<meta name="robots" content="noindex,nofollow">
<title>Goethe A2 Schreiben · {e(d["title"])} — Sophia Deutsch Akademie</title>
<link rel="icon" href="../assets/apple-touch-icon.png">
<link rel="stylesheet" href="../assets/pretendard.css">
<style>
{CSS}</style>
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
  <footer class="foot"><a href="index.html#mode">{BACK} Goethe A2 모의고사</a><span>© 2026 Sophia Deutsch Akademie</span></footer>
</main>
</body>
</html>
'''
    return page


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


def main():
    d = json.load(open(os.path.join(HERE, "guide-data.json"), encoding="utf-8"))
    page = build(d)
    open(OUT, "w", encoding="utf-8").write(page)
    theme = os.path.join(APP, "..", "tools", "soda-theme.py")
    if os.path.exists(theme):
        subprocess.run([sys.executable, theme, OUT, "--kind", "index"], check=True)
    n1, n2 = len(d["teil1"]["answers"]), len(d["teil2"]["answers"])
    print(f"geschrieben: {OUT} ({os.path.getsize(OUT) / 1024:.0f} KB), 모범 답안 {n1}+{n2}편")


if __name__ == "__main__":
    main()
