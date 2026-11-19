#!/usr/bin/env python3
"""Goethe A2 목록 페이지(index.html)의 Modelltest 페이지에 「작문 연습」 줄을 넣습니다.

python3 digital-src/schreibuebung/add-links.py        (앱 폴더 goethe-a2/ 에서, 또는 어디서든)

- 앱 폴더에 `Goethe A2 Modelltest N 작문 연습.html`이 있는 회차만 넣습니다.
- 페이퍼 시험 페이지(#mN): Schreiben 영역의 첫 줄로 들어갑니다(Sprechen 영역의 「말하기 실전 연습」과 같은 모양).
- 디지털 시험 페이지(#dN): 「Am Computer」 영역의 Schreiben 줄 바로 아래에 들어갑니다.
- 이미 들어 있으면 건너뛰고, 문구가 바뀌었으면 고칩니다. 작문 연습 파일이 없어진 회차의 줄은 지웁니다. 몇 번을 실행해도 결과가 같습니다.
"""
import os
import re
import sys
from urllib.parse import quote

APP = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
INDEX = os.path.join(APP, "index.html")
MARK = "sw-live"
ROW = re.compile(r'<div class="it ' + MARK + r'">.*?</div>\n')

html = open(INDEX, encoding="utf-8").read()
added = kept = removed = updated = 0
nums = sorted({int(x) for x in re.findall(r'<section class="page mdt" id="m(\d+)"', html)})
for n in nums:
    name = f"Goethe A2 Modelltest {n} 작문 연습.html"
    row = (f'<div class="it {MARK}"><span class="t">Üben</span><span class="d">작문 연습'
           f'<span>A1 답안을 A2 표현으로 고쳐 쓰기 · Aufgabe 1·2</span></span>'
           f'<a class="go" href="{quote(name)}">연습</a></div>\n')
    exists = os.path.exists(os.path.join(APP, name))
    for prefix in ("m", "d"):
        sid = f"{prefix}{n}"
        i = html.index(f'<section class="page mdt" id="{sid}"')
        j = html.index("</section>", i)
        blk = html[i:j]
        has = MARK in blk
        if not exists:
            if has:
                blk = ROW.sub("", blk)
                removed += 1
        elif has:
            new = ROW.sub(lambda _m: row, blk, count=1)
            if new == blk:
                kept += 1
            else:
                blk = new
                updated += 1
        else:
            if prefix == "m":
                m = re.search(r'<div class="mod"><h3 lang="de">Schreiben<small>[^<]*</small></h3>\n', blk)
                if not m:
                    sys.exit(f"Modelltest {n}: 페이퍼 페이지의 Schreiben 영역을 찾지 못했습니다")
                k = blk.index('<div class="it">', m.end())
            else:
                m = re.search(r'<div class="it"><span class="t">Schreiben</span>.*?</div>\n', blk)
                if not m:
                    sys.exit(f"Modelltest {n}: 디지털 페이지의 Schreiben 줄을 찾지 못했습니다")
                k = m.end()
            blk = blk[:k] + row + blk[k:]
            added += 1
        html = html[:i] + blk + html[j:]
open(INDEX, "w", encoding="utf-8").write(html)
print(f"index.html: 「작문 연습」 줄 {added}개 넣음, {updated}개 고침, {kept}개 그대로, {removed}개 지움")
