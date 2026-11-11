#!/usr/bin/env python3
"""Goethe B1 해설 데이터 점검 — 의심스러운 곳을 알려 줍니다(멈추지 않음).

python3 -I check.py <app-folder> <N> [<N> …]      N을 생략하면 erkN_lesen.py가 있는 모든 회차

살펴보는 것
  1. 해설 글(why, wrong, trap, unused) 속의 „…“ 인용이 그 시험의 본문·대본·문항에 있는지
  2. 반말, ‘~다’ 체, 해요체가 설명 글에 섞였는지 / ‘von Beruf’, 낮은 따옴표 ‚
  3. 말하기 Teil 1의 제목과 점, Teil 2의 주제가 PDF 14–16쪽과 같은지 (pdftotext 필요)
  4. Lesen 3의 unused가 실제로 쓰이지 않는 광고를 모두 말하는지
  5. 빠진 키, 빈 글, 문항 수
  6. tip이 ‘문항 순서와 본문 순서가 같다’고 하는데 실제 인용 위치가 어긋나는지
"""
import glob
import importlib
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
APP = sys.argv[1]
NS = [int(x) for x in sys.argv[2:]] or sorted(int(re.search(r"erk(\d+)_lesen", f).group(1)) for f in glob.glob(os.path.join(HERE, "erk*_lesen.py")))


def flat(o):
    """dict·list 안의 모든 문자열."""
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for v in o.values():
            yield from flat(v)
    elif isinstance(o, (list, tuple)):
        for v in o:
            yield from flat(v)


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def pdftext(pdf, page):
    try:
        return norm(subprocess.run(["pdftotext", "-layout", "-f", str(page), "-l", str(page), pdf, "-"],
                                   capture_output=True, text=True).stdout)
    except OSError:
        return None


BAD_END = re.compile(r"(?<![니까])다[.!]?$")          # ~한다. ~이다. (합니다/입니다는 통과)
YO_END = re.compile(r"[요죠][.!?]?$")


def sentences(t):
    t = re.sub(r"„[^“]*“", "Q", t)                    # 독일어 인용은 뺍니다
    t = re.sub(r"‘[^’]*’", "q", t)                    # 뜻풀이 따옴표 안은 뺍니다
    t = re.sub(r"\([^)]*\)", "", t)
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", t) if s.strip()]


total = 0
for N in NS:
    warn = []
    W = warn.append
    D = json.load(open(os.path.join(APP, "digital-src", "data", f"mt{N}.json"), encoding="utf-8"))
    for m in (f"erk{N}_lesen", f"erk{N}_hoeren"):
        sys.modules.pop(m, None)
    le = importlib.import_module(f"erk{N}_lesen")
    ho = importlib.import_module(f"erk{N}_hoeren")
    corpus = norm(" ".join(flat({k: D[k] for k in ("lesen", "hoeren", "hoertexte", "schreiben")})))

    def items(part):
        if "texts" in part:
            return [i for t in part["texts"] for i in t["items"]]
        return part["items"]

    parts = [("L1", le.LESEN1), ("L2", le.LESEN2), ("L3", le.LESEN3), ("L4", le.LESEN4), ("L5", le.LESEN5),
             ("H1", ho.HOEREN1), ("H2", ho.HOEREN2), ("H3", ho.HOEREN3), ("H4", ho.HOEREN4)]
    want = {"L1": 6, "L2": 6, "L3": 7, "L4": 7, "L5": 4, "H1": 10, "H2": 5, "H3": 7, "H4": 8}
    for name, part in parts:
        its = items(part)
        if len(its) != want[name]:
            W(f"{name}: 문항 {len(its)}개 (기대 {want[name]})")
        if not part.get("tip"):
            W(f"{name}: tip 없음")
        for it in its:
            where = f"{name} {it['no']}"
            for k in ("basis", "why"):
                if not it.get(k):
                    W(f"{where}: {k} 없음")
            if name in ("L1", "L3", "H1", "H2", "H3", "H4") and not it.get("stko"):
                W(f"{where}: stko 없음")
            if name in ("L2", "L5", "H2") or (name == "H1" and it["ans"] in "abc"):
                w = it.get("wrong", {})
                if sorted(w) != sorted(set("abc") - {it["ans"]}):
                    W(f"{where}: wrong 보기 {sorted(w)} (정답 {it['ans']})")
                if name in ("H1", "H2") and "…" not in it["stko"]:
                    W(f"{where}: a/b/c 줄기 번역에 …가 없음")
            if name in ("L1", "L2", "L5") and len(it.get("vocab", [])) < 3:
                W(f"{where}: vocab {len(it.get('vocab', []))}개")
            # 1. 해설 글 속 „…“ 인용
            texts = [it.get("why", ""), it.get("trap", "") or ""] + list(it.get("wrong", {}).values())
            for t in texts:
                for q in re.findall(r"„([^“]+)“", t):
                    for piece in re.split(r"\s*…\s*", q):
                        piece = piece.strip(" .,;:!?")
                        if len(piece) >= 8 and piece not in corpus:
                            W(f"{where}: 원문에 없는 „…“: {piece[:70]}")
            # 2. 어조
            for k, t in [("why", it.get("why", "")), ("trap", it.get("trap", "") or "")] + [(f"wrong {a}", b) for a, b in it.get("wrong", {}).items()]:
                for s in sentences(t):
                    if BAD_END.search(s):
                        W(f"{where} {k}: ‘~다’ 체? … {s[-40:]}")
                    if YO_END.search(s):
                        W(f"{where} {k}: 해요체? … {s[-40:]}")
            if it.get("stko"):
                for s in sentences(it["stko"]):
                    if BAD_END.search(s) or YO_END.search(s):
                        W(f"{where} stko: 합니다체가 아님 … {s[-40:]}")
        for k in ("intro", "tip", "unused"):
            for s in sentences(part.get(k, "") or ""):
                if BAD_END.search(s) or YO_END.search(s):
                    W(f"{name} {k}: 어조 … {s[-40:]}")
    # 6. 문항 순서와 본문·대본 순서 (tip이 ‘순서가 같다’고 말하는데 어긋나면 알림)
    L_, HT_ = D["lesen"], D["hoertexte"]
    b_ = L_["t1"]["blog"]
    src = {"L1": " ".join(b_["paragraphs"]),
           "L5": " ".join(s_["heading"] + " " + s_["text"] for s_ in L_["t5"]["doc"]["sections"]),
           "H2": HT_["t2"]["text"].replace("\n\n", " "),
           "H3": " ".join(u["text"] for u in HT_["t3"]["turns"]),
           "H4": " ".join(u["text"] for u in HT_["t4"]["turns"])}
    for name, part in parts:
        if name not in src:
            continue
        # 문항마다 인용 위치의 (가장 앞, 가장 뒤). 뒤 문항의 인용이 모두 앞 문항의 인용보다 앞에 있으면 순서가 바뀐 것
        pos = []
        for it in part["items"]:
            ps = [src[name].find(b[0]) for b in it["basis"]]
            if name == "H4":   # 정답인 사람이 말한 인용만
                spk = D["hoeren"]["t4"]["speakers"]
                ps = [src[name].find(b[0]) for b in it["basis"]
                      if any(b[0] in u["text"] and u["who"] in spk[it["ans"]] for u in HT_["t4"]["turns"])]
            ps = [x for x in ps if x >= 0] or [-1]
            pos.append((it["no"], min(ps), max(ps)))
        bad = [f"{b[0]}번이 {a[0]}번보다 먼저" for a, b in zip(pos, pos[1:]) if 0 <= b[2] < a[1]]
        if bad and re.search(r"순서(가|와)[^.]*같습니다", part.get("tip", "")) and "대체로" not in part.get("tip", ""):
            W(f"{name} tip: 순서가 같다고 했지만 원문에서는 {', '.join(bad)} 나옵니다")
        elif bad:
            print(f"   (참고) MT{N} {name}: 원문에서 {', '.join(bad)}")
    # 4. Lesen 3 unused
    t3 = D["lesen"]["t3"]
    used = {i["answer"] for i in t3["items"]} | {t3["example"]["answer"]}
    for a in t3["ads"]:
        if a["letter"] not in used and not re.search(rf"(?<![a-zA-Z]){a['letter']}(?![a-zA-Z])", le.LESEN3.get("unused", "")):
            W(f"L3 unused: 쓰이지 않는 광고 {a['letter']}에 대한 말이 없음")
    # 쓰기·말하기
    S, SP = ho.SCHREIBEN, ho.SPRECHEN
    for k, t in enumerate(S["tasks"], 1):
        for key in ("title", "situation", "points", "traps", "model_ko", "redemittel"):
            if not t.get(key):
                W(f"Schreiben {k}: {key} 없음")
        if k == 2 and not t.get("post_ko"):
            W("Schreiben 2: post_ko 없음")
        for s in [x for tr in t.get("traps", []) for x in sentences(tr)] + sentences(t.get("situation", "")):
            if BAD_END.search(s) or YO_END.search(s):
                W(f"Schreiben {k}: 어조 … {s[-40:]}")
    for key in ("title", "task", "leit", "muster", "redemittel"):
        if not SP["t1"].get(key):
            W(f"Sprechen 1: {key} 없음")
    if len(SP["t1"].get("leit", [])) != 4:
        W(f"Sprechen 1: leit {len(SP['t1'].get('leit', []))}개")
    if len(SP["t2"].get("themen", [])) != 2 or any(len(th.get("ideas", [])) != 3 for th in SP["t2"].get("themen", [])):
        W("Sprechen 2: themen 2개, ideas 3개씩이어야 함")
    if not SP["t3"].get("fragen"):
        W("Sprechen 3: fragen 없음")
    for s in [x for t in (SP["t1"].get("points", []) + [SP["t1"].get("task", ""), SP["t1"].get("muster", ""), SP["t3"].get("muster", "")]
                          + SP["t2"].get("points", []) + SP["t3"].get("points", [])) for x in sentences(t)]:
        if BAD_END.search(s) or YO_END.search(s):
            W(f"Sprechen: 어조 … {s[-40:]}")
    # 3. PDF 대조
    pdf = os.path.join(APP, f"Goethe B1 Modelltest {N}.pdf")
    p14 = pdftext(pdf, 14)
    if p14 is None:
        W("pdftotext가 없어 말하기 과제를 PDF와 대조하지 못함")
    else:
        if norm(SP["t1"]["title"]) not in p14:
            W(f"Sprechen 1: 제목이 14쪽에 없음: {SP['t1']['title']}")
        for a, _ in SP["t1"]["leit"]:
            if norm(a) not in p14:
                W(f"Sprechen 1: 14쪽에 없는 점: {a}")
        for pg, th in zip((15, 16), SP["t2"]["themen"]):
            words = re.findall(r"\w+", th["title"])
            px = pdftext(pdf, pg)
            if not all(w in px for w in words):
                W(f"Sprechen 2: {pg}쪽에 없는 주제: {th['title']}")
        p19 = pdftext(pdf, 19).replace("- ", "")
        for a, _ in SP["t1"]["redemittel"]:
            a2 = norm(a).rstrip(".?!")
            if a2.replace("-", "") not in p19.replace("-", "") and not all(w in p19 for w in re.findall(r"\w{5,}", a2)):
                W(f"Sprechen 1: 19쪽 모범 대화에 없는 표현(직접 쓴 문장이면 무시): {a}")
    # 공통
    blob = " ".join(flat([p for _, p in parts] + [S, SP]))
    if "von Beruf" in blob:
        W("‘von Beruf’ 표현이 있음")
    if "‚" in blob:
        W("낮은 따옴표 ‚ 가 있음")
    if re.search(r"[가-힣]'|'[가-힣]", blob):
        W("곧은 따옴표 ' 가 한국어에 붙어 있음 (‘ ’로)")
    print(f"== Modelltest {N}: {len(warn)}건")
    for w in warn:
        print("  ·", w)
    total += len(warn)
print(f"합계 {total}건")
