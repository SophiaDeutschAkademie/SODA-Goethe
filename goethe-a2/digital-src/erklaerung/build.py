#!/usr/bin/env python3
"""Goethe-Zertifikat A2 Modelltest N 해설 — 단일 HTML 빌드.

python3 -I build.py <app-folder> <N> <font.ttf> <out.html> [web]
해설 데이터: erkN_lesen.py, erkN_hoeren.py (형식은 FORMAT.md)
web: 저장소용 — 그림은 img/ 경로로 연결하고, 시험 페이지로 돌아가는 버튼과 접속 집계 태그를 넣습니다.
web이 없으면 그림을 파일 안에 넣은 오프라인판을 만듭니다.
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
_l = importlib.import_module(f"erk{N}_lesen")
_h = importlib.import_module(f"erk{N}_hoeren")
LESEN1, LESEN2, LESEN3, LESEN4 = _l.LESEN1, _l.LESEN2, _l.LESEN3, _l.LESEN4
HOEREN1, HOEREN2, HOEREN3, HOEREN4, SCHREIBEN, SPRECHEN = (_h.HOEREN1, _h.HOEREN2, _h.HOEREN3, _h.HOEREN4,
                                                           _h.SCHREIBEN, _h.SPRECHEN)
L, H, S = D["lesen"], D["hoeren"], D["schreiben"]

spec = importlib.util.spec_from_file_location("sodatheme", os.path.join(APP, "..", "tools", "soda-theme.py"))
st = importlib.util.module_from_spec(spec)
spec.loader.exec_module(st)

e = html.escape


def de(s):
    return f'<span lang="de">{e(s)}</span>'


def src(path):
    if WEB:
        return path
    ext = os.path.splitext(path)[1].lower()
    mime = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}[ext]
    return f"data:{mime};base64," + base64.b64encode(open(os.path.join(APP, path), "rb").read()).decode()


# ---------- 검사 ----------
def key(items):
    return {i["no"]: i["answer"] for i in items}


H2_ITEMS = [p for p in H["t2"]["persons"] if p["no"] != "0"]
checks = [("Lesen 1", LESEN1, key(L["t1"]["items"])), ("Lesen 2", LESEN2, key(L["t2"]["items"])),
          ("Lesen 3", LESEN3, key(L["t3"]["items"])), ("Lesen 4", LESEN4, key(L["t4"]["items"])),
          ("Hören 1", HOEREN1, key(H["t1"]["items"])), ("Hören 2", HOEREN2, key(H2_ITEMS)),
          ("Hören 3", HOEREN3, key(H["t3"]["items"])), ("Hören 4", HOEREN4, key(H["t4"]["items"]))]
for name, mine, ref in checks:
    got = {i["no"]: i["ans"] for i in mine["items"]}
    if got != ref:
        sys.exit(f"{name} 정답 불일치: {got} != {ref}")


def need(text, quotes, where):
    for q, _ in quotes:
        if q not in text:
            sys.exit(f"{where}: 원문에 없는 인용: {q[:70]}")


t1 = L["t1"]
art = " ".join([t1.get("title", ""), t1.get("lead", ""), " ".join(t1["paragraphs"]), t1.get("quote", "")])
board = " ".join(r["floor"] + " " + r["text"] for r in L["t2"]["board"]["rows"])
m = L["t3"]["mail"]
mail = " ".join([m.get("subject", ""), m.get("greeting", ""), " ".join(m["paragraphs"]), " ".join(m.get("closing", []))])
ads = " ".join(a["alt"] for a in L["t4"]["ads"].values())
for it in LESEN1["items"]:
    need(art, it["basis"], f"Lesen {it['no']}")
for it in LESEN2["items"]:
    need(board, it["basis"], f"Lesen {it['no']}")
for it in LESEN3["items"]:
    need(mail, it["basis"], f"Lesen {it['no']}")
for it in LESEN4["items"]:
    need(ads, it["basis"], f"Lesen {it['no']}")
paras = [S["tasks"][k]["model"]["text"].split("\n\n") for k in (0, 1)]
for k in (0, 1):
    if len(paras[k]) != len(SCHREIBEN["tasks"][k]["model_ko"]):
        sys.exit(f"Schreiben {k + 1}: model_ko {len(SCHREIBEN['tasks'][k]['model_ko'])}개, 모범 답안 문단 {len(paras[k])}개")


# ---------- 조각 ----------
def quotes(basis):
    return "".join(f'<blockquote><p class="q">{de(q)}</p><p class="tr">{e(ko)}</p></blockquote>' for q, ko in basis)


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


def section(sid, small, title, intro, tipt):
    return (f'<section id="{sid}"><h2><small>{small}</small>{title}</h2>'
            + (f'<p class="intro">{e(intro)}</p>' if intro else "") + tip(tipt))


# ---------- Lesen ----------
p = [section("l1", "Lesen", f'Teil 1 · 신문 기사 <span lang="de">„{e(t1["title"])}“</span>', LESEN1.get("intro"), LESEN1["tip"])]
for it, q in zip(LESEN1["items"], L["t1"]["items"]):
    head = f'<p class="pick">{de(q["stem"])}</p>'
    p.append(card(it["no"], f'<b>{it["ans"]}</b>', head,
                  quotes(it["basis"]) + f'<p>{e(it["why"])}</p>' + opts(q["options"], it["ans"], it.get("wrong", {})) + vocab(it.get("vocab"))))
SEC_L1 = "".join(p) + "</section>"

bd = L["t2"]["board"]
btab = ('<table class="tbl board"><tbody>' + "".join(f'<tr><td lang="de">{e(r["floor"])}</td><td lang="de">{e(r["text"])}</td></tr>' for r in bd["rows"])
        + "</tbody></table>")
p = [section("l2", "Lesen", f'Teil 2 · 안내판 <span lang="de">{e(bd.get("title", ""))}</span>', LESEN2.get("intro"), LESEN2["tip"]),
     f'<details class="full"><summary>안내판 전체 보기</summary><div class="letter">{btab}</div></details>']
for it, q in zip(LESEN2["items"], L["t2"]["items"]):
    head = f'<p class="pick">{de(q["stem"])}</p><p class="tr">{e(it["stko"])}</p>'
    p.append(card(it["no"], f'<b>{it["ans"]}</b><i lang="de">{e(q["options"][it["ans"]])}</i>', head,
                  quotes(it["basis"]) + f'<p>{e(it["why"])}</p>' + opts(q["options"], it["ans"], it.get("wrong", {}))))
SEC_L2 = "".join(p) + "</section>"

p = [section("l3", "Lesen", f'Teil 3 · 이메일 <span lang="de">„{e(m.get("subject", ""))}“</span>', LESEN3.get("intro"), LESEN3["tip"])]
for it, q in zip(LESEN3["items"], L["t3"]["items"]):
    head = f'<p class="pick">{de(q["stem"])}</p>'
    p.append(card(it["no"], f'<b>{it["ans"]}</b>', head,
                  quotes(it["basis"]) + f'<p>{e(it["why"])}</p>' + opts(q["options"], it["ans"], it.get("wrong", {})) + vocab(it.get("vocab"))))
SEC_L3 = "".join(p) + "</section>"

t4 = L["t4"]
adgrid = '<div class="ads">' + "".join(f'<figure><figcaption>{k}</figcaption><img src="{src(a["img"])}" alt="{e(a["alt"])}" loading="lazy"></figure>'
                                       for k, a in t4["ads"].items()) + "</div>"
p = [section("l4", "Lesen", "Teil 4 · 광고 고르기", LESEN4.get("intro"), LESEN4["tip"]),
     f'<details class="full" open><summary>광고 a–f</summary>{adgrid}</details>']
for it, q in zip(LESEN4["items"], t4["items"]):
    head = f'<p class="pick">{de(q["text"])}</p><p class="tr">{e(it["stko"])}</p><p class="cond"><b>조건</b>{e(it["cond"])}</p>'
    p.append(card(it["no"], f'<b>{it["ans"]}</b>', head, quotes(it["basis"]) + f'<p>{e(it["why"])}</p>' + trap(it.get("trap"))))
p.append(f'<p class="note">{e(LESEN4["unused"])}</p>')
SEC_L4 = "".join(p) + "</section>"


# ---------- Hören ----------
def hsec(sid, k, data, times):
    return section(sid, "Hören", f"Teil {k} · {e(data['title'])} ({times})", data.get("intro"), data["tip"])


p = [hsec("h1", 1, HOEREN1, "각 2회")]
for it, q in zip(HOEREN1["items"], H["t1"]["items"]):
    head = f'<p class="pick">{de(q["stem"])}</p><p class="tr">{e(it["stko"])}</p>'
    p.append(card(it["no"], f'<b>{it["ans"]}</b>', head,
                  '<h6>들은 내용</h6>' + quotes(it["basis"]) + f'<p>{e(it["why"])}</p>' + opts(q["options"], it["ans"], it.get("wrong", {}))))
SEC_H1 = "".join(p) + "</section>"

pics = H["t2"]["pictures"]
answers = {pp["answer"] for pp in H["t2"]["persons"]}
pgrid = '<div class="pics">' + "".join(
    f'<figure class="{"" if k in answers else "un"}"><img src="{src(v["img"])}" alt="{e(v["alt"])}" loading="lazy"><figcaption><b>{k}</b><span lang="de">{e(v["alt"])}</span></figcaption></figure>'
    for k, v in pics.items()) + "</div>"
ex = next(pp for pp in H["t2"]["persons"] if pp["no"] == "0")
p = [hsec("h2", 2, HOEREN2, "1회"),
     f'<details class="full" open><summary>그림 a–i <small>(흐린 그림 = 아무도 고르지 않는 그림, 예시 0: {e(ex["name"])} → {ex["answer"]})</small></summary>{pgrid}</details>']
for it, q in zip(HOEREN2["items"], H2_ITEMS):
    a = pics[it["ans"]]
    head = (f'<p class="pick">{de(q["name"])}</p>'
            f'<div class="pics one rv"><figure class="ok"><img src="{src(a["img"])}" alt="{e(a["alt"])}" loading="lazy"><figcaption><b>{it["ans"]}</b><span lang="de">{e(a["alt"])}</span></figcaption></figure></div>')
    p.append(card(it["no"], f'<b>{it["ans"]}</b>', head, '<h6>들은 내용</h6>' + quotes(it["basis"]) + f'<p>{e(it["why"])}</p>' + trap(it.get("trap"))))
SEC_H2 = "".join(p) + "</section>"

p = [hsec("h3", 3, HOEREN3, "1회")]
for it, q in zip(HOEREN3["items"], H["t3"]["items"]):
    figs = "".join(f'<figure class="{"ok" if k == it["ans"] else ""}"><img src="{src(v["img"])}" alt="{e(v["alt"])}" loading="lazy">'
                   f'<figcaption><b>{k}</b><span lang="de">{e(v["alt"])}</span></figcaption></figure>' for k, v in q["options"].items())
    wrong = it.get("wrong", {})
    wl = "".join(f'<li><b>{k}</b> {e(t)}</li>' for k, t in wrong.items())
    head = f'<p class="pick">{de(q["stem"])}</p><p class="tr">{e(it["stko"])}</p><div class="pics three">{figs}</div>'
    p.append(card(it["no"], f'<b>{it["ans"]}</b>', head, '<h6>들은 내용</h6>' + quotes(it["basis"]) + f'<p>{e(it["why"])}</p>'
                  + (f'<ul class="dots">{wl}</ul>' if wl else "")))
SEC_H3 = "".join(p) + "</section>"

p = [hsec("h4", 4, HOEREN4, "2회")]
if H["t4"].get("context"):
    p.append(f'<p class="intro" lang="de">{e(H["t4"]["context"])}</p>')
for it, q in zip(HOEREN4["items"], H["t4"]["items"]):
    head = f'<p class="pick">{de(q["text"])}</p><p class="tr">{e(it["stko"])}</p>'
    p.append(card(it["no"], f'<b class="jn">{e(it["ans"])}</b>', head, '<h6>들은 내용</h6>' + quotes(it["basis"]) + f'<p>{e(it["why"])}</p>'))
SEC_H4 = "".join(p) + "</section>"


# ---------- Schreiben ----------
def _tbl(rows):
    return '<table class="tbl"><tbody>' + "".join(f'<tr><td lang="de">{e(a)}</td><td>{e(b)}</td></tr>' for a, b in rows) + "</tbody></table>"


def _em(t):
    return re.sub(r"\*(.+?)\*", r"<em>\1</em>", e(t))


blocks = [f'<section id="w"><h2><small>Schreiben</small>쓰기 · Aufgabe 1과 2</h2><p class="intro">{e(SCHREIBEN["intro"])}</p>']
for t, mine, ps in zip(S["tasks"], SCHREIBEN["tasks"], paras):
    model = "".join(f'<div class="mrow"><span class="lp"></span><p lang="de">{e(x).replace(chr(10), "<br>")}</p><p class="tr">{e(k)}</p></div>'
                    for x, k in zip(ps, mine["model_ko"]))
    task_de = "".join(f"<p>{e(x)}</p>" for x in t["situation"]) + '<ul class="dots">' + "".join(f"<li>{e(x)}</li>" for x in t["points"]) + f"</ul><p>{e(t['instruction'])}</p>"
    lps = "".join(f'<li><span class="n">{i}</span><div><p lang="de">{e(a)}</p><p class="tr">{e(b)}</p><p class="ex" lang="de">{e(c)}</p></div></li>'
                  for i, (a, b, c) in enumerate(mine["points"], 1))
    blocks.append(f"""<h3 class="task">Aufgabe {t["no"]} · {e(mine["title"])} <small>{t["words"][0]}–{t["words"][1]}단어 · 약 {t["minutes"]}분</small></h3>
<p class="lead2">{e(mine["situation"])}</p>
<div class="box" lang="de"><h5>과제</h5>{task_de}</div>
<h4 class="sub3">세 가지 내용과 쓸 수 있는 문장</h4><ol class="lps">{lps}</ol>
<h4 class="sub3">자주 하는 실수</h4><ul class="dots">{"".join(f"<li>{e(x)}</li>" for x in mine["traps"])}</ul>
<h4 class="sub3">모범 답안 <small lang="de">{e(t["model"].get("label", ""))}</small></h4><div class="model">{model}</div>
<h4 class="sub3">쓸 수 있는 표현</h4>{_tbl(mine["redemittel"])}""")
good = "".join(f'<tr><th lang="de">{e(g["label"])}</th><td lang="de">{_em(g["text"])}</td></tr>' for g in S.get("good", []))
blocks.append(f"""<h3>채점 기준</h3><table class="tbl crit"><tbody>{"".join(f'<tr><th>{e(a)}</th><td><span lang="de">{e(b)}</span><br>{e(c)}</td></tr>' for a, b, c in SCHREIBEN["criteria"])}</tbody></table>
{f'<h4 class="sub3">좋은 답안의 조건 <small>(시험지 18쪽)</small></h4><table class="tbl"><tbody>{good}</tbody></table>' if good else ""}
<p class="note">{e(SCHREIBEN["criteria_note"])}</p></section>""")
SEC_W = "".join(blocks)


# ---------- Sprechen ----------
def rm(rows):
    return _tbl(rows)


sp = SPRECHEN


def _sp_part(k, name, t):
    out = f'<h3>Teil {k} · <span lang="de">{e(name)}</span></h3><p class="lead2">{e(t["task"])}</p>'
    if t.get("a") and t.get("b"):
        out += (f'<div class="two"><div class="box"><h5>{e(t.get("a_label", "A"))}</h5><p>{e(t["a"])}</p></div>'
                f'<div class="box"><h5>{e(t.get("b_label", "B"))}</h5><p>{e(t["b"])}</p></div></div>')
    if t.get("steps"):
        out += '<ol class="steps">' + "".join(f'<li><b lang="de">{e(a)}</b><span>{e(b)}</span></li>' for a, b in t["steps"]) + "</ol>"
    if t.get("points"):
        out += '<ul class="dots">' + "".join(f"<li>{e(x)}</li>" for x in t["points"]) + "</ul>"
    return out + rm(t["redemittel"])


SEC_M = (f'<section id="m"><h2><small>Sprechen</small>말하기 · {e(sp["head"])}</h2>'
         + "".join(_sp_part(k, n, sp[f"t{k}"]) for k, n in zip((1, 2, 3), sp["names"]))
         + f'<p class="note">{e(sp["note"])}</p></section>')


# ---------- 정답표 ----------
def krow(label, href, items):
    cells = "".join(f'<a href="#a{n}"><span>{n}</span><b>{e(a)}</b></a>' for n, a in items)
    return f'<div class="krow"><h4><a href="{href}">{label}</a></h4><div class="kc">{cells}</div></div>'


def ks(items):
    return [(i["no"], i["answer"]) for i in items if i["no"] != "0"]


KEY = ('<section id="key"><h2><small>Lösungsschlüssel</small>정답표</h2><p class="intro">번호를 누르면 해설로 이동합니다. Lesen과 Hören은 번호가 각각 1번부터 시작합니다.</p>'
       + krow("Lesen Teil 1", "#l1", ks(L["t1"]["items"])) + krow("Lesen Teil 2", "#l2", ks(L["t2"]["items"]))
       + krow("Lesen Teil 3", "#l3", ks(L["t3"]["items"])) + krow("Lesen Teil 4", "#l4", ks(L["t4"]["items"]))
       + krow("Hören Teil 1", "#h1", ks(H["t1"]["items"])).replace('href="#a', 'href="#ha') + krow("Hören Teil 2", "#h2", ks(H2_ITEMS)).replace('href="#a', 'href="#ha')
       + krow("Hören Teil 3", "#h3", ks(H["t3"]["items"])).replace('href="#a', 'href="#ha') + krow("Hören Teil 4", "#h4", ks(H["t4"]["items"])).replace('href="#a', 'href="#ha')
       + """<table class="tbl pts"><thead><tr><th>모듈</th><th>구성</th><th>점수</th></tr></thead><tbody>
<tr><td>Lesen</td><td>20문항 × 1,25점</td><td>25점</td></tr>
<tr><td>Hören</td><td>20문항 × 1,25점</td><td>25점</td></tr>
<tr><td>Schreiben</td><td>선생님 채점</td><td>25점</td></tr>
<tr><td>Sprechen</td><td>선생님 채점</td><td>25점</td></tr>
</tbody></table><p class="note">100점 만점에 60점 이상이면 합격입니다.</p></section>""")

# Lesen과 Hören 번호가 겹치므로 Hören 카드의 id는 ha1…ha20
SEC_H = SEC_H1 + SEC_H2 + SEC_H3 + SEC_H4
SEC_H = SEC_H.replace('<article class="card" id="a', '<article class="card" id="ha')

body_html = KEY + SEC_L1 + SEC_L2 + SEC_L3 + SEC_L4 + SEC_H + SEC_W + SEC_M
chars = set(body_html) | set(f"Goethe-Zertifikat A2 Modelltest {ROMAN} 해설 SODA Lehrwerk Sophia Deutsch Akademie 정답 가리기 보기 목차 정답표 위로 다크 모드 켜기 끄기 켜짐 꺼짐 누르면 라이트로 바뀌어요")
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
NAV = [("key", "정답표"), ("l1", "Lesen 1"), ("l2", "Lesen 2"), ("l3", "Lesen 3"), ("l4", "Lesen 4"),
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
<title>Goethe A2 Modelltest {ROMAN} 해설</title>
<style>{CSS}</style>
{EXTRA_HEAD}<style id="soda-dark">{st.BUTTON_CSS}</style>
</head>
<body>
<header class="cover">
<div class="brand"><img src="data:image/png;base64,{LOGO64}" alt=""><b>Sophia Deutsch Akademie</b></div>
<p class="eyebrow">SODA Lehrwerk · Goethe-Zertifikat A2</p>
<h1>Modelltest {ROMAN}</h1>
<p class="sub">해설</p>
<p class="lead">Lesen · Hören 40문항의 근거와 함정, Schreiben 모범 답안, Sprechen 진행 요령</p>
</header>
<nav class="nav" aria-label="목차"><div class="navin">{nav}<button type="button" id="hide" aria-pressed="false">정답 가리기</button></div></nav>
<main>{body_html}</main>
<footer class="foot"><span>© Sophia Deutsch Akademie · Goethe A2 Modelltest {ROMAN} 해설</span><a href="#top" onclick="scrollTo(0,0);return false">위로</a></footer>
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
