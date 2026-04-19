# Plan: Wiki Verification MCP Server

## Context

During the SRE book ingestion (34 chapters), writes and edits were pre-approved — those ran cleanly. What kept triggering permission prompts was the **post-write verification** each subagent did at the end of a chapter: `ls` to confirm new pages existed, `tail` to check the log entry, `grep` to verify cross-links resolved, `wc -l` to sanity-check page size, plus the occasional `awk`/`sed`/inline `python3`. Every chapter produced roughly five such calls, each a distinct command shape, each a separate prompt.

An audit of all 34 subagent transcripts (`~/.claude/projects/.../subagents/agent-*.jsonl`) shows **176 total Bash calls**, all read-only, clustered into six semantic tasks:

| Calls | Task |
|---|---|
| ~70 | "Does page X exist on disk after I wrote it?" (`ls`) |
| ~30 | "Is the page a reasonable length?" (`wc -l`) |
| ~30 | "Did my new cross-links resolve? Did my section heading land?" (`grep`, inline `python3`) |
| ~22 | "Did the tail of `log.md` / `index.md` look right after I appended?" (`tail`) |
| ~10 | "Where did my section end up in this long file?" (`grep -n "^## "`, `awk 'NR>=X'`) |
| ~14 | Noise: one agent's failed `git log` chain (16 calls), a few `pwd`/`echo`/`printf`/heredoc log appends |

The conclusion from the data is **not** that the server needs to absorb writes — writes already work. It needs to absorb the handful of verification commands the subagents repeatedly reach for, by exposing them as named, semantically narrow read-only tools that live under one MCP allowlist.

Goal: a local stdio MCP server (`wiki-mcp`) the wiki project registers, with a small set of read-only inspection tools that cover those six tasks. Writes continue to go through the standard Write/Edit/Bash path the user already approves.

## What gets absorbed (and what doesn't)

**Absorbed by MCP tools (read-only verification):**
- File-existence / listing under `wiki/` and `raw/`
- Frontmatter and section introspection on a wiki page
- Tailing `wiki/log.md` / `wiki/index.md`
- Link-resolution checks (do all `[[wikilink]]`s on a page, or across the whole wiki, resolve to real files?)
- Grep-scoped-to-wiki text search
- Listing section headings in a long page with line numbers

**Not absorbed — stays on the existing already-approved path:**
- Writing new wiki pages (`Write`)
- Editing existing wiki pages (`Edit`)
- Appending to `wiki/log.md` and `wiki/index.md` (`Edit`)
- `raw/` reads — `Read` already covers them; no prompt
- Anything that mutates state

**Deliberately not built:**
- Any "ingest a whole chapter" super-tool. The judgment calls (which concepts to carve out, how to phrase cross-book links, create-vs-augment) are what the subagent should keep doing.
- A lint invoker. CLAUDE.md wants lint to stay manual.
- A shell-escape tool. If I re-expose `ls`, I reintroduce prompts; the point is semantic tools.

## Alternative worth mentioning

Before building an MCP server, a cheaper fix exists: add a permissions allowlist in `.claude/settings.json` for read-only commands scoped to the wiki root —

```
"Bash(ls:/Users/tom/dev/sw-eng-llm-wiki/*)",
"Bash(wc -l:/Users/tom/dev/sw-eng-llm-wiki/wiki/*)",
"Bash(tail -*:/Users/tom/dev/sw-eng-llm-wiki/wiki/*)",
"Bash(grep:*)",
```

— which the `fewer-permission-prompts` skill is designed to produce. That removes the prompts with ~0 code. The trade-off is that the subagent keeps constructing ad-hoc shell pipelines; it doesn't get a stable, semantic interface, and there's no way to enforce "read-only" at the tool boundary — an agent could still reach for `rm` with a different command shape.

**Recommendation: build the MCP server.** Once built, future book ingestions (there are several more PDFs in `raw/` not yet ingested) get a cleaner interface. The settings allowlist alone is a five-minute patch but leaves the subagent's behaviour unchanged: it'll keep constructing pipelines and hitting edge cases (the `git log` spiral, the `python3 -c` wikilink scripts). Named tools guide the agent toward the right action.

## Tool surface

Language: **Python**, using the official `mcp` SDK, `uv`-managed, shipped as `wiki-mcp/` next to the existing `wiki-linter/` and `pdf-extractor/` projects. Python keeps the toolchain uniform and lets the server reuse `wiki-linter`'s frontmatter parser for link extraction.

Transport: **stdio**. Registered in `.mcp.json` at the repo root so contributors pick it up automatically.

All tools are read-only. All paths resolve inside the wiki / raw roots; escapes are rejected.

### Inspection tools (replacing `ls`, `wc`, `grep`, `tail`, `awk`)

1. **`wiki_page_status`** — absorbs the `ls page.md` + `wc -l page.md` pattern (~100 calls together).
   - Input: `pages: [string]` (bare page names, no `.md`).
   - Output: list of `{page, exists: bool, line_count: int?, size_bytes: int?, last_updated: string?}`.
   - One call replaces the "loop over new page names and `ls -la` each" pattern that showed up in at least 8 chapter transcripts.

2. **`wiki_tail_log`** — absorbs `tail -N wiki/log.md` (~15 calls).
   - Input: `lines: int = 30`.
   - Output: last N lines of `wiki/log.md`.

3. **`wiki_tail_index`** — absorbs `tail -N wiki/index.md` (~5 calls).
   - Input: `lines: int = 20`.
   - Output: last N lines of `wiki/index.md`.

4. **`wiki_list_sections`** — absorbs `grep -n "^## " page.md` and `grep -n "^## " | tail -N` (~10 calls).
   - Input: `page: string`.
   - Output: `[{level: int, heading: string, line: int}]` for every `##`/`###` in the page.

5. **`wiki_read_range`** — absorbs `awk 'NR>=X && NR<=Y' page.md` and `sed -n 'X,Yp' page.md` (~4 calls).
   - Input: `page: string`, `start_line: int`, `end_line: int`.
   - Output: exact text in that line range.

6. **`wiki_search`** — absorbs the general-purpose `grep pattern wiki/*.md` (~15 calls). Constrains scope to `wiki/`.
   - Input: `pattern: string`, `files: [string]? = null` (default: all wiki pages), `context: int = 0`.
   - Output: `[{page, line, snippet}]`.

### Link-resolution tool (replacing inline `python3 -c` wikilink scripts)

7. **`wiki_check_links`** — absorbs the ad-hoc wikilink resolvers subagents wrote inline with `python3 -c "…"` (at least 4 chapters did this, Ch 27 had the longest).
   - Input: `pages: [string]? = null` (default: all pages, but typical call is just the freshly-edited set).
   - Output: `[{page, missing_targets: [string]}]`. Empty list per page means all `[[links]]` resolve.

### Discovery tools (replacing `ls raw/` and full-wiki listing)

8. **`raw_list_chapters`** — absorbs `ls raw/<book>/chapter-*.md`.
   - Input: `book: string` (directory name under `raw/`).
   - Output: sorted list of chapter filenames. Numeric-aware sort (so `chapter-02` comes before `chapter-10`).

9. **`wiki_list_pages`** — absorbs `ls wiki/` (and the many `ls wiki/ | grep -iE "…"` variants).
   - Input: `name_filter: string? = null` (simple substring, no regex — the 69% common case in the transcripts).
   - Output: list of page names (no `.md`).

### Already covered — not re-exposed

- Page content reads: the standard `Read` tool is fine and doesn't prompt.
- Writes: `Write`/`Edit` already approved.
- File existence in general: the subagent tends to prefer `ls` over `Read`-with-handled-error; `wiki_page_status` gives the named alternative.

## Implementation sketch

```
wiki-mcp/
  pyproject.toml
  src/wiki_mcp/
    __init__.py
    server.py        # MCP server registration, tool dispatch
    paths.py         # resolve wiki / raw roots; reject escapes
    inspect.py       # wiki_page_status, wiki_tail_log, wiki_tail_index, wiki_list_sections, wiki_read_range
    search.py        # wiki_search (rg subprocess), wiki_list_pages
    links.py         # wiki_check_links — reuse wiki-linter's wikilink regex
    raw.py           # raw_list_chapters
  tests/
    test_inspect.py
    test_search.py
    test_links.py
    fixtures/wiki/   # sandbox wiki tree
```

Implementation points:

- **Read-only enforcement**: `paths.py` exposes only `wiki_read_path(name)` and `raw_read_path(book, chapter)`. No write helpers exist in the module at all; `server.py` has no way to mutate.
- **Link regex**: lift from `wiki-linter/lint.py` (`re.findall(r'\[\[([^\]|#]+)', content)`) so the definition of a wikilink stays single-sourced.
- **Search**: subprocess `rg --json` if ripgrep is on PATH, fall back to pure-Python scan. `wiki-linter` already depends on stdlib only; follow the same rule.
- **Sort for chapters**: natural sort via `re.split(r'(\d+)', name)` to keep `chapter-02` < `chapter-10`.
- **Caching**: none. Everything hits disk. 176 calls over a full book ingestion is trivial.

## Configuration handoff

Register the server in `.mcp.json` at repo root:

```json
{
  "mcpServers": {
    "wiki-mcp": {
      "command": "uv",
      "args": ["run", "--project", "wiki-mcp", "python", "-m", "wiki_mcp.server"],
      "env": {
        "WIKI_ROOT": "${workspaceFolder}/wiki",
        "RAW_ROOT": "${workspaceFolder}/raw"
      }
    }
  }
}
```

Allowlist the tools in `.claude/settings.json` under `permissions.allow`:

```
"mcp__wiki-mcp__wiki_page_status",
"mcp__wiki-mcp__wiki_tail_log",
"mcp__wiki-mcp__wiki_tail_index",
"mcp__wiki-mcp__wiki_list_sections",
"mcp__wiki-mcp__wiki_read_range",
"mcp__wiki-mcp__wiki_search",
"mcp__wiki-mcp__wiki_check_links",
"mcp__wiki-mcp__wiki_list_pages",
"mcp__wiki-mcp__raw_list_chapters"
```

Update `.claude/skills/ingest-book/SKILL.md` to add a one-paragraph note under the `<CRITICAL>` section: "After writing/editing pages, use the `wiki-mcp` tools (`wiki_page_status`, `wiki_check_links`, `wiki_tail_log`) for verification rather than shelling out to `ls`/`wc`/`grep`."

## Files the implementation will touch

- `wiki-mcp/` — new project directory (all new files).
- `.mcp.json` — new root-level file registering the server.
- `.claude/settings.json` — add nine allowlist entries.
- `.claude/skills/ingest-book/SKILL.md` — one-paragraph addition.
- No changes to existing wiki content.

## Reuse of existing code

- `wiki-linter/lint.py` — copy its wikilink regex and frontmatter field parsers into `wiki_mcp/links.py` and `wiki_mcp/inspect.py`. Single source of truth for what a wikilink and a frontmatter block look like. If the overlap grows, factor into a `wiki_common` package later.
- `pdf-extractor/extract.py` — no reuse.

## Verification

1. **Unit tests** (`uv run pytest wiki-mcp`): create a fixture wiki with three pages and one bad wikilink; assert each tool returns the expected shape. Target 100% branch coverage on `paths.py` (path-escape rejection).
2. **MCP protocol sanity**: spawn the server via `uv run python -m wiki_mcp.server` and use the `mcp` SDK's `stdio_client` test harness to list tools and invoke each once. Confirms the JSON-Schema input validation.
3. **Real-wiki dry-run**: point the server at `/Users/tom/dev/sw-eng-llm-wiki/wiki` and call `wiki_check_links` with no arguments. Expected: exit clean (or reveal the same issues `wiki-linter` would — which is a useful sanity check).
4. **Live ingestion rehearsal with prompt count** — run against a throwaway copy, not the real wiki.
   - `cp -R /Users/tom/dev/sw-eng-llm-wiki /tmp/wiki-rehearsal` (or `rsync -a` to preserve perms).
   - Point the MCP server at the copy by setting `WIKI_ROOT=/tmp/wiki-rehearsal/wiki` and `RAW_ROOT=/tmp/wiki-rehearsal/raw` in its env before launch.
   - Pick an un-ingested chapter from another book (e.g. a chapter from *Fundamentals of Data Engineering*), run the ingestion subagent against the copy, and tally permission prompts. Target: zero `Bash` prompts during the verification phase; writes may still prompt if not pre-approved, which is fine.
   - Nothing under `/Users/tom/dev/sw-eng-llm-wiki/` is touched; blow away `/tmp/wiki-rehearsal/` after.
5. **Linter round-trip** — also against the `/tmp` copy.
   - After the rehearsal, run `uv run python /Users/tom/dev/sw-eng-llm-wiki/wiki-linter/lint.py /tmp/wiki-rehearsal/wiki/` and confirm zero new errors introduced (compare against the linter output from the same copy *before* the rehearsal — diff should show only the changes the subagent made).
   - Cross-check that `wiki_check_links` pointed at `/tmp/wiki-rehearsal/wiki/` agrees with the linter's notion of a broken link.

If all five pass, the server is ready and the next book ingestion runs without verification-phase prompts.
