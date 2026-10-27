#!/usr/bin/env python3
"""Validate a Modelltest JSON file against SCHEMA.md (Goethe-Zertifikat B2).

Usage: python3 digital-src/validate.py digital-src/data/mt1.json [more files...]
Prints errors (must fix) and warnings (check), then a compact answer summary
to compare against the Lösungsschlüssel (PDF page 17).
"""
import json
import re
import sys

RF = {"R", "F"}
ABC = {"a", "b", "c"}
ABCD = set("abcd")
A_H = set("abcdefgh")

SUSPICIOUS = [
    (re.compile(r"[|{}]"), "OCR-Artefakt (| { })"),
    (re.compile(r"neseL|neröH|nebierhcS|nehcerpS|Kandidatenblätter|vorgeschlagene Arbeitszeit"), "Seitenrand/Kopfzeile im Text"),
    (re.compile(r"­"), "weiches Trennzeichen (U+00AD)"),
    (re.compile(r"[a-zäöüß]- [a-zäöüß]"), "möglicher Trennstrich am Zeilenende nicht entfernt (oder Ergänzungsstrich – prüfen)"),
    (re.compile(r"  "), "doppeltes Leerzeichen"),
    (re.compile(r"\s[,.;:!?]"), "Leerzeichen vor Satzzeichen"),
    (re.compile(r"^\s|\s$"), "Leerzeichen am Anfang/Ende"),
    (re.compile(r"[A-Za-zäöüß]{2,}[0-9]|[0-9][a-zäöüß]{3,}"), "Buchstabe/Ziffer verklebt (OCR?)"),
    (re.compile(r"\b(?:[a-z]+[A-Z]{2,}[a-z]*)\b"), "Groß/Kleinschreibung mitten im Wort (OCR?)"),
    (re.compile(r"—"), "Geviertstrich — (im Original meist Halbgeviert –)"),
    (re.compile(r"\"|''|``"), "gerade Anführungszeichen statt „…“"),
]
GAP = re.compile(r"\[(\d+)\]")


class V:
    def __init__(self, path):
        self.path = path
        self.errors = []
        self.warnings = []

    def err(self, where, msg):
        self.errors.append(f"{where}: {msg}")

    def warn(self, where, msg):
        self.warnings.append(f"{where}: {msg}")

    def text(self, where, s, required=True, check=True):
        if s is None or (isinstance(s, str) and not s.strip()):
            if required:
                self.err(where, "leer")
            return
        if not isinstance(s, str):
            self.err(where, f"kein String: {type(s).__name__}")
            return
        if check:
            s2 = GAP.sub("N", s)
            for rx, label in SUSPICIOUS:
                m = rx.search(s2)
                if m:
                    a = max(0, m.start() - 25)
                    self.warn(where, f"{label}: …{s2[a:m.end() + 25]}…")
            if re.search(r"[\[\]]", s2):
                self.warn(where, "eckige Klammer außerhalb von Lücken [N]")

    def texts(self, where, arr, minlen=1):
        if not isinstance(arr, list):
            self.err(where, "keine Liste")
            return
        if len(arr) < minlen:
            self.err(where, f"zu wenige Einträge ({len(arr)} < {minlen})")
        for i, s in enumerate(arr):
            self.text(f"{where}[{i}]", s)

    def numbered(self, where, items, nums):
        if not isinstance(items, list):
            self.err(where, "keine Liste")
            return []
        got = [str(it.get("no")) for it in items]
        if got != [str(n) for n in nums]:
            self.err(where, f"Nummern {got} erwartet {[str(n) for n in nums]}")
        return items

    def rf(self, where, it):
        self.text(f"{where}.text", it.get("text"))
        if it.get("answer") not in RF:
            self.err(f"{where}.answer", f"ungültig: {it.get('answer')!r} (erlaubt {sorted(RF)})")

    def abc(self, where, it):
        self.text(f"{where}.stem", it.get("stem"))
        opts = it.get("options")
        if not isinstance(opts, dict) or set(opts) != ABC:
            self.err(f"{where}.options", f"braucht genau a, b, c: {opts!r}")
        else:
            for k in "abc":
                self.text(f"{where}.options.{k}", opts[k])
                if re.match(r"^\s*[abc]\s", opts[k] or ""):
                    self.warn(f"{where}.options.{k}", "Antwortbuchstabe am Anfang mit abgeschrieben?")
        ans = it.get("answer")
        if ans not in ABC:
            self.err(f"{where}.answer", f"ungültig: {ans!r}")

    def letters(self, where, d, allowed):
        if not isinstance(d, dict) or set(d) != set(allowed):
            self.err(where, f"braucht genau {''.join(sorted(allowed))}: {sorted(d) if isinstance(d, dict) else d!r}")
            return {}
        for k in sorted(d):
            self.text(f"{where}.{k}", d[k])
        return d

    def partition(self, where, answers, example, unused, universe=A_H):
        used = list(answers)
        if example:
            used.append(example)
        used += list(unused or [])
        if sorted(used) != sorted(universe):
            self.err(where, f"Antworten {answers} + Beispiel {example} + nicht gebraucht {unused} ergeben nicht a–h genau einmal")


def validate(path):
    v = V(path)
    try:
        d = json.load(open(path, encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        print(f"{path}: JSON-Fehler: {e}")
        return False
    for k in ("id", "roman", "lesen", "hoeren", "schreiben"):
        if k not in d:
            v.err("top", f"fehlt: {k}")
    if v.errors:
        report(v, d)
        return False
    L, H, S = d["lesen"], d["hoeren"], d["schreiben"]
    summary = {}

    # ---- Lesen t1: Forum, 4 Personen a-d, Aufgaben 1-9
    t = L.get("t1", {})
    v.text("lesen.t1.instruction", t.get("instruction"))
    f = t.get("forum", {})
    v.text("lesen.t1.forum.title", f.get("title"))
    posts = f.get("posts", [])
    if [p.get("letter") for p in posts] != list("abcd"):
        v.err("lesen.t1.forum.posts", f"Buchstaben {[p.get('letter') for p in posts]} – erwartet a–d")
    for p in posts:
        w = f"lesen.t1.forum.posts.{p.get('letter')}"
        v.text(f"{w}.name", p.get("name"))
        v.text(f"{w}.time", p.get("time"), required=False)
        v.texts(f"{w}.paragraphs", p.get("paragraphs"), 1)
        words = sum(len(x.split()) for x in p.get("paragraphs", []) if isinstance(x, str))
        if words < 100:
            v.warn(w, f"nur {words} Wörter – Beitrag vollständig?")
    ex = t.get("example") or {}
    if str(ex.get("no")) != "0":
        v.err("lesen.t1.example", "Beispiel 0 fehlt")
    v.text("lesen.t1.example.text", ex.get("text"))
    if ex.get("answer") not in ABCD:
        v.err("lesen.t1.example.answer", f"ungültig: {ex.get('answer')!r}")
    items = v.numbered("lesen.t1.items", t.get("items", []), range(1, 10))
    for it in items:
        v.text(f"lesen.t1.{it.get('no')}.text", it.get("text"))
        if it.get("answer") not in ABCD:
            v.err(f"lesen.t1.{it.get('no')}.answer", f"ungültig: {it.get('answer')!r}")
    summary["L1"] = " ".join(str(it.get("answer")) for it in items) + f"  (Bsp. {ex.get('answer')})"

    # ---- Lesen t2: Lückentext, Sätze a-h, Lücken 10-15
    t = L.get("t2", {})
    v.text("lesen.t2.instruction", t.get("instruction"))
    v.text("lesen.t2.title", t.get("title"))
    v.text("lesen.t2.lead", t.get("lead"), required=False)
    v.texts("lesen.t2.paragraphs", t.get("paragraphs"), 4)
    v.text("lesen.t2.source", t.get("source"))
    marks = [m for p in t.get("paragraphs", []) if isinstance(p, str) for m in GAP.findall(p)]
    if sorted(marks, key=int) != ["0", "10", "11", "12", "13", "14", "15"]:
        v.err("lesen.t2.paragraphs", f"Lücken {marks} – erwartet [0] und [10]–[15] je einmal")
    ex = t.get("example") or {}
    v.text("lesen.t2.example.text", ex.get("text"), check=False)
    sents = v.letters("lesen.t2.sentences", t.get("sentences"), A_H)
    items = v.numbered("lesen.t2.items", t.get("items", []), range(10, 16))
    ans = []
    for it in items:
        a = it.get("answer")
        if a not in A_H:
            v.err(f"lesen.t2.{it.get('no')}.answer", f"ungültig: {a!r}")
        ans.append(a)
    if len(set(ans)) != len(ans):
        v.err("lesen.t2.items", f"Satz doppelt vergeben: {ans}")
    un = t.get("unused") or []
    if len(un) != 2:
        v.err("lesen.t2.unused", f"genau 2 Sätze bleiben übrig: {un}")
    v.partition("lesen.t2", ans, None, un)
    words = sum(len(p.split()) for p in t.get("paragraphs", []) if isinstance(p, str))
    if words < 200:
        v.warn("lesen.t2.paragraphs", f"nur {words} Wörter – Text vollständig?")
    summary["L2"] = " ".join(str(a) for a in ans) + f"  (nicht gebraucht {','.join(un)})"
    del sents

    # ---- Lesen t3: Artikel, a/b/c, 16-21
    t = L.get("t3", {})
    v.text("lesen.t3.instruction", t.get("instruction"))
    v.text("lesen.t3.tasksIntro", t.get("tasksIntro"), required=False)
    v.text("lesen.t3.title", t.get("title"))
    v.text("lesen.t3.lead", t.get("lead"), required=False)
    v.texts("lesen.t3.paragraphs", t.get("paragraphs"), 4)
    v.text("lesen.t3.source", t.get("source"))
    words = sum(len(p.split()) for p in t.get("paragraphs", []) if isinstance(p, str))
    if words < 300:
        v.warn("lesen.t3.paragraphs", f"nur {words} Wörter – Text vollständig?")
    v.abc("lesen.t3.example", t.get("example") or {})
    items = v.numbered("lesen.t3.items", t.get("items", []), range(16, 22))
    for it in items:
        v.abc(f"lesen.t3.{it.get('no')}", it)
    summary["L3"] = " ".join(str(it.get("answer")) for it in items)

    # ---- Lesen t4: Äußerungen a-h, Überschriften 22-27
    t = L.get("t4", {})
    v.text("lesen.t4.instruction", t.get("instruction"))
    v.text("lesen.t4.title", t.get("title"))
    ex = t.get("example") or {}
    v.text("lesen.t4.example.text", ex.get("text"), check=False)
    if ex.get("answer") not in A_H:
        v.err("lesen.t4.example.answer", f"ungültig: {ex.get('answer')!r}")
    items = v.numbered("lesen.t4.items", t.get("items", []), range(22, 28))
    ans = []
    for it in items:
        v.text(f"lesen.t4.{it.get('no')}.text", it.get("text"), check=False)
        a = it.get("answer")
        if a not in A_H:
            v.err(f"lesen.t4.{it.get('no')}.answer", f"ungültig: {a!r}")
        ans.append(a)
    if len(set(ans)) != len(ans):
        v.err("lesen.t4.items", f"Äußerung doppelt vergeben: {ans}")
    texts = t.get("texts", [])
    if [x.get("letter") for x in texts] != list("abcdefgh"):
        v.err("lesen.t4.texts", f"Buchstaben {[x.get('letter') for x in texts]} – erwartet a–h")
    for x in texts:
        w = f"lesen.t4.texts.{x.get('letter')}"
        v.text(f"{w}.text", x.get("text"))
        v.text(f"{w}.byline", x.get("byline"), required=False)
        if len(str(x.get("text", "")).split()) < 25:
            v.warn(w, "sehr kurz – Äußerung vollständig?")
    un = t.get("unused") or []
    if len(un) != 1:
        v.err("lesen.t4.unused", f"genau 1 Äußerung bleibt übrig: {un}")
    v.partition("lesen.t4", ans, ex.get("answer"), un)
    summary["L4"] = " ".join(str(a) for a in ans) + f"  (Bsp. {ex.get('answer')}, nicht gebraucht {','.join(un)})"

    # ---- Lesen t5: Paragrafen, Überschriften a-h, 28-30
    t = L.get("t5", {})
    v.text("lesen.t5.instruction", t.get("instruction"))
    v.text("lesen.t5.title", t.get("title"))
    v.text("lesen.t5.subtitle", t.get("subtitle"), required=False)
    v.letters("lesen.t5.headings", t.get("headings"), A_H)
    ex = t.get("example") or {}
    v.text("lesen.t5.example.label", ex.get("label"))
    v.texts("lesen.t5.example.paragraphs", ex.get("paragraphs"), 1)
    if ex.get("answer") not in A_H:
        v.err("lesen.t5.example.answer", f"ungültig: {ex.get('answer')!r}")
    items = v.numbered("lesen.t5.items", t.get("items", []), range(28, 31))
    ans = []
    for it in items:
        v.text(f"lesen.t5.{it.get('no')}.label", it.get("label"))
        v.texts(f"lesen.t5.{it.get('no')}.paragraphs", it.get("paragraphs"), 1)
        a = it.get("answer")
        if a not in A_H:
            v.err(f"lesen.t5.{it.get('no')}.answer", f"ungültig: {a!r}")
        ans.append(a)
    un = t.get("unused") or []
    if len(un) != 4:
        v.err("lesen.t5.unused", f"genau 4 Überschriften bleiben übrig: {un}")
    v.partition("lesen.t5", ans, ex.get("answer"), un)
    summary["L5"] = " ".join(str(a) for a in ans) + f"  (Bsp. {ex.get('answer')}, nicht gebraucht {','.join(un)})"

    # ---- Hören t1
    t = H.get("t1", {})
    v.text("hoeren.t1.instruction", t.get("instruction"))
    exs = t.get("example") or []
    if [str(e.get("no")) for e in exs] != ["01", "02"]:
        v.warn("hoeren.t1.example", f"Beispielnummern {[e.get('no') for e in exs]} (erwartet 01, 02)")
    for e in exs:
        if e.get("type") == "rf":
            v.rf(f"hoeren.t1.example.{e.get('no')}", e)
        else:
            v.abc(f"hoeren.t1.example.{e.get('no')}", e)
    tx = t.get("texts", [])
    if len(tx) != 5:
        v.err("hoeren.t1.texts", f"braucht 5 Texte, hat {len(tx)}")
    flat = []
    for i, x in enumerate(tx):
        v.text(f"hoeren.t1.texts[{i}].label", x.get("label"))
        flat += x.get("items", [])
    v.numbered("hoeren.t1.items", flat, range(1, 11))
    for it in flat:
        n = int(it.get("no", 0) or 0)
        want = "rf" if n % 2 == 1 else "abc"
        if it.get("type") != want:
            v.err(f"hoeren.t1.{n}.type", f"{it.get('type')!r} erwartet {want}")
        if want == "rf":
            v.rf(f"hoeren.t1.{n}", it)
        else:
            v.abc(f"hoeren.t1.{n}", it)
    summary["H1"] = " ".join(str(it.get("answer")) for it in flat) + "  (Bsp. " + ", ".join(str(e.get("answer")) for e in exs) + ")"

    # ---- Hören t2
    t = H.get("t2", {})
    for k in ("instruction", "context"):
        v.text(f"hoeren.t2.{k}", t.get(k))
    items = v.numbered("hoeren.t2.items", t.get("items", []), range(11, 17))
    for it in items:
        v.abc(f"hoeren.t2.{it.get('no')}", it)
    summary["H2"] = " ".join(str(it.get("answer")) for it in items)

    # ---- Hören t3
    t = H.get("t3", {})
    v.text("hoeren.t3.instruction", t.get("instruction"))
    sp = t.get("speakers") or {}
    if set(sp) != ABC:
        v.err("hoeren.t3.speakers", f"braucht a, b, c: {sp!r}")
    for k in sorted(sp):
        v.text(f"hoeren.t3.speakers.{k}", sp[k])
    ex = t.get("example") or {}
    v.text("hoeren.t3.example.text", ex.get("text"))
    if ex.get("answer") not in ABC:
        v.err("hoeren.t3.example.answer", f"ungültig: {ex.get('answer')!r}")
    items = v.numbered("hoeren.t3.items", t.get("items", []), range(17, 23))
    for it in items:
        v.text(f"hoeren.t3.{it.get('no')}.text", it.get("text"))
        if it.get("answer") not in ABC:
            v.err(f"hoeren.t3.{it.get('no')}.answer", f"ungültig: {it.get('answer')!r}")
    summary["H3"] = " ".join(str(it.get("answer")) for it in items) + f"  (Bsp. {ex.get('answer')})"

    # ---- Hören t4
    t = H.get("t4", {})
    v.text("hoeren.t4.instruction", t.get("instruction"))
    items = v.numbered("hoeren.t4.items", t.get("items", []), range(23, 31))
    for it in items:
        v.abc(f"hoeren.t4.{it.get('no')}", it)
    summary["H4"] = " ".join(str(it.get("answer")) for it in items)

    # ---- Schreiben
    v.text("schreiben.intro", S.get("intro"))
    tasks = S.get("tasks", [])
    if [tk.get("no") for tk in tasks] != [1, 2]:
        v.err("schreiben.tasks", f"Nummern {[tk.get('no') for tk in tasks]} erwartet [1, 2]")
    for tk, (mins, words) in zip(tasks, ((50, 150), (25, 100))):
        w = f"schreiben.{tk.get('no')}"
        if tk.get("minutes") != mins:
            v.warn(f"{w}.minutes", f"{tk.get('minutes')} (üblich {mins})")
        if tk.get("words") != words:
            v.warn(f"{w}.words", f"{tk.get('words')} (üblich {words})")
        v.texts(f"{w}.situation", tk.get("situation"), 1)
        pts = tk.get("points") or []
        if len(pts) != 4:
            v.err(f"{w}.points", f"braucht 4 Inhaltspunkte, hat {len(pts)}")
        for i, p in enumerate(pts):
            v.text(f"{w}.points[{i}]", p)
            if p.lstrip().startswith(("–", "-", "•", "■")):
                v.warn(f"{w}.points[{i}]", "Aufzählungszeichen entfernen")
        v.text(f"{w}.instruction", tk.get("instruction"))
        if f"mindestens {tk.get('words')} Wörter" not in (tk.get("instruction") or ""):
            v.warn(f"{w}.instruction", "Wortzahl stimmt nicht mit words überein")
        m = tk.get("model") or {}
        v.text(f"{w}.model.label", m.get("label"), required=True)
        v.text(f"{w}.model.text", m.get("text"), check=False)
        mt = m.get("text") or ""
        if re.search(r"(^|\n)\s*[1-4]\s", mt):
            v.warn(f"{w}.model.text", "Randziffer 1–4 mit abgeschrieben?")
        mw = len(re.findall(r"[A-Za-zÄÖÜäöüß0-9]+(?:[’'-][A-Za-zÄÖÜäöüß0-9]+)*", mt))
        if mt and mw < words * 0.7:
            v.warn(f"{w}.model.text", f"nur {mw} Wörter – Musterlösung vollständig?")
        v.text(f"{w}.typicalErrors", tk.get("typicalErrors"), required=True)

    # ---- Index-Angaben
    ix = d.get("index") or {}
    for k in ("t1", "t2", "t3", "t4"):
        v.text(f"index.hoeren.{k}", (ix.get("hoeren") or {}).get(k))
    if len(ix.get("schreiben") or []) != 2:
        v.err("index.schreiben", "braucht 2 Einträge")
    sprechen = ix.get("sprechen") or {}
    if len(sprechen.get("vortrag") or []) != 4:
        v.err("index.sprechen.vortrag", "braucht 4 Themen (A1, A2, B1, B2)")
    v.text("index.sprechen.diskussion", sprechen.get("diskussion"))

    report(v, d, summary)
    return not v.errors


def report(v, d, summary=None):
    print(f"== {v.path}  (Modelltest {d.get('roman', '?')})")
    for e in v.errors:
        print("  ERROR  ", e)
    for w in v.warnings:
        print("  warn   ", w)
    if summary:
        print("  Antworten:")
        for k, s in summary.items():
            print(f"    {k}: {s}")
    print("  OK" if not v.errors else f"  {len(v.errors)} Fehler, {len(v.warnings)} Warnungen")


if __name__ == "__main__":
    ok = all([validate(p) for p in sys.argv[1:]])
    sys.exit(0 if ok else 1)
