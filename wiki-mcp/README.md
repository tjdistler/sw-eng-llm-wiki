# wiki-mcp

Read-only MCP server exposing verification tools for the `wiki/` knowledge base. Lets Claude Code confirm page existence, tail the log/index, inspect sections, read line ranges, search, and check wiki-links without spawning a shell for each lookup.

## Usage

Claude Code launches the server automatically via `.mcp.json` at the repo root:

```json
{
  "mcpServers": {
    "wiki-mcp": {
      "command": "uv",
      "args": ["run", "--project", "wiki-mcp", "python", "-m", "wiki_mcp.server"]
    }
  }
}
```

First-time setup:

```bash
cd wiki-mcp
uv sync
```

Run the stdio server manually (for debugging):

```bash
uv run python -m wiki_mcp.server
```

## Tools

| Tool | Purpose |
|------|---------|
| `wiki_page_status` | Check page existence; report line count, size, `**Last updated**`. |
| `wiki_tail_log` | Last N lines of `wiki/log.md`. |
| `wiki_tail_index` | Last N lines of `wiki/index.md`. |
| `wiki_list_sections` | All `##`+ headings in a page, with level and line number. |
| `wiki_read_range` | Exact text between two 1-indexed line numbers (inclusive). |
| `wiki_search` | Regex search scoped to `wiki/` (ripgrep if available, else pure Python). |
| `wiki_check_links` | Resolve every `[[wikilink]]` and report broken targets. |
| `wiki_list_pages` | List all wiki pages, optional substring filter. |
| `raw_list_chapters` | List chapter files under `raw/<book>/`, naturally sorted. |

All tools are read-only. The module intentionally exposes no write helpers.

## Configuration

| Env var | Default | Purpose |
|---------|---------|---------|
| `WIKI_ROOT` | `<repo>/wiki` | Override the wiki directory. |
| `RAW_ROOT` | `<repo>/raw` | Override the raw source directory. |

Paths are resolved relative to the repo the server ships inside, so `cwd` drift does not silently produce empty results. Page and book names may not contain path separators or `..` segments — escapes raise `PathEscape`.

## Tests

```bash
uv run pytest
```
