#!/usr/bin/env python3
"""디지털 시험 화면의 제출 주소(SUBMIT_URL)를 한 번에 바꿉니다. 저장소 루트에서 실행합니다.
  python3 tools/set-submit-url.py "https://script.google.com/macros/s/…/exec"
template.html, digital.html, 작문 연습 페이지(… 작문 연습.html)를 모두 바꾸고, 이미 같은 주소면 건너뜁니다.
"""
import glob, re, sys
if len(sys.argv) != 2 or not re.fullmatch(r'https://script\.google\.com/macros/s/[A-Za-z0-9_-]+/exec', sys.argv[1]):
    sys.exit('사용법: python3 tools/set-submit-url.py "https://script.google.com/macros/s/…/exec"')
url = sys.argv[1]
n = 0
for p in sorted(glob.glob('*/digital-src/template.html') + glob.glob('*/digital.html') + glob.glob('*/* 작문 연습.html')):
    s = open(p, encoding='utf-8').read()
    t, k = re.subn(r"(var SUBMIT_URL = ')[^']*(';)", lambda m: m.group(1) + url + m.group(2), s)
    if k and t != s:
        open(p, 'w', encoding='utf-8').write(t); n += 1; print('updated', p)
print(n, 'files updated')
