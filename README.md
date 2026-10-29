# SODA Modelltest · Goethe-Zertifikat

Goethe-Zertifikat A2, B1, B2 모의고사(Modelltest)입니다. 페이퍼 시험(PDF, 듣기 MP3)과 디지털 시험 화면을 함께 제공합니다. Sophia Deutsch Akademie의 SODA Lehrwerk 목차에서 열립니다.

용량 한도(GitHub Pages 1 GB) 때문에 Goethe와 telc는 저장소를 나눴습니다. telc 모의고사는 `SODA-TELC` 저장소에 있습니다.

| 폴더 | 내용 |
|---|---|
| `goethe-a2/` | Goethe-Zertifikat A2, Modelltest 5개와 쓰기 시험 대비 가이드(`schreiben-guide.html`) |
| `goethe-b1/` | Goethe-Zertifikat B1, Modelltest 10개 (예전 단일 파일 오프라인 버전 `… offline.html` 포함, 목차에서는 연결하지 않음) |
| `goethe-b2/` | Goethe-Zertifikat B2, Modelltest 5개 |
| `tools/` | 다크 모드 스위치와 「목차」 버튼을 넣는 `soda-theme.py` |
| `assets/` | 시작 페이지의 로고와 글꼴 |
| `index.html` | 이 저장소의 시작 페이지 (세 앱 목록, Lehrwerk 목차로 가는 링크) |

## 웹 주소

Settings → Pages → Build and deployment에서 Source를 `Deploy from a branch`, Branch를 `main` / `/ (root)`로 지정합니다.

- 시작 페이지: https://sophiadeutschakademie.github.io/SODA-Goethe/
- 각 앱: 위 주소 뒤에 폴더 이름을 붙입니다. 예) https://sophiadeutschakademie.github.io/SODA-Goethe/goethe-b1/
- Lehrwerk 목차: https://sophiadeutschakademie.github.io/SODA-Lehrwerk/#inhalt

`.nojekyll` 파일은 숨김 파일이라 폴더에서 안 보일 수 있어요. 지우지 마세요.

## 앱 폴더 구성

```
index.html       표지, 응시 방식, 페이퍼 목록, 디지털 목록, Modelltest별 페이지
digital.html     디지털 시험 화면
<시험> Modelltest N.pdf, N.k.mp3   문제지와 듣기 음원
digital-src/     digital.html과 index.html의 원본(데이터, 템플릿, 빌드 스크립트)
```

앱을 다시 만드는 방법과 새 Modelltest를 추가하는 방법은 각 앱 폴더의 `digital-src/README.md`에 있습니다.

## 같은 주소를 쓰는 저장 공간

학생의 답과 결과는 학생 브라우저에만 저장되고 앱마다 저장 이름이 다릅니다(`sodaGZA2.v1.`, `sodaGZB1.v1.`, `sodaGZB2.v1.`). 다크 모드 선택(`soda-theme`)은 Lehrwerk의 모든 앱이 함께 씁니다. Lehrwerk와 이 저장소는 같은 `sophiadeutschakademie.github.io` 주소 아래에 있어서 저장된 답과 다크 모드 선택이 그대로 이어집니다. 사용자 지정 도메인으로 바꾸면 이 연결이 끊어질 수 있어요.

## 다크 모드와 목차 버튼

`tools/soda-theme.py`가 모든 앱에 다크 모드 스위치를 넣고, 목록 페이지(`index.html`)에는 「목차」 버튼도 넣습니다. 버튼은 Lehrwerk 목차로 돌아가며, 주소는 `tools/soda-theme.py` 맨 위의 `LEHRWERK_TOC`에 있습니다. 각 앱의 `build-digital.py`와 `build-index.py`가 파일을 쓴 뒤 자동으로 부르고, 직접 쓸 때는 다음처럼 실행합니다. 몇 번을 실행해도 결과가 같습니다.

```
python3 tools/soda-theme.py goethe-b1/index.html --kind index
```
