#!/usr/bin/env python3
"""Build English and German EPUB, HTML, and PDF editions from chapter Markdown."""

from __future__ import annotations

import argparse
import html
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
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
CSS = ROOT / "book.css"

EDITIONS = {
    "german": {
        "chapters": ROOT / "modern-german-chapters",
        "frontmatter": ROOT / "frontmatter" / "german.md",
        "basename": "Stolz-und-Vorurteil-modernes-Deutsch",
        "title": "Stolz und Vorurteil",
        "subtitle": "Eine moderne deutsche Übersetzung",
        "author": "Jane Austen",
        "translator": "ChatGPT, mit Hilfe von Patrick Stein",
        "dedication": "Für meine Eltern Brigitte und Wolfgang, damit Ihr Euch auch dran erfreuen könnt",
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


def build_markdown(edition: dict[str, object]) -> Path:
    chapter_dir = edition["chapters"]
    assert isinstance(chapter_dir, Path)
    output = DIST / f"{edition['basename']}.md"
    parts = [Path(edition["frontmatter"]).read_text(encoding="utf-8").rstrip()]
    parts.extend(path.read_text(encoding="utf-8").rstrip() for path in chapter_files(chapter_dir))
    output.write_text("\n\n".join(parts) + "\n", encoding="utf-8")
    return output


def build_pandoc(markdown: Path, edition: dict[str, object]) -> None:
    basename = str(edition["basename"])
    common = [
        "pandoc", str(markdown), "--standalone", "--toc", "--toc-depth=1",
        "--css", str(CSS), "--metadata", f"title={edition['title']}",
        "--metadata", f"author={edition['author']}", "--metadata", f"lang={edition['language']}",
    ]
    translator = edition.get("translator")
    if translator:
        common += ["--metadata", f"translator={translator}"]
    run(common + ["--to=html5", "--output", str(DIST / f"{basename}.html")])
    run(common + ["--to=epub3", "--output", str(DIST / f"{basename}.epub")])


def inline_markdown(text: str) -> str:
    escaped = html.escape(text)
    return re.sub(r"\*([^*]+)\*", r"<i>\1</i>", escaped)


def page_number(canvas, document) -> None:
    if document.page > 1:
        canvas.setFont("Times-Roman", 9)
        canvas.setFillColor(HexColor("#5e4530"))
        canvas.drawCentredString(A5[0] / 2, 12 * mm, str(document.page - 1))


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

    story = [Paragraph(str(edition["title"]), title), Paragraph(str(edition["subtitle"]), subtitle)]
    story.append(Paragraph(f"Von {edition['author']}", credit))
    if edition.get("translator"):
        story.append(Paragraph(f"Deutsche Übersetzung: {edition['translator']}", credit))
    if edition.get("dedication"):
        story.extend([Spacer(1, 24), Paragraph(str(edition["dedication"]), credit)])
    story.append(PageBreak())

    chapter_dir = edition["chapters"]
    assert isinstance(chapter_dir, Path)
    chapters = chapter_files(chapter_dir)
    for chapter_index, chapter in enumerate(chapters):
        blocks = [block.strip() for block in chapter.read_text(encoding="utf-8").split("\n\n") if block.strip()]
        story.append(Paragraph(inline_markdown(blocks[0].removeprefix("# ")), heading))
        for block in blocks[1:]:
            story.append(Paragraph(inline_markdown(block), body))
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
