# Stolz und Vorurteil - modernes Deutsch

Eine direkte Neuübersetzung von Jane Austens *Pride and Prejudice* in modernes Deutsch. Grundlage ist die mitgelieferte Project-Gutenberg-EPUB-Ausgabe des englischen Originals.

## Ausgaben

- Englisches Original: Jane Austen, *Pride and Prejudice* (1813), aus der mitgelieferten Project-Gutenberg-Ausgabe.
- Deutsche Übersetzung: ChatGPT, mit Hilfe von Patrick Stein.
- Deutsch-englische Lernfassung: jeder Absatz zuerst in modernem Deutsch, danach im englischen Original.
- Englisch-deutsche Lernfassung: jeder Absatz zuerst im englischen Original, danach in modernem Deutsch.
- Widmung: »Für meine Eltern Brigitte und Wolfgang, damit Ihr Euch auch dran erfreuen könnt«.

## Aufbau

- `source-chapters/`: englische Referenzkapitel, aus der EPUB extrahiert
- `modern-german-chapters/`: die 61 fertigen deutschen Kapitel
- `illustrations/`: 97 Illustrationen und 59 dekorative Initialen von Hugh Thomson aus der George-Allen-Ausgabe von 1894, ergänzt um drei neu erzeugte Initialen für `F`, `U` und `Z`
- `frontmatter/`: Titel-, Quellen- und Widmungsseiten
- `tools/`: Extraktion, Prüfung und Erstellung der Buchausgaben
- `dist/`: erzeugte EPUB-, HTML- und PDF-Ausgaben der deutschen, englischen und beiden zweisprachigen Fassungen
- `.github/workflows/` und `.gitea/workflows/`: CI-Builds für GitHub Actions und Gitea Actions

## Bauen

Voraussetzungen: Python 3, `reportlab` und Pandoc.

```sh
python3 -m pip install reportlab
python3 tools/build_book.py all
python3 tools/verify_translation.py
```

Eine einzelne Ausgabe lässt sich mit `german`, `english`, `german-english`
oder `english-german` statt `all` bauen. `bilingual` bleibt als Kurzform für
`german-english` erhalten. Beide zweisprachigen Lernfassungen werden
automatisch aus den absatzgleichen deutschen und englischen Kapiteln erzeugt,
sodass die Texte bei späteren Korrekturen synchron bleiben.

In beiden Lernfassungen erscheinen auch die Bildunterschriften zweisprachig
und in der jeweiligen Sprachreihenfolge. Bild und Unterschriften werden als
gemeinsamer Seitenblock gesetzt, damit die Beschriftung nicht auf die
Folgeseite rutscht.

Die Übersetzungsregeln stehen in [AGENTS.md](AGENTS.md). Die Eingabe-EPUB selbst bleibt unverändert in `/Users/jolly/Downloads/pg1342-images-3.epub`.

Die deutsche Ausgabe übernimmt die Kapitelköpfe, Szenenbilder, Schlussvignetten und dekorativen Kapitelinitialen der illustrierten Ausgabe. Das historische Frontispiz »Reading Jane’s Letters. Chap 34.« erscheint als Szenenbild unmittelbar nach dem ersten Absatz von Kapitel XXXIV. Englische Bildtexte im historischen Originalbild bleiben unverändert; zusätzlich erscheint jeweils eine deutsche Bildunterschrift.

Für jedes deutsche Kapitel wählt der Buchbau eine Initiale mit dem passenden Anfangsbuchstaben. Wenn möglich bleibt das historische Bild in seinem Ursprungskapitel; danach werden zunächst alle verfügbaren Varianten eines Buchstabens verwendet, bevor sich ein Motiv wiederholt. Die im englischen Bestand nicht vorhandenen Buchstaben `F`, `U` und `Z` werden durch ausdrücklich als neu erzeugt dokumentierte Bilder ergänzt.

Um die historischen Bilddateien, Initialen und ihre Manifeste erneut aus der Quell-EPUB zu importieren:

```sh
python3 tools/import_illustrations.py /Users/jolly/Downloads/pg1342-images-3.epub
```

## GitHub-Veröffentlichungen

Beim Veröffentlichen eines GitHub-Releases baut die GitHub Action die deutsche
Fassung und beide zweisprachigen Lernfassungen. Sie hängt für jede Ausgabe drei
Formate sowie ein Formatarchiv an das Release:

- `Stolz-und-Vorurteil-modernes-Deutsch.epub`
- `Stolz-und-Vorurteil-modernes-Deutsch.html`
- `Stolz-und-Vorurteil-modernes-Deutsch.pdf`
- `Stolz-und-Vorurteil-modernes-Deutsch.zip` mit allen drei Formaten
- `Stolz-und-Vorurteil-Deutsch-Englisch.epub`
- `Stolz-und-Vorurteil-Deutsch-Englisch.html`
- `Stolz-und-Vorurteil-Deutsch-Englisch.pdf`
- `Stolz-und-Vorurteil-Deutsch-Englisch.zip` mit allen drei Formaten
- `Pride-and-Prejudice-Englisch-Deutsch.epub`
- `Pride-and-Prejudice-Englisch-Deutsch.html`
- `Pride-and-Prejudice-Englisch-Deutsch.pdf`
- `Pride-and-Prejudice-Englisch-Deutsch.zip` mit allen drei Formaten

Für ein bereits vorhandenes Release kann die Action manuell über **Actions → Build book editions → Run workflow** gestartet werden. Dazu wird dessen Tag, zum Beispiel `2026.07.24.0919`, in `release_tag` eingetragen.

## Gitea-Veröffentlichungen

Beim Veröffentlichen eines Gitea-Releases baut die Gitea Action dieselben zwölf Dateien und hängt sie an das Release. Der Build installiert Python, ReportLab und Pandoc direkt im Debian-Container, damit er auch auf dem ARM64-Runner funktioniert.

Für ein bereits vorhandenes Release kann die Action manuell über **Actions → Build book editions → Run workflow** gestartet werden. Dazu wird dessen Tag in `release_tag` eingetragen. Ein erneuter Lauf ersetzt gleichnamige Release-Dateien.
