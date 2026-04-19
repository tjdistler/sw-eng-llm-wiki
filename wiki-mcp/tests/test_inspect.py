from wiki_mcp.inspect import (
    wiki_list_sections,
    wiki_page_status,
    wiki_read_range,
    wiki_tail_index,
    wiki_tail_log,
)


def test_page_status_existing_and_missing(sandbox):
    out = wiki_page_status(["alpha", "beta.md", "nonexistent"])
    by_name = {r["page"]: r for r in out}
    assert by_name["alpha"]["exists"] is True
    assert by_name["alpha"]["line_count"] > 0
    assert by_name["alpha"]["size_bytes"] > 0
    assert by_name["alpha"]["last_updated"] == "2026-04-18"
    assert by_name["beta.md"]["exists"] is True
    assert by_name["nonexistent"]["exists"] is False
    assert by_name["nonexistent"]["line_count"] is None


def test_page_status_rejects_escape_silently(sandbox):
    out = wiki_page_status(["../raw/fake/chapter-01"])
    assert out[0]["exists"] is False


def test_tail_log_default(sandbox):
    text = wiki_tail_log(2)
    lines = text.splitlines()
    assert len(lines) == 2
    assert lines[-1] == "2026-04-18 — added alpha."


def test_tail_index(sandbox):
    text = wiki_tail_index(3)
    assert "gamma" in text


def test_list_sections_returns_levels_and_lines(sandbox):
    out = wiki_list_sections("alpha")
    levels = [(s["level"], s["heading"]) for s in out]
    assert (2, "Section One") in levels
    assert (3, "Sub A") in levels
    assert (2, "Related pages") in levels
    # all line numbers positive and ascending
    nums = [s["line"] for s in out]
    assert nums == sorted(nums)
    assert all(n > 0 for n in nums)


def test_read_range_inclusive(sandbox):
    out = wiki_read_range("alpha", 1, 1)
    assert out == "# Alpha"
    body = wiki_read_range("alpha", 1, 3)
    assert body.count("\n") == 2
