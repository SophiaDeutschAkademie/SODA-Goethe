# Goethe-Zertifikat B1 해설 — 모든 Modelltest가 함께 쓰는 글
# (함정 유형, 쓰기 채점 기준, 말하기의 고정된 과제와 요령)

# 시험지 20쪽 Kommentar의 „Acht Fallentypen“. mtN.json의 kommentar.lesen / kommentar.hoeren 에 문항마다 글자가 붙어 있습니다.
FALLEN = [
    ("P", "바꿔 말하기", "Paraphrase", "정답은 본문이나 대본의 말을 그대로 쓰지 않고 다른 말로 바꿔서 나옵니다. 같은 단어가 아니라 같은 뜻을 찾아야 합니다."),
    ("N", "부정·제한", "Negation / Einschränkung", "nicht, nur, kaum, außer, nicht mehr als, ausschließlich 같은 말 하나가 뜻을 뒤집거나 좁힙니다."),
    ("A", "계획과 실제", "Absicht vs. Realität", "wollte eigentlich, sollte, hätte, versprochen, geplant는 계획이나 약속일 뿐입니다. 실제로 일어났는지는 뒤 문장에 나옵니다."),
    ("K", "양보", "Konzessiv", "Ich verstehe …, aber / zwar … aber / trotzdem 에서는 뒤쪽이 그 사람의 진짜 생각입니다."),
    ("W", "단어 함정", "Wortfalle", "본문이나 대본의 핵심 단어가 틀린 보기에 그대로 들어 있습니다. 단어가 같다고 고르면 틀립니다."),
    ("Z", "숫자·시간", "Zahlen und Zeit", "시각, 요일, 나이 제한이 나옵니다. 계산하거나 비교해야 할 때가 많습니다."),
    ("S", "말하는 사람", "Sprecher / Perspektive", "누가 말했는지, 누가 한 일인지를 묻습니다. 진행자가 정리한 말과 손님이 직접 한 말을 구별해야 합니다."),
    ("B", "조건·예외", "Bedingung / Ausnahme", "nur wenn, falls, gegen Gebühr, in Begleitung 같은 조건이나 예외가 답을 정합니다."),
]

SCHREIBEN_INTRO = ("쓰기 시험은 60분이고 과제는 세 개입니다. Aufgabe 1은 친구에게 보내는 E-Mail(약 80단어, 20분), "
                   "Aufgabe 2는 방명록에 올리는 의견 글(Diskussionsbeitrag, 약 80단어, 25분), "
                   "Aufgabe 3은 격식을 갖춘 짧은 E-Mail(약 40단어, 15분)입니다. 어느 과제부터 써도 됩니다. "
                   "친구에게는 du, 집주인·상사·선생님에게는 Sie를 끝까지 지키고, 쓰고 나서 부문장의 동사 위치와 명사의 대문자를 확인하십시오.")

# 시험지 18쪽 „Bewertung“과 guide-data.json 기준
SCHREIBEN_CRITERIA = [
    ["Erfüllung", "과제 수행", "Leitpunkt를 모두 다루었는지, 글의 종류와 말투(du/Sie)가 맞는지, 분량이 맞는지를 봅니다. Leitpunkt가 하나 빠질 때마다 한 단계씩 내려갑니다."],
    ["Kohärenz", "글의 연결", "호칭, 도입, 맺음이 갖추어졌는지, weil, deshalb, trotzdem 같은 연결어로 문장이 이어지는지를 봅니다."],
    ["Wortschatz", "어휘", "주제에 맞는 어휘를 다양하게 썼는지를 봅니다. 실수가 있어도 뜻이 통하면 감점이 작습니다."],
    ["Strukturen", "문법", "부문장(weil, dass, wenn, obwohl), 제안과 부탁의 접속법 2식(könnte, wäre es möglich) 같은 구조를 정확하게 썼는지를 봅니다."],
]
SCHREIBEN_NOTE = ("Aufgabe 1은 40점, Aufgabe 2는 40점, Aufgabe 3은 20점으로 합계 100점이고, 60점 이상이면 합격입니다. "
                  "기준마다 A–E 다섯 단계로 채점하며, Erfüllung이 E이면(주제와 상관없는 글) 그 과제는 0점입니다.")
POINTS_TITLE = {1: "Leitpunkt 세 개와 쓸 수 있는 문장", 2: "글의 구성과 쓸 수 있는 문장", 3: "꼭 써야 할 내용과 쓸 수 있는 문장"}

SPRECHEN = {
    "head": "약 15분, 두 사람이 함께 · 준비 시간 15분",
    "intro": ("말하기 시험은 두 사람이 함께 봅니다. 시험 전에 15분 동안 혼자 준비하면서 메모를 만들 수 있습니다. "
              "시험에서는 메모를 읽지 말고 키워드만 보면서 말해야 합니다."),
    "names": ["Gemeinsam etwas planen", "Ein Thema präsentieren", "Über ein Thema sprechen"],
    "meta": ["약 3분 · 28점", "약 3분 · 40점", "약 2분 · 16점"],
    "note": "모범 대화와 모범 발표는 시험지 19쪽에 있습니다. 발음(Aussprache)은 세 부분을 통틀어 16점으로 따로 채점합니다.",
    "t1": {
        "points": [
            "네 가지 점을 하나씩 모두 다루십시오. 마지막 „…“는 비어 있는 점입니다. 필요한 것을 하나 스스로 정해서 말합니다.",
            "제안에는 이유를 붙이십시오: Ich schlage vor, dass wir …, weil …",
            "파트너의 제안에 꼭 반응하십시오. 그대로 받거나(Einverstanden.), 일부만 받고 다른 안을 냅니다(Gute Idee, aber …).",
            "마지막에 정한 것을 한두 문장으로 정리하고, 누가 무엇을 맡는지 말하십시오: Also, ich kümmere mich um …, und du …",
            "시험지의 모범 대화처럼 파트너와는 du로 말하면 자연스럽습니다. 한번 정한 호칭은 끝까지 지키십시오.",
        ],
        "redemittel": [
            ["Ich schlage vor, dass wir …", "…하자고 제안해요."],
            ["Wie wäre es, wenn wir …?", "우리가 …하면 어때요?"],
            ["Was hältst du davon?", "그건 어떻게 생각해요?"],
            ["Gute Idee. / Einverstanden.", "좋은 생각이에요. / 좋아요, 그렇게 해요."],
            ["Das finde ich nicht so gut, weil …", "그건 별로인 것 같아요. 왜냐하면 …"],
            ["Ich würde lieber …", "저는 차라리 …하고 싶어요."],
            ["Könntest du … übernehmen?", "…를 맡아 줄 수 있어요?"],
            ["Dann machen wir es so: …", "그럼 이렇게 해요: …"],
        ],
    },
    "t2": {
        "task": ("두 주제 가운데 하나를 골라 약 3분 동안 발표합니다. 시험지에 Folie(슬라이드) 다섯 장이 인쇄되어 있고, "
                 "왼쪽 지시문대로 한 장씩 말하면 됩니다. 발표는 시험관과 파트너에게 합니다."),
        "folien": [
            ["Folie 1", "Stellen Sie Ihr Thema vor. Erklären Sie den Inhalt und die Struktur Ihrer Präsentation.", "주제를 소개하고, 발표의 내용과 순서를 알립니다."],
            ["Folie 2", "Berichten Sie von Ihrer Situation oder einem Erlebnis im Zusammenhang mit dem Thema.", "주제와 관련된 내 상황이나 경험을 이야기합니다."],
            ["Folie 3", "Berichten Sie von der Situation in Ihrem Heimatland und geben Sie Beispiele.", "내 나라(한국)의 상황을 예와 함께 이야기합니다."],
            ["Folie 4", "Nennen Sie die Vor- und Nachteile und sagen Sie dazu Ihre Meinung. Geben Sie auch Beispiele.", "장점과 단점을 말하고, 예를 들어 내 의견을 말합니다."],
            ["Folie 5", "Beenden Sie Ihre Präsentation und bedanken Sie sich bei den Zuhörern.", "발표를 마무리하고 듣는 사람에게 감사 인사를 합니다."],
        ],
        "note": "위 문장은 Folie 2–4에 쓸 수 있는 예입니다. Thema 1의 모범 발표 전체는 시험지 19쪽에 있습니다.",
        "points": [
            "시험관은 Folie 3(내 나라의 상황)과 Folie 4(이유가 있는 의견)에서 B1 수준인지를 봅니다. 이 두 장을 가장 충실하게 준비하십시오.",
            "다섯 장을 모두 다루어야 합니다. 한 장이라도 빠지면 과제 수행(Erfüllung) 점수가 내려갑니다. 한 장에 서너 문장이면 약 3분이 됩니다.",
            "Folie 1에서 순서를 먼저 알리십시오: Zuerst …, dann …, danach …, zum Schluss …",
            "Folie 2는 과거 시제로 내 경험을, Folie 3은 „In Korea …“로 한국의 상황을 말합니다. 정확한 통계는 필요 없습니다. 내가 아는 예를 하나 들면 됩니다.",
            "Folie 4에서는 장점과 단점을 하나 이상씩 말한 뒤 꼭 내 의견을 말하십시오: Meiner Meinung nach …",
            "메모는 문장이 아니라 키워드로 적으십시오. 메모를 그대로 읽으면 감점됩니다.",
        ],
        "redemittel": [
            ["Ich möchte heute über das Thema „…“ sprechen.", "Folie 1 · 오늘 „…“라는 주제로 이야기하겠습니다."],
            ["Zuerst erzähle ich von meinen Erfahrungen, dann …, danach … Zum Schluss fasse ich kurz zusammen.", "Folie 1 · 먼저 제 경험을 이야기하고, 그다음에 …, 그 뒤에 … 끝으로 짧게 정리하겠습니다."],
            ["Ich selbst … / Als ich …, habe ich …", "Folie 2 · 저는 … / 제가 …했을 때 …했습니다."],
            ["In meinem Heimatland Korea ist es so: …", "Folie 3 · 제 나라 한국에서는 이렇습니다: …"],
            ["Ein Vorteil ist, dass … Ein Nachteil ist, dass …", "Folie 4 · 장점은 …라는 것입니다. 단점은 …라는 것입니다."],
            ["Meiner Meinung nach …, weil …", "Folie 4 · 제 생각에는 … 왜냐하면 …"],
            ["Zusammenfassend kann ich sagen: …", "Folie 5 · 정리하면 이렇게 말할 수 있습니다: …"],
            ["Vielen Dank fürs Zuhören. Haben Sie noch Fragen?", "Folie 5 · 들어 주셔서 감사합니다. 질문이 있으십니까?"],
        ],
    },
    "t3": {
        "task": ("파트너의 발표가 끝나면 a) 발표가 어땠는지 피드백(Rückmeldung)을 하고 b) 발표에 대해 질문을 하나 합니다. "
                 "내 발표가 끝난 뒤에는 파트너와 시험관의 피드백과 질문에 대답합니다."),
        "points": [
            "피드백은 감사 → 내용 한 가지 → 질문의 순서로 하십시오. „Das war gut.“만 말하면 내용이 없는 피드백입니다.",
            "발표에서 들은 내용을 하나 짚어 말하십시오: Ich fand interessant, dass … / Das wusste ich nicht.",
            "질문은 발표 내용에 대한 진짜 질문이어야 합니다. 발표를 들으면서 궁금한 점을 한 단어로 적어 두십시오.",
            "질문을 받으면 짧게 답하고 이유를 한 문장 붙이십시오. 바로 생각나지 않으면 „Das ist eine gute Frage.“로 시간을 벌 수 있습니다.",
        ],
        "redemittel": [
            ["Vielen Dank für deine Präsentation.", "발표 고마워요."],
            ["Sie war klar aufgebaut und gut zu verstehen.", "구성이 분명하고 이해하기 쉬웠어요."],
            ["Ich fand besonders interessant, dass …", "…라는 점이 특히 흥미로웠어요."],
            ["Das wusste ich nicht. / Das war neu für mich.", "그건 몰랐어요. / 저에게는 새로운 내용이었어요."],
            ["Du hast gesagt, dass … Mich würde interessieren, ob …", "…라고 했는데, …인지 궁금해요."],
            ["Das ist eine gute Frage. Ich denke, …", "좋은 질문이에요. 제 생각에는 …"],
            ["Ehrlich gesagt …", "솔직히 말하면 …"],
        ],
    },
    # 시험지 19쪽 „Worauf die Prüfenden achten“
    "achten": [
        ["Teil 1", "네 가지 점 모두에 제안을 하고 이유를 말합니다. 파트너의 말에 반응하고(Einverstanden, aber …), 마지막에 함께 정한 결과를 정리합니다."],
        ["Teil 2", "구성을 먼저 알리고, 다섯 장을 모두 다루고, 예를 들고, 의견의 이유를 말하고, 감사 인사를 합니다."],
        ["Teil 3", "내용이 있는 피드백을 하고(„Das war gut“만으로는 부족합니다), 발표에 대한 진짜 질문을 하고, 시험관의 질문에 대답합니다."],
        ["Sprache", "발음을 알아들을 수 있어야 합니다. 뜻이 분명하게 전달되면 실수는 크게 방해가 되지 않습니다."],
    ],
}
