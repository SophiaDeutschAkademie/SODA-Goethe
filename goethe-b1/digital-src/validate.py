#!/usr/bin/env python3
"""Validate a Modelltest JSON file against SCHEMA.md.

Usage: python3 digital-src/validate.py digital-src/data/mt4.json [more files...]
Prints errors (must fix) and warnings (check), then a compact answer summary
to compare against the Lösungsschlüssel.
"""
import json
import re
import sys

RF = {"R", "F"}
JN = {"J", "N"}
ABC = {"a", "b", "c"}
ADS = set("abcdefghij")

SUSPICIOUS = [
    (re.compile(r"[|\[\]{}]"), "OCR-Artefakt (| [ ] { })"),
    (re.compile(r"neseL|neröH|nebierhcS|nehcerpS|Kandidatenblätter|Arbeitszeit"), "Seitenrand/Kopfzeile im Text"),
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
            for rx, label in SUSPICIOUS:
                m = rx.search(s)
                if m:
                    a = max(0, m.start() - 25)
                    self.warn(where, f"{label}: …{s[a:m.end() + 25]}…")

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

    def rf(self, where, it, answers=RF):
        self.text(f"{where}.text", it.get("text"))
        if it.get("answer") not in answers:
            self.err(f"{where}.answer", f"ungültig: {it.get('answer')!r} (erlaubt {sorted(answers)})")

    def abc(self, where, it, allow_null=False):
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
        if ans not in ABC and not (allow_null and ans is None):
            self.err(f"{where}.answer", f"ungültig: {ans!r}")


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

    # ---- Lesen t1
    t = L.get("t1", {})
    v.text("lesen.t1.instruction", t.get("instruction"))
    b = t.get("blog", {})
    v.text("lesen.t1.blog.title", b.get("title"))
    v.text("lesen.t1.blog.site", b.get("site"), required=False)
    v.text("lesen.t1.blog.date", b.get("date"), required=False)
    v.text("lesen.t1.blog.closing", b.get("closing"), required=False)
    v.texts("lesen.t1.blog.paragraphs", b.get("paragraphs"), 2)
    ex = t.get("example") or {}
    if str(ex.get("no")) != "0":
        v.err("lesen.t1.example", "Beispiel 0 fehlt")
    v.rf("lesen.t1.example", ex)
    items = v.numbered("lesen.t1.items", t.get("items", []), range(1, 7))
    for it in items:
        v.rf(f"lesen.t1.{it.get('no')}", it)
    summary["L1"] = " ".join(str(it.get("answer")) for it in items)

    # ---- Lesen t2
    t = L.get("t2", {})
    texts = t.get("texts", [])
    if len(texts) != 2:
        v.err("lesen.t2.texts", f"braucht 2 Texte, hat {len(texts)}")
    ans2 = []
    for ti, (tx, nums) in enumerate(zip(texts, (range(7, 10), range(10, 13)))):
        w = f"lesen.t2.texts[{ti}]"
        v.text(f"{w}.instruction", tx.get("instruction"))
        v.text(f"{w}.title", tx.get("title"))
        v.text(f"{w}.lead", tx.get("lead"), required=False)
        v.texts(f"{w}.paragraphs", tx.get("paragraphs"), 1)
        v.text(f"{w}.source", tx.get("source"))
        v.text(f"{w}.footnote", tx.get("footnote"), required=False)
        if tx.get("example"):
            v.abc(f"{w}.example", tx["example"])
        elif ti == 0:
            v.warn(f"{w}.example", "kein Beispiel beim ersten Text?")
        items = v.numbered(f"{w}.items", tx.get("items", []), nums)
        for it in items:
            v.abc(f"{w}.{it.get('no')}", it)
            ans2.append(str(it.get("answer")))
        words = sum(len(p.split()) for p in tx.get("paragraphs", []) if isinstance(p, str))
        if words < 120:
            v.warn(f"{w}.paragraphs", f"nur {words} Wörter – Text vollständig?")
    summary["L2"] = " ".join(ans2)

    # ---- Lesen t3
    t = L.get("t3", {})
    v.text("lesen.t3.instruction", t.get("instruction"))
    v.text("lesen.t3.context", t.get("context"))
    ex = t.get("example") or {}
    v.text("lesen.t3.example.text", ex.get("text"))
    if ex.get("answer") not in ADS:
        v.err("lesen.t3.example.answer", f"ungültig: {ex.get('answer')!r}")
    items = v.numbered("lesen.t3.items", t.get("items", []), range(13, 20))
    used = []
    for it in items:
        v.text(f"lesen.t3.{it.get('no')}.text", it.get("text"))
        a = it.get("answer")
        if a not in ADS | {"0"}:
            v.err(f"lesen.t3.{it.get('no')}.answer", f"ungültig: {a!r}")
        used.append(a)
    letters = [a for a in used if a != "0"]
    if len(set(letters)) != len(letters):
        v.err("lesen.t3.items", f"Anzeige doppelt vergeben: {used}")
    if ex.get("answer") in letters:
        v.err("lesen.t3.items", "Beispiel-Anzeige wurde noch einmal vergeben")
    if used.count("0") != 1:
        v.warn("lesen.t3.items", f"erwartet genau eine 0, gefunden {used.count('0')}")
    ads = t.get("ads", [])
    if [a.get("letter") for a in ads] != list("abcdefghij"):
        v.err("lesen.t3.ads", f"Buchstaben {[a.get('letter') for a in ads]} – erwartet a–j")
    for a in ads:
        w = f"lesen.t3.ads.{a.get('letter')}"
        content = [a.get(k) for k in ("header", "tag", "title", "subtitle", "footer")]
        content += list(a.get("facts") or []) + list(a.get("body") or [])
        content = [c for c in content if isinstance(c, str) and c.strip()]
        if len(" ".join(content).split()) < 15:
            v.warn(w, "sehr wenig Text – Anzeige vollständig?")
        for k in ("header", "tag", "title", "subtitle", "footer"):
            v.text(f"{w}.{k}", a.get(k), required=False)
        for i, s in enumerate(a.get("facts") or []):
            v.text(f"{w}.facts[{i}]", s)
        for i, s in enumerate(a.get("body") or []):
            v.text(f"{w}.body[{i}]", s)
    DESIGNS = {"inst", "serif", "dashed", "barhead", "rules", "inverse", "classified", "mono", "tearoff", "chalk", "corp", "hotel",
               "band", "stamp", "logo", "browser", "stripes", "ticket", "postcard", "badge", "timetable", "bignum", "route", "pinned",
               "rounded", "dropcap", "coupon", "greyband", "club", "speech", "notebook", "sign"}
    ICONS = {"bus", "columns", "paw", "key", "wrench", "note", "plug"}
    dz = [a.get("design") for a in ads if a.get("design")]
    for a in ads:
        dsg = a.get("design")
        if dsg and dsg not in DESIGNS:
            v.err(f"lesen.t3.ads.{a.get('letter')}.design", f"unbekanntes Layout {dsg!r}")
        ic = (a.get("deco") or {}).get("icon")
        if ic and ic not in ICONS:
            v.err(f"lesen.t3.ads.{a.get('letter')}.deco.icon", f"unbekanntes Symbol {ic!r}")
    if len(dz) != len(set(dz)):
        v.warn("lesen.t3.ads", f"Layout mehrfach verwendet: {dz}")
    summary["L3"] = " ".join(str(a) for a in used) + f"  (Bsp. {ex.get('answer')})"

    # ---- Lesen t4
    t = L.get("t4", {})
    v.text("lesen.t4.instruction", t.get("instruction"))
    v.text("lesen.t4.context", t.get("context"))
    v.text("lesen.t4.header", t.get("header"), required=False)
    v.text("lesen.t4.site", t.get("site"), required=False)
    ex = t.get("example") or {}
    v.text("lesen.t4.example.name", ex.get("name"))
    v.text("lesen.t4.example.byline", ex.get("byline"), required=False)
    v.rf("lesen.t4.example", ex, JN)
    items = v.numbered("lesen.t4.items", t.get("items", []), range(20, 27))
    for it in items:
        w = f"lesen.t4.{it.get('no')}"
        v.text(f"{w}.name", it.get("name"))
        v.text(f"{w}.byline", it.get("byline"), required=False)
        v.rf(w, it, JN)
        if it.get("byline") and it.get("name") and not it["byline"].startswith(it["name"]):
            v.warn(w, f"byline passt nicht zum Namen: {it['name']} / {it['byline']}")
        words = len((it.get("text") or "").split())
        if words < 35:
            v.warn(w, f"nur {words} Wörter – Kommentar vollständig?")
    summary["L4"] = " ".join(str(it.get("answer")) for it in items)

    # ---- Lesen t5
    t = L.get("t5", {})
    v.text("lesen.t5.instruction", t.get("instruction"))
    v.text("lesen.t5.context", t.get("context"))
    doc = t.get("doc", {})
    v.text("lesen.t5.doc.title", doc.get("title"))
    v.text("lesen.t5.doc.intro", doc.get("intro"), required=False)
    v.text("lesen.t5.doc.footer", doc.get("footer"), required=False)
    secs = doc.get("sections", [])
    if not secs:
        v.err("lesen.t5.doc.sections", "leer")
    for i, s in enumerate(secs):
        v.text(f"lesen.t5.doc.sections[{i}].heading", s.get("heading"), required=False)
        if (s.get("heading") or "").endswith(":"):
            v.warn(f"lesen.t5.doc.sections[{i}].heading", "Doppelpunkt am Ende entfernen")
        v.text(f"lesen.t5.doc.sections[{i}].text", s.get("text"))
    if t.get("example"):
        v.abc("lesen.t5.example", t["example"])
    items = v.numbered("lesen.t5.items", t.get("items", []), range(27, 31))
    for it in items:
        v.abc(f"lesen.t5.{it.get('no')}", it)
    summary["L5"] = " ".join(str(it.get("answer")) for it in items)

    # ---- Hören t1
    t = H.get("t1", {})
    v.text("hoeren.t1.instruction", t.get("instruction"))
    v.text("hoeren.t1.readNote", t.get("readNote"), required=False)
    exs = t.get("example") or []
    if [str(e.get("no")) for e in exs] != ["01", "02"]:
        v.warn("hoeren.t1.example", f"Beispielnummern {[e.get('no') for e in exs]} (erwartet 01, 02)")
    for e in exs:
        if e.get("type") == "rf":
            v.text(f"hoeren.t1.example.{e.get('no')}.text", e.get("text"))
            if e.get("answer") not in RF | {None}:
                v.err(f"hoeren.t1.example.{e.get('no')}.answer", f"ungültig: {e.get('answer')!r}")
        else:
            v.abc(f"hoeren.t1.example.{e.get('no')}", e, allow_null=True)
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
    summary["H1"] = " ".join(str(it.get("answer")) for it in flat)

    # ---- Hören t2
    t = H.get("t2", {})
    for k in ("instruction", "readNote", "context"):
        v.text(f"hoeren.t2.{k}", t.get(k))
    items = v.numbered("hoeren.t2.items", t.get("items", []), range(11, 16))
    for it in items:
        v.abc(f"hoeren.t2.{it.get('no')}", it)
    summary["H2"] = " ".join(str(it.get("answer")) for it in items)

    # ---- Hören t3
    t = H.get("t3", {})
    for k in ("instruction", "readNote", "context"):
        v.text(f"hoeren.t3.{k}", t.get(k))
    items = v.numbered("hoeren.t3.items", t.get("items", []), range(16, 23))
    for it in items:
        v.rf(f"hoeren.t3.{it.get('no')}", it)
    summary["H3"] = " ".join(str(it.get("answer")) for it in items)

    # ---- Hören t4
    t = H.get("t4", {})
    for k in ("instruction", "readNote", "context"):
        v.text(f"hoeren.t4.{k}", t.get(k))
    sp = t.get("speakers") or {}
    if set(sp) != ABC:
        v.err("hoeren.t4.speakers", f"braucht a, b, c: {sp!r}")
    for k in sorted(sp):
        v.text(f"hoeren.t4.speakers.{k}", sp[k])
    ex = t.get("example") or {}
    v.text("hoeren.t4.example.text", ex.get("text"))
    if ex.get("answer") not in ABC:
        v.err("hoeren.t4.example.answer", f"ungültig: {ex.get('answer')!r}")
    items = v.numbered("hoeren.t4.items", t.get("items", []), range(23, 31))
    for it in items:
        v.text(f"hoeren.t4.{it.get('no')}.text", it.get("text"))
        if it.get("answer") not in ABC:
            v.err(f"hoeren.t4.{it.get('no')}.answer", f"ungültig: {it.get('answer')!r}")
    summary["H4"] = " ".join(str(it.get("answer")) for it in items)

    # ---- Schreiben
    v.text("schreiben.intro", S.get("intro"))
    tasks = S.get("tasks", [])
    if [tk.get("no") for tk in tasks] != [1, 2, 3]:
        v.err("schreiben.tasks", f"Nummern {[tk.get('no') for tk in tasks]} erwartet [1, 2, 3]")
    for tk, (mins, words) in zip(tasks, ((20, 80), (25, 80), (15, 40))):
        w = f"schreiben.{tk.get('no')}"
        if tk.get("minutes") != mins:
            v.warn(f"{w}.minutes", f"{tk.get('minutes')} (üblich {mins})")
        if tk.get("words") != words:
            v.warn(f"{w}.words", f"{tk.get('words')} (üblich {words})")
        v.texts(f"{w}.situation", tk.get("situation"), 1)
        for i, p in enumerate(tk.get("points") or []):
            v.text(f"{w}.points[{i}]", p)
            if p.lstrip().startswith(("–", "-", "•")):
                v.warn(f"{w}.points[{i}]", "Aufzählungszeichen entfernen")
        if tk.get("no") == 1 and len(tk.get("points") or []) != 3:
            v.err(f"{w}.points", "Aufgabe 1 braucht 3 Leitpunkte")
        if tk.get("post"):
            for k in ("site", "label", "author", "text"):
                v.text(f"{w}.post.{k}", tk["post"].get(k), required=(k != "label"))
        elif tk.get("no") == 2:
            v.warn(f"{w}.post", "Aufgabe 2 ohne Gästebuch-Beitrag?")
        v.text(f"{w}.instruction", tk.get("instruction"))
        m = tk.get("model") or {}
        v.text(f"{w}.model.label", m.get("label"), required=False)
        v.text(f"{w}.model.text", m.get("text"), check=False)
        mt = m.get("text") or ""
        if re.search(r"(^|\n)\s*[123]\s", mt):
            v.warn(f"{w}.model.text", "Randziffer 1/2/3 mit abgeschrieben?")
        mw = len(re.findall(r"[A-Za-zÄÖÜäöüß0-9]+(?:[’'-][A-Za-zÄÖÜäöüß0-9]+)*", mt))
        if mt and mw < words * 0.8:
            v.warn(f"{w}.model.text", f"nur {mw} Wörter – Musterlösung vollständig?")
        v.text(f"{w}.typicalErrors", tk.get("typicalErrors"), required=False)

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
