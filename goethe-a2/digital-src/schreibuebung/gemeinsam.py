# Goethe-Zertifikat A2 작문 연습 — 모든 Modelltest가 함께 쓰는 글
# 글 속의 «…»는 독일어 조각입니다(빌드가 <b lang="de">로 바꿉니다).

LEAD = "A1 수준의 답안을 주어진 A2 표현으로 고쳐 씁니다 · Schreiben Aufgabe 1·2"

STEPS = [
    ["과제와 A1 답안 읽기",
     "A1 답안에는 세 가지 내용이 다 들어 있습니다. 다만 짧은 문장만 늘어놓았고, 이유와 질문, 부탁을 아주 단순하게 씁니다."],
    ["주어진 표현으로 고쳐 쓰기",
     "번호마다 A1 문장과 쓸 표현, 도움말이 있습니다. 그 표현을 넣어 A1 문장을 A2 문장으로 다시 씁니다. 쓴 내용은 이 브라우저에 저절로 저장됩니다."],
    ["예시와 비교하기",
     "다 쓴 뒤 「예시 보기」를 눌러 A2 예시와 비교합니다. 예시는 답의 한 가지일 뿐입니다. 주어진 표현을 맞게 썼다면 다르게 써도 됩니다."],
    ["글 전체 확인하기",
     "「내 글 전체」에서 고쳐 쓴 문장이 이어진 글과 단어 수를 확인합니다. 소피아 독일어학원 수강생은 맨 아래에서 선생님께 제출할 수 있습니다."],
]

# 사용법 아래의 짧은 안내
HOW_NOTE = ("시험에서는 두 과제를 모두 씁니다(30분). 첫째 과제(Aufgabe 1)는 친구에게 보내는 SMS로 20–30단어, "
            "둘째 과제(Aufgabe 2)는 E-Mail로 30–40단어이며, 호칭과 끝인사, 이름도 단어 수에 넣어 셉니다.")

DIFF_TITLE = "A1 답안과 A2 답안은 이렇게 다릅니다"
DIFF = [
    ["문장 잇기", "짧은 문장을 마침표로 늘어놓습니다. «Ich komme spät. Der Zug ist nicht pünktlich.»",
     "und, aber, denn, deshalb, weil, wenn으로 이어 씁니다. «Ich komme leider zu spät, weil mein Zug Verspätung hat.»"],
    ["지난 일", "지금 상태만 씁니다. «Der Reifen ist kaputt.»",
     "현재완료로 무슨 일이 있었는지 씁니다. «Ein Reifen ist kaputtgegangen. / Ich habe … gefunden.»"],
    ["질문", "그대로 짧게 묻습니다. «Wann ist die Rezeption offen?»",
     "간접 의문문으로 정중하게 묻습니다. «Könnten Sie mir sagen, bis wann …? / Ich möchte wissen, ob …»"],
    ["부탁과 제안", "«Ich will Größe 41. / Wir treffen uns um 19 Uhr.»",
     "접속법 2식과 질문으로 부드럽게 씁니다. «Ich hätte gern … / Würden Sie mir … schicken? / Wollen wir uns … treffen?»"],
    ["사과", "«Entschuldigung!»", "«Entschuldige bitte, das wollte ich nicht!»"],
]
DIFF_NOTE = ("이 차이는 쓰기 채점 기준 Sprache(어휘와 문장 구조가 다양하고 정확한가)에 그대로 나타납니다. "
             "세 가지 내용이 같아도 문장을 잇고 정중한 표현을 쓰면 A2 답안이 됩니다.")

# 과제마다 맨 위에 붙는 짧은 안내. 호칭이 «Sehr geehrte …»이면 Sie, 아니면 du로 봅니다.
KIND = {"du": "친구에게 보내는 {kind} · du", "Sie": "격식 있는 {kind} · Sie"}

# 내 글 전체 아래의 제출 전 확인(마지막 줄의 단어 수 확인은 빌드가 과제의 범위로 붙입니다)
CHECK = {
    "du": ["세 가지 내용(Punkt 1–3)을 모두 썼습니까?",
           "친구에게 du, dir, dein으로 썼습니까?",
           "호칭 뒤에 쉼표를 찍고, 다음 줄을 소문자로 시작했습니까?",
           "weil, dass, wenn, ob 뒤에서 동사를 맨 끝에 두었습니까?"],
    "Sie": ["«Sehr geehrte …,»로 시작하고 «Mit freundlichen Grüßen»으로 끝냈습니까?",
            "«Sie, Ihnen, Ihr»를 대문자로 쓰고, 중간에 du로 바꾸지 않았습니까?",
            "세 가지 내용(Punkt 1–3)을 모두 썼습니까?",
            "질문과 부탁을 정중하게 썼습니까? «Könnten Sie …? / Ich hätte gern …»"],
}

# 내 글 전체와 예시의 단어 수 기준(쓰기 가이드와 같음): 호칭, 본문, 끝인사, 이름을 모두 셉니다.
# 범위는 과제(../data/mtN.json의 words)에서 가져옵니다.
COUNT_NOTE = "호칭, 끝인사, 이름도 셉니다"

SUBMIT_TITLE = "선생님께 제출하기"
SUBMIT_TAG = "소피아 독일어학원 수강생 전용"
SUBMIT_TEXT = [
    "이 제출하기는 <b>소피아 독일어학원 수강생 전용</b>입니다. 수강생이 아니라면 제출하지 말고 「전체 복사」나 「txt 저장」으로 글을 보관하십시오.",
    "제출하면 Aufgabe 1·2에서 고쳐 쓴 문장과 완성한 글이 선생님 메일로 전송됩니다. 선생님이 확인한 뒤 알려 드립니다. 제출 전에 이름을 확인하십시오.",
]
