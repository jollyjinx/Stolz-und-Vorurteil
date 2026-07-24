#!/usr/bin/env python3
"""Build English and German EPUB, HTML, and PDF editions from chapter Markdown."""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A5
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Image as ReportLabImage,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
CSS = ROOT / "book.css"
ILLUSTRATIONS = ROOT / "illustrations"
ILLUSTRATION_MANIFEST = ILLUSTRATIONS / "manifest.json"

EDITIONS = {
    "german": {
        "chapters": ROOT / "modern-german-chapters",
        "frontmatter": ROOT / "frontmatter" / "german.md",
        "basename": "Stolz-und-Vorurteil-modernes-Deutsch",
        "title": "Stolz und Vorurteil",
        "subtitle": "Eine moderne deutsche Übersetzung",
        "author": "Jane Austen",
        "translator": "ChatGPT, mit Hilfe von Patrick Stein",
        "illustrator": "Hugh Thomson",
        "illustrations": True,
        "dedication": "Für meine Eltern Brigitte und Wolfgang, damit Ihr Euch auch dran erfreuen könnt",
        "download_url": "https://github.com/jollyjinx/Stolz-und-Vorurteil/releases",
        "license_name": "MIT License",
        "license_url": "https://github.com/jollyjinx/Stolz-und-Vorurteil/blob/main/LICENSE",
        "language": "de-DE",
    },
    "english": {
        "chapters": ROOT / "source-chapters",
        "frontmatter": ROOT / "frontmatter" / "english.md",
        "basename": "Pride-and-Prejudice-English",
        "title": "Pride and Prejudice",
        "subtitle": "The supplied Project Gutenberg source edition",
        "author": "Jane Austen",
        "translator": None,
        "dedication": None,
        "language": "en-US",
    },
}


def run(command: list[str]) -> None:
    print("+", " ".join(command))
    subprocess.run(command, cwd=ROOT, check=True)


def chapter_files(directory: Path) -> list[Path]:
    files = sorted(directory.glob("*.md"))
    if len(files) != 61:
        raise RuntimeError(f"Expected 61 chapters in {directory}, found {len(files)}.")
    return files


def load_illustrations() -> list[dict[str, object]]:
    if not ILLUSTRATION_MANIFEST.exists():
        raise RuntimeError(
            f"Illustration manifest is missing: {ILLUSTRATION_MANIFEST}"
        )
    entries = json.loads(ILLUSTRATION_MANIFEST.read_text(encoding="utf-8"))
    if not isinstance(entries, list):
        raise RuntimeError("Illustration manifest must contain a JSON list.")
    for entry in entries:
        image = ILLUSTRATIONS / str(entry["image"])
        if not image.exists():
            raise RuntimeError(f"Illustration is missing: {image}")
    return entries


def markdown_illustration(entry: dict[str, object]) -> str:
    caption = str(entry.get("caption_de") or "")
    path = f"illustrations/{entry['image']}"
    return f"![{caption}]({path}){{.book-illustration}}"


def illustrated_chapter_markdown(
    chapter: Path,
    chapter_number: int,
    illustrations: list[dict[str, object]],
) -> str:
    blocks = [
        block.strip()
        for block in chapter.read_text(encoding="utf-8").split("\n\n")
        if block.strip()
    ]
    body = blocks[1:]
    by_position: dict[int, list[dict[str, object]]] = {}
    for entry in illustrations:
        if int(entry["chapter"]) != chapter_number:
            continue
        position = int(entry["after_paragraph"])
        if position > len(body):
            raise RuntimeError(
                f"Illustration {entry['image']} follows paragraph {position}, "
                f"but {chapter.name} has only {len(body)} paragraphs."
            )
        by_position.setdefault(position, []).append(entry)

    output = [blocks[0]]
    output.extend(markdown_illustration(entry) for entry in by_position.get(0, []))
    for position, paragraph in enumerate(body, start=1):
        output.append(paragraph)
        output.extend(
            markdown_illustration(entry)
            for entry in by_position.get(position, [])
        )
    return "\n\n".join(output)


def build_markdown(edition: dict[str, object]) -> Path:
    chapter_dir = edition["chapters"]
    assert isinstance(chapter_dir, Path)
    output = DIST / f"{edition['basename']}.md"
    parts = [Path(edition["frontmatter"]).read_text(encoding="utf-8").rstrip()]
    chapters = chapter_files(chapter_dir)
    if edition.get("illustrations"):
        illustrations = load_illustrations()
        frontispieces = [
            entry for entry in illustrations if int(entry["chapter"]) == 0
        ]
        if len(frontispieces) != 1:
            raise RuntimeError("Expected exactly one frontispiece.")
        parts.append(markdown_illustration(frontispieces[0]))
        parts.extend(
            illustrated_chapter_markdown(path, number, illustrations)
            for number, path in enumerate(chapters, start=1)
        )
    else:
        parts.extend(path.read_text(encoding="utf-8").rstrip() for path in chapters)
    output.write_text("\n\n".join(parts) + "\n", encoding="utf-8")
    return output


def build_pandoc(markdown: Path, edition: dict[str, object]) -> None:
    basename = str(edition["basename"])
    common = [
        "pandoc", str(markdown), "--standalone", "--toc", "--toc-depth=1",
        "--css", str(CSS), "--metadata", f"title={edition['title']}",
        "--metadata", f"author={edition['author']}", "--metadata", f"lang={edition['language']}",
        "--resource-path", str(ROOT),
    ]
    translator = edition.get("translator")
    if translator:
        common += ["--metadata", f"translator={translator}"]
    illustrator = edition.get("illustrator")
    if illustrator:
        common += [
            "--metadata", f"illustrator={illustrator}",
            "--metadata", f"contributor={illustrator}",
        ]
    run(common + [
        "--self-contained", "--to=html5",
        "--output", str(DIST / f"{basename}.html"),
    ])
    run(common + ["--to=epub3", "--output", str(DIST / f"{basename}.epub")])


def inline_markdown(text: str) -> str:
    escaped = html.escape(text)
    return re.sub(r"\*([^*]+)\*", r"<i>\1</i>", escaped)


def page_number(canvas, document) -> None:
    if document.page > 1:
        canvas.setFont("Times-Roman", 9)
        canvas.setFillColor(HexColor("#5e4530"))
        canvas.drawCentredString(A5[0] / 2, 12 * mm, str(document.page - 1))


def pdf_illustration(
    entry: dict[str, object],
    caption_style: ParagraphStyle,
    *,
    max_height: float = 125 * mm,
) -> KeepTogether:
    image_path = ILLUSTRATIONS / str(entry["image"])
    image = ReportLabImage(str(image_path))
    scale = min(
        (112 * mm) / image.imageWidth,
        max_height / image.imageHeight,
        1.0,
    )
    image.drawWidth = image.imageWidth * scale
    image.drawHeight = image.imageHeight * scale
    image.hAlign = "CENTER"
    flowables = [Spacer(1, 4 * mm), image]
    caption = entry.get("caption_de")
    if caption:
        flowables.append(Paragraph(html.escape(str(caption)), caption_style))
    flowables.append(Spacer(1, 4 * mm))
    return KeepTogether(flowables)


def build_pdf(edition: dict[str, object]) -> None:
    basename = str(edition["basename"])
    output = DIST / f"{basename}.pdf"
    document = SimpleDocTemplate(
        str(output), pagesize=A5, rightMargin=18 * mm, leftMargin=18 * mm,
        topMargin=20 * mm, bottomMargin=20 * mm,
        title=str(edition["title"]), author=str(edition["author"]),
    )
    styles = getSampleStyleSheet()
    title = ParagraphStyle("BookTitle", parent=styles["Title"], fontName="Times-Bold", fontSize=26,
                           leading=32, textColor=HexColor("#372b20"), alignment=TA_CENTER, spaceAfter=14)
    subtitle = ParagraphStyle("BookSubtitle", parent=styles["Normal"], fontName="Times-Italic", fontSize=14,
                              leading=20, alignment=TA_CENTER, textColor=HexColor("#5e4530"), spaceAfter=42)
    credit = ParagraphStyle("Credit", parent=styles["Normal"], fontName="Times-Roman", fontSize=10.5,
                            leading=16, alignment=TA_CENTER, spaceAfter=12)
    heading = ParagraphStyle("Chapter", parent=styles["Heading1"], fontName="Times-Bold", fontSize=17,
                             leading=23, textColor=HexColor("#372b20"), spaceBefore=2, spaceAfter=18)
    body = ParagraphStyle("Body", parent=styles["BodyText"], fontName="Times-Roman", fontSize=10.5,
                          leading=15, alignment=TA_JUSTIFY, spaceAfter=10)
    caption = ParagraphStyle("IllustrationCaption", parent=styles["Normal"], fontName="Times-Italic",
                             fontSize=9.5, leading=13, alignment=TA_CENTER,
                             textColor=HexColor("#5e4530"), spaceBefore=7, spaceAfter=2)

    story = [Paragraph(str(edition["title"]), title), Paragraph(str(edition["subtitle"]), subtitle)]
    story.append(Paragraph(f"Von {edition['author']}", credit))
    if edition.get("translator"):
        story.append(Paragraph(f"Deutsche Übersetzung: {edition['translator']}", credit))
    if edition.get("illustrator"):
        story.append(Paragraph(f"Illustrationen: {edition['illustrator']} (1894)", credit))
    if edition.get("dedication"):
        story.extend([Spacer(1, 24), Paragraph(str(edition["dedication"]), credit)])
    if edition.get("download_url"):
        download_url = html.escape(str(edition["download_url"]), quote=True)
        story.extend([
            Spacer(1, 12),
            Paragraph(f'Kostenloser Download:<br/><link href="{download_url}">{download_url}</link>', credit),
        ])
    if edition.get("license_name") and edition.get("license_url"):
        license_name = html.escape(str(edition["license_name"]))
        license_url = html.escape(str(edition["license_url"]), quote=True)
        story.append(Paragraph(f'Lizenz: <link href="{license_url}">{license_name}</link>', credit))
    story.append(PageBreak())

    illustrations = load_illustrations() if edition.get("illustrations") else []
    if illustrations:
        frontispieces = [
            entry for entry in illustrations if int(entry["chapter"]) == 0
        ]
        if len(frontispieces) != 1:
            raise RuntimeError("Expected exactly one frontispiece.")
        story.append(
            pdf_illustration(
                frontispieces[0],
                caption,
                max_height=142 * mm,
            )
        )
        story.append(PageBreak())

    chapter_dir = edition["chapters"]
    assert isinstance(chapter_dir, Path)
    chapters = chapter_files(chapter_dir)
    for chapter_index, chapter in enumerate(chapters):
        blocks = [block.strip() for block in chapter.read_text(encoding="utf-8").split("\n\n") if block.strip()]
        chapter_illustrations = [
            entry
            for entry in illustrations
            if int(entry["chapter"]) == chapter_index + 1
        ]
        by_position: dict[int, list[dict[str, object]]] = {}
        for entry in chapter_illustrations:
            position = int(entry["after_paragraph"])
            if position > len(blocks) - 1:
                raise RuntimeError(
                    f"Illustration {entry['image']} follows paragraph {position}, "
                    f"but {chapter.name} has only {len(blocks) - 1} paragraphs."
                )
            by_position.setdefault(position, []).append(entry)

        story.append(Paragraph(inline_markdown(blocks[0].removeprefix("# ")), heading))
        story.extend(
            pdf_illustration(entry, caption)
            for entry in by_position.get(0, [])
        )
        for position, block in enumerate(blocks[1:], start=1):
            story.append(Paragraph(inline_markdown(block), body))
            story.extend(
                pdf_illustration(entry, caption)
                for entry in by_position.get(position, [])
            )
        if chapter_index != len(chapters) - 1:
            story.append(PageBreak())
    document.build(story, onFirstPage=page_number, onLaterPages=page_number)


def build(edition_name: str) -> None:
    edition = EDITIONS[edition_name]
    markdown = build_markdown(edition)
    build_pandoc(markdown, edition)
    build_pdf(edition)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("edition", choices=["german", "english", "all"], default="all", nargs="?")
    args = parser.parse_args()
    if shutil.which("pandoc") is None:
        raise SystemExit("pandoc is required; install it and rerun this command.")
    DIST.mkdir(exist_ok=True)
    for edition_name in (EDITIONS if args.edition == "all" else [args.edition]):
        build(edition_name)


if __name__ == "__main__":
    main()
