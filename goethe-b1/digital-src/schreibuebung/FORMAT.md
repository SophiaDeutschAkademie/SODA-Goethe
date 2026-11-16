# 작문 연습 데이터 형식 — Goethe-Zertifikat B1 (swN.py)

`sw1.py`(Modelltest I)가 기준 예시입니다. 같은 키, 같은 분량과 어조로 씁니다.

```python
AUFGABEN = [
  {"ko": "과제 요약(합니다체, 두세 문장)",                      # Aufgabe 1 · 친구에게 E-Mail
   "parts": [
     {"fix": "Lieber Jonas,"},                                  # 고치지 않는 줄(호칭, 끝인사와 이름)
     {"role": "도입",                                           # 번호 옆 이름. 문단 나누기에도 씁니다(gemeinsam.PARA)
      "a2": "A2 문장(독일어)",
      "use": "Schade, dass du … konntest!",                      # 쓸 B1 표현
      "use_ko": "…하지 못해서 아쉬워요!",                        # 표현의 뜻
      "tip": "도움말(합니다체). 독일어 조각은 «…»로 감쌉니다.",
      "b1": "{schade, dass} du am Wochenende nicht mitkommen {konntest}! …"},   # {…}는 강조
     …,
     {"fix": "Liebe Grüße\nMina"}],
   "sum": ["A2 → B1에서 바뀐 점(합니다체)", …]},
  {…},                                                          # Aufgabe 2 · 의견 글(fix 없음)
  {… "parts": [{"role": "호칭", "short": True, "a2": "Hallo Frau Berger,", … "b1": "{Sehr geehrte Frau Berger,}"},
               …,
               {"role": "끝인사", "short": True, "a2": "Liebe Grüße", … "b1": "{Mit freundlichen Grüßen}"},
               {"fix": "Mina Kim"}]},                            # Aufgabe 3 · 격식 있는 E-Mail
]
```

## 짜는 법

- Aufgabe 1·2는 번호 다섯~일곱 개, Aufgabe 3은 호칭과 끝인사를 포함해 다섯~여섯 개입니다. 번호 하나에 주어진 표현 하나를 씁니다.
- Aufgabe 1의 role: 도입, Leitpunkt 1, Leitpunkt 2, Leitpunkt 3, 마무리. Aufgabe 2: 반응, 의견, 이유, 예, 반대 의견(또는 의견 정리), 마무리. Aufgabe 3은 하는 일을 짧게(사과와 이유, 다른 날짜 제안, 부탁 …). 호칭과 끝인사는 `"short": True`로 한 줄 칸을 씁니다.
- A2 답안에는 과제의 내용(Leitpunkt)이 모두 들어 있어야 합니다. 문법은 맞게, 문장은 짧게, 연결은 und·aber·dann 정도로, 낱말은 gut·toll·schön처럼 단순하게 씁니다. 부문장은 되도록 쓰지 않습니다. Aufgabe 3의 A2 답안은 «Hallo Frau …,», «Liebe Grüße»처럼 말투를 틀리게 둡니다.
- B1 예시는 A2 문장에 주어진 표현을 넣어 고친 문장입니다. 표현과 상관없는 내용을 새로 더하지 않습니다(작은 보충은 됩니다). 표현이 들어간 자리와 바뀐 동사 자리를 `{…}`로 감쌉니다.
- 예시 전체의 단어 수(호칭, 끝인사, 이름 포함)는 Aufgabe 1·2가 70–100, Aufgabe 3이 33–50입니다. 빌드가 확인합니다.
- 호칭 뒤 다음 줄은 소문자로 시작합니다(명사와 Sie·Ihr는 대문자). 빌드가 확인합니다.
- 회차마다 표현이 겹치지 않게 고릅니다. 다섯 회차를 합쳐 부문장(dass, weil, wenn, obwohl, als, seitdem, ob, 간접 의문문), 관계문, zu 부정사, um … zu, 접속법 2식(wäre, könnte, hätte, würde), 수동태, 2단 연결어(nicht nur … sondern auch, zwar … aber, einerseits … andererseits, je … desto)가 고루 나오게 합니다.

## 쓰는 말

- 한국어는 **합니다체**입니다. 반말과 ‘~다’ 체는 쓰지 않습니다(빌드가 확인합니다). `use_ko`만 해요체로 씁니다(친구에게 쓰는 말의 뜻풀이).
- 문법 용어는 한국어로: 부문장, 관계대명사, 관계문, 접속법 2식, 분리동사, 화법조동사, 3격, 4격, 수동태. 현재완료의 haben/sein은 ‘조동사’라고 부르지 않습니다(‘sein과 함께 완료형을 만듭니다’).
- 독일어 조각 뒤의 조사는 한국어로 읽은 소리에 맞춥니다: dass(다스)로, weil(바일)로, wenn(벤)으로, das Problem(프로블렘)을. 헷갈리면 «…» 뒤에 한국어 낱말을 두거나 괄호로 씁니다: 호칭(«Lieber Jonas,»)과.
- ‘von Beruf’ 표현은 쓰지 않습니다.
