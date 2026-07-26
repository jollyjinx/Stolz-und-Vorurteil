# Illustrationen

Dieser Ordner enthält 97 Zeichnungen und 59 dekorative Initialbuchstaben von Hugh Thomson aus der 1894 bei George Allen erschienenen illustrierten Ausgabe von Jane Austens *Pride and Prejudice*. Sie wurden aus der mitgelieferten Project-Gutenberg-EPUB `pg1342-images-3.epub` übernommen.

`manifest.json` hält für jede Abbildung fest:

- Kapitel und Position nach dem jeweils vorausgehenden Absatz
- Art der Abbildung (Kapitelkopf oder Illustration im Text)
- englische Originalbeschriftung in `caption_en`
- deutsche Übersetzung in `caption_de`

Von den 97 Abbildungen besitzen 68 ein vollständiges deutsch-englisches
Beschriftungspaar. Der Buchbau bricht ab, wenn nur eine der beiden Sprachen
vorhanden ist.

Die historischen Bilddateien bleiben unverändert. Englische Schrift, die Teil
einer Zeichnung ist, bleibt deshalb sichtbar. Die rein deutsche Ausgabe
ergänzt darunter die deutsche Bildunterschrift. In den beiden zweisprachigen Fassungen
folgen beide Beschriftungen direkt unter dem Bild:

- Deutsch–Englisch: zuerst `caption_de`, danach `caption_en`
- Englisch–Deutsch: zuerst `caption_en`, danach `caption_de`

Für HTML und EPUB erzeugt der Buchbau dafür einen gemeinsamen
`.book-figure`-Block mit einer begrenzten Bildhöhe und unterdrücktem internen
Seitenumbruch. Im PDF bilden Bild und alle Beschriftungen einen gemeinsamen
`KeepTogether`-Block. Dadurch bleiben die Bildunterschriften bei dem Bild, zu
dem sie gehören.

Das Frontispiz der englischen Ausgabe zeigt eine Szene aus Kapitel XXXIV und
wird in den illustrierten Ausgaben dort nach dem ersten Absatz eingesetzt.

`initials/` enthält die 59 tatsächlich als Buchstaben gezeichneten historischen Kapitelinitialen und ihr Manifest. Kapitel I verwendet im englischen EPUB nur ein gesetztes `I`; Kapitel XXXVI stellt neben dem ausgeschriebenen Namen `ELIZABETH` ein buchstabenloses Schwertornament, das nicht zum Buchstabenkatalog gehört. Die drei im Originalbestand fehlenden deutschen Initialen `F`, `U` und `Z` liegen als neu erzeugte, ausdrücklich nicht historische Ergänzungen unter `generated-initials/`.

Der Import lässt sich mit folgendem Befehl reproduzieren:

```sh
python3 tools/import_illustrations.py /Users/jolly/Downloads/pg1342-images-3.epub
```
