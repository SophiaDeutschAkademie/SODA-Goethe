# Modelltest JSON schema (digital exam data)

One file per Modelltest: `digital-src/data/mtN.json`, UTF-8, valid JSON.
Run `python3 digital-src/validate.py digital-src/data/mtN.json` until it prints `OK` with no errors.

## General transcription rules (very important)

- Copy the German text **verbatim** from the PDF: same words, punctuation, capitalisation, „…“ quotes, – dashes, … ellipsis, ß, ä/ö/ü, numbers, units, e-mail/web addresses. Do not correct, shorten, paraphrase or modernise anything.
- Join the lines of one paragraph with single spaces. Remove only word-break hyphenation at line ends (`Verbin-` + `dung` → `Verbindung`). Keep real hyphens of compounds and abbreviations (`E-Mail`, `WLAN-Router`, `Kundenberater/-in`, `(m/w/d)`, `Mitglieds-App` if the hyphen is part of the word). When unsure, look at the page image and use common German spelling to decide.
- A new paragraph in the PDF (blank line / indent / visible gap) = a new string in `paragraphs`.
- Leave out page furniture: page numbers, the header line `Kandidatenblätter · 65 Minuten Lesen`, the rotated side label (`Lesen`, `neseL`, `neröH`, `nebierhcS` …), `Arbeitszeit: …` lines, the `Lesen Teil 1` heading itself, the `Richtig / Falsch`, `Ja / Nein`, `a b c` answer boxes, and `Anzeige: ____` blanks.
- Ignore decorative graphics (logos, stars ★, rotated/mirrored decorative strings such as `8140 .rN · TTIRTNIE`, stamps like `ERST ab 18` unless they carry information a reader needs – if they carry information, write it normally, e.g. `Erst ab 18`).
- Letter-spaced headings (`S T U D I O O R D N U N G · F I T N E S S S T U D I O V I TA L`, `L E S E R K O M M E N TA R E`) are written normally (`STUDIOORDNUNG · FITNESSSTUDIO VITAL`). Keep the original capitalisation of the visible heading.
- Item numbers are strings: `"0"`, `"1"`, … `"30"`, Hören example numbers `"01"`, `"02"`.
- Answers: Richtig/Falsch → `"R"`/`"F"`; Ja/Nein → `"J"`/`"N"`; multiple choice → `"a"`/`"b"`/`"c"`; Lesen Teil 3 → ad letter `"a"`…`"j"` or `"0"`; Hören Teil 4 → `"a"`/`"b"`/`"c"` (speaker column).
- **Every item answer must come from the Lösungsschlüssel page** (usually page 17). Example (Beispiel) answers come from the marked box / filled blank on the task page.
- Multiple-choice stems usually end with ` …` – keep exactly as printed. Options: keep the text after the letter, without the letter itself.

## Top level

```json
{
  "id": 4,
  "roman": "IV",
  "lesen": { "t1": {...}, "t2": {...}, "t3": {...}, "t4": {...}, "t5": {...} },
  "hoeren": { "t1": {...}, "t2": {...}, "t3": {...}, "t4": {...} },
  "schreiben": { "intro": "...", "tasks": [ {...}, {...}, {...} ] },
  "notes": "free text: anything uncertain, OCR doubts, discrepancies you found and how you resolved them"
}
```

## Lesen

### t1 – Blog/E-Mail, Richtig/Falsch, items 1–6
```json
"t1": {
  "instruction": "Lesen Sie den Text und die Aufgaben 1 bis 6 dazu. Wählen Sie: Sind die Aussagen Richtig oder Falsch?",
  "blog": {
    "site": "dienstags-um-acht.de · Daniel",
    "date": "Sonntag, 8. Dezember",
    "title": "Lampenfieber",
    "paragraphs": ["Gestern war es so weit: mein erstes Konzert. …", "…"],
    "closing": "Bis bald, Daniel"
  },
  "example": { "no": "0", "text": "Daniel singt seit diesem Jahr in einem Chor.", "answer": "R" },
  "items": [ { "no": "1", "text": "Die Idee, in einem Chor zu singen, kam nicht von Daniel selbst.", "answer": "R" } ]
}
```
`site`/`date`/`closing` may be `""` if the PDF has none. If the text is an e-mail, put sender/subject lines in `site`/`date`/`title` as printed.

### t2 – two press texts, a/b/c, items 7–9 and 10–12
```json
"t2": {
  "texts": [
    {
      "instruction": "Lesen Sie den Text aus der Presse und die Aufgaben 7 bis 9 dazu. Wählen Sie bei jeder Aufgabe die richtige Lösung a, b oder c.",
      "title": "Eine Stunde Ruhe",
      "lead": "In Oberkirchen dreht ein Supermarkt jeden Mittwoch Musik und Licht herunter.",
      "paragraphs": ["Jeden Mittwoch um 15 Uhr wird es …"],
      "footnote": "",
      "source": "aus einer deutschen Zeitung",
      "example": { "no": "0", "stem": "Die stille Stunde …", "options": { "a": "gibt es jeden Tag.", "b": "gibt es einmal pro Woche.", "c": "gibt es nur am Wochenende." }, "answer": "b" },
      "items": [ { "no": "7", "stem": "In diesem Text geht es um …", "options": { "a": "…", "b": "…", "c": "…" }, "answer": "c" } ]
    },
    { "instruction": "… Aufgaben 10 bis 12 …", "title": "…", "lead": "…", "paragraphs": [], "footnote": "*Pensionist = österreichischer Standard für „Rentner“", "source": "aus einer österreichischen Zeitung", "example": null, "items": [] }
  ]
}
```
The press texts are printed in **two columns**: read the whole left column first, then the right column (check the page image!). `pdftotext -raw` order is NOT reliable for these pages.

### t3 – Anzeigen, items 13–19
```json
"t3": {
  "instruction": "Lesen Sie die Situationen 13 bis 19 und die Anzeigen a bis j aus verschiedenen deutschsprachigen Medien. Wählen Sie: Welche Anzeige passt zu welcher Situation? Sie können jede Anzeige nur einmal verwenden. Die Anzeige aus dem Beispiel können Sie nicht mehr verwenden. Für eine Situation gibt es keine passende Anzeige. In diesem Fall schreiben Sie 0.",
  "context": "Einige Ihrer Bekannten suchen eine Stelle, einen Ausbildungsplatz oder einen Nebenjob.",
  "example": { "no": "0", "text": "…", "answer": "b" },
  "items": [ { "no": "13", "text": "…", "answer": "h" } ],
  "ads": [
    {
      "letter": "a",
      "header": "Volkshochschule Nord",
      "tag": "FRÜHJAHR",
      "title": "Spanisch für die Reise – Mexiko, Kuba, Spanien",
      "subtitle": "Sprache und Alltag für unterwegs",
      "facts": ["Montag und Mittwoch · 18.30–20.00 Uhr", "12 Abende ab 8. April · 180 €"],
      "body": ["Am Ende können Sie im Restaurant bestellen, …"],
      "footer": "www.vhs-nord.de · 0421 / 36 10 10"
    }
  ]
}
```
Exactly 10 ads a–j. All ad fields except `letter` are optional (use `""` or `[]`). Use the fields to keep the visible structure: `header` = organisation/brand name, `tag` = small label (e.g. `STELLENANGEBOT`, `AUSBILDUNG`), `title` = main bold heading, `subtitle`, `facts` = short detail lines (times, prices, dates), `body` = running text paragraphs, `footer` = contact line(s) (several contacts joined with ` · `). Every piece of information printed in the ad must end up somewhere.

### Optional: ad layouts (`design`, `deco`)

Each ad may carry `"design"` (layout name) and `"deco"` (layout options). Use a different layout for every ad of one Modelltest; the text fields stay the same. Without `design` the app picks layouts in a fixed rotation.

| design | look | uses |
|---|---|---|
| `inst` | institution card, header line with tag, facts as table | course, school |
| `serif` | grey paper, serif type, italic subtitle | workshop, craft |
| `dashed` | dashed frame, price/contact strip at the bottom | course with price |
| `barhead` | black header bar (optional `deco.icon`) | business |
| `rules` | thick rules top and bottom, centred serif title | restaurant, culture |
| `inverse` | dark background, white type | club, youth, tech |
| `classified` | newspaper classified, justified serif, bold lead | small ad |
| `mono` | typewriter body, facts as table (optional `deco.icon`) | practice, repair |
| `tearoff` | flyer with tear-off phone strips (`deco.strip`, else phone from footer) | notice board |
| `chalk` | chalkboard, handwriting | café, school |
| `corp` | company wordmark, thin rules | job offer |
| `hotel` | double frame, small caps (`deco.stars` or `deco.icon`) | hotel, museum |
| `band` | grey band with big tag word | training, service |
| `stamp` | round badge with the tag | offer with condition |
| `logo` | round initial logo (or `deco.icon`) | salon, association |
| `browser` | browser window (`deco.url`, `deco.button`) | online offer |
| `stripes` | diagonal stripes top and bottom | urgent job, emergency |
| `ticket` | ticket with side stub (`deco.stub`) | cinema, event |
| `postcard` | postcard, handwritten title, price stamp from tag | holiday |
| `badge` | black price box from tag, square bullets for facts | holiday home |
| `timetable` | black bar, timetable lines from facts, price | train trip |
| `bignum` | big number from tag (`12 TAGE`) | cruise, course length |
| `route` | route line from a fact `A – B – C` | cycling tour |
| `pinned` | pinned paper note | volunteer, community |
| `rounded` | rounded thick frame, spaced capitals (optional `deco.icon`) | camping, pets |
| `dropcap` | classified with drop cap | language school |
| `coupon` | dashed coupon with scissors | camp, cleaning |
| `greyband` | grey title band | travel agency, tutoring |
| `club` | green-white club band | sports club |
| `speech` | speech-bubble title | language café |
| `notebook` | lined paper, handwritten title | tutoring |
| `sign` | dark enamel sign (optional `deco.icon`) | shop |

Icons for `deco.icon`: `bus`, `columns`, `paw`, `key`, `wrench`, `note`, `plug`.

### t4 – Leserkommentare, Ja/Nein, items 20–26
```json
"t4": {
  "instruction": "Lesen Sie die Texte 20 bis 26. Wählen Sie: Ist die Person für offene Geschäfte am Sonntag, Ja oder Nein?",
  "context": "In einer Zeitschrift lesen Sie Kommentare zu einem Artikel über Städte, in denen Geschäfte künftig auch sonntags öffnen dürfen.",
  "header": "LESERKOMMENTARE",
  "site": "www.verbraucher-magazin.de/forum",
  "example": { "no": "0", "name": "Ursula", "byline": "Ursula, 58, Stuttgart", "text": "Sechs Tage in der Woche kann man einkaufen, …", "answer": "N" },
  "items": [ { "no": "20", "name": "Marco", "byline": "Marco, 29, Leipzig", "text": "Ich arbeite als Pfleger im Schichtdienst, …", "answer": "J" } ]
}
```
The comments are in two columns, each comment ends with its byline (right-aligned). Do not mix comments up – check the image.

### t5 – Hausordnung/Regeln, a/b/c, items 27–30
```json
"t5": {
  "instruction": "Lesen Sie die Aufgaben 27 bis 30 und den Text dazu. Wählen Sie bei jeder Aufgabe die richtige Lösung a, b oder c.",
  "context": "Sie haben sich in einem Fitnessstudio angemeldet und lesen die Studioordnung.",
  "doc": {
    "title": "STUDIOORDNUNG · FITNESSSTUDIO VITAL",
    "intro": "",
    "sections": [ { "heading": "Mitgliedschaft und Zutritt", "text": "Mitglied werden kann man ab 14 Jahren; …" } ],
    "footer": ""
  },
  "example": null,
  "items": [ { "no": "27", "stem": "Wer 15 Jahre alt ist, …", "options": { "a": "braucht nur eine Unterschrift der Eltern.", "b": "darf nur zusammen mit einem Erwachsenen trainieren.", "c": "kann in diesem Alter noch nicht Mitglied im Studio werden." }, "answer": "b" } ]
}
```
Section `heading` without the trailing colon. If the document has no inline headings, use one section with `heading: ""`. Items 27–30 are printed in two columns (27 | 28 / 29 | 30) – options of different items must not be mixed.

## Hören

### t1 – five short texts, items 1–10 (odd = Richtig/Falsch, even = a/b/c)
```json
"t1": {
  "instruction": "Sie hören nun fünf kurze Texte. Sie hören jeden Text zweimal. Zu jedem Text lösen Sie zwei Aufgaben. Wählen Sie bei jeder Aufgabe die richtige Lösung.",
  "readNote": "Lesen Sie zuerst das Beispiel. Dazu haben Sie 10 Sekunden Zeit.",
  "example": [
    { "no": "01", "type": "rf", "text": "Am Dienstagvormittag gibt es im Haus kein Wasser.", "answer": "R" },
    { "no": "02", "type": "abc", "stem": "Frau Albers soll …", "options": { "a": "…", "b": "…", "c": "…" }, "answer": "b" }
  ],
  "texts": [
    { "label": "Text 1", "items": [
      { "no": "1", "type": "rf", "text": "Die Fähre erreicht den Hafen zur geplanten Zeit.", "answer": "F" },
      { "no": "2", "type": "abc", "stem": "Wer mit dem Auto reist, …", "options": { "a": "…", "b": "…", "c": "…" }, "answer": "c" }
    ] }
  ]
}
```
Exactly 5 texts. Example answers: if the boxes are not marked on the task page, take them from the Hörtexte (transcript) pages; if still unclear use `null`.

### t2 – one text, a/b/c, items 11–15
```json
"t2": {
  "instruction": "Sie hören nun einen Text. Sie hören den Text einmal. Dazu lösen Sie fünf Aufgaben. Wählen Sie bei jeder Aufgabe die richtige Lösung a, b oder c.",
  "readNote": "Lesen Sie jetzt die Aufgaben 11 bis 15. Dazu haben Sie 60 Sekunden Zeit.",
  "context": "Sie machen mit einer Gruppe eine Kanutour auf der Lahn. Vor dem Start erklärt der Tourleiter, Herr Brandes, den Ablauf.",
  "items": [ { "no": "11", "stem": "Die Tour …", "options": { "a": "…", "b": "…", "c": "…" }, "answer": "b" } ]
}
```

### t3 – conversation, Richtig/Falsch, items 16–22
```json
"t3": {
  "instruction": "Sie hören nun ein Gespräch. Sie hören das Gespräch einmal. Dazu lösen Sie sieben Aufgaben. Wählen Sie: Sind die Aussagen Richtig oder Falsch?",
  "readNote": "Lesen Sie jetzt die Aufgaben 16 bis 22. Dazu haben Sie 60 Sekunden Zeit.",
  "context": "Sie stehen an einer Bushaltestelle und hören, wie sich zwei Nachbarn, Frau Kaya und Herr Lorenz, unterhalten.",
  "items": [ { "no": "16", "text": "Herr Lorenz ist mit seinem Bruder gewandert.", "answer": "F" } ]
}
```

### t4 – discussion, Zuordnung a/b/c, items 23–30
```json
"t4": {
  "instruction": "Sie hören nun eine Diskussion. Sie hören die Diskussion zweimal. Dazu lösen Sie acht Aufgaben. Ordnen Sie die Aussagen zu: Wer sagt was?",
  "readNote": "Lesen Sie jetzt die Aussagen 23 bis 30. Dazu haben Sie 60 Sekunden Zeit.",
  "context": "Die Moderatorin der Radiosendung „Standpunkte“ diskutiert mit der Café-Besitzerin Miriam Scholz und dem Verbraucherberater Klaus Hartmann über die Frage: „Brauchen wir noch Bargeld?“",
  "speakers": { "a": "Moderatorin", "b": "Miriam Scholz", "c": "Klaus Hartmann" },
  "example": { "no": "0", "text": "Viele Menschen in Deutschland bezahlen noch gern mit Scheinen und Münzen.", "answer": "a" },
  "items": [ { "no": "23", "text": "Seit im Café kein Bargeld mehr angenommen wird, warten die Kunden kürzer.", "answer": "b" } ]
}
```

## Schreiben (page 13 = tasks, page 18(+19) = Musterlösungen)

```json
"schreiben": {
  "intro": "Das Modul Schreiben besteht aus drei Teilen. In den Aufgaben 1 und 3 schreiben Sie E-Mails, in Aufgabe 2 schreiben Sie einen Diskussionsbeitrag. Sie können mit jeder Aufgabe beginnen. Schreiben Sie Ihre Texte auf den Antwortbogen.",
  "tasks": [
    {
      "no": 1, "minutes": 20, "words": 80,
      "situation": ["Sie haben letzte Woche Ihre Führerscheinprüfung bestanden. Ein Freund/Eine Freundin von Ihnen, der/die in einer anderen Stadt wohnt, weiß noch nichts davon."],
      "points": ["Beschreiben Sie: Wie war die Prüfung?", "Begründen Sie: Warum ist der Führerschein für Sie wichtig?", "Machen Sie einen Vorschlag für einen gemeinsamen Ausflug."],
      "post": null,
      "instruction": "Schreiben Sie eine E-Mail (circa 80 Wörter). Schreiben Sie etwas zu allen drei Punkten. Achten Sie auf den Textaufbau (Anrede, Einleitung, Reihenfolge der Inhaltspunkte, Schluss).",
      "model": { "label": "E-Mail an eine Freundin, ca. 95 Wörter", "text": "Betreff: Ich hab’s geschafft!\n\nLiebe Sara,\n\nstell dir vor: …\n\nLiebe Grüße\nTomasz" },
      "typicalErrors": "Leitpunkt 2 wird nur beschrieben, nicht begründet · Vorschlag ohne Ziel oder Zeitpunkt · Sie statt du."
    },
    {
      "no": 2, "minutes": 25, "words": 80,
      "situation": ["Sie haben im Fernsehen eine Sendung zum Thema „Mit Mitte zwanzig noch bei den Eltern wohnen?“ gesehen. Im Online-Gästebuch der Sendung finden Sie folgende Meinung:"],
      "points": [],
      "post": { "site": "www.tv-familienforum.de", "label": "Gästebuch", "author": "Leon · 22.10. 19:47 Uhr", "text": "Ich bin 26 und wohne noch bei meinen Eltern. …" },
      "instruction": "Schreiben Sie nun Ihre Meinung zum Thema (circa 80 Wörter).",
      "model": { "label": "Diskussionsbeitrag, ca. 95 Wörter", "text": "…" },
      "typicalErrors": "…"
    },
    {
      "no": 3, "minutes": 15, "words": 40,
      "situation": ["Ihre Chefin, Frau Albrecht, hat Sie gebeten, am kommenden Samstag zu arbeiten, weil ein Kollege krank ist. Sie haben an diesem Tag aber schon etwas anderes vor."],
      "points": [],
      "post": null,
      "instruction": "Schreiben Sie an Frau Albrecht. Entschuldigen Sie sich höflich, nennen Sie den Grund und machen Sie einen anderen Vorschlag. Schreiben Sie eine E-Mail (circa 40 Wörter). Vergessen Sie nicht die Anrede und den Gruß am Schluss.",
      "model": { "label": "E-Mail an die Chefin, ca. 45 Wörter", "text": "…" },
      "typicalErrors": "…"
    }
  ]
}
```
- `points` without the leading dash. `situation` = all sentences between the task heading and the bullet points / Gästebuch box / instruction.
- `model.text`: keep the line structure of the Musterlösung: `\n` for a line break (e.g. after the greeting, before the name), `\n\n` between paragraphs. Leave out the grey margin digits 1/2/3 that mark the Leitpunkte. The Musterlösungen page has several columns – make sure each model text is complete and not mixed with the neighbouring column or the "Bewertung" table.
- `typicalErrors`: the line(s) for this Aufgabe in the "Typische Fehler" list (without the leading digit). `""` if there is none.
