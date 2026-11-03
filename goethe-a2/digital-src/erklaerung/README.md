# erklaerung (Goethe-Zertifikat A2)

Modelltest별 해설 페이지(`Goethe A2 Modelltest N 해설.html`)의 원본입니다. Modelltest 1–10이 있습니다.

| 파일 | 내용 |
|---|---|
| `erkN_lesen.py` | Modelltest N의 Lesen 1–20 해설 |
| `erkN_hoeren.py` | Modelltest N의 Hören 1–20 해설, Schreiben(Aufgabe 1·2), Sprechen(Teil 1–3) |
| `FORMAT.md` | 해설 데이터 형식과 쓰는 규칙 |
| `build.py` | 위 데이터와 `../data/mtN.json`, `../../img/`의 그림을 합쳐 HTML 한 파일을 만듭니다 |
| `style.css` | 해설 페이지 스타일(telc 해설과 같은 틀 + 그림 배치) |

## 다시 만들기

앱 폴더(`goethe-a2/`)에서 실행합니다. Pretendard 원본(`PretendardVariable.ttf`)이 필요합니다.

```
for n in 1 2 3 4 5 6 7 8 9 10; do python3 -I digital-src/erklaerung/build.py . $n PretendardVariable.ttf "Goethe A2 Modelltest $n 해설.html" web; done
python3 digital-src/build-index.py
python3 ../tools/add-sprechen-links.py
python3 ../tools/add-paper-submit.py goethe-a2
```

- `web`을 붙이면 그림을 `img/` 경로로 연결하고, 오른쪽 위에 「Modelltest N」(시험 페이지로 돌아가기) 버튼과 접속 집계 태그를 넣습니다. 빼면 그림까지 파일 안에 넣은 오프라인판(약 1 MB)이 됩니다.
- `build.py`는 정답(Hören 2는 예시를 뺀 다섯 명), Lesen 인용, 모범 답안 문단 수를 검사하고 어긋나면 멈춥니다.
- `build-index.py`는 해설 파일이 있는 시험 페이지에 「해설」 버튼(Lösungsschlüssel 앞)을 넣습니다.
