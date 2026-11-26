#!/usr/bin/env python3
"""디지털 시험 화면(template.html과 digital.html)에 「시험이 끝나면 결과를 선생님께 자동 제출」을 넣습니다.

저장소 루트에서 실행합니다.
  python3 tools/add-auto-submit.py telc-b1 telc-b2 telc-c1-hs        (SODA-TELC)
  python3 tools/add-auto-submit.py goethe-a2 goethe-b1 goethe-b2     (SODA-Goethe)

- tools/add-submit.py 로 「선생님께 제출하기」가 이미 들어 있는 화면에 넣습니다.
- 학생이 Abgeben을 누르거나 시험 시간이 다 되면(finish) 같은 전송 코드(postSubmission)로 결과를 자동 전송합니다.
  실패하면 4초 뒤 한 번 더 시도하고, 그래도 안 되면 결과 화면에서 직접 제출하라고 안내합니다.
- 시작 화면에 이름을 적지 않았으면 이름 칸에 「(이름 없음)」으로 보냅니다. 결과 화면의 제출하기는 다시 제출용으로 남습니다.
- 이미 들어 있으면 건너뛰므로 몇 번을 실행해도 결과가 같습니다.
- build-digital.py 로 digital.html 을 다시 만들면 template.html 의 내용이 그대로 들어갑니다(이 스크립트를 다시 실행할 필요 없음).
"""
import os, re, sys

MARK = 'function autoSubmit('

COMMON = r"""  /* 제출 내용을 Apps Script 웹 앱에 보냅니다. 직접 제출하기와 시험 종료 때의 자동 제출이 함께 씁니다. */
  function postSubmission(res, nm, onOk, onFail) {
    var sp = speakingRec();
    var body = resultText(res).replace(/^Name: .*$/m, 'Name: ' + nm);
    var payload = {
      v: 1, kind: 'modelltest', exam: EXAM_LABEL, mt: String(R.mt), module: MOD[R.mod].name, name: nm, finished: res.finished,
      used: fmt(res.used), byTime: !!res.byTime, body: body,
      speaking: sp ? { label: sp.label || '', teile: sp.teile || [], user: sp.user || '', updated: sp.updated || '', text: sp.text } : null,
      page: location.href.split('#')[0]
    };
    var done = false;
    var timer = setTimeout(function () { fail('응답이 없습니다. 인터넷 연결을 확인하고 다시 눌러 주십시오.'); }, 60000);
    function fail(msg) { if (done) return; done = true; clearTimeout(timer); onFail(msg); }
    fetch(SUBMIT_URL, { method: 'POST', body: JSON.stringify(payload) }).then(function (r) { return r.json(); }).then(function (j) {
      if (done) return;
      if (!j || !j.ok) { fail((j && j.message) || '제출하지 못했습니다. 잠시 뒤 다시 눌러 주십시오.'); return; }
      done = true; clearTimeout(timer);
      var at = nowStr();
      if (nm !== NO_NAME) lsSet('name', nm);
      lsSet(RESULT_KEY + '.sent', { finished: res.finished, at: at });
      onOk(at, sp);
    }, function () { fail('서버에 연결하지 못했습니다. 인터넷 연결을 확인하고 다시 눌러 주십시오. 계속 안 되면 위의 txt 저장으로 파일을 받아 선생님께 보내 주십시오.'); });
  }
  /* 시험이 끝나면(제출하기를 눌렀거나 시간이 다 되었을 때) 결과를 자동으로 선생님께 보냅니다. 실패하면 4초 뒤 한 번 더 보냅니다. */
  function autoSubmit(res) {
    if (!SUBMIT_URL) return;
    var nm = (res.name || '').replace(/\s+/g, ' ').trim() || NO_NAME, tries = 0;
    function show(cls, msg) { var el = $('#autoSt'); if (el) { el.className = 'st ' + cls; el.textContent = msg; } }
    show('', '선생님께 자동 제출하고 있습니다…');
    (function go() {
      tries++;
      postSubmission(res, nm, function (at, sp) {
        show('ok', at + ' 선생님께 자동 제출했습니다.' + (sp ? ' 말하기 기록도 함께 제출되었습니다.' : ''));
      }, function (msg) {
        if (tries < 2) { show('', '자동 제출을 다시 시도하고 있습니다…'); setTimeout(go, 4000); return; }
        show('no', '자동 제출하지 못했습니다. 결과 화면에서 「선생님께 제출하기」를 눌러 주십시오. (' + msg + ')');
      });
    })();
  }
"""

NEW_CLICK = """      btn.disabled = true; st.className = 'st'; st.textContent = '제출하고 있습니다…';
      postSubmission(res, nm, function (at, sp) {
        btn.disabled = false; btn.textContent = '다시 제출하기';
        st.className = 'st ok'; st.textContent = at + ' 제출했습니다.' + (sp ? ' 말하기 기록도 함께 제출되었습니다.' : '');
      }, function (msg) { btn.disabled = false; st.className = 'st no'; st.textContent = msg; });
"""

OLD_END = "(res.byTime ? '시험 시간이 끝나 자동으로 제출되었습니다.' : '제출이 완료되었습니다.') + ' 결과 화면에서 ' + (M.writing ? '답안을 확인하고 선생님께 제출할 수 있습니다.' : '점수와 정답을 확인하세요.') + '</p>' +"
NEW_END = """(res.byTime ? '시험 시간이 끝났습니다. ' : '') + '결과는 선생님께 자동으로 제출됩니다. 결과 화면에서 ' + (M.writing ? '답안을 확인할 수 있습니다.' : '점수와 정답을 확인하세요.') + '</p>' +
      '<p class="st" id="autoSt" role="status" style="margin:6px 0 0"></p>' +"""
OLD_SB = "이 선생님 메일로 전송됩니다. 제출 전에 이름을 확인하십시오.</p>';"
NEW_SB = "이 선생님 메일로 전송됩니다. 시험이 끝나면 자동으로 제출되며, 이름을 고치거나 ✓/✗를 바꾼 뒤에는 다시 제출하십시오.</p>';"
CSS_A = ".sub .st.no{color:#b3261e}\n"
CSS_N = CSS_A + "#autoSt{font-size:13.5px;font-weight:700}\n#autoSt.ok{color:#1f7a4d}\n#autoSt.no{color:#b3261e}\n"


def patch(path):
    s = open(path, encoding='utf-8').read()
    if MARK in s:
        return 'skip'
    # 1) 이름 없음 표시
    m = re.search(r"  var SPRECHEN_ID = '[^']*';\n", s)
    assert m and len(re.findall(r"  var SPRECHEN_ID = '[^']*';\n", s)) == 1, (path, 'SPRECHEN_ID')
    s = s[:m.end()] + "  var NO_NAME = '(이름 없음)';\n" + s[m.end():]
    # 2) 공통 전송 함수
    a = '  function submitBox(res) {'
    assert s.count(a) == 1, (path, 'submitBox')
    s = s.replace(a, COMMON + a)
    # 3) 직접 제출하기가 같은 함수를 쓰게 함
    i = s.index("      var sp = speakingRec();\n      var body = txt.replace(")
    j = s.index("    });\n  }\n\n  function showResult(")
    s = s[:i] + NEW_CLICK + s[j:]
    # 4) 시험 종료 때 자동 제출
    s, n = re.subn(r'(S = null;\s*showEnd\(res\);)(\s*\})', r'\1\n    autoSubmit(res);\2', s)
    assert n == 1, (path, 'finish')
    # 5) 끝 화면 문구와 상태 줄
    assert s.count(OLD_END) == 1, (path, 'end msg')
    s = s.replace(OLD_END, NEW_END)
    assert s.count(OLD_SB) == 1, (path, 'submitBox msg')
    s = s.replace(OLD_SB, NEW_SB)
    # 6) CSS
    assert s.count(CSS_A) == 1, (path, 'css')
    s = s.replace(CSS_A, CSS_N)
    open(path, 'w', encoding='utf-8').write(s)
    return 'patched'


if __name__ == '__main__':
    for fo in sys.argv[1:]:
        for p in (os.path.join(fo, 'digital-src', 'template.html'), os.path.join(fo, 'digital.html')):
            print(p, patch(p))
