import subprocess

import pytest

from wiki_mcp import search as search_module
from wiki_mcp.raw import _natural_key, raw_list_chapters
from wiki_mcp.search import wiki_list_pages, wiki_search


def test_list_pages_all(sandbox):
    pages = wiki_list_pages()
    assert pages == ["alpha", "beta", "gamma", "index", "log"]


def test_list_pages_filter(sandbox):
    assert wiki_list_pages("alph") == ["alpha"]
    assert wiki_list_pages("zzz") == []


def test_list_pages_name_filters_or_union(sandbox):
    # alpha and gamma, not beta — union of two substrings.
    assert wiki_list_pages(name_filters=["alph", "gamm"]) == ["alpha", "gamma"]


def test_list_pages_name_filters_empty_list_returns_all(sandbox):
    # An empty or all-empty-string filter list must not filter anything out.
    assert wiki_list_pages(name_filters=[]) == ["alpha", "beta", "gamma", "index", "log"]
    assert wiki_list_pages(name_filters=[""]) == ["alpha", "beta", "gamma", "index", "log"]


def test_list_pages_rejects_both_filters(sandbox):
    with pytest.raises(ValueError, match="name_filter"):
        wiki_list_pages(name_filter="a", name_filters=["b"])


def test_search_finds_match(sandbox):
    hits = wiki_search("orphaned")
    assert any(h["page"] == "gamma" and "orphaned" in h["snippet"] for h in hits)


def test_search_respects_files_filter(sandbox):
    hits = wiki_search("Summary", files=["alpha"])
    assert all(h["page"] == "alpha" for h in hits)


def test_search_empty_pattern(sandbox):
    assert wiki_search("") == []


def test_raw_list_chapters_natural_sort(sandbox):
    chapters = raw_list_chapters("fake")
    names = [c["chapter"] for c in chapters]
    assert names == ["chapter-01.md", "chapter-02.md", "chapter-03.md", "chapter-10.md"]


def test_raw_list_chapters_reports_line_count_and_size(sandbox):
    chapters = raw_list_chapters("fake")
    # Sandbox writes single-line files like "# chapter-01.md\n".
    for entry in chapters:
        assert set(entry.keys()) == {"chapter", "line_count", "size_bytes"}
        assert entry["line_count"] == 1
        # "# chapter-01.md\n" → 17 bytes, etc. Just check non-zero and sensible.
        assert entry["size_bytes"] > 0
    # Verify a real chapter path to cross-check line count against disk.
    ch1 = next(c for c in chapters if c["chapter"] == "chapter-01.md")
    assert ch1["line_count"] == 1


def test_search_empty_files_list_returns_nothing(sandbox):
    # An explicit empty list must NOT silently fall through to "all pages".
    assert wiki_search("Summary", files=[]) == []


def test_search_invalid_regex_raises_value_error(sandbox):
    with pytest.raises(ValueError, match="Invalid regex"):
        wiki_search("[unclosed")


def test_search_match_in_prior_context_window_stays_classified_as_match(tmp_path, monkeypatch):
    wiki = tmp_path / "wiki"
    wiki.mkdir()
    (wiki / "x.md").write_text(
        "alpha\nbeta\ngamma\ndelta\nbeta\nepsilon\n", encoding="utf-8"
    )
    monkeypatch.setenv("WIKI_ROOT", str(wiki))
    monkeypatch.setenv("RAW_ROOT", str(tmp_path))

    results = wiki_search("beta", context=3)
    by_line = {r["line"]: r["kind"] for r in results}
    # Both "beta" lines must be classified as matches, even though line 5
    # falls inside the context window that the line-2 hit opens up.
    assert by_line[2] == "match"
    assert by_line[5] == "match"


def test_natural_key_stable_across_digit_and_nondigit_prefixes():
    # Regression: mixing int and str at the same tuple index used to raise
    # TypeError under the old tuple-based key.
    names = ["foreword.md", "1-chapter.md", "chapter-01.md", "chapter-2.md"]
    # Must not raise — with the old tuple-based key this comparison threw.
    names.sort(key=_natural_key)
    # Sanity checks on natural ordering.
    assert _natural_key("chapter-01.md") < _natural_key("chapter-2.md")  # 1 < 2
    assert _natural_key("chapter-2.md") < _natural_key("chapter-10.md")  # 2 < 10


def test_search_rg_path_parses_json(sandbox, monkeypatch):
    """With a fake `rg` on PATH, _search_rg must parse ripgrep's JSON stream."""
    captured = {}

    def fake_which(name):
        return "/usr/local/bin/rg" if name == "rg" else None

    def fake_run(cmd, capture_output, text, check):
        captured["cmd"] = cmd
        stdout = (
            '{"type":"begin","data":{"path":{"text":"/tmp/alpha.md"}}}\n'
            '{"type":"match","data":{"path":{"text":"/tmp/alpha.md"},'
            '"lines":{"text":"hit line\\n"},"line_number":7,"submatches":[]}}\n'
            '{"type":"context","data":{"path":{"text":"/tmp/alpha.md"},'
            '"lines":{"text":"after\\n"},"line_number":8,"submatches":[]}}\n'
            '{"type":"end","data":{"path":{"text":"/tmp/alpha.md"}}}\n'
            "not-json-should-be-skipped\n"
        )
        return subprocess.CompletedProcess(cmd, 0, stdout=stdout, stderr="")

    monkeypatch.setattr(search_module.shutil, "which", fake_which)
    monkeypatch.setattr(search_module.subprocess, "run", fake_run)

    results = wiki_search("anything", files=["alpha"])
    assert [r["kind"] for r in results] == ["match", "context"]
    assert results[0] == {"page": "alpha", "line": 7, "snippet": "hit line", "kind": "match"}
    assert results[1]["line"] == 8
    # Sanity-check that we passed --json and the file list to rg.
    assert "--json" in captured["cmd"]
    assert captured["cmd"][-2] == "--"


def test_search_rg_regex_error_surfaces_as_value_error(sandbox, monkeypatch):
    """Invalid regex must raise ValueError whether or not rg is available."""
    monkeypatch.setattr(search_module.shutil, "which", lambda name: "/usr/local/bin/rg")
    # subprocess.run should never be reached — pre-validation catches it.
    monkeypatch.setattr(
        search_module.subprocess, "run",
        lambda *a, **k: pytest.fail("rg should not be invoked with an invalid pattern"),
    )
    with pytest.raises(ValueError, match="Invalid regex"):
        wiki_search("[unclosed", files=["alpha"])
