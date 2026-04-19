from pathlib import Path

import pytest

from wiki_mcp.paths import PathEscape, raw_read_path, wiki_read_path, wiki_root


def test_wiki_read_path_accepts_plain_name(sandbox):
    p = wiki_read_path("alpha")
    assert p.name == "alpha.md"
    assert p.exists()


def test_wiki_read_path_accepts_md_suffix(sandbox):
    p = wiki_read_path("alpha.md")
    assert p.name == "alpha.md"


def test_wiki_read_path_rejects_traversal(sandbox):
    with pytest.raises(PathEscape):
        wiki_read_path("../raw/fake/chapter-01")


def test_wiki_read_path_rejects_slash(sandbox):
    with pytest.raises(PathEscape):
        wiki_read_path("subdir/alpha")


def test_wiki_read_path_rejects_dot(sandbox):
    with pytest.raises(PathEscape):
        wiki_read_path("..")


def test_raw_read_path_requires_book(sandbox):
    with pytest.raises(PathEscape):
        raw_read_path("")


def test_raw_read_path_rejects_slash_in_book(sandbox):
    with pytest.raises(PathEscape):
        raw_read_path("fake/chapter-01.md")


def test_raw_read_path_returns_book_dir(sandbox):
    p = raw_read_path("fake")
    assert p.is_dir()


def test_wiki_root_falls_back_to_repo_when_env_unset(monkeypatch, tmp_path):
    """With no WIKI_ROOT set, we must resolve to the real repo's wiki/ — not cwd.

    This is the regression guard for the silent-empty-wiki failure mode: if
    Claude Code ever launches the server from a cwd that isn't the repo root,
    we still find the right wiki.
    """
    monkeypatch.delenv("WIKI_ROOT", raising=False)
    monkeypatch.chdir(tmp_path)  # cwd that contains no wiki/

    resolved = wiki_root()
    # Derived from this test file's location, independent of the test's cwd.
    expected = Path(__file__).resolve().parents[2] / "wiki"
    assert resolved == expected.resolve()


def test_wiki_root_falls_through_to_cwd_when_repo_dir_missing(monkeypatch, tmp_path):
    """If the repo-relative default isn't a directory, we fall through to cwd.

    Simulated by pointing the default at a name that won't exist at the repo
    root (so the first branch of the fallback fails).
    """
    monkeypatch.delenv("WIKI_ROOT", raising=False)
    (tmp_path / "custom-wiki-name").mkdir()
    monkeypatch.chdir(tmp_path)

    # The "wiki" default would succeed via the repo-relative branch, so we
    # exercise the fall-through by calling _resolve_root directly with a name
    # that doesn't exist at the repo root.
    from wiki_mcp.paths import _resolve_root

    resolved = _resolve_root("NONEXISTENT_ENV", "custom-wiki-name")
    assert resolved == (tmp_path / "custom-wiki-name").resolve()


def test_wiki_read_path_rejects_symlink_to_outside(tmp_path, monkeypatch):
    """A symlink inside the wiki that points outside the wiki must be rejected."""
    wiki = tmp_path / "wiki"
    wiki.mkdir()
    outside = tmp_path / "outside.md"
    outside.write_text("leak", encoding="utf-8")
    (wiki / "evil.md").symlink_to(outside)
    monkeypatch.setenv("WIKI_ROOT", str(wiki))
    monkeypatch.setenv("RAW_ROOT", str(tmp_path))

    with pytest.raises(PathEscape):
        wiki_read_path("evil")
