# Plan: Wiki-MCP V2 — close remaining Bash prompts

## Context

`wiki-mcp` v1 (see `WIKI-MCP-PLAN.md`) shipped before the *Fundamentals of Data Engineering* ingestion. That run touched 22 subagents and one orchestrator. Writes were pre-approved; v1's nine read-only tools were allowlisted. Yet the user was still prompted multiple times for `Bash`.

Auditing the transcripts at `~/.claude/projects/-Users-tom-dev-sw-eng-llm-wiki/5ea7bc6b-510f-4d8e-bdb5-5fff8a78b1a1/` (main session plus 22 `subagents/agent-*.jsonl`) produced this breakdown of remaining `Bash` calls:

| Calls | Pattern | Root cause |
|---:|---|---|
| 9 | `python3 -c "…open('/Users/tom/.claude/projects/.../tool-results/mcp-wiki-mcp-wiki_check_links-*.txt')…"` and `jq -r '.[] \| .text' …/tool-results/… \| python3 …` | `wiki_check_links` returns one entry per wiki page (166 pages, ~67 KB). Claude CLI materialises large tool results as files under `.claude/projects/.../tool-results/`; agents then re-parse those files to filter for entries with non-empty `missing_targets`. |
| 5 | `wc -l /…/raw/fundamentals-of-data-engineering/chapter-*.md` | `wiki_page_status` doesn't cover `raw/`. Subagents size a chapter before reading to decide whether to read it whole or in chunks. |
| 5 | `wc -l /…/wiki/{index,log,<page>}.md` | `wiki_page_status` returns `line_count`, but agents still reached for `wc`. Partial SKILL.md compliance. |
| 7 | `ls /…/wiki/` (1 with a piped `grep -iE "enc\|threat\|vpn\|…"`) | Habit; `wiki_list_pages` exists. The piped-grep call was a multi-substring filter which v1 doesn't support. |
| 3 | `tail -5 wiki/log.md`, `tail -c 200 … \| od -c` | `wiki_tail_log` exists and is allowlisted. One `od` debugging call is a true one-off. |
| 2 | `cat >> wiki/log.md << 'EOF' … EOF` (end-of-chapter log append) | `Edit` requires a prior `Read` and exact-match `old_string`; `cat >>` is easier. Writes are explicitly out of scope for wiki-mcp per v1. |
| 1 | `grep -n "FoDE Ch" wiki/index.md` | `wiki_search` covers this; single call is habit, not worth special-casing. |

Two effects dominate: **output-size pressure** on `wiki_check_links` (which the plan didn't anticipate, and which by itself accounts for the "read the agent logs in `.claude` for link analysis" behaviour the user flagged) and **gaps in coverage for `raw/`**. Everything else is long-tail habit.

## Goal

Eliminate the two dominant causes. Shrink the long tail with small, low-risk changes. Do not introduce writes into wiki-mcp.

Target: zero Bash prompts on a full-book ingestion of the next un-ingested book in `raw/`.

## What changes

### 1. `wiki_check_links` — filter to issues by default (closes 9 prompts)

The agent never wants the clean entries; it always post-filters them out. Do the filtering server-side.

- New output shape:
  ```json
  {
    "total_pages_checked": 166,
    "pages_with_issues": [
      {"page": "storage", "missing_targets": ["cold-tier"]},
      …
    ]
  }
  ```
- Add an optional `include_clean: bool = false` escape hatch for the rare case an agent wants the full matrix. Default `false` keeps the payload small.
- Preserve the `error: "page-not-found"` entry when a caller names a page that doesn't exist — that's diagnostic, not noise, so it goes into `pages_with_issues` with an empty `missing_targets` and the `error` key.

Implementation touches only `wiki-mcp/src/wiki_mcp/links.py` and the tool description in `server.py`. Update `tests/test_links.py`.

### 2. Raw-chapter introspection (closes 5 prompts)

Two design options; pick the first.

**Option A — augment `raw_list_chapters`** *(recommended)*. Today it returns `["chapter-01.md", "chapter-02.md", …]`. Change the return shape to:
```json
[
  {"chapter": "chapter-01-data-engineering-described.md", "line_count": 412, "size_bytes": 31840},
  …
]
```
One call now tells the agent which chapter is next *and* how big it is. No new tool surface; the server-side cost is a single `stat` + line-count per chapter (≤30 chapters per book).

**Option B** — new `raw_chapter_status(book, chapters: [string])` mirroring `wiki_page_status`. Rejected: 5 prompts don't justify a second tool when one existing tool can carry the data for free.

Update `raw.py`, the `raw_list_chapters` description in `server.py`, and `tests/test_raw.py` if it exists.

### 3. `wiki_list_pages` — accept multiple substrings (closes the one piped `ls | grep -iE` prompt, and pre-empts similar patterns)

Change input schema from:
```json
{ "name_filter": "string?" }
```
to:
```json
{ "name_filter": "string?", "name_filters": "string[]?" }
```
where `name_filters` is an OR-combined list of substrings (case-insensitive), and `name_filter` stays for backward compatibility. Reject callers passing both — keeps the semantics clear.

This is a 5-line change in `search.py` plus a description update.

### 4. SKILL.md — stronger wording to route `wc -l`, `ls`, `grep` through MCP (addresses the 5 wiki-side `wc` calls, most `ls` calls, the stray `grep`)

The current paragraph lists the MCP tools as an alternative. Replace with an explicit "do not use" list and a one-liner mapping:

| Don't shell out to… | Use instead |
|---|---|
| `ls wiki/` | `mcp__wiki-mcp__wiki_list_pages` |
| `ls raw/<book>/` | `mcp__wiki-mcp__raw_list_chapters` |
| `wc -l` on a wiki page | `mcp__wiki-mcp__wiki_page_status` (returns `line_count`) |
| `wc -l` on a raw chapter | `mcp__wiki-mcp__raw_list_chapters` (returns `line_count` per chapter after change #2) |
| `grep` in wiki | `mcp__wiki-mcp__wiki_search` |
| `tail wiki/log.md` or `wiki/index.md` | `mcp__wiki-mcp__wiki_tail_log` / `wiki_tail_index` |

Keep the paragraph tight. SKILL.md is already concise.

### 5. Log append — leave `cat >>` alone, but document the `Edit` pattern

Two `cat >> log.md` heredoc calls is below the bar for a wiki-mcp write tool (v1's invariant is read-only). The cheap fix: add a single line to SKILL.md: "When appending to `wiki/log.md`, use `Edit` with an `old_string` that anchors on the last existing line — do not use `cat >> … << EOF`." The agent already `Read`s `log.md` during chapter ingestion; `Edit` is viable.

If that turns out not to stick, the fallback is a settings allowlist entry:
```
"Bash(cat:/Users/tom/dev/sw-eng-llm-wiki/wiki/log.md)"
```
But try the SKILL.md nudge first — a stable tool boundary is preferable to an allowlist for a path that accepts a shell redirect.

### 6. Explicitly not changed

- `wiki_tail_log` / `wiki_tail_index` / `wiki_read_range` / `wiki_list_sections` — already absorb their targets.
- Raw-content reads — `Read` handles them without prompts.
- The `tail … | od` debugging one-off — not worth a tool.

## Files touched

- `wiki-mcp/src/wiki_mcp/links.py` — filter + `include_clean` param.
- `wiki-mcp/src/wiki_mcp/raw.py` — return dicts with `line_count`, `size_bytes`.
- `wiki-mcp/src/wiki_mcp/search.py` — add `name_filters` branch in `wiki_list_pages`.
- `wiki-mcp/src/wiki_mcp/server.py` — update three input schemas and tool descriptions (`wiki_check_links`, `raw_list_chapters`, `wiki_list_pages`).
- `wiki-mcp/tests/test_links.py`, `test_raw.py`, `test_search.py` — update expectations.
- `.claude/skills/ingest-book/SKILL.md` — replace the guidance paragraph with the mapping table and the log-append note.
- No changes to `.claude/settings.json` (the existing allowlist still covers the tool names; tool inputs/outputs change but allowlist is per-tool-name).
- No changes to `wiki/`.

## Backward compatibility

All three tool-shape changes are breaking for any external consumer. There are none — the server is only called from this repo's subagents. The skill update lands in the same commit, and the next ingestion will use the new shapes from the first call.

If the user ever reruns an old subagent transcript against this server, `wiki_check_links` output will differ and `raw_list_chapters` returns dicts instead of strings. Acceptable.

## Verification

1. **Unit tests** — `uv run --project wiki-mcp pytest`. Assert `wiki_check_links` returns the new `{total_pages_checked, pages_with_issues}` shape with a 3-page fixture; `include_clean=true` returns per-page entries. Assert `raw_list_chapters` returns dicts with `line_count` matching a fixture chapter's real line count. Assert `wiki_list_pages(name_filters=["x","y"])` returns the OR-union, and passing both `name_filter` and `name_filters` raises.
2. **MCP protocol sanity** — spawn the server, list tools, call each changed tool once. Confirms the JSON-Schema validation accepts the new inputs.
3. **Size check on the real wiki** — call `wiki_check_links` against `/Users/tom/dev/sw-eng-llm-wiki/wiki` and measure the response size. Target: under 4 KB in the default case (was ~67 KB). If current wiki has no issues at all, the response should be ~50 bytes.
4. **Rehearsal on a `/tmp` copy** — same protocol as the v1 plan's step 4. `rsync -a` the repo to `/tmp/wiki-rehearsal`, point the server's `WIKI_ROOT`/`RAW_ROOT` at the copy, pick an un-ingested chapter from another book (e.g. *The Pragmatic Programmer* if present, else a chapter skipped during the FoDE run), and run `/ingest-book` against the copy. Tally Bash prompts. Target: zero during verification; writes may still prompt.
5. **Linter round-trip** — after the rehearsal, `uv run python wiki-linter/lint.py /tmp/wiki-rehearsal/wiki/` should show zero new errors vs. the pre-rehearsal baseline; `wiki_check_links` and the linter must agree on the set of broken links.

If all five pass, the next real book ingestion should run clean.

## Rollout

One commit per numbered change, in order. Each is independently revertable. Run tests after each. Commit #4 (SKILL.md) lands with whichever code commit it depends on to avoid a window where the skill points at a tool shape that doesn't exist yet.
