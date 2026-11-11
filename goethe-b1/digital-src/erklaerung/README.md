# erklaerung (Goethe-Zertifikat B1)

Modelltest별 해설 페이지(`Goethe B1 Modelltest N 해설.html`)의 원본입니다.

| 파일 | 내용 |
|---|---|
| `erkN_lesen.py` | Modelltest N의 Lesen 1–30 해설(근거 문장, 정답 이유, 함정, 어휘) |
| `erkN_hoeren.py` | Modelltest N의 Hören 1–30 해설, Schreiben(Aufgabe 1–3), Sprechen(Teil 1–3) |
| `gemeinsam.py` | 모든 회차가 함께 쓰는 글: 함정 유형 여덟 가지, 쓰기 채점 기준, 말하기의 고정된 과제와 공통 요령·표현 |
| `FORMAT.md` | 해설 데이터 형식과 쓰는 규칙 |
| `build.py` | 위 데이터와 `../data/mtN.json`을 합쳐 HTML 한 파일을 만듭니다 |
| `check.py` | 해설 글 속 인용, 어조, 말하기 과제의 독일어를 살펴보는 점검 도구 |
| `add-buttons.py` | `../../index.html`의 각 Modelltest 페이지에 「해설」 버튼(Lösungsschlüssel 앞)을 넣습니다 |
| `style.css` | 해설 페이지 스타일(Goethe A2·telc 해설과 같은 틀) |

## 다시 만들기

앱 폴더(`goethe-b1/`)에서 실행합니다. Pretendard 원본(`PretendardVariable.ttf`, https://github.com/orioncactus/pretendard)이 필요합니다. 페이지에 쓰인 글자만 골라 파일 안에 넣습니다.

```
for n in 1 2 3 4 5 6 7 8 9 10; do python3 -I digital-src/erklaerung/build.py . $n PretendardVariable.ttf "Goethe B1 Modelltest $n 해설.html" web; done
python3 -I digital-src/erklaerung/check.py .
python3 digital-src/erklaerung/add-buttons.py
```

- 마지막 인자 `web`은 저장소용입니다. 오른쪽 위에 「Modelltest N」(시험 페이지로 돌아가기) 버튼과 접속 집계 태그를 넣습니다. 빼면 학생에게 파일로 주는 오프라인판이 됩니다.
- `build.py`는 만들기 전에 해설의 정답을 `mtN.json`과 대조하고, Lesen·Hören 인용이 본문과 대본(`hoertexte`)에 그대로 있는지, Hören 4 인용을 정답인 사람이 말했는지, 쓰기 Leitpunkt와 모범 답안 문단 수가 맞는지 확인합니다. 하나라도 다르면 멈춥니다.
- 문항 카드의 「함정 유형」은 `mtN.json`의 `kommentar`(시험지 20–21쪽)에서 가져옵니다.
- Goethe B1의 `index.html`은 손으로 관리하는 파일입니다(`build-index.py` 없음). `add-buttons.py`는 해설 파일이 있는 회차에만 버튼을 넣고, 이미 있으면 건너뜁니다. 몇 번을 실행해도 결과가 같습니다.
