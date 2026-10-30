#!/usr/bin/env python3
"""Modelltest 1·2 페이지의 Sprechen(Mündlicher Ausdruck) 영역에 「말하기 실전 연습」 줄을 넣습니다.
저장소 루트에서 실행합니다. 이미 들어 있으면 건너뛰므로 몇 번을 실행해도 결과가 같습니다.
build-index.py 로 index.html 을 다시 만든 뒤에는 이 스크립트를 한 번 더 실행하십시오.
"""
import re, sys
BASE = 'https://sophiadeutschakademie.github.io/SODA-Lehrwerk/sprechen/'
APPS = {  # 폴더: 앱 안 시험 id
    'goethe-a2': 'goethe-a2',
    'goethe-b1': 'goethe-b1',
    'goethe-b2': 'goethe-b2',
}
MARK = 'sp-live'
total = 0
for folder, base_id in APPS.items():
    p = folder + '/index.html'
    s = open(p, encoding='utf-8').read()
    for n in (1, 2):
        exam = base_id if n == 1 else base_id + '-2'
        row = ('<div class="it %s"><span class="t">Üben</span><span class="d">말하기 실전 연습<span>시험관·파트너와 Teil별로 연습 · 소피아 독일어학원 재학생 전용 · 아이디와 비밀번호 필요</span></span>'
               '<a class="go" href="%s#%s" target="_blank" rel="noopener">연습</a></div>\n') % (MARK, BASE, exam)
        for prefix in ('m', 'd'):
            sid = '%s%d' % (prefix, n)
            i = s.index('<section class="page mdt" id="%s"' % sid)
            j = s.index('</section>', i)
            blk = s[i:j]
            if MARK in blk:
                continue
            m = re.search(r'<div class="mod"><h3 lang="de">(?:Sprechen|Mündlicher Ausdruck)[^\n]*</h3>\n', blk)
            assert m, (folder, sid)
            # 첫 .it 앞에 넣습니다(디지털 쪽은 안내 문단 note 뒤)
            k = blk.index('<div class="it">', m.end())
            blk2 = blk[:k] + row + blk[k:]
            s = s[:i] + blk2 + s[j:]
            total += 1
    open(p, 'w', encoding='utf-8').write(s)
print('patched', total)
