# Cover artwork / Umschlaggestaltung

**English:** This directory contains four newly generated cover images for
the release editions. They were created with OpenAI on 28 July 2026 as
original artwork. A photograph of a historical *Pride and Prejudice* binding
served only as a mood and craft reference; the photograph itself is not
included, edited, or reproduced.

**Deutsch:** Dieser Ordner enthält vier neu erzeugte Umschlagbilder für die
Veröffentlichungsausgaben. Sie wurden am 28. Juli 2026 mit OpenAI als
eigenständige Gestaltung erstellt. Das Foto eines historischen
*Pride-and-Prejudice*-Einbands diente lediglich als Referenz für Stimmung und
handwerkliche Anmutung; das Foto selbst wird weder eingebunden noch
bearbeitet oder reproduziert.

## Editions / Ausgaben

- `Stolz-und-Vorurteil-modernes-Deutsch.png`: German edition / deutsche
  Ausgabe
- `Stolz-und-Vorurteil-Einfaches-Deutsch.png`: Easy German edition / Ausgabe
  in Einfachem Deutsch
- `Stolz-und-Vorurteil-Deutsch-Englisch.png`: bilingual, German first /
  zweisprachig, Deutsch zuerst
- `Pride-and-Prejudice-Englisch-Deutsch.png`: bilingual, English first /
  zweisprachig, Englisch zuerst

All images are 1024 × 1536 pixel RGB PNG files. The shared design uses a new
symmetrical composition with two peacocks, a central oval cartouche, botanical
ornaments, and restrained gold, emerald, teal, and burgundy linework on black
bookcloth. It deliberately avoids the reference cover's single peacock,
pedestal, full-field tail arrangement, and calligraphic title layout.

Alle Bilder sind RGB-PNG-Dateien mit 1024 × 1536 Pixeln. Die gemeinsame
Gestaltung verwendet eine neue symmetrische Komposition aus zwei Pfauen,
zentraler ovaler Titelkartusche, Pflanzenornamenten und zurückhaltenden Gold-,
Smaragd-, Petrol- und Burgundertönen auf schwarzem Buchleinen. Sie vermeidet
bewusst den einzelnen Pfau, den Sockel, die flächige Schwanzfederanordnung und
den kalligrafischen Titelsatz der Referenz.

The book builder embeds the matching image as the semantic EPUB cover, places
it before the title block in the standalone HTML edition, and uses it as the
first full cover page of the PDF. The English source-only build has no newly
generated cover and remains unchanged.

Der Buchbau bindet das jeweils passende Bild als semantisches EPUB-Cover ein,
stellt es in der eigenständigen HTML-Ausgabe vor den Titelblock und verwendet
es als erste ganzseitige Umschlagseite der PDF-Ausgabe. Der rein englische
Referenz-Build besitzt kein neu erzeugtes Cover und bleibt unverändert.

The Easy German cover was generated with OpenAI on 8 August 2026. It keeps
the oval frame, symmetrical botanical linework, muted gold, and historical
bookcloth character of the established series while using a warm ivory ground,
dark green type, fewer ornaments, and small mirrored books and quills for
clearer recognition and improved thumbnail legibility.

Der Umschlag für Einfaches Deutsch wurde am 8. August 2026 mit OpenAI erzeugt.
Er übernimmt ovalen Rahmen, symmetrische Pflanzenlinien, gedämpftes Gold und
die historische Bucheinband-Anmutung der bestehenden Reihe. Ein warmer
elfenbeinfarbener Grund, dunkelgrüne Schrift, weniger Ornamente sowie kleine
gespiegelte Bücher und Schreibfedern sorgen für eine klare Unterscheidung und
bessere Lesbarkeit in der Vorschau.

## Generation prompts / Erzeugungsprompts

The master prompt requested an original late-Victorian Arts-and-Crafts
bookbinding with a black cloth ground, paired peacocks, rising feather and
botanical borders, a central oval title cartouche, and exact German title
text. It explicitly prohibited replication of the reference composition,
publisher marks, watermarks, mockups, and invented lettering.

Der Hauptprompt verlangte einen eigenständigen Arts-and-Crafts-Bucheinband im
Stil des späten 19. Jahrhunderts mit schwarzem Leinen, einem Pfauenpaar,
aufsteigenden Feder- und Pflanzenbordüren, einer ovalen Titelkartusche und
exaktem deutschem Titeltext. Die konkrete Komposition der Referenz,
Verlagszeichen, Wasserzeichen, Buchattrappen und erfundene Schriftzeichen
wurden ausdrücklich ausgeschlossen.

The bilingual variants reused the master design and changed only the text and
the minimum necessary spacing:

- German first: `STOLZ UND VORURTEIL`, `PRIDE AND PREJUDICE`,
  `Vollständig zweisprachig · Deutsch zuerst`, `JANE AUSTEN`
- English first: `PRIDE AND PREJUDICE`, `STOLZ UND VORURTEIL`,
  `Fully bilingual · English first`, `JANE AUSTEN`

Die zweisprachigen Varianten übernehmen die Hauptgestaltung und ändern
ausschließlich den Text sowie die dafür unbedingt erforderlichen Abstände.

The Easy German prompt used the modern German cover only as a visual-family
reference. It requested a new, calmer late-19th-century clothbinding design
with warm ivory cloth, high-contrast dark green type, muted gold botanical
linework, a generous central oval, and mirrored books and quills. The exact
required text was `STOLZ UND VORURTEIL`, `In Einfachem Deutsch`, and
`JANE AUSTEN`; extra wording, misspellings, publisher marks, watermarks,
photorealism, and mockup perspective were prohibited.

Für den Umschlag in Einfachem Deutsch diente der moderne deutsche Umschlag nur
als Referenz für die gemeinsame Gestaltungsfamilie. Verlangt wurde ein neuer,
ruhigerer Bucheinband im Stil des späten 19. Jahrhunderts: warmes
elfenbeinfarbenes Leinen, kontrastreiche dunkelgrüne Schrift, gedämpfte goldene
Pflanzenlinien, ein großzügiges zentrales Oval sowie gespiegelte Bücher und
Schreibfedern. Der exakte Text lautete `STOLZ UND VORURTEIL`,
`In Einfachem Deutsch` und `JANE AUSTEN`. Zusätzliche Wörter, Schreibfehler,
Verlagszeichen, Wasserzeichen, Fotorealismus und eine Buchattrappen-Perspektive
waren ausgeschlossen.
