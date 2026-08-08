# Editions / Ausgaben

Each direct child directory represents one public edition or one derived
edition definition. Edition IDs use lowercase ASCII words separated by
hyphens and match the command accepted by `tools/build_book.py`.

Jedes direkte Unterverzeichnis beschreibt eine öffentliche Ausgabe oder die
Definition einer abgeleiteten Ausgabe. Ausgaben-IDs bestehen aus
kleingeschriebenen ASCII-Wörtern mit Bindestrichen und entsprechen dem Befehl
für `tools/build_book.py`.

| Edition ID | Content / Inhalt | Kind / Art |
|---|---|---|
| `english` | Project Gutenberg English reference | independent / eigenständig |
| `modern-german` | modern German translation | independent / eigenständig |
| `easy-german` | accessible Easy German translation | independent / eigenständig |
| `easy-english` | accessible Easy English adaptation | independent / eigenständig |
| `german-english` | German-first paragraph pairs | derived / abgeleitet |
| `english-german` | English-first paragraph pairs | derived / abgeleitet |

An independent edition normally owns `chapters/` and `frontmatter.md`. Optional
edition-local files are `introduction.md`, `glossary.json`, `notes.json`,
`alignment-manifest.json`, and `GUIDANCE.md`. A derived edition owns only the
metadata and front matter that differ; its chapter inputs are declared in the
builder.

Eine eigenständige Ausgabe besitzt gewöhnlich `chapters/` und
`frontmatter.md`. Optionale ausgabenspezifische Dateien sind
`introduction.md`, `glossary.json`, `notes.json`, `alignment-manifest.json` und
`GUIDANCE.md`. Eine abgeleitete Ausgabe besitzt nur abweichende Metadaten und
Titelei; ihre Kapitelquellen werden im Buchbau angegeben.

See [Adding an edition](../docs/ADDING_AN_EDITION.md) for the complete
checklist. / Die vollständige Checkliste steht unter
[Neue Ausgabe hinzufügen](../docs/ADDING_AN_EDITION.md).
