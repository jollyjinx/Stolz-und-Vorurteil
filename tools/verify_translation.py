#!/usr/bin/env python3
"""Verify the chapter-level structure of the German translation."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source-chapters"
TRANSLATION = ROOT / "modern-german-chapters"


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


def main() -> None:
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

    if failures:
        print("Translation verification failed:", *failures, sep="\n- ")
        raise SystemExit(1)
    print(f"Verified {len(source_files)} translated chapters with matching headings and paragraph counts.")


if __name__ == "__main__":
    main()
