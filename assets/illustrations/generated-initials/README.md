# Neu erzeugte Initialbuchstaben

Dieser Ordner enthält drei neu erzeugte dekorative Initialen für Buchstaben,
die unter den historischen Initialbildern der englischen Ausgabe nicht
vorkommen:

- `initial-f.png` für Kapitel LXI: »Für all ihre …«
- `initial-u.png` für Kapitel VIII: »Um fünf Uhr …«
- `initial-z.png` für Kapitel XLIX: »Zwei Tage …«

Die Bilder sind **keine historischen Arbeiten von Hugh Thomson**. Sie wurden
am 25. Juli 2026 mit OpenAIs eingebautem Bildgenerator neu erzeugt. Fünf
Initialen aus der George-Allen-Ausgabe von 1894 dienten ausschließlich als
Stilreferenzen.

Die Arbeitsausgaben wurden auf den technischen Aufbau der historischen
Initialbilder gebracht: 100 Pixel Breite, weißer Hintergrund und indizierte
16-stufige Graustufen-PNGs. Die Höhen ergeben sich aus dem jeweiligen Motiv:

- `F`: 100 × 140 Pixel
- `U`: 100 × 110 Pixel
- `Z`: 100 × 119 Pixel

## Erzeugungsprompt

Für jeden Buchstaben wurde derselbe Prompt mit dem jeweils eingesetzten
Großbuchstaben verwendet:

> Use case: historical-scene  
> Asset type: decorative chapter-opening initial for a book  
> Input images: Images 1–5 are style references only from Hugh Thomson's 1894 illustrated Pride and Prejudice; do not copy a specific figure or composition.  
> Primary request: create one ornamental uppercase letter `{LETTER}` in precisely the same visual tradition as the references.  
> Subject: a clearly legible, dominant capital `{LETTER}` drawn as an elegant Victorian display initial; integrate one very small, tasteful Regency-era human figure into the negative space or baseline of the letter, as the references do.  
> Style/medium: 1890s British black-and-white pen-and-ink line engraving, delicate varied line weight, sparse cross-hatching, playful book-illustration miniature, aged print character without artificial distress.  
> Composition/framing: one isolated upright capital `{LETTER}`, centered, compact near-square or slightly tall crop, generous white margin; the `{LETTER}` must remain unmistakable at 100-pixel width.  
> Color palette: pure white background, black and soft-gray ink only.  
> Text (verbatim): `"{LETTER}"`  
> Constraints: render exactly one uppercase `{LETTER}` and no other letters, words, punctuation, numerals, borders, captions, signatures, logos, or watermark; flat white paper background; crisp clean silhouette; no shadows, color, paper texture, or scene backdrop; preserve the letter as the main shape.
