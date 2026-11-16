/* Goethe B1 작문 연습: 자동 저장, 내 글 전체, 예시 보기, 복사·txt 저장, 선생님께 제출하기(소피아 독일어학원 수강생 전용) */
(function () {
  'use strict';
  var D = JSON.parse(document.getElementById('sw-data').textContent);
  var SUBMIT_URL = '__SUBMIT_URL__';
  var PREFIX = 'sodaGZB1.v1.', KEY = 'uebung.' + D.mt;

  function lsGet(k) { try { var v = window.localStorage.getItem(PREFIX + k); return v ? JSON.parse(v) : null; } catch (e) { return null; } }
  function lsSet(k, v) { try { window.localStorage.setItem(PREFIX + k, JSON.stringify(v)); return true; } catch (e) { return false; } }
  function lsDel(k) { try { window.localStorage.removeItem(PREFIX + k); } catch (e) {} }
  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function words(s) { s = String(s || '').trim(); return s ? s.split(/\s+/).length : 0; }
  function clean(s) { return String(s || '').replace(/\r/g, '').replace(/\s+/g, ' ').trim(); }
  function pad(n) { return (n < 10 ? '0' : '') + n; }
  function nowStr() { var d = new Date(); return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate()) + ' ' + pad(d.getHours()) + ':' + pad(d.getMinutes()); }

  var S = lsGet(KEY);
  if (!S || typeof S !== 'object' || !S.t || typeof S.t !== 'object') S = { v: 1, t: {} };
  var saveTimer = null;
  function saveNow() { clearTimeout(saveTimer); saveTimer = null; S.at = new Date().toISOString(); lsSet(KEY, S); }
  function saveSoon() { clearTimeout(saveTimer); saveTimer = setTimeout(saveNow, 350); }
  window.addEventListener('pagehide', function () { if (saveTimer) saveNow(); });
  document.addEventListener('visibilitychange', function () { if (document.visibilityState === 'hidden' && saveTimer) saveNow(); });

  var toastEl = $('#toast'), toastTimer = null;
  function toast(msg, bad) {
    if (!toastEl) return;
    toastEl.textContent = msg; toastEl.className = 'toast' + (bad ? ' no' : ''); toastEl.hidden = false;
    clearTimeout(toastTimer); toastTimer = setTimeout(function () { toastEl.hidden = true; }, 2600);
  }

  function val(k) { return clean(S.t[k]); }
  function partsOf(a) { return a.parts.filter(function (p) { return p.k; }); }
  function filled(a) { return partsOf(a).filter(function (p) { return val(p.k); }).length; }

  /* 블록(줄·문단)을 이어 붙여 글 한 편을 만듭니다. 비어 있는 번호는 글에서 빠집니다 */
  function letterText(a) {
    var out = [];
    a.layout.forEach(function (b) {
      var t = b.items.map(function (it) { return it.fix !== undefined ? it.fix : val(it.k); }).filter(Boolean).join(' ');
      if (!t) return;
      if (b.tight && out.length) out[out.length - 1] += '\n' + t; else out.push(t);
    });
    return out.join('\n\n');
  }
  function letterHtml(a) {
    var out = [];
    a.layout.forEach(function (b) {
      var bits = b.items.map(function (it) {
        if (it.fix !== undefined) return esc(it.fix);
        var v = val(it.k);
        return v ? esc(v) : '<span class="miss"><span class="pn">' + it.k.split('-')[1] + '</span>아직 쓰지 않음</span>';
      });
      var h = bits.join(' ');
      if (b.tight && out.length) out[out.length - 1] = out[out.length - 1].replace(/<\/p>$/, '\n' + h + '</p>');
      else out.push('<p' + (b.line ? ' class="gr"' : '') + '>' + h + '</p>');
    });
    return out.join('');
  }
  function wordsOf(a) { return filled(a) ? words(letterText(a)) : 0; }

  function refresh(a) {
    var n = filled(a), tot = partsOf(a).length, w = wordsOf(a);
    var pr = $('#prog' + a.no); if (pr) { pr.textContent = '작성 ' + n + ' / ' + tot; pr.classList.toggle('full', n === tot); }
    var ml = $('#mine' + a.no + ' .ml'); if (ml) ml.innerHTML = letterHtml(a);
    var wc = $('#mine' + a.no + ' .wc');
    if (wc) {
      wc.textContent = w + '단어';
      wc.className = 'wc' + (!n ? '' : w < a.lo ? ' lo' : w > a.hi ? ' hi' : ' ok');
    }
    var sc = $('#subcnt'); if (sc) sc.textContent = D.aufg.map(function (x) { return 'Aufgabe ' + x.no + ' ' + filled(x) + '/' + partsOf(x).length; }).join(' · ');
  }
  function grow(t) { t.style.height = 'auto'; t.style.height = (t.scrollHeight + 2) + 'px'; }

  var byKey = {};
  D.aufg.forEach(function (a) { partsOf(a).forEach(function (p) { byKey[p.k] = a; }); });

  $$('textarea.ans').forEach(function (t) {
    var k = t.getAttribute('data-k');
    if (S.t[k]) t.value = S.t[k];
    var li = t.closest('.part'), pv = li && $('.pv', li);
    function mark() { if (li) li.classList.toggle('filled', !!clean(t.value)); if (pv) pv.textContent = t.value; }
    mark();
    t.addEventListener('input', function () {
      S.t[k] = t.value; saveSoon(); grow(t); mark(); refresh(byKey[k]);
    });
    t.addEventListener('blur', function () { if (saveTimer) saveNow(); });
  });
  function growAll() { $$('textarea.ans').forEach(grow); }
  growAll();
  window.addEventListener('resize', function () { clearTimeout(growAll.t); growAll.t = setTimeout(growAll, 150); });
  D.aufg.forEach(refresh);

  /* 예시 보기 */
  function setEx(btn, on) {
    var box = document.getElementById(btn.getAttribute('aria-controls'));
    if (!box) return;
    box.hidden = !on; btn.setAttribute('aria-expanded', on ? 'true' : 'false'); btn.textContent = on ? '예시 접기' : '예시 보기';
  }
  $$('.exb').forEach(function (b) { b.addEventListener('click', function () { setEx(b, b.getAttribute('aria-expanded') !== 'true'); }); });
  var all = $('#exall');
  if (all) all.addEventListener('click', function () {
    var on = all.getAttribute('aria-pressed') !== 'true';
    $$('.exb').forEach(function (b) { setEx(b, on); });
    $$('details.b1f').forEach(function (d) { d.open = on; });
    all.setAttribute('aria-pressed', on ? 'true' : 'false'); all.textContent = on ? '예시 모두 접기' : '예시 모두 보기';
    document.body.classList.toggle('exall', on);
  });

  /* 복사·txt 저장 */
  function copyText(txt) {
    function fallback() {
      var ta = document.createElement('textarea'); ta.value = txt; ta.setAttribute('readonly', ''); ta.style.position = 'fixed'; ta.style.top = '0'; ta.style.opacity = '0';
      document.body.appendChild(ta); ta.select();
      var ok = false; try { ok = document.execCommand('copy'); } catch (e) { ok = false; }
      document.body.removeChild(ta);
      toast(ok ? '복사했습니다.' : '복사하지 못했습니다. 글을 직접 선택해 복사하십시오.', !ok);
    }
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(txt).then(function () { toast('복사했습니다.'); }, fallback);
    else fallback();
  }
  function downloadText(txt, name) {
    try {
      var blob = new Blob([txt], { type: 'text/plain;charset=utf-8' });
      var a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = name;
      document.body.appendChild(a); a.click();
      setTimeout(function () { URL.revokeObjectURL(a.href); document.body.removeChild(a); }, 800);
    } catch (e) { toast('파일을 저장하지 못했습니다.', true); }
  }
  $$('.cp').forEach(function (b) {
    b.addEventListener('click', function () {
      var a = D.aufg[Number(b.getAttribute('data-a')) - 1];
      if (!filled(a)) { toast('아직 쓴 문장이 없습니다.', true); return; }
      copyText(letterText(a));
    });
  });

  function report(name) {
    var L = [D.title + ' (A2 → B1)', '이름: ' + (name || ''), '보낸 시각: ' + nowStr(),
      '작성: ' + D.aufg.map(function (a) { return 'Aufgabe ' + a.no + ' ' + filled(a) + '/' + partsOf(a).length; }).join(' · ')];
    D.aufg.forEach(function (a) {
      L.push('', '==== Aufgabe ' + a.no + ' · ' + a.title + ' ====');
      partsOf(a).forEach(function (p) {
        L.push('', p.n + ' ' + p.role, 'A2: ' + p.a2, '표현: ' + p.use, '학생: ' + (val(p.k) || '(쓰지 않음)'));
      });
      L.push('', '---- 완성한 글 (' + wordsOf(a) + '단어, 목표 약 ' + a.target + '단어) ----', filled(a) ? letterText(a) : '(쓰지 않음)');
    });
    return L.join('\n');
  }
  var nameIn = $('#subName');
  var saved = lsGet('name');
  if (nameIn && typeof saved === 'string') nameIn.value = saved;
  function curName() { return nameIn ? clean(nameIn.value) : ''; }
  function fileName() { var n = curName(); return D.title + (n ? ' ' + n : '') + '.txt'; }
  function anyFilled() { return D.aufg.some(function (a) { return filled(a) > 0; }); }
  var cpall = $('#cpall'), dl = $('#dl'), reset = $('#reset');
  if (cpall) cpall.addEventListener('click', function () { if (!anyFilled()) { toast('아직 쓴 문장이 없습니다.', true); return; } copyText(report(curName())); });
  if (dl) dl.addEventListener('click', function () { if (!anyFilled()) { toast('아직 쓴 문장이 없습니다.', true); return; } downloadText(report(curName()), fileName()); });
  if (reset) reset.addEventListener('click', function () {
    if (!anyFilled()) { toast('지울 내용이 없습니다.'); return; }
    if (!window.confirm('이 Modelltest에서 쓴 문장을 모두 지울까요? 지운 내용은 되돌릴 수 없습니다.')) return;
    S = { v: 1, t: {} }; lsDel(KEY); lsDel(KEY + '.sent');
    $$('textarea.ans').forEach(function (t) { t.value = ''; grow(t); var li = t.closest('.part'); if (li) li.classList.remove('filled'); var pv = li && $('.pv', li); if (pv) pv.textContent = ''; });
    D.aufg.forEach(refresh);
    var st = $('#subSt'); if (st) { st.className = 'st'; st.textContent = ''; }
    var sb = $('#sb'); if (sb) sb.textContent = '선생님께 제출하기';
    toast('지웠습니다.');
  });

  /* 선생님께 제출하기 (소피아 독일어학원 수강생 전용) */
  var sb = $('#sb'), stEl = $('#subSt');
  var sent = lsGet(KEY + '.sent');
  if (sent && sent.at && sb) { sb.textContent = '다시 제출하기'; stEl.className = 'st ok'; stEl.textContent = sent.at + ' 제출했습니다.'; }
  if (sb) sb.addEventListener('click', function () {
    var nm = curName();
    if (!nm) { toast('이름을 입력하십시오.', true); if (nameIn) nameIn.focus(); return; }
    if (!anyFilled()) { toast('아직 쓴 문장이 없습니다.', true); return; }
    if (!SUBMIT_URL || SUBMIT_URL.indexOf('https://') !== 0) { stEl.className = 'st no'; stEl.textContent = '제출 주소가 아직 설정되지 않았습니다. 선생님께 문의하십시오.'; return; }
    if (saveTimer) saveNow();
    var at = nowStr(), body = report(nm), cnt = D.aufg.reduce(function (s, a) { return s + filled(a); }, 0);
    var payload = {
      v: 1, app: 'lehrwerk', appName: D.title, kind: 'modelltest', exam: 'Goethe B1', mt: String(D.mt), module: '작문 연습',
      name: nm, finished: at, used: '', count: String(cnt), body: body, page: location.href.split('#')[0]
    };
    sb.disabled = true; stEl.className = 'st'; stEl.textContent = '제출하고 있습니다…';
    var done = false;
    var timer = setTimeout(function () { fail('응답이 없습니다. 인터넷 연결을 확인하고 다시 눌러 주십시오.'); }, 60000);
    function fail(msg) { if (done) return; done = true; clearTimeout(timer); sb.disabled = false; stEl.className = 'st no'; stEl.textContent = msg; }
    fetch(SUBMIT_URL, { method: 'POST', body: JSON.stringify(payload) }).then(function (r) { return r.json(); }).then(function (j) {
      if (done) return;
      if (!j || !j.ok) { fail((j && j.message) || '제출하지 못했습니다. 잠시 뒤 다시 눌러 주십시오.'); return; }
      done = true; clearTimeout(timer); sb.disabled = false; sb.textContent = '다시 제출하기';
      lsSet('name', nm); lsSet(KEY + '.sent', { at: at, count: cnt });
      stEl.className = 'st ok'; stEl.textContent = at + ' 제출했습니다.';
    }, function () { fail('서버에 연결하지 못했습니다. 인터넷 연결을 확인하고 다시 눌러 주십시오. 계속 안 되면 「txt 저장」으로 파일을 받아 선생님께 보내 주십시오.'); });
  });
})();
