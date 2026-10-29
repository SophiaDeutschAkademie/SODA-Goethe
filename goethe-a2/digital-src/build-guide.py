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
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)  # python3 -I 로 돌려도 guidelib를 찾도록
from guidelib import NUMS, e, finish, page, section, table, words  # noqa: E402

APP = os.path.dirname(HERE)
OUT = os.path.join(APP, "schreiben-guide.html")


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

    return page("Schreiben", d, nav, secs)


def main():
    d = json.load(open(os.path.join(HERE, "guide-data.json"), encoding="utf-8"))
    page = build(d)
    open(OUT, "w", encoding="utf-8").write(page)
    finish(OUT, APP)
    n1, n2 = len(d["teil1"]["answers"]), len(d["teil2"]["answers"])
    print(f"geschrieben: {OUT} ({os.path.getsize(OUT) / 1024:.0f} KB), 모범 답안 {n1}+{n2}편")


if __name__ == "__main__":
    main()
