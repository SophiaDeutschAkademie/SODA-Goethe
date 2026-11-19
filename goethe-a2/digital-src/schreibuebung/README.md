# schreibuebung (Goethe-Zertifikat A2 작문 연습)

Modelltest별 작문 연습 페이지(`Goethe A2 Modelltest N 작문 연습.html`)의 원본입니다. Schreiben Aufgabe 1(SMS)과 Aufgabe 2(E-Mail)마다 세 가지 내용은 다 갖췄지만 문장이 아주 단순한 A1 답안을 주고, 학생이 번호마다 주어진 A2 표현으로 고쳐 씁니다. 지금은 Modelltest I–V에 있습니다.

| 파일 | 내용 |
|---|---|
| `swN.py` | Modelltest N의 A1 답안, 번호마다 쓸 A2 표현·뜻·도움말·A2 예시, 과제별 요약(형식은 `FORMAT.md`) |
| `gemeinsam.py` | 모든 회차가 함께 쓰는 글: 사용법, A1과 A2의 차이, 제출 전 확인 |
| `build.py` | 위 데이터와 `../data/mtN.json`(과제 원문, 단어 수 범위), `../erklaerung/erkN_hoeren.py`(과제 제목, Punkt 번역), `../../index.html`(시험지 쪽수)을 합쳐 HTML 한 파일을 만듭니다 |
| `style.css` | 이 페이지에만 쓰는 스타일. 해설 페이지의 `../erklaerung/style.css` 뒤에 붙습니다 |
| `app.js` | 자동 저장, 내 글 전체와 단어 수, 예시 보기, 복사·txt 저장, 선생님께 제출하기 |
| `add-links.py` | `../../index.html`의 Modelltest 페이지에 「작문 연습」 줄을 넣습니다 |

## 다시 만들기

앱 폴더(`goethe-a2/`)에서 실행합니다. 해설과 같은 Pretendard 원본(`PretendardVariable.ttf`, https://github.com/orioncactus/pretendard)이 필요하고, 페이지에 쓰인 글자와 학생이 칠 독일어 글자만 골라 파일 안에 넣습니다.

```
for n in 1 2 3 4 5; do python3 -B -I digital-src/schreibuebung/build.py . $n PretendardVariable.ttf "Goethe A2 Modelltest $n 작문 연습.html" web; done
python3 -B -I digital-src/schreibuebung/add-links.py
```

- 마지막 인자 `web`은 저장소용입니다. 오른쪽 위에 「Modelltest N」(시험 페이지로 돌아가기) 버튼, 접속 집계 태그, 학습 포탈 학습 저장(`/SODA-LERNPORTAL/sync.js`)이 들어갑니다. 빼면 학생에게 파일로 주는 오프라인판이 됩니다. 오프라인판도 제출하기는 됩니다.
- `build-index.py`로 `index.html`을 다시 만들면 「작문 연습」 줄이 빠지므로 `add-links.py`를 다시 실행합니다. 몇 번을 실행해도 결과가 같습니다.
- `build.py`는 만들기 전에 검사하고, 어긋나면 멈춥니다: 과제 수(Aufgabe 1·2), 번호마다 필요한 칸, Punkt 1–3이 차례대로 다 있는지, `{…}` 짝, A2 예시의 단어 수(과제의 범위 20–30, 30–40), A1 답안이 A2 예시보다 짧은지, 호칭 다음 줄의 소문자, 한국어 글의 ‘~다’ 체와 반말. 주어진 표현의 낱말이 예시에 없으면 알림만 보입니다.
- 새 회차를 더할 때는 `swN.py`를 만들고, 그 회차의 해설 데이터(`../erklaerung/erkN_hoeren.py`)가 있어야 합니다. 그다음 위 명령으로 만들고 `add-links.py`를 실행합니다.

## 페이지에서 하는 일

- 학생이 쓴 문장은 브라우저의 localStorage `sodaGZA2.v1.uebung.N`에 저절로 저장됩니다. 학습 포탈에 로그인한 학생은 sync.js가 이 값을 서버에 올려 다른 기기에서도 이어 씁니다. 이름은 디지털 시험 화면과 같은 `sodaGZA2.v1.name`을 씁니다.
- 과제 상자에는 시험지와 같은 상황과 세 가지 내용(Punkt), 그 한국어 번역이 있고, 번호마다 어느 Punkt를 쓰는 부분인지 함께 보입니다.
- 「내 글 전체」는 고쳐 쓴 문장을 호칭, 끝인사와 함께 이어 붙여, 번호마다 줄을 바꿔 보여 줍니다(시험의 모범 답안과 같은 모양). 단어 수는 쓰기 가이드와 같이 호칭, 본문, 끝인사, 이름을 모두 세고, 범위를 벗어나면 빨간색, 범위 안이면 초록색입니다.
- 「선생님께 제출하기」(소피아 독일어학원 수강생 전용)는 디지털 시험 화면과 같은 Apps Script 웹 앱으로 보냅니다. 번호마다 A1 문장·쓸 표현·학생 답과 완성한 글이 한 통으로 가고, 메일 제목은 「[SODA 학습 기록] Goethe A2 Modelltest N 작문 연습 · 이름」입니다. 제출 주소는 빌드할 때 `../template.html`의 `SUBMIT_URL`에서 가져오고, `tools/set-submit-url.py`가 이 페이지들의 주소도 함께 바꿉니다.
- 인쇄하면 밝은 색의 연습지가 됩니다: 쓰기 칸은 줄 친 칸으로 바뀌고(쓴 문장이 있으면 그 문장), 예시와 요약은 「예시 모두 보기」를 켰을 때만 나옵니다. Aufgabe마다 새 쪽에서 시작합니다.
