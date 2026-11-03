# 해설 데이터 형식 — Goethe-Zertifikat A2 (erkN_lesen.py, erkN_hoeren.py)

Goethe A2 해설은 이 폴더의 `build.py`로 만듭니다. 쓰는 규칙(어조, 따옴표, 근거 인용, 함정 설명)은 telc B1 해설과 같습니다. **`/home/claude/soda-telc/telc-b1/digital-src/erklaerung/FORMAT.md`의 ‘쓰는 말’과 예시 `erk1_lesen.py`, `erk1_hoeren.py`를 먼저 읽고 같은 깊이와 어조로 씁니다.** 학생은 A2 수험생이므로 문장은 더 짧고 쉽게 씁니다. 문법 용어는 한국어로 쓰고, 꼭 필요할 때만 씁니다.

## 근거 자료 (앱 폴더 `goethe-a2/`)

| 자료 | 위치 |
|---|---|
| 문제, 본문, 정답, 쓰기 과제와 모범 답안, 좋은 답안 조건(`schreiben.good`) | `digital-src/data/mtN.json` |
| Kommentar(문항별 함정, 교사용) | `mtN.json`의 `kommentar.rows` (L1–L4, H1–H4) |
| 광고 a–f의 글 | `lesen.t4.ads.<글자>.alt` |
| Hören 그림의 이름 | `hoeren.t2.pictures.<글자>.alt`, `hoeren.t3.items[].options.<글자>.alt` |
| 말하기 과제 | `Goethe A2 Modelltest N.pdf` 14–16쪽 |
| 말하기 모범 예시 | 19쪽 |
| Hörtexte(듣기 대본) | 22–23쪽 |
| 쓰기·말하기 채점 기준과 요령 | `digital-src/guide-data.json`, `sprechen-data.json` |

PDF에는 글자층이 있습니다. `pdftotext -layout -f 22 -l 23 "Goethe A2 Modelltest N.pdf" -`로 읽고, 두 단의 순서는 `pdftoppm -r 120 -f 22 -l 22 -png …`로 그림을 만들어 확인합니다. 줄 끝 하이픈은 이어 붙이되 E-Mail 같은 진짜 하이픈은 둡니다.

## erkN_lesen.py

```python
LESEN1 = {"intro": "기사 내용 한 줄 요약", "tip": "푸는 요령",
          "items": [{"no": "1", "ans": "b", "basis": [["기사 원문 인용", "해석"]], "why": "정답 이유",
                     "wrong": {"a": "오답 이유", "c": "오답 이유"}, "vocab": [["독일어", "한국어"], …]}, …]}   # 1–5
LESEN2 = {"intro": "안내판 설명", "tip": "…",
          "items": [{"no": "6", "ans": "b", "stko": "상황 문장 번역", "basis": [["안내판 원문 인용", "해석"]],
                     "why": "…", "wrong": {"a": "…", "c": "…"}}, …]}                                         # 6–10
LESEN3 = {"intro": "이메일 내용 요약", "tip": "…", "items": [ LESEN1과 같은 키 ]}                           # 11–15
LESEN4 = {"intro": "", "tip": "…", "unused": "아무도 고르지 않는 광고와 X 문항 설명",
          "items": [{"no": "16", "ans": "d", "stko": "상황 번역", "cond": "조건 요약",
                     "basis": [["광고 글(alt) 인용", "해석"]], "why": "…", "trap": "함정(없으면 \"\")"}, …]}   # 16–20, X 포함
```

- 인용은 원문을 한 글자도 바꾸지 않고 잘라 옵니다. Lesen 1은 기사(`title`, `lead`, `paragraphs`, `quote`), Lesen 2는 안내판 한 줄(`floor`와 `text`), Lesen 3은 이메일(`subject`, `greeting`, `paragraphs`, `closing`), Lesen 4는 광고 `alt`에서 자릅니다. 빌드가 확인합니다.
- 예시 문항(0번)은 해설하지 않습니다.

## erkN_hoeren.py

```python
HOEREN1 = {"title": "짧은 글 다섯 개", "intro": "", "tip": "…",
           "items": [{"no": "1", "ans": "a", "stko": "질문 번역", "basis": [["대본 인용", "해석"]], "why": "…",
                      "wrong": {"b": "…", "c": "…"}}, …]}                       # 1–5, 두 번 들음
HOEREN2 = {"title": "대화: …", "intro": "대화 상황", "tip": "…",
           "items": [{"no": "6", "ans": "d", "basis": [["대본 인용", "해석"]], "why": "…", "trap": "…"}, …]}   # 6–10, 사람별 그림, 한 번
HOEREN3 = {"title": "짧은 대화 다섯 개", "intro": "", "tip": "…",
           "items": [{"no": "11", "ans": "a", "stko": "질문 번역", "basis": [...], "why": "…",
                      "wrong": {"b": "그림 b가 틀린 이유", "c": "…"}}, …]}       # 11–15, 그림 고르기, 한 번
HOEREN4 = {"title": "인터뷰: …", "intro": "", "tip": "…",
           "items": [{"no": "16", "ans": "Nein", "stko": "문장 번역", "basis": [...], "why": "…"}, …]}   # 16–20, Ja/Nein, 두 번
SCHREIBEN = {
  "intro": "쓰기 시험 구성(Aufgabe 1 SMS 20–30단어 약 10분, Aufgabe 2 E-Mail 30–40단어 약 20분)과 공통 요령",
  "tasks": [
    {"title": "Carla에게 SMS", "situation": "상황 요약과 형식(du/Sie, 호칭, 끝인사)",
     "points": [["독일어 내용 지시(mtN.json points 그대로)", "한국어", "쓸 수 있는 독일어 문장"], … 3개],
     "traps": ["자주 하는 실수(typicalErrors를 참고해 한국어로)", …],
     "model_ko": ["모범 답안 문단별 번역", …],      # model.text를 \n\n로 나눈 문단 수와 같게
     "redemittel": [["독일어", "한국어"], …]},
    {… Aufgabe 2 …}
  ],
  "criteria": [["Erfüllung", "Aufgabenerfüllung", "설명"], …],   # guide-data.json 기준
  "criteria_note": "점수와 단어 수 기준을 한 문장으로(guide-data.json 기준)"
}
SPRECHEN = {
  "names": ["Fragen zur Person", "Von sich erzählen", "Gemeinsam etwas planen"],   # PDF 이름 그대로
  "head": "약 15분, 두 사람이 함께",
  "note": "말하기 모범 예시는 PDF 19쪽에 있습니다.",
  "t1": {"task": "…", "points": [...], "redemittel": [[독일어, 한국어], …]},
  "t2": {"task": "…", "points": [...], "redemittel": [...]},
  "t3": {"task": "…", "a": "A의 일정 요약(있으면)", "b": "B의 일정 요약", "a_label": "A의 일정", "b_label": "B의 일정",
         "points": [...], "redemittel": [...]}
}
```

- Hören 문장(`stko`)과 공식 편지의 번역은 합니다체, SMS·친구 메일의 번역은 해요체입니다. 반말과 ‘~다’ 체는 쓰지 않습니다(어휘 뜻풀이는 사전형 가능).
- Hören 2는 사람 이름(`persons`)에 그림 글자를 고르는 문제입니다. 쓰이지 않는 그림 세 개 가운데 대화에 나오는 것(함정)을 `trap`에 씁니다.
- Hören 3의 `wrong`은 그림 이름(`alt`)을 넣어 설명합니다.
- 말하기 예문에 ‘von Beruf’ 질문은 쓰지 않습니다. 직업은 „Was machen Sie beruflich?“ / „Was machst du beruflich?“로 묻습니다.

## 확인

```
cd goethe-a2
python3 -I digital-src/erklaerung/build.py . N <PretendardVariable.ttf> /tmp/check.html
```
빌드는 정답(Hören 2는 예시를 뺀 사람 다섯 명), Lesen 인용, 모범 답안 문단 수를 검사합니다. Hören 인용은 PDF 대본과 스크립트로 대조합니다.
