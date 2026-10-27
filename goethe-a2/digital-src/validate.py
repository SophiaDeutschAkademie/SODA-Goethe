#!/usr/bin/env python3
"""data/mtN.json 형식과 정답 검사 (Goethe-Zertifikat A2).

python3 digital-src/validate.py digital-src/data/mt*.json

검사 내용: 항목 번호와 개수, 보기 a/b/c, 정답이 보기 안에 있는지, Lesen Teil 4의 X 한 개, 안 쓰는 글자 계산,
그림 파일 존재, 쓰기 과제·모범 답안, index 블록. 같은 폴더의 PDF(`Goethe A2 Modelltest N.pdf`, 17쪽 Lösungsschlüssel)가 있으면
JSON의 정답 40개와 PDF 정답을 비교합니다(pdftotext 필요).
"""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
errors = []


def err(msg):
    errors.append(msg)


def need(cond, msg):
    if not cond:
        err(msg)


def nonempty(v):
    return isinstance(v, str) and v.strip() != ""


def check_abc(label, it, ex=False):
    need(nonempty(it.get("stem")), f"{label}: stem fehlt")
    o = it.get("options") or {}
    need(sorted(o) == ["a", "b", "c"], f"{label}: options a/b/c fehlen")
    for k in "abc":
        need(nonempty(o.get(k)), f"{label}: Option {k} leer")
    need(it.get("answer") in ("a", "b", "c"), f"{label}: answer {it.get('answer')!r}")


def check_img(label, p, base=ROOT):
    need(nonempty(p), f"{label}: img fehlt")
    if nonempty(p):
        need(os.path.exists(os.path.join(base, p)), f"{label}: Datei fehlt {p}")


def nos(items, first, last):
    return [it.get("no") for it in items] == [str(i) for i in range(first, last + 1)]


def pdf_answers(n):
    pdf = os.path.join(ROOT, f"Goethe A2 Modelltest {n}.pdf")
    if not os.path.exists(pdf):
        return None
    try:
        txt = subprocess.run(["pdftotext", "-f", "17", "-l", "17", "-layout", pdf, "-"], capture_output=True, text=True, check=True).stdout
    except Exception:
        return None
    out = {}
    # Spaltenweise: jede Zeile hat bis zu drei "nr antwort"-Paare
    for line in txt.splitlines():
        for m in re.finditer(r"(?<![\w.])(\d{1,2})\s{2,}([abc]|[a-i]|X|Ja|Nein)(?=\s{2,}|\s*$)", line):
            nr = int(m.group(1))
            if 1 <= nr <= 20 and m.group(2):
                out.setdefault(nr, []).append(m.group(2))
    return out


def validate(path):
    d = json.load(open(path, encoding="utf-8"))
    n = d.get("id")
    L, H, S, IX = d.get("lesen", {}), d.get("hoeren", {}), d.get("schreiben", {}), d.get("index", {})
    need(isinstance(n, int) and 1 <= n, "id fehlt")
    need(nonempty(d.get("roman")), "roman fehlt")
    got = {}  # Aufgabe -> Antwort (für den PDF-Vergleich), getrennt nach Lesen/Hören

    # ---------- Lesen
    t = L.get("t1", {})
    for k in ("instruction", "title", "lead", "tasksIntro", "image", "imageAlt", "quote", "source"):
        need(nonempty(t.get(k)), f"Lesen t1.{k} fehlt")
    need(len(t.get("paragraphs", [])) >= 3, "Lesen t1: weniger als 3 Absätze")
    check_img("Lesen t1.image", t.get("image"))
    check_abc("Lesen t1.example", t.get("example", {}))
    need(t.get("example", {}).get("no") == "0", "Lesen t1.example.no")
    need(nos(t.get("items", []), 1, 5), "Lesen t1: Items 1–5")
    for it in t.get("items", []):
        check_abc(f"Lesen {it.get('no')}", it)
        got[("L", int(it["no"]))] = it.get("answer")

    t = L.get("t2", {})
    need(nonempty(t.get("instruction")), "Lesen t2.instruction fehlt")
    b = t.get("board", {})
    need(nonempty(b.get("title")) and nonempty(b.get("label")), "Lesen t2.board title/label")
    need(len(b.get("rows", [])) >= 4, "Lesen t2.board: zu wenige Zeilen")
    for r in b.get("rows", []):
        need(nonempty(r.get("floor")) and nonempty(r.get("text")), "Lesen t2.board: leere Zeile")
    check_abc("Lesen t2.example", t.get("example", {}))
    need(nos(t.get("items", []), 6, 10), "Lesen t2: Items 6–10")
    for it in t.get("items", []):
        check_abc(f"Lesen {it.get('no')}", it)
        got[("L", int(it["no"]))] = it.get("answer")

    t = L.get("t3", {})
    need(nonempty(t.get("instruction")) and nonempty(t.get("tasksIntro")), "Lesen t3: instruction/tasksIntro")
    m = t.get("mail", {})
    for k in ("from", "to", "subject", "greeting"):
        need(nonempty(m.get(k)), f"Lesen t3.mail.{k} fehlt")
    need(len(m.get("paragraphs", [])) >= 3, "Lesen t3.mail: Absätze")
    need(len(m.get("closing", [])) >= 1, "Lesen t3.mail.closing")
    check_abc("Lesen t3.example", t.get("example", {}))
    need(nos(t.get("items", []), 11, 15), "Lesen t3: Items 11–15")
    for it in t.get("items", []):
        check_abc(f"Lesen {it.get('no')}", it)
        got[("L", int(it["no"]))] = it.get("answer")

    t = L.get("t4", {})
    need(nonempty(t.get("instruction")), "Lesen t4.instruction fehlt")
    ex = t.get("example", {})
    need(ex.get("no") == "0" and nonempty(ex.get("text")) and ex.get("answer") in list("abcdef"), "Lesen t4.example")
    need(nos(t.get("items", []), 16, 20), "Lesen t4: Items 16–20")
    used = []
    xs = 0
    for it in t.get("items", []):
        need(nonempty(it.get("text")), f"Lesen {it.get('no')}: text fehlt")
        a = it.get("answer")
        need(a in list("abcdef") + ["X"], f"Lesen {it.get('no')}: answer {a!r}")
        if a == "X":
            xs += 1
        else:
            used.append(a)
        got[("L", int(it["no"]))] = a
    need(xs == 1, f"Lesen t4: genau ein X erwartet, gefunden {xs}")
    need(len(set(used)) == len(used) and ex.get("answer") not in used, "Lesen t4: Buchstaben doppelt oder Beispiel wieder benutzt")
    free = sorted(set("abcdef") - set(used) - {ex.get("answer")})
    need(t.get("unused") == free, f"Lesen t4.unused {t.get('unused')} statt {free}")
    need(sorted(t.get("ads", {})) == list("abcdef"), "Lesen t4.ads a–f")
    for k, a in t.get("ads", {}).items():
        check_img(f"Lesen t4.ads.{k}", a.get("img"))
        need(nonempty(a.get("alt")) and len(a["alt"]) > 40, f"Lesen t4.ads.{k}.alt zu kurz")

    # ---------- Hören
    t = H.get("t1", {})
    need(nonempty(t.get("instruction")), "Hören t1.instruction fehlt")
    need(nos(t.get("items", []), 1, 5), "Hören t1: Items 1–5")
    for it in t.get("items", []):
        check_abc(f"Hören {it.get('no')}", it)
        got[("H", int(it["no"]))] = it.get("answer")

    t = H.get("t2", {})
    need(nonempty(t.get("instruction")), "Hören t2.instruction fehlt")
    ps = t.get("persons", [])
    need([p.get("no") for p in ps] == ["0", "6", "7", "8", "9", "10"], "Hören t2: Personen 0, 6–10")
    need(all(nonempty(p.get("name")) for p in ps), "Hören t2: Name fehlt")
    ans2 = [p.get("answer") for p in ps]
    need(all(a in list("abcdefghi") for a in ans2), f"Hören t2: Antworten {ans2}")
    need(len(set(ans2)) == len(ans2), "Hören t2: Buchstabe doppelt")
    free2 = sorted(set("abcdefghi") - set(ans2))
    need(t.get("unused") == free2, f"Hören t2.unused {t.get('unused')} statt {free2}")
    need(sorted(t.get("pictures", {})) == list("abcdefghi"), "Hören t2.pictures a–i")
    for k, a in t.get("pictures", {}).items():
        check_img(f"Hören t2.pictures.{k}", a.get("img"))
        need(nonempty(a.get("alt")), f"Hören t2.pictures.{k}.alt fehlt")
    for p in ps[1:]:
        got[("H", int(p["no"]))] = p.get("answer")

    t = H.get("t3", {})
    need(nonempty(t.get("instruction")), "Hören t3.instruction fehlt")
    need(nos(t.get("items", []), 11, 15), "Hören t3: Items 11–15")
    for it in t.get("items", []):
        no = it.get("no")
        need(nonempty(it.get("stem")), f"Hören {no}: stem fehlt")
        need(it.get("answer") in ("a", "b", "c"), f"Hören {no}: answer")
        need(sorted(it.get("options", {})) == ["a", "b", "c"], f"Hören {no}: options")
        for k, o in it.get("options", {}).items():
            check_img(f"Hören {no}{k}", o.get("img"))
            need(nonempty(o.get("alt")), f"Hören {no}{k}: alt fehlt")
        got[("H", int(no))] = it.get("answer")

    t = H.get("t4", {})
    need(nonempty(t.get("instruction")) and nonempty(t.get("context")), "Hören t4: instruction/context")
    need(t.get("example", {}).get("no") == "0" and t.get("example", {}).get("answer") in ("Ja", "Nein"), "Hören t4.example")
    need(nos(t.get("items", []), 16, 20), "Hören t4: Items 16–20")
    for it in t.get("items", []):
        need(nonempty(it.get("text")), f"Hören {it.get('no')}: text fehlt")
        need(it.get("answer") in ("Ja", "Nein"), f"Hören {it.get('no')}: answer {it.get('answer')!r}")
        got[("H", int(it["no"]))] = it.get("answer")

    # ---------- Schreiben
    need(nonempty(S.get("intro")), "Schreiben.intro fehlt")
    tasks = S.get("tasks", [])
    need(len(tasks) == 2, "Schreiben: zwei Aufgaben erwartet")
    for i, tk in enumerate(tasks):
        lab = f"Schreiben Aufgabe {i + 1}"
        need(tk.get("no") == i + 1, f"{lab}: no")
        need(tk.get("minutes") == (10, 20)[i] if i < 2 else False, f"{lab}: minutes {tk.get('minutes')}")
        need(tk.get("words") == ([20, 30], [30, 40])[i] if i < 2 else False, f"{lab}: words {tk.get('words')}")
        need(len(tk.get("situation", [])) >= 1 and all(nonempty(x) for x in tk.get("situation", [])), f"{lab}: situation")
        need(len(tk.get("points", [])) == 3 and all(nonempty(x) for x in tk.get("points", [])), f"{lab}: drei Inhaltspunkte erwartet")
        need(nonempty(tk.get("instruction")), f"{lab}: instruction")
        mdl = tk.get("model", {})
        need(nonempty(mdl.get("label")) and nonempty(mdl.get("text")), f"{lab}: model")
        need(nonempty(tk.get("typicalErrors")), f"{lab}: typicalErrors")
        words = len(re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9]+(?:['’\-][A-Za-zÀ-ÖØ-öø-ÿ0-9]+)*", re.sub(r"^Betreff:.*\n", "", mdl.get("text", ""))))
        need(words >= tk.get("words", [0, 0])[0], f"{lab}: Mustertext hat nur {words} Wörter")
    need([g.get("label") for g in S.get("good", [])] == ["Erfüllung", "Register", "Wortschatz", "Strukturen"], "Schreiben.good: Erfüllung/Register/Wortschatz/Strukturen")
    need(all(nonempty(g.get("text")) for g in S.get("good", [])), "Schreiben.good: Text")

    # ---------- index
    h = IX.get("hoeren", {})
    need(sorted(h) == ["t1", "t2", "t3", "t4"] and all(nonempty(v) for v in h.values()), "index.hoeren t1–t4")
    need(len(IX.get("schreiben", [])) == 2 and all(nonempty(v) for v in IX.get("schreiben", [])), "index.schreiben: 2 Titel")
    sp = IX.get("sprechen", {})
    need(len(sp.get("teil1", [])) == 8 and all(nonempty(v) for v in sp.get("teil1", [])), "index.sprechen.teil1: 8 Karten")
    need(len(sp.get("teil2", [])) == 2 and all(nonempty(v) for v in sp.get("teil2", [])), "index.sprechen.teil2: 2 Karten")
    need(nonempty(sp.get("teil3")), "index.sprechen.teil3")

    # ---------- Vergleich mit dem Lösungsschlüssel im PDF
    pa = pdf_answers(n) if isinstance(n, int) else None
    if pa is None:
        print(f"  Hinweis: PDF-Vergleich übersprungen (Goethe A2 Modelltest {n}.pdf oder pdftotext fehlt)")
    else:
        # Zeilen "nr antwort" erscheinen in der Reihenfolge Lesen 1–15, Lesen 16–20, Hören 1–5, Hören 6–10, Hören 11–15, Hören 16–20
        want = {}
        for (mod, nr), a in got.items():
            want.setdefault(nr, {})[mod] = a
        for nr in range(1, 21):
            vals = pa.get(nr, [])
            exp = []
            if nr <= 5 or 11 <= nr <= 15 or True:
                pass
            for mod in ("L", "H"):
                if mod in want.get(nr, {}):
                    exp.append(want[nr][mod])
            need(sorted(exp) == sorted(vals[:len(exp)]) or sorted(exp) == sorted(vals), f"PDF-Lösungsschlüssel: Aufgabe {nr}: JSON {exp}, PDF {vals}")
    return d


def main():
    files = sys.argv[1:]
    if not files:
        sys.exit(__doc__)
    bad = 0
    for p in files:
        errors.clear()
        try:
            validate(p)
        except Exception as e:  # kaputtes JSON oder fehlende Felder
            err(f"Ausnahme: {type(e).__name__}: {e}")
        if errors:
            bad += 1
            print(f"{os.path.basename(p)}: {len(errors)} Fehler")
            for m in errors:
                print("  -", m)
        else:
            print(f"{os.path.basename(p)}: OK")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
