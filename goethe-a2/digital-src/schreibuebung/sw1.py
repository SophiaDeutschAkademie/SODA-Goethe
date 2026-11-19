# Goethe-Zertifikat A2 Modelltest I — 작문 연습 (A1 답안 → A2)
# 형식: FORMAT.md. a2의 {…}는 주어진 표현이 들어간 자리(화면에서 강조), tip의 «…»는 독일어 조각입니다.

AUFGABEN = [
    {   # Aufgabe 1 · SMS an Carla: Schlüssel gefunden
        "ko": "토요일에 친구 Carla의 생일 파티에 다녀왔는데, 오늘 가방에서 내 것이 아닌 열쇠를 발견했습니다. "
              "Carla에게 SMS를 보내 무엇을 발견했는지 쓰고, 누구의 열쇠인지 묻고, 언제 어디에서 돌려줄지 제안합니다.",
        "parts": [
            {"fix": "Hallo Carla,"},
            {"role": "Punkt 1",
             "a1": "ich habe einen Schlüssel. Er ist nicht von mir.",
             "use": "Ich habe … gefunden.",
             "use_ko": "…을 발견했어요",
             "tip": "지난 일은 현재완료(haben + 과거분사)로 씁니다. 과거분사 gefunden은 맨 끝에 옵니다. «fremd»는 ‘남의, 모르는’이라는 뜻이고, 남성 4격 명사 앞에서는 «einen fremden Schlüssel»이 됩니다.",
             "a2": "ich {habe} einen fremden Schlüssel {gefunden}."},
            {"role": "Punkt 2",
             "a1": "Ist das dein Schlüssel? Oder von wem ist er?",
             "use": "Weißt du, wem …?",
             "use_ko": "누구 것인지 알아요?",
             "tip": "«wem»은 ‘누구에게’라는 뜻의 3격 의문사입니다. gehören(…의 것이다)은 3격과 씁니다: «Er gehört dir.» «Weißt du, …?» 뒤에 질문을 붙이면 동사(gehört)가 맨 끝으로 갑니다.",
             "a2": "Gehört er dir? Oder {weißt du, wem} er {gehört}?"},
            {"role": "Punkt 3",
             "a1": "Ich komme morgen zu dir.",
             "use": "Soll ich … bringen?",
             "use_ko": "제가 …을 가져다줄까요?",
             "tip": "«Soll ich …?»는 내가 무엇을 해 줄지 제안하는 질문입니다. 동사원형 bringen은 맨 끝에 옵니다. 대명사가 둘이면 4격(ihn)을 3격(dir)보다 앞에 둡니다. 언제(morgen um sechs)와 어디(nach Hause)를 모두 씁니다.",
             "a2": "{Soll ich} ihn dir morgen um sechs nach Hause {bringen}?"},
            {"fix": "Liebe Grüße\nJisu"},
        ],
        "sum": [
            "«Ich habe einen Schlüssel.»을 현재완료 «Ich habe … gefunden.»으로 바꿔 무슨 일이 있었는지 썼습니다.",
            "«Von wem ist er?»를 간접 의문문 «Weißt du, wem er gehört?»로 바꿔, 과제가 요구한 두 번째 질문을 정확하게 했습니다.",
            "«Ich komme morgen zu dir.»를 «Soll ich ihn dir … bringen?»으로 바꿔, 무엇을 해 줄지 제안하는 질문으로 만들었습니다.",
        ],
    },
    {   # Aufgabe 2 · E-Mail an die Vermieterin: Handwerker am Dienstag
        "ko": "집주인 Albers 씨가 다음 주 화요일 9시에 수리 기사가 와서 부엌 창문을 고친다고 알려 주었습니다. "
              "그날 집에 없으므로 E-Mail을 보내 알려 줘서 고맙다고 하고, 집에 없는 이유를 쓰고, 수리 기사가 집에 들어갈 방법을 제안합니다.",
        "parts": [
            {"fix": "Sehr geehrte Frau Albers,"},
            {"role": "Punkt 1",
             "a1": "danke für die Information.",
             "use": "Vielen Dank, dass Sie …",
             "use_ko": "…해 주셔서 감사합니다",
             "tip": "무엇에 감사하는지 dass 문장으로 씁니다. dass 문장에서는 동사가 맨 끝에 오고, 현재완료이면 과거분사 다음에 haben이 맨 끝에 옵니다: «dass Sie mich informiert haben». 호칭 다음 줄이므로 소문자 vielen으로 시작합니다.",
             "a2": "{vielen Dank, dass Sie} mich {informiert haben}."},
            {"role": "Punkt 2",
             "a1": "Am Dienstag fahre ich nach Hamburg. Ich bin nicht zu Hause.",
             "use": "…, deshalb …",
             "use_ko": "…, 그래서 …",
             "tip": "deshalb는 앞 문장의 결과를 이어 줍니다. deshalb 바로 다음에 동사(bin)가 오고, 그다음에 주어(ich)가 옵니다. 앞 문장의 화법조동사 muss는 두 번째 자리에, 동사원형 fahren은 맨 끝에 옵니다.",
             "a2": "Am Dienstag muss ich nach Hamburg fahren, {deshalb bin ich} nicht da."},
            {"role": "Punkt 3",
             "a1": "Meine Nachbarin hat einen Schlüssel.",
             "use": "Wenn Sie möchten, …",
             "use_ko": "원하시면 …",
             "tip": "wenn 문장에서는 동사(möchten)가 맨 끝에 옵니다. wenn 문장이 앞에 오면 뒤 문장은 동사(kann)로 시작합니다. abholen(받아 가다)은 분리동사지만 화법조동사와 함께 쓰면 붙여서 맨 끝에 씁니다.",
             "a2": "{Wenn Sie möchten, kann} der Handwerker den Schlüssel bei meiner Nachbarin abholen."},
            {"fix": "Mit freundlichen Grüßen\nJisu Kim"},
        ],
        "sum": [
            "«danke für die Information»을 «Vielen Dank, dass Sie mich informiert haben»으로 바꿔, 무엇에 감사하는지 문장으로 썼습니다.",
            "두 문장을 deshalb로 이어 이유와 결과를 한 문장에 담았습니다.",
            "제안은 «Wenn Sie möchten, …»으로 시작해 집주인의 뜻을 묻는 정중한 문장으로 만들었습니다.",
        ],
    },
]
