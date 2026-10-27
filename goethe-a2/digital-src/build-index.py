#!/usr/bin/env python3
"""index.html(표지 · 응시 방식 · 페이퍼 목록 · 디지털 목록 · 시험별 페이지)을 data/mtN.json과 이 폴더의 PDF·MP3에서 만듭니다.

python3 digital-src/build-index.py        # 이 앱 폴더의 index.html을 다시 씁니다

필요한 것: 이 앱 폴더의 `Goethe A2 Modelltest N.pdf`, `Goethe A2 Modelltest N.1.mp3` ~ `N.4.mp3`, digital-src/data/mtN.json
(`index` 블록: Hören 주제, Schreiben 제목, Sprechen 주제), ffprobe(음원 길이)
"""
import argparse
import base64
import glob
import html
import json
import os
import re
import subprocess
import sys
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
LEVEL = "A2"
PREFIX = "sodaGZA2.v1."
PDF_PAGES = {"lesen": [2, 4, 5, 7], "hoeren": [9, 10, 11, 12], "schreiben": 13, "sprechen": [14, 15, 16],
             "loesung": 17, "muster": 18, "dialoge": 19, "kommentar": 20, "hoertexte": 22}
ARROW = ('<svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true"><path d="M5.5 2.5 11 8l-5.5 5.5" fill="none" '
         'stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>')
ARROW_R = ('<svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true"><path d="M2.5 8h11M9 3.5 13.5 8 9 12.5" fill="none" '
           'stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def e(s):
    return html.escape(str(s), quote=True)


def check_glyphs(font_path, text):
    """Warnt, wenn Zeichen in fonts/pretendard-index.woff fehlen (sie erscheinen dann in der Systemschrift)."""
    try:
        from fontTools.ttLib import TTFont
    except ImportError:
        return
    cmap = TTFont(font_path).getBestCmap()
    missing = sorted({c for c in text if ord(c) >= 0x20 and ord(c) not in cmap and not c.isspace()})
    if missing:
        print("Hinweis: Diese Zeichen fehlen in fonts/pretendard-index.woff und erscheinen in der Systemschrift:", "".join(missing))


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                         capture_output=True, text=True, check=True).stdout.strip()
    return float(out)


def mmss(sec):
    s = int(round(sec))
    return f"{s // 60}:{s % 60:02d}"


def split_topic(s):
    """'Interview: Hitze in deutschen Städten' -> ('Interview', 'Hitze in deutschen Städten')"""
    if ":" in s:
        a, b = s.split(":", 1)
        return a.strip(), b.strip()
    return "", s.strip()


def roman_no(n):
    return f"{n:02d}"


class Test:
    def __init__(self, n, repo):
        self.n = n
        self.d = json.load(open(os.path.join(HERE, "data", f"mt{n}.json"), encoding="utf-8"))
        self.roman = self.d["roman"]
        self.pdf = quote(f"Goethe {LEVEL} Modelltest {n}.pdf")
        self.dur = []
        for k in range(1, 5):
            fp = os.path.join(repo, f"Goethe {LEVEL} Modelltest {n}.{k}.mp3")
            if not os.path.exists(fp):
                sys.exit(f"Audio fehlt: {fp}")
            self.dur.append(duration(fp))
        if not os.path.exists(os.path.join(repo, f"Goethe {LEVEL} Modelltest {n}.pdf")):
            sys.exit(f"PDF fehlt: Modelltest {n}")

    def mp3(self, k):
        return quote(f"Goethe {LEVEL} Modelltest {self.n}.{k}.mp3")

    def pg(self, p):
        return f'{self.pdf}#page={p}'

    def short(self):
        L = self.d["lesen"]
        t4 = split_topic(self.d["index"]["hoeren"]["t4"])[1]
        return f'{L["t1"]["title"]} · {t4}'


def link(t, p, label=None):
    return f'<a class="p" href="{t.pg(p)}" target="_blank" rel="noopener">{label or "S. " + str(p)}</a>'


def item(tag, title, desc, right):
    return f'<div class="it"><span class="t">{e(tag)}</span><span class="d" lang="de">{e(title)}<span>{e(desc)}</span></span>{right}</div>'


def paper_page(t):
    d, ix, L = t.d, t.d["index"], t.d["lesen"]
    n = t.n
    out = []
    out.append(f'<section class="page mdt" id="m{n}" aria-labelledby="m{n}-h">')
    out.append('<div class="brand"><img src="__LOGO__" alt=""><b>Sophia Deutsch Akademie</b></div>')
    out.append('<div class="main">')
    out.append(f'<p class="eyebrow">Goethe-Zertifikat {LEVEL}</p>')
    out.append(f'<h2 id="m{n}-h" lang="de">Modelltest {e(t.roman)}</h2>')
    out.append('<p class="lead">Lesen · Hören · Schreiben · Sprechen — 23 Seiten, Hörtexte 4 Dateien</p>')
    out.append('<div class="actions">'
               f'<a class="btn" href="{t.pdf}" target="_blank" rel="noopener">PDF 열기</a>'
               f'<a class="btn ghost" href="{t.pdf}" download>PDF 다운로드</a>'
               f'<a class="btn ghost" href="#d{n}">디지털로 풀기</a>'
               f'<a class="btn ghost" href="{t.pg(PDF_PAGES["loesung"])}" target="_blank" rel="noopener">Lösungsschlüssel</a></div>')
    # Lesen
    out.append('<div class="mod"><h3 lang="de">Lesen<small>30 Min.</small></h3>')
    pl = PDF_PAGES["lesen"]
    m4 = re.search(r"Personen suchen (.+?)\.", L["t4"]["instruction"])
    out.append(item("Teil 1", L["t1"]["title"], "Zeitungsartikel · a / b / c · 1–5", link(t, pl[0])))
    out.append(item("Teil 2", L["t2"]["board"]["title"], "Informationstafel · a / b / c · 6–10", link(t, pl[1])))
    out.append(item("Teil 3", L["t3"]["mail"]["subject"], "E-Mail · a / b / c · 11–15", link(t, pl[2])))
    out.append(item("Teil 4", "Anzeigen: " + (m4.group(1) if m4 else "a–f"), "Situationen und Anzeigen a–f · eine Aufgabe ohne Lösung (X) · 16–20", link(t, pl[3])))
    out.append('</div>')
    # Hören
    out.append('<div class="mod"><h3 lang="de">Hören<small>ca. 30 Min.</small></h3>')
    kinds = [("Kurze Texte", "zweimal", "Aufgaben 1–5"), ("Gespräch", "einmal", "Bilder a–i · 6–10"),
             ("Kurze Gespräche", "einmal", "Bilder a–c · 11–15"), ("Interview", "zweimal", "Ja / Nein · 16–20")]
    for k in range(4):
        topic = ix["hoeren"][f"t{k + 1}"]
        typ, title = split_topic(topic)
        kind = kinds[k][0]
        if k in (0, 2):
            title = topic
        desc = f'{kind} · {kinds[k][1]} · {kinds[k][2]} · {mmss(t.dur[k])}'
        right = (link(t, PDF_PAGES["hoeren"][k]) +
                 f'<audio controls preload="none" src="{t.mp3(k + 1)}" aria-label="Hören Teil {k + 1}"></audio>'
                 f'<a class="dl" href="{t.mp3(k + 1)}" download>MP3 다운로드</a>')
        out.append(item(f"Teil {k + 1}", title, desc, right))
    out.append('</div>')
    # Schreiben
    out.append('<div class="mod"><h3 lang="de">Schreiben<small>30 Min.</small></h3>')
    tasks = d["schreiben"]["tasks"]
    for i, tk in enumerate(tasks):
        out.append(item(f"Aufgabe {i + 1}", ix["schreiben"][i], f'{tk["words"][0]}–{tk["words"][1]} Wörter · etwa {tk["minutes"]} Min.', link(t, PDF_PAGES["schreiben"])))
    out.append('</div>')
    # Sprechen
    sp = ix["sprechen"]
    out.append('<div class="mod"><h3 lang="de">Sprechen<small>ca. 15 Min. · zu zweit</small></h3>')
    out.append(item("Teil 1", "Fragen zur Person", " · ".join(sp["teil1"]) + " · circa 3 Min.", link(t, PDF_PAGES["sprechen"][0])))
    out.append(item("Teil 2", "Von sich erzählen", f'{sp["teil2"][0]} / {sp["teil2"][1]} · circa 6 Min.', link(t, PDF_PAGES["sprechen"][1])))
    out.append(item("Teil 3", "Gemeinsam etwas planen", f'{sp["teil3"]} · circa 5 Min.', link(t, PDF_PAGES["sprechen"][2])))
    out.append('</div>')
    # Materialien
    out.append('<div class="mod"><h3 lang="de">Lösungen und Materialien</h3>')
    out.append(item("Lösungen", "Lösungsschlüssel", "Lesen · Hören · Punkte · Seite 17", link(t, PDF_PAGES["loesung"])))
    out.append(item("Schreiben", "Musterlösungen", "Schreiben Aufgabe 1–2 · Typische Fehler · Seite 18", link(t, PDF_PAGES["muster"])))
    out.append(item("Sprechen", "Musterdialoge", "Sprechen Teil 1–3 · Seite 19", link(t, PDF_PAGES["dialoge"])))
    out.append(item("Lehrende", "Kommentar", "Fallen und Distraktoren · Seite 20–21", link(t, PDF_PAGES["kommentar"])))
    out.append(item("Hörtexte", "Transkripte", "Hören Teil 1–4 · Seite 22–23", link(t, PDF_PAGES["hoertexte"])))
    out.append('</div></div>')
    out.append(f'<div class="foot"><a href="#list">← Modelltest</a><span>Goethe {LEVEL} · Modelltest {e(t.roman)}</span></div></section>')
    return "\n".join(out)


def digital_page(t):
    n = t.n
    ix = t.d["index"]
    out = []
    out.append(f'<section class="page mdt" id="d{n}" aria-labelledby="d{n}-h">')
    out.append('<div class="brand"><img src="__LOGO__" alt=""><b>Sophia Deutsch Akademie</b></div>')
    out.append('<div class="main">')
    out.append(f'<p class="eyebrow">Goethe-Zertifikat {LEVEL} · Digital</p>')
    out.append(f'<h2 id="d{n}-h" lang="de">Modelltest {e(t.roman)}</h2>')
    out.append('<p class="lead">모듈을 고르면 디지털 시험 화면이 열립니다. 시작 전에 화면 사용법(튜토리얼)을 볼 수 있고, 제출하면 바로 채점됩니다.</p>')
    out.append('<div class="mod"><h3 lang="de">Am Computer<small>Lesen · Hören · Schreiben</small></h3>')
    rows = [("Lesen", "4 Teile · 20 Aufgaben", "30 Minuten · Text links, Aufgaben rechts · Markieren", "lesen"),
            ("Hören", "4 Teile · 20 Aufgaben", "ca. 30 Minuten · automatische Wiedergabe · Kopfhörer empfohlen", "hoeren"),
            ("Schreiben", "2 Aufgaben", "30 Minuten · SMS und E-Mail · Textfeld mit Wörterzähler", "schreiben")]
    for tag, title, desc, m in rows:
        out.append(f'<div class="it"><span class="t">{tag}</span><span class="d" lang="de">{title}<span>{desc}</span></span>'
                   f'<a class="go" href="digital.html#{n}-{m}">시작</a><span class="stt" data-m="{m}"></span></div>')
    out.append('</div>')
    out.append('<div class="mod"><h3 lang="de">Sprechen<small>vor Ort · zu zweit</small></h3>')
    out.append('<p class="note">Sprechen ist auch bei der digitalen Prüfung eine Prüfung mit Prüfenden vor Ort; die Aufgaben bekommen Sie auf Papier. · '
               '말하기는 디지털 시험에서도 시험관과 대면으로 보고, 과제지는 종이로 받습니다.</p>')
    out.append(item("Teil 1–3", "Kandidatenblätter", "Fragen zur Person · Von sich erzählen · Gemeinsam etwas planen", link(t, PDF_PAGES["sprechen"][0])))
    out.append(item("Muster", "Musterdialoge", "Sprechen Teil 1–3", link(t, PDF_PAGES["dialoge"])))
    out.append('</div></div>')
    out.append(f'<div class="foot"><a href="#digital">← Modelltest digital</a><a href="#{n}">페이퍼 자료 (PDF · MP3) →</a></div></section>')
    return "\n".join(out)


def toc(tests, prefix, label):
    lis = []
    for t in tests:
        lis.append(f'<li><a class="tocl" href="#{prefix}{t.n}"><span class="no">{roman_no(t.n)}</span><span>'
                   f'<span class="nm" lang="de">Modelltest {e(t.roman)}</span><span class="ds" lang="de">{e(t.short())}</span></span>'
                   f'<span class="lk">{ARROW}</span></a></li>')
    return f'<ol class="toc" aria-label="{label}">\n' + "\n".join(lis) + '\n    </ol>'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=os.path.dirname(HERE))
    ap.add_argument("--out", default="")
    a = ap.parse_args()
    nums = sorted(int(re.search(r"mt(\d+)\.json$", f).group(1)) for f in glob.glob(os.path.join(HERE, "data", "mt*.json")))
    tests = [Test(n, a.repo) for n in nums]
    ids = ["cover", "mode", "list", "digital"] + [f"m{n}" for n in nums] + [f"d{n}" for n in nums]
    hide = ",".join(f'html:not([data-page="{i}"]) #{i}' for i in ids) + "{display:none}"
    anim = ",".join(f"#{i}" for i in ids) + "{animation:pgIn .35s ease both}"
    reduced = "@media (prefers-reduced-motion:reduce){" + ",".join(f"#{i}" for i in ids) + "{animation:none}}"
    css = open(os.path.join(HERE, "index-style.css"), encoding="utf-8").read()
    css = css.replace("/*HIDE*/", hide).replace("/*ANIM*/", anim).replace("/*REDUCED*/", reduced)
    font = base64.b64encode(open(os.path.join(HERE, "fonts", "pretendard-index.woff"), "rb").read()).decode()
    logo = "data:image/png;base64," + base64.b64encode(open(os.path.join(HERE, "logo-index.png"), "rb").read()).decode()
    lo, hi = nums[0], nums[-1]
    rng = f"{lo}–{hi}"
    pre = ('<!DOCTYPE html>\n<html lang="ko">\n<head>\n<meta charset="UTF-8">\n'
           '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
           '<meta name="color-scheme" content="light">\n<meta name="robots" content="noindex,nofollow">\n'
           "<script>(function(){var h=location.hash.replace('#','');var p='cover';if(h==='mode'||h==='list'||h==='digital')p=h;"
           f"else if(/^[{lo}-{hi}]$/.test(h))p='m'+h;else if(/^d[{lo}-{hi}]$/.test(h))p=h;"
           "document.documentElement.setAttribute('data-page',p);})();</script>\n"
           f'<title>Goethe {LEVEL} Modelltest — Sophia Deutsch Akademie</title>\n'
           '<style>/* Pretendard (SIL Open Font License 1.1, digital-src/fonts/Pretendard-OFL.txt), Teilmenge mit den hier verwendeten Zeichen */'
           f'@font-face{{font-family:"Pretendard SODA";src:url(data:font/woff;base64,{font}) format("woff");font-weight:45 930;font-style:normal;font-display:swap}}</style>\n'
           f'<style>\n{css}</style>\n</head>\n<body>\n')
    brand = '<div class="brand"><img src="__LOGO__" alt=""><b>Sophia Deutsch Akademie</b></div>'
    body = f'''<header class="page" id="cover">
  <div class="brand"><img src="__LOGO__" alt="Sophia Deutsch Akademie 로고"><b>Sophia Deutsch Akademie</b></div>
  <div class="main">
    <p class="eyebrow">Prüfungsvorbereitung</p>
    <h1 lang="de">Goethe {LEVEL}</h1>
    <p class="lead">Modelltest {rng} · Papier und digital</p>
    <div class="rule" aria-hidden="true"></div>
    <a class="start" href="#mode" id="start" style="text-decoration:none">시작하기 {ARROW_R}</a>
  </div>
  <div class="foot"><span>© 2026 Sophia Deutsch Akademie</span></div>
</header>

<section class="page" id="mode" aria-labelledby="mode-h">
  {brand}
  <div class="main">
    <p class="eyebrow">Goethe {LEVEL}</p>
    <h2 id="mode-h">응시 방식</h2>
    <p class="lead" style="margin:0 0 28px;font-size:15px">보실 시험 방식을 고르세요.</p>
    <div class="modes">
      <a class="mode" href="#list"><span class="mk" lang="de">Papier</span><b>페이퍼 시험</b><span class="ds">PDF 문제지와 듣기 음원(MP3)을 열거나 내려받아 종이에 풉니다. 해답·듣기 대본·모범 답안이 PDF에 함께 있습니다.</span><span class="go2">PDF · 음원 받기 {ARROW}</span></a>
      <a class="mode" href="#digital"><span class="mk" lang="de">Digital</span><b>디지털 시험</b><span class="ds">Lesen · Hören · Schreiben을 컴퓨터에서 디지털 시험 화면 그대로 풉니다. 남은 시간 표시, 음원 자동 재생, 단어 수 자동 계산, 제출 후 바로 채점됩니다.</span><span class="go2">컴퓨터에서 풀기 {ARROW}</span></a>
    </div>
    <p class="note">디지털 시험은 PC·노트북 화면에 맞춰져 있습니다. 듣기는 헤드폰을 권합니다. Sprechen은 두 방식 모두 시험관과 대면으로 봅니다.</p>
  </div>
  <div class="foot"><a href="#">← 표지</a><span>Goethe {LEVEL}</span></div>
</section>

<section class="page" id="list" aria-labelledby="list-h">
  {brand}
  <div class="main">
    <p class="eyebrow">Goethe {LEVEL} · Papier</p>
    <h2 id="list-h" lang="de">Modelltest</h2>
    <p class="lead">페이퍼 시험 · 모의고사를 선택하면 PDF 문제지와 듣기 음원을 열거나 내려받을 수 있습니다.</p>
    {toc(tests, "", "Modelltest 목록")}
  </div>
  <div class="foot"><a href="#mode">← 응시 방식</a><span>Goethe {LEVEL} · Papier</span></div>
</section>

<section class="page" id="digital" aria-labelledby="dg-h">
  {brand}
  <div class="main">
    <p class="eyebrow">Goethe {LEVEL} · Digital</p>
    <h2 id="dg-h" lang="de">Modelltest digital</h2>
    <p class="lead">디지털 시험 · 모의고사를 고른 뒤 Lesen · Hören · Schreiben 모듈을 컴퓨터에서 풉니다.</p>
    {toc(tests, "d", "디지털 Modelltest 목록")}
  </div>
  <div class="foot"><a href="#mode">← 응시 방식</a><span>Goethe {LEVEL} · Digital</span></div>
</section>

'''
    pages = "\n".join(paper_page(t) for t in tests) + "\n" + "\n".join(digital_page(t) for t in tests) + "\n"
    script = f'''<script>
(function(){{
  var root=document.documentElement;
  function fmt(s){{s=Math.max(0,Math.ceil(s));var m=Math.floor(s/60),x=s%60;return(m<10?'0':'')+m+':'+(x<10?'0':'')+x;}}
  function get(k){{try{{var v=localStorage.getItem('{PREFIX}'+k);return v?JSON.parse(v):null;}}catch(e){{return null;}}}}
  function status(n){{
    var els=document.querySelectorAll('#d'+n+' .stt');
    for(var i=0;i<els.length;i++){{
      var k='mt'+n+'.'+els[i].getAttribute('data-m'),st=get(k+'.state'),rs=get(k+'.result'),t='';
      if(st&&st.remaining>1)t='진행 중 · 남은 시간 '+fmt(st.remaining)+' (이어서 풀기 가능)';
      else if(rs&&rs.score)t='최근 결과 '+rs.score.correct+'/'+rs.score.total+' · '+String(rs.score.points).replace('.',',')+'점 ('+rs.finished+')';
      else if(rs)t='최근 제출 '+rs.finished;
      els[i].textContent=t;
    }}
  }}
  function route(){{var h=location.hash.replace('#','');var p='cover';if(h==='mode'||h==='list'||h==='digital')p=h;else if(/^[{lo}-{hi}]$/.test(h))p='m'+h;else if(/^d[{lo}-{hi}]$/.test(h))p=h;root.setAttribute('data-page',p);window.scrollTo(0,0);if(p.charAt(0)==='d'&&p!=='digital')status(p.slice(1));}}
  window.addEventListener('hashchange',route);
  route();
}})();
</script>
</body>
</html>
'''
    doc = (pre + body + pages + script).replace("__LOGO__", logo)
    check_glyphs(os.path.join(HERE, "fonts", "pretendard-index.woff"), re.sub(r"data:[^\"')]+", "", doc))
    out = a.out or os.path.join(a.repo, "index.html")
    open(out, "w", encoding="utf-8").write(doc)
    # Lehrwerk 공통 다크 모드 스위치(tools/soda-theme.py)를 넣습니다
    theme = os.path.join(HERE, "..", "..", "tools", "soda-theme.py")
    if os.path.exists(theme):
        subprocess.run([sys.executable, theme, out, "--kind", "index"], check=True)
    print(f"geschrieben: {out} ({len(doc.encode('utf-8')) / 1024:.0f} KB), Modelltests: {', '.join(str(n) for n in nums)}")


if __name__ == "__main__":
    main()
