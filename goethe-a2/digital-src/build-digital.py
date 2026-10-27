#!/usr/bin/env python3
"""digital.html(Goethe A2 디지털 시험 화면)을 data/mtN.json에서 만듭니다.

python3 digital-src/build-digital.py            # 저장소 루트의 digital.html을 다시 씁니다
python3 digital-src/build-digital.py --only 4,5 # 일부 Modelltest만 넣어 시험해 볼 때
"""
import argparse
import base64
import datetime as dt
import glob
import json
import re
import os
import subprocess
import sys
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
PAGES = {"loesung": 17, "muster": 18, "kommentar": 20, "hoertexte": 22}  # PDF-Seiten (Lösungsschlüssel, Musterlösungen, Kommentar, Hörtexte)
PAGES_OVERRIDE = {}  # z. B. {6: {"loesung": 18, "muster": 19, "kommentar": 21, "hoertexte": 23}}


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                         capture_output=True, text=True, check=True).stdout.strip()
    return round(float(out), 2)


def check_glyphs(font_path, text):
    """Warnt, wenn Zeichen fehlen (dann neu erzeugen: python3 digital-src/make-font.py PretendardVariable.ttf)."""
    try:
        from fontTools.ttLib import TTFont
    except ImportError:
        return
    cmap = TTFont(font_path).getBestCmap()
    missing = sorted({c for c in text if ord(c) >= 0x20 and ord(c) not in cmap and not c.isspace()})
    if missing:
        print("Hinweis: Diese Zeichen fehlen in fonts/pretendard-soda.woff und erscheinen in der Systemschrift:", "".join(missing))


def strip_notes(obj, top=True):
    """Entfernt Felder, die nur für die Übersichtsseite oder die Pflege gedacht sind (notes, index)."""
    if isinstance(obj, dict):
        return {k: strip_notes(v, False) for k, v in obj.items() if k != "notes" and not (top and k == "index")}
    if isinstance(obj, list):
        return [strip_notes(v, False) for v in obj]
    return obj


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=os.path.dirname(HERE))
    ap.add_argument("--only", default="")
    ap.add_argument("--out", default="")
    a = ap.parse_args()
    only = {int(x) for x in a.only.split(",") if x.strip()}
    tests = {}
    files = glob.glob(os.path.join(HERE, "data", "mt*.json"))
    nums = sorted(int(re.search(r"mt(\d+)\.json$", f).group(1)) for f in files if re.search(r"mt(\d+)\.json$", f))
    for n in nums:
        if only and n not in only:
            continue
        p = os.path.join(HERE, "data", f"mt{n}.json")
        d = strip_notes(json.load(open(p, encoding="utf-8")))
        audio = []
        for k in range(1, 5):
            fn = f"Goethe A2 Modelltest {n}.{k}.mp3"
            fp = os.path.join(a.repo, fn)
            if not os.path.exists(fp):
                sys.exit(f"Audio fehlt: {fp}")
            audio.append({"src": quote(fn), "dur": duration(fp)})
        d["audio"] = audio
        d["pdf"] = quote(f"Goethe A2 Modelltest {n}.pdf")
        d["pages"] = PAGES_OVERRIDE.get(n, PAGES)
        tests[str(n)] = d
    if not tests:
        sys.exit("keine Daten")
    build = dt.datetime.now().strftime("%Y%m%d%H%M")
    data = json.dumps({"build": build, "tests": tests}, ensure_ascii=False, separators=(",", ":"))
    data = data.replace("</", "<\\/")
    logo = base64.b64encode(open(os.path.join(HERE, "logo-small.png"), "rb").read()).decode()
    src = open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
    font_path = os.path.join(HERE, "fonts", "pretendard-soda.woff")
    font = base64.b64encode(open(font_path, "rb").read()).decode()
    check_glyphs(font_path, src + data)
    for ph in ("__EXAM_DATA__", "__LOGO_DATA_URI__", "__UI_FONT__"):
        if src.count(ph) != 1:
            sys.exit(f"Platzhalter {ph} kommt {src.count(ph)}x vor")
    html = src.replace("__EXAM_DATA__", data).replace("__LOGO_DATA_URI__", "data:image/png;base64," + logo).replace("__UI_FONT__", font)
    out = a.out or os.path.join(a.repo, "digital.html")
    open(out, "w", encoding="utf-8").write(html)
    # Lehrwerk 공통 다크 모드 스위치(tools/soda-theme.py)를 넣습니다
    theme = os.path.join(HERE, "..", "..", "tools", "soda-theme.py")
    if os.path.exists(theme):
        subprocess.run([sys.executable, theme, out, "--kind", "exam"], check=True)
    print(f"geschrieben: {out} ({len(html.encode('utf-8')) / 1024:.0f} KB), Modelltests: {', '.join(sorted(tests))}, build {build}")


if __name__ == "__main__":
    main()
