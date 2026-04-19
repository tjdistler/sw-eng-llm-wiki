"""Inspection tools: page status, tail, sections, read-range."""

from __future__ import annotations

import re
from dataclasses import dataclass

from .paths import PathEscape, wiki_read_path, wiki_root


LAST_UPDATED_RE = re.compile(r"^\*\*Last updated\*\*:\s*(\S+)\s*$", re.MULTILINE)
HEADING_RE = re.compile(r"^(#{2,6})\s+(.+?)\s*$")


@dataclass
class PageStatus:
    page: str
    exists: bool
    line_count: int | None = None
    size_bytes: int | None = None
    last_updated: str | None = None

    def to_dict(self) -> dict:
        return {
            "page": self.page,
            "exists": self.exists,
            "line_count": self.line_count,
            "size_bytes": self.size_bytes,
            "last_updated": self.last_updated,
        }


def wiki_page_status(pages: list[str]) -> list[dict]:
    results: list[PageStatus] = []
    for name in pages:
        try:
            path = wiki_read_path(name)
        except PathEscape:
            results.append(PageStatus(page=name, exists=False))
            continue
        if not path.exists():
            results.append(PageStatus(page=name, exists=False))
            continue
        text = path.read_text(encoding="utf-8")
        m = LAST_UPDATED_RE.search(text)
        results.append(PageStatus(
            page=name,
            exists=True,
            line_count=text.count("\n") + (0 if text.endswith("\n") or text == "" else 1),
            size_bytes=path.stat().st_size,
            last_updated=m.group(1) if m else None,
        ))
    return [r.to_dict() for r in results]


def _tail(path_name: str, lines: int) -> str:
    if lines <= 0:
        return ""
    path = wiki_root() / path_name
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8")
    split = text.splitlines()
    return "\n".join(split[-lines:])


def wiki_tail_log(lines: int = 30) -> str:
    return _tail("log.md", lines)


def wiki_tail_index(lines: int = 20) -> str:
    return _tail("index.md", lines)


def wiki_list_sections(page: str) -> list[dict]:
    path = wiki_read_path(page)
    if not path.exists():
        raise FileNotFoundError(f"Wiki page does not exist: {page}")
    out: list[dict] = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        m = HEADING_RE.match(line)
        if not m:
            continue
        out.append({
            "level": len(m.group(1)),
            "heading": m.group(2).strip(),
            "line": i,
        })
    return out


def wiki_read_range(page: str, start_line: int, end_line: int) -> str:
    if start_line < 1:
        raise ValueError("start_line must be >= 1")
    if end_line < start_line:
        raise ValueError("end_line must be >= start_line")
    path = wiki_read_path(page)
    if not path.exists():
        raise FileNotFoundError(f"Wiki page does not exist: {page}")
    lines = path.read_text(encoding="utf-8").splitlines()
    # Inclusive, 1-indexed.
    return "\n".join(lines[start_line - 1:end_line])
