from wiki_mcp.links import wiki_check_links


def test_missing_target_reported(sandbox):
    result = wiki_check_links(["alpha"])
    issues = result["pages_with_issues"]
    alpha = next(r for r in issues if r["page"] == "alpha")
    assert "ghost" in alpha["missing_targets"]
    # [[beta]] is a real page — it must not be flagged
    assert "beta" not in alpha["missing_targets"]
    # fenced-code pseudo-link must not be flagged
    assert "not-a-link" not in alpha["missing_targets"]


def test_all_pages_when_none_passed_filters_clean_by_default(sandbox):
    result = wiki_check_links()
    assert result["total_pages_checked"] >= 3
    issue_pages = {r["page"] for r in result["pages_with_issues"]}
    # alpha has a missing [[ghost]] — it must surface.
    assert "alpha" in issue_pages
    # beta is clean — it must NOT surface in the filtered default.
    assert "beta" not in issue_pages


def test_include_clean_returns_per_page_entries(sandbox):
    results = wiki_check_links(include_clean=True)
    assert isinstance(results, list)
    pages = {r["page"] for r in results}
    assert {"alpha", "beta", "gamma"}.issubset(pages)
    beta = next(r for r in results if r["page"] == "beta")
    assert beta["missing_targets"] == []


def test_duplicate_targets_deduplicated(sandbox):
    result = wiki_check_links(["alpha"])
    alpha = next(r for r in result["pages_with_issues"] if r["page"] == "alpha")
    assert alpha["missing_targets"].count("ghost") == 1


def test_page_not_found_surfaces_as_issue(sandbox):
    result = wiki_check_links(["does-not-exist"])
    issues = result["pages_with_issues"]
    assert len(issues) == 1
    assert issues[0]["page"] == "does-not-exist"
    assert issues[0]["error"] == "page-not-found"
    assert issues[0]["missing_targets"] == []
