# Modelltest JSON schema (Goethe-Zertifikat A2, digital exam data)

One file per Modelltest: `digital-src/data/mtN.json`, UTF-8, valid JSON.
Run `python3 digital-src/validate.py digital-src/data/mtN.json` until it prints `OK` with no errors. If `Goethe A2 Modelltest N.pdf` and `pdftotext` are available, the validator also compares all 40 answers with the Lösungsschlüssel on page 17.

## Transcription rules

- Copy the German text verbatim from the PDF: words, punctuation, „…“ quotes, – dashes, … ellipsis, ß, ä/ö/ü, numbers, units.
- Join the lines of one paragraph with single spaces. Remove only word-break hyphenation at line ends. Keep real hyphens (`E-Mail`, `Kinder- und Jugendärztin`).
- A new paragraph in the PDF = a new string in `paragraphs`.
- Leave out page furniture: page numbers, the header line `Kandidatenblätter · 30 Minuten Lesen`, `vorgeschlagene Arbeitszeit` lines, answer boxes.
- Item numbers are strings: `"0"` (example), `"1"` … `"20"`.
- Answers: multiple choice → `"a"`/`"b"`/`"c"`; Lesen Teil 4 → ad letter `"a"`…`"f"` or `"X"` (no ad fits); Hören Teil 2 → picture letter `"a"`…`"i"`; Hören Teil 3 → picture letter `"a"`/`"b"`/`"c"`; Hören Teil 4 → `"Ja"` / `"Nein"`.
- Every item answer comes from the Lösungsschlüssel page (17). Example answers come from the marked box on the task page.
- Italics inside `typicalErrors` and `model` texts: `*like this*`. The exam screen turns them into `<em>`.

## Top level

```json
{
  "id": 1, "roman": "I",
  "lesen": { "t1": {}, "t2": {}, "t3": {}, "t4": {} },
  "hoeren": { "t1": {}, "t2": {}, "t3": {}, "t4": {} },
  "schreiben": { "intro": "…", "tasks": [ {}, {} ], "good": [ {} ] },
  "index": { "hoeren": {}, "schreiben": [], "sprechen": {} },
  "notes": "free text, not shown to students"
}
```

`build-digital.py` removes `index` and `notes` from `digital.html`; `build-index.py` reads `index`.

## Lesen (30 min, 20 items, 1,25 points each)

### t1 – Zeitungsartikel, items 1–5 (a/b/c)
```json
"t1": {
  "instruction": "…", "title": "…", "lead": "…", "paragraphs": ["…"], "quote": "„…“",
  "source": "aus einer deutschen Tageszeitung", "tasksIntro": "…",
  "image": "img/mt1-lesen-foto.jpg", "imageAlt": "…",
  "example": { "no": "0", "stem": "Marion Kessler …", "options": { "a": "…", "b": "…", "c": "…" }, "answer": "a" },
  "items": [ { "no": "1", "stem": "…", "options": { "a": "…", "b": "…", "c": "…" }, "answer": "b" } ]
}
```
`quote` and the photo are optional; `imageAlt` describes the photo for screen readers.

### t2 – Informationstafel, items 6–10 (a/b/c)
```json
"t2": {
  "instruction": "…",
  "board": { "title": "Gesundheitszentrum am Lindenplatz", "label": "WEGWEISER", "rows": [ { "floor": "4. Stock", "text": "…" } ] },
  "example": { "no": "0", "stem": "Situation …", "options": { "a": "4. Stock", "b": "3. Stock", "c": "anderer Stock" }, "answer": "a" },
  "items": [ { "no": "6", "stem": "Situation …", "options": { "a": "…", "b": "…", "c": "…" }, "answer": "b" } ]
}
```
`rows` follow the board from top to bottom (floor label, then the listing as one string with ` · ` separators).

### t3 – E-Mail, items 11–15 (a/b/c)
`instruction`, `mail { from, to, subject, greeting, paragraphs, closing[] }`, `tasksIntro`, `example { no, stem, options, answer }`, `items [ { no, stem, options, answer } ]`.

### t4 – Anzeigen, items 16–20 (a–f or X)
```json
"t4": {
  "instruction": "…",
  "example": { "no": "0", "text": "Tim möchte …", "answer": "a" },
  "items": [ { "no": "16", "text": "Situation …", "answer": "d" }, { "no": "20", "text": "…", "answer": "X" } ],
  "ads": { "a": { "img": "img/mt1-anzeige-a.png", "alt": "full text of the ad, for screen readers" } },
  "unused": ["c"]
}
```
Six ads (a–f), one is used for the example, four are matched, one stays unused (`unused`). Exactly one item has the answer `"X"` (no ad fits). Each ad is a cropped picture from the PDF; `alt` repeats its text.

## Hören (ca. 30 min, 20 items, 1,25 points each)

- `t1` – five short texts, items 1–5 (a/b/c), each twice. `instruction`, `items [ { no, stem, options, answer } ]`.
- `t2` – conversation, items 6–10, once. `persons [ { no, name, answer } ]` – the first entry is the example (`"no": "0"`); `pictures { a…i: { img, alt } }`; `unused` lists the three letters nobody takes. The answer is the picture letter.
- `t3` – five short conversations, items 11–15 (a/b/c), once. Each option is a picture: `options { a: { img, alt }, b: {…}, c: {…} }`.
- `t4` – interview, items 16–20 (Ja/Nein), twice. `instruction`, `context`, `example { no: "0", text, answer }`, `items [ { no, text, answer } ]`.

The audio files are `Goethe A2 Modelltest N.1.mp3` … `N.4.mp3` in the app folder, one per Teil.

## Schreiben (30 min)

```json
"schreiben": {
  "intro": "…",
  "tasks": [
    { "no": 1, "minutes": 10, "words": [20, 30], "situation": ["…"], "points": ["…", "…", "…"], "instruction": "…",
      "model": { "label": "SMS, 30 Wörter", "text": "…" }, "typicalErrors": "…" },
    { "no": 2, "minutes": 20, "words": [30, 40], "…": "…" }
  ],
  "good": [ { "label": "Erfüllung", "text": "…" } ]
}
```
`words` is `[minimum, maximum]`. `model` and `typicalErrors` come from page 18; `good` lists what a good answer does. All three are shown only after submission. Schreiben is not scored automatically: the result screen explains that teachers grade it (25 points) and lets the learner send the text to the teacher.

## index (for index.html)

```json
"index": {
  "hoeren": { "t1": "Fünf kurze Texte", "t2": "Gespräch: …", "t3": "Fünf kurze Gespräche", "t4": "Interview: …" },
  "schreiben": ["SMS an …: …", "E-Mail an …: …"],
  "sprechen": { "teil1": ["8 keyword cards"], "teil2": ["Thema 1", "Thema 2"], "teil3": "Planungsaufgabe (Zeitangabe)" }
}
```
