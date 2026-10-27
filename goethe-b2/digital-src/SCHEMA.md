# Modelltest JSON schema (Goethe-Zertifikat B2, digital exam data)

One file per Modelltest: `digital-src/data/mtN.json`, UTF-8, valid JSON.
Run `python3 digital-src/validate.py digital-src/data/mtN.json` until it prints `OK` with no errors.

## Transcription rules

- Copy the German text verbatim from the PDF: words, punctuation, „…“ quotes, – dashes, … ellipsis, ß, ä/ö/ü, numbers, units, subscripts (CO₂).
- Join the lines of one paragraph with single spaces. Remove only word-break hyphenation at line ends. Keep real hyphens (`Schlaf- und Liegewagen`, `E-Mail`).
- A new paragraph in the PDF = a new string in `paragraphs`.
- Leave out page furniture: page numbers, the header line `Kandidatenblätter · 65 Minuten Lesen`, the rotated side label, `vorgeschlagene Arbeitszeit` lines, answer boxes.
- Two-column pages (Lesen Teil 2, Teil 4): read the whole left column first, then the right column. A paragraph can continue from the bottom of the left column to the top of the right column.
- Item numbers are strings: `"0"` (example), `"1"` … `"30"`; Hören example numbers `"01"`, `"02"`.
- Answers: Richtig/Falsch → `"R"`/`"F"`; multiple choice → `"a"`/`"b"`/`"c"`; matching → letter `"a"`…`"h"`; Lesen Teil 1 → person letter `"a"`…`"d"`; Hören Teil 3 → speaker column `"a"`/`"b"`/`"c"`.
- Every item answer comes from the Lösungsschlüssel page (17). Example answers come from the marked box on the task page.

## Top level

```json
{
  "id": 1, "roman": "I",
  "lesen": { "t1": {}, "t2": {}, "t3": {}, "t4": {}, "t5": {} },
  "hoeren": { "t1": {}, "t2": {}, "t3": {}, "t4": {} },
  "schreiben": { "intro": "…", "tasks": [ {}, {} ] },
  "index": { "hoeren": {}, "schreiben": [], "sprechen": {} },
  "notes": "free text, not shown to students"
}
```

`build-digital.py` removes `index` and `notes` from `digital.html`; `build-index.py` reads `index`.

## Lesen (65 min, 30 items)

### t1 – Forum, items 1–9 (Wer sagt was? a–d)
```json
"t1": {
  "instruction": "…",
  "forum": { "title": "Auszeit vom Smartphone",
             "posts": [ { "letter": "a", "name": "Merve", "time": "14.03. · 21:47 Uhr", "paragraphs": ["…"] } ] },
  "example": { "no": "0", "text": "Wer hat …?", "answer": "a" },
  "items": [ { "no": "1", "text": "Wer …?", "answer": "b" } ]
}
```
Four posts (a–d). The answer is the letter of the person.

### t2 – Lückentext, items 10–15
```json
"t2": {
  "instruction": "…", "title": "…", "lead": "…",
  "paragraphs": ["… [0] …", "… [10] …"],
  "source": "aus einer deutschen Zeitschrift",
  "example": { "no": "0", "text": "Satz, der in Lücke [0] steht." },
  "sentences": { "a": "…", "b": "…", "c": "…", "d": "…", "e": "…", "f": "…", "g": "…", "h": "…" },
  "unused": ["b", "f"],
  "items": [ { "no": "10", "answer": "c" } ]
}
```
Gap markers are written `[0]`, `[10]` … `[15]` inside the paragraphs. `sentences` has eight entries; two of them are not used (`unused`).

### t3 – Zeitungsartikel, items 16–21 (a/b/c)
`instruction`, `tasksIntro`, `title`, `lead`, `paragraphs`, `source`, `example { no, stem, options{a,b,c}, answer }`, `items [ { no, stem, options, answer } ]`.

### t4 – Überschriften und Äußerungen, items 22–27
```json
"t4": {
  "instruction": "…", "title": "Bargeld – ein Auslaufmodell?",
  "example": { "no": "0", "text": "Überschrift", "answer": "a" },
  "items": [ { "no": "22", "text": "Überschrift", "answer": "e" } ],
  "texts": [ { "letter": "a", "text": "Äußerung", "byline": "Bettina, Kassel" } ],
  "unused": ["g"]
}
```
Eight Äußerungen (a–h); the example uses one, six are matched, one stays unused.

### t5 – Paragrafen und Überschriften, items 28–30
```json
"t5": {
  "instruction": "…", "title": "Teilnahmebedingungen", "subtitle": "…",
  "headings": { "a": "…", "b": "…", "c": "…", "d": "…", "e": "…", "f": "…", "g": "…", "h": "…" },
  "unused": ["a", "c", "f", "g"],
  "example": { "no": "0", "label": "§ 0", "paragraphs": ["…"], "answer": "b" },
  "items": [ { "no": "28", "label": "§ 28", "paragraphs": ["(1) …", "(2) …"], "answer": "e" } ]
}
```

## Hören (ca. 40 min, 30 items)

- `t1` – five short texts, items 1–10 (odd = Richtig/Falsch, even = a/b/c), each text once. `example` is a list of two items (`01` type `rf`, `02` type `abc`); `texts` is a list of five `{ label, items }`, each item `{ no, type: "rf"|"abc", text | stem+options, answer }`.
- `t2` – interview, items 11–16 (a/b/c), twice. `instruction`, `context`, `items [ { no, stem, options, answer } ]`.
- `t3` – radio discussion, items 17–22, once. `speakers { a, b, c }`, `example { no: "0", text, answer }`, `items [ { no, text, answer } ]`. The answer is the speaker.
- `t4` – lecture, items 23–30 (a/b/c), twice. `instruction`, `items [ { no, stem, options, answer } ]`.

## Schreiben (75 min)

```json
"schreiben": {
  "intro": "…",
  "tasks": [
    { "no": 1, "minutes": 50, "words": 150, "situation": ["…"], "points": ["…", "…", "…", "…"], "instruction": "…",
      "model": { "label": "Forumsbeitrag, ca. 200 Wörter", "text": "…" }, "typicalErrors": "…" },
    { "no": 2, "minutes": 25, "words": 100, "…": "…" }
  ]
}
```
`words` is the minimum word count. Aufgabe 1 counts 60, Aufgabe 2 counts 40 of 100 points. `model` and `typicalErrors` come from page 18 and are shown only after submission.

## index (for index.html)

```json
"index": {
  "hoeren": { "t1": "Fünf kurze Texte", "t2": "Interview: …", "t3": "Radiogespräch: …", "t4": "Vortrag: …" },
  "schreiben": ["Forumsbeitrag: …", "Nachricht an …"],
  "sprechen": { "vortrag": ["A Thema 1", "A Thema 2", "B Thema 1", "B Thema 2"], "diskussion": "Frage der Diskussion" }
}
```
