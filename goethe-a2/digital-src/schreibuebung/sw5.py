# Goethe-Zertifikat A2 Modelltest V — 작문 연습 (A1 답안 → A2)
# 형식: FORMAT.md. a2의 {…}는 주어진 표현이 들어간 자리(화면에서 강조), tip의 «…»는 독일어 조각입니다.

AUFGABEN = [
    {   # Aufgabe 1 · SMS an Timo: Karte für das Basketballspiel
        "ko": "금요일 저녁 농구 경기 표가 두 장 있는데, 함께 가기로 한 형제(Bruder)가 아파서 갈 수 없습니다. "
              "친구 Timo에게 SMS를 보내 표가 남은 이유를 쓰고, 시간이 있는지 묻고, 어디에서 몇 시에 만날지 제안합니다.",
        "parts": [
            {"fix": "Hallo Timo,"},
            {"role": "Punkt 1",
             "a1": "ich habe zwei Karten für Basketball. Mein Bruder ist krank.",
             "use": "…, denn …",
             "use_ko": "…, 왜냐하면 …",
             "tip": "«übrig haben»은 ‘남아 있다’라는 뜻이고, 문장에서 맨 끝에 오는 말은 übrig입니다. 이유는 denn으로 이어 씁니다. denn 뒤에서는 동사가 맨 끝으로 가지 않고 주어 다음(두 번째 자리)에 옵니다. «fürs»는 «für das»를 줄인 말입니다.",
             "a2": "ich habe eine Karte fürs Basketballspiel übrig, {denn} mein Bruder {ist} krank."},
            {"role": "Punkt 2",
             "a1": "Hast du Zeit?",
             "use": "Hättest du … Zeit?",
             "use_ko": "… 시간 있어요?(부드럽게)",
             "tip": "hättest는 haben의 접속법 2식으로, «Hast du …?»보다 부드럽게 묻는 말입니다. 언제인지(am Freitag)도 함께 씁니다.",
             "a2": "{Hättest du} am Freitag {Zeit}?"},
            {"role": "Punkt 3",
             "a1": "Wir treffen uns um 19 Uhr am Eingang.",
             "use": "Wollen wir uns … treffen?",
             "use_ko": "우리 …에서 만날까요?",
             "tip": "«Wollen wir …?»는 ‘우리 …할까요?’라고 제안하는 질문입니다. sich treffen(만나다)은 재귀동사라 uns가 들어가고, 동사원형 treffen은 맨 끝에 옵니다.",
             "a2": "{Wollen wir uns} um sieben am Eingang {treffen}?"},
            {"fix": "Viele Grüße\nJiwon"},
        ],
        "sum": [
            "«Ich habe zwei Karten für Basketball.»을 «Ich habe eine Karte fürs Basketballspiel übrig, denn …»으로 바꿔, 표가 남은 이유를 한 문장에 담았습니다.",
            "«Hast du Zeit?»를 접속법 2식 «Hättest du … Zeit?»로 바꿔 부드럽게 물었습니다.",
            "«Wir treffen uns …»를 «Wollen wir uns … treffen?»으로 바꿔 제안하는 질문으로 만들었습니다.",
        ],
    },
    {   # Aufgabe 2 · E-Mail an die Sprachschule: Deutschkurs am Abend
        "ko": "독일어 실력을 높이고 싶어서 어학원 Lingua의 ‘저녁 독일어 과정’ 광고를 보았습니다. "
              "어학원에 E-Mail을 보내 과정을 찾는 이유를 쓰고, 수업 시간과 수강료를 묻고, 미리 시험을 봐야 하는지 묻습니다.",
        "parts": [
            {"fix": "Sehr geehrte Damen und Herren,"},
            {"role": "Punkt 1",
             "a1": "ich möchte Deutsch lernen. Ich will im Oktober studieren.",
             "use": "…, weil ich … möchte.",
             "use_ko": "…하고 싶기 때문에",
             "tip": "weil 문장에 화법조동사가 있으면 동사원형(studieren)이 먼저 오고, 화법조동사(möchte)가 맨 끝에 옵니다: «weil ich ab Oktober studieren möchte». «ab Oktober»는 ‘10월부터’라는 뜻입니다.",
             "a2": "ich suche einen Abendkurs, {weil ich} ab Oktober studieren {möchte}."},
            {"role": "Punkt 2",
             "a1": "Wann ist der Kurs? Was kostet er?",
             "use": "Würden Sie mir … schicken?",
             "use_ko": "…을 보내 주시겠어요?",
             "tip": "«Würden Sie …?»는 접속법 2식으로 정중하게 부탁하는 말입니다. 동사원형(schicken)은 맨 끝에 옵니다. 묻고 싶은 두 가지(die Kurszeiten, den Preis)를 und로 묶어 한 문장에 담습니다.",
             "a2": "{Würden Sie mir} bitte die Kurszeiten und den Preis {schicken}?"},
            {"role": "Punkt 3",
             "a1": "Muss ich einen Test machen?",
             "use": "Ich möchte wissen, ob …",
             "use_ko": "…인지 알고 싶습니다",
             "tip": "예·아니요로 답하는 질문을 «Ich möchte wissen, …» 뒤에 붙일 때는 ob을 씁니다. ob 문장에서도 화법조동사(muss)가 맨 끝에 옵니다. «vorher»는 ‘미리, 그전에’라는 뜻입니다.",
             "a2": "{Ich möchte wissen, ob} ich vorher einen Test machen {muss}."},
            {"fix": "Mit freundlichen Grüßen\nJiwon Han"},
        ],
        "sum": [
            "과정을 찾는 이유는 weil 문장으로 쓰고, 화법조동사 möchte를 맨 끝에 두었습니다.",
            "두 가지 질문을 «Würden Sie mir … schicken?»이라는 정중한 부탁 한 문장으로 바꿨습니다.",
            "«Muss ich einen Test machen?»을 «Ich möchte wissen, ob …»으로 바꿔 간접 의문문으로 썼습니다.",
        ],
    },
]
