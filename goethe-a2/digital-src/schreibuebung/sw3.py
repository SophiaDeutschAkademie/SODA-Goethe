# Goethe-Zertifikat A2 Modelltest III — 작문 연습 (A1 답안 → A2)
# 형식: FORMAT.md. a2의 {…}는 주어진 표현이 들어간 자리(화면에서 강조), tip의 «…»는 독일어 조각입니다.

AUFGABEN = [
    {   # Aufgabe 1 · SMS an Nele: krank, kein Kino
        "ko": "오늘 저녁 친구 Nele와 영화를 보러 가기로 했는데, 아파서 갈 수 없습니다. "
              "Nele에게 SMS를 보내 못 가는 이유를 쓰고, 내 표를 어떻게 할지 말하고, 다른 날 만나자고 제안합니다.",
        "parts": [
            {"fix": "Hallo Nele,"},
            {"role": "Punkt 1",
             "a1": "ich bin krank. Ich kann nicht kommen.",
             "use": "Ich bin … geworden.",
             "use_ko": "…해졌어요",
             "tip": "werden(…이 되다)의 현재완료는 sein과 함께 씁니다: «ich bin krank geworden». 못 가는 일은 und로 이어 붙입니다. mitkommen(함께 가다)은 분리동사지만 화법조동사와 함께 쓰면 붙여서 맨 끝에 씁니다.",
             "a2": "ich {bin} krank {geworden} und kann heute nicht mitkommen."},
            {"role": "Punkt 2",
             "a1": "Paul kann meine Karte haben.",
             "use": "Frag doch …, ob …",
             "use_ko": "…에게 …인지 물어봐요",
             "tip": "ob은 ‘…인지 아닌지’라는 뜻이고, ob 문장에서는 동사(möchte)가 맨 끝에 옵니다. 명령문에 doch를 넣으면 부드러운 제안이 됩니다.",
             "a2": "{Frag doch} Paul, {ob} er meine Karte {möchte}."},
            {"role": "Punkt 3",
             "a1": "Wir trinken am Samstag Kaffee.",
             "use": "Wie wäre es mit …?",
             "use_ko": "…은 어때요?",
             "tip": "부드럽게 제안하는 접속법 2식 표현입니다. mit 뒤에는 3격이 옵니다: «mit einem Kaffee». 다른 날(am Samstag)도 함께 씁니다.",
             "a2": "{Wie wäre es mit} einem Kaffee am Samstag?"},
            {"fix": "Liebe Grüße\nYuna"},
        ],
        "sum": [
            "«Ich bin krank.»를 현재완료 «Ich bin krank geworden»으로 바꾸고, 못 가는 일을 und로 이었습니다.",
            "표를 어떻게 할지는 doch를 넣은 명령문과 ob 문장으로 부드럽게 썼습니다.",
            "다른 날 만나자는 제안은 «Wie wäre es mit einem Kaffee am Samstag?»처럼 접속법 2식으로 썼습니다.",
        ],
    },
    {   # Aufgabe 2 · E-Mail an die Chefin: freier Tag am Freitag
        "ko": "사무실에서 일하는데, 다음 주 금요일에 중요한 약속이 있어 출근할 수 없습니다. "
              "상사 Steinmann 씨에게 E-Mail을 보내 이유를 쓰고, 그날 쉬어도 되는지 묻고, 일을 언제 대신할지 제안합니다.",
        "parts": [
            {"fix": "Sehr geehrte Frau Steinmann,"},
            {"role": "Punkt 1",
             "a1": "am Freitag habe ich einen Arzttermin. Ich komme nicht.",
             "use": "Weil …, kann ich …",
             "use_ko": "… 때문에 …할 수 없습니다",
             "tip": "weil 문장을 앞에 쓸 수도 있습니다. 이때 weil 문장의 동사(habe)는 맨 끝에 오고, 뒤 문장은 동사(kann)로 시작합니다. 호칭 다음 줄이므로 소문자 weil로 시작합니다.",
             "a2": "{weil} ich am Freitag einen Arzttermin {habe, kann ich} nicht zur Arbeit kommen."},
            {"role": "Punkt 2",
             "a1": "Ich möchte frei haben.",
             "use": "Darf ich …?",
             "use_ko": "…해도 될까요?",
             "tip": "허락을 구할 때는 화법조동사 dürfen을 씁니다: «Darf ich …?» 동사원형(nehmen)은 맨 끝에 옵니다. «Urlaub nehmen»은 ‘휴가를 내다’, «an diesem Tag»은 ‘그날’이라는 뜻입니다.",
             "a2": "{Darf ich} an diesem Tag Urlaub {nehmen}?"},
            {"role": "Punkt 3",
             "a1": "Ich arbeite am Montag mehr.",
             "use": "Dafür … länger.",
             "use_ko": "그 대신 … 더 오래 …",
             "tip": "dafür는 여기에서 ‘그 대신’이라는 뜻입니다. dafür가 맨 앞에 오면 동사(arbeite)가 바로 뒤에 옵니다. länger는 lang의 비교급으로 ‘더 오래’라는 뜻이고, 얼마나 더 할지(zwei Stunden)도 씁니다.",
             "a2": "{Dafür} arbeite ich am Montag zwei Stunden {länger}."},
            {"fix": "Mit freundlichen Grüßen\nYuna Choi"},
        ],
        "sum": [
            "이유를 말하는 weil 문장을 앞에 두고, 뒤 문장을 동사(kann)로 시작했습니다.",
            "«Ich möchte frei haben.»을 «Darf ich …?»로 바꿔 허락을 구하는 질문으로 만들었습니다.",
            "«Ich arbeite am Montag mehr.»를 «Dafür arbeite ich … länger.»로 바꿔, 언제 얼마나 더 일할지 분명히 썼습니다.",
        ],
    },
]
