---
title: Adding a book edition / Eine Buchausgabe hinzufügen
description: Directory contract and integration checklist for future Pride and Prejudice editions.
doc_type: contributor-guide
status: active
scope: editions
---

# Adding a book edition / Eine Buchausgabe hinzufügen

## Principle / Grundsatz

Keep everything unique to an edition in `editions/<edition-id>/`. Put a file
under `shared/` only when several editions intentionally use the same source;
put reusable artwork and styling under `assets/`. Generated books always go to
`dist/` and are never source material.

Alles, was nur zu einer Ausgabe gehört, bleibt in
`editions/<edition-id>/`. Eine Datei gehört nur dann nach `shared/`, wenn
mehrere Ausgaben bewusst dieselbe Quelle verwenden; wiederverwendbare Bilder
und Stile gehören nach `assets/`. Erzeugte Bücher liegen immer in `dist/` und
sind niemals Quellmaterial.

Choose a stable edition ID made from lowercase ASCII words separated by
hyphens, for example `annotated-english`. This ID should also be the builder's
command-line name. Do not encode a version number in the directory name;
versions come from the commit date in `YYYY.MM.DD.HHMMSS` format.

Eine stabile Ausgaben-ID besteht aus kleingeschriebenen ASCII-Wörtern mit
Bindestrichen, zum Beispiel `annotated-english`. Dieselbe ID soll als
Baukommando dienen. Keine Versionsnummer in den Verzeichnisnamen schreiben;
die Version stammt aus dem Commit-Datum im Format `YYYY.MM.DD.HHMMSS`.

## Directory contract / Verzeichnisvertrag

```text
editions/<edition-id>/
  chapters/                 # required for an independent text edition
  frontmatter.md            # required
  introduction.md           # optional edition-specific pre-reading text
  glossary.json             # optional controlled terms and reader glossary
  notes.json                # optional paragraph-anchored reader notes
  alignment-manifest.json   # required for a reviewed transformed text
  GUIDANCE.md               # required when the edition has special rules
```

- `chapters/` contains only chapter headings and book text. Notes and build
  instructions do not belong in chapter files. / `chapters/` enthält nur
  Kapitelüberschriften und Buchtext. Anmerkungen und Bauanweisungen gehören
  nicht in Kapiteldateien.
- `frontmatter.md` contains edition-specific source and copyright text. Cover
  labels, output names, title-page metadata, and dedications are registered in
  `tools/build_book.py`. / `frontmatter.md` enthält ausgabenspezifische
  Quellen- und Rechtstexte. Umschlagtexte, Dateinamen, Titelblatt-Metadaten und
  Widmungen werden in `tools/build_book.py` registriert.
- `introduction.md`, `glossary.json`, and `notes.json` stay local when their
  wording or reading level belongs to one edition. / Einführung, Glossar und
  Anmerkungen bleiben lokal, wenn Wortlaut oder Leseniveau nur zu einer
  Ausgabe gehören.
- `GUIDANCE.md` is a front-matter document and is binding for work on that
  edition. It records the source of truth, language level, fidelity rules,
  typography, and review checklist. / `GUIDANCE.md` ist ein Front-Matter-
  Dokument und für diese Ausgabe verbindlich. Es beschreibt Referenztext,
  Sprachniveau, Treueregeln, Typografie und Prüfcheckliste.
- Derived editions such as bilingual layouts do not duplicate chapters. They
  contain their own `frontmatter.md` and point the builder at the independent
  chapter sets. / Abgeleitete Ausgaben wie zweisprachige Fassungen duplizieren
  keine Kapitel. Sie besitzen eine eigene `frontmatter.md`; der Buchbau
  verweist auf die eigenständigen Kapitelsätze.

## Integration checklist / Integrationscheckliste

1. Create `editions/<edition-id>/` according to the contract above. Add the
   edition and its paths to the `EDITIONS` registry in `tools/build_book.py`.
   / Das Ausgabenverzeichnis anlegen und die Ausgabe mit ihren Pfaden im
   `EDITIONS`-Register in `tools/build_book.py` ergänzen.
2. Reuse `assets/covers/peacock-binding-template.png`; configure the title,
   author, edition type, and output basename in the builder. Do not create a
   pre-labelled cover. / Die gemeinsame Pfauen-Einbandvorlage verwenden und
   Titel, Autorin, Ausgabentyp sowie Dateinamen im Buchbau festlegen. Keinen
   fertig beschrifteten Umschlag anlegen.
3. If the text is translated, simplified, annotated, or otherwise transformed,
   extend `tools/verify_translation.py` with edition-specific structure and
   content checks. Add an alignment manifest only after every changed source
   and target pair has been reviewed. / Bei Übersetzungen, Vereinfachungen,
   Anmerkungen oder anderen Bearbeitungen die ausgabenspezifischen Prüfungen
   ergänzen. Ein Zuordnungsmanifest erst nach der inhaltlichen Prüfung aller
   geänderten Quell- und Zielpaare aktualisieren.
4. Add the edition to both `.github/workflows/build.yml` and
   `.gitea/workflows/build.yml`, including every intended release asset.
   Keep the two release sets identical. / Die Ausgabe samt Release-Dateien in
   beide Workflows aufnehmen und beide Dateisätze identisch halten.
5. Add the edition to the public edition list, repository layout, build
   commands, and release asset list in `README.md`. Update `AGENTS.md` when the
   edition introduces a lasting editorial rule. / Ausgabe, Baukommando und
   Release-Dateien im öffentlichen `README.md` dokumentieren; dauerhafte
   Redaktionsregeln zusätzlich in `AGENTS.md` festhalten.
6. Run the verifier, build the new edition, inspect its HTML, EPUB, PDF, and
   rendered cover, and confirm that internal images resolve from
   `assets/illustrations/`. / Prüfung und Buchbau ausführen, HTML, EPUB, PDF und
   Umschlag kontrollieren und die Bildpfade aus `assets/illustrations/`
   bestätigen.

## Required checks / Erforderliche Prüfungen

```sh
python3 tools/verify_translation.py
python3 tools/build_book.py <edition-id>
git diff --check
```

For a transformed chapter set, verification must cover all 61 chapters,
headings, exact paragraph alignment, dialogue and emphasis, numbers and names,
notes, glossary terms, and the reviewed alignment hashes. A successful build
alone is not a content review.

Bei einem bearbeiteten Kapitelsatz müssen alle 61 Kapitel, Überschriften, die
exakte Absatzzuordnung, Dialoge und Hervorhebungen, Zahlen und Namen,
Anmerkungen, Glossarbegriffe sowie die geprüften Zuordnungs-Hashes kontrolliert
werden. Ein erfolgreicher Buchbau ersetzt keine inhaltliche Prüfung.
