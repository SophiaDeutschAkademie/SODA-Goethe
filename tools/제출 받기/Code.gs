/**
 * SODA Modelltest 제출 받기
 * Modelltest 시험 화면(SODA-Goethe, SODA-TELC)의 제출을 선생님 메일로 전달합니다.
 *  - 디지털 시험: 「선생님께 제출하기」가 보낸 필기 결과(점수·답안·작성한 글)와 말하기 실전 연습 기록이 한 통에 들어갑니다.
 *  - 페이퍼 시험: 학생이 올린 풀이 PDF가 첨부되어 오고, 말하기 실전 연습 기록이 있으면 함께 들어갑니다.
 *  - SODA-Lehrwerk 학습 기록: Hörtraining·Lesetraining의 「메일로 보내기」가 보낸 학습 기록이 txt·json 첨부와 함께 옵니다.
 * 설정 방법은 같은 폴더의 「설정 안내.md」입니다.
 */

// 제출 내용을 받을 메일 주소. 비워 두면 이 스크립트를 배포한 Google 계정의 메일로 옵니다.
var TEACHER_EMAIL = 'info@sophiadeutsch.com';
// 제출 기록을 스프레드시트에도 쌓으려면 스프레드시트 주소 중간의 ID를 넣습니다(선택). 비워 두면 메일만 보냅니다.
var SHEET_ID = '';

var MAX_BODY = 150000;               // 글 내용 최대 글자 수
var MAX_FILES = 5;                   // 페이퍼 제출 PDF 최대 개수
var MAX_PDF_BYTES = 15 * 1024 * 1024; // 페이퍼 제출 PDF 합계 최대 크기
var MAX_DATA = 3000000;              // Lehrwerk 학습 기록 원본(json) 최대 글자 수

function doGet() {
  return out_({ ok: true, message: 'SODA Modelltest 제출 받기가 켜져 있습니다.' });
}

function doPost(e) {
  try {
    var d = JSON.parse((e && e.postData && e.postData.contents) || '{}');
    if (d && d.app === 'lehrwerk') return lehrwerk_(d);
    if (d && d.kind === 'modelltest-paper') return paper_(d);
    return digital_(d);
  } catch (err) {
    return out_({ ok: false, message: '서버에서 처리하지 못했습니다. 잠시 뒤 다시 시도해 주십시오.' });
  }
}

/* ---------- 디지털 시험 ---------- */
function digital_(d) {
  var name = clean_(d.name, 60), exam = clean_(d.exam, 40), mt = clean_(d.mt, 6), mod = clean_(d.module, 20);
  if (d.v !== 1 || d.kind !== 'modelltest' || !name || !exam || !mt || !mod || typeof d.body !== 'string') {
    return out_({ ok: false, message: '제출 형식이 맞지 않습니다.' });
  }
  if (d.body.length > MAX_BODY || (d.speaking && String(d.speaking.text || '').length > MAX_BODY)) {
    return out_({ ok: false, message: '제출 내용이 너무 깁니다.' });
  }
  if (dup_([name, exam, mt, mod, d.finished, d.body.length].join('|'))) return out_({ ok: true });

  var sp = d.speaking && d.speaking.text ? d.speaking : null;
  var subject = '[SODA Modelltest] ' + exam + ' Modelltest ' + mt + ' · ' + mod + ' · ' + name;
  var parts = [
    '학생: ' + name,
    '시험: ' + exam + ' Modelltest ' + mt + ' · ' + mod,
    '제출 시각: ' + clean_(d.finished, 30) + ' · 풀이 시간 ' + clean_(d.used, 10) + (d.byTime ? ' (시간 종료)' : ''),
    '말하기 기록: ' + spLine_(sp),
    '', '==== 필기 결과 ====', d.body
  ];
  if (sp) parts.push('', '==== 말하기 실전 연습 기록 ====', sp.text);
  var body = parts.join('\n');
  var fname = safe_(exam + ' Modelltest ' + mt + ' ' + mod + ' ' + name) + '.txt';
  MailApp.sendEmail({
    to: to_(), subject: subject, body: body, name: 'SODA Modelltest',
    attachments: [Utilities.newBlob(body, 'text/plain', fname)]
  });
  log_([new Date(), name, exam, mt, mod, clean_(d.finished, 30), clean_(d.used, 10), sp ? 'Teil ' + (sp.teile || []).join(',') : '', clean_(d.page, 200)]);
  return out_({ ok: true });
}

/* ---------- 페이퍼 시험: 풀이 PDF 첨부 ---------- */
function paper_(d) {
  var name = clean_(d.name, 60), exam = clean_(d.exam, 40), mt = clean_(d.mt, 6);
  var files = d.files;
  if (d.v !== 1 || !name || !exam || !mt || !Array.isArray(files) || !files.length) {
    return out_({ ok: false, message: '제출 형식이 맞지 않습니다.' });
  }
  if (files.length > MAX_FILES) return out_({ ok: false, message: 'PDF는 ' + MAX_FILES + '개까지 올릴 수 있습니다.' });
  if (d.speaking && String(d.speaking.text || '').length > MAX_BODY) return out_({ ok: false, message: '제출 내용이 너무 깁니다.' });

  var blobs = [], total = 0, names = [];
  for (var i = 0; i < files.length; i++) {
    var f = files[i] || {};
    if (typeof f.data !== 'string' || !f.data) return out_({ ok: false, message: '파일을 읽지 못했습니다.' });
    var bytes = Utilities.base64Decode(f.data);
    // PDF 파일은 %PDF 로 시작합니다.
    if (bytes.length < 5 || bytes[0] !== 37 || bytes[1] !== 80 || bytes[2] !== 68 || bytes[3] !== 70) {
      return out_({ ok: false, message: 'PDF 파일만 올릴 수 있습니다.' });
    }
    total += bytes.length;
    if (total > MAX_PDF_BYTES) return out_({ ok: false, message: '파일이 너무 큽니다. 합계 ' + Math.round(MAX_PDF_BYTES / 1048576) + 'MB 이하로 줄여 주십시오.' });
    var fn = safe_(String(f.name || ('답안 ' + (i + 1))).replace(/\.pdf$/i, '')).slice(0, 80) + '.pdf';
    names.push(fn);
    blobs.push(Utilities.newBlob(bytes, 'application/pdf', fn));
  }
  if (dup_(['paper', name, exam, mt, d.finished, total].join('|'))) return out_({ ok: true });

  var sp = d.speaking && d.speaking.text ? d.speaking : null;
  var subject = '[SODA Modelltest 답안 PDF] ' + exam + ' Modelltest ' + mt + ' · ' + name;
  var parts = [
    '학생: ' + name,
    '시험: ' + exam + ' Modelltest ' + mt + ' (페이퍼 시험)',
    '제출 시각: ' + clean_(d.finished, 30),
    '첨부 PDF ' + names.length + '개: ' + names.join(', '),
    '말하기 기록: ' + spLine_(sp)
  ];
  if (sp) {
    parts.push('', '==== 말하기 실전 연습 기록 ====', sp.text);
    blobs.push(Utilities.newBlob(parts.join('\n'), 'text/plain', safe_(exam + ' Modelltest ' + mt + ' ' + name + ' 말하기 기록') + '.txt'));
  }
  MailApp.sendEmail({ to: to_(), subject: subject, body: parts.join('\n'), name: 'SODA Modelltest', attachments: blobs });
  log_([new Date(), name, exam, mt, '페이퍼 PDF ' + names.length + '개', clean_(d.finished, 30), '', sp ? 'Teil ' + (sp.teile || []).join(',') : '', clean_(d.page, 200)]);
  return out_({ ok: true });
}

/* ---------- SODA-Lehrwerk 학습 기록 (Hörtraining · Lesetraining) ---------- */
function lehrwerk_(d) {
  var name = clean_(d.name, 60), app = clean_(d.appName, 40), sent = clean_(d.finished, 30);
  if (d.v !== 1 || !name || !app || typeof d.body !== 'string' || !d.body) {
    return out_({ ok: false, message: '보내기 형식이 맞지 않습니다.' });
  }
  if (d.body.length > MAX_BODY || (typeof d.data === 'string' && d.data.length > MAX_DATA)) {
    return out_({ ok: false, message: '기록이 너무 깁니다. 「파일로 저장」으로 받은 파일을 선생님께 보내 주십시오.' });
  }
  if (dup_(['lehrwerk', name, app, sent, d.body.length].join('|'))) return out_({ ok: true });

  var base = safe_(app + ' 학습 기록 ' + name + ' ' + sent);
  var att = [Utilities.newBlob(d.body, 'text/plain', base + '.txt')];
  if (typeof d.data === 'string' && d.data) att.push(Utilities.newBlob(d.data, 'application/json', base + '.json'));
  MailApp.sendEmail({
    to: to_(), subject: '[SODA 학습 기록] ' + app + ' · ' + name, body: d.body, name: 'SODA Lehrwerk', attachments: att
  });
  log_([new Date(), name, 'Lehrwerk ' + app, '학습 기록', clean_(d.count, 8) + '건', sent, '', '', clean_(d.page, 200)]);
  return out_({ ok: true });
}

/* ---------- 도우미 ---------- */
function to_() { return TEACHER_EMAIL || Session.getEffectiveUser().getEmail(); }
function spLine_(sp) { return sp ? 'Teil ' + (sp.teile || []).join(', ') + ' 포함 (연습 계정 ' + clean_(sp.user, 40) + ')' : '없음'; }
// 같은 내용을 몇 초 안에 두 번 받으면 한 번만 처리합니다(더블 클릭 방지). 이미 받았으면 true.
function dup_(s) {
  var cache = CacheService.getScriptCache();
  var key = Utilities.base64EncodeWebSafe(Utilities.computeDigest(Utilities.DigestAlgorithm.MD5, s));
  if (cache.get(key)) return true;
  cache.put(key, '1', 20);
  return false;
}
function log_(row) {
  if (!SHEET_ID) return;
  SpreadsheetApp.openById(SHEET_ID).getSheets()[0].appendRow(row);
}
function safe_(s) { return String(s).replace(/[\\\/:*?"<>|_]+/g, ' ').replace(/\s+/g, ' ').trim(); }
function clean_(v, n) { return String(v == null ? '' : v).replace(/[\r\n\t]+/g, ' ').trim().slice(0, n); }
function out_(o) { return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON); }
