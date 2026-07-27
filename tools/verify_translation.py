#!/usr/bin/env python3
"""Verify the chapter-level structure of the German translation."""

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
ALIGNMENT_MANIFEST = ROOT / "alignment-manifest.json"


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
) -> None:
    if not ALIGNMENT_MANIFEST.exists():
        failures.append(f"alignment manifest is missing: {ALIGNMENT_MANIFEST}")
        return
    manifest = json.loads(ALIGNMENT_MANIFEST.read_text(encoding="utf-8"))
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
            "audited alignment changed in chapter(s) "
            + ", ".join(f"{chapter:02d}" for chapter in changed)
            + "; review the paragraph pairing, then run "
            "tools/verify_translation.py --update-alignment-manifest"
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
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    failures: list[str] = []
    source_files = sorted(SOURCE.glob("*.md"))
    translated_files = sorted(TRANSLATION.glob("*.md"))

    if len(source_files) != 61:
        failures.append(f"expected 61 source chapters, found {len(source_files)}")
    if len(translated_files) != 61:
        failures.append(f"expected 61 translated chapters, found {len(translated_files)}")

    for source_path in source_files:
        number = source_path.name[:2]
        matches = list(TRANSLATION.glob(f"{number}-*.md"))
        if len(matches) != 1:
            failures.append(f"chapter {number}: expected exactly one translation, found {len(matches)}")
            continue
        translated_path = matches[0]
        source_paragraphs = paragraphs(source_path)
        translated_paragraphs = paragraphs(translated_path)
        if not re.fullmatch(r"# Kapitel [IVXLCDM]+", translated_paragraphs[0]):
            failures.append(f"chapter {number}: invalid heading in {translated_path.name}")
        if len(source_paragraphs) != len(translated_paragraphs):
            failures.append(
                f"chapter {number}: source has {len(source_paragraphs)} paragraphs; "
                f"translation has {len(translated_paragraphs)}"
            )
        for language, items in (
            ("source", source_paragraphs),
            ("translation", translated_paragraphs),
        ):
            for paragraph_number in suspicious_mid_sentence_splits(items):
                failures.append(
                    f"chapter {number}: {language} paragraph {paragraph_number} "
                    "appears to end in the middle of a sentence"
                )

    if args.epub:
        verify_epub_source(args.epub, failures)

    records = alignment_records(source_files, translated_files)
    if not args.update_alignment_manifest:
        verify_alignment_manifest(records, failures)

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

    total_paragraphs = sum(int(record["paragraphs"]) for record in records)
    print(
        f"Verified {len(source_files)} translated chapters with "
        f"{total_paragraphs} aligned paragraph pairs."
    )


if __name__ == "__main__":
    main()
