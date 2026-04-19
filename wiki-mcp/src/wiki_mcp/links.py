"""Wikilink resolution.

The wikilink regex and code-fence stripping mirror wiki-linter/lint.py so the
two tools agree on what counts as a link.
"""

from __future__ import annotations

import re

from .paths import PathEscape, wiki_read_path, wiki_root


# Matches [[target]], [[target#anchor]], [[target|label]] — same as wiki-linter.
WIKILINK_RE = re.compile(r"\[\[([^\]\[|#]*)(?:#([^\]\[|]+))?(?:\|([^\]\[]+))?\]\]")


def _strip_code_fences(text: str) -> str:
    out: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            out.append("")
            continue
        out.append("" if in_fence else line)
    return "\n".join(out)


def _extract_targets(text: str) -> list[str]:
    scrubbed = _strip_code_fences(text)
    targets: list[str] = []
    for m in WIKILINK_RE.finditer(scrubbed):
        target = (m.group(1) or "").strip().rstrip("\\")
        if target:
            targets.append(target)
    return targets


def _all_stems() -> set[str]:
    root = wiki_root()
    if not root.exists():
        return set()
    return {p.stem for p in root.glob("*.md")}


def wiki_check_links(
    pages: list[str] | None = None,
    include_clean: bool = False,
) -> dict | list[dict]:
    stems = _all_stems()
    root = wiki_root()

    if pages is None:
        sources = sorted(root.glob("*.md"))
    else:
        sources = []
        for name in pages:
            try:
                path = wiki_read_path(name)
            except PathEscape:
                continue
            sources.append(path)

    per_page: list[dict] = []
    for path in sources:
        if path.exists():
            missing: list[str] = []
            for target in _extract_targets(path.read_text(encoding="utf-8")):
                if target not in stems and target not in missing:
                    missing.append(target)
            per_page.append({"page": path.stem, "missing_targets": missing})
        else:
            per_page.append(
                {"page": path.stem, "missing_targets": [], "error": "page-not-found"}
            )

    if include_clean:
        return per_page

    pages_with_issues = [
        entry
        for entry in per_page
        if entry["missing_targets"] or "error" in entry
    ]
    return {
        "total_pages_checked": len(per_page),
        "pages_with_issues": pages_with_issues,
    }
