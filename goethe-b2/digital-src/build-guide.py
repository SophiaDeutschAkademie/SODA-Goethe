#!/usr/bin/env python3
"""Goethe B2 쓰기 시험 대비 가이드(schreiben-guide.html)를 만듭니다.

입력  guide-data.json   가이드의 모든 글과 모범 답안
출력  ../schreiben-guide.html (이 앱 폴더)

모범 답안의 단어 수는 이 스크립트가 직접 세고, 범위를 벗어나면 멈춥니다.
  Teil 1  150~260단어 (본문만), Teil 2  100~170단어 (Anrede + 본문 + Gruß + 이름)
공통 헬퍼와 기본 CSS는 guidelib.py 에 있습니다(다른 레벨 앱의 guidelib.py 와 같은 파일, 레벨 이름만 다름).

사용법 (앱 폴더에서)
  python3 -I digital-src/build-guide.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)  # python3 -I 로 돌려도 guidelib를 찾도록
from guidelib import NUMS, e, finish, page, section, table, words  # noqa: E402

APP = os.path.dirname(HERE)
OUT = os.path.join(APP, "schreiben-guide.html")


def texts(part):
    """모범 답안 카드. Teil 1(포럼 글)은 본문만, Teil 2는 Anrede·본문·Gruß를 보여 줍니다."""
    lo, hi = part["range"]
    cards = []
    for i, a in enumerate(part["answers"]):
        anrede, gruss = a.get("anrede", ""), a.get("gruss", "")
        paras = a["body"].split("\n\n")
        total = words(anrede) + words(a["body"]) + words(gruss)
        if not (lo <= total <= hi):
            sys.exit(f'{part["no"]} 모범 답안 {i + 1} "{a["title"]}": {total}단어, 범위 {lo}~{hi}를 벗어났습니다')
        ps = "".join(f'<p lang="de" class="lt-t">{e(p)}</p>' for p in paras)
        if anrede:
            gl = "".join(f'<p lang="de">{e(l)}</p>' for l in gruss.split("\n"))
            box = f'<div class="lt-b"><p lang="de">{e(anrede)}</p>{ps}<div class="lt-g">{gl}</div></div>'
            count = f'<b>{total}</b> Wörter <span>Anrede·Gruß·이름 포함</span>'
        else:
            box = f'<div class="lt-b">{ps}</div>'
            count = f'<b>{total}</b> Wörter <span>본문 기준</span>'
        pts = '<ol class="lp" lang="de">' + "".join(f"<li>{e(p)}</li>" for p in a["points"]) + "</ol>"
        cards.append(
            f'<article class="lt"><header class="lt-h"><span class="lt-n" aria-hidden="true">{NUMS[i]}</span>'
            f'<div><h3>{e(a["title"])}</h3><p class="lt-p" lang="de">{e(a["task"])}</p></div></header>'
            f'{pts}{box}<p class="lt-c">{count}</p></article>')
    return f'<div class="lts">{"".join(cards)}</div>'


def build(d):
    A = "auto"
    secs = []
    ov = d["overview"]
    secs.append(section(ov["id"], "Überblick", ov["title"],
                        '<dl class="kv">' + "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in ov["rows"]) + "</dl>" +
                        f'<h3 class="sub">{e(d["diff"]["title"])}</h3><p class="note">{e(d["diff"]["text"])}</p>'))

    sc = d["scoring"]
    inner = (table(["기준", "보는 것"], sc["criteria"], "crit2", A) +
             f'<p class="note">{e(sc["levels_note"])}</p>'
             f'<p class="warn"><b>0점 규칙</b>{e(sc["zero"])}</p>'
             f'<h3 class="sub">{e(sc["rules_title"])}</h3><ul class="bul">' + "".join(f"<li>{e(r)}</li>" for r in sc["rules"]) + "</ul>")
    secs.append(section(sc["id"], "Bewertung", sc["title"], inner, e(sc["intro"])))

    st = d["steps"]
    secs.append(section(st["id"], "Vorbereitung", st["title"], '<ol class="num">' + "".join(
        f'<li><span class="n">{e(n)}</span><span>{e(t)}</span></li>' for n, t in st["rows"]) + "</ol>"))

    pl = d["plan"]
    secs.append(section(pl["id"], "Lernplan", pl["title"], table(["주차", "집중 과제", "내용"], pl["rows"], "plan", A), e(pl["intro"])))

    sg = d["strategy"]
    inner = (f'<h3 class="sub">{e(sg["time_title"])}</h3>' + table(sg["time_head"], sg["time"], "tm", A) +
             f'<h3 class="sub">{e(sg["tips_title"])}</h3><ol class="num circ">' + "".join(
                 f'<li><span class="n">{e(n)}</span><span>{e(t)}</span></li>' for n, t in sg["tips"]) + "</ol>")
    secs.append(section(sg["id"], "Strategie", sg["title"], inner, e(sg["intro"])))

    ck = d["checklist"]
    secs.append(section(ck["id"], "Checkliste", ck["title"], '<ul class="chk">' + "".join(
        f'<li><span class="bx" aria-hidden="true"></span><span><b>{i + 1}</b>{e(t)}</span></li>' for i, t in enumerate(ck["items"])) + "</ul>"))

    for key in ("teil1", "teil2"):
        part = d[key]
        inner = (f'<h3 class="sub">{e(part["structure_title"])}</h3>' + table(part["structure_head"], part["structure"], "struct", A))
        if part.get("apply"):
            inner += f'<p class="note">{e(part["apply"])}</p>'
        inner += (f'<h3 class="sub">{e(part["phrases_title"])}</h3>' + table(["기능", "포인트", "고득점 표현 (B2급)"], part["phrases"], "phr", A))
        if part.get("reasons"):
            inner += f'<h3 class="sub">{e(part["reasons_title"])}</h3><p class="note">{e(part["reasons"])}</p>'
        inner += f'<h3 class="sub">{e(part["answers_title"])}</h3><p class="note">{e(part["answers_note"])}</p>' + texts(part)
        secs.append(section(part["id"], part["no"], part["title"], inner, e(part["lead"])))

    gr = d["grammar"]
    secs.append(section(gr["id"], "Grammatik", gr["title"], table(gr["head"], gr["rows"], "gram", A), e(gr["intro"])))

    nav = [("uebersicht", "시험 구조"), ("bewertung", "채점"), ("schritte", "준비 6단계"), ("plan", "4주 플랜"),
           ("strategie", "시간 배분"), ("checkliste", "체크리스트"), ("teil1", "Teil 1 포럼 글"), ("teil2", "Teil 2 격식 메시지"),
           ("grammatik", "문법 16")]
    return page("Schreiben", d, nav, secs, CSS_EXTRA)


CSS_EXTRA = """.tbl.crit2 td:first-child,.tbl.tm td:first-child,.tbl.plan td:first-child,.tbl.struct td:first-child,.tbl.gram td:first-child{font-weight:700}
.tbl.crit2 td:first-child{white-space:nowrap}
.tbl.tm td:nth-child(2){font-weight:700;color:var(--ochre-ink);white-space:nowrap}
.tbl.plan td:first-child{color:var(--ochre-ink);white-space:nowrap}
.tbl.plan td:nth-child(2){font-weight:700}
.tbl.struct td:first-child{color:var(--ochre-ink);white-space:nowrap}
.tbl.struct td:nth-child(3){font-size:14px}
.tbl.phr td:first-child{font-weight:700;white-space:nowrap}
.tbl.phr td:nth-child(2){color:var(--ink-3);font-size:13.5px;white-space:nowrap}
.tbl.phr td:nth-child(3){font-weight:600}
.tbl.gram td:nth-child(2){color:var(--ink-3)}
.tbl.gram td:nth-child(3){font-weight:600}
.lp{margin:12px 0 0;padding:0;list-style:none;font-size:13.5px;line-height:1.55;color:var(--ink-2)}
.lp li{position:relative;padding-left:16px;margin:0 0 2px}
.lp li::before{content:"·";position:absolute;left:4px;font-weight:700;color:var(--ochre-ink)}
.lt-t{margin-top:0}
"""


def main():
    d = json.load(open(os.path.join(HERE, "guide-data.json"), encoding="utf-8"))
    html_out = build(d)
    open(OUT, "w", encoding="utf-8").write(html_out)
    finish(OUT, APP)
    c = [len(d[k]["answers"]) for k in ("teil1", "teil2")]
    print(f"geschrieben: {OUT} ({os.path.getsize(OUT) / 1024:.0f} KB), 모범 답안 {c[0]}+{c[1]}편")


if __name__ == "__main__":
    main()
