# Pride and Prejudice / Stolz und Vorurteil

## Modern German and bilingual editions / Moderne deutsche und zweisprachige Ausgaben

**English:** A direct new translation of Jane Austen’s *Pride and Prejudice*
into modern German, accompanied by fully bilingual editions for English- and
German-speaking readers as well as language learners. The English text is
based on the supplied Project Gutenberg EPUB edition.

**Deutsch:** Eine direkte Neuübersetzung von Jane Austens *Pride and
Prejudice* in modernes Deutsch, ergänzt um vollständig zweisprachige Ausgaben
für deutsch- und englischsprachige Leser sowie für Sprachlernende. Grundlage
des englischen Textes ist die mitgelieferte Project-Gutenberg-EPUB-Ausgabe.

## Editions / Ausgaben

| Build target / Build-Ziel | Contents / Inhalt | Filename / Dateibasis | Release |
|---|---|---|---|
| `german` | Modern German translation / Moderne deutsche Übersetzung | `Stolz-und-Vorurteil-modernes-Deutsch` | yes / ja |
| `english` | Project Gutenberg English original / Englisches Project-Gutenberg-Original | `Pride-and-Prejudice-English` | build artifact only / nur Build-Artefakt |
| `german-english` | Fully bilingual, German first / Vollständig zweisprachig, Deutsch zuerst | `Stolz-und-Vorurteil-Deutsch-Englisch` | yes / ja |
| `english-german` | Fully bilingual, English first / Vollständig zweisprachig, Englisch zuerst | `Pride-and-Prejudice-Englisch-Deutsch` | yes / ja |

**English:** The German translation was created by ChatGPT with the assistance
of Patrick Stein. The dedication reads: “For my parents Brigitte and Wolfgang,
so that you may enjoy it too.”

**Deutsch:** Die deutsche Übersetzung stammt von ChatGPT, mit Hilfe von
Patrick Stein. Die Widmung lautet: »Für meine Eltern Brigitte und Wolfgang,
damit Ihr Euch auch dran erfreuen könnt«.

## Bilingual reading / Zweisprachig lesen

**English:** Both bilingual editions contain the complete novel as 2,051
German-English paragraph pairs. Every paragraph is present in both languages,
allowing English- and German-speaking readers to read in their preferred
language while keeping the other text immediately available for comparison.

- `german-english` presents the modern German translation first, followed
  directly by the English original. It is especially convenient for readers
  who prefer German first and for German speakers learning English.
- `english-german` presents the English original first, followed directly by
  the modern German translation. It is especially convenient for readers who
  prefer English first and for English speakers learning German.

These are equal bilingual reading editions, not merely study aids. They also
support shared reading and direct comparison of Jane Austen’s original with
the modern German translation without switching between separate books.

**Deutsch:** Beide zweisprachigen Fassungen enthalten den vollständigen Roman
in 2.051 deutsch-englischen Absatzpaaren. Jeder Absatz ist in beiden Sprachen
vorhanden. Dadurch können deutsch- und englischsprachige Leser in ihrer
bevorzugten Sprache lesen und den jeweils anderen Text direkt vergleichen.

- `german-english` zeigt zuerst die moderne deutsche Übersetzung und direkt
  danach das englische Original. Diese Variante eignet sich besonders für
  Leser, die Deutsch zuerst sehen möchten, sowie für Deutschsprachige beim
  Englischlernen.
- `english-german` zeigt zuerst das englische Original und direkt danach die
  moderne deutsche Übersetzung. Diese Variante eignet sich besonders für
  Leser, die Englisch zuerst sehen möchten, sowie für Englischsprachige beim
  Deutschlernen.

Beide Varianten sind gleichwertige zweisprachige Leseausgaben und nicht nur
Lernhilfen. Sie ermöglichen ebenso gemeinsames Lesen und den unmittelbaren
Vergleich von Jane Austens Original mit der modernen deutschen Übersetzung,
ohne zwischen getrennten Büchern zu wechseln.

## Repository layout / Aufbau

- `source-chapters/`: English reference chapters extracted from the EPUB /
  englische Referenzkapitel, aus der EPUB extrahiert
- `modern-german-chapters/`: all 61 completed German chapters / alle 61
  fertigen deutschen Kapitel
- `illustrations/`: 97 Hugh Thomson illustrations and 59 historical
  decorative initials from the 1894 George Allen edition, plus three newly
  generated initials for `F`, `U`, and `Z` / 97 Illustrationen und 59
  historische Initialen von Hugh Thomson, ergänzt um drei neu erzeugte
  Initialen für `F`, `U` und `Z`
- `covers/`: newly generated cover artwork for the German and both bilingual
  release editions / neu erzeugte Umschlaggestaltung für die deutsche und
  beide zweisprachigen Veröffentlichungsausgaben
- `frontmatter/`: title, source, and dedication pages / Titel-, Quellen- und
  Widmungsseiten
- `tools/`: extraction, verification, and book-building tools / Werkzeuge für
  Extraktion, Prüfung und Buchbau
- `dist/`: generated EPUB, HTML, and PDF editions / erzeugte EPUB-, HTML- und
  PDF-Ausgaben
- `.github/workflows/` and `.gitea/workflows/`: GitHub Actions and Gitea
  Actions builds / CI-Builds für GitHub Actions und Gitea Actions

## Build / Bauen

**Requirements / Voraussetzungen:** Python 3, `lxml`, `reportlab`, and Pandoc.

```sh
python3 -m pip install lxml reportlab
python3 tools/build_book.py all
python3 tools/verify_translation.py
python3 tools/verify_translation.py --epub /Users/jolly/Downloads/pg1342-images-3.epub
```

**English:** Replace `all` with `german`, `english`, `german-english`, or
`english-german` to build a single edition. `bilingual` remains an alias for
`german-english`. The bilingual editions are generated automatically from the
paragraph-aligned English and German chapters, keeping both texts synchronized
when corrections are made.

**Deutsch:** Statt `all` kann mit `german`, `english`, `german-english` oder
`english-german` eine einzelne Ausgabe gebaut werden. `bilingual` bleibt als
Kurzform für `german-english` erhalten. Die zweisprachigen Fassungen werden
automatisch aus den absatzgleichen englischen und deutschen Kapiteln erzeugt,
sodass beide Texte bei späteren Korrekturen synchron bleiben.

**English:** The three release editions use their matching artwork from
`covers/`: as the semantic cover in EPUB, before the title block in HTML, and
as the first full cover page in PDF. The English source-only build remains
without newly generated cover artwork.

**Deutsch:** Die drei Veröffentlichungsausgaben verwenden jeweils das
passende Bild aus `covers/`: als semantisches Cover im EPUB, vor dem Titelblock
im HTML und als erste ganzseitige Umschlagseite im PDF. Der rein englische
Referenz-Build bleibt ohne neu erzeugte Umschlaggestaltung.

**English:** The verifier checks headings, paragraph counts, suspicious
mid-sentence splits, and the hashes of every manually audited chapter pairing
in `alignment-manifest.json`. The optional `--epub` check also proves that the
committed English chapters exactly match a fresh extraction of the supplied
EPUB. After an intentional text change, update the manifest only after
reviewing every changed English-German pair:

**Deutsch:** Die Prüfung kontrolliert Überschriften, Absatzanzahlen,
verdächtige Satztrennungen und die Hashes jeder manuell geprüften
Kapitelzuordnung in `alignment-manifest.json`. Mit der optionalen
`--epub`-Prüfung wird zusätzlich nachgewiesen, dass die eingecheckten
englischen Kapitel exakt einer neuen Extraktion der mitgelieferten EPUB-Datei
entsprechen. Nach einer beabsichtigten Textänderung darf das Manifest erst
aktualisiert werden, wenn jedes geänderte Englisch-Deutsch-Paar geprüft wurde:

```sh
python3 tools/verify_translation.py --update-alignment-manifest
```

### Illustrations and captions / Illustrationen und Bildunterschriften

**English:** Both bilingual editions contain 68 complete caption pairs in
their respective language order. The build verifies that a caption exists in
both languages or in neither. Each image and all of its captions form one
unbreakable page block, preventing captions from moving to the next page.
Each English-German paragraph pair likewise forms one pagination unit whenever
it fits on a page. Illustrations are inserted only between complete pairs and
can never separate an original paragraph from its translation.

The German edition includes the chapter headings, scene illustrations, ending
vignettes, and decorative chapter initials from the illustrated source. The
historical frontispiece “Reading Jane’s Letters. Chap 34.” appears as a scene
illustration after the first paragraph of Chapter XXXIV. English text drawn
inside a historical illustration remains unchanged and is accompanied by a
translated caption.

For every German chapter, the builder selects an initial matching its opening
letter. It keeps the historical design in its source chapter where possible,
then uses every available variant before repeating a design. The missing
letters `F`, `U`, and `Z` are supplied by clearly documented newly generated
images.

**Deutsch:** Beide zweisprachigen Fassungen enthalten 68 vollständige
Bildunterschriftspaare in der jeweiligen Sprachreihenfolge. Der Buchbau prüft,
dass eine Beschriftung entweder in beiden Sprachen oder in keiner vorhanden
ist. Bild und sämtliche Unterschriften bilden einen gemeinsamen,
untrennbaren Seitenblock, damit keine Beschriftung auf die Folgeseite rutscht.
Ebenso bildet jedes deutsch-englische Absatzpaar eine gemeinsame
Seiteneinheit, sofern es vollständig auf eine Seite passt. Illustrationen
stehen ausschließlich zwischen vollständigen Paaren und können Original und
zugehörige Übersetzung nie voneinander trennen.

Die deutsche Ausgabe übernimmt Kapitelköpfe, Szenenbilder, Schlussvignetten
und dekorative Kapitelinitialen der illustrierten Quelle. Das historische
Frontispiz »Reading Jane’s Letters. Chap 34.« erscheint als Szenenbild nach
dem ersten Absatz von Kapitel XXXIV. Englischer Text innerhalb einer
historischen Zeichnung bleibt unverändert und wird durch eine übersetzte
Bildunterschrift ergänzt.

Für jedes deutsche Kapitel wählt der Buchbau eine Initiale mit dem passenden
Anfangsbuchstaben. Wenn möglich bleibt das historische Motiv in seinem
Ursprungskapitel; danach werden alle verfügbaren Varianten verwendet, bevor
sich ein Motiv wiederholt. Die fehlenden Buchstaben `F`, `U` und `Z` werden
durch eindeutig dokumentierte neu erzeugte Bilder ergänzt.

**English:** The source assets can be imported again with the following
command.

**Deutsch:** Die Quellbilder und Manifeste lassen sich mit folgendem Befehl
erneut importieren.

```sh
python3 tools/import_illustrations.py /Users/jolly/Downloads/pg1342-images-3.epub
```

**English:** Translation rules are documented in [AGENTS.md](AGENTS.md). The
source EPUB remains unchanged at
`/Users/jolly/Downloads/pg1342-images-3.epub`.

**Deutsch:** Die Übersetzungsregeln stehen in [AGENTS.md](AGENTS.md). Die
Quell-EPUB bleibt unter `/Users/jolly/Downloads/pg1342-images-3.epub`
unverändert.

## GitHub releases / GitHub-Veröffentlichungen

**English:** Publishing a GitHub release builds the modern German edition and
both bilingual editions. Each is attached in three formats and as a ZIP
archive:

**Deutsch:** Beim Veröffentlichen eines GitHub-Releases werden die moderne
deutsche und beide zweisprachigen Fassungen gebaut. Jede wird in drei Formaten
und als ZIP-Archiv angehängt:

- `Stolz-und-Vorurteil-modernes-Deutsch.epub`
- `Stolz-und-Vorurteil-modernes-Deutsch.html`
- `Stolz-und-Vorurteil-modernes-Deutsch.pdf`
- `Stolz-und-Vorurteil-modernes-Deutsch.zip`
- `Stolz-und-Vorurteil-Deutsch-Englisch.epub`
- `Stolz-und-Vorurteil-Deutsch-Englisch.html`
- `Stolz-und-Vorurteil-Deutsch-Englisch.pdf`
- `Stolz-und-Vorurteil-Deutsch-Englisch.zip`
- `Pride-and-Prejudice-Englisch-Deutsch.epub`
- `Pride-and-Prejudice-Englisch-Deutsch.html`
- `Pride-and-Prejudice-Englisch-Deutsch.pdf`
- `Pride-and-Prejudice-Englisch-Deutsch.zip`

**English:** To publish the files to an existing release, run **Actions →
Build book editions → Run workflow** and enter its tag, for example
`2026.07.24.0919`, in `release_tag`.

**Deutsch:** Um die Dateien an ein vorhandenes Release anzuhängen, unter
**Actions → Build book editions → Run workflow** dessen Tag, zum Beispiel
`2026.07.24.0919`, in `release_tag` eintragen.

## Gitea releases / Gitea-Veröffentlichungen

**English:** Gitea Actions builds and publishes the same twelve files. The
workflow installs Python, ReportLab, and Pandoc in its Debian container so it
also works on the ARM64 runner. A repeated run replaces release assets with
the same names.

**Deutsch:** Gitea Actions baut und veröffentlicht dieselben zwölf Dateien.
Der Workflow installiert Python, ReportLab und Pandoc im Debian-Container,
damit er auch auf dem ARM64-Runner funktioniert. Ein erneuter Lauf ersetzt
gleichnamige Release-Dateien.

**English:** For an existing release, run **Actions → Build book editions →
Run workflow** and provide its tag in `release_tag`.

**Deutsch:** Für ein vorhandenes Release unter **Actions → Build book editions
→ Run workflow** dessen Tag in `release_tag` eintragen.
