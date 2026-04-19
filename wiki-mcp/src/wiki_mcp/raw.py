"""raw/ discovery tools."""

from __future__ import annotations

import re

from .paths import raw_read_path


_DIGIT_RUN = re.compile(r"\d+")


def _natural_key(name: str) -> str:
    """Zero-pad digit runs so lexicographic sort yields natural order.

    Using a string key keeps the comparison type-stable — mixing int and str
    tuple elements risks `TypeError` on Python 3 for names where different
    segments sit at the same index.
    """
    return _DIGIT_RUN.sub(lambda m: m.group(0).zfill(20), name.lower())


def raw_list_chapters(book: str) -> list[str]:
    book_dir = raw_read_path(book)
    if not book_dir.is_dir():
        raise FileNotFoundError(f"Raw book directory does not exist: {book}")
    names = [p.name for p in book_dir.glob("*.md")]
    names.sort(key=_natural_key)
    return names
