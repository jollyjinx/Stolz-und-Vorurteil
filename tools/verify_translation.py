#!/usr/bin/env python3
"""Verify both German translations and their chapter-level alignment."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source-chapters"
TRANSLATION = ROOT / "modern-german-chapters"
EASY_TRANSLATION = ROOT / "easy-german-chapters"
ALIGNMENT_MANIFEST = ROOT / "alignment-manifest.json"
EASY_ALIGNMENT_MANIFEST = ROOT / "easy-german-alignment-manifest.json"
EASY_GLOSSARY = ROOT / "easy-german-glossary.json"
EASY_NOTES = ROOT / "easy-german-notes.json"


def paragraphs(path: Path) -> list[str]:
    return [paragraph.strip() for paragraph in path.read_text(encoding="utf-8").split("\n\n") if paragraph.strip()]


def suspicious_mid_sentence_splits(items: list[str]) -> list[int]:
    """Return paragraph numbers whose following break cuts through a sentence."""
    return [
        number
        for number, (current, following) in enumerate(
            zip(items[1:], items[2:]),
            start=1,
        )
        if current[-1].isalnum() and following[0].islower()
    ]


def digest(items: list[str]) -> str:
    canonical = "\0".join(items).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def alignment_records(
    source_files: list[Path],
    translated_files: list[Path],
) -> list[dict[str, object]]:
    translated_by_number = {
        path.name[:2]: path
        for path in translated_files
    }
    records: list[dict[str, object]] = []
    for source_path in source_files:
        number = source_path.name[:2]
        translated_path = translated_by_number.get(number)
        if translated_path is None:
            continue
        source_body = paragraphs(source_path)[1:]
        translated_body = paragraphs(translated_path)[1:]
        records.append(
            {
                "chapter": int(number),
                "paragraphs": len(source_body),
                "source_sha256": digest(source_body),
                "translation_sha256": digest(translated_body),
            }
        )
    return records


def verify_alignment_manifest(
    records: list[dict[str, object]],
    failures: list[str],
    manifest_path: Path = ALIGNMENT_MANIFEST,
    label: str = "audited alignment",
) -> None:
    if not manifest_path.exists():
        failures.append(f"{label} manifest is missing: {manifest_path}")
        return
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    expected = manifest.get("chapters") if isinstance(manifest, dict) else None
    if expected != records:
        expected_by_chapter = {
            record["chapter"]: record
            for record in expected or []
            if isinstance(record, dict) and "chapter" in record
        }
        actual_by_chapter = {
            record["chapter"]: record
            for record in records
        }
        changed = sorted(
            chapter
            for chapter in set(expected_by_chapter) | set(actual_by_chapter)
            if expected_by_chapter.get(chapter) != actual_by_chapter.get(chapter)
        )
        failures.append(
            f"{label} changed in chapter(s) "
            + ", ".join(f"{chapter:02d}" for chapter in changed)
            + "; review the paragraph pairing, then run "
            + (
                "tools/verify_translation.py --update-alignment-manifest"
                if manifest_path == ALIGNMENT_MANIFEST
                else "tools/verify_translation.py --update-easy-alignment-manifest"
            )
        )


def verify_epub_source(epub_path: Path, failures: list[str]) -> None:
    from split_epub import extract

    with tempfile.TemporaryDirectory() as temporary_directory:
        extracted = Path(temporary_directory)
        extract(epub_path, extracted)
        for source_path in sorted(SOURCE.glob("*.md")):
            extracted_path = extracted / source_path.name
            if not extracted_path.exists():
                failures.append(
                    f"EPUB extraction did not produce {source_path.name}"
                )
            elif (
                source_path.read_text(encoding="utf-8")
                != extracted_path.read_text(encoding="utf-8")
            ):
                failures.append(
                    f"{source_path.name} differs from a fresh EPUB extraction"
                )


def verify_chapter_set(
    source_files: list[Path],
    translated_files: list[Path],
    translated_directory: Path,
    label: str,
    failures: list[str],
) -> None:
    if len(translated_files) != 61:
        failures.append(
            f"expected 61 {label} chapters, found {len(translated_files)}"
        )
    for source_path in source_files:
        number = source_path.name[:2]
        matches = list(translated_directory.glob(f"{number}-*.md"))
        if len(matches) != 1:
            failures.append(
                f"{label} chapter {number}: expected exactly one translation, "
                f"found {len(matches)}"
            )
            continue
        translated_path = matches[0]
        source_paragraphs = paragraphs(source_path)
        translated_paragraphs = paragraphs(translated_path)
        if not translated_paragraphs:
            failures.append(f"{label} chapter {number}: file is empty")
            continue
        if not re.fullmatch(r"# Kapitel [IVXLCDM]+", translated_paragraphs[0]):
            failures.append(
                f"{label} chapter {number}: invalid heading in {translated_path.name}"
            )
        if len(source_paragraphs) != len(translated_paragraphs):
            failures.append(
                f"{label} chapter {number}: source has {len(source_paragraphs)} "
                f"paragraphs; translation has {len(translated_paragraphs)}"
            )
        if label == "Easy German" and "[^" in translated_path.read_text(encoding="utf-8"):
            failures.append(
                f"{label} chapter {number}: footnote markup belongs in "
                "easy-german-notes.json, not the chapter file"
            )
        if (
            label == "Easy German"
            and len(translated_paragraphs) > 1
            and re.match(r"^[^A-Za-zÄÖÜäöüß]*[A-ZÄÖÜ]{2,}\b", translated_paragraphs[1])
        ):
            failures.append(
                f"{label} chapter {number}: opening word uses source-style "
                "all caps instead of normal German capitalization"
            )
        for language, items in (
            ("source", source_paragraphs),
            (label, translated_paragraphs),
        ):
            for paragraph_number in suspicious_mid_sentence_splits(items):
                failures.append(
                    f"{label} chapter {number}: {language} paragraph "
                    f"{paragraph_number} appears to end in the middle of a sentence"
                )


def verify_easy_german_metadata(
    easy_files: list[Path],
    failures: list[str],
) -> None:
    try:
        glossary_payload = json.loads(EASY_GLOSSARY.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        failures.append(f"cannot read Easy German glossary: {error}")
        glossary_payload = {}
    glossary_entries = (
        glossary_payload.get("entries")
        if isinstance(glossary_payload, dict)
        else None
    )
    if not isinstance(glossary_entries, list) or not glossary_entries:
        failures.append("Easy German glossary needs a non-empty entries list")
    else:
        terms: set[str] = set()
        for entry in glossary_entries:
            if not isinstance(entry, dict):
                failures.append("Easy German glossary entries must be objects")
                continue
            term = str(entry.get("term") or "").strip()
            if not term or not str(entry.get("description") or "").strip():
                failures.append("Easy German glossary entry lacks term or description")
            if not str(entry.get("translator_guidance") or "").strip():
                failures.append(f"Easy German glossary term {term!r} lacks guidance")
            if term in terms:
                failures.append(f"duplicate Easy German glossary term: {term}")
            terms.add(term)

    try:
        notes_payload = json.loads(EASY_NOTES.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        failures.append(f"cannot read Easy German notes: {error}")
        return
    notes = notes_payload.get("notes") if isinstance(notes_payload, dict) else None
    if not isinstance(notes, list):
        failures.append("Easy German notes need a notes list")
        return
    files_by_chapter = {int(path.name[:2]): path for path in easy_files}
    note_ids: set[str] = set()
    for note in notes:
        if not isinstance(note, dict):
            failures.append("Easy German notes must be objects")
            continue
        note_id = str(note.get("id") or "").strip()
        phrase = str(note.get("phrase") or "").strip()
        note_text = str(note.get("text") or "").strip()
        try:
            chapter = int(note.get("chapter", 0))
            paragraph_number = int(note.get("paragraph", 0))
        except (TypeError, ValueError):
            failures.append(f"Easy German note {note_id!r} has an invalid anchor")
            continue
        if not re.fullmatch(r"[a-z0-9-]+", note_id):
            failures.append(f"invalid Easy German note id: {note_id!r}")
        if note_id in note_ids:
            failures.append(f"duplicate Easy German note id: {note_id}")
        note_ids.add(note_id)
        if not phrase or not note_text:
            failures.append(f"Easy German note {note_id!r} lacks phrase or text")
        chapter_path = files_by_chapter.get(chapter)
        if chapter_path is None:
            failures.append(
                f"Easy German note {note_id!r} points to missing chapter {chapter}"
            )
            continue
        chapter_paragraphs = paragraphs(chapter_path)[1:]
        if not 1 <= paragraph_number <= len(chapter_paragraphs):
            failures.append(
                f"Easy German note {note_id!r} points outside chapter {chapter}"
            )
        elif phrase not in chapter_paragraphs[paragraph_number - 1]:
            failures.append(
                f"Easy German note {note_id!r} cannot find {phrase!r} in "
                f"chapter {chapter}, paragraph {paragraph_number}"
            )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify source integrity and audited paragraph alignment."
    )
    parser.add_argument(
        "--epub",
        type=Path,
        help="also compare source-chapters with a fresh extraction of this EPUB",
    )
    parser.add_argument(
        "--update-alignment-manifest",
        action="store_true",
        help="record the current, manually reviewed chapter pairings",
    )
    parser.add_argument(
        "--update-easy-alignment-manifest",
        action="store_true",
        help="record the current, reviewed English-Easy German chapter pairings",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    failures: list[str] = []
    source_files = sorted(SOURCE.glob("*.md"))
    translated_files = sorted(TRANSLATION.glob("*.md"))
    easy_files = sorted(EASY_TRANSLATION.glob("*.md"))

    if len(source_files) != 61:
        failures.append(f"expected 61 source chapters, found {len(source_files)}")
    verify_chapter_set(
        source_files,
        translated_files,
        TRANSLATION,
        "Modern German",
        failures,
    )
    verify_chapter_set(
        source_files,
        easy_files,
        EASY_TRANSLATION,
        "Easy German",
        failures,
    )
    verify_easy_german_metadata(easy_files, failures)

    if args.epub:
        verify_epub_source(args.epub, failures)

    records = alignment_records(source_files, translated_files)
    easy_records = alignment_records(source_files, easy_files)
    if not args.update_alignment_manifest:
        verify_alignment_manifest(records, failures)
    if not args.update_easy_alignment_manifest:
        verify_alignment_manifest(
            easy_records,
            failures,
            EASY_ALIGNMENT_MANIFEST,
            "reviewed Easy German alignment",
        )

    if failures:
        print("Translation verification failed:", *failures, sep="\n- ")
        raise SystemExit(1)

    if args.update_alignment_manifest:
        manifest = {
            "version": 1,
            "description": (
                "Hashes of chapter paragraph sequences after manual "
                "English-German alignment review."
            ),
            "chapters": records,
        }
        ALIGNMENT_MANIFEST.write_text(
            json.dumps(manifest, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"Updated {ALIGNMENT_MANIFEST}.")
    if args.update_easy_alignment_manifest:
        manifest = {
            "version": 1,
            "description": (
                "Hashes of chapter paragraph sequences after English-Easy "
                "German alignment and accessibility review."
            ),
            "chapters": easy_records,
        }
        EASY_ALIGNMENT_MANIFEST.write_text(
            json.dumps(manifest, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"Updated {EASY_ALIGNMENT_MANIFEST}.")

    total_paragraphs = sum(int(record["paragraphs"]) for record in records)
    print(
        f"Verified {len(source_files)} translated chapters with "
        f"{total_paragraphs} aligned paragraph pairs."
    )
    easy_total = sum(int(record["paragraphs"]) for record in easy_records)
    print(
        f"Verified {len(easy_files)} Easy German chapters with "
        f"{easy_total} aligned paragraph pairs."
    )


if __name__ == "__main__":
    main()
