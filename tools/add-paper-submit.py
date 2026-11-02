#!/usr/bin/env python3
"""페이퍼 시험 페이지(index.html의 m1, m2, … 구역)에 「풀이 PDF 제출하기」 상자를 넣습니다.

저장소 루트에서 실행합니다.
  python3 tools/add-paper-submit.py goethe-a2 goethe-b1 goethe-b2        (SODA-Goethe)
  python3 tools/add-paper-submit.py telc-b1 telc-b2 telc-c1-hs           (SODA-TELC)

- 종이 시험지에 푼 답안을 스캔·촬영해 PDF로 만든 학생이 PDF를 올려 제출합니다(소피아 독일어학원 수강생 전용 안내 포함).
- PDF는 Google Apps Script 웹 앱(tools/제출 받기/Code.gs)이 선생님 메일에 첨부해 전달합니다.
- 같은 브라우저에서 한 말하기 실전 연습 기록이 있으면 함께 전송합니다(디지털 시험 제출하기와 같은 방식).
- 제출 주소는 각 앱의 digital.html 에 들어 있는 SUBMIT_URL 을 읽어 씁니다. 먼저 tools/set-submit-url.py 를 실행해 두십시오.
- 이미 들어 있으면 건너뛰므로 몇 번을 실행해도 결과가 같습니다. build-index.py 로 index.html 을 다시 만든 뒤에는 한 번 더 실행하십시오
  (add-sprechen-links.py 와 같은 이유입니다).
"""
import os, re, sys

SPRECHEN = 'https://sophiadeutschakademie.github.io/SODA-Lehrwerk/sprechen/'
APPS = {  # 폴더: (시험 이름, 말하기 연습 앱의 시험 id 앞부분, 비어 있으면 말하기 연습 없음)
    'goethe-a2': ('Goethe A2', 'goethe-a2'),
    'goethe-b1': ('Goethe B1', 'goethe-b1'),
    'goethe-b2': ('Goethe B2', 'goethe-b2'),
    'telc-b1': ('telc B1', 'telc-b1'),
    'telc-b2': ('telc B2', 'telc-b2'),
    'telc-c1-hs': ('telc C1 Hochschule', ''),
}
MARK = 'soda-psub'

CSS = """.psub{margin:34px 0 0;padding:18px 20px;border:1px solid var(--line);border-radius:12px;max-width:700px}
.psub h3{margin:0 0 4px;font-size:17px;line-height:1.4}
.psub h3 em{font-style:normal;font-size:12.5px;font-weight:700;color:var(--ink-3);margin-left:8px}
.psub p{margin:7px 0 0;font-size:14px;line-height:1.65;color:var(--ink-3)}
.psub p.psp{color:var(--ink);font-weight:700}
.psub label{display:flex;flex-wrap:wrap;align-items:center;gap:10px;margin:14px 0 0;font-size:14.5px;font-weight:700}
.psub input[type=text]{height:40px;min-width:220px;padding:0 12px;border:1px solid var(--line);border-radius:8px;background:transparent;color:inherit;font:inherit;font-weight:500}
.psub input[type=file]{max-width:100%;font:inherit;font-size:14px;font-weight:500}
.psub .plist{margin:8px 0 0;font-size:13.5px;color:var(--ink-3)}
.psub .pacts{display:flex;flex-wrap:wrap;align-items:center;gap:14px;margin-top:16px}
.psub .pbtn:disabled{opacity:.45;cursor:not-allowed}
.psub .pst{font-size:14px;font-weight:700}
.psub .pst.ok{color:#1f7a4d}
.psub .pst.no{color:#b3261e}
.psub a{color:inherit}
"""


def box(n, label, base):
    exam_id = base if n == 1 else '%s-%d' % (base, n) if base else ''
    h = ('<div class="psub" id="m%d-psub" data-exam="%s" data-mt="%d" data-sp="%s">\n'
         '<h3>풀이 PDF 제출하기<em>소피아 독일어학원 수강생 전용</em></h3>\n'
         '<p>이 제출하기는 <b>소피아 독일어학원 수강생 전용</b>입니다. 수강생이 아니라면 제출하지 마십시오.</p>\n'
         '<p>종이 시험지에 푼 답안을 스캔하거나 사진으로 찍어 PDF로 만든 뒤 올리면 선생님 메일로 전송됩니다. PDF만 올릴 수 있고(최대 5개, 합계 15MB 이하), 점수는 자동으로 계산되지 않습니다. 선생님이 확인한 뒤 알려 드립니다.</p>\n') % (n, label, n, exam_id)
    if base:
        h += ('<p class="psp">말하기 기록: 확인 중</p>\n'
              '<p>말하기는 <a href="%s#%s" target="_blank" rel="noopener">말하기 실전 연습</a>(수강생 로그인)에서 연습합니다. 같은 브라우저에서 연습한 기록은 제출할 때 자동으로 함께 전송됩니다.</p>\n') % (SPRECHEN, exam_id)
    h += ('<label>이름 <input class="pname" type="text" maxlength="60" autocomplete="name"></label>\n'
          '<label>PDF 파일 <input class="pfile" type="file" accept="application/pdf,.pdf" multiple></label>\n'
          '<div class="plist"></div>\n'
          '<div class="pacts"><button class="start pbtn" type="button">선생님께 제출하기</button><span class="pst" role="status"></span></div>\n'
          '</div>\n')
    return h


JS = r"""<script id="soda-psub">
(function () {
  var URL = '__URL__', MAX_FILES = 5, MAX_BYTES = 15 * 1024 * 1024;
  function $(s, r) { return (r || document).querySelector(s); }
  function mb(b) { return (b / 1048576).toFixed(1) + 'MB'; }
  function nowStr() { var d = new Date(), p = function (n) { return (n < 10 ? '0' : '') + n; }; return d.getFullYear() + '-' + p(d.getMonth() + 1) + '-' + p(d.getDate()) + ' ' + p(d.getHours()) + ':' + p(d.getMinutes()); }
  function speaking(box) {
    var id = box.getAttribute('data-sp'); if (!id) return null;
    try { var v = window.localStorage.getItem('soda-sprechen:mdt:' + id), o = v ? JSON.parse(v) : null; return o && o.text ? o : null; } catch (e) { return null; }
  }
  function showSp(box) {
    var el = $('.psp', box); if (!el) return;
    var sp = speaking(box);
    el.textContent = sp ? '말하기 기록 포함: Teil ' + (sp.teile || []).join(', ') + ' (' + (sp.user || '') + ' · ' + String(sp.updated || '').slice(0, 10) + ')' : '말하기 기록: 이 브라우저에는 이 Modelltest의 말하기 연습 기록이 없습니다.';
  }
  function status(box, cls, msg) { var s = $('.pst', box); s.className = 'pst' + (cls ? ' ' + cls : ''); s.textContent = msg; }
  function isPdf(f) { return f.type === 'application/pdf' || /\.pdf$/i.test(f.name); }
  function check(box) {
    var inp = $('.pfile', box), fs = Array.prototype.slice.call(inp.files || []), list = $('.plist', box), total = 0, bad = '';
    fs.forEach(function (f) { total += f.size; if (!isPdf(f)) bad = 'PDF 파일만 올릴 수 있습니다: ' + f.name; });
    if (!bad && fs.length > MAX_FILES) bad = 'PDF는 ' + MAX_FILES + '개까지 올릴 수 있습니다.';
    if (!bad && total > MAX_BYTES) bad = '파일이 너무 큽니다(' + mb(total) + '). 합계 15MB 이하로 줄여 주십시오.';
    list.textContent = fs.length ? fs.map(function (f) { return f.name + ' (' + mb(f.size) + ')'; }).join(' · ') : '';
    if (bad) status(box, 'no', bad); else status(box, '', '');
    return { files: fs, ok: !bad && fs.length > 0, bad: bad };
  }
  function read(f) {
    return new Promise(function (res, rej) {
      var r = new FileReader();
      r.onload = function () { var s = String(r.result), i = s.indexOf(','); res({ name: f.name, size: f.size, data: s.slice(i + 1) }); };
      r.onerror = function () { rej(new Error('read')); };
      r.readAsDataURL(f);
    });
  }
  function send(box) {
    var nm = ($('.pname', box).value || '').replace(/\s+/g, ' ').trim(), c = check(box), btn = $('.pbtn', box);
    if (!nm) { status(box, 'no', '이름을 입력하십시오.'); $('.pname', box).focus(); return; }
    if (!c.files.length) { status(box, 'no', 'PDF 파일을 선택하십시오.'); return; }
    if (!c.ok) return;
    if (!URL) { status(box, 'no', '제출 주소가 아직 설정되지 않았습니다. 선생님께 문의하십시오.'); return; }
    try { window.localStorage.setItem('soda-psub-name', nm); } catch (e) { }
    btn.disabled = true; status(box, '', '파일을 읽고 있습니다…');
    var done = false, timer = setTimeout(function () { fail('응답이 없습니다. 인터넷 연결을 확인하고 다시 눌러 주십시오.'); }, 180000);
    function fail(msg) { if (done) return; done = true; clearTimeout(timer); btn.disabled = false; status(box, 'no', msg); }
    Promise.all(c.files.map(read)).then(function (files) {
      if (done) return;
      var sp = speaking(box);
      var payload = {
        v: 1, kind: 'modelltest-paper', exam: box.getAttribute('data-exam'), mt: box.getAttribute('data-mt'), name: nm, finished: nowStr(), files: files,
        speaking: sp ? { label: sp.label || '', teile: sp.teile || [], user: sp.user || '', updated: sp.updated || '', text: sp.text } : null,
        page: location.href.split('#')[0]
      };
      status(box, '', '제출하고 있습니다… 파일이 크면 시간이 걸립니다. 창을 닫지 마십시오.');
      return fetch(URL, { method: 'POST', body: JSON.stringify(payload) }).then(function (r) { return r.json(); }).then(function (j) {
        if (done) return;
        if (!j || !j.ok) { fail((j && j.message) || '제출하지 못했습니다. 잠시 뒤 다시 눌러 주십시오.'); return; }
        done = true; clearTimeout(timer); btn.disabled = false;
        $('.pfile', box).value = ''; $('.plist', box).textContent = '';
        status(box, 'ok', nowStr() + ' 제출했습니다.' + (sp ? ' 말하기 기록도 함께 제출되었습니다.' : ''));
      });
    }).catch(function () { fail('제출하지 못했습니다. 인터넷 연결을 확인하고 다시 눌러 주십시오. 파일이 크면 용량을 줄여 다시 시도하십시오.'); });
  }
  document.addEventListener('click', function (e) {
    var t = e.target, g = t.closest && t.closest('[data-psub-go]');
    if (g) { e.preventDefault(); var b = document.getElementById(g.getAttribute('data-psub-go')); if (b) { b.scrollIntoView({ behavior: 'smooth', block: 'center' }); showSp(b); } return; }
    var btn = t.closest && t.closest('.psub .pbtn'); if (btn) send(btn.closest('.psub'));
  });
  document.addEventListener('change', function (e) { var t = e.target; if (t.classList && t.classList.contains('pfile')) check(t.closest('.psub')); });
  var boxes = document.querySelectorAll('.psub'), nm = '';
  try { nm = window.localStorage.getItem('soda-psub-name') || ''; } catch (e) { }
  for (var i = 0; i < boxes.length; i++) { showSp(boxes[i]); if (nm) $('.pname', boxes[i]).value = nm; }
  window.addEventListener('hashchange', function () { var b = document.querySelectorAll('.psub'); for (var i = 0; i < b.length; i++) showSp(b[i]); });
})();
</script>
"""


def submit_url(folder):
    s = open(os.path.join(folder, 'digital.html'), encoding='utf-8').read()
    m = re.search(r"var SUBMIT_URL = '([^']*)';", s)
    assert m, (folder, 'SUBMIT_URL')
    return m.group(1)


def patch(folder, label, base):
    p = os.path.join(folder, 'index.html')
    s = open(p, encoding='utf-8').read()
    if MARK in s:
        return 'skip'
    # CSS (soda-dark 앞)
    a = '<style id="soda-dark">'
    assert s.count(a) == 1, (p, 'soda-dark')
    s = s.replace(a, '<style id="soda-psub-css">\n' + CSS + '</style>\n' + a)
    # 페이퍼 구역마다 상자와 바로가기
    count = 0
    for m in list(re.finditer(r'<section class="page mdt" id="m(\d+)"', s))[::-1]:
        n = int(m.group(1))
        i = m.start(); j = s.index('</section>', i)
        sec = s[i:j]
        k = sec.rindex('<div class="foot">')
        pre = sec[:k].rstrip()
        assert pre.endswith('</div>'), (p, n, 'main end')
        sec2 = pre[:-6] + box(n, label, base) + '</div>\n' + sec[k:]
        go = '<a class="btn ghost" href="#d%d">디지털로 풀기</a>' % n
        assert sec2.count(go) == 1, (p, n, 'actions')
        sec2 = sec2.replace(go, go + '<a class="btn ghost" href="#%d" data-psub-go="m%d-psub">풀이 PDF 제출</a>' % (n, n))
        s = s[:i] + sec2 + s[j:]
        count += 1
    # 스크립트(</body> 앞)
    assert s.count('</body>') == 1, (p, 'body')
    s = s.replace('</body>', JS.replace('__URL__', submit_url(folder)) + '</body>')
    open(p, 'w', encoding='utf-8').write(s)
    return 'patched %d sections' % count


if __name__ == '__main__':
    for fo in (sys.argv[1:] or list(APPS)):
        print(fo, patch(fo, *APPS[fo]))
