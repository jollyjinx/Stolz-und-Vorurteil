# Stolz und Vorurteil - modernes Deutsch

Eine direkte Neuübersetzung von Jane Austens *Pride and Prejudice* in modernes Deutsch. Grundlage ist die mitgelieferte Project-Gutenberg-EPUB-Ausgabe des englischen Originals.

## Ausgaben

- Englisches Original: Jane Austen, *Pride and Prejudice* (1813), aus der mitgelieferten Project-Gutenberg-Ausgabe.
- Deutsche Übersetzung: ChatGPT, mit Hilfe von Patrick Stein.
- Widmung: »Für meine Eltern Brigitte und Wolfgang, damit Ihr Euch auch dran erfreuen könnt«.

## Aufbau

- `source-chapters/`: englische Referenzkapitel, aus der EPUB extrahiert
- `modern-german-chapters/`: die 61 fertigen deutschen Kapitel
- `frontmatter/`: Titel-, Quellen- und Widmungsseiten
- `tools/`: Extraktion, Prüfung und Erstellung der Buchausgaben
- `dist/`: erzeugte EPUB-, HTML- und PDF-Ausgaben beider Sprachfassungen
- `.github/workflows/` und `.gitea/workflows/`: CI-Builds für GitHub Actions und Gitea Actions

## Bauen

Voraussetzungen: Python 3, `reportlab` und Pandoc.

```sh
python3 -m pip install reportlab
python3 tools/build_book.py all
python3 tools/verify_translation.py
```

Die Übersetzungsregeln stehen in [AGENTS.md](AGENTS.md). Die Eingabe-EPUB selbst bleibt unverändert in `/Users/jolly/Downloads/pg1342-images-3.epub`.
