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
- `illustrations/` enthält Hugh Thomsons Illustrationen und dekorative Initialen aus der George-Allen-Ausgabe von 1894. `manifest.json` ordnet die Illustrationen kapitel- und absatzgenau zu; `initials/manifest.json` katalogisiert die historischen Initialen nach Buchstabe und Ursprungskapitel. Die drei neu erzeugten Initialen `F`, `U` und `Z` liegen mit eindeutig dokumentierter Provenienz unter `generated-initials/`. Die Kapitel-Markdown-Dateien bleiben dadurch textrein.
- Die historischen Bilddateien werden nicht retuschiert. Wo englischer Text Teil der Zeichnung ist, ergänzt der Buchbau eine deutsche Bildunterschrift unter dem unveränderten Original.
- Bewahre Handlung, Ironie, Erzählperspektive, Dialogwechsel und Absatzstruktur. Formuliere idiomatisches, gegenwärtiges Hochdeutsch; vermeide bewusst altertümelnde Syntax, sofern sie nicht eine Figur charakterisiert.
- Namen, Ortsnamen, Anreden und Titel bleiben grundsätzlich englisch. `Mr.`, `Mrs.`, `Miss`, `Lady` und `Sir` bleiben erhalten, damit die soziale Tonlage nicht verfälscht wird.
- Nutze deutsche Guillemets (`»…«`) für direkte Rede und den langen Gedankenstrich (`—`) für abrupte Unterbrechungen. Kursivsetzungen werden in Markdown mit `*…*` erhalten.
- Jedes fertige Kapitel beginnt mit `# Kapitel <römische Zahl>` und enthält ausschließlich den übersetzten Kapiteltext; keine englischen Abschnitte, Notizen oder Zusammenfassungen.
- Prüfe vor dem Abschließen eines Kapitels: keine ausgelassenen Absätze, konsistente Namen und Anreden, keine maschinell wirkenden Satzfragmente.
