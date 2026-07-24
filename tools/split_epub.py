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
    """Return the readable paragraph text, retaining simple emphasis."""
    for page_number in element.xpath('.//*[contains(@class, "x-ebookmaker-pageno")]'):
        page_number.drop_tree()
    for image in element.xpath('.//img'):
        image.drop_tree()
    text = "".join(element.itertext())
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract(epub_path: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    chapter_number = 0

    with zipfile.ZipFile(epub_path) as epub:
        for member in EPUB_MEMBERS:
            document = html.fromstring(epub.read(member))
            headings = []
            for heading in document.xpath("//h2"):
                ids = heading.xpath(".//@id")
                if any(CHAPTER_ID.match(value) for value in ids):
                    headings.append(heading)

            for index, heading in enumerate(headings):
                chapter_number += 1
                next_heading = headings[index + 1] if index + 1 < len(headings) else None
                parts = []
                node = heading
                while True:
                    node = node.getnext()
                    if node is None or node is next_heading:
                        break
                    if node.tag in {"p", "blockquote"}:
                        paragraph = markdown_for(node)
                        if paragraph and not paragraph.startswith("[Copyright"):
                            parts.append(paragraph)

                roman = re.search(r"CHAPTER\s+([IVXLCDM]+)|Chapter\s+([IVXLCDM]+)", " ".join(heading.itertext()))
                numeral = next(group for group in roman.groups() if group) if roman else str(chapter_number)
                content = f"# Chapter {numeral}\n\n" + "\n\n".join(parts) + "\n"
                (output_dir / f"{chapter_number:02d}-chapter-{numeral.lower()}.md").write_text(
                    content, encoding="utf-8"
                )

    if chapter_number != 61:
        raise RuntimeError(f"Expected 61 chapters, extracted {chapter_number}.")


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: split_epub.py INPUT.epub OUTPUT_DIRECTORY")
    extract(Path(sys.argv[1]), Path(sys.argv[2]))


if __name__ == "__main__":
    main()
