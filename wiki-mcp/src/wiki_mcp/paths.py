"""Root resolution and path-escape rejection.

Only read-only helpers are exposed. There is intentionally no write helper here;
the server has no way to mutate the filesystem.
"""

from __future__ import annotations

import os
from pathlib import Path


class PathEscape(ValueError):
    """Raised when a request would resolve outside the configured roots."""


def _resolve_root(env_var: str, default_name: str) -> Path:
    raw = os.environ.get(env_var)
    if raw:
        return Path(raw).expanduser().resolve()
    # Prefer the repo this server ships inside: src/wiki_mcp/paths.py → repo root.
    # Robust against cwd drift; Claude Code normally launches us from the repo,
    # but if that ever changes, silent empty-wiki responses are a worse failure
    # mode than a mis-set override.
    src_based = Path(__file__).resolve().parents[3] / default_name
    if src_based.is_dir():
        return src_based.resolve()
    return (Path.cwd() / default_name).resolve()


def wiki_root() -> Path:
    return _resolve_root("WIKI_ROOT", "wiki")


def raw_root() -> Path:
    return _resolve_root("RAW_ROOT", "raw")


def _ensure_within(root: Path, candidate: Path) -> Path:
    root = root.resolve()
    resolved = candidate.resolve()
    try:
        resolved.relative_to(root)
    except ValueError as e:
        raise PathEscape(f"{candidate} resolves outside {root}") from e
    return resolved


def wiki_read_path(name: str) -> Path:
    """Return an absolute path inside the wiki root for the given page name.

    `name` may include or omit the `.md` suffix, but may not contain path
    separators or `..` segments.
    """
    if not name or name in (".", ".."):
        raise PathEscape(f"Invalid page name: {name!r}")
    if "/" in name or "\\" in name:
        raise PathEscape(f"Page name may not contain path separators: {name!r}")
    filename = name if name.endswith(".md") else f"{name}.md"
    return _ensure_within(wiki_root(), wiki_root() / filename)


def raw_read_path(book: str, chapter: str | None = None) -> Path:
    """Return an absolute path inside the raw root for a book or chapter."""
    if not book or book in (".", ".."):
        raise PathEscape(f"Invalid book name: {book!r}")
    if "/" in book or "\\" in book:
        raise PathEscape(f"Book name may not contain path separators: {book!r}")
    candidate = raw_root() / book
    if chapter is not None:
        if "/" in chapter or "\\" in chapter or chapter in (".", ".."):
            raise PathEscape(f"Invalid chapter name: {chapter!r}")
        candidate = candidate / chapter
    return _ensure_within(raw_root(), candidate)
