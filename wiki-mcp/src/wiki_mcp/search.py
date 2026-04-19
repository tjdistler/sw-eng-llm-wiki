"""Search tools: wiki_search, wiki_list_pages."""

from __future__ import annotations

import json
import re
import shutil
import subprocess

from .paths import PathEscape, wiki_read_path, wiki_root


def wiki_list_pages(
    name_filter: str | None = None,
    name_filters: list[str] | None = None,
) -> list[str]:
    if name_filter is not None and name_filters is not None:
        raise ValueError(
            "Pass either name_filter or name_filters, not both."
        )
    root = wiki_root()
    if not root.exists():
        return []
    pages = sorted(p.stem for p in root.glob("*.md"))
    if name_filter:
        needle = name_filter.lower()
        pages = [p for p in pages if needle in p.lower()]
    elif name_filters:
        needles = [n.lower() for n in name_filters if n]
        if needles:
            pages = [p for p in pages if any(n in p.lower() for n in needles)]
    return pages


def _target_paths(files: list[str] | None):
    root = wiki_root()
    if files is None:
        return sorted(root.glob("*.md"))
    paths = []
    for name in files:
        try:
            path = wiki_read_path(name)
        except PathEscape:
            continue
        if path.exists():
            paths.append(path)
    return paths


def wiki_search(
    pattern: str,
    files: list[str] | None = None,
    context: int = 0,
) -> list[dict]:
    if not pattern:
        return []
    # Pre-validate with Python's regex engine so the error shape is the same
    # regardless of whether we dispatch to ripgrep or the pure-Python fallback.
    # Patterns valid in rg but not Python will false-positive here, which is
    # acceptable for the narrow set of features we expect wiki authors to use.
    try:
        regex = re.compile(pattern)
    except re.error as e:
        raise ValueError(f"Invalid regex: {e}") from e

    paths = _target_paths(files)
    if not paths:
        return []

    rg = shutil.which("rg")
    if rg:
        return _search_rg(rg, pattern, paths, context)
    return _search_py(regex, paths, context)


def _search_rg(rg: str, pattern: str, paths, context: int) -> list[dict]:
    cmd = [rg, "--json", "--no-heading", "--line-number"]
    if context > 0:
        cmd += ["-C", str(context)]
    cmd += ["-e", pattern, "--"]
    cmd += [str(p) for p in paths]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    # rg exits 1 when no matches; both 0 and 1 are normal.
    if proc.returncode not in (0, 1):
        raise RuntimeError(f"ripgrep failed ({proc.returncode}): {proc.stderr.strip()}")

    out: list[dict] = []
    for raw in proc.stdout.splitlines():
        if not raw:
            continue
        try:
            evt = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if evt.get("type") not in ("match", "context"):
            continue
        data = evt.get("data", {})
        path_text = data.get("path", {}).get("text", "")
        stem = _stem(path_text)
        line_no = data.get("line_number")
        snippet = data.get("lines", {}).get("text", "")
        out.append({
            "page": stem,
            "line": line_no,
            "snippet": snippet.rstrip("\n"),
            "kind": evt["type"],
        })
    return out


def _search_py(regex: re.Pattern[str], paths, context: int) -> list[dict]:
    out: list[dict] = []
    for path in paths:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        hits: set[int] = {i for i, line in enumerate(lines) if regex.search(line)}
        if not hits:
            continue
        emitted: set[int] = set()
        # Expand each hit's window, but classify kind by whether the emitted
        # line is itself a match — so a match never gets demoted to context
        # just because it falls inside an earlier hit's context window.
        for hit in sorted(hits):
            lo = max(0, hit - context)
            hi = min(len(lines), hit + context + 1)
            for idx in range(lo, hi):
                if idx in emitted:
                    continue
                emitted.add(idx)
                out.append({
                    "page": path.stem,
                    "line": idx + 1,
                    "snippet": lines[idx],
                    "kind": "match" if idx in hits else "context",
                })
    return out


def _stem(path_text: str) -> str:
    if not path_text:
        return ""
    name = path_text.rsplit("/", 1)[-1]
    return name[:-3] if name.endswith(".md") else name
