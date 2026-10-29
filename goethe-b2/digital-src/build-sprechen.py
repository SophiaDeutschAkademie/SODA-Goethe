#!/usr/bin/env python3
"""Goethe B2 말하기 시험 대비 가이드(sprechen-guide.html)를 만듭니다.

입력  sprechen-data.json   가이드의 모든 글, 대화, 발표, 문답
출력  ../sprechen-guide.html (이 앱 폴더)

빌드할 때 Teil 1 모범 발표(5단 합계)의 단어 수가 words_range 안에 드는지 검사하고, 어긋나면 멈춥니다.
공통 헬퍼와 기본 CSS는 guidelib.py 에 있습니다(schreiben-guide.html과 공유).

사용법 (앱 폴더에서)
  python3 -I digital-src/build-sprechen.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)  # python3 -I 로 돌려도 guidelib를 찾도록
from guidelib import NUMS, e, finish, page, section, table, words  # noqa: E402

APP = os.path.dirname(HERE)
OUT = os.path.join(APP, "sprechen-guide.html")
A = "auto"


def trim(rows):
    """데이터의 3번째 열(기본 문장)은 B1 가이드에서 쓰지 않습니다."""
    return [[r[0], r[1], r[3]] for r in rows]


def trim(rows):
    return rows


def dialogs(part):
    out = []
    for i, d in enumerate(part["dialogs"]):
        head = (f'<header class="lt-h"><span class="lt-n" aria-hidden="true">{NUMS[i]}</span>'
                f'<div><h3 lang="de">{e(d["title"])}</h3><p class="lt-p">Diskussion · circa 5 Min.</p></div></header>')
        aufgabe = f'<p class="dg-t"><b>Aufgabe</b><span lang="de">{e(d["aufgabe"])}</span></p>'
        lines = []
        for ln in d["lines"]:
            who, txt = ln.split(": ", 1)
            lines.append(f'<p class="dl"><b aria-label="{who}">{who}</b><span lang="de">{e(txt)}</span></p>')
        out.append(f'<article class="dg">{head}{aufgabe}<div class="dg-b">{"".join(lines)}</div></article>')
    return f'<div class="dgs">{"".join(out)}</div>'


def talks(part):
    lo, hi = part["words_range"]
    labels = part["folien_labels"]
    cards = []
    for i, a in enumerate(part["answers"]):
        if len(a["folien"]) != 5:
            sys.exit(f'Teil 1 발표 {i + 1} "{a["title"]}": 5단이 아닙니다')
        n = sum(words(f) for f in a["folien"])
        if not (lo <= n <= hi):
            sys.exit(f'Teil 1 발표 {i + 1} "{a["title"]}": {n}단어, 범위 {lo}~{hi}를 벗어났습니다')
        fol = "".join(f'<p class="fo"><b>{e(lb)}</b><span lang="de">{e(f)}</span></p>' for lb, f in zip(labels, a["folien"]))
        qa = (f'<div class="qa"><p><span class="who">파트너 질문</span><span lang="de">{e(a["q"])}</span></p>'
              f'<p><span class="who">답변</span><span lang="de">{e(a["a"])}</span></p></div>')
        cards.append(
            f'<article class="lt"><header class="lt-h"><span class="lt-n" aria-hidden="true">{NUMS[i]}</span>'
            f'<div><h3 lang="de">{e(a["title"])}</h3><p class="lt-p" lang="de">„{e(a["thema"])}“</p></div></header>'
            f'<div class="lt-b">{fol}</div>{qa}'
            f'<p class="lt-c"><b>{n}</b> Wörter <span>축약본 · 실전 4분은 더 길게</span></p></article>')
    return f'<div class="lts">{"".join(cards)}</div>'


def build(d):
    secs = []

    ov = d["overview"]
    secs.append(section(ov["id"], "Überblick", ov["title"],
                        '<dl class="kv">' + "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in ov["rows"]) + "</dl>" +
                        f'<h3 class="sub">{e(ov["diff_title"])}</h3><p class="note">{e(ov["diff"])}</p>'
                        f'<h3 class="sub">{e(ov["ablauf_title"])}</h3>' +
                        table(["순서", "시간", "하는 일", "채점"], ov["ablauf"], "abl", A)))

    sc = d["scoring"]
    inner = (table(sc["head"], sc["criteria"], "crit3", A) +
             f'<h3 class="sub">{e(sc["rules_title"])}</h3><ul class="bul">' + "".join(f"<li>{e(r)}</li>" for r in sc["rules"]) + "</ul>")
    secs.append(section(sc["id"], "Bewertung", sc["title"], inner, e(sc["intro"])))

    st = d["steps"]
    secs.append(section(st["id"], "Vorbereitung", st["title"], '<ol class="num">' + "".join(
        f'<li><span class="n">{e(n)}</span><span>{e(t)}</span></li>' for n, t in st["rows"]) + "</ol>"))

    pl = d["plan"]
    secs.append(section(pl["id"], "Lernplan", pl["title"], table(["주차", "영역", "내용"], pl["rows"], "plan", A), e(pl["intro"])))

    tp = d["topics"]
    secs.append(section(tp["id"], "Themen", tp["title"], table(tp["head"], tp["rows"], "tp", A), e(tp["intro"])))

    dy = d["dayof"]
    secs.append(section(dy["id"], "Prüfungstag", dy["title"], '<ol class="num circ">' + "".join(
        f'<li><span class="n">{"①②③④"[i]}</span><span>{e(t)}</span></li>' for i, t in enumerate(dy["items"])) + "</ol>"))

    t1 = d["teil1"]
    inner = (f'<h3 class="sub">{e(t1["structure_title"])}</h3>' + table(t1["structure_head"], t1["structure"], "flow3", A) +
             f'<p class="dg-t"><b>Aufgabe</b><span lang="de">{e(t1["aufgabe_tpl"])}</span></p>'
             f'<h3 class="sub">{e(t1["phrases_title"])}</h3>' + table(["기능", "포인트", "고득점 문장"], t1["phrases"], "phr", A) +
             f'<h3 class="sub">{e(t1["answers_title"])}</h3><p class="note">{e(t1["answers_note"])}</p>' + talks(t1))
    secs.append(section(t1["id"], t1["no"], t1["title"], inner, e(t1["lead"])))

    t2 = d["teil2"]
    inner = (f'<h3 class="sub">{e(t2["phrases_title"])}</h3>' + table(["기능", "포인트", "고득점 표현"], t2["phrases"], "phr", A) +
             f'<h3 class="sub">{e(t2["dialogs_title"])}</h3><p class="note">{e(t2["dialogs_note"])}</p>' + dialogs(t2))
    secs.append(section(t2["id"], t2["no"], t2["title"], inner, e(t2["lead"])))

    g = d["grammar"]
    secs.append(section(g["id"], "Grammatik", g["title"], table(g["head"], g["rows"], "gr", A), e(g["intro"])))

    nav = [("uebersicht", "시험 구조"), ("bewertung", "채점"), ("vorbereitung", "준비 6단계"), ("plan", "4주 플랜"),
           ("themen", "주제"), ("pruefungstag", "시험 당일"), ("teil1", "Teil 1 발표"), ("teil2", "Teil 2 토론"), ("grammatik", "문법 16")]
    return page("Sprechen", d, nav, secs, CSS_EXTRA)


CSS_EXTRA = """.tbl.abl td:first-child,.tbl.plan td:first-child,.tbl.phr td:first-child,.tbl.flow td:first-child,.tbl.flow3 td:first-child,.tbl.crit3 td:first-child,.tbl.lv td:first-child,.tbl.tp td:first-child,.tbl.ptk td:first-child,.tbl.gr td:first-child{font-weight:700}
.tbl.abl td:nth-child(2),.tbl.plan td:first-child{white-space:nowrap}
.tbl.abl td:nth-child(2){color:var(--ochre-ink);font-weight:700}
.tbl.plan td:first-child{color:var(--ochre-ink);letter-spacing:.06em}
.tbl.plan td:nth-child(2){font-weight:700}
.tbl.crit3 td:nth-child(2){color:var(--ochre-ink);font-size:13.5px;font-weight:600}
.tbl.lv td:first-child{color:var(--ochre-ink);font-size:18px}
.qa{margin-top:12px;font-size:14px;line-height:1.6;word-break:normal}
.qa p{margin:0 0 4px;display:grid;grid-template-columns:78px minmax(0,1fr);column-gap:6px}
.qa .who{font-size:12px;font-weight:800;color:var(--ochre-ink);padding-top:2px}
.fo{margin:0 0 10px;font-size:14.5px;line-height:1.7;word-break:normal}
.fo:last-child{margin-bottom:0}
.fo b{display:block;margin-bottom:2px;font-size:11.5px;letter-spacing:.1em;color:var(--ochre-ink)}
.dgs{display:grid;gap:16px;margin-top:6px}
.dg{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:18px 20px 16px}
.dg-t{margin-top:12px;font-size:14px;line-height:1.6;color:var(--ink-2)}
.dg-t b{display:inline-block;margin-right:8px;font-size:11.5px;letter-spacing:.12em;color:var(--ochre-ink)}
.pts{display:flex;flex-wrap:wrap;gap:6px;margin-top:12px}
.pts li{font-size:13px;padding:3px 11px;border:1px solid var(--line);border-radius:999px;background:var(--mist)}
.dg-b{margin-top:12px;padding:12px 14px;background:var(--mist);border-radius:10px}
.dl{display:grid;grid-template-columns:26px minmax(0,1fr);column-gap:8px;margin:0 0 7px;font-size:14.5px;line-height:1.65;word-break:normal}
.dl:last-child{margin-bottom:0}
.dl b{width:22px;height:22px;margin-top:2px;border-radius:50%;background:var(--navy);color:var(--ivory);font-size:12px;line-height:22px;text-align:center}
@media print{.dg{break-inside:avoid}}
"""


def main():
    d = json.load(open(os.path.join(HERE, "sprechen-data.json"), encoding="utf-8"))
    html = build(d)
    open(OUT, "w", encoding="utf-8").write(html)
    finish(OUT, APP)
    t1 = d["teil1"]["answers"]
    counts = ", ".join(str(sum(words(f) for f in a["folien"])) for a in t1)
    print(f"geschrieben: {OUT} ({os.path.getsize(OUT) / 1024:.0f} KB), Teil 1 발표 {len(t1)}편({counts}단어), Teil 2 토론 {len(d['teil2']['dialogs'])}편")


if __name__ == "__main__":
    main()
