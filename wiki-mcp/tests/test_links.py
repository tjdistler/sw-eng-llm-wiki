from wiki_mcp.links import wiki_check_links


def test_missing_target_reported(sandbox):
    results = wiki_check_links(["alpha"])
    alpha = next(r for r in results if r["page"] == "alpha")
    assert "ghost" in alpha["missing_targets"]
    # [[beta]] is a real page — it must not be flagged
    assert "beta" not in alpha["missing_targets"]
    # fenced-code pseudo-link must not be flagged
    assert "not-a-link" not in alpha["missing_targets"]


def test_all_pages_when_none_passed(sandbox):
    results = wiki_check_links()
    pages = {r["page"] for r in results}
    assert {"alpha", "beta", "gamma"}.issubset(pages)
    beta = next(r for r in results if r["page"] == "beta")
    assert beta["missing_targets"] == []


def test_duplicate_targets_deduplicated(sandbox):
    results = wiki_check_links(["alpha"])
    alpha = next(r for r in results if r["page"] == "alpha")
    assert alpha["missing_targets"].count("ghost") == 1
