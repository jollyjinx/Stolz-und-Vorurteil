#!/usr/bin/env python3
"""Import Hugh Thomson's 1894 illustrations from the supplied EPUB.

The generated manifest records the original location of each illustration as
the number of the preceding prose paragraph.  This keeps the translated
chapter Markdown text-only while allowing the build to place each image at the
same point in the German edition.
"""

from __future__ import annotations

import argparse
import json
import re
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ILLUSTRATIONS = ROOT / "illustrations"
MANIFEST = ILLUSTRATIONS / "manifest.json"
EPUB_MEMBERS = [
    f"OEBPS/4736806169548129032_1342-h-{part}.htm.xhtml"
    for part in range(6)
]
CHAPTER_ID = re.compile(r"^(?:Chapter_I|CHAPTER_[IVXLCDM]+)$")
COPYRIGHT = re.compile(r"^\[\s*Copyright\b", re.IGNORECASE)

# Captions are rendered as German text below the unmodified public-domain
# artwork.  Quoted fragments retain the book's German guillemet convention.
GERMAN_CAPTIONS: dict[str, str] = {
    "A note for Miss Bennet.": "»Eine Nachricht für Miss Bennet.«",
    "Accompanied by their aunt": "»In Begleitung ihrer Tante«",
    "After a short survey": "»Nach kurzer Besichtigung«",
    "At the door.": "»An der Tür«",
    "But now it comes out.": "»Aber jetzt kommt es heraus.«",
    "But perhaps you would like to read it": "»Aber vielleicht möchten Sie ihn lesen.«",
    "Cheerful prognostics": "»Frohe Vorhersagen«",
    "Conjecturing as to the date.": "»Sie rätselten über den Zeitpunkt.«",
    "Covering a screen.": "»Einen Wandschirm bespannen«",
    "Dawson": "Dawson",
    "Engaged by the river.": "»Am Fluss beschäftigt«",
    "He came down to see the place": "»Er kam her, um sich das Anwesen anzusehen.«",
    "He rode a black horse.": "»Er ritt ein schwarzes Pferd.«",
    "Hearing herself called.": "»Als sie ihren Namen rufen hörte«",
    "His parting obeisance.": "»Seine Abschiedsverbeugung«",
    "How nicely we are crammed in.": "»Wie schön eng wir zusammengedrängt sind!«",
    "I am determined never to speak of it again": "»Ich habe beschlossen, mit niemandem mehr darüber zu sprechen.«",
    "I am sure she did not listen.": "»Ich bin sicher, sie hat nicht zugehört.«",
    "I have not an instant to lose": "»Ich darf keinen Augenblick verlieren.«",
    "I hope Mr. Bingley will like it.": "»Ich hoffe, Mr. Bingley wird er gefallen.«",
    "In Conversation with the ladies": "»Im Gespräch mit den Damen«",
    "I’m the tallest": "»Ich bin die Größte.«",
    "Jane happened to look round.": "»Jane sah zufällig zurück.«",
    "Lady Catherine, said she, you have given me a treasure.": "»Lady Catherine«, sagte sie, »Sie haben mir einen Schatz geschenkt.«",
    "Lizzy, my dear, I want to speak to you.": "»Lizzy, meine Liebe, ich möchte mit dir sprechen.«",
    "Meeting accidentally in Town": "»Eine zufällige Begegnung in der Stadt«",
    "Mr. & Mrs. Bennet": "Mr. und Mrs. Bennet",
    "Mr. Darcy with him.": "»Mr. Darcy ist bei ihm.«",
    "Mrs Bennet and her two youngest girls.": "Mrs. Bennet und ihre beiden jüngsten Töchter",
    "Mrs. Long and her nieces.": "Mrs. Long und ihre Nichten",
    "No, no; stay where you are": "»Nein, nein; bleiben Sie, wo Sie sind.«",
    "Offended two or three young ladies": "»Er beleidigte zwei oder drei junge Damen.«",
    "On looking up.": "»Als sie aufblickte«",
    "On the Stairs.": "»Auf der Treppe«",
    "Piling up the fire.": "»Das Feuer schüren«",
    "Protested he must be entirely mistaken.": "»Sie beteuerte, er müsse sich vollkommen irren.«",
    "Protested that he never read novels": "»Er erklärte entschuldigend, er lese niemals Romane.«",
    "Reading Jane’s Letters. Chap 34.": "Beim Lesen von Janes Briefen. Kapitel XXXIV.",
    "She is tolerable": "»Sie ist passabel.«",
    "So much love and eloquence": "»So viel Liebe und Beredsamkeit«",
    "Such very superior dancing is not often seen.": "»Solch ausgezeichnetes Tanzen sieht man nicht oft.«",
    "Tenderly flirting": "»Zärtlich flirten«",
    "The Apothecary came": "»Der Apotheker kam.«",
    "The Post.": "Die Post",
    "The arrival of the Gardiners.": "Die Ankunft der Gardiners",
    "The efforts of his aunt.": "»Die Bemühungen seiner Tante«",
    "The elevation of his feelings.": "»Die Höhe seiner Empfindungen«",
    "The entreaties of several": "»Die Bitten mehrerer Personen«",
    "The first pleasing earnest of their welcome.": "»Das erste erfreuliche Zeichen ihres Willkommens«",
    "The gentlemen accompanied him.": "»Die Herren begleiteten ihn.«",
    "The obsequious civility.": "»Die unterwürfige Höflichkeit«",
    "The officers of the ——shire": "»Die Offiziere des ——shire-Regiments«",
    "The spiteful old ladies.": "»Die gehässigen alten Damen«",
    "They had forgotten to leave any message": "»Sie hatten vergessen, eine Nachricht zu hinterlassen.«",
    "To make herself agreeable to all": "»Sie wollte allen angenehm sein.«",
    "To whom I have related the affair": "»Dem ich die Angelegenheit erzählt habe«",
    "Unable to utter a syllable.": "»Unfähig, auch nur eine Silbe hervorzubringen«",
    "Walked back with them": "»Er ging mit ihnen zurück.«",
    "When Colonel Miller’s regiment went.": "»Als Colonel Millers Regiment abzog«",
    "When the Party entered": "»Als die Gesellschaft eintrat«",
    "Whenever she spoke in a low voice": "»Wann immer sie leise sprach«",
    "Will you come and see me.": "»Werden Sie mich besuchen kommen?«",
    "With an affectionate smile.": "»Mit einem liebevollen Lächeln«",
    "Without once opening his lips": "»Ohne auch nur einmal den Mund zu öffnen«",
    "delighted to see their dear friend again.": "»Hocherfreut, ihren lieben Freund wiederzusehen«",
    "he never failed to inform them": "»Er versäumte nie, sie darüber zu informieren.«",
    "they entered the breakfast room": "»Sie betraten das Frühstückszimmer.«",
    "to assure you in the most animated language.": "»Ihnen mit den lebhaftesten Worten zu versichern«",
}


def local_name(element) -> str:
    return element.tag.rsplit("}", 1)[-1]


def has_class(element, class_name: str) -> bool:
    return class_name in element.get("class", "").split()


def readable_text(element, *, exclude_images: bool = False) -> str:
    """Return text without EPUB page markers, copyright lines, or images."""
    parts: list[str] = []

    def visit(node) -> None:
        if has_class(node, "x-ebookmaker-pageno"):
            return
        if exclude_images and local_name(node) == "img":
            return
        if local_name(node) == "p":
            raw = re.sub(r"\s+", " ", "".join(node.itertext())).strip()
            if COPYRIGHT.match(raw):
                return
        if node.text:
            parts.append(node.text)
        for child in node:
            visit(child)
            if child.tail:
                parts.append(child.tail)

    visit(element)
    text = re.sub(r"\s+", " ", "".join(parts)).strip()
    text = re.sub(r"\s*\[\s*Copyright\b.*?\]\s*", " ", text, flags=re.IGNORECASE)
    text = re.sub(
        r"\s+H\.?\s*T\.?\s*(?:Feb(?:ruary)?\.?\s*)?94\s*$",
        "",
        text,
        flags=re.IGNORECASE,
    )
    return re.sub(r"\s+", " ", text).strip().strip("“”\" ")


def image_caption(image, container) -> str | None:
    captions = [node for node in container.iter() if has_class(node, "caption")]
    if captions:
        caption = readable_text(captions[0])
        return caption or None
    alt = re.sub(r"\s+", " ", image.get("alt", "")).strip().strip("[] ")
    return alt or None


def illustration_entry(
    image,
    chapter: int,
    after_paragraph: int,
    kind: str,
    container,
) -> dict[str, object] | None:
    filename = Path(image.get("src", "")).name
    if not filename.lower().endswith(".jpg"):
        return None
    caption_en = image_caption(image, container)
    return {
        "chapter": chapter,
        "after_paragraph": after_paragraph,
        "kind": kind,
        "image": filename,
        "caption_en": caption_en,
        "caption_de": GERMAN_CAPTIONS.get(caption_en) if caption_en else None,
    }


def collect(epub_path: Path) -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    chapter_number = 0
    paragraph_number = 0

    with zipfile.ZipFile(epub_path) as epub:
        front_document = ET.fromstring(epub.read(EPUB_MEMBERS[0]))
        source_frontispieces = [
            node
            for node in front_document.iter()
            if local_name(node) == "img" and "_i_003.jpg" in node.get("src", "")
        ]
        if len(source_frontispieces) != 1:
            raise RuntimeError("Expected exactly one source frontispiece.")
        jane_letters_illustration = illustration_entry(
            source_frontispieces[0],
            chapter=34,
            after_paragraph=1,
            kind="inline",
            container=source_frontispieces[0],
        )
        assert jane_letters_illustration is not None
        entries.append(jane_letters_illustration)

        for member in EPUB_MEMBERS:
            document = ET.fromstring(epub.read(member))
            body = next(
                node for node in document.iter() if local_name(node) == "body"
            )
            for node in body:
                ids = [
                    descendant.get("id", "")
                    for descendant in node.iter()
                    if descendant.get("id")
                ]
                is_chapter_heading = (
                    local_name(node) == "h2"
                    and any(CHAPTER_ID.match(value) for value in ids)
                )
                if is_chapter_heading:
                    chapter_number += 1
                    paragraph_number = 0
                    kind = "chapter-heading"
                elif chapter_number:
                    kind = "inline"
                else:
                    continue

                for image in (
                    descendant
                    for descendant in node.iter()
                    if local_name(descendant) == "img"
                ):
                    entry = illustration_entry(
                        image,
                        chapter=chapter_number,
                        after_paragraph=paragraph_number,
                        kind=kind,
                        container=node,
                    )
                    if entry:
                        entries.append(entry)

                if not is_chapter_heading and local_name(node) in {"p", "blockquote"}:
                    paragraph = readable_text(node, exclude_images=True)
                    if paragraph and not COPYRIGHT.match(paragraph):
                        paragraph_number += 1

    if chapter_number != 61:
        raise RuntimeError(f"Expected 61 chapters, found {chapter_number}.")
    return sorted(
        entries,
        key=lambda entry: (
            int(entry["chapter"]),
            int(entry["after_paragraph"]),
        ),
    )


def import_files(epub_path: Path, entries: list[dict[str, object]]) -> None:
    missing = sorted(
        {
            str(entry["caption_en"])
            for entry in entries
            if entry["caption_en"] and not entry["caption_de"]
        }
    )
    if missing:
        print("Missing German captions:")
        for caption in missing:
            print(f"- {caption}")
        raise SystemExit(1)

    ILLUSTRATIONS.mkdir(exist_ok=True)
    with zipfile.ZipFile(epub_path) as epub:
        for filename in sorted({str(entry["image"]) for entry in entries}):
            member = f"OEBPS/{filename}"
            (ILLUSTRATIONS / filename).write_bytes(epub.read(member))
    MANIFEST.write_text(
        json.dumps(entries, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("epub", type=Path)
    parser.add_argument(
        "--inspect",
        action="store_true",
        help="print the collected manifest without copying files",
    )
    args = parser.parse_args()
    entries = collect(args.epub)
    if args.inspect:
        print(json.dumps(entries, ensure_ascii=False, indent=2))
    else:
        import_files(args.epub, entries)
        print(f"Imported {len(entries)} illustrations into {ILLUSTRATIONS}.")


if __name__ == "__main__":
    main()
