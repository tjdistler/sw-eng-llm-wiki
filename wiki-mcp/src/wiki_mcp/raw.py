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


def _count_lines(path) -> int:
    count = 0
    with path.open("rb") as f:
        for _ in f:
            count += 1
    return count


def raw_list_chapters(book: str) -> list[dict]:
    book_dir = raw_read_path(book)
    if not book_dir.is_dir():
        raise FileNotFoundError(f"Raw book directory does not exist: {book}")
    paths = sorted(book_dir.glob("*.md"), key=lambda p: _natural_key(p.name))
    entries: list[dict] = []
    for path in paths:
        stat = path.stat()
        entries.append({
            "chapter": path.name,
            "line_count": _count_lines(path),
            "size_bytes": stat.st_size,
        })
    return entries
