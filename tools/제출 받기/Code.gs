/**
 * SODA Modelltest 제출 받기
 * Modelltest 디지털 시험 화면(SODA-Goethe, SODA-TELC)의 「선생님께 제출하기」가 보낸 내용을 선생님 메일로 전달합니다.
 * 필기 결과(점수·답안·작성한 글)와 말하기 실전 연습 기록이 한 통에 들어갑니다. 설정 방법은 같은 폴더의 「설정 안내.md」입니다.
 */

// 제출 내용을 받을 메일 주소. 비워 두면 이 스크립트를 배포한 Google 계정의 메일로 옵니다.
var TEACHER_EMAIL = '';
// 제출 기록을 스프레드시트에도 쌓으려면 스프레드시트 주소 중간의 ID를 넣습니다(선택). 비워 두면 메일만 보냅니다.
var SHEET_ID = '';

var MAX_BODY = 150000;

function doGet() {
  return out_({ ok: true, message: 'SODA Modelltest 제출 받기가 켜져 있습니다.' });
}

function doPost(e) {
  try {
    var d = JSON.parse((e && e.postData && e.postData.contents) || '{}');
    var name = clean_(d.name, 60), exam = clean_(d.exam, 40), mt = clean_(d.mt, 6), mod = clean_(d.module, 20);
    if (d.v !== 1 || d.kind !== 'modelltest' || !name || !exam || !mt || !mod || typeof d.body !== 'string') {
      return out_({ ok: false, message: '제출 형식이 맞지 않습니다.' });
    }
    if (d.body.length > MAX_BODY || (d.speaking && String(d.speaking.text || '').length > MAX_BODY)) {
      return out_({ ok: false, message: '제출 내용이 너무 깁니다.' });
    }
    // 같은 내용을 몇 초 안에 두 번 받으면 한 번만 처리합니다(더블 클릭 방지).
    var cache = CacheService.getScriptCache();
    var key = Utilities.base64EncodeWebSafe(Utilities.computeDigest(Utilities.DigestAlgorithm.MD5, [name, exam, mt, mod, d.finished, d.body.length].join('|')));
    if (cache.get(key)) return out_({ ok: true });
    cache.put(key, '1', 20);

    var to = TEACHER_EMAIL || Session.getEffectiveUser().getEmail();
    var sp = d.speaking && d.speaking.text ? d.speaking : null;
    var subject = '[SODA Modelltest] ' + exam + ' Modelltest ' + mt + ' · ' + mod + ' · ' + name;
    var parts = [
      '학생: ' + name,
      '시험: ' + exam + ' Modelltest ' + mt + ' · ' + mod,
      '제출 시각: ' + clean_(d.finished, 30) + ' · 풀이 시간 ' + clean_(d.used, 10) + (d.byTime ? ' (시간 종료)' : ''),
      '말하기 기록: ' + (sp ? 'Teil ' + (sp.teile || []).join(', ') + ' 포함 (연습 계정 ' + clean_(sp.user, 40) + ')' : '없음'),
      '', '==== 필기 결과 ====', d.body
    ];
    if (sp) parts.push('', '==== 말하기 실전 연습 기록 ====', sp.text);
    var body = parts.join('\n');
    var fname = (exam + ' Modelltest ' + mt + ' ' + mod + ' ' + name + '.txt').replace(/[\\\/:*?"<>|_]+/g, ' ');
    MailApp.sendEmail({
      to: to, subject: subject, body: body, name: 'SODA Modelltest',
      attachments: [Utilities.newBlob(body, 'text/plain', fname)]
    });

    if (SHEET_ID) {
      var sh = SpreadsheetApp.openById(SHEET_ID).getSheets()[0];
      sh.appendRow([new Date(), name, exam, mt, mod, clean_(d.finished, 30), clean_(d.used, 10), sp ? 'Teil ' + (sp.teile || []).join(',') : '', clean_(d.page, 200)]);
    }
    return out_({ ok: true });
  } catch (err) {
    return out_({ ok: false, message: '서버에서 처리하지 못했습니다. 잠시 뒤 다시 시도해 주십시오.' });
  }
}

function clean_(v, n) { return String(v == null ? '' : v).replace(/[\r\n\t]+/g, ' ').trim().slice(0, n); }
function out_(o) { return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON); }
