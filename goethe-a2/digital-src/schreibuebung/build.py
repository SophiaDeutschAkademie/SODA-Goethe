#!/usr/bin/env python3
"""Goethe-Zertifikat A2 Modelltest N 작문 연습 — 단일 HTML 빌드.

python3 -I build.py <app-folder> <N> <font.ttf> <out.html> [web]
작문 연습 데이터: swN.py (형식은 FORMAT.md), 모든 회차가 함께 쓰는 글: gemeinsam.py
과제 원문은 ../data/mtN.json, 과제 제목과 Punkt 번역은 ../erklaerung/erkN_hoeren.py, 시험지 쪽수는 앱 폴더의 index.html에서 가져옵니다.
web: 저장소용 — 시험 페이지로 돌아가는 버튼, 접속 집계 태그, 학습 포탈 학습 저장(sync.js)을 넣습니다.
     없으면 학생에게 파일로 주는 오프라인판입니다(제출하기는 그대로 됩니다).

빌드 전에 검사합니다(어긋나면 멈춤): 과제 수(Aufgabe 1·2), 번호마다 필요한 칸, Punkt 1–3이 차례대로 다 있는지,
{…} 짝, A2 예시의 단어 수(과제의 범위, 호칭·끝인사·이름 포함), A1 답안이 A2 예시보다 짧은지, 호칭 다음 줄의 소문자,
한국어 글의 어조(‘~다’ 체·반말).
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
TITLE = f"Goethe A2 Modelltest {ROMAN} 작문 연습"


def plain(t):
    return t.replace("{", "").replace("}", "")


def words(t):
    return len(t.split())


def ko(t):
    """한국어 글 속의 «…»를 독일어 조각으로 표시합니다."""
    return re.sub(r"«(.+?)»", lambda m: f'<b class="de" lang="de">{m.group(1)}</b>', e(t))


def marked(t):
    """A2 예시의 {…}를 강조로 바꿉니다."""
    return re.sub(r"\{(.+?)\}", lambda m: f"<mark>{m.group(1)}</mark>", e(t))


def punkt(role):
    m = re.fullmatch(r"Punkt ([1-3])", role)
    return int(m.group(1)) if m else None


def counted(p):
    """단어 수에 넣는 칸인지: Betreff 줄만 세지 않습니다(쓰기 가이드와 같음)."""
    return not ("fix" in p and p["fix"].startswith("Betreff:"))


def total(seq, key):
    return sum(words(p["fix"] if "fix" in p else plain(p[key])) for p in seq if counted(p))


def register(seq):
    first = next((p["fix"] for p in seq if "fix" in p and counted(p)), "")
    return "Sie" if first.startswith("Sehr geehrte") else "du"


# ---------- 검사 ----------
CAP_OK = {"Sie", "Ihnen", "Ihr", "Ihre", "Ihren", "Ihrem", "Ihrer", "Ihres", "Entschuldigung"}
BAD_END = re.compile(r"(?<![니까])다[.!]?$")
BANMAL = re.compile(r"(?:한다|했다|이다|있다|없다|된다|않는다|하자|해라|이야|거야)[.!]?$")
SKIP_NEED = {"sein", "sich", "etwas", "jemandem", "jemanden"}


def tone(text, where):
    for s in re.split(r"(?<=[.!?])\s+", text.strip()):
        s = re.sub(r"«.+?»", "", s).strip()
        if s and (BAD_END.search(s) or BANMAL.search(s)):
            sys.exit(f"{where}: ‘~다’ 체나 반말로 끝나는 문장: {s}")


def found(w, bag):
    """주어진 표현의 낱말이 예시에 있는지(분리동사의 zu와 어미 변화는 느슨하게 봅니다)."""
    if w in bag or (w == "zu" and any("zu" in x for x in bag)):
        return True
    stem = re.sub(r"(?:en|n)$", "", w)
    return len(stem) >= 4 and any(stem in x for x in bag)


if len(AUF) != 2 or len(S) != 2 or len(ERK) != 2:
    sys.exit("과제는 Aufgabe 1·2, 두 개여야 합니다")
for no, (a, t, erk) in enumerate(zip(AUF, S, ERK), 1):
    where = f"Modelltest {N} Aufgabe {no}"
    tone(a["ko"], where + " ko")
    for s in a["sum"]:
        tone(s, where + " sum")
    seq = a["parts"]
    parts = [p for p in seq if "fix" not in p]
    if not 3 <= len(parts) <= len(CIRC):
        sys.exit(f"{where}: 고쳐 쓸 번호가 {len(parts)}개입니다")
    if "fix" not in seq[0] or "fix" not in seq[-1]:
        sys.exit(f"{where}: 첫 칸은 호칭, 마지막 칸은 끝인사와 이름(fix)입니다")
    roles = [p.get("role", "") for p in parts]
    pk = [punkt(r) for r in roles if punkt(r)]
    if sorted(set(pk)) != [1, 2, 3] or pk != sorted(pk):
        sys.exit(f"{where}: Punkt 1–3을 차례대로 모두 씁니다: {roles}")
    odd = [r for r in roles if not punkt(r) and r not in ("도입", "마무리")]
    if odd:
        sys.exit(f"{where}: role은 Punkt 1–3, 도입, 마무리 가운데 하나입니다: {odd}")
    if len(t["points"]) != 3 or len(erk["points"]) != 3:
        sys.exit(f"{where}: 과제의 Punkt가 세 개가 아닙니다")
    for i, p in enumerate(parts, 1):
        for key in ("role", "a1", "use", "use_ko", "tip", "a2"):
            if not p.get(key):
                sys.exit(f"{where} {CIRC[i - 1]}: {key}가 없습니다")
        if p["a2"].count("{") != p["a2"].count("}") or "{" not in p["a2"] or re.search(r"\{[^}]*\{", p["a2"]):
            sys.exit(f"{where} {CIRC[i - 1]}: a2의 {{…}} 짝이 맞지 않습니다: {p['a2']}")
        if "{" in p["a1"]:
            sys.exit(f"{where} {CIRC[i - 1]}: a1에는 {{…}}를 쓰지 않습니다")
        tone(p["tip"], f"{where} {CIRC[i - 1]} tip")
        tone(p["use_ko"], f"{where} {CIRC[i - 1]} use_ko")
        bag = set(re.findall(r"[a-zäöüß]+", plain(p["a2"]).lower()))
        need = [w for w in re.findall(r"[a-zäöüß]+", p["use"].lower()) if w not in SKIP_NEED]
        miss = [w for w in need if not found(w, bag)]
        if miss:
            print(f"  알림 {where} {CIRC[i - 1]}: 표현의 낱말이 예시에 없습니다: {miss}", file=sys.stderr)
    for x, p in enumerate(seq[:-1]):
        if p.get("fix", "").rstrip().endswith(","):
            nxt = seq[x + 1]
            for key in ("a1", "a2"):
                tt = plain(nxt.get(key, ""))
                # 명사와 존칭(Sie, Ihr …)은 호칭 다음 줄에서도 대문자입니다
                if tt and not tt[0].islower() and tt.split()[0].strip(",.!?:") not in CAP_OK:
                    sys.exit(f"{where}: 호칭 다음 줄은 소문자로 시작합니다: {tt[:30]}")
    lo, hi = t["words"]
    n1, n2 = total(seq, "a1"), total(seq, "a2")
    if not lo <= n2 <= hi:
        sys.exit(f"{where}: A2 예시 {n2}단어, 범위 {lo}~{hi}를 벗어났습니다")
    if n1 >= n2:
        sys.exit(f"{where}: A1 답안({n1}단어)이 A2 예시({n2}단어)보다 짧아야 합니다")


# ---------- 글의 짜임(줄) ----------
def layout(no, seq):
    """호칭·끝인사는 한 줄씩, 고쳐 쓰는 번호는 한 덩어리로 묶고 번호마다 줄을 바꿉니다(시험의 모범 답안과 같은 모양).
    nc: 단어 수에 넣지 않는 줄(Betreff)."""
    out, body, n = [], None, 0
    for p in seq:
        if "fix" in p:
            out.append({"line": True, "nc": not counted(p), "items": [{"fix": p["fix"]}]})
            body = None
            continue
        n += 1
        if body is None:
            body = {"br": True, "items": []}
            out.append(body)
        body["items"].append({"k": f"{no}-{n}", "n": CIRC[n - 1]})
    return out


def render(lay, seq, kind):
    """kind: a1(번호 붙은 A1 답안) 또는 a2(강조 붙은 A2 예시)."""
    by, n = {}, 0
    for p in seq:
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
            if kind == "a1":
                hs.append(f'<span class="pn">{CIRC.index(it["n"]) + 1}</span>{e(p["a1"])}')
                ts.append(p["a1"])
            else:
                hs.append(marked(p["a2"]))
                ts.append(plain(p["a2"]))
        sep_h, sep_t = ("<br>", "\n") if b.get("br") else (" ", " ")
        cls = ' class="gr"' if b.get("line") else ""
        html_out.append(f"<p{cls}>{sep_h.join(hs)}</p>")
        text_out.append(sep_t.join(ts))
    return "".join(html_out), "\n\n".join(text_out)


# ---------- 조각 ----------
def task_pages():
    """index.html의 페이퍼 시험 페이지에서 Aufgabe 1·2의 시험지 쪽수를 찾습니다."""
    try:
        idx = open(os.path.join(APP, "index.html"), encoding="utf-8").read()
        i = idx.index(f'<section class="page mdt" id="m{N}"')
        blk = idx[i:idx.index("</section>", i)]
    except (OSError, ValueError):
        return {}
    k = blk.find('<h3 lang="de">Schreiben')
    out = {}
    for no in (1, 2):
        m = re.search(r'<span class="t">Aufgabe ' + str(no) + r'</span>[^\n]*?#page=(\d+)', blk[k:] if k >= 0 else blk)
        if m:
            out[no] = int(m.group(1))
    return out


PAGES = task_pages()


def task_box(no, t, erk):
    page = f" <small>시험지 {PAGES[no]}쪽</small>" if no in PAGES else ""
    out = "".join(f"<p>{e(x)}</p>" for x in t["situation"])
    out += '<ul class="dots">' + "".join(f"<li>{e(x)}</li>" for x in t["points"]) + "</ul>"
    out += f"<p>{e(t['instruction'])}</p>"
    box = f'<div class="box" lang="de"><h5 lang="ko">과제{page}</h5>{out}</div>'
    box += ('<ol class="lpko">' + "".join(f'<li><b>{i}</b><span>{e(x[1])}</span></li>' for i, x in enumerate(erk["points"], 1))
            + "</ol>")
    return box


def part_card(no, i, p, erk):
    k = f"{no}-{i}"
    lines = max(2, -(-len(plain(p["a2"])) // 52) + 1)
    n = punkt(p["role"])
    lpk = f'<span class="lpk">{e(erk["points"][n - 1][1].rstrip("."))}</span>' if n else ""
    return f"""<li class="part" id="p{k}">
<div class="ph"><span class="pn">{i}</span><span class="role">{e(p["role"])}</span>{lpk}<span class="ok">✓ 작성</span></div>
<div class="a1s"><span class="lab">A1</span><p lang="de">{e(p["a1"])}</p></div>
<div class="use"><span class="lab">쓸 표현</span><span class="ux" lang="de">{e(p["use"])}</span><em>{e(p["use_ko"])}</em></div>
<p class="hint">{ko(p["tip"])}</p>
<textarea class="ans" data-k="{k}" rows="2" lang="de" spellcheck="false" autocapitalize="off" autocomplete="off" autocorrect="off" aria-label="{i}번 A2 문장" placeholder="A2 문장으로 고쳐 쓰십시오"></textarea>
<div class="pv" lang="de"></div><div class="pl" aria-hidden="true">{"<i></i>" * lines}</div>
<div class="pbar"><button class="sbtn exb" type="button" aria-expanded="false" aria-controls="x{k}">예시 보기</button></div>
<div class="ex" id="x{k}" hidden><span class="lab">A2 예시</span><p lang="de">{marked(p["a2"])}</p></div>
</li>"""


sections, data_aufg = [], []
for no, (a, t, erk) in enumerate(zip(AUF, S, ERK), 1):
    seq = a["parts"]
    parts = [p for p in seq if "fix" not in p]
    lay = layout(no, seq)
    a1_html, _ = render(lay, seq, "a1")
    a2_html, _ = render(lay, seq, "a2")
    n1, n2 = total(seq, "a1"), total(seq, "a2")
    lo, hi = t["words"]
    reg = register(seq)
    fixes = [p["fix"].replace("\n", " ") for p in seq if "fix" in p and counted(p)]
    frame = f"호칭(«{fixes[0]}»)과 끝인사(«{fixes[-1]}»)는 그대로 둡니다. 번호가 붙은 부분만 고쳐 씁니다."
    kind = G.KIND[reg].format(kind="SMS" if no == 1 else "E-Mail")
    cards = "".join(part_card(no, i, p, erk) for i, p in enumerate(parts, 1))
    chk = "".join(f"<li><span>{ko(x)}</span></li>" for x in G.CHECK[reg] + [f"호칭과 끝인사, 이름까지 세어 {lo}–{hi}단어입니까?"])
    summ = "".join(f"<li>{ko(x)}</li>" for x in a["sum"])
    sections.append(f"""<section id="w{no}" class="aufg" data-a="{no}">
<h2><small>Aufgabe {no} · {lo}–{hi}단어 · 약 {t["minutes"]}분</small>{e(erk["title"])}</h2>
<p class="kind">{e(kind)}</p>
<p class="intro">{e(a["ko"])}</p>
{task_box(no, t, erk)}
<h3 class="sub3">A1 답안 <span class="cnt">{n1}단어</span></h3>
<div class="a1l" lang="de">{a1_html}</div>
<h3 class="sub3">A2로 고쳐 쓰기 <span class="prog" id="prog{no}">작성 0 / {len(parts)}</span></h3>
<p class="frame">{ko(frame)}</p>
<ol class="parts">{cards}</ol>
<details class="mine" id="mine{no}"><summary>내 글 전체 <span class="wc">0단어</span><small>목표 {lo}–{hi}단어 · {e(G.COUNT_NOTE)}</small></summary>
<div class="ml" lang="de"></div>
<div class="acts"><button class="sbtn cp" type="button" data-a="{no}">이 글 복사</button></div>
<h5>제출 전 확인</h5><ul class="chk">{chk}</ul></details>
<details class="a2f"><summary>A2 예시 답안 전체 <span class="wc ok">{n2}단어</span><small>A1 답안 {n1}단어</small></summary>
<div class="ml" lang="de">{a2_html}</div></details>
<h4 class="sub3 sumh">A1 → A2, 이렇게 바뀌었습니다</h4>
<ul class="dots sum">{summ}</ul>
</section>""")
    data_aufg.append({
        "no": str(no), "title": erk["title"], "lo": lo, "hi": hi,
        "layout": [{"line": bool(b.get("line")), "nc": bool(b.get("nc")), "br": bool(b.get("br")),
                    "items": [({"fix": it["fix"]} if "fix" in it else {"k": it["k"], "n": it["n"]}) for it in b["items"]]}
                   for b in lay],
        "parts": [{"k": f"{no}-{i}", "n": CIRC[i - 1], "role": p["role"], "a1": p["a1"], "use": p["use"]}
                  for i, p in enumerate(parts, 1)],
    })

steps = "".join(f"<li><b>{e(x)}</b>{e(y)}</li>" for x, y in G.STEPS)
diff = "".join(f'<li><b>{e(x)}</b><div class="d2"><small>A1</small>{ko(y)}</div><div class="d1"><small>A2</small>{ko(z)}</div></li>'
               for x, y, z in G.DIFF)
save_note = ("쓴 내용은 이 브라우저에 저절로 저장됩니다. 학습 포탈에 로그인한 상태라면 다른 기기에서도 이어서 쓸 수 있습니다."
             if WEB else "쓴 내용은 이 브라우저에 저절로 저장됩니다. 파일을 다른 곳으로 옮기면 저장한 내용이 이어지지 않을 수 있습니다.")
HOW = f"""<section id="how"><h2><small>Schreibübung</small>이렇게 연습합니다</h2>
<ol class="steps">{steps}</ol>
<p class="note">{e(G.HOW_NOTE)}</p>
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

NAV = [("how", "사용법"), ("w1", "Aufgabe 1"), ("w2", "Aufgabe 2"), ("sub", "제출")]
nav = "".join(f'<a href="#{x}">{y}</a>' for x, y in NAV)
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
<p class="eyebrow">SODA Lehrwerk · Goethe-Zertifikat A2</p>
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
