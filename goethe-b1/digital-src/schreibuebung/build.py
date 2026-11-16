#!/usr/bin/env python3
"""Goethe-Zertifikat B1 Modelltest N 작문 연습 — 단일 HTML 빌드.

python3 -I build.py <app-folder> <N> <font.ttf> <out.html> [web]
작문 연습 데이터: swN.py (형식은 FORMAT.md), 모든 회차가 함께 쓰는 글: gemeinsam.py
과제 원문은 ../data/mtN.json, 과제 제목·방명록 글 해석·Leitpunkt 번역은 ../erklaerung/erkN_hoeren.py에서 가져옵니다.
web: 저장소용 — 시험 페이지로 돌아가는 버튼, 접속 집계 태그, 학습 포탈 학습 저장(sync.js)을 넣습니다.
     없으면 학생에게 파일로 주는 오프라인판입니다(제출하기는 그대로 됩니다).

빌드 전에 검사합니다(어긋나면 멈춤): 과제 수, 번호마다 필요한 칸, {…} 짝, B1 예시의 단어 수(쓰기 가이드 기준),
호칭 다음 줄의 소문자, 한국어 글의 어조(‘~다’ 체·반말).
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
S = D["schreiben"]["tasks"]
G = importlib.import_module("gemeinsam")
AUF = importlib.import_module(f"sw{N}").AUFGABEN


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ERK = _load(os.path.join(APP, "digital-src", "erklaerung", f"erk{N}_hoeren.py"), f"erk{N}_hoeren").SCHREIBEN["tasks"]
st = _load(os.path.join(APP, "..", "tools", "soda-theme.py"), "sodatheme")

e = html.escape
CIRC = "①②③④⑤⑥⑦⑧⑨"
TITLE = f"Goethe B1 Modelltest {ROMAN} 작문 연습"


def plain(t):
    return t.replace("{", "").replace("}", "")


def words(t):
    return len(t.split())


def ko(t):
    """한국어 글 속의 «…»를 독일어 조각으로 표시합니다."""
    return re.sub(r"«(.+?)»", lambda m: f'<b class="de" lang="de">{m.group(1)}</b>', e(t))


def marked(t):
    """B1 예시의 {…}를 강조로 바꿉니다."""
    return re.sub(r"\{(.+?)\}", lambda m: f"<mark>{m.group(1)}</mark>", e(t))


# ---------- 검사 ----------
CAP_OK = {"Sie", "Ihnen", "Ihr", "Ihre", "Ihren", "Ihrem", "Ihrer", "Ihres", "Entschuldigung"}
BAD_END = re.compile(r"(?<![니까])다[.!]?$")
BANMAL = re.compile(r"(?:한다|했다|이다|있다|없다|된다|않는다|하자|해라|이야|거야)[.!]?$")


def tone(text, where):
    for s in re.split(r"(?<=[.!?])\s+", text.strip()):
        s = re.sub(r"«.+?»", "", s).strip()
        if s and (BAD_END.search(s) or BANMAL.search(s)):
            sys.exit(f"{where}: ‘~다’ 체나 반말로 끝나는 문장: {s}")


if len(AUF) != 3 or len(S) != 3:
    sys.exit("과제는 Aufgabe 1–3, 세 개여야 합니다")
for no, a in enumerate(AUF, 1):
    where = f"Modelltest {N} Aufgabe {no}"
    tone(a["ko"], where + " ko")
    for s in a["sum"]:
        tone(s, where + " sum")
    parts = [p for p in a["parts"] if "fix" not in p]
    if not 3 <= len(parts) <= len(CIRC):
        sys.exit(f"{where}: 고쳐 쓸 번호가 {len(parts)}개입니다")
    for i, p in enumerate(parts, 1):
        for key in ("role", "a2", "use", "use_ko", "tip", "b1"):
            if not p.get(key):
                sys.exit(f"{where} {CIRC[i - 1]}: {key}가 없습니다")
        if p["b1"].count("{") != p["b1"].count("}") or "{" not in p["b1"] or re.search(r"\{[^}]*\{", p["b1"]):
            sys.exit(f"{where} {CIRC[i - 1]}: b1의 {{…}} 짝이 맞지 않습니다: {p['b1']}")
        tone(p["tip"], f"{where} {CIRC[i - 1]} tip")
        # 주어진 표현의 낱말이 예시에 들어 있는지(순서와 어미 변화는 보지 않음)
        bag = set(re.findall(r"[\wäöüÄÖÜß]+", plain(p["b1"]).lower()))
        need = [w for w in re.findall(r"[\wäöüÄÖÜß]+", p["use"].lower()) if w not in ("sein",)]
        # 분리동사의 zu(auszuprobieren)는 낱말 안에 들어 있으면 됩니다
        miss = [w for w in need if w not in bag and not (w == "zu" and any("zu" in x for x in bag))]
        if miss:
            print(f"  알림 {where} {CIRC[i - 1]}: 표현의 낱말이 예시에 없습니다: {miss}", file=sys.stderr)
    seq = a["parts"]
    for x, p in enumerate(seq[:-1]):
        head = p.get("fix") or (p.get("b1") if p.get("short") else None)
        if head and plain(head).rstrip().endswith(","):
            nxt = seq[x + 1]
            for key in ("a2", "b1"):
                t = plain(nxt.get(key, ""))
                # 명사와 존칭(Sie, Ihr …)은 호칭 다음 줄에서도 대문자입니다
                if t and not t[0].islower() and t.split()[0].strip(",.!?:") not in CAP_OK:
                    sys.exit(f"{where}: 호칭 다음 줄은 소문자로 시작합니다: {t[:30]}")
    total = sum(words(p.get("fix") or plain(p["b1"])) for p in a["parts"])
    lo, hi = G.RANGE[no]
    if not lo <= total <= hi:
        sys.exit(f"{where}: B1 예시 {total}단어, 범위 {lo}~{hi}를 벗어났습니다")


# ---------- 글의 짜임(줄·문단) ----------
def layout(no, parts):
    """파트를 줄과 문단으로 묶습니다. tight: 앞 줄에 바로 붙는 줄(끝인사 다음의 이름)."""
    out, cur, n = [], None, 0
    for p in parts:
        if "fix" in p:
            out.append({"line": True, "tight": bool(out and out[-1].get("gruss")), "items": [{"fix": p["fix"]}]})
            cur = None
            continue
        n += 1
        item = {"k": f"{no}-{n}", "n": CIRC[n - 1]}
        if p.get("short"):
            out.append({"line": True, "gruss": p["role"] == "끝인사", "items": [item]})
            cur = None
            continue
        g = G.PARA.get(p["role"], 0) if no in (1, 2) else 0
        if cur is None or cur["g"] != g:
            cur = {"g": g, "items": []}
            out.append(cur)
        cur["items"].append(item)
    return out


def render(lay, parts, kind):
    """kind: a2(번호 붙은 A2 답안) 또는 b1(강조 붙은 B1 예시)."""
    by = {}
    n = 0
    for p in parts:
        if "fix" not in p:
            n += 1
            by[CIRC[n - 1]] = p
    html_out, text_out = [], []
    for b in lay:
        hs, ts = [], []
        for it in b["items"]:
            if "fix" in it:
                hs.append(e(it["fix"]))
                ts.append(it["fix"])
                continue
            p = by[it["n"]]
            if kind == "a2":
                hs.append(f'<span class="pn">{CIRC.index(it["n"]) + 1}</span>{e(p["a2"])}')
                ts.append(p["a2"])
            else:
                hs.append(marked(p["b1"]))
                ts.append(plain(p["b1"]))
        h, t = " ".join(hs), " ".join(ts)
        if b.get("tight") and html_out:
            html_out[-1] = html_out[-1][:-4] + "\n" + h + "</p>"
            text_out[-1] += "\n" + t
        else:
            cls = ' class="gr"' if b.get("line") else ""
            html_out.append(f"<p{cls}>{h}</p>")
            text_out.append(t)
    return "".join(html_out), "\n\n".join(text_out)


# ---------- 조각 ----------
def task_box(no, t, erk):
    out = "".join(f"<p>{e(x)}</p>" for x in t["situation"])
    if t["points"]:
        out += '<ul class="dots">' + "".join(f"<li>{e(x)}</li>" for x in t["points"]) + "</ul>"
    if t.get("post"):
        po = t["post"]
        out += (f'<div class="post"><p class="ph"><b>{e(po.get("label", ""))}</b>{e(po.get("site", ""))}</p>'
                f'<p class="pa">{e(po.get("author", ""))}</p><p>{e(po["text"])}</p></div>')
    out += f"<p>{e(t['instruction'])}</p>"
    box = f'<div class="box" lang="de"><h5 lang="ko">과제 <small>시험지 13쪽</small></h5>{out}</div>'
    if no == 1:
        box += ('<ol class="lpko">' + "".join(f'<li><b>{i}</b><span>{e(x[1])}</span></li>' for i, x in enumerate(erk["points"], 1))
                + "</ol>")
    if erk.get("post_ko"):
        box += f'<details class="pk"><summary>방명록 글 해석</summary><p>{e(erk["post_ko"])}</p></details>'
    return box


def part_card(no, i, p):
    k = f"{no}-{i}"
    short = bool(p.get("short"))
    lines = 1 if short else max(2, -(-len(plain(p["b1"])) // 52) + 1)
    ta_cls = "ans short" if short else "ans"
    rows = 1 if short else 3
    return f"""<li class="part" id="p{k}">
<div class="ph"><span class="pn">{i}</span><span class="role">{e(p["role"])}</span><span class="ok">✓ 작성</span></div>
<div class="a2s"><span class="lab">A2</span><p lang="de">{e(p["a2"])}</p></div>
<div class="use"><span class="lab">쓸 표현</span><span class="ux" lang="de">{e(p["use"])}</span><em>{e(p["use_ko"])}</em></div>
<p class="hint">{ko(p["tip"])}</p>
<textarea class="{ta_cls}" data-k="{k}" rows="{rows}" lang="de" spellcheck="false" autocapitalize="off" autocomplete="off" autocorrect="off" aria-label="{i}번 B1 문장" placeholder="B1 문장으로 고쳐 쓰십시오"></textarea>
<div class="pv" lang="de"></div><div class="pl" aria-hidden="true">{"<i></i>" * lines}</div>
<div class="pbar"><button class="sbtn exb" type="button" aria-expanded="false" aria-controls="x{k}">예시 보기</button></div>
<div class="ex" id="x{k}" hidden><span class="lab">B1 예시</span><p lang="de">{marked(p["b1"])}</p></div>
</li>"""


sections, data_aufg = [], []
for no, (a, t, erk) in enumerate(zip(AUF, S, ERK), 1):
    parts = [p for p in a["parts"] if "fix" not in p]
    lay = layout(no, a["parts"])
    a2_html, a2_text = render(lay, a["parts"], "a2")
    b1_html, b1_text = render(lay, a["parts"], "b1")
    fixes = [p["fix"].replace("\n", " ") for p in a["parts"] if "fix" in p]
    if no == 1:
        frame = f"호칭(«{fixes[0]}»)과 끝인사(«{fixes[-1]}»)는 그대로 둡니다. 번호가 붙은 부분만 고쳐 씁니다."
    elif no == 2:
        frame = "의견 글이므로 호칭과 끝인사가 없습니다. 번호마다 고쳐 쓴 문장이 차례대로 이어져 글 한 편이 됩니다."
    else:
        frame = f"호칭과 끝인사도 고쳐 씁니다. 이름(«{fixes[-1]}»)은 그대로 둡니다."
    cards = "".join(part_card(no, i, p) for i, p in enumerate(parts, 1))
    chk = "".join(f"<li><span>{ko(x)}</span></li>" for x in G.CHECK[no])
    summ = "".join(f"<li>{ko(x)}</li>" for x in a["sum"])
    lo, hi = G.RANGE[no]
    sections.append(f"""<section id="w{no}" class="aufg" data-a="{no}">
<h2><small>Aufgabe {no} · 약 {t["words"]}단어 · {t["minutes"]}분</small>{e(erk["title"])}</h2>
<p class="kind">{e(G.KIND[no])}</p>
<p class="intro">{e(a["ko"])}</p>
{task_box(no, t, erk)}
<h3 class="sub3">A2 답안 <span class="cnt">{words(a2_text)}단어</span></h3>
<div class="a2l" lang="de">{a2_html}</div>
<h3 class="sub3">B1로 고쳐 쓰기 <span class="prog" id="prog{no}">작성 0 / {len(parts)}</span></h3>
<p class="frame">{ko(frame)}</p>
<ol class="parts">{cards}</ol>
<details class="mine" id="mine{no}"><summary>내 글 전체 <span class="wc">0단어</span><small>목표 약 {G.TARGET[no]}단어 ({lo}–{hi})</small></summary>
<div class="ml" lang="de"></div>
<div class="acts"><button class="sbtn cp" type="button" data-a="{no}">이 글 복사</button></div>
<h5>제출 전 확인</h5><ul class="chk">{chk}</ul></details>
<details class="b1f"><summary>B1 예시 답안 전체 <span class="wc ok">{words(b1_text)}단어</span><small>A2 답안 {words(a2_text)}단어</small></summary>
<div class="ml" lang="de">{b1_html}</div></details>
<h4 class="sub3 sumh">A2 → B1, 이렇게 바뀌었습니다</h4>
<ul class="dots sum">{summ}</ul>
</section>""")
    data_aufg.append({
        "no": no, "title": erk["title"], "target": G.TARGET[no], "lo": lo, "hi": hi,
        "layout": [{"line": bool(b.get("line")), "tight": bool(b.get("tight")),
                    "items": [({"fix": it["fix"]} if "fix" in it else {"k": it["k"], "n": it["n"]}) for it in b["items"]]}
                   for b in lay],
        "parts": [{"k": f"{no}-{i}", "n": CIRC[i - 1], "role": p["role"], "a2": p["a2"], "use": p["use"]} for i, p in enumerate(parts, 1)],
    })

steps = "".join(f"<li><b>{e(a)}</b>{e(b)}</li>" for a, b in G.STEPS)
diff = "".join(f'<li><b>{e(a)}</b><div class="d2"><small>A2</small>{ko(b)}</div><div class="d1"><small>B1</small>{ko(c)}</div></li>'
               for a, b, c in G.DIFF)
save_note = ("쓴 내용은 이 브라우저에 저절로 저장됩니다. 학습 포탈에 로그인한 상태라면 다른 기기에서도 이어서 쓸 수 있습니다."
             if WEB else "쓴 내용은 이 브라우저에 저절로 저장됩니다. 파일을 다른 곳으로 옮기면 저장한 내용이 이어지지 않을 수 있습니다.")
HOW = f"""<section id="how"><h2><small>Schreibübung</small>이렇게 연습합니다</h2>
<ol class="steps">{steps}</ol>
<h3>{e(G.DIFF_TITLE)}</h3>
<ul class="diff">{diff}</ul>
<p class="note">{e(G.DIFF_NOTE)}</p>
<p class="save">{e(save_note)}</p></section>"""

SUB = f"""<section id="sub"><h2><small>Abgabe</small>제출과 보관</h2>
<div class="subbox"><h3>{e(G.SUBMIT_TITLE)}<em>{e(G.SUBMIT_TAG)}</em></h3>
{"".join(f"<p>{x}</p>" for x in G.SUBMIT_TEXT)}
<p class="sc">작성: <span id="subcnt"></span></p>
<label>이름 <input id="subName" type="text" maxlength="60" autocomplete="name"></label>
<div class="acts"><button class="btn" id="sb" type="button">선생님께 제출하기</button><span class="st" id="subSt" role="status"></span></div></div>
<div class="acts keep"><button class="sbtn" id="cpall" type="button">전체 복사</button><button class="sbtn" id="dl" type="button">txt 저장</button><button class="sbtn" id="reset" type="button">쓴 내용 모두 지우기</button></div>
</section>"""

# 제출 주소: 디지털 시험 화면(template.html)과 같은 주소를 씁니다. tools/set-submit-url.py가 이 파일들도 함께 바꿉니다.
tpl = open(os.path.join(APP, "digital-src", "template.html"), encoding="utf-8").read()
m = re.search(r"var SUBMIT_URL = '([^']*)';", tpl)
SUBMIT_URL = m.group(1) if m else ""

APPJS = open(os.path.join(HERE, "app.js"), encoding="utf-8").read().replace("var SUBMIT_URL = '__SUBMIT_URL__';", f"var SUBMIT_URL = '{SUBMIT_URL}';")
if f"var SUBMIT_URL = '{SUBMIT_URL}';" not in APPJS:
    sys.exit("app.js에서 SUBMIT_URL 줄을 찾지 못했습니다")
DATA = json.dumps({"mt": str(N), "roman": ROMAN, "title": TITLE, "aufg": data_aufg}, ensure_ascii=False).replace("</", "<\\/")

NAV = [("how", "사용법"), ("w1", "Aufgabe 1"), ("w2", "Aufgabe 2"), ("w3", "Aufgabe 3"), ("sub", "제출")]
nav = "".join(f'<a href="#{a}">{b}</a>' for a, b in NAV)
body_html = HOW + "".join(sections) + SUB

if WEB:
    back = (st.TOC_JS.replace("__HREF__", f"index.html#{N}").replace("목차로 돌아가기", f"Modelltest {ROMAN} 페이지로 돌아가기")
            .replace("</svg>목차", f"</svg>Modelltest {ROMAN}"))
    theme_js = st.SYNC_TAG + "\n" + st.THEME_JS.replace("__TOC__", back)
    EXTRA_HEAD = st.ANALYTICS_TAG
else:
    theme_js = st.THEME_JS.replace("__TOC__", "")
    EXTRA_HEAD = ""

CSS = (open(os.path.join(HERE, "..", "erklaerung", "style.css"), encoding="utf-8").read()
       + open(os.path.join(HERE, "style.css"), encoding="utf-8").read())
LOGO64 = base64.b64encode(open(os.path.join(APP, "digital-src", "logo-small.png"), "rb").read()).decode()


def page(font64):
    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
{theme_js}
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="color-scheme" content="dark">
<meta name="theme-color" content="#14181E">
<title>{TITLE}</title>
<style>{CSS.replace("__FONT__", font64)}</style>
{EXTRA_HEAD}<style id="soda-dark">{st.BUTTON_CSS}</style>
</head>
<body>
<header class="cover">
<div class="brand"><img src="data:image/png;base64,{LOGO64}" alt=""><b>Sophia Deutsch Akademie</b></div>
<p class="eyebrow">SODA Lehrwerk · Goethe-Zertifikat B1</p>
<h1>Modelltest {ROMAN}</h1>
<p class="sub">작문 연습</p>
<p class="lead">{e(G.LEAD)}</p>
</header>
<nav class="nav" aria-label="목차"><div class="navin">{nav}<button type="button" id="exall" aria-pressed="false">예시 모두 보기</button></div></nav>
<main>{body_html}</main>
<footer class="foot"><span>© Sophia Deutsch Akademie · {TITLE}</span><a href="#top" onclick="scrollTo(0,0);return false">위로</a></footer>
<div class="toast" id="toast" role="status" hidden></div>
<script type="application/json" id="sw-data">{DATA}</script>
<script>{APPJS}</script>
</body>
</html>
"""


draft = page("")
# 글꼴: 화면에 쓰는 글자, 스크립트 안내 문구, 학생이 칠 독일어 글자(라틴 문자와 문장 부호)
chars = set(draft)
from fontTools import subset  # noqa: E402
from fontTools.ttLib import TTFont  # noqa: E402
cps = set(range(0x20, 0x7F)) | set(range(0xA0, 0x180)) | {0x2013, 0x2014, 0x2018, 0x2019, 0x201A, 0x201C, 0x201D, 0x201E,
                                                          0x2026, 0x20AC, 0x2022, 0x2192, 0x25B8, 0x25BE, 0x25A1, 0x2713}
cps |= {ord(c) for c in chars if ord(c) >= 0x20}
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
out = page(base64.b64encode(buf.getvalue()).decode())
if "_" in os.path.basename(OUT):
    sys.exit("파일 이름에 밑줄(_)을 쓰지 않습니다")
open(OUT, "w", encoding="utf-8").write(out)
print(OUT, os.path.getsize(OUT), "bytes,", len(cps), "glyphs")
