# Illustrationen

Dieser Ordner enthält 97 Zeichnungen von Hugh Thomson aus der 1894 bei George Allen erschienenen illustrierten Ausgabe von Jane Austens *Pride and Prejudice*. Sie wurden aus der mitgelieferten Project-Gutenberg-EPUB `pg1342-images-3.epub` übernommen.

`manifest.json` hält für jede Abbildung fest:

- Kapitel und Position nach dem jeweils vorausgehenden Absatz
- Art der Abbildung (Frontispiz, Kapitelkopf oder Illustration im Text)
- englische Originalbeschriftung
- deutsche Bildunterschrift

Die historischen Bilddateien bleiben unverändert. Englische Schrift, die Teil einer Zeichnung ist, bleibt deshalb sichtbar; die deutsche Ausgabe ergänzt darunter eine deutsche Bildunterschrift. Die dekorativen Initialbuchstaben der englischen Ausgabe sind nicht enthalten.

Der Import lässt sich mit folgendem Befehl reproduzieren:

```sh
python3 tools/import_illustrations.py /Users/jolly/Downloads/pg1342-images-3.epub
```
