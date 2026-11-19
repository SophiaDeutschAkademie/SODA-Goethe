# Goethe-Zertifikat A2 Modelltest IV — 작문 연습 (A1 답안 → A2)
# 형식: FORMAT.md. a2의 {…}는 주어진 표현이 들어간 자리(화면에서 강조), tip의 «…»는 독일어 조각입니다.

AUFGABEN = [
    {   # Aufgabe 1 · SMS an Anna: Reifen kaputt
        "ko": "친구 Anna가 주말 동안 자전거를 빌려주었는데, 타이어 하나가 망가졌습니다. "
              "Anna에게 SMS를 보내 무슨 일이 있었는지 쓰고, 사과하고, 어떻게 해결할지 제안합니다.",
        "parts": [
            {"fix": "Hallo Anna,"},
            {"role": "Punkt 1",
             "a1": "dein Fahrrad hat ein Problem. Der Reifen ist kaputt.",
             "use": "… ist … kaputtgegangen.",
             "use_ko": "…이 망가졌어요",
             "tip": "kaputtgehen(고장 나다, 망가지다)은 sein과 함께 현재완료를 만듭니다: «ist … kaputtgegangen». 분리동사라서 ge가 kaputt와 gangen 사이에 들어갑니다. «von deinem Fahrrad»는 ‘네 자전거의’라는 뜻입니다.",
             "a2": "am Sonntag {ist} ein Reifen von deinem Fahrrad {kaputtgegangen}."},
            {"role": "Punkt 2",
             "a1": "Entschuldigung!",
             "use": "Entschuldige bitte, …",
             "use_ko": "미안해요, …",
             "tip": "친구에게 사과할 때는 entschuldigen의 du 명령형 «Entschuldige bitte!»를 씁니다. «das wollte ich nicht»는 ‘그러려던 게 아니었어요’라는 뜻으로, wollen의 과거형 wollte를 씁니다.",
             "a2": "{Entschuldige bitte}, das {wollte} ich nicht!"},
            {"role": "Punkt 3",
             "a1": "Ich bringe das Fahrrad in die Werkstatt. Ich bezahle.",
             "use": "Ich lasse … reparieren.",
             "use_ko": "…을 수리 맡길게요",
             "tip": "«lassen + 동사원형»은 ‘다른 사람에게 …하게 하다’라는 뜻입니다. 내가 직접 고치지 않고 가게에 맡길 때 씁니다. lasse는 두 번째 자리에, 동사원형 reparieren은 맨 끝에 옵니다.",
             "a2": "Ich {lasse} den Reifen morgen {reparieren} und bezahle das natürlich."},
            {"fix": "Viele Grüße\nDohyun"},
        ],
        "sum": [
            "«Der Reifen ist kaputt.»를 sein과 함께 쓰는 현재완료 «ist … kaputtgegangen»으로 바꿔 무슨 일이 있었는지 썼습니다.",
            "«Entschuldigung!»을 «Entschuldige bitte, das wollte ich nicht!»로 바꿔 사과를 더 분명하게 했습니다.",
            "해결 방법은 «lassen + 동사원형»으로 쓰고, 비용도 내겠다고 했습니다.",
        ],
    },
    {   # Aufgabe 2 · E-Mail an den Online-Shop: falsche Größe
        "ko": "인터넷 쇼핑몰에서 운동화를 주문했는데, 오늘 온 상자에 다른 사이즈가 들어 있었습니다. "
              "고객 센터에 E-Mail을 보내 무엇을 주문했고 무엇을 받았는지 쓰고, 원하는 것을 말하고, 잘못 온 신발을 어떻게 돌려보내는지 묻습니다.",
        "parts": [
            {"fix": "Sehr geehrte Damen und Herren,"},
            {"role": "Punkt 1",
             "a1": "ich habe Schuhe in Größe 41 bestellt. Ich habe Größe 44 bekommen.",
             "use": "Ich habe … bestellt, aber … bekommen.",
             "use_ko": "…을 주문했는데 …을 받았습니다",
             "tip": "현재완료 문장 두 개를 aber로 이을 때, 같은 haben은 한 번만 써도 됩니다. 과거분사(bestellt, bekommen)는 각 부분의 맨 끝에 옵니다.",
             "a2": "ich {habe} Schuhe in Größe 41 {bestellt, aber} Größe 44 {bekommen}."},
            {"role": "Punkt 2",
             "a1": "Ich will Größe 41.",
             "use": "Ich hätte gern …",
             "use_ko": "…을 받고 싶습니다",
             "tip": "«Ich will …»은 상대에게 무례하게 들릴 수 있습니다. 원하는 것을 정중하게 말할 때는 접속법 2식 «Ich hätte gern …»을 씁니다. «in der richtigen Größe»는 ‘맞는 사이즈로’라는 뜻입니다(in + 3격).",
             "a2": "{Ich hätte gern} Schuhe in der richtigen Größe."},
            {"role": "Punkt 3",
             "a1": "Wie schicke ich die Schuhe zurück?",
             "use": "Bitte schreiben Sie mir, wie …",
             "use_ko": "어떻게 …하는지 알려 주십시오",
             "tip": "«Bitte schreiben Sie mir, …»는 Sie에게 하는 정중한 부탁입니다. 뒤에 질문(wie …)을 붙이면 동사(kann)가 맨 끝으로 갑니다. zurückschicken(돌려보내다)은 분리동사지만 화법조동사와 함께 쓰면 붙여서 맨 끝에 씁니다.",
             "a2": "{Bitte schreiben Sie mir, wie} ich die falschen Schuhe zurückschicken {kann}."},
            {"fix": "Mit freundlichen Grüßen\nDohyun Lee"},
        ],
        "sum": [
            "주문한 것과 받은 것을 aber로 이어 한 문장으로 썼습니다(«habe … bestellt, aber … bekommen»).",
            "«Ich will …»을 정중한 «Ich hätte gern …»으로 바꿨습니다.",
            "«Wie schicke ich … zurück?»을 «Bitte schreiben Sie mir, wie …»로 바꿔, 정중한 부탁 속의 질문으로 만들었습니다.",
        ],
    },
]
