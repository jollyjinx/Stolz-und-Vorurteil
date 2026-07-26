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
- Die beiden vollständig zweisprachigen Fassungen werden beim Buchbau automatisch aus den absatzgleichen Dateien in `modern-german-chapters/` und `source-chapters/` erzeugt. Beide enthalten jeden Absatz auf Deutsch und Englisch und müssen als Leseausgaben für deutsch- und englischsprachige Leser sowie als Lernhilfen dokumentiert werden. `german-english` zeigt Deutsch zuerst, `english-german` Englisch zuerst. Keine separaten zweisprachigen Kapiteldateien pflegen.
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
