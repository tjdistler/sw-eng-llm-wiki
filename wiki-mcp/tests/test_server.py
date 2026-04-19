"""Smoke test: spawn the server and talk MCP over stdio."""

from __future__ import annotations

import os
import sys

import pytest

pytestmark = pytest.mark.anyio

try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
except ImportError:  # pragma: no cover
    pytest.skip("mcp client APIs unavailable", allow_module_level=True)


@pytest.fixture
def anyio_backend():
    return "asyncio"


async def _exercise(sandbox):
    env = {
        **os.environ,
        "WIKI_ROOT": str(sandbox["wiki"]),
        "RAW_ROOT": str(sandbox["raw"]),
    }
    params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "wiki_mcp.server"],
        env=env,
    )
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            names = {t.name for t in tools.tools}
            assert {
                "wiki_page_status",
                "wiki_tail_log",
                "wiki_tail_index",
                "wiki_list_sections",
                "wiki_read_range",
                "wiki_search",
                "wiki_check_links",
                "wiki_list_pages",
                "raw_list_chapters",
            } == names

            result = await session.call_tool(
                "wiki_page_status", {"pages": ["alpha", "nonexistent"]}
            )
            assert not result.isError
            payload = result.content[0].text
            assert '"alpha"' in payload
            assert '"exists": true' in payload


async def test_stdio_roundtrip(sandbox):
    await _exercise(sandbox)
