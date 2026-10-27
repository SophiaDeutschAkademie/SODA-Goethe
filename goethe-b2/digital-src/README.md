# digital-src

디지털 시험 화면(`digital.html`)과 목록 페이지(`index.html`)의 원본입니다. 학생은 이 폴더를 쓰지 않습니다.

| 파일 | 내용 |
|---|---|
| `template.html` | 시험 화면 코드. 모든 Modelltest가 함께 씁니다 |
| `data/mtN.json` | Modelltest N의 지문, 문항, 정답, 쓰기 과제, 모범 답안, 목록 페이지용 `index` 블록. 형식은 `SCHEMA.md` |
| `build-digital.py` | `data`와 `template.html`을 합쳐 이 앱 폴더의 `digital.html`을 만듭니다. 음원 길이는 이 폴더의 MP3에서 읽습니다 |
| `build-index.py` | `data`, PDF, MP3로 이 앱 폴더의 `index.html`(표지·응시 방식·목록·시험별 페이지)을 만듭니다 |
| `index-style.css` | `index.html`의 스타일 |
| `validate.py` | `data/mtN.json` 형식 검사 |
| `logo-small.png`, `logo-index.png` | 시험 화면, 목록 페이지의 로고 |
| `fonts/pretendard-soda.woff`, `fonts/pretendard-index.woff` | Pretendard 중 시험 화면, 목록 페이지에 쓰는 글자만 담은 파일(SIL OFL 1.1, `fonts/Pretendard-OFL.txt`) |
| `make-font.py` | 시험 화면에 새 한글 문구를 넣어 글자가 빠지면 Pretendard 원본에서 글꼴 파일을 다시 만듭니다 |

## 다시 만들기

```
python3 digital-src/validate.py digital-src/data/mt*.json
python3 digital-src/build-digital.py
python3 digital-src/build-index.py
```

`ffprobe`(ffmpeg)가 필요합니다.

`python3 ...` 명령은 이 앱 폴더(`<앱 이름>/`)에서 실행합니다. 파일을 다시 만들 때마다 `../tools/soda-theme.py`가 Lehrwerk 공통 다크 모드 스위치를 자동으로 넣습니다.

## 새 Modelltest 추가

1. 이 앱 폴더에 `Goethe B2 Modelltest N.pdf`와 `Goethe B2 Modelltest N.1.mp3` ~ `N.4.mp3`를 올립니다.
2. `SCHEMA.md` 형식으로 `data/mtN.json`을 만들고 `validate.py`로 확인합니다. 정답은 PDF의 Lösungsschlüssel과 대조합니다.
3. `build-digital.py`, `build-index.py`를 차례로 실행합니다.

시험 화면 주소는 `digital.html#N-lesen`, `digital.html#N-hoeren`, `digital.html#N-schreiben`입니다. 학생의 답과 결과는 학생 브라우저에만 저장됩니다.

PDF 쪽 번호(Lösungsschlüssel 17, Musterlösungen 18, Kommentar 20, Hörtexte 22 등)는 `build-digital.py`의 `PAGES`와 `build-index.py`의 `PDF_PAGES`에 있습니다. 쪽 구성이 다른 시험을 추가하면 이 값을 고칩니다.
