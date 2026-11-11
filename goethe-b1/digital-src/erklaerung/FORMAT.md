# 해설 데이터 형식 — Goethe-Zertifikat B1 (erkN_lesen.py, erkN_hoeren.py)

Goethe B1 해설은 이 폴더의 `build.py`로 만듭니다. 틀과 쓰는 규칙은 Goethe A2 해설(`../../../goethe-a2/digital-src/erklaerung/`)과 telc B1 해설을 따르고, B1 시험 구성에 맞게 바꾼 점만 다릅니다. **Modelltest 1의 `erk1_lesen.py`, `erk1_hoeren.py`가 기준 예시입니다. 같은 변수, 같은 키, 같은 분량과 어조로 씁니다.**

## 근거 자료 (앱 폴더 `goethe-b1/`)

| 자료 | 위치 |
|---|---|
| 문제, 본문, 정답, 쓰기 과제와 모범 답안 | `digital-src/data/mtN.json` (`lesen`, `hoeren`, `schreiben`) |
| Hörtexte(듣기 대본) | `mtN.json`의 `hoertexte` (시험지 22–24쪽과 같음) |
| Kommentar(문항별 함정 유형과 설명, 교사용) | `mtN.json`의 `kommentar.lesen["1"…"30"]`, `kommentar.hoeren["1"…"30"]`, `kommentar.schreibenSprechen` (시험지 20–21쪽) |
| 말하기 과제 | `Goethe B1 Modelltest N.pdf` 14–16쪽 |
| 말하기 모범 대화·발표·문답, 시험관이 보는 것 | 19쪽 |
| 쓰기 채점 기준 | 18쪽 „Bewertung“, `digital-src/guide-data.json` |

PDF에는 글자층이 있습니다. 19쪽은 두 단이므로 `pdftotext -f 19 -l 19 -x 0 -y 0 -W 297 -H 842 -layout …`(왼쪽), `-x 297 -W 298`(오른쪽)으로 나눠 읽습니다. **정답은 mtN.json이 기준**이고 Kommentar와 어긋나면 보고합니다.

## erkN_lesen.py

```python
LESEN1 = {"intro": "블로그 내용 요약", "tip": "푸는 요령",                                    # 1–6, Richtig/Falsch
          "items": [{"no": "1", "ans": "R", "stko": "문장 번역", "basis": [["본문 인용", "해석"]], "why": "정답 이유",
                     "vocab": [["독일어", "한국어"], …]}, …]}
LESEN2 = {"tip": "…", "texts": [                                                             # 7–9, 10–12, a/b/c
            {"intro": "기사 1 요약", "items": [{"no": "7", "ans": "a", "basis": [...], "why": "…",
                                               "wrong": {"b": "오답 이유", "c": "오답 이유"}, "vocab": [...]}, …]},
            {"intro": "기사 2 요약", "items": [ … ]}]}
LESEN3 = {"intro": "상황 설명과 예시에 쓴 광고", "tip": "…", "unused": "아무도 고르지 않는 광고와 그 광고가 노리는 문항",   # 13–19 (0 포함)
          "items": [{"no": "13", "ans": "a", "stko": "상황 번역", "cond": "조건 요약", "basis": [["광고 인용", "해석"]],
                     "why": "…", "trap": "함정(없으면 \"\")"}, …]}
LESEN4 = {"intro": "주제와 Ja/Nein의 뜻", "tip": "…",                                          # 20–26, Ja/Nein
          "items": [{"no": "20", "ans": "J", "basis": [["독자 의견 인용", "해석"]], "why": "…", "trap": "…"}, …]}
LESEN5 = {"intro": "문서 설명", "tip": "…", "items": [ LESEN2의 문항과 같은 키 ]}              # 27–30, a/b/c
```

- 정답 글자는 mtN.json과 같습니다: Richtig/Falsch는 `"R"`/`"F"`, Ja/Nein은 `"J"`/`"N"`, 광고는 글자 또는 `"0"`.
- 인용은 원문을 한 글자도 바꾸지 않고 잘라 옵니다(따옴표 „ “, 줄표 –, 숫자 표기 포함). 문장 일부만 잘라도 되지만 잘라 낸 부분은 원문과 똑같아야 합니다. 빌드가 확인합니다.
  - Lesen 1은 블로그(`title`, `paragraphs`, `closing`), Lesen 2는 그 기사(`title`, `lead`, `paragraphs`), Lesen 5는 문서(`sections`)에서 자릅니다.
  - Lesen 3은 **광고 한 칸의 한 항목 안에서**(`header`, `title`, `subtitle`, `facts` 한 줄, `body` 한 문단, `footer`) 자릅니다. 정답 광고에서 가져온 인용이 하나 이상 있어야 합니다. 0번 문항은 고르기 쉬운 광고에서 맞지 않는 조건을 인용합니다. 화면에는 인용 앞에 광고 글자가 자동으로 붙습니다.
  - Lesen 4는 그 사람의 글 안에서 자릅니다. 글 전체는 카드 안에 접힌 채로 들어갑니다.
- `vocab`은 Lesen 1·2·5에만 3개씩 씁니다. 명사는 관사와 복수형(der Unfall, ¨-e), 전치사 짝은 + Akk./+ Dat.
- 예시 문항(0번)은 해설하지 않습니다.
- 문항마다 Kommentar의 함정 유형(바꿔 말하기, 부정·제한 …)이 자동으로 표시됩니다. 유형의 뜻은 `gemeinsam.py`의 `FALLEN`에 있습니다.

## erkN_hoeren.py

```python
HOEREN1 = {"intro": "다섯 글 소개", "tip": "…",                                                # 1–10, 글마다 R/F 1개 + a/b/c 1개, 두 번
           "texts": [{"scene": "기차 안 안내 방송",
                      "items": [{"no": "1", "ans": "F", "stko": "문장 번역", "basis": [["대본 인용", "해석"]], "why": "…"},
                                {"no": "2", "ans": "b", "stko": "문항 줄기 번역 …", "basis": [...], "why": "…",
                                 "wrong": {"a": "…", "c": "…"}}]}, … 5개]}
HOEREN2 = {"title": "농가 민박 Sonnenhof의 환영 인사", "intro": "…", "tip": "…",               # 11–15, a/b/c, 한 번
           "items": [{"no": "11", "ans": "b", "stko": "…", "basis": [...], "why": "…", "wrong": {...}}, …]}
HOEREN3 = {"title": "대화: Nina와 Tom의 주말", "intro": "…", "tip": "…",                       # 16–22, R/F, 한 번
           "items": [{"no": "16", "ans": "F", "stko": "…", "basis": [...], "why": "…"}, …]}
HOEREN4 = {"title": "토론: …", "intro": "…(두 손님의 입장)", "tip": "…",                       # 23–30, 누가 말했는가, 두 번
           "items": [{"no": "23", "ans": "b", "stko": "…", "basis": [...], "why": "…", "trap": "다른 사람을 고르기 쉬운 이유(없으면 \"\")"}, …]}
SCHREIBEN = {"tasks": [
  {"title": "친구에게 E-Mail: …", "situation": "상황 요약과 형식(du, 호칭, 끝인사)",                      # Aufgabe 1
   "points": [["Leitpunkt(mtN.json 그대로)", "한국어", "쓸 수 있는 독일어 문장"], … 3개],
   "traps": ["자주 하는 실수", …], "model_ko": ["모범 답안 문단별 번역", …], "redemittel": [["독일어", "한국어"], …]},
  {"title": "의견 글: „…“", "situation": "…", "post_ko": "방명록 글 번역",                               # Aufgabe 2
   "points": [["Auf den Beitrag reagieren", "방명록 글에 반응하기", "예문"], ["Eigene Meinung", …], ["Begründung und Beispiel", …], ["Schluss", …]],
   "traps": [...], "model_ko": [...], "redemittel": [...]},
  {"title": "… 씨에게 E-Mail", "situation": "…(Sie, 호칭, 끝인사, 약 40단어)",                           # Aufgabe 3
   "points": [["과제문의 지시(독일어)", "한국어", "예문"], …], "traps": [...], "model_ko": [...], "redemittel": [...]}]}
SPRECHEN = {
  "t1": {"title": "과제 상자의 제목(PDF 14쪽 그대로)", "task": "상황 설명(한국어)",
         "leit": [["PDF의 점(독일어 그대로)", "한국어"], … 4개],                     # 마지막 „…“는 넣지 않습니다
         "points": ["이 과제에만 해당하는 요령", …], "muster": "19쪽 모범 대화가 무엇을 어떻게 정하는지 요약",
         "redemittel": [["19쪽 모범 대화에서 고른 문장", "한국어"], …]},
  "t2": {"themen": [{"title": "Thema 1 제목(PDF 15쪽 그대로)", "ko": "한국어", "ideas": [["Folie 2 예문", "한국어"], ["Folie 3 예문", "한국어"], ["Folie 4 예문", "한국어"]]},
                    {"title": "Thema 2 제목(PDF 16쪽 그대로)", …}],
         "note": "…", "points": ["…"]},
  "t3": {"muster": "19쪽 모범 문답 요약", "fragen": [["질문(독일어)", "Thema 1 · 한국어"], …]}}
```

- `stko`: R/F 문장과 Hören 4 문장은 문장 전체를, a/b/c 문항은 줄기만 번역하고 끝에 ` …`를 붙입니다.
- Hören 인용은 `hoertexte`에서 그대로 자릅니다. Teil 3·4는 **한 사람의 발화 하나 안에서** 자릅니다(두 사람의 말이 필요하면 `basis`를 두 개로). 화면에는 인용 앞에 말한 사람이 자동으로 붙습니다. 같은 말이 여러 사람에게 있으면 셋째 칸에 이름을 적습니다: `["인용", "해석", "Brenner"]`.
- Hören 4는 정답인 사람이 말한 인용이 하나 이상 있어야 합니다(빌드가 확인).
- `model_ko`는 모범 답안(`model.text`)을 `\n\n`로 나눈 문단 수와 같은 개수입니다.
- 쓰기 채점 기준, 말하기의 고정된 과제(Folie 다섯 장, Teil 3)와 공통 요령·표현은 `gemeinsam.py`에 있고 모든 회차가 함께 씁니다. 회차 파일에는 그 시험에만 해당하는 내용을 씁니다.
- 말하기 Teil 2의 `ideas`는 Folie 2(내 경험), 3(한국의 상황), 4(장단점과 의견) 순서입니다. Folie 3은 한국 학습자가 바로 쓸 수 있게 „In Korea …“로 씁니다. Thema 1은 19쪽 모범 발표를 참고합니다.

## 쓰는 말

- 한국어는 **합니다체**입니다. 반말과 ‘~다’ 체는 쓰지 않습니다(어휘 뜻풀이는 사전형 가능). 비유 없이 직접 설명합니다.
- 번역: 문항 문장(`stko`), 신문 기사, 규정, 안내 방송, 환영 인사, 진행자의 말, 격식 있는 편지는 합니다체. 블로그, 독자 의견, 친구끼리의 대화, 토론 손님의 말, 친구에게 쓰는 편지와 의견 글은 해요체.
- 형제자매의 위아래를 알 수 없으면 ‘남자 형제’, ‘여자 형제’로 옮깁니다. Stock은 층수가 달라 헷갈리므로 ‘위층’ 또는 독일어 그대로 씁니다(Erdgeschoss = 1층).
- 문법 용어는 한국어로(2격, 3격, 4격, 관계대명사, 접속법 2식, 분리동사, 부문장), 필요하면 괄호에 독일어.
- 한국어 안의 강조·뜻풀이 따옴표는 ‘…’(U+2018, U+2019). 독일어 인용은 „…“. `‚`(낮은 따옴표)는 쓰지 않습니다.
- `why`는 문장·보기의 어느 말이 본문·대본의 어느 말과 같거나 다른지 짚습니다(바꿔 말하기, 숫자·요일, 부정, nur/ausschließlich/eigentlich/aber 뒤).
- 함정(`trap`, `wrong`)은 **왜 그 보기를 고르기 쉬운지와 왜 틀렸는지**를 원문 근거와 함께 씁니다. Kommentar를 참고하되 그대로 옮기지 말고 학생에게 풀어서 설명합니다.
- 말하기·쓰기 예문에 „Was machst du von Beruf?“ 같은 ‘von Beruf’ 표현은 쓰지 않습니다. 직업은 „Was machen Sie beruflich?“로 묻습니다.

## 확인

```
cd goethe-b1
python3 -I digital-src/erklaerung/build.py . N <PretendardVariable.ttf> /tmp/check.html
python3 -I digital-src/erklaerung/check.py . N
```
`build.py`는 정답, Lesen·Hören 인용, Hören 4 인용의 말하는 사람, Leitpunkt, 모범 답안 문단 수를 검사하고 어긋나면 멈춥니다. `check.py`는 해설 글 속의 „…“ 인용이 원문에 있는지, 반말·‘~다’ 체가 섞였는지, 말하기 과제의 독일어가 PDF와 같은지 살펴보고 의심스러운 곳을 알려 줍니다(사람이 읽고 판단합니다).
