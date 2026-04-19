"""Shared fixtures: a small in-tree wiki/raw sandbox for tool tests."""

from __future__ import annotations

import os
from pathlib import Path

import pytest


def _write(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


@pytest.fixture
def sandbox(tmp_path, monkeypatch):
    wiki = tmp_path / "wiki"
    raw = tmp_path / "raw"
    wiki.mkdir()
    raw.mkdir()

    _write(wiki / "alpha.md", (
        "# Alpha\n"
        "\n"
        "**Summary**: Alpha page.\n"
        "**Sources**: `raw/fake/chapter-01.md`\n"
        "**Last updated**: 2026-04-18\n"
        "\n"
        "---\n"
        "\n"
        "Alpha links to [[beta]] and a missing [[ghost]] and a fenced\n"
        "```\n"
        "code [[not-a-link]]\n"
        "```\n"
        "block.\n"
        "\n"
        "## Section One\n"
        "\n"
        "Text.\n"
        "\n"
        "### Sub A\n"
        "\n"
        "More.\n"
        "\n"
        "## Related pages\n"
        "\n"
        "- [[beta]]\n"
    ))

    _write(wiki / "beta.md", (
        "# Beta\n"
        "\n"
        "**Summary**: Beta page.\n"
        "**Sources**: `raw/fake/chapter-02.md`\n"
        "**Last updated**: 2026-04-17\n"
        "\n"
        "---\n"
        "\n"
        "Beta references [[alpha]] but nothing missing.\n"
        "\n"
        "## Related pages\n"
        "\n"
        "- [[alpha]]\n"
    ))

    _write(wiki / "gamma.md", (
        "# Gamma\n"
        "\n"
        "**Summary**: Gamma page.\n"
        "**Sources**: `raw/fake/chapter-03.md`\n"
        "**Last updated**: 2026-04-16\n"
        "\n"
        "---\n"
        "\n"
        "Gamma is orphaned.\n"
        "\n"
        "## Related pages\n"
        "\n"
        "- [[alpha]]\n"
    ))

    _write(wiki / "index.md", (
        "# Index\n\n"
        "- [[alpha]]\n"
        "- [[beta]]\n"
        "- [[gamma]]\n"
    ))

    _write(wiki / "log.md", (
        "# Log\n\n"
        "2026-04-15 — seeded wiki.\n"
        "2026-04-17 — added beta.\n"
        "2026-04-18 — added alpha.\n"
    ))

    # raw/fake/ with natural-sort chapters.
    (raw / "fake").mkdir()
    for name in ["chapter-01.md", "chapter-02.md", "chapter-10.md", "chapter-03.md"]:
        _write(raw / "fake" / name, f"# {name}\n")

    monkeypatch.setenv("WIKI_ROOT", str(wiki))
    monkeypatch.setenv("RAW_ROOT", str(raw))

    yield {"wiki": wiki, "raw": raw}
