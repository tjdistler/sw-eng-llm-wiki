"""MCP stdio server exposing read-only wiki verification tools."""

from __future__ import annotations

import asyncio
import json
from typing import Any, Callable

import mcp.types as types
from mcp.server import Server
from mcp.server.stdio import stdio_server

from . import inspect as wiki_inspect
from . import links as wiki_links
from . import raw as wiki_raw
from . import search as wiki_search


TOOL_SPECS: list[dict[str, Any]] = [
    {
        "name": "wiki_page_status",
        "description": (
            "Check whether one or more wiki pages exist on disk, and report "
            "line count, size, and **Last updated** date for each that does."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "pages": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Page names (with or without `.md`).",
                    "minItems": 1,
                }
            },
            "required": ["pages"],
            "additionalProperties": False,
        },
    },
    {
        "name": "wiki_tail_log",
        "description": "Return the last N lines of `wiki/log.md`.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "lines": {"type": "integer", "minimum": 1, "default": 30}
            },
            "additionalProperties": False,
        },
    },
    {
        "name": "wiki_tail_index",
        "description": "Return the last N lines of `wiki/index.md`.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "lines": {"type": "integer", "minimum": 1, "default": 20}
            },
            "additionalProperties": False,
        },
    },
    {
        "name": "wiki_list_sections",
        "description": (
            "List every `##`/`###`+ heading in a wiki page, with level and "
            "line number. Covers the `grep -n '^## ' page.md` pattern."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "page": {"type": "string", "description": "Page name (with or without `.md`)."}
            },
            "required": ["page"],
            "additionalProperties": False,
        },
    },
    {
        "name": "wiki_read_range",
        "description": "Return the exact text of a wiki page between two 1-indexed line numbers (inclusive).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "page": {"type": "string"},
                "start_line": {"type": "integer", "minimum": 1},
                "end_line": {"type": "integer", "minimum": 1},
            },
            "required": ["page", "start_line", "end_line"],
            "additionalProperties": False,
        },
    },
    {
        "name": "wiki_search",
        "description": (
            "Regex search across the wiki (scoped to `wiki/`). Returns page, line, "
            "and snippet per hit. Uses ripgrep if available, otherwise pure Python."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "pattern": {"type": "string"},
                "files": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional subset of page names to search. Defaults to all wiki pages.",
                },
                "context": {
                    "type": "integer",
                    "minimum": 0,
                    "default": 0,
                    "description": "Lines of surrounding context per match.",
                },
            },
            "required": ["pattern"],
            "additionalProperties": False,
        },
    },
    {
        "name": "wiki_check_links",
        "description": (
            "Resolve every `[[wikilink]]` across the given pages (default: all pages) "
            "and report any that point at a page that does not exist. Ignores anchors. "
            "By default returns `{total_pages_checked, pages_with_issues}` — only pages "
            "with missing targets or a `page-not-found` error appear in `pages_with_issues`. "
            "Pass `include_clean: true` to get the full per-page list instead."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "pages": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional subset of page names. Defaults to all wiki pages.",
                },
                "include_clean": {
                    "type": "boolean",
                    "default": False,
                    "description": "If true, return one entry per page (including clean pages) instead of the filtered summary.",
                },
            },
            "additionalProperties": False,
        },
    },
    {
        "name": "wiki_list_pages",
        "description": (
            "List every wiki page (no `.md` suffix). Optional substring filter. "
            "Use `name_filter` for a single substring, or `name_filters` for an "
            "OR-combined list of substrings (case-insensitive either way). Passing "
            "both is an error."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "name_filter": {
                    "type": "string",
                    "description": "Single case-insensitive substring filter.",
                },
                "name_filters": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "OR-combined list of case-insensitive substrings.",
                },
            },
            "additionalProperties": False,
        },
    },
    {
        "name": "raw_list_chapters",
        "description": (
            "List chapter markdown files under a raw/<book>/ directory, naturally sorted. "
            "Each entry includes `chapter`, `line_count`, and `size_bytes` so callers can "
            "decide whether to read a chapter whole or in chunks without shelling out to `wc -l`."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "book": {"type": "string", "description": "Directory name under raw/."}
            },
            "required": ["book"],
            "additionalProperties": False,
        },
    },
]


Handler = Callable[[dict[str, Any]], Any]


def _dispatch() -> dict[str, Handler]:
    return {
        "wiki_page_status": lambda a: wiki_inspect.wiki_page_status(a["pages"]),
        "wiki_tail_log": lambda a: wiki_inspect.wiki_tail_log(a.get("lines", 30)),
        "wiki_tail_index": lambda a: wiki_inspect.wiki_tail_index(a.get("lines", 20)),
        "wiki_list_sections": lambda a: wiki_inspect.wiki_list_sections(a["page"]),
        "wiki_read_range": lambda a: wiki_inspect.wiki_read_range(
            a["page"], a["start_line"], a["end_line"]
        ),
        "wiki_search": lambda a: wiki_search.wiki_search(
            a["pattern"], a.get("files"), a.get("context", 0)
        ),
        "wiki_check_links": lambda a: wiki_links.wiki_check_links(
            a.get("pages"), a.get("include_clean", False)
        ),
        "wiki_list_pages": lambda a: wiki_search.wiki_list_pages(
            a.get("name_filter"), a.get("name_filters")
        ),
        "raw_list_chapters": lambda a: wiki_raw.raw_list_chapters(a["book"]),
    }


def build_server() -> Server:
    server: Server = Server("wiki-mcp")
    dispatch = _dispatch()

    @server.list_tools()
    async def list_tools() -> list[types.Tool]:
        return [
            types.Tool(
                name=spec["name"],
                description=spec["description"],
                inputSchema=spec["inputSchema"],
            )
            for spec in TOOL_SPECS
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict[str, Any]) -> list[types.TextContent]:
        handler = dispatch.get(name)
        if handler is None:
            raise ValueError(f"Unknown tool: {name}")
        result = handler(arguments or {})
        payload = _to_text(result)
        return [types.TextContent(type="text", text=payload)]

    return server


def _to_text(result: Any) -> str:
    if isinstance(result, str):
        return result
    return json.dumps(result, indent=2, ensure_ascii=False)


async def _run() -> None:
    server = build_server()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


def main() -> None:
    asyncio.run(_run())


if __name__ == "__main__":
    main()
