#!/usr/bin/env python3
"""Extract the 61 prose chapters from the supplied Project Gutenberg EPUB."""

from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path

from lxml import html


EPUB_MEMBERS = [
    f"OEBPS/4736806169548129032_1342-h-{part}.htm.xhtml"
    for part in range(6)
]
CHAPTER_ID = re.compile(r"^(?:Chapter_I|CHAPTER_[IVXLCDM]+)$")


def markdown_for(element) -> str:
    """Return readable paragraph text, including image-based initials."""
    for page_number in element.xpath('.//*[contains(@class, "x-ebookmaker-pageno")]'):
        page_number.drop_tree()
    for figure in element.xpath(
        './/*[contains(concat(" ", normalize-space(@class), " "), " figcenter ")]'
    ):
        figure.drop_tree()
    for image in element.xpath('.//img'):
        # Chapter initials are images whose alt text is the opening letter.
        # Convert them to inline text instead of silently deleting the letter.
        image.tag = "span"
        image.text = image.get("alt", "")
        image.attrib.clear()
    text = "".join(element.itertext())
    text = re.sub(r"\s+", " ", text).strip()
    return text


def is_chapter_heading(element) -> bool:
    if element.tag != "h2":
        return False
    return any(
        CHAPTER_ID.match(value)
        for value in element.xpath(".//@id")
    )


def append_paragraph(parts: list[str], paragraph: str) -> None:
    """Append prose, rejoining paragraphs split only by an illustration."""
    if (
        parts
        and parts[-1][-1].isalnum()
        and paragraph[0].islower()
    ):
        parts[-1] += f" {paragraph}"
    else:
        parts.append(paragraph)


def extract(epub_path: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    chapters: list[tuple[str, list[str]]] = []
    current_parts: list[str] | None = None

    with zipfile.ZipFile(epub_path) as epub:
        for member in EPUB_MEMBERS:
            document = html.fromstring(epub.read(member))
            for node in document.xpath("//body/*"):
                if is_chapter_heading(node):
                    chapter_number = len(chapters) + 1
                    chapter_id = next(
                        value
                        for value in node.xpath(".//@id")
                        if CHAPTER_ID.match(value)
                    )
                    numeral = (
                        "I"
                        if chapter_id == "Chapter_I"
                        else chapter_id.removeprefix("CHAPTER_")
                    )
                    current_parts = []
                    chapters.append((numeral, current_parts))
                    continue

                if current_parts is None:
                    continue

                classes = node.get("class", "").split()
                is_letter = node.tag == "div" and "blockquot" in classes
                if is_letter:
                    for letter_paragraph in node.xpath("./p"):
                        paragraph = markdown_for(letter_paragraph)
                        if paragraph:
                            append_paragraph(current_parts, paragraph)
                    continue

                if node.tag not in {"p", "blockquote"}:
                    continue
                if "fint" in classes:
                    continue

                paragraph = markdown_for(node)
                if paragraph and not paragraph.startswith("[Copyright"):
                    append_paragraph(current_parts, paragraph)

    if len(chapters) != 61:
        raise RuntimeError(f"Expected 61 chapters, extracted {len(chapters)}.")

    for chapter_number, (numeral, parts) in enumerate(chapters, start=1):
        content = f"# Chapter {numeral}\n\n" + "\n\n".join(parts) + "\n"
        (output_dir / f"{chapter_number:02d}-chapter-{numeral.lower()}.md").write_text(
            content, encoding="utf-8"
        )


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: split_epub.py INPUT.epub OUTPUT_DIRECTORY")
    extract(Path(sys.argv[1]), Path(sys.argv[2]))


if __name__ == "__main__":
    main()
