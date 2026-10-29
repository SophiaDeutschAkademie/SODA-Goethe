# digital-src

디지털 시험 화면(`digital.html`)과 목록 페이지(`index.html`)의 원본입니다. 학생은 이 폴더를 쓰지 않습니다.

| 파일 | 내용 |
|---|---|
| `template.html` | 시험 화면 코드. 모든 Modelltest가 함께 씁니다 |
| `data/mtN.json` | Modelltest N의 지문, 문항, 정답, 쓰기 과제, 모범 답안, 목록 페이지용 `index` 블록. 형식은 `SCHEMA.md` |
| `build-digital.py` | `data`와 `template.html`을 합쳐 이 앱 폴더의 `digital.html`을 만듭니다. 음원 길이는 이 폴더의 MP3에서 읽습니다 |
| `build-index.py` | `data`, PDF, MP3로 이 앱 폴더의 `index.html`(표지·응시 방식·목록·시험별 페이지)을 만듭니다 |
| `index-style.css` | `index.html`의 스타일 |
| `validate.py` | `data/mtN.json` 형식 검사. 이 폴더의 PDF가 있으면 정답 40개를 Lösungsschlüssel와 대조합니다 |
| `logo-small.png`, `logo-index.png` | 시험 화면, 목록 페이지의 로고 |
| `fonts/pretendard-soda.woff`, `fonts/pretendard-index.woff` | Pretendard 중 시험 화면, 목록 페이지에 쓰는 글자만 담은 파일(SIL OFL 1.1, `fonts/Pretendard-OFL.txt`) |
| `guide-data.json`, `build-guide.py` | 쓰기 시험 대비 가이드(`../schreiben-guide.html`)의 글과 모범 답안 20편, 이를 HTML로 만드는 스크립트. 모범 답안의 단어 수(Anrede·본문·Gruß·이름 합계)를 세어 Teil 1 20~30, Teil 2 30~40을 벗어나면 멈춥니다 |
| `make-font.py` | 시험 화면에 새 한글 문구를 넣어 글자가 빠지면 Pretendard 원본에서 글꼴 파일을 다시 만듭니다 |

그림은 `../img/`에 있습니다. Lesen Teil 1의 사진(`mtN-lesen-foto.jpg`), Lesen Teil 4의 광고 6장(`mtN-anzeige-a..f.png`), Hören Teil 2의 그림 a–i(`mtN-hoeren2-*.webp`), Hören Teil 3의 그림(`mtN-hoeren3-<문항><a|b|c>.webp`)입니다. 앞의 사진·광고는 PDF에서 잘라 낸 것이고, Hören Teil 2·3의 그림 120장은 SODA 삽화 그림체로 새로 만든 것입니다(Recraft 4.1 Flash로 생성, 시계·달력·가격표·식탁 그림은 코드로 직접 그림).

## 다시 만들기

```
python3 digital-src/validate.py digital-src/data/mt*.json
python3 digital-src/build-digital.py
python3 digital-src/build-index.py
python3 digital-src/build-guide.py
```

`ffprobe`(ffmpeg)가 필요합니다.

`python3 ...` 명령은 이 앱 폴더(`<앱 이름>/`)에서 실행합니다. 파일을 다시 만들 때마다 `../tools/soda-theme.py`가 Lehrwerk 공통 다크 모드 스위치를 자동으로 넣습니다.

## 새 Modelltest 추가

1. 이 앱 폴더에 `Goethe A2 Modelltest N.pdf`와 `Goethe A2 Modelltest N.1.mp3` ~ `N.4.mp3`를 올립니다.
2. PDF에서 사진, 광고, 그림을 잘라 `img/`에 넣습니다(파일 이름 규칙은 위).
3. `SCHEMA.md` 형식으로 `data/mtN.json`을 만들고 `validate.py`로 확인합니다. 정답은 PDF의 Lösungsschlüssel과 대조합니다.
4. `build-digital.py`, `build-index.py`를 차례로 실행합니다.

시험 화면 주소는 `digital.html#N-lesen`, `digital.html#N-hoeren`, `digital.html#N-schreiben`입니다. 학생의 답과 결과는 학생 브라우저에만 저장됩니다(키 접두어 `sodaGZA2.v1.`).

PDF 쪽 번호(Lösungsschlüssel 17, Musterlösungen 18, Musterdialoge 19, Kommentar 20, Hörtexte 22 등)는 `build-digital.py`의 `PAGES`와 `build-index.py`의 `PDF_PAGES`에 있습니다. 쪽 구성이 다른 시험을 추가하면 이 값을 고칩니다.

## 시험 구성(A2)

| 모듈 | 시간 | 구성 | 점수 |
|---|---|---|---|
| Lesen | 30분 | Teil 1 신문 기사 1–5, Teil 2 안내판 6–10, Teil 3 이메일 11–15, Teil 4 광고 16–20(해당 없음 X 한 문항) | 20문항 × 1,25 = 25점 |
| Hören | 약 30분 | Teil 1 짧은 글 1–5(2회), Teil 2 그림 연결 6–10(1회), Teil 3 짧은 대화 11–15(1회), Teil 4 인터뷰 Ja/Nein 16–20(2회) | 20문항 × 1,25 = 25점 |
| Schreiben | 30분 | Aufgabe 1 SMS 20–30 Wörter(약 10분), Aufgabe 2 E-Mail 30–40 Wörter(약 20분) | 25점(선생님 채점) |
| Sprechen | 약 15분 | Teil 1 Fragen zur Person, Teil 2 Von sich erzählen, Teil 3 Gemeinsam etwas planen | 25점 |

합격은 전체 60점 이상(100점 만점)입니다.
