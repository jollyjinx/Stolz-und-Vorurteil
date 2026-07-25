# Illustrationen

Dieser Ordner enthält 97 Zeichnungen und 59 dekorative Initialbuchstaben von Hugh Thomson aus der 1894 bei George Allen erschienenen illustrierten Ausgabe von Jane Austens *Pride and Prejudice*. Sie wurden aus der mitgelieferten Project-Gutenberg-EPUB `pg1342-images-3.epub` übernommen.

`manifest.json` hält für jede Abbildung fest:

- Kapitel und Position nach dem jeweils vorausgehenden Absatz
- Art der Abbildung (Kapitelkopf oder Illustration im Text)
- englische Originalbeschriftung
- deutsche Bildunterschrift

Die historischen Bilddateien bleiben unverändert. Englische Schrift, die Teil einer Zeichnung ist, bleibt deshalb sichtbar; die deutsche Ausgabe ergänzt darunter eine deutsche Bildunterschrift. Das Frontispiz der englischen Ausgabe zeigt eine Szene aus Kapitel XXXIV und wird in der deutschen Ausgabe dort nach dem ersten Absatz eingesetzt.

`initials/` enthält die 59 tatsächlich als Buchstaben gezeichneten historischen Kapitelinitialen und ihr Manifest. Kapitel I verwendet im englischen EPUB nur ein gesetztes `I`; Kapitel XXXVI stellt neben dem ausgeschriebenen Namen `ELIZABETH` ein buchstabenloses Schwertornament, das nicht zum Buchstabenkatalog gehört. Die drei im Originalbestand fehlenden deutschen Initialen `F`, `U` und `Z` liegen als neu erzeugte, ausdrücklich nicht historische Ergänzungen unter `generated-initials/`.

Der Import lässt sich mit folgendem Befehl reproduzieren:

```sh
python3 tools/import_illustrations.py /Users/jolly/Downloads/pg1342-images-3.epub
```
