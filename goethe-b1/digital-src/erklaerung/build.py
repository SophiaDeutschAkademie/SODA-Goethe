#!/usr/bin/env python3
"""Goethe-Zertifikat B1 Modelltest N 해설 — 단일 HTML 빌드.

python3 -I build.py <app-folder> <N> <font.ttf> <out.html> [web]
해설 데이터: erkN_lesen.py, erkN_hoeren.py (형식은 FORMAT.md), 모든 회차가 함께 쓰는 글: gemeinsam.py
web: 저장소용 — 시험 페이지로 돌아가는 버튼과 접속 집계 태그를 넣습니다. 없으면 학생에게 파일로 주는 오프라인판입니다.

빌드 전에 검사합니다(어긋나면 멈춤): 정답, Lesen·Hören 인용이 원문에 그대로 있는지,
Hören 4 인용의 말하는 사람이 정답과 같은지, 모범 답안 문단 수.
"""
import base64
import html
import importlib
import importlib.util
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

APP, N, FONT, OUT = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
WEB = len(sys.argv) > 5 and sys.argv[5] == "web"
D = json.load(open(os.path.join(APP, "digital-src", "data", f"mt{N}.json"), encoding="utf-8"))
ROMAN = D["roman"]
G = importlib.import_module("gemeinsam")
_l = importlib.import_module(f"erk{N}_lesen")
_h = importlib.import_module(f"erk{N}_hoeren")
LESEN1, LESEN2, LESEN3, LESEN4, LESEN5 = _l.LESEN1, _l.LESEN2, _l.LESEN3, _l.LESEN4, _l.LESEN5
HOEREN1, HOEREN2, HOEREN3, HOEREN4, SCHREIBEN, SPRECHEN = (_h.HOEREN1, _h.HOEREN2, _h.HOEREN3, _h.HOEREN4,
                                                           _h.SCHREIBEN, _h.SPRECHEN)
L, H, S, HT, K = D["lesen"], D["hoeren"], D["schreiben"], D["hoertexte"], D["kommentar"]

spec = importlib.util.spec_from_file_location("sodatheme", os.path.join(APP, "..", "tools", "soda-theme.py"))
st = importlib.util.module_from_spec(spec)
spec.loader.exec_module(st)

e = html.escape
WORD = {"R": "Richtig", "F": "Falsch", "J": "Ja", "N": "Nein"}


def de(s):
    return f'<span lang="de">{e(s)}</span>'


# ---------- 검사 ----------
def same(name, mine, ref):
    got = {i["no"]: i["ans"] for i in mine}
    want = {i["no"]: i["answer"] for i in ref}
    if got != want:
        sys.exit(f"{name} 정답 불일치: {got} != {want}")


def need(text, basis, where):
    for b in basis:
        if b[0] not in text:
            sys.exit(f"{where}: 원문에 없는 인용: {b[0][:80]}")


same("Lesen 1", LESEN1["items"], L["t1"]["items"])
for x in (0, 1):
    same(f"Lesen 2 글 {x + 1}", LESEN2["texts"][x]["items"], L["t2"]["texts"][x]["items"])
same("Lesen 3", LESEN3["items"], L["t3"]["items"])
same("Lesen 4", LESEN4["items"], L["t4"]["items"])
same("Lesen 5", LESEN5["items"], L["t5"]["items"])
for x in range(5):
    same(f"Hören 1 Text {x + 1}", HOEREN1["texts"][x]["items"], H["t1"]["texts"][x]["items"])
same("Hören 2", HOEREN2["items"], H["t2"]["items"])
same("Hören 3", HOEREN3["items"], H["t3"]["items"])
same("Hören 4", HOEREN4["items"], H["t4"]["items"])

blog = L["t1"]["blog"]
BLOG = " ".join([blog.get("site", ""), blog.get("date", ""), blog.get("title", ""), " ".join(blog["paragraphs"]), blog.get("closing", "")])
for it in LESEN1["items"]:
    need(BLOG, it["basis"], f"Lesen {it['no']}")
for x, tx in enumerate(L["t2"]["texts"]):
    txt = " ".join([tx.get("title", ""), tx.get("lead", ""), " ".join(tx["paragraphs"]), tx.get("footnote", "")])
    for it in LESEN2["texts"][x]["items"]:
        need(txt, it["basis"], f"Lesen {it['no']}")
ADS = {a["letter"]: " ".join(x for x in [a.get("header", ""), a.get("tag", ""), a.get("title", ""), a.get("subtitle", ""),
                                         *a.get("facts", []), *a.get("body", []), a.get("footer", "")] if x)
       for a in L["t3"]["ads"]}


def ad_of(q, where):
    for k, t in ADS.items():
        if q in t:
            return k
    sys.exit(f"{where}: 광고 한 칸 안에 없는 인용: {q[:80]}")


for it in LESEN3["items"]:
    for b in it["basis"]:
        ad_of(b[0], f"Lesen {it['no']}")
    if it["ans"] != "0" and not any(b[0] in ADS[it["ans"]] for b in it["basis"]):
        sys.exit(f"Lesen {it['no']}: 정답 광고 {it['ans']}에서 가져온 인용이 없습니다")
for it, q in zip(LESEN4["items"], L["t4"]["items"]):
    need(q["text"], it["basis"], f"Lesen {it['no']}")
doc = L["t5"]["doc"]
DOC = " ".join([doc.get("title", ""), doc.get("intro", ""), " ".join((s["heading"] + " " + s["text"]).strip() for s in doc["sections"]), doc.get("footer", "")])
for it in LESEN5["items"]:
    need(DOC, it["basis"], f"Lesen {it['no']}")

for x in range(5):
    for it in HOEREN1["texts"][x]["items"]:
        need(HT["t1"]["texts"][x]["text"], it["basis"], f"Hören {it['no']}")
H2TXT = HT["t2"]["text"].replace("\n\n", " ")
for it in HOEREN2["items"]:
    need(H2TXT, it["basis"], f"Hören {it['no']}")


def who_of(turns, b, where):
    """인용이 들어 있는 발화의 말하는 사람. basis의 셋째 칸에 이름을 적으면 그 사람의 발화에서 찾습니다."""
    want = b[2] if len(b) > 2 else None
    for u in turns:
        if b[0] in u["text"] and (want is None or u["who"] == want):
            return u["who"]
    sys.exit(f"{where}: 한 사람의 발화 안에 없는 인용: {b[0][:80]}")


for it in HOEREN3["items"]:
    for b in it["basis"]:
        who_of(HT["t3"]["turns"], b, f"Hören {it['no']}")
SPK = H["t4"]["speakers"]
for it in HOEREN4["items"]:
    whos = [who_of(HT["t4"]["turns"], b, f"Hören {it['no']}") for b in it["basis"]]
    if not any(w in SPK[it["ans"]] for w in whos):
        sys.exit(f"Hören {it['no']}: 정답({SPK[it['ans']]})이 말한 인용이 없습니다: {whos}")

paras = [t["model"]["text"].split("\n\n") for t in S["tasks"]]
for k, t in enumerate(SCHREIBEN["tasks"]):
    if len(paras[k]) != len(t["model_ko"]):
        sys.exit(f"Schreiben {k + 1}: model_ko {len(t['model_ko'])}개, 모범 답안 문단 {len(paras[k])}개")
if len(SCHREIBEN["tasks"][0]["points"]) != len(S["tasks"][0]["points"]):
    sys.exit("Schreiben 1: Leitpunkt 수가 다릅니다")
for mine, ref in zip(SCHREIBEN["tasks"][0]["points"], S["tasks"][0]["points"]):
    if mine[0] != ref:
        sys.exit(f"Schreiben 1: Leitpunkt가 시험지와 다릅니다: {mine[0]}")


# ---------- 조각 ----------
def quotes(basis, label=None):
    out = []
    for b in basis:
        lab = label(b) if label else ""
        out.append(f'<blockquote><p class="q">{lab}{de(b[0])}</p><p class="tr">{e(b[1])}</p></blockquote>')
    return "".join(out)


def vocab(v):
    if not v:
        return ""
    return '<div class="voc"><h5>어휘</h5><ul>' + "".join(f'<li><b lang="de">{e(a)}</b><span>{e(b)}</span></li>' for a, b in v) + "</ul></div>"


def card(no, ans_html, head, body):
    return (f'<article class="card" id="a{no}"><header><span class="no">{no}</span>'
            f'<span class="ans">{ans_html}</span><div class="hd">{head}</div></header>'
            f'<div class="exp">{body}</div></article>')


def tip(t):
    return f'<p class="tip"><b>푸는 요령</b>{e(t)}</p>'


def opts(options, ans, wrong):
    return '<ol class="opts">' + "".join(
        f'<li class="{"ok" if k == ans else ""}"><b>{k}</b><span lang="de">{e(v)}</span>'
        + (f'<em>{e(wrong[k])}</em>' if k in wrong else "") + "</li>" for k, v in options.items()) + "</ol>"


def trap(t, label="함정"):
    return f'<p class="trap"><b>{label}</b>{e(t)}</p>' if t else ""


def why(t):
    return f"<p>{e(t)}</p>"


FT = {t[0]: t for t in G.FALLEN}


def ft(part, no):
    """Kommentar의 함정 유형 표시."""
    k = K[part].get(str(no))
    if not k or k["type"] not in FT:
        return ""
    _, ko, name, _ = FT[k["type"]]
    return f'<p class="ft"><b>함정 유형</b><span>{e(ko)}</span><i lang="de">{e(name)}</i></p>'


def section(sid, small, title, intro, tipt):
    return (f'<section id="{sid}"><h2><small>{small}</small>{title}</h2>'
            + (f'<p class="intro">{e(intro)}</p>' if intro else "") + tip(tipt))


def full(summary, inner):
    return f'<details class="full"><summary>{summary}</summary><div class="letter">{inner}</div></details>'


def ctx(t):
    return f'<p class="ctx" lang="de">{e(t)}</p>' if t else ""


def jn(a):
    return f'<b class="jn">{WORD[a]}</b>'


# ---------- Lesen ----------
t1 = L["t1"]
blog_html = (f'<p class="meta" lang="de">{e(" · ".join(x for x in (blog.get("site"), blog.get("date")) if x))}</p>'
             f'<p class="ttl" lang="de">{e(blog["title"])}</p>'
             + "".join(f'<p lang="de">{e(x)}</p>' for x in blog["paragraphs"])
             + (f'<p lang="de">{e(blog["closing"])}</p>' if blog.get("closing") else ""))
p = [section("l1", "Lesen", f'Teil 1 · 블로그 <span lang="de">„{e(blog["title"])}“</span>', LESEN1.get("intro"), LESEN1["tip"]),
     full("본문 전체 보기", blog_html)]
for it, q in zip(LESEN1["items"], t1["items"]):
    head = f'<p class="pick">{de(q["text"])}</p><p class="tr">{e(it["stko"])}</p>'
    p.append(card(it["no"], jn(it["ans"]), head, ft("lesen", it["no"]) + quotes(it["basis"]) + why(it["why"]) + vocab(it.get("vocab"))))
SEC_L1 = "".join(p) + "</section>"

p = [section("l2", "Lesen", "Teil 2 · 신문 기사 두 편", LESEN2.get("intro"), LESEN2["tip"])]
for tx, mine in zip(L["t2"]["texts"], LESEN2["texts"]):
    nos = [i["no"] for i in tx["items"]]
    body = (f'<p class="ttl" lang="de">{e(tx["title"])}</p><p lang="de"><b>{e(tx["lead"])}</b></p>'
            + "".join(f'<p lang="de">{e(x)}</p>' for x in tx["paragraphs"])
            + (f'<p class="meta" lang="de">{e(tx["footnote"])}</p>' if tx.get("footnote") else "")
            + (f'<p class="meta" lang="de">{e(tx["source"])}</p>' if tx.get("source") else ""))
    p.append(f'<h3 class="txt"><span lang="de">„{e(tx["title"])}“</span> <small>{nos[0]}–{nos[-1]}번</small></h3>'
             f'<p class="intro">{e(mine["intro"])}</p>' + full("본문 전체 보기", body))
    for it, q in zip(mine["items"], tx["items"]):
        head = f'<p class="pick">{de(q["stem"])}</p>'
        p.append(card(it["no"], f'<b>{it["ans"]}</b>', head,
                      ft("lesen", it["no"]) + quotes(it["basis"]) + why(it["why"]) + opts(q["options"], it["ans"], it.get("wrong", {})) + vocab(it.get("vocab"))))
SEC_L2 = "".join(p) + "</section>"

t3 = L["t3"]
used = {i["answer"]: i["no"] for i in t3["items"] if i["answer"] != "0"}


def adcard(a):
    k = a["letter"]
    if k == t3["example"]["answer"]:
        use, cls = "예시 0", "ex"
    elif k in used:
        use, cls = f"{used[k]}번", ""
    else:
        use, cls = "쓰이지 않음", "un"
    out = [f'<figcaption><b>{k}</b><span class="use">{use}</span></figcaption>']
    if a.get("tag"):
        out.append(f'<p class="ad-tag" lang="de">{e(a["tag"])}</p>')
    if a.get("header"):
        out.append(f'<p class="ad-header" lang="de">{e(a["header"])}</p>')
    if a.get("title"):
        out.append(f'<p class="ad-title" lang="de">{e(a["title"])}</p>')
    if a.get("subtitle"):
        out.append(f'<p class="ad-sub" lang="de">{e(a["subtitle"])}</p>')
    if a.get("facts"):
        out.append('<ul class="ad-facts" lang="de">' + "".join(f"<li>{e(x)}</li>" for x in a["facts"]) + "</ul>")
    out += [f'<p lang="de">{e(x)}</p>' for x in a.get("body", [])]
    if a.get("footer"):
        out.append(f'<p class="ad-footer" lang="de">{e(a["footer"])}</p>')
    return f'<figure class="adt {cls}">' + "".join(out) + "</figure>"


adgrid = '<div class="adts">' + "".join(adcard(a) for a in t3["ads"]) + "</div>"
p = [section("l3", "Lesen", "Teil 3 · 광고 고르기", LESEN3.get("intro"), LESEN3["tip"]), ctx(t3.get("context")),
     f'<details class="full"><summary>광고 a–j 전체 보기</summary>{adgrid}</details>']
for it, q in zip(LESEN3["items"], t3["items"]):
    head = f'<p class="pick">{de(q["text"])}</p><p class="tr">{e(it["stko"])}</p><p class="cond"><b>조건</b>{e(it["cond"])}</p>'
    if it["ans"] == "0":
        ans = "<b>0</b><i>맞는 광고 없음</i>"
    else:
        a = next(x for x in t3["ads"] if x["letter"] == it["ans"])
        ans = f'<b>{it["ans"]}</b><i lang="de">{e(a.get("header") or a.get("title") or "")}</i>'
    lab = lambda b, no=it["no"]: f'<b class="who">{ad_of(b[0], no)}</b>'  # noqa: E731
    p.append(card(it["no"], ans, head, ft("lesen", it["no"]) + quotes(it["basis"], lab) + why(it["why"]) + trap(it.get("trap"))))
p.append(f'<p class="note">{e(LESEN3["unused"])}</p>')
SEC_L3 = "".join(p) + "</section>"

t4 = L["t4"]
m = re.search(r"Wählen Sie: (.+)$", t4["instruction"])
frage = m.group(1) if m else ""
ex = t4["example"]
p = [section("l4", "Lesen", "Teil 4 · 독자 의견", LESEN4.get("intro"), LESEN4["tip"]), ctx(t4.get("context")),
     f'<p class="frage"><b>질문</b>{de(frage)}</p>',
     f'<p class="note exnote">예시 0 · {de(ex["byline"])} → {WORD[ex["answer"]]}</p>']
for it, q in zip(LESEN4["items"], t4["items"]):
    head = f'<p class="pick">{de(q["byline"])}</p>'
    src = f'<details class="src"><summary>글 전체 보기</summary><p lang="de">{e(q["text"])}</p></details>'
    p.append(card(it["no"], jn(it["ans"]), head, ft("lesen", it["no"]) + quotes(it["basis"]) + why(it["why"]) + trap(it.get("trap")) + src))
SEC_L4 = "".join(p) + "</section>"

t5 = L["t5"]
doc_html = (f'<p class="ttl" lang="de">{e(doc["title"])}</p>' + (f'<p lang="de">{e(doc["intro"])}</p>' if doc.get("intro") else "")
            + "".join(f'<p lang="de">{("<b>" + e(s["heading"]) + "</b> ") if s["heading"] else ""}{e(s["text"])}</p>' for s in doc["sections"])
            + (f'<p lang="de">{e(doc["footer"])}</p>' if doc.get("footer") else ""))
p = [section("l5", "Lesen", f'Teil 5 · 규정 <span lang="de">{e(doc["title"])}</span>', LESEN5.get("intro"), LESEN5["tip"]), ctx(t5.get("context")),
     full("본문 전체 보기", doc_html)]
for it, q in zip(LESEN5["items"], t5["items"]):
    head = f'<p class="pick">{de(q["stem"])}</p>'
    p.append(card(it["no"], f'<b>{it["ans"]}</b>', head,
                  ft("lesen", it["no"]) + quotes(it["basis"]) + why(it["why"]) + opts(q["options"], it["ans"], it.get("wrong", {})) + vocab(it.get("vocab"))))
SEC_L5 = "".join(p) + "</section>"


# ---------- Hören ----------
def hsec(sid, k, title, data, times):
    return section(sid, "Hören", f"Teil {k} · {e(title)} ({times})", data.get("intro"), data["tip"])


def hcard(it, q, lab=None, extra=""):
    """Richtig/Falsch 문장 또는 a/b/c 문항 한 개."""
    if "options" in q:
        head = f'<p class="pick">{de(q["stem"])}</p><p class="tr">{e(it["stko"])}</p>'
        ans = f'<b>{it["ans"]}</b>'
        tail = opts(q["options"], it["ans"], it.get("wrong", {}))
    else:
        head = f'<p class="pick">{de(q["text"])}</p><p class="tr">{e(it["stko"])}</p>'
        ans = jn(it["ans"])
        tail = ""
    return card(it["no"], ans, head, ft("hoeren", it["no"]) + "<h6>들은 내용</h6>" + quotes(it["basis"], lab) + why(it["why"]) + tail + trap(it.get("trap")) + extra)


def turns_html(turns):
    return "".join(f'<p lang="de"><b>{e(u["who"])}:</b> {e(u["text"])}</p>' for u in turns)


p = [hsec("h1", 1, "짧은 글 다섯 개", HOEREN1, "각 2회")]
for x, (tx, mine, ht) in enumerate(zip(H["t1"]["texts"], HOEREN1["texts"], HT["t1"]["texts"]), 1):
    nos = [i["no"] for i in tx["items"]]
    p.append(f'<h3 class="txt">Text {x} · {e(mine["scene"])} <small>{nos[0]}–{nos[-1]}번</small></h3>'
             + full("대본 보기", f'<p class="meta" lang="de">{e(ht["scene"])}</p><p lang="de">{e(ht["text"])}</p>'))
    for it, q in zip(mine["items"], tx["items"]):
        p.append(hcard(it, q))
SEC_H1 = "".join(p) + "</section>"

p = [hsec("h2", 2, HOEREN2["title"], HOEREN2, "1회"), ctx(H["t2"].get("context")),
     full("대본 전체 보기", "".join(f'<p lang="de">{e(x)}</p>' for x in HT["t2"]["text"].split("\n\n")))]
for it, q in zip(HOEREN2["items"], H["t2"]["items"]):
    p.append(hcard(it, q))
SEC_H2 = "".join(p) + "</section>"

p = [hsec("h3", 3, HOEREN3["title"], HOEREN3, "1회"), ctx(H["t3"].get("context")),
     full("대본 전체 보기", turns_html(HT["t3"]["turns"]))]
for it, q in zip(HOEREN3["items"], H["t3"]["items"]):
    lab = lambda b, no=it["no"]: f'<b class="who">{e(who_of(HT["t3"]["turns"], b, no))}</b>'  # noqa: E731
    p.append(hcard(it, q, lab))
SEC_H3 = "".join(p) + "</section>"

spk = "".join(f"<li><b>{k}</b><span lang=\"de\">{e(v)}</span></li>" for k, v in SPK.items())
ex4 = H["t4"]["example"]
p = [hsec("h4", 4, HOEREN4["title"], HOEREN4, "2회"), ctx(H["t4"].get("context")),
     f'<ul class="spk">{spk}</ul>',
     f'<p class="note exnote">예시 0 · {de(ex4["text"])} → {ex4["answer"]} {de(SPK[ex4["answer"]])}</p>',
     full("대본 전체 보기", turns_html(HT["t4"]["turns"]))]
for it, q in zip(HOEREN4["items"], H["t4"]["items"]):
    lab = lambda b, no=it["no"]: f'<b class="who">{e(who_of(HT["t4"]["turns"], b, no))}</b>'  # noqa: E731
    head = f'<p class="pick">{de(q["text"])}</p><p class="tr">{e(it["stko"])}</p>'
    ans = f'<b>{it["ans"]}</b><i lang="de">{e(SPK[it["ans"]])}</i>'
    p.append(card(it["no"], ans, head, ft("hoeren", it["no"]) + "<h6>들은 내용</h6>" + quotes(it["basis"], lab) + why(it["why"]) + trap(it.get("trap"))))
SEC_H4 = "".join(p) + "</section>"


# ---------- Schreiben ----------
def _tbl(rows, cls=""):
    return f'<table class="tbl {cls}"><tbody>' + "".join(f'<tr><td lang="de">{e(a)}</td><td>{e(b)}</td></tr>' for a, b in rows) + "</tbody></table>"


blocks = [f'<section id="w"><h2><small>Schreiben</small>쓰기 · Aufgabe 1–3</h2><p class="intro">{e(SCHREIBEN.get("intro") or G.SCHREIBEN_INTRO)}</p>']
for t, mine, ps in zip(S["tasks"], SCHREIBEN["tasks"], paras):
    model = "".join(f'<div class="mrow"><span class="lp"></span><p lang="de">{e(x).replace(chr(10), "<br>")}</p><p class="tr">{e(k)}</p></div>'
                    for x, k in zip(ps, mine["model_ko"]))
    task_de = "".join(f"<p>{e(x)}</p>" for x in t["situation"])
    if t["points"]:
        task_de += '<ul class="dots">' + "".join(f"<li>{e(x)}</li>" for x in t["points"]) + "</ul>"
    post = ""
    if t.get("post"):
        po = t["post"]
        task_de += (f'<div class="post"><p class="ph"><b>{e(po.get("label", ""))}</b>{e(po.get("site", ""))}</p>'
                    f'<p class="pa">{e(po.get("author", ""))}</p><p>{e(po["text"])}</p></div>')
        post = f'<p class="tr postko"><b>방명록 글 해석</b>{e(mine["post_ko"])}</p>'
    task_de += f"<p>{e(t['instruction'])}</p>"
    lps = "".join(f'<li><span class="n">{i}</span><div><p lang="de">{e(a)}</p><p class="tr">{e(b)}</p><p class="ex" lang="de">{e(c)}</p></div></li>'
                  for i, (a, b, c) in enumerate(mine["points"], 1))
    blocks.append(f"""<h3 class="task">Aufgabe {t["no"]} · {e(mine["title"])} <small>약 {t["words"]}단어 · {t["minutes"]}분</small></h3>
<p class="lead2">{e(mine["situation"])}</p>
<div class="box" lang="de"><h5>과제</h5>{task_de}</div>{post}
<h4 class="sub3">{G.POINTS_TITLE[t["no"]]}</h4><ol class="lps">{lps}</ol>
<h4 class="sub3">자주 하는 실수</h4><ul class="dots">{"".join(f"<li>{e(x)}</li>" for x in mine["traps"])}</ul>
<h4 class="sub3">모범 답안 <small lang="de">{e(t["model"].get("label", ""))}</small></h4><div class="model">{model}</div>
<h4 class="sub3">쓸 수 있는 표현</h4>{_tbl(mine["redemittel"])}""")
blocks.append(f"""<h3>채점 기준</h3><table class="tbl crit"><tbody>{"".join(f'<tr><th lang="de">{e(a)}</th><td><b>{e(b)}</b><br>{e(c)}</td></tr>' for a, b, c in G.SCHREIBEN_CRITERIA)}</tbody></table>
<p class="note">{e(G.SCHREIBEN_NOTE)}</p></section>""")
SEC_W = "".join(blocks)


# ---------- Sprechen ----------
GS = G.SPRECHEN
sp1, sp2, sp3 = SPRECHEN["t1"], SPRECHEN["t2"], SPRECHEN["t3"]


def dots(items):
    return '<ul class="dots">' + "".join(f"<li>{e(x)}</li>" for x in items) + "</ul>"


def h3sp(k):
    return f'<h3 class="task">Teil {k} · <span lang="de">{e(GS["names"][k - 1])}</span> <small>{GS["meta"][k - 1]}</small></h3>'


M = [f'<section id="m"><h2><small>Sprechen</small>말하기 · {e(GS["head"])}</h2><p class="intro">{e(GS["intro"])}</p>']
M.append(h3sp(1) + f'<p class="lead2">{e(sp1["task"])}</p>'
         + f'<div class="box"><h5 lang="de">{e(sp1["title"])}</h5>{_tbl(sp1["leit"], "inbox")}</div>'
         + '<h4 class="sub3">진행 요령</h4>' + dots(sp1.get("points", []) + GS["t1"]["points"])
         + (f'<h4 class="sub3">모범 대화의 흐름 <small>시험지 19쪽</small></h4><p>{e(sp1["muster"])}</p>' if sp1.get("muster") else "")
         + '<h4 class="sub3">쓸 수 있는 표현</h4>' + _tbl(sp1.get("redemittel", []) + GS["t1"]["redemittel"]))
folien = '<ol class="folien">' + "".join(f'<li><b>{e(a)}</b><span lang="de">{e(b)}</span><em>{e(c)}</em></li>' for a, b, c in GS["t2"]["folien"]) + "</ol>"
themen = ""
for k, th in enumerate(sp2["themen"], 1):
    rows = "".join(f'<tr><th>Folie {i}</th><td><span lang="de">{e(a)}</span><br><span class="tr">{e(b)}</span></td></tr>' for i, (a, b) in zip((2, 3, 4), th["ideas"]))
    themen += (f'<h4 class="sub3">Thema {k} · <span lang="de">{e(th["title"])}</span> <small>{e(th["ko"])}</small></h4>'
               f'<table class="tbl idea"><tbody>{rows}</tbody></table>')
M.append(h3sp(2) + f'<p class="lead2">{e(GS["t2"]["task"])}</p>' + folien + themen
         + (f'<p class="note">{e(sp2["note"])}</p>' if sp2.get("note") else "")
         + '<h4 class="sub3">진행 요령</h4>' + dots(sp2.get("points", []) + GS["t2"]["points"])
         + '<h4 class="sub3">쓸 수 있는 표현</h4>' + _tbl(GS["t2"]["redemittel"]))
M.append(h3sp(3) + f'<p class="lead2">{e(GS["t3"]["task"])}</p>'
         + '<h4 class="sub3">진행 요령</h4>' + dots(sp3.get("points", []) + GS["t3"]["points"])
         + (f'<h4 class="sub3">모범 문답의 흐름 <small>시험지 19쪽</small></h4><p>{e(sp3["muster"])}</p>' if sp3.get("muster") else "")
         + '<h4 class="sub3">이 시험의 주제로 할 수 있는 질문</h4>' + _tbl(sp3["fragen"])
         + '<h4 class="sub3">쓸 수 있는 표현</h4>' + _tbl(GS["t3"]["redemittel"]))
M.append('<h3>시험관이 보는 것</h3><table class="tbl crit wide"><tbody>'
         + "".join(f'<tr><th lang="de">{e(a)}</th><td>{e(b)}</td></tr>' for a, b in GS["achten"]) + "</tbody></table>"
         + f'<p class="note">{e(GS["note"])}</p></section>')
SEC_M = "".join(M)


# ---------- 정답표 ----------
def krow(label, href, items, pre="a"):
    cells = "".join(f'<a href="#{pre}{n}"><span>{n}</span><b>{e(WORD.get(a, a))}</b></a>' for n, a in items)
    return f'<div class="krow"><h4><a href="{href}">{label}</a></h4><div class="kc">{cells}</div></div>'


def ks(items):
    return [(i["no"], i["answer"]) for i in items]


fallen = "".join(f'<tr><th><span class="ftc">{e(ko)}</span></th><td><span lang="de">{e(name)}</span><br>{e(desc)}</td></tr>' for _, ko, name, desc in G.FALLEN)
KEY = ('<section id="key"><h2><small>Lösungsschlüssel</small>정답표</h2><p class="intro">번호를 누르면 해설로 이동합니다. Lesen과 Hören은 번호가 각각 1번부터 시작합니다.</p>'
       + krow("Lesen Teil 1", "#l1", ks(L["t1"]["items"]))
       + krow("Lesen Teil 2", "#l2", [x for t in L["t2"]["texts"] for x in ks(t["items"])])
       + krow("Lesen Teil 3", "#l3", ks(L["t3"]["items"])) + krow("Lesen Teil 4", "#l4", ks(L["t4"]["items"]))
       + krow("Lesen Teil 5", "#l5", ks(L["t5"]["items"]))
       + krow("Hören Teil 1", "#h1", [x for t in H["t1"]["texts"] for x in ks(t["items"])], "ha")
       + krow("Hören Teil 2", "#h2", ks(H["t2"]["items"]), "ha") + krow("Hören Teil 3", "#h3", ks(H["t3"]["items"]), "ha")
       + krow("Hören Teil 4", "#h4", ks(H["t4"]["items"]), "ha")
       + """<table class="tbl pts"><thead><tr><th>모듈</th><th>구성</th><th>점수</th></tr></thead><tbody>
<tr><td>Lesen</td><td>30문항, 문항마다 같은 점수 (18문항 = 60점)</td><td>100점</td></tr>
<tr><td>Hören</td><td>30문항, 문항마다 같은 점수 (18문항 = 60점)</td><td>100점</td></tr>
<tr><td>Schreiben</td><td>Aufgabe 1 40점 · Aufgabe 2 40점 · Aufgabe 3 20점</td><td>100점</td></tr>
<tr><td>Sprechen</td><td>Teil 1 28점 · Teil 2 40점 · Teil 3 16점 · Aussprache 16점</td><td>100점</td></tr>
</tbody></table><p class="note">모듈마다 100점 만점에 60점 이상이면 합격입니다. 네 모듈은 따로 채점하고, 떨어진 모듈만 다시 볼 수 있습니다.</p>"""
       + f'<details class="full fallen"><summary>함정 유형 여덟 가지 <small>문항마다 붙어 있는 표시의 뜻</small></summary><table class="tbl"><tbody>{fallen}</tbody></table></details></section>')

# Lesen과 Hören 번호가 겹치므로 Hören 카드의 id는 ha1…ha30
SEC_H = (SEC_H1 + SEC_H2 + SEC_H3 + SEC_H4).replace('<article class="card" id="a', '<article class="card" id="ha')

body_html = KEY + SEC_L1 + SEC_L2 + SEC_L3 + SEC_L4 + SEC_L5 + SEC_H + SEC_W + SEC_M
chars = set(body_html) | set(f"Goethe-Zertifikat B1 Modelltest {ROMAN} 해설 SODA Lehrwerk Sophia Deutsch Akademie 정답 가리기 보기 목차 정답표 위로 다크 모드 켜기 끄기 켜짐 꺼짐 누르면 라이트로 바뀌어요 페이지로 돌아가기 근거와 함정 모범 답안 진행 요령 문항")
from fontTools import subset  # noqa: E402
from fontTools.ttLib import TTFont  # noqa: E402
cps = set(range(0x20, 0x7F)) | {ord(c) for c in chars if ord(c) >= 0x20}
f = TTFont(FONT)
o = subset.Options()
o.flavor = "woff"
o.layout_features = ["kern", "liga", "calt", "locl", "tnum", "ccmp", "mark", "mkmk"]
o.notdef_outline = True
ss = subset.Subsetter(o)
ss.populate(unicodes=sorted(cps))
ss.subset(f)
f.flavor = "woff"
buf = io.BytesIO()
f.save(buf)
FONT64 = base64.b64encode(buf.getvalue()).decode()
LOGO64 = base64.b64encode(open(os.path.join(APP, "digital-src", "logo-small.png"), "rb").read()).decode()
CSS = open(os.path.join(HERE, "style.css"), encoding="utf-8").read().replace("__FONT__", FONT64)
NAV = [("key", "정답표"), ("l1", "Lesen 1"), ("l2", "Lesen 2"), ("l3", "Lesen 3"), ("l4", "Lesen 4"), ("l5", "Lesen 5"),
       ("h1", "Hören 1"), ("h2", "Hören 2"), ("h3", "Hören 3"), ("h4", "Hören 4"), ("w", "Schreiben"), ("m", "Sprechen")]
nav = "".join(f'<a href="#{a}">{b}</a>' for a, b in NAV)
if WEB:
    back = (st.TOC_JS.replace("__HREF__", f"index.html#{N}").replace("목차로 돌아가기", f"Modelltest {ROMAN} 페이지로 돌아가기")
            .replace("</svg>목차", f"</svg>Modelltest {ROMAN}"))
    theme_js = st.THEME_JS.replace("__TOC__", back)
    EXTRA_HEAD = st.ANALYTICS_TAG
else:
    theme_js = st.THEME_JS.replace("__TOC__", "")
    EXTRA_HEAD = ""

page = f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
{theme_js}
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="color-scheme" content="dark">
<meta name="theme-color" content="#14181E">
<title>Goethe B1 Modelltest {ROMAN} 해설</title>
<style>{CSS}</style>
{EXTRA_HEAD}<style id="soda-dark">{st.BUTTON_CSS}</style>
</head>
<body>
<header class="cover">
<div class="brand"><img src="data:image/png;base64,{LOGO64}" alt=""><b>Sophia Deutsch Akademie</b></div>
<p class="eyebrow">SODA Lehrwerk · Goethe-Zertifikat B1</p>
<h1>Modelltest {ROMAN}</h1>
<p class="sub">해설</p>
<p class="lead">Lesen · Hören 60문항의 근거와 함정, Schreiben 모범 답안, Sprechen 진행 요령</p>
</header>
<nav class="nav" aria-label="목차"><div class="navin">{nav}<button type="button" id="hide" aria-pressed="false">정답 가리기</button></div></nav>
<main>{body_html}</main>
<footer class="foot"><span>© Sophia Deutsch Akademie · Goethe B1 Modelltest {ROMAN} 해설</span><a href="#top" onclick="scrollTo(0,0);return false">위로</a></footer>
<script>
(function(){{
  var b=document.getElementById('hide'), d=document.body;
  b.addEventListener('click',function(){{
    var on=!d.classList.contains('hide'); d.classList.toggle('hide',on); b.setAttribute('aria-pressed',on?'true':'false');
    b.textContent=on?'정답 보기':'정답 가리기';
    document.querySelectorAll('.card.open').forEach(function(c){{c.classList.remove('open');}});
  }});
  document.addEventListener('click',function(ev){{
    if(!d.classList.contains('hide')) return;
    var c=ev.target.closest('.card'); if(c && !ev.target.closest('a')) c.classList.add('open');
  }});
}})();
</script>
</body>
</html>
"""
open(OUT, "w", encoding="utf-8").write(page)
print(OUT, os.path.getsize(OUT), "bytes,", len(cps), "glyphs")
