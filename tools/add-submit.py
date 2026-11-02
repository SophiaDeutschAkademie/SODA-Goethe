#!/usr/bin/env python3
"""디지털 시험 화면(template.html과 digital.html)의 결과 화면에 「선생님께 제출하기」를 넣습니다.

저장소 루트에서 실행합니다.
  python3 tools/add-submit.py goethe-a2 goethe-b1 goethe-b2        (SODA-Goethe)
  python3 tools/add-submit.py telc-b1 telc-b2 telc-c1-hs           (SODA-TELC)

- 옛 「메일로 보내기」(받는 사람이 비어 있던 mailto 버튼)를 대체합니다.
- 제출 내용(필기 결과·답안)과 같은 브라우저에 저장된 말하기 실전 연습 기록을 한 건으로 묶어 Google Apps Script 웹 앱에 보내고,
  웹 앱이 선생님 메일로 전달합니다. 스크립트와 설정 방법은 tools/제출 받기/ 에 있습니다.
- 이미 들어 있으면 건너뛰므로 몇 번을 실행해도 결과가 같습니다.
- build-digital.py 로 digital.html 을 다시 만들면 template.html 의 내용이 그대로 들어갑니다(이 스크립트를 다시 실행할 필요 없음).
"""
import re, sys, os

# 제출 주소(Apps Script 웹 앱 배포 주소). 비워 두면 버튼이 안내 문구만 보여 줍니다.
SUBMIT_URL = ''
SPRECHEN = 'https://sophiadeutschakademie.github.io/SODA-Lehrwerk/sprechen/'
APPS = {  # 폴더: (시험 이름, 말하기 연습 앱의 시험 id 앞부분, 비어 있으면 말하기 연습 없음)
    'goethe-a2': ('Goethe A2', 'goethe-a2'),
    'goethe-b1': ('Goethe B1', 'goethe-b1'),
    'goethe-b2': ('Goethe B2', 'goethe-b2'),
    'telc-b1': ('telc B1', 'telc-b1'),
    'telc-b2': ('telc B2', 'telc-b2'),
    'telc-c1-hs': ('telc C1 Hochschule', ''),
}
MARK = 'SODA-SUBMIT'

CSS = """.sub{margin:22px 0 0;padding:16px 18px;border:1px solid var(--line);border-radius:8px}
.sub h3{margin:0 0 4px;font-size:16px}
.sub h3 em{font-style:normal;font-size:12.5px;font-weight:700;color:var(--muted);margin-left:8px}
.sub p{margin:6px 0 0;font-size:13.5px;line-height:1.6;color:var(--muted)}
.sub p.mem{color:inherit;font-weight:700}
.sub .nm{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin:12px 0 4px;font-size:14px;font-weight:700}
.sub .nm input{height:38px;min-width:200px;padding:0 12px;border:1px solid var(--line);border-radius:6px;background:transparent;color:inherit;font:inherit;font-weight:500}
.sub .st{font-size:13.5px;font-weight:700}
.sub .st.ok{color:#1f7a4d}
.sub .st.no{color:#b3261e}
.sub a{color:inherit;text-decoration:underline}
"""

JS = r"""  /* ---------- SODA-SUBMIT: 선생님께 제출하기 (소피아 독일어학원 수강생 전용) ---------- */
  function speakingRec() {
    if (!SPRECHEN_ID) return null;
    var id = String(R.mt) === '1' ? SPRECHEN_ID : SPRECHEN_ID + '-' + R.mt;
    try {
      var v = window.localStorage.getItem('soda-sprechen:mdt:' + id);
      var o = v ? JSON.parse(v) : null;
      return o && o.text ? o : null;
    } catch (e) { return null; }
  }
  function submitBox(res) {
    var sp = speakingRec(), sent = lsGet(RESULT_KEY + '.sent');
    var done = sent && sent.finished === res.finished;
    var h = '<div class="sub" id="subbox"><h3>선생님께 제출하기<em>소피아 독일어학원 수강생 전용</em></h3>' +
      '<p>이 제출하기는 <b>소피아 독일어학원 수강생 전용</b>입니다. 수강생이 아니라면 제출하지 말고 위의 복사·txt 저장으로 결과를 보관하십시오.</p>' +
      '<p>제출하면 ' + (M.writing ? '작성한 글' : '점수와 답안') + '이 선생님 메일로 전송됩니다. 제출 전에 이름을 확인하십시오.</p>';
    if (SPRECHEN_ID) {
      h += '<p class="mem">' + (sp ? '말하기 기록 포함: Teil ' + sp.teile.join(', ') + ' (' + esc(sp.user || '') + ' · ' + esc(String(sp.updated || '').slice(0, 10)) + ')' : '말하기 기록: 이 브라우저에는 이 Modelltest의 말하기 연습 기록이 없습니다.') + '</p>' +
        '<p>말하기는 <a href="' + SPRECHEN + '#' + (String(R.mt) === '1' ? SPRECHEN_ID : SPRECHEN_ID + '-' + R.mt) + '" target="_blank" rel="noopener">말하기 실전 연습</a>(수강생 로그인)에서 연습합니다. 같은 브라우저에서 연습한 기록은 제출할 때 자동으로 함께 전송됩니다.</p>';
    }
    h += '<label class="nm">이름 <input id="subName" type="text" maxlength="60" autocomplete="name" value="' + esc(res.name || '') + '"></label>' +
      '<div class="acts" style="margin-top:8px"><button class="btn pri" id="sb" type="button">' + (done ? '다시 제출하기' : '선생님께 제출하기') + '</button>' +
      '<span class="st' + (done ? ' ok' : '') + '" id="subSt" role="status">' + (done ? esc(sent.at) + ' 제출했습니다.' : '') + '</span></div></div>';
    return h;
  }
  function bindSubmit(res, txt) {
    var btn = $('#sb'), st = $('#subSt'), name = $('#subName');
    if (!btn) return;
    btn.addEventListener('click', function () {
      var nm = (name.value || '').replace(/\s+/g, ' ').trim();
      if (!nm) { toast('이름을 입력하십시오.', true); name.focus(); return; }
      if (!SUBMIT_URL) { st.className = 'st no'; st.textContent = '제출 주소가 아직 설정되지 않았습니다. 선생님께 문의하십시오.'; return; }
      var sp = speakingRec();
      var body = txt.replace(/^Name: .*$/m, 'Name: ' + nm);
      var payload = {
        v: 1, kind: 'modelltest', exam: EXAM_LABEL, mt: String(R.mt), module: MOD[R.mod].name, name: nm, finished: res.finished,
        used: fmt(res.used), byTime: !!res.byTime, body: body,
        speaking: sp ? { label: sp.label || '', teile: sp.teile || [], user: sp.user || '', updated: sp.updated || '', text: sp.text } : null,
        page: location.href.split('#')[0]
      };
      btn.disabled = true; st.className = 'st'; st.textContent = '제출하고 있습니다…';
      var done = false;
      var timer = setTimeout(function () { if (!done) fail('응답이 없습니다. 인터넷 연결을 확인하고 다시 눌러 주십시오.'); }, 60000);
      function fail(msg) { if (done) return; done = true; clearTimeout(timer); btn.disabled = false; st.className = 'st no'; st.textContent = msg; }
      fetch(SUBMIT_URL, { method: 'POST', body: JSON.stringify(payload) }).then(function (r) { return r.json(); }).then(function (j) {
        if (done) return;
        if (!j || !j.ok) { fail((j && j.message) || '제출하지 못했습니다. 잠시 뒤 다시 눌러 주십시오.'); return; }
        done = true; clearTimeout(timer); btn.disabled = false; btn.textContent = '다시 제출하기';
        var at = nowStr();
        lsSet('name', nm); lsSet(RESULT_KEY + '.sent', { finished: res.finished, at: at });
        st.className = 'st ok'; st.textContent = at + ' 제출했습니다.' + (sp ? ' 말하기 기록도 함께 제출되었습니다.' : '');
      }, function () { fail('서버에 연결하지 못했습니다. 인터넷 연결을 확인하고 다시 눌러 주십시오. 계속 안 되면 위의 txt 저장으로 파일을 받아 선생님께 보내 주십시오.'); });
    });
  }

"""


def patch(path, label, base):
    s = open(path, encoding='utf-8').read()
    if MARK in s:
        return 'skip'
    # 1) 상수
    m = re.search(r"  /\* 선생님 이메일 주소를 넣으면[^\n]*\n  var LEHRER_MAIL = '';\n", s)
    assert m, (path, 'LEHRER_MAIL')
    consts = ("  /* " + MARK + ": 제출 주소(Google Apps Script 웹 앱). tools/제출 받기/ 설정 안내.md 참고. */\n"
              "  var SUBMIT_URL = '%s';\n  var EXAM_LABEL = '%s';\n  var SPRECHEN_ID = '%s';\n  var SPRECHEN = '%s';\n") % (SUBMIT_URL, label, base, SPRECHEN)
    s = s[:m.start()] + consts + s[m.end():]
    # 2) CSS
    a = '.acts{display:flex'
    assert s.count(a) == 1, (path, 'css anchor', s.count(a))
    s = s.replace(a, CSS + a)
    # 3) 함수
    f = re.search(r"\n  function showResult\(", s)
    assert f, (path, 'showResult')
    s = s[:f.start() + 1] + JS + s[f.start() + 1:]
    # 4) 결과 화면: 제출 상자 + 버튼 정리
    b = "    h += '<div class=\"acts\" style=\"margin-top:22px\"><button class=\"btn pri\" id=\"cp\""
    assert s.count(b) == 1, (path, 'acts anchor', s.count(b))
    s = s.replace(b, "    h += submitBox(res);\n" + b)
    ml = '<button class="btn" id="ml" type="button">메일로 보내기</button>'
    assert s.count(ml) == 1, (path, 'ml button')
    s = s.replace(ml, '')
    # 5) 핸들러
    hd = re.search(r"    \$\('#ml'\)\.addEventListener\('click', function \(\) \{\n.*?\n    \}\);\n", s, re.S)
    assert hd, (path, 'ml handler')
    s = s[:hd.start()] + "    bindSubmit(res, txt);\n" + s[hd.end():]
    # 6) 안내 문구(있을 때만)
    s = s.replace("답안을 확인하고 선생님께 보낼 수 있습니다.", "답안을 확인하고 선생님께 제출할 수 있습니다.")
    s = s.replace("아래 버튼으로 선생님께 답안을 보내 첨삭을 받으세요.", "수강생은 아래 「선생님께 제출하기」로 답안을 보내 첨삭을 받으세요.")
    open(path, 'w', encoding='utf-8').write(s)
    return 'patched'


def main(folders):
    for fo in folders:
        label, base = APPS[fo]
        for rel in ('digital-src/template.html', 'digital.html'):
            p = os.path.join(fo, rel)
            print(p, patch(p, label, base))


if __name__ == '__main__':
    main(sys.argv[1:] or list(APPS))
