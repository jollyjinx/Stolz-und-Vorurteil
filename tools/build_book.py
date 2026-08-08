#!/usr/bin/env python3
"""Build modern, Easy German, English, and bilingual book editions."""

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
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import (
    Image as ReportLabImage,
    ImageAndFlowables,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
CSS = ROOT / "book.css"
COVERS = ROOT / "covers"
ILLUSTRATIONS = ROOT / "illustrations"
ILLUSTRATION_MANIFEST = ILLUSTRATIONS / "manifest.json"
EASY_GERMAN_GLOSSARY = ROOT / "easy-german-glossary.json"
EASY_GERMAN_NOTES = ROOT / "easy-german-notes.json"
INITIAL_MANIFESTS = [
    ILLUSTRATIONS / "initials" / "manifest.json",
    ILLUSTRATIONS / "generated-initials" / "manifest.json",
]
OPENING_INITIAL = re.compile(r"^(?P<prefix>[^A-ZÄÖÜ]*)(?P<letter>[A-ZÄÖÜ])(?P<rest>.*)$", re.DOTALL)

COVER_LABELS = {
    "de": {
        "by": "Von",
        "translation": "Deutsche Übersetzung",
        "illustrations": "Illustrationen",
        "download": "Kostenloser Download",
        "license": "Lizenz",
    },
    "en": {
        "by": "By",
        "translation": "German translation",
        "illustrations": "Illustrations",
        "download": "Free download",
        "license": "License",
    },
}

EDITIONS = {
    "german": {
        "chapters": ROOT / "modern-german-chapters",
        "frontmatter": ROOT / "frontmatter" / "german.md",
        "basename": "Stolz-und-Vorurteil-modernes-Deutsch",
        "title": "Stolz und Vorurteil",
        "subtitle": "Eine moderne deutsche Übersetzung",
        "cover": COVERS / "Stolz-und-Vorurteil-modernes-Deutsch.png",
        "author": "Jane Austen",
        "translator": "ChatGPT, mit Hilfe von Patrick Stein",
        "illustrator": "Hugh Thomson",
        "illustrations": True,
        "initials": True,
        "initials_credit": "Dekorative Initialen: Hugh Thomson (1894); F, U und Z ergänzt mit OpenAI (2026)",
        "dedication": "Für meine Eltern Brigitte und Wolfgang, damit Ihr Euch auch dran erfreuen könnt",
        "download_url": "https://github.com/jollyjinx/Stolz-und-Vorurteil/releases",
        "license_name": "MIT License",
        "license_url": "https://github.com/jollyjinx/Stolz-und-Vorurteil/blob/main/LICENSE",
        "language": "de-DE",
    },
    "easy-german": {
        "chapters": ROOT / "easy-german-chapters",
        "frontmatter": ROOT / "frontmatter" / "easy-german.md",
        "introduction": ROOT / "frontmatter" / "easy-german-introduction.md",
        "basename": "Stolz-und-Vorurteil-Einfaches-Deutsch",
        "title": "Stolz und Vorurteil",
        "subtitle": "In Einfachem Deutsch",
        "cover": COVERS / "Stolz-und-Vorurteil-Einfaches-Deutsch.png",
        "author": "Jane Austen",
        "translator": "ChatGPT, mit Hilfe von Patrick Stein",
        "illustrator": "Hugh Thomson",
        "illustrations": True,
        "initials": True,
        "allow_missing_initials": True,
        "notes": True,
        "glossary": True,
        "numeric_chapter_headings": True,
        "initials_credit": "Dekorative Initialen: Hugh Thomson (1894); F, U und Z ergänzt mit OpenAI (2026)",
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
    "german-english": {
        "chapters": ROOT / "modern-german-chapters",
        "paired_chapters": ROOT / "source-chapters",
        "frontmatter": ROOT / "frontmatter" / "bilingual.md",
        "basename": "Stolz-und-Vorurteil-Deutsch-Englisch",
        "title": "Stolz und Vorurteil / Pride and Prejudice",
        "subtitle": "Vollständig zweisprachig: Deutsch zuerst",
        "cover": COVERS / "Stolz-und-Vorurteil-Deutsch-Englisch.png",
        "author": "Jane Austen",
        "translator": "ChatGPT, mit Hilfe von Patrick Stein",
        "illustrator": "Hugh Thomson",
        "illustrations": True,
        "initials": True,
        "paired": True,
        "primary_language": "de",
        "secondary_language": "en",
        "secondary_label": "EN",
        "initials_credit": "Dekorative Initialen: Hugh Thomson (1894); F, U und Z ergänzt mit OpenAI (2026)",
        "dedication": "Für deutsch- und englischsprachige Leser und alle, die die jeweils andere Sprache lernen",
        "download_url": "https://github.com/jollyjinx/Stolz-und-Vorurteil/releases",
        "license_name": "MIT License",
        "license_url": "https://github.com/jollyjinx/Stolz-und-Vorurteil/blob/main/LICENSE",
        "language": "de-DE",
    },
    "english-german": {
        "chapters": ROOT / "source-chapters",
        "paired_chapters": ROOT / "modern-german-chapters",
        "frontmatter": ROOT / "frontmatter" / "english-german.md",
        "basename": "Pride-and-Prejudice-Englisch-Deutsch",
        "title": "Pride and Prejudice / Stolz und Vorurteil",
        "subtitle": "Fully bilingual: English first",
        "cover": COVERS / "Pride-and-Prejudice-Englisch-Deutsch.png",
        "author": "Jane Austen",
        "translator": "ChatGPT, mit Hilfe von Patrick Stein",
        "illustrator": "Hugh Thomson",
        "illustrations": True,
        "initials": True,
        "allow_missing_initials": True,
        "paired": True,
        "primary_language": "en",
        "secondary_language": "de",
        "secondary_label": "DE",
        "initials_credit": "Decorative initials: Hugh Thomson (1894)",
        "dedication": "For German- and English-speaking readers and everyone learning either language",
        "download_url": "https://github.com/jollyjinx/Stolz-und-Vorurteil/releases",
        "license_name": "MIT License",
        "license_url": "https://github.com/jollyjinx/Stolz-und-Vorurteil/blob/main/LICENSE",
        "language": "en-US",
    },
}


class OpeningInitialImage(ReportLabImage):
    """A scalable initial image with optional punctuation on its left."""

    def __init__(self, filename: str, prefix: str = "") -> None:
        super().__init__(filename)
        scale = min(
            (14 * mm) / self.imageWidth,
            (25 * mm) / self.imageHeight,
            1.0,
        )
        self._opening_image_width = self.imageWidth * scale
        self._opening_image_height = self.imageHeight * scale
        self._opening_prefix = prefix
        self._opening_prefix_font_size = 15.0
        self._opening_prefix_width = (
            stringWidth(prefix, "Times-Roman", self._opening_prefix_font_size)
            + 0.6 * mm
            if prefix
            else 0.0
        )
        self._opening_natural_height = self._opening_image_height
        self.drawWidth = self._opening_prefix_width + self._opening_image_width
        self.drawHeight = self._opening_image_height

    def draw(self) -> None:
        factor = self.drawHeight / self._opening_natural_height
        prefix_width = self._opening_prefix_width * factor
        if self._opening_prefix:
            font_size = self._opening_prefix_font_size * factor
            self.canv.setFont("Times-Roman", font_size)
            self.canv.drawString(
                0,
                self.drawHeight - font_size * 0.86,
                self._opening_prefix,
            )
        self.canv.drawImage(
            self._img or self.filename,
            prefix_width,
            0,
            self._opening_image_width * factor,
            self._opening_image_height * factor,
            mask=self._mask,
        )


def run(command: list[str]) -> None:
    print("+", " ".join(command))
    subprocess.run(command, cwd=ROOT, check=True)


def edition_cover(edition: dict[str, object]) -> Path | None:
    cover = edition.get("cover")
    if cover is None:
        return None
    cover_path = Path(cover)
    if not cover_path.exists():
        raise RuntimeError(f"Cover image is missing: {cover_path}")
    return cover_path


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
        has_german_caption = bool(entry.get("caption_de"))
        has_english_caption = bool(entry.get("caption_en"))
        if has_german_caption != has_english_caption:
            raise RuntimeError(
                f"Illustration captions must be present in both languages: {image}"
            )
    return entries


def load_easy_german_glossary() -> list[dict[str, str]]:
    if not EASY_GERMAN_GLOSSARY.exists():
        raise RuntimeError(f"Easy German glossary is missing: {EASY_GERMAN_GLOSSARY}")
    payload = json.loads(EASY_GERMAN_GLOSSARY.read_text(encoding="utf-8"))
    entries = payload.get("entries") if isinstance(payload, dict) else None
    if not isinstance(entries, list) or not entries:
        raise RuntimeError("Easy German glossary must contain a non-empty entries list.")
    normalized: list[dict[str, str]] = []
    seen_terms: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise RuntimeError("Each Easy German glossary entry must be an object.")
        term = str(entry.get("term") or "").strip()
        description = str(entry.get("description") or "").strip()
        sort_key = str(entry.get("sort") or term).strip()
        guidance = str(entry.get("translator_guidance") or "").strip()
        if not term or not description or not guidance:
            raise RuntimeError(
                "Every Easy German glossary entry needs term, description, "
                "and translator_guidance."
            )
        if term in seen_terms:
            raise RuntimeError(f"Duplicate Easy German glossary term: {term}")
        seen_terms.add(term)
        normalized.append(
            {
                "term": term,
                "description": description,
                "sort": sort_key,
                "translator_guidance": guidance,
            }
        )
    return sorted(normalized, key=lambda entry: entry["sort"].casefold())


def load_easy_german_notes() -> list[dict[str, object]]:
    if not EASY_GERMAN_NOTES.exists():
        raise RuntimeError(f"Easy German notes are missing: {EASY_GERMAN_NOTES}")
    payload = json.loads(EASY_GERMAN_NOTES.read_text(encoding="utf-8"))
    notes = payload.get("notes") if isinstance(payload, dict) else None
    if not isinstance(notes, list):
        raise RuntimeError("Easy German notes must contain a notes list.")
    normalized: list[dict[str, object]] = []
    seen_ids: set[str] = set()
    seen_anchors: set[tuple[int, int, str]] = set()
    for number, note in enumerate(notes, start=1):
        if not isinstance(note, dict):
            raise RuntimeError("Each Easy German note must be an object.")
        note_id = str(note.get("id") or "").strip()
        chapter = int(note.get("chapter", 0))
        paragraph = int(note.get("paragraph", 0))
        phrase = str(note.get("phrase") or "").strip()
        note_text = str(note.get("text") or "").strip()
        if not note_id or not re.fullmatch(r"[a-z0-9-]+", note_id):
            raise RuntimeError(f"Invalid Easy German note id: {note_id!r}")
        if note_id in seen_ids:
            raise RuntimeError(f"Duplicate Easy German note id: {note_id}")
        if not 1 <= chapter <= 61 or paragraph < 1 or not phrase or not note_text:
            raise RuntimeError(f"Invalid Easy German note: {note_id}")
        anchor = (chapter, paragraph, phrase)
        if anchor in seen_anchors:
            raise RuntimeError(f"Duplicate Easy German note anchor: {anchor}")
        seen_ids.add(note_id)
        seen_anchors.add(anchor)
        normalized.append(
            {
                "id": note_id,
                "chapter": chapter,
                "paragraph": paragraph,
                "phrase": phrase,
                "text": note_text,
                "number": number,
            }
        )
    normalized.sort(
        key=lambda note: (
            int(note["chapter"]),
            int(note["paragraph"]),
            int(note["number"]),
        )
    )
    for number, note in enumerate(normalized, start=1):
        note["number"] = number
    return normalized


def notes_for_chapter(
    notes: list[dict[str, object]],
    chapter_number: int,
) -> list[dict[str, object]]:
    return [note for note in notes if int(note["chapter"]) == chapter_number]


def annotate_markdown_paragraph(
    paragraph: str,
    paragraph_number: int,
    chapter_notes: list[dict[str, object]],
) -> str:
    annotated = paragraph
    for note in chapter_notes:
        if int(note["paragraph"]) != paragraph_number:
            continue
        phrase = str(note["phrase"])
        if phrase not in annotated:
            raise RuntimeError(
                f"Easy German note {note['id']} cannot find {phrase!r} in "
                f"paragraph {paragraph_number}."
            )
        annotated = annotated.replace(
            phrase,
            f"{phrase}[^easy-{note['id']}]",
            1,
        )
    return annotated


def easy_german_note_definitions(
    chapter_notes: list[dict[str, object]],
) -> list[str]:
    return [
        f"[^easy-{note['id']}]: {note['text']}"
        for note in chapter_notes
    ]


def easy_german_glossary_markdown() -> str:
    parts = [
        "# Glossar",
        (
            "Hier werden wichtige Personen, Orte und Begriffe noch einmal "
            "erklärt. Du kannst die Einträge nach dem Lesen oder beim "
            "erneuten Lesen nachschlagen."
        ),
    ]
    for entry in load_easy_german_glossary():
        parts.extend([f"## {entry['term']}", entry["description"]])
    return "\n\n".join(parts)


def markdown_illustration(
    entry: dict[str, object],
    languages: tuple[str, ...] = ("de",),
) -> str:
    path = f"illustrations/{entry['image']}"
    output = [
        "::: {.book-figure}",
        f"![]({path}){{.book-illustration}}",
    ]
    for language in languages:
        caption = str(entry.get(f"caption_{language}") or "")
        if caption:
            caption_text = f"[{caption}]{{lang={language}}}"
            if len(languages) > 1:
                caption_text = (
                    f"[{language.upper()}]{{.caption-language}} "
                    f"{caption_text}"
                )
            output.extend(
                [
                    "",
                    caption_text,
                ]
            )
    output.append(":::")
    return "\n".join(output)


def load_initials() -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    for manifest in INITIAL_MANIFESTS:
        if not manifest.exists():
            raise RuntimeError(f"Initial manifest is missing: {manifest}")
        manifest_entries = json.loads(manifest.read_text(encoding="utf-8"))
        if not isinstance(manifest_entries, list):
            raise RuntimeError(f"Initial manifest must contain a JSON list: {manifest}")
        entries.extend(manifest_entries)

    for entry in entries:
        letter = str(entry.get("letter", ""))
        if len(letter) != 1 or not letter.isalpha() or not letter.isupper():
            raise RuntimeError(f"Invalid initial letter: {letter!r}")
        image = ILLUSTRATIONS / str(entry["image"])
        if not image.exists():
            raise RuntimeError(f"Initial image is missing: {image}")
    return entries


def split_opening_initial(
    paragraph: str,
    expected_letter: str | None = None,
) -> tuple[str, str, str]:
    match = OPENING_INITIAL.match(paragraph)
    if not match:
        raise RuntimeError(f"Cannot find chapter-opening initial in: {paragraph[:80]!r}")
    prefix = match.group("prefix")
    letter = match.group("letter")
    remainder = match.group("rest")
    if expected_letter is not None and letter != expected_letter:
        raise RuntimeError(
            f"Chapter begins with {letter!r}, but its initial image is "
            f"cataloged as {expected_letter!r}."
        )
    return prefix, letter, remainder


def assign_initials(
    chapters: list[Path],
    catalog: list[dict[str, object]],
    *,
    allow_missing: bool = False,
) -> dict[int, dict[str, object]]:
    openings = {
        number: split_opening_initial(
            next(
                block.strip()
                for block in chapter.read_text(encoding="utf-8").split("\n\n")
                if block.strip() and not block.lstrip().startswith("#")
            )
        )
        for number, chapter in enumerate(chapters, start=1)
    }
    assignments: dict[int, dict[str, object]] = {}
    used_images: set[str] = set()

    # Preserve an initial in its historical source chapter whenever the
    # translated opening happens to begin with the same letter.
    for chapter, (_, letter, _) in openings.items():
        exact = next(
            (
                entry
                for entry in catalog
                if entry.get("source_chapter") == chapter
                and str(entry["letter"]) == letter
            ),
            None,
        )
        if exact:
            assignments[chapter] = exact
            used_images.add(str(exact["image"]))

    # Then use every still-available design for the required letter before
    # repeating one.  This keeps the German edition as varied as possible.
    for chapter, (_, letter, _) in openings.items():
        if chapter in assignments:
            continue
        unused = [
            entry
            for entry in catalog
            if str(entry["letter"]) == letter
            and str(entry["image"]) not in used_images
        ]
        if unused:
            chosen = unused[0]
            assignments[chapter] = chosen
            used_images.add(str(chosen["image"]))

    repeated_by_letter: dict[str, int] = {}
    for chapter, (_, letter, _) in openings.items():
        if chapter in assignments:
            continue
        candidates = [
            entry for entry in catalog if str(entry["letter"]) == letter
        ]
        if not candidates:
            if allow_missing:
                continue
            raise RuntimeError(f"No decorative initial is available for {letter!r}.")
        repeat_index = repeated_by_letter.get(letter, 0)
        assignments[chapter] = candidates[repeat_index % len(candidates)]
        repeated_by_letter[letter] = repeat_index + 1

    if not allow_missing and len(assignments) != len(chapters):
        raise RuntimeError(
            f"Expected {len(chapters)} initial assignments, found {len(assignments)}."
        )
    return assignments


def markdown_initial(
    paragraph: str,
    entry: dict[str, object],
) -> str:
    prefix, letter, remainder = split_opening_initial(
        paragraph,
        str(entry["letter"]),
    )
    path = f"illustrations/{entry['image']}"
    image = f"![{letter}]({path}){{.chapter-initial}}"
    if prefix:
        punctuation = f"[{prefix}]{{.chapter-initial-punctuation}}"
        group = f"[{punctuation}{image}]{{.chapter-initial-group}}"
    else:
        group = f"[{image}]{{.chapter-initial-group}}"
    return f"{group}{remainder}"


def illustrated_chapter_markdown(
    chapter: Path,
    chapter_number: int,
    illustrations: list[dict[str, object]],
    initial: dict[str, object] | None = None,
    notes: list[dict[str, object]] | None = None,
    display_heading: str | None = None,
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

    chapter_notes = notes_for_chapter(notes or [], chapter_number)
    output = [display_heading or blocks[0]]
    output.extend(markdown_illustration(entry) for entry in by_position.get(0, []))
    for position, paragraph in enumerate(body, start=1):
        paragraph = annotate_markdown_paragraph(
            paragraph,
            position,
            chapter_notes,
        )
        if position == 1 and initial:
            paragraph = markdown_initial(paragraph, initial)
        output.append(paragraph)
        output.extend(
            markdown_illustration(entry)
            for entry in by_position.get(position, [])
        )
    output.extend(easy_german_note_definitions(chapter_notes))
    return "\n\n".join(output)


def paired_chapter_markdown(
    primary_chapter: Path,
    secondary_chapter: Path,
    chapter_number: int,
    illustrations: list[dict[str, object]],
    primary_language: str,
    secondary_language: str,
    secondary_label: str,
    initial: dict[str, object] | None = None,
) -> str:
    primary_blocks = [
        block.strip()
        for block in primary_chapter.read_text(encoding="utf-8").split("\n\n")
        if block.strip()
    ]
    secondary_blocks = [
        block.strip()
        for block in secondary_chapter.read_text(encoding="utf-8").split("\n\n")
        if block.strip()
    ]
    if len(primary_blocks) != len(secondary_blocks):
        raise RuntimeError(
            f"Cannot pair chapter {chapter_number}: {primary_chapter.name} has "
            f"{len(primary_blocks) - 1} paragraphs, but {secondary_chapter.name} "
            f"has {len(secondary_blocks) - 1}."
        )

    by_position: dict[int, list[dict[str, object]]] = {}
    for entry in illustrations:
        if int(entry["chapter"]) != chapter_number:
            continue
        position = int(entry["after_paragraph"])
        if position > len(primary_blocks) - 1:
            raise RuntimeError(
                f"Illustration {entry['image']} follows paragraph {position}, "
                f"but {primary_chapter.name} has only {len(primary_blocks) - 1} paragraphs."
            )
        by_position.setdefault(position, []).append(entry)

    primary_heading = primary_blocks[0].removeprefix("# ")
    secondary_heading = secondary_blocks[0].removeprefix("# ")
    output = [f"# {primary_heading} / {secondary_heading}"]
    output.extend(
        markdown_illustration(
            entry,
            (primary_language, secondary_language),
        )
        for entry in by_position.get(0, [])
    )
    for position, (primary, secondary) in enumerate(
        zip(primary_blocks[1:], secondary_blocks[1:], strict=True),
        start=1,
    ):
        if position == 1 and initial:
            primary = markdown_initial(primary, initial)
        output.append(
            "\n\n".join(
                [
                    ":::: {.learner-pair}",
                    f"::: {{.learner-paragraph .learner-primary lang={primary_language}}}\n{primary}\n:::",
                    f"::: {{.learner-paragraph .learner-secondary lang={secondary_language} data-label={secondary_label}}}\n{secondary}\n:::",
                    "::::",
                ]
            )
        )
        output.extend(
            markdown_illustration(
                entry,
                (primary_language, secondary_language),
            )
            for entry in by_position.get(position, [])
        )
    return "\n\n".join(output)


def build_markdown(edition: dict[str, object]) -> Path:
    chapter_dir = edition["chapters"]
    assert isinstance(chapter_dir, Path)
    output = DIST / f"{edition['basename']}.md"
    parts = [Path(edition["frontmatter"]).read_text(encoding="utf-8").rstrip()]
    if edition.get("introduction"):
        parts.append(
            Path(edition["introduction"]).read_text(encoding="utf-8").rstrip()
        )
    chapters = chapter_files(chapter_dir)
    if edition.get("paired"):
        paired_chapter_dir = edition["paired_chapters"]
        assert isinstance(paired_chapter_dir, Path)
        paired_chapters = chapter_files(paired_chapter_dir)
        primary_language = str(edition["primary_language"])
        secondary_language = str(edition["secondary_language"])
        secondary_label = str(edition["secondary_label"])
        illustrations = load_illustrations() if edition.get("illustrations") else []
        initials = (
            assign_initials(
                chapters,
                load_initials(),
                allow_missing=bool(edition.get("allow_missing_initials")),
            )
            if edition.get("initials")
            else {}
        )
        frontispieces = [
            entry for entry in illustrations if int(entry["chapter"]) == 0
        ]
        parts.extend(
            markdown_illustration(
                entry,
                (primary_language, secondary_language),
            )
            for entry in frontispieces
        )
        parts.extend(
            paired_chapter_markdown(
                primary_path,
                secondary_path,
                number,
                illustrations,
                primary_language,
                secondary_language,
                secondary_label,
                initials.get(number),
            )
            for number, (primary_path, secondary_path) in enumerate(
                zip(chapters, paired_chapters, strict=True),
                start=1,
            )
        )
    elif edition.get("illustrations"):
        illustrations = load_illustrations()
        notes = load_easy_german_notes() if edition.get("notes") else []
        initials = (
            assign_initials(
                chapters,
                load_initials(),
                allow_missing=bool(edition.get("allow_missing_initials")),
            )
            if edition.get("initials")
            else {}
        )
        frontispieces = [
            entry for entry in illustrations if int(entry["chapter"]) == 0
        ]
        parts.extend(markdown_illustration(entry) for entry in frontispieces)
        parts.extend(
            illustrated_chapter_markdown(
                path,
                number,
                illustrations,
                initials.get(number),
                notes,
                f"# Kapitel {number}"
                if edition.get("numeric_chapter_headings")
                else None,
            )
            for number, path in enumerate(chapters, start=1)
        )
    else:
        parts.extend(path.read_text(encoding="utf-8").rstrip() for path in chapters)
    if edition.get("glossary"):
        parts.append(easy_german_glossary_markdown())
    output.write_text("\n\n".join(parts) + "\n", encoding="utf-8")
    return output


def build_pandoc(markdown: Path, edition: dict[str, object]) -> None:
    basename = str(edition["basename"])
    cover = edition_cover(edition)
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
    html_command = common + [
        "--self-contained", "--to=html5",
        "--output", str(DIST / f"{basename}.html"),
    ]
    cover_fragment: Path | None = None
    if cover:
        cover_fragment = DIST / f".{basename}-cover.html"
        cover_fragment.write_text(
            '<div class="book-cover">\n'
            f'  <img src="{html.escape(str(cover), quote=True)}" '
            f'alt="{html.escape(str(edition["title"]), quote=True)}">\n'
            "</div>\n",
            encoding="utf-8",
        )
        html_command += ["--include-before-body", str(cover_fragment)]
    try:
        run(html_command)
    finally:
        if cover_fragment:
            cover_fragment.unlink(missing_ok=True)

    epub_command = common + ["--to=epub3", "--output", str(DIST / f"{basename}.epub")]
    if cover:
        epub_command += ["--epub-cover-image", str(cover)]
    run(epub_command)


def inline_markdown(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"\[([^]]+)]\((https?://[^)]+)\)", r'<link href="\2">\1</link>', escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", escaped)
    escaped = re.sub(r"\*([^*]+)\*", r"<i>\1</i>", escaped)
    return re.sub(r"`([^`]+)`", r'<font name="Courier">\1</font>', escaped)


def markdown_content_blocks(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        _, separator, text = text.partition("\n---\n")
        if not separator:
            raise RuntimeError(f"Unclosed YAML front matter in {path}")
    return [block.strip() for block in text.split("\n\n") if block.strip()]


def pdf_annotated_text(
    text: str,
    paragraph_number: int,
    chapter_notes: list[dict[str, object]],
) -> str:
    rendered = inline_markdown(text)
    for note in chapter_notes:
        if int(note["paragraph"]) != paragraph_number:
            continue
        phrase = inline_markdown(str(note["phrase"]))
        if phrase not in rendered:
            raise RuntimeError(
                f"Easy German note {note['id']} cannot find {note['phrase']!r} "
                f"in PDF paragraph {paragraph_number}."
            )
        rendered = rendered.replace(
            phrase,
            f"{phrase}<super>[{note['number']}]</super>",
            1,
        )
    return rendered


def append_pdf_markdown(
    story: list[object],
    path: Path,
    heading_style: ParagraphStyle,
    subheading_style: ParagraphStyle,
    body_style: ParagraphStyle,
) -> None:
    for block in markdown_content_blocks(path):
        if block == "\\newpage":
            story.append(PageBreak())
        elif block.startswith("# "):
            story.append(Paragraph(inline_markdown(block[2:]), heading_style))
        elif block.startswith("## "):
            story.append(Paragraph(inline_markdown(block[3:]), subheading_style))
        else:
            story.append(Paragraph(inline_markdown(block.replace("\n", " ")), body_style))


def page_number(canvas, document, offset: int = 1) -> None:
    if document.page > offset:
        canvas.setFont("Times-Roman", 9)
        canvas.setFillColor(HexColor("#5e4530"))
        canvas.drawCentredString(
            A5[0] / 2,
            12 * mm,
            str(document.page - offset),
        )


def draw_pdf_cover(canvas, cover: Path) -> None:
    image = ImageReader(str(cover))
    image_width, image_height = image.getSize()
    scale = min(A5[0] / image_width, A5[1] / image_height)
    draw_width = image_width * scale
    draw_height = image_height * scale
    canvas.saveState()
    canvas.setFillColor(HexColor("#050706"))
    canvas.rect(0, 0, A5[0], A5[1], stroke=0, fill=1)
    canvas.drawImage(
        image,
        (A5[0] - draw_width) / 2,
        (A5[1] - draw_height) / 2,
        width=draw_width,
        height=draw_height,
        preserveAspectRatio=True,
        anchor="c",
    )
    canvas.restoreState()


def pdf_illustration(
    entry: dict[str, object],
    caption_style: ParagraphStyle,
    *,
    languages: tuple[str, ...] = ("de",),
    max_height: float = 112 * mm,
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
    for language in languages:
        caption = entry.get(f"caption_{language}")
        if caption:
            caption_text = html.escape(str(caption))
            if len(languages) > 1:
                label = html.escape(language.upper())
                caption_text = f"<b>{label}</b>&nbsp;&nbsp;{caption_text}"
            flowables.append(
                Paragraph(
                    caption_text,
                    caption_style,
                )
            )
    flowables.append(Spacer(1, 4 * mm))
    return KeepTogether(flowables)


def pdf_initial_image(
    entry: dict[str, object],
    prefix: str = "",
) -> OpeningInitialImage:
    image_path = ILLUSTRATIONS / str(entry["image"])
    return OpeningInitialImage(str(image_path), prefix)


def build_pdf(edition: dict[str, object]) -> None:
    basename = str(edition["basename"])
    cover = edition_cover(edition)
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
    section_heading = ParagraphStyle(
        "SectionHeading", parent=heading, fontSize=20, leading=26,
        spaceBefore=4, spaceAfter=18,
    )
    subheading = ParagraphStyle(
        "Subheading", parent=styles["Heading2"], fontName="Times-Bold",
        fontSize=13, leading=18, textColor=HexColor("#5e4530"),
        spaceBefore=12, spaceAfter=7, keepWithNext=True,
    )
    body = ParagraphStyle("Body", parent=styles["BodyText"], fontName="Times-Roman", fontSize=10.5,
                          leading=15, alignment=TA_JUSTIFY, spaceAfter=10)
    note_style = ParagraphStyle(
        "EasyGermanNote", parent=body, fontSize=8.5, leading=12,
        leftIndent=5 * mm, rightIndent=2 * mm, textColor=HexColor("#5e4530"),
        backColor=HexColor("#f6f1eb"), borderPadding=(3, 5, 3, 5),
        spaceBefore=-4, spaceAfter=10,
    )
    glossary_term = ParagraphStyle(
        "GlossaryTerm", parent=subheading, keepWithNext=True,
    )
    learner_primary = ParagraphStyle(
        "LearnerPrimary", parent=body, spaceAfter=4
    )
    learner_secondary = ParagraphStyle(
        "LearnerSecondary", parent=body, fontSize=9.8, leading=14,
        leftIndent=5 * mm, rightIndent=2 * mm, textColor=HexColor("#5e4530"),
        backColor=HexColor("#f6f1eb"), borderPadding=(3, 5, 3, 5),
        spaceAfter=12,
    )
    caption = ParagraphStyle("IllustrationCaption", parent=styles["Normal"], fontName="Times-Italic",
                             fontSize=9.5, leading=13, alignment=TA_CENTER,
                             textColor=HexColor("#5e4530"), spaceBefore=7, spaceAfter=2)

    cover_language = str(edition["language"])[:2]
    cover_labels = COVER_LABELS.get(cover_language, COVER_LABELS["en"])
    story = []
    if cover:
        story.append(PageBreak())
    story.extend(
        [
            Paragraph(str(edition["title"]), title),
            Paragraph(str(edition["subtitle"]), subtitle),
        ]
    )
    story.append(Paragraph(f"{cover_labels['by']} {edition['author']}", credit))
    if edition.get("translator"):
        story.append(
            Paragraph(
                f"{cover_labels['translation']}: {edition['translator']}",
                credit,
            )
        )
    if edition.get("illustrator"):
        story.append(
            Paragraph(
                f"{cover_labels['illustrations']}: {edition['illustrator']} (1894)",
                credit,
            )
        )
    if edition.get("initials_credit"):
        story.append(Paragraph(str(edition["initials_credit"]), credit))
    if edition.get("dedication"):
        story.extend([Spacer(1, 24), Paragraph(str(edition["dedication"]), credit)])
    if edition.get("download_url"):
        download_url = html.escape(str(edition["download_url"]), quote=True)
        story.extend([
            Spacer(1, 12),
            Paragraph(
                f'{cover_labels["download"]}:<br/>'
                f'<link href="{download_url}">{download_url}</link>',
                credit,
            ),
        ])
    if edition.get("license_name") and edition.get("license_url"):
        license_name = html.escape(str(edition["license_name"]))
        license_url = html.escape(str(edition["license_url"]), quote=True)
        story.append(
            Paragraph(
                f'{cover_labels["license"]}: '
                f'<link href="{license_url}">{license_name}</link>',
                credit,
            )
        )
    story.append(PageBreak())

    introduction = edition.get("introduction")
    if introduction:
        append_pdf_markdown(
            story,
            Path(introduction),
            section_heading,
            subheading,
            body,
        )

    illustrations = load_illustrations() if edition.get("illustrations") else []
    primary_illustration_language = str(
        edition.get("primary_language") or str(edition["language"])[:2]
    )
    illustration_languages = (primary_illustration_language,)
    if edition.get("paired"):
        illustration_languages += (str(edition["secondary_language"]),)
    if illustrations:
        frontispieces = [
            entry for entry in illustrations if int(entry["chapter"]) == 0
        ]
        for frontispiece in frontispieces:
            story.extend(
                [
                    pdf_illustration(
                        frontispiece,
                        caption,
                        languages=illustration_languages,
                        max_height=(124 if edition.get("paired") else 132) * mm,
                    ),
                    PageBreak(),
                ]
            )

    chapter_dir = edition["chapters"]
    assert isinstance(chapter_dir, Path)
    chapters = chapter_files(chapter_dir)
    paired_chapters: list[Path] = []
    if edition.get("paired"):
        paired_chapter_dir = edition["paired_chapters"]
        assert isinstance(paired_chapter_dir, Path)
        paired_chapters = chapter_files(paired_chapter_dir)
    initials = (
        assign_initials(
            chapters,
            load_initials(),
            allow_missing=bool(edition.get("allow_missing_initials")),
        )
        if edition.get("initials")
        else {}
    )
    easy_notes = load_easy_german_notes() if edition.get("notes") else []
    for chapter_index, chapter in enumerate(chapters):
        blocks = [block.strip() for block in chapter.read_text(encoding="utf-8").split("\n\n") if block.strip()]
        paired_blocks: list[str] = []
        if edition.get("paired"):
            paired_blocks = [
                block.strip()
                for block in paired_chapters[chapter_index]
                .read_text(encoding="utf-8")
                .split("\n\n")
                if block.strip()
            ]
            if len(blocks) != len(paired_blocks):
                raise RuntimeError(
                    f"Cannot pair chapter {chapter_index + 1}: "
                    f"{len(blocks) - 1} primary and {len(paired_blocks) - 1} secondary paragraphs."
                )
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

        chapter_heading = (
            f"Kapitel {chapter_index + 1}"
            if edition.get("numeric_chapter_headings")
            else blocks[0].removeprefix("# ")
        )
        if paired_blocks:
            chapter_heading += f" / {paired_blocks[0].removeprefix('# ')}"
        story.append(Paragraph(inline_markdown(chapter_heading), heading))
        story.extend(
            pdf_illustration(
                entry,
                caption,
                languages=illustration_languages,
            )
            for entry in by_position.get(0, [])
        )
        chapter_notes = notes_for_chapter(easy_notes, chapter_index + 1)
        for position, block in enumerate(blocks[1:], start=1):
            paragraph_style = learner_primary if paired_blocks else body
            initial = initials.get(chapter_index + 1) if position == 1 else None
            paragraph_flowables = []
            if initial:
                prefix, _, remainder = split_opening_initial(
                    block,
                    str(initial["letter"]),
                )
                paragraph_flowables.append(
                    ImageAndFlowables(
                        pdf_initial_image(initial, prefix),
                        [
                            Paragraph(
                                pdf_annotated_text(
                                    remainder,
                                    position,
                                    chapter_notes,
                                ),
                                paragraph_style,
                            )
                        ],
                        imageRightPadding=3 * mm,
                        imageBottomPadding=1.5 * mm,
                        imageSide="left",
                    )
                )
            else:
                paragraph_flowables.append(
                    Paragraph(
                        pdf_annotated_text(block, position, chapter_notes),
                        paragraph_style,
                    )
                )
            paragraph_flowables.extend(
                Paragraph(
                    f"<b>[{note['number']}]</b>&nbsp;&nbsp;"
                    f"{inline_markdown(str(note['text']))}",
                    note_style,
                )
                for note in chapter_notes
                if int(note["paragraph"]) == position
            )
            if paired_blocks:
                secondary = paired_blocks[position]
                secondary_label = html.escape(str(edition["secondary_label"]))
                paragraph_flowables.append(
                    Paragraph(
                        f'<font size="7"><b>{secondary_label}</b></font>&nbsp;&nbsp;{inline_markdown(secondary)}',
                        learner_secondary,
                    )
                )
                story.append(KeepTogether(paragraph_flowables))
            elif any(
                int(note["paragraph"]) == position
                for note in chapter_notes
            ):
                story.append(KeepTogether(paragraph_flowables))
            else:
                story.extend(paragraph_flowables)
            story.extend(
                pdf_illustration(
                    entry,
                    caption,
                    languages=illustration_languages,
                )
                for entry in by_position.get(position, [])
            )
        if chapter_index != len(chapters) - 1:
            story.append(PageBreak())
    if edition.get("glossary"):
        story.extend([PageBreak(), Paragraph("Glossar", section_heading)])
        story.append(
            Paragraph(
                (
                    "Hier werden wichtige Personen, Orte und Begriffe noch einmal "
                    "erklärt. Du kannst die Einträge nach dem Lesen oder beim "
                    "erneuten Lesen nachschlagen."
                ),
                body,
            )
        )
        for entry in load_easy_german_glossary():
            story.extend(
                [
                    Paragraph(inline_markdown(entry["term"]), glossary_term),
                    Paragraph(inline_markdown(entry["description"]), body),
                ]
            )
    if cover:
        document.build(
            story,
            onFirstPage=lambda canvas, document: draw_pdf_cover(canvas, cover),
            onLaterPages=lambda canvas, document: page_number(
                canvas,
                document,
                offset=2,
            ),
        )
    else:
        document.build(story, onFirstPage=page_number, onLaterPages=page_number)


def build(edition_name: str) -> None:
    edition = EDITIONS[edition_name]
    markdown = build_markdown(edition)
    build_pandoc(markdown, edition)
    build_pdf(edition)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "edition",
        choices=[*EDITIONS, "bilingual", "all"],
        default="all",
        nargs="?",
    )
    args = parser.parse_args()
    if shutil.which("pandoc") is None:
        raise SystemExit("pandoc is required; install it and rerun this command.")
    DIST.mkdir(exist_ok=True)
    selected = "german-english" if args.edition == "bilingual" else args.edition
    for edition_name in (EDITIONS if selected == "all" else [selected]):
        build(edition_name)


if __name__ == "__main__":
    main()
