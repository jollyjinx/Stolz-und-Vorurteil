# Reusable cover artwork / Wiederverwendbare Umschlaggestaltung

**English:** `peacock-binding-template.png` is the single visual master for
all book editions. It is a 1024 × 1536 pixel RGB PNG with a dark bookcloth
ground, paired peacocks, botanical ornaments, and an empty central oval. The
book builder adds the title, author, edition name, and version number
deterministically with Pillow and writes the finished edition covers to
`dist/*-cover.png`.

**Deutsch:** `peacock-binding-template.png` ist die einzige Bildvorlage für
alle Buchausgaben. Die RGB-PNG-Datei ist 1024 × 1536 Pixel groß und zeigt einen
dunklen Bucheinband mit zwei Pfauen, Pflanzenornamenten und einer leeren ovalen
Titelkartusche. Der Buchbau setzt Titel, Autorin, Ausgabenbezeichnung und
Versionsnummer reproduzierbar mit Pillow und schreibt die fertigen Umschläge
nach `dist/*-cover.png`.

## Provenance / Herkunft

**English:** The established modern German cover was originally generated
with OpenAI on 28 July 2026 as original artwork. A photograph of a historical
*Pride and Prejudice* binding served only as a mood and craft reference; the
photograph itself is not included, edited, or reproduced. On 8 August 2026,
OpenAI removed only the title, subtitle, and author lettering from that cover.
The border, oval, peacocks, feathers, flowers, colors, and aged binding texture
were preserved to create the reusable master.

**Deutsch:** Der Umschlag der modernen deutschen Ausgabe wurde am 28. Juli
2026 mit OpenAI als eigenständige Gestaltung erzeugt. Das Foto eines
historischen *Pride-and-Prejudice*-Einbands diente nur als Referenz für
Stimmung und handwerkliche Anmutung; das Foto selbst wird weder eingebunden
noch bearbeitet oder reproduziert. Am 8. August 2026 entfernte OpenAI nur
Titel, Untertitel und Autorinnenname aus diesem Umschlag. Rahmen, Oval, Pfauen,
Federn, Blumen, Farben und die gealterte Einbandstruktur blieben für die
wiederverwendbare Vorlage erhalten.

The earlier separately lettered covers are retained in `legacy/` for design
provenance only. The builder never reads them.

Die früheren einzeln beschrifteten Umschläge bleiben nur zur Dokumentation der
Gestaltung in `legacy/` erhalten. Der Buchbau verwendet sie nicht.

## Build behavior / Verhalten beim Buchbau

The cover wording comes from the edition metadata in `tools/build_book.py`:

- title / Titel
- edition type / Ausgabentyp
- `JANE AUSTEN`
- `VERSION <number>` / `VERSION <Nummer>`

`--version YYYY.MM.DD.HHMMSS` has the highest priority. Otherwise the builder
uses the `BOOK_VERSION` environment variable, followed by the current commit
date in `YYYY.MM.DD.HHMMSS` format. An explicit version remains available for
reproducible previews.

`--version YYYY.MM.DD.HHMMSS` hat die höchste Priorität. Andernfalls verwendet
der Buchbau die Umgebungsvariable `BOOK_VERSION` und danach das Datum des
aktuellen Commits im Format `YYYY.MM.DD.HHMMSS`. Für reproduzierbare Vorschauen
kann weiterhin eine bestimmte Versionsnummer angegeben werden.

The generated image is embedded as the semantic EPUB cover, placed before the
title block in standalone HTML, and used as the first full PDF page. The PNG
also remains in `dist/` as a separate build artifact.

Das erzeugte Bild wird als semantischer EPUB-Umschlag eingebunden, im
eigenständigen HTML vor den Titelblock gestellt und als erste ganzseitige
PDF-Seite verwendet. Zusätzlich bleibt die PNG-Datei als eigenes
Build-Artefakt in `dist/` erhalten.

## Image-edit prompt / Prompt für die Bildbearbeitung

The reusable master was made by editing the established modern German cover:
remove every piece of lettering from the central oval; reconstruct the cleared
areas with matching dark aged bookcloth; preserve the complete border, oval,
dotted rim, peacocks, feathers, flowers, vines, jewel colors, and distressed
print texture; leave the divider ornaments in place; add no new text, symbols,
watermarks, cropping, or redesign.

Die wiederverwendbare Vorlage entstand durch Bearbeitung des bestehenden
modernen deutschen Umschlags: sämtliche Schrift aus der ovalen Titelkartusche
entfernen; die freien Flächen mit passender dunkler, gealterter
Bucheinbandstruktur ergänzen; Rahmen, Oval, Punktrand, Pfauen, Federn, Blumen,
Ranken, Schmuckfarben und Druckstruktur vollständig erhalten; die
Trennornamente beibehalten; keine neue Schrift, Symbole, Wasserzeichen,
Beschnitte oder Umgestaltung hinzufügen.
