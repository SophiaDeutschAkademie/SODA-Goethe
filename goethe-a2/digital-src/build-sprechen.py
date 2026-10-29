#!/usr/bin/env python3
"""Goethe A2 말하기 시험 대비 가이드(sprechen-guide.html)를 만듭니다.

입력  sprechen-data.json   가이드의 모든 글, 이야기, 대화
출력  ../sprechen-guide.html (이 앱 폴더)

빌드할 때 이 스크립트가 직접 검사하고, 어긋나면 멈춥니다.
  Teil 2 모범 이야기  본문 단어 수가 words_range 안에 드는지
  Teil 3 유형 A 대화  합의한 시간대가 두 사람의 일정표 어느 항목과도 겹치지 않는지,
                      일정표 항목이 7~21시 안에서 서로 겹치지 않는지
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


def hm(h):
    """16.5 -> '16:30'"""
    return f"{int(h):02d}:{int(round((h - int(h)) * 60)):02d}"


def check_calendar(d):
    """유형 A 대화의 일정표와 합의 시간대를 검사합니다."""
    s0, s1 = d["slot"]
    where = f'대화 "{d["title"]}"'
    if s1 - s0 < 1:
        sys.exit(f"{where}: 합의 시간대가 1시간 미만입니다")
    for who in ("kal_a", "kal_b"):
        prev_end = 7
        for s, t, txt in d[who]:
            if not (7 <= s < t <= 21):
                sys.exit(f"{where}: {who} 항목 {txt} 의 시간 {s}~{t} 이(가) 7~21시를 벗어났습니다")
            if s < prev_end:
                sys.exit(f"{where}: {who} 항목 {txt} 이(가) 앞 항목과 겹칩니다")
            prev_end = t
            if s < s1 and t > s0:
                sys.exit(f"{where}: 합의 시간대 {s0}~{s1} 이(가) {who} 의 '{txt}'({s}~{t})와 겹칩니다")


def cal_box(label, entries):
    lis = "".join(f'<li><time>{hm(s)}–{hm(t)}</time><span lang="de">{e(txt)}</span></li>' for s, t, txt in entries)
    return f'<div><h4>{e(label)}</h4><ul>{lis}</ul></div>'


def dialogs(part):
    out = []
    for i, d in enumerate(part["dialogs"]):
        typ = d["typ"]
        if typ == "A":
            check_calendar(d)
            sub = "유형 A · 약속 정하기 (일정표)"
        else:
            sub = "유형 B · 함께 조직하기"
        head = (f'<header class="lt-h"><span class="lt-n" aria-hidden="true">{NUMS[i]}</span>'
                f'<div><h3 lang="de">{e(d["title"])}</h3><p class="lt-p">{sub}</p></div></header>')
        aufgabe = f'<p class="dg-t"><b>Aufgabe</b><span lang="de">{e(d["aufgabe"])}</span></p>'
        extra = ""
        if typ == "A":
            extra = ('<div class="cal">' + cal_box(f'A의 일정표 · {d["day"]}', d["kal_a"]) +
                     cal_box(f'B의 일정표 · {d["day"]}', d["kal_b"]) + "</div>" +
                     f'<p class="dg-r">두 사람이 함께 비는 시간 <span>{hm(d["slot"][0])}–{hm(d["slot"][1])}</span></p>')
        else:
            extra = '<ul class="pts" lang="de">' + "".join(f"<li>{e(p)}</li>" for p in d["points"]) + "</ul>"
        lines = []
        for ln in d["lines"]:
            who, txt = ln.split(": ", 1)
            lines.append(f'<p class="dl"><b aria-label="{who}">{who}</b><span lang="de">{e(txt)}</span></p>')
        out.append(f'<article class="dg">{head}{aufgabe}{extra}<div class="dg-b">{"".join(lines)}</div></article>')
    return f'<div class="dgs">{"".join(out)}</div>'


def stories(part):
    lo, hi = part["words_range"]
    cards = []
    for i, a in enumerate(part["answers"]):
        n = words(a["body"])
        if not (lo <= n <= hi):
            sys.exit(f'Teil 2 이야기 {i + 1} "{a["title"]}": 본문 {n}단어, 범위 {lo}~{hi}를 벗어났습니다')
        cards.append(
            f'<article class="lt"><header class="lt-h"><span class="lt-n" aria-hidden="true">{NUMS[i]}</span>'
            f'<div><h3 lang="de">{e(a["title"])}</h3><p class="lt-p" lang="de">{e(a["leit"])}</p></div></header>'
            f'<p class="kard"><b>KARTE · Stichwörter</b><span lang="de">{e(a["stich"])}</span></p>'
            f'<div class="lt-b"><p lang="de">{e(a["body"])}</p></div>'
            f'<div class="qa"><p><span class="who">시험관</span><span lang="de">{e(a["q"])}</span></p>'
            f'<p><span class="who">답변</span><span lang="de">{e(a["a"])}</span></p></div>'
            f'<p class="lt-c"><b>{n}</b> Wörter <span>본문 기준</span></p></article>')
    return f'<div class="lts">{"".join(cards)}</div>'


def build(d):
    secs = []
    A = "auto"

    ov, ab = d["overview"], d["overview"]
    secs.append(section(ov["id"], "Überblick", ov["title"],
                        '<dl class="kv">' + "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in ov["rows"]) + "</dl>" +
                        f'<h3 class="sub">{e(ov["ablauf_title"])}</h3>' +
                        table(["순서", "시간", "하는 일", "채점"], ov["ablauf"], "abl", A)))

    sc = d["scoring"]
    inner = (table(["기준", "세부 항목", "보는 것"], sc["criteria"], "crit3", A) +
             f'<p class="warn"><b>0점 규칙</b>{e(sc["zero"])}</p>'
             f'<h3 class="sub">{e(sc["rules_title"])}</h3><ul class="bul">' + "".join(f"<li>{e(r)}</li>" for r in sc["rules"]) + "</ul>")
    secs.append(section(sc["id"], "Bewertung", sc["title"], inner, e(sc["intro"])))

    st = d["steps"]
    secs.append(section(st["id"], "Vorbereitung", st["title"], '<ol class="num">' + "".join(
        f'<li><span class="n">{e(n)}</span><span>{e(t)}</span></li>' for n, t in st["rows"]) + "</ol>"))

    pl = d["plan"]
    secs.append(section(pl["id"], "Lernplan", pl["title"], table(["주차", "영역", "내용"], pl["rows"], "plan", A), e(pl["intro"])))

    dy = d["dayof"]
    secs.append(section(dy["id"], "Prüfungstag", dy["title"], '<ol class="num circ">' + "".join(
        f'<li><span class="n">{"①②③④"[i]}</span><span>{e(t)}</span></li>' for i, t in enumerate(dy["items"])) + "</ol>"))

    mi = d["mistakes"]
    secs.append(section(mi["id"], "Fehler", mi["title"], table(["✗ 실수", "✓ 올바른 표현", "설명"], mi["rows"], "mis", A)))

    wu = d["warmup"]
    secs.append(section(wu["id"], "Einstieg", wu["title"], table(["시험관 질문", "답변 예시"], wu["rows"], "wu", A), e(wu["intro"])))

    t1 = d["teil1"]
    inner = (f'<h3 class="sub">{e(t1["phrases_title"])}</h3>' + table(["기능", "문법", "기본 (통과)", "고득점 문장"], t1["phrases"], "phr", A) +
             f'<p class="note">{e(t1["note"])}</p>'
             f'<h3 class="sub">{e(t1["flow_title"])}</h3>' + table(["단계", "표현"], t1["flow"], "flow", A) +
             f'<h3 class="sub">{e(t1["keywords_title"])}</h3>' + table(["구분", "키워드"], t1["keywords"], "kw", A) +
             f'<h3 class="sub">{e(t1["qa_title"])}</h3><p class="note" lang="de">{e(t1["qa_aufgabe"])}</p>' +
             table(["카드", "질문 (A)", "답변 (B)"], t1["qa"], "qa3", A))
    secs.append(section(t1["id"], t1["no"], t1["title"], inner, e(t1["lead"])))

    t2 = d["teil2"]
    inner = (f'<p class="warn"><b>{e(t2["warn_title"])}</b>{e(t2["warn"])}</p>'
             f'<h3 class="sub">{e(t2["phrases_title"])}</h3>' + table(["기능", "문법", "기본 (통과)", "고득점 문장"], t2["phrases"], "phr", A) +
             f'<h3 class="sub">{e(t2["template_title"])}</h3>' + table(["단계", "표현"], t2["template"], "flow", A) +
             f'<h3 class="sub">{e(t2["perfekt_title"])}</h3><p class="note">{e(t2["perfekt_note"])}</p>' +
             table(["haben + p.p.", "haben + p.p. ", "sein + p.p."], t2["perfekt"], "pf", A) +
             f'<h3 class="sub">{e(t2["answers_title"])}</h3><p class="note">{e(t2["answers_note"])}</p>' + stories(t2))
    secs.append(section(t2["id"], t2["no"], t2["title"], inner, e(t2["lead"])))

    t3 = d["teil3"]
    inner = (f'<p class="note first">{e(t3["note"])}</p>'
             f'<h3 class="sub">{e(t3["phrases_title"])}</h3>' + table(["기능", "문법", "기본 (통과)", "고득점 문장"], t3["phrases"], "phr", A) +
             f'<h3 class="sub">{e(t3["flow_title"])}</h3>' + table(["단계", "표현", "예"], t3["flow"], "flow3", A) +
             f'<h3 class="sub">{e(t3["dialogs_title"])}</h3><p class="note">{e(t3["dialogs_note"])}</p>' + dialogs(t3))
    secs.append(section(t3["id"], t3["no"], t3["title"], inner, e(t3["lead"])))

    ze = d["zeit"]
    secs.append(section(ze["id"], "Zeit", ze["title"],
                        f'<p class="warn"><b>{e(ze["warn_title"])}</b>{e(ze["warn"])}</p>' + table(ze["head"], ze["rows"], "zt", A) +
                        f'<p class="note">{e(ze["note"])}</p>'))

    au = d["aussprache"]
    secs.append(section(au["id"], "Aussprache", au["title"], table(au["head"], au["rows"], "ap", A), e(au["intro"])))

    rp = d["repair"]
    secs.append(section(rp["id"], "Nachfragen", rp["title"], table(rp["head"], rp["rows"], "rp", A), e(rp["intro"])))

    nav = [("uebersicht", "시험 구조"), ("bewertung", "채점"), ("schritte", "준비 5단계"), ("plan", "4주 플랜"),
           ("pruefungstag", "시험 당일"), ("fehler", "실수"), ("einstieg", "도입 대화"), ("teil1", "Teil 1 질문과 답"),
           ("teil2", "Teil 2 이야기"), ("teil3", "Teil 3 계획"), ("zeit", "시간 표현"), ("aussprache", "발음"), ("wiederholen", "되묻기")]
    return page("Sprechen", d, nav, secs, CSS_EXTRA)


CSS_EXTRA = """.note.first{margin-top:14px}
.tbl.abl td:first-child,.tbl.plan td:first-child,.tbl.flow td:first-child,.tbl.flow3 td:first-child,.tbl.kw td:first-child,.tbl.zt td:first-child,.tbl.ap td:first-child,.tbl.wu td:first-child,.tbl.qa3 td:first-child,.tbl.crit3 td:first-child,.tbl.rp td:first-child{font-weight:700}
.tbl.abl td:nth-child(2),.tbl.plan td:first-child{white-space:nowrap}
.tbl.abl td:nth-child(2){color:var(--ochre-ink);font-weight:700}
.tbl.crit3 td:nth-child(2){color:var(--ochre-ink);font-size:13.5px;font-weight:600}
.tbl.plan td:nth-child(2){font-weight:700}
.tbl.plan td:first-child{color:var(--ochre-ink);letter-spacing:.06em}
.tbl.flow3 td:nth-child(2){font-weight:600}
.tbl.zt td:nth-child(2){color:var(--ink-2)}
.tbl.ap td:first-child{font-size:20px;color:var(--ochre-ink)}
.tbl.pf td{white-space:nowrap}
.tbl.wu td:first-child{font-weight:700}
.kard{margin-top:12px;padding:9px 13px;border:1.5px dashed var(--line);border-radius:10px;font-size:13.5px;color:var(--ink-2);line-height:1.55}
.kard b{display:block;font-size:11.5px;letter-spacing:.12em;color:var(--ochre-ink);margin-bottom:1px}
.qa{margin-top:12px;font-size:14px;line-height:1.6;word-break:normal}
.qa p{margin:0 0 4px;display:grid;grid-template-columns:48px minmax(0,1fr);column-gap:6px}
.qa .who{font-size:12px;font-weight:800;color:var(--ochre-ink);padding-top:2px}
.dgs{display:grid;gap:16px;margin-top:6px}
.dg{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:18px 20px 16px}
.dg-t{margin-top:12px;font-size:14px;line-height:1.6;color:var(--ink-2)}
.dg-t b{display:inline-block;margin-right:8px;font-size:11.5px;letter-spacing:.12em;color:var(--ochre-ink)}
.cal{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;margin-top:12px}
.cal>div{background:var(--mist);border-radius:10px;padding:10px 12px;font-size:13.5px;line-height:1.5}
.cal h4{margin:0 0 4px;font-size:12px;font-weight:700;letter-spacing:.06em;color:var(--ochre-ink)}
.cal ul{margin:0}
.cal li{display:flex;gap:10px;padding:1px 0}
.cal time{flex:none;color:var(--ink-3);font-variant-numeric:tabular-nums}
.dg-r{margin-top:10px;font-size:13.5px;font-weight:700;color:var(--ink-2)}
.dg-r span{color:var(--ochre-ink);margin-left:6px}
.pts{display:flex;flex-wrap:wrap;gap:6px;margin-top:12px}
.pts li{font-size:13px;padding:3px 11px;border:1px solid var(--line);border-radius:999px;background:var(--mist)}
.dg-b{margin-top:12px;padding:12px 14px;background:var(--mist);border-radius:10px}
.dl{display:grid;grid-template-columns:26px minmax(0,1fr);column-gap:8px;margin:0 0 7px;font-size:14.5px;line-height:1.65;word-break:normal}
.dl:last-child{margin-bottom:0}
.dl b{width:22px;height:22px;margin-top:2px;border-radius:50%;background:var(--navy);color:var(--ivory);font-size:12px;line-height:22px;text-align:center}
@media (max-width:560px){.cal{grid-template-columns:1fr}.tbl.pf td{white-space:normal}}
@media print{.dg{break-inside:avoid}}
"""


def main():
    d = json.load(open(os.path.join(HERE, "sprechen-data.json"), encoding="utf-8"))
    page_html = build(d)
    open(OUT, "w", encoding="utf-8").write(page_html)
    finish(OUT, APP)
    t2, t3 = d["teil2"]["answers"], d["teil3"]["dialogs"]
    counts = ", ".join(str(words(a["body"])) for a in t2)
    print(f"geschrieben: {OUT} ({os.path.getsize(OUT) / 1024:.0f} KB), Teil 2 이야기 {len(t2)}편({counts}단어), Teil 3 대화 {len(t3)}편")


if __name__ == "__main__":
    main()
