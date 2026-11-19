# Goethe-Zertifikat A2 Modelltest II — 작문 연습 (A1 답안 → A2)
# 형식: FORMAT.md. a2의 {…}는 주어진 표현이 들어간 자리(화면에서 강조), tip의 «…»는 독일어 조각입니다.

AUFGABEN = [
    {   # Aufgabe 1 · SMS an Mia: Zug mit Verspätung
        "ko": "친구 Mia와 저녁 7시에 콘서트홀 앞에서 만나기로 했는데, 기차가 30분 늦습니다. "
              "Mia에게 SMS를 보내 늦는 이유와 도착 시각을 알리고, 그동안 Mia가 할 일을 제안합니다.",
        "parts": [
            {"fix": "Hallo Mia,"},
            {"role": "Punkt 1",
             "a1": "ich komme spät. Der Zug ist nicht pünktlich.",
             "use": "…, weil …",
             "use_ko": "… 때문에",
             "tip": "weil은 이유를 붙이는 말입니다. weil 문장에서는 동사(hat)가 맨 끝에 옵니다. «Verspätung haben»은 ‘(기차 등이) 늦다, 연착하다’라는 뜻입니다.",
             "a2": "ich komme leider zu spät, {weil} mein Zug Verspätung {hat}."},
            {"role": "Punkt 2",
             "a1": "Ich bin um 19.30 Uhr da.",
             "use": "erst gegen …",
             "use_ko": "…쯤에야(생각보다 늦게)",
             "tip": "«erst»는 ‘생각보다 늦게, …에야’라는 뜻이고, «gegen + 시각»은 ‘… 시쯤’이라는 뜻입니다. 정확한 시각을 모를 때 씁니다. «halb acht»는 8시 반이 아니라 7시 반입니다.",
             "a2": "Ich bin {erst gegen} halb acht da."},
            {"role": "Punkt 3",
             "a1": "Du kannst die Karten holen.",
             "use": "Du könntest …",
             "use_ko": "…하면 좋겠어요",
             "tip": "könntest는 können의 접속법 2식으로, 부드럽게 제안할 때 씁니다. 동사원형 abholen은 맨 끝에 옵니다. «schon mal»은 ‘그동안 먼저’라는 뜻입니다.",
             "a2": "{Du könntest} schon mal die Karten {abholen}."},
            {"fix": "Viele Grüße\nMinho"},
        ],
        "sum": [
            "«Der Zug ist nicht pünktlich.»를 weil 문장으로 바꿔 늦는 이유를 앞 문장에 붙였습니다.",
            "도착 시각에는 «erst gegen …»을 넣어 ‘생각보다 늦게, … 시쯤’이라는 뜻을 담았습니다.",
            "«Du kannst …»를 접속법 2식 «Du könntest …»로 바꿔 부드럽게 제안했습니다.",
        ],
    },
    {   # Aufgabe 2 · E-Mail an das Hotel: Späte Ankunft
        "ko": "금요일에 Hotel Seeblick에 방을 예약했는데, 밤늦게야 도착합니다. "
              "호텔에 E-Mail을 보내 언제쯤 왜 늦게 도착하는지 쓰고, 프런트가 몇 시까지 여는지, 늦게도 먹을 것이 있는지 묻습니다.",
        "parts": [
            {"fix": "Sehr geehrte Damen und Herren,"},
            {"role": "Punkt 1",
             "a1": "ich komme am Freitag um 23 Uhr. Mein Flug ist spät.",
             "use": "…, denn …",
             "use_ko": "…, 왜냐하면 …",
             "tip": "denn도 weil처럼 이유를 말합니다. 하지만 denn 뒤에서는 동사가 맨 끝으로 가지 않고 주어 다음(두 번째 자리)에 옵니다: «denn mein Flug landet spät». «gegen 23 Uhr»는 ‘23시쯤’이라는 뜻입니다.",
             "a2": "ich komme am Freitag gegen 23 Uhr, {denn} mein Flug {landet} spät."},
            {"role": "Punkt 2",
             "a1": "Wann ist die Rezeption offen?",
             "use": "Könnten Sie mir sagen, bis wann …?",
             "use_ko": "몇 시까지 …인지 알려 주시겠어요?",
             "tip": "«Könnten Sie …?»는 접속법 2식의 정중한 부탁입니다. 뒤에 질문(bis wann …)을 붙이면 간접 의문문이 되어 동사(ist)가 맨 끝으로 갑니다. ‘몇 시까지’는 «bis wann»입니다.",
             "a2": "{Könnten Sie mir sagen, bis wann} die Rezeption geöffnet {ist}?"},
            {"role": "Punkt 3",
             "a1": "Gibt es dann Essen?",
             "use": "Gibt es … noch etwas zu essen?",
             "use_ko": "…에도 아직 먹을 것이 있나요?",
             "tip": "«etwas zu essen»은 ‘먹을 것’이라는 뜻입니다. «so spät noch»는 ‘그렇게 늦게도 아직’이라는 뜻이어서, 늦은 시간에도 되는지 정확하게 물을 수 있습니다.",
             "a2": "{Gibt es} so spät {noch etwas zu essen}?"},
            {"fix": "Mit freundlichen Grüßen\nMinho Park"},
        ],
        "sum": [
            "이유는 denn으로 이었습니다. weil과 달리 denn 뒤에서는 동사가 두 번째 자리에 옵니다.",
            "«Wann ist die Rezeption offen?»을 «Könnten Sie mir sagen, bis wann …?»으로 바꿔 정중하게 물었습니다.",
            "«Gibt es dann Essen?»을 «Gibt es so spät noch etwas zu essen?»으로 바꿔, 늦은 시간에도 먹을 것이 있는지 정확하게 물었습니다.",
        ],
    },
]
