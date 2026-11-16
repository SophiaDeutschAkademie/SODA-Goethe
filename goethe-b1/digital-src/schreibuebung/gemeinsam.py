# Goethe-Zertifikat B1 작문 연습 — 모든 Modelltest가 함께 쓰는 글
# 글 속의 «…»는 독일어 조각입니다(빌드가 <b lang="de">로 바꿉니다).

LEAD = "A2 수준의 답안을 주어진 B1 표현으로 고쳐 씁니다 · Schreiben Aufgabe 1–3"

STEPS = [
    ["과제와 A2 답안 읽기",
     "A2 답안에는 과제의 내용이 다 들어 있습니다. 다만 짧은 문장을 늘어놓았고, 문장을 잇는 말과 이유가 부족합니다."],
    ["주어진 표현으로 고쳐 쓰기",
     "번호마다 A2 문장과 쓸 표현, 도움말이 있습니다. 그 표현을 넣어 A2 문장을 B1 문장으로 다시 씁니다. 쓴 내용은 이 브라우저에 저절로 저장됩니다."],
    ["예시와 비교하기",
     "다 쓴 뒤 「예시 보기」를 눌러 B1 예시와 비교합니다. 예시는 답의 한 가지일 뿐입니다. 주어진 표현을 맞게 썼다면 다르게 써도 됩니다."],
    ["글 전체 확인하기",
     "「내 글 전체」에서 고쳐 쓴 문장이 이어진 글과 단어 수를 확인합니다. 소피아 독일어학원 수강생은 맨 아래에서 선생님께 제출할 수 있습니다."],
]

DIFF_TITLE = "A2 답안과 B1 답안은 이렇게 다릅니다"
DIFF_HEAD = ["", "A2 답안", "B1 답안"]
DIFF = [
    ["문장 잇기", "짧은 문장을 마침표로 늘어놓습니다. «Wir haben in einem Hostel gewohnt. Das Hostel liegt in Kreuzberg.»",
     "weil, dass, wenn, obwohl, 관계대명사로 이어 한 문장으로 만듭니다. «… in einem Hostel, das in Kreuzberg liegt.»"],
    ["이유", "좋았다, 중요하다고만 씁니다. «Das war am besten.»",
     "weil, denn, deshalb로 이유를 붙입니다. «Am besten hat mir … gefallen, weil …»"],
    ["제안과 부탁", "그대로 말하거나 명령합니다. «Kommst du mit? / Schreiben Sie mir.»",
     "접속법 2식으로 부드럽게 씁니다. «Wie wäre es, wenn …? / Könnten Sie …?»"],
    ["의견", "«Ich finde: … ist gut.»",
     "«Meiner Meinung nach … / Ich bin davon überzeugt, dass … / Einerseits …, andererseits …»"],
    ["말투 (Aufgabe 3)", "«Hallo Frau …, / Liebe Grüße»", "«Sehr geehrte Frau …, / Mit freundlichen Grüßen»"],
]
DIFF_NOTE = ("이 차이는 쓰기 채점 기준의 Kohärenz(글의 연결), Wortschatz(어휘), Strukturen(문법)에 그대로 나타납니다. "
             "같은 내용이라도 문장을 이어 쓰고 이유와 정중한 표현을 넣으면 B1 답안이 됩니다.")

# 과제마다 맨 위에 붙는 짧은 안내
KIND = {1: "친구에게 쓰는 E-Mail · du", 2: "방명록에 올리는 의견 글 · 호칭과 끝인사 없음", 3: "격식 있는 E-Mail · Sie"}

# 내 글 전체 아래의 제출 전 확인
CHECK = {
    1: ["세 가지 Leitpunkt(묘사, 이유, 제안)를 모두 썼습니까?",
        "친구에게 du, dir, dein으로 썼습니까?",
        "호칭 뒤에 쉼표를 찍고, 다음 줄을 소문자로 시작했습니까?",
        "weil, dass, wenn 같은 부문장에서 동사를 맨 끝에 두었습니까?",
        "약 80단어입니까?"],
    2: ["글쓴이의 글에 먼저 반응했습니까?",
        "내 의견과 이유, 내 경험의 예를 썼습니까?",
        "반대쪽 의견을 한 번 인정하고, 마무리 문장으로 끝냈습니까?",
        "호칭과 끝인사 없이 썼습니까?",
        "약 80단어입니까?"],
    3: ["«Sehr geehrte(r) …,»로 시작하고 «Mit freundlichen Grüßen»으로 끝냈습니까?",
        "«Sie, Ihnen, Ihr»를 대문자로 썼습니까?",
        "과제가 요구한 내용(사과, 이유, 제안이나 질문)을 모두 썼습니까?",
        "약 40단어입니까?"],
}

# 글을 이어 붙일 때 문단 나누기: Aufgabe 1·2에서 같은 번호끼리 한 문단이 됩니다.
# Aufgabe 3은 호칭·끝인사·이름만 따로 줄이고 나머지는 한 문단입니다.
PARA = {
    "도입": 1, "Leitpunkt 1": 1, "Leitpunkt 2": 2, "Leitpunkt 3": 3, "마무리": 3,
    "반응": 1, "의견": 1, "이유": 2, "예": 2, "반대 의견": 3, "의견 정리": 3,
}

# 내 글 전체와 예시의 단어 수 기준(쓰기 가이드와 같음). 이름, 호칭, 끝인사를 함께 셉니다.
RANGE = {1: (70, 100), 2: (70, 100), 3: (33, 50)}
TARGET = {1: 80, 2: 80, 3: 40}

SUBMIT_TITLE = "선생님께 제출하기"
SUBMIT_TAG = "소피아 독일어학원 수강생 전용"
SUBMIT_TEXT = [
    "이 제출하기는 <b>소피아 독일어학원 수강생 전용</b>입니다. 수강생이 아니라면 제출하지 말고 「전체 복사」나 「txt 저장」으로 글을 보관하십시오.",
    "제출하면 Aufgabe 1–3에서 고쳐 쓴 문장과 완성한 글이 선생님 메일로 전송됩니다. 선생님이 확인한 뒤 알려 드립니다. 제출 전에 이름을 확인하십시오.",
]
