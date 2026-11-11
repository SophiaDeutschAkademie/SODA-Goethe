#!/usr/bin/env python3
"""Goethe B1 목록 페이지(index.html)의 각 Modelltest 페이지에 「해설」 버튼을 넣습니다.

python3 digital-src/erklaerung/add-buttons.py        (앱 폴더 goethe-b1/ 에서, 또는 어디서든)

- 앱 폴더에 `Goethe B1 Modelltest N 해설.html`이 있는 회차만 넣습니다.
- 버튼은 페이퍼 시험 페이지(#mN)의 버튼 줄에서 Lösungsschlüssel 바로 앞에 들어갑니다.
- 이미 들어 있으면 건너뜁니다. 해설 파일이 없어진 회차의 버튼은 지웁니다. 몇 번을 실행해도 결과가 같습니다.
"""
import os
import re
import sys
from urllib.parse import quote

APP = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
INDEX = os.path.join(APP, "index.html")
html = open(INDEX, encoding="utf-8").read()
added = kept = removed = 0
for m in sorted({int(x) for x in re.findall(r'href="Goethe%20B1%20Modelltest%20(\d+)\.pdf#page=17" target="_blank" rel="noopener">Lösungsschlüssel</a></div>', html)}):
    name = f"Goethe B1 Modelltest {m} 해설.html"
    btn = f'<a class="btn ghost" href="{quote(name)}">해설</a>'
    key = f'<a class="btn ghost" href="Goethe%20B1%20Modelltest%20{m}.pdf#page=17" target="_blank" rel="noopener">Lösungsschlüssel</a></div>'
    has = btn + key in html
    if os.path.exists(os.path.join(APP, name)):
        if has:
            kept += 1
        else:
            if html.count(key) != 1:
                sys.exit(f"Modelltest {m}: Lösungsschlüssel 버튼을 한 곳으로 정하지 못했습니다 ({html.count(key)}곳)")
            html = html.replace(key, btn + key)
            added += 1
    elif has:
        html = html.replace(btn + key, key)
        removed += 1
open(INDEX, "w", encoding="utf-8").write(html)
print(f"index.html: 「해설」 버튼 {added}개 넣음, {kept}개 그대로, {removed}개 지움")
