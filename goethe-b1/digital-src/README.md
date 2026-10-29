# digital-src

디지털 시험 화면(`digital.html`)의 원본입니다. 학생은 이 폴더를 쓰지 않습니다.

| 파일 | 내용 |
|---|---|
| `template.html` | 시험 화면 코드. 모든 Modelltest가 함께 씁니다 |
| `data/mtN.json` | Modelltest N의 지문, 문항, 정답, 쓰기 과제, 모범 답안. 형식은 `SCHEMA.md` |
| `build-digital.py` | `data`와 `template.html`을 합쳐 이 앱 폴더의 `digital.html`을 만듭니다. 음원 길이는 이 폴더의 MP3에서 읽습니다 |
| `guidelib.py` | 두 가이드 페이지가 함께 쓰는 헬퍼(표, 섹션, 페이지 틀)와 기본 CSS |
| `guide-data.json`, `build-guide.py` | 쓰기 시험 대비 가이드(`../schreiben-guide.html`)의 글과 모범 답안 30편, 이를 HTML로 만드는 스크립트. 모범 답안의 단어 수가 범위 안인지 빌드할 때 검사합니다 |
| `sprechen-data.json`, `build-sprechen.py` | 말하기 시험 대비 가이드(`../sprechen-guide.html`)의 글, Teil 1 대화 10편, Teil 2 발표 10편, Teil 3 문답 10편, 이를 HTML로 만드는 스크립트. 발표 단어 수를 빌드할 때 검사합니다 |
| `validate.py` | `data/mtN.json` 형식 검사 |
| `logo-small.png` | 시험 화면 왼쪽 위 로고 |
| `fonts/pretendard-soda.woff` | 시험 화면 글꼴 Pretendard 중 화면에 쓰는 글자만 담은 파일(SIL OFL 1.1, `fonts/Pretendard-OFL.txt`) |
| `make-font.py` | 화면에 새 한글 문구를 넣어 글자가 빠지면 Pretendard 원본에서 글꼴 파일을 다시 만듭니다 |

## 다시 만들기

```
python3 digital-src/validate.py digital-src/data/mt*.json
python3 digital-src/build-digital.py
python3 digital-src/build-guide.py
python3 digital-src/build-sprechen.py
```

`ffprobe`(ffmpeg)가 필요합니다.

`python3 ...` 명령은 이 앱 폴더(`<앱 이름>/`)에서 실행합니다. 파일을 다시 만들 때마다 `../tools/soda-theme.py`가 Lehrwerk 공통 다크 모드 스위치를 자동으로 넣습니다.

## 새 Modelltest 추가

1. 이 앱 폴더에 `Goethe B1 Modelltest N.pdf`와 `Goethe B1 Modelltest N.1.mp3` ~ `N.4.mp3`를 올립니다.
2. `SCHEMA.md` 형식으로 `data/mtN.json`을 만들고 `validate.py`로 확인합니다. 정답은 PDF의 Lösungsschlüssel과 대조합니다.
3. `build-digital.py`를 실행합니다.
4. `index.html`에 페이퍼 페이지(`#N`)와 디지털 페이지(`#dN`)를 기존 항목과 같은 형식으로 추가합니다.

시험 화면 주소는 `digital.html#N-lesen`, `digital.html#N-hoeren`, `digital.html#N-schreiben`입니다. 학생의 답과 결과는 학생 브라우저에만 저장됩니다.
