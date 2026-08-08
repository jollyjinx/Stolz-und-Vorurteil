---
title: Stolz und Vorurteil - Übersetzungsleitfaden
description: Arbeitsregeln für die direkte Neuübersetzung von Jane Austens Pride and Prejudice in modernes Deutsch.
doc_type: agent-guidance
status: active
scope: Books/Stolz-und-Vorurteil-modern-deutsch
source:
  title: Pride and Prejudice
  author: Jane Austen
  source_file: /Users/jolly/Downloads/pg1342-images-3.epub
  source_status: Project Gutenberg public-domain edition
---

# Übersetzungsleitfaden

- Die Übersetzung wird direkt aus der mitgelieferten englischen Project-Gutenberg-Ausgabe angefertigt. Keine Übersetzungsdienste und keine Übernahme bestehender deutscher Übersetzungen.
- `source-chapters/` ist nur die aufbereitete englische Referenz. Die auslieferbaren Kapitel liegen einzeln in `modern-german-chapters/`.
- `easy-german-chapters/` enthält die vollständige zusätzliche Ausgabe in Einfachem Deutsch. Sie ist weder gekürzt noch als formal geregelte *Leichte Sprache* ausgewiesen. Für diese Kapitel gelten zusätzlich und vorrangig die Regeln in `AI/easy-german-translation.md` sowie die verbindlichen Schreibweisen in `easy-german-glossary.json`.
- Fußnoten der Ausgabe in Einfachem Deutsch werden zentral in `easy-german-notes.json` an Kapitel und Absatz verankert und erst beim Buchbau eingesetzt. Dadurch bleiben die Kapiteldateien textrein und absatzgleich mit der englischen Quelle. Dasselbe Glossar dient dem Übersetzungsprozess und wird als Leseglossar am Ende des Buches erzeugt.
- Die EPUB-Extraktion behandelt die sechs XHTML-Dateien als fortlaufenden Text, übernimmt den `alt`-Buchstaben historischer Initialen, erhält jeden inneren Briefabsatz einzeln, verbindet nur durch Illustrationen getrennte Absatzfragmente und verwirft Druckervermerke. Prüfe die eingecheckte Referenz lokal mit `python3 tools/verify_translation.py --epub /Users/jolly/Downloads/pg1342-images-3.epub`.
- Die beiden vollständig zweisprachigen Fassungen werden beim Buchbau automatisch aus den absatzgleichen Dateien in `modern-german-chapters/` und `source-chapters/` erzeugt. Beide enthalten jeden Absatz auf Deutsch und Englisch und müssen als Leseausgaben für deutsch- und englischsprachige Leser sowie als Lernhilfen dokumentiert werden. `german-english` zeigt Deutsch zuerst, `english-german` Englisch zuerst. Keine separaten zweisprachigen Kapiteldateien pflegen.
- `alignment-manifest.json` fixiert die manuell geprüfte Absatzfolge kapitelweise. Aktualisiere es mit `python3 tools/verify_translation.py --update-alignment-manifest` nur nach einer erneuten inhaltlichen Prüfung sämtlicher geänderter Englisch-Deutsch-Paare; gleiche Absatzanzahlen allein beweisen keine korrekte Zuordnung.
- `easy-german-alignment-manifest.json` erfüllt dieselbe Aufgabe für Einfaches Deutsch. Aktualisiere es mit `python3 tools/verify_translation.py --update-easy-alignment-manifest` erst nach Inhalts-, Absatz- und Zugänglichkeitsprüfung sämtlicher geänderter Kapitel.
- Titel-, Metadaten- und Beschriftungsreihenfolge folgt der jeweils zuerst stehenden Sprache: Deutsch in `german-english`, Englisch in `english-german`.
- Das öffentliche `README.md` bleibt vollständig zweisprachig. Inhaltliche Änderungen werden dort gleichwertig auf Englisch und Deutsch dokumentiert; gemeinsame Befehle und Dateilisten müssen nicht dupliziert werden.
- In der englisch-deutschen Fassung nutzt der Buchbau historische Initialen, wo ein passender Buchstabe vorhanden ist. Fehlt ein Motiv im Bestand, bleibt der normale gesetzte Anfangsbuchstabe stehen.
- `illustrations/` enthält Hugh Thomsons Illustrationen und dekorative Initialen aus der George-Allen-Ausgabe von 1894. `manifest.json` ordnet die Illustrationen kapitel- und absatzgenau zu; `initials/manifest.json` katalogisiert die historischen Initialen nach Buchstabe und Ursprungskapitel. Die drei neu erzeugten Initialen `F`, `U` und `Z` liegen mit eindeutig dokumentierter Provenienz unter `generated-initials/`. Die Kapitel-Markdown-Dateien bleiben dadurch textrein.
- Die historischen Bilddateien werden nicht retuschiert. In den zweisprachigen Fassungen stehen die deutsche und englische Bildunterschrift in derselben Sprachreihenfolge wie der Fließtext direkt unter dem unveränderten Original. Bild und alle Bildunterschriften bilden im EPUB-, HTML- und PDF-Buchbau einen untrennbaren Seitenblock.
- In den zweisprachigen Fassungen bildet jedes deutsch-englische Absatzpaar einen gemeinsamen Seitenblock. Illustrationen dürfen nur zwischen vollständigen Absatzpaaren stehen, nie zwischen Original und zugehöriger Übersetzung.
- Bildbeschriftungen in `illustrations/manifest.json` müssen entweder als vollständiges Paar aus `caption_de` und `caption_en` oder in beiden Sprachen leer vorliegen; der Buchbau prüft diese Invariante.
- Bewahre Handlung, Ironie, Erzählperspektive, Dialogwechsel und Absatzstruktur. Formuliere idiomatisches, gegenwärtiges Hochdeutsch; vermeide bewusst altertümelnde Syntax, sofern sie nicht eine Figur charakterisiert.
- Namen, Ortsnamen, Anreden und Titel bleiben grundsätzlich englisch. `Mr.`, `Mrs.`, `Miss`, `Lady` und `Sir` bleiben erhalten, damit die soziale Tonlage nicht verfälscht wird.
- Nutze deutsche Guillemets (`»…«`) für direkte Rede und den langen Gedankenstrich (`—`) für abrupte Unterbrechungen. Kursivsetzungen werden in Markdown mit `*…*` erhalten.
- Jedes fertige Kapitel beginnt mit `# Kapitel <römische Zahl>` und enthält ausschließlich den übersetzten Kapiteltext; keine englischen Abschnitte, Notizen oder Zusammenfassungen.
- Prüfe vor dem Abschließen eines Kapitels: keine ausgelassenen Absätze, konsistente Namen und Anreden, keine maschinell wirkenden Satzfragmente.
