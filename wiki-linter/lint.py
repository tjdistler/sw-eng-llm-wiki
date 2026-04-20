"""wiki-linter — deterministic structural linter for the sw-eng-llm-wiki.

Runs read-only checks that a Python script can verify reliably:
page format, wikilink integrity, orphans, index sync, citation validity,
filename convention, and `**Last updated**` parseability.

Semantic checks (contradictions, outdated claims, missing-concept judgement)
are out of scope by design — the user handles those on the linter's report.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path


SEVERITY_ORDER = {"error": 0, "warning": 1, "info": 2}
IGNORED_PAGES = {"index.md", "log.md"}
INBOUND_EXCLUDED_SOURCES = {"index.md", "log.md"}  # meta-pages; links from them don't rescue an orphan
MOC_PREFIX = "moc-"
META_PAGE_NAMES = {"index.md", "log.md", "question-patterns.md"}
CANONICAL_RELATED_LABELS = ("Prerequisite", "Generalizes", "Alternative", "Contrast", "See also")

WIKILINK_RE = re.compile(r"\[\[([^\]\[|#]*)(?:#([^\]\[|]+))?(?:\|([^\]\[]+))?\]\]")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
SUMMARY_RE = re.compile(r"^\*\*Summary\*\*:\s*(.+?)\s*$")
SOURCES_RE = re.compile(r"^\*\*Sources\*\*:\s*(.*)$")
LAST_UPDATED_RE = re.compile(r"^\*\*Last updated\*\*:\s*(\S+)\s*$")
BACKTICK_SPAN_RE = re.compile(r"`([^`]+)`")
INLINE_SOURCE_RE = re.compile(r"\(source:\s*([^)]+?)\)")
VALID_FILENAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*\.md$")
RELATED_BULLET_LABEL_RE = re.compile(r"^\s*-\s+\*\*([^*]+?):\*\*")
SLUG_QUOTE_RE = re.compile(r"[\u2018\u2019\u201C\u201D'\"`]")  # stripped before dashification
SLUG_NORMALIZE_RE = re.compile(r"[^a-z0-9]+")


@dataclass
class Finding:
    severity: str
    check: str
    page: str
    line: int | None
    message: str
    suggestion: str | None = None


@dataclass
class Link:
    target: str          # "" means same-page anchor
    anchor: str | None
    label: str | None
    line: int


@dataclass
class Page:
    path: Path
    name: str
    stem: str
    text: str
    lines: list[str]
    title: str | None = None
    summary_line: int | None = None
    sources_line: int | None = None
    sources_files: list[str] = field(default_factory=list)
    last_updated_line: int | None = None
    last_updated: str | None = None
    divider_line: int | None = None
    related_pages_line: int | None = None
    headings: list[tuple[int, int, str]] = field(default_factory=list)
    outbound: list[Link] = field(default_factory=list)
    inline_sources: list[tuple[int, str]] = field(default_factory=list)


def slugify(s: str) -> str:
    s = SLUG_QUOTE_RE.sub("", s.lower())
    return SLUG_NORMALIZE_RE.sub("-", s).strip("-")


def is_moc_page(name_or_stem: str) -> bool:
    """True for `moc-*.md` filenames and their stems (`moc-*`)."""
    return name_or_stem.startswith(MOC_PREFIX)


def is_meta_page(name: str) -> bool:
    """True for filenames that are navigational / meta (not concept pages).

    Covers `index.md`, `log.md`, `question-patterns.md`, and any `moc-*.md`.
    """
    return name in META_PAGE_NAMES or (name.startswith(MOC_PREFIX) and name.endswith(".md"))


def strip_noise(text: str) -> str:
    """Zero out fenced code blocks so they don't yield false-positive wikilinks.

    Line numbers are preserved by substituting blank lines.
    """
    out: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            out.append("")
            continue
        out.append("" if in_fence else line)
    return "\n".join(out)


def parse_page(path: Path) -> Page:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    page = Page(path=path, name=path.name, stem=path.stem, text=text, lines=lines)

    for i, line in enumerate(lines, start=1):
        if page.title is None and line.startswith("# "):
            page.title = line[2:].strip()
        if page.summary_line is None and SUMMARY_RE.match(line):
            page.summary_line = i
        m_src = SOURCES_RE.match(line)
        if m_src and page.sources_line is None:
            page.sources_line = i
            page.sources_files = BACKTICK_SPAN_RE.findall(m_src.group(1))
        m_upd = LAST_UPDATED_RE.match(line)
        if m_upd and page.last_updated_line is None:
            page.last_updated_line = i
            page.last_updated = m_upd.group(1)
        if page.divider_line is None and line.strip() == "---" and i > 1:
            page.divider_line = i
        if page.related_pages_line is None and line.strip().lower() == "## related pages":
            page.related_pages_line = i
        m_h = HEADING_RE.match(line)
        if m_h:
            page.headings.append((i, len(m_h.group(1)), m_h.group(2).strip()))

    scrubbed = strip_noise(text)
    for i, line in enumerate(scrubbed.splitlines(), start=1):
        for m in WIKILINK_RE.finditer(line):
            target = m.group(1).strip().rstrip("\\")
            anchor = m.group(2).strip().rstrip("\\") if m.group(2) else None
            label = m.group(3).strip() if m.group(3) else None
            page.outbound.append(Link(target=target, anchor=anchor, label=label, line=i))
        for m in INLINE_SOURCE_RE.finditer(line):
            page.inline_sources.append((i, m.group(1).strip()))

    return page


def check_page_format(page: Page) -> list[Finding]:
    findings: list[Finding] = []
    required = [
        (page.title is None, 1, "page-format", "Missing top-level `# Title` heading",
         "Add `# Page Title` as the first line"),
        (page.summary_line is None, None, "page-format", "Missing `**Summary**:` line",
         "Add a `**Summary**: …` line after the title"),
        (page.sources_line is None, None, "page-format", "Missing `**Sources**:` line",
         "Add a `**Sources**: …` line listing the raw/ files this page draws from"),
        (page.last_updated_line is None, None, "page-format", "Missing `**Last updated**:` line",
         "Add a `**Last updated**: YYYY-MM-DD` line"),
        (page.divider_line is None, None, "page-format", "Missing `---` divider after frontmatter",
         "Add a `---` line between frontmatter and body"),
        (page.related_pages_line is None, None, "page-format", "Missing `## Related pages` section",
         "Add a `## Related pages` section with `[[links]]` to related concepts"),
    ]
    for condition, line, check, msg, sug in required:
        if condition:
            findings.append(Finding("error", check, page.name, line, msg, sug))
    return findings


def check_last_updated(page: Page, today: date) -> list[Finding]:
    if page.last_updated is None:
        return []
    try:
        parsed = datetime.strptime(page.last_updated, "%Y-%m-%d").date()
    except ValueError:
        return [Finding("error", "date", page.name, page.last_updated_line,
                        f"Invalid `**Last updated**` value: {page.last_updated!r}",
                        "Use `YYYY-MM-DD` format")]
    if parsed > today:
        return [Finding("error", "date", page.name, page.last_updated_line,
                        f"`**Last updated**` is in the future: {page.last_updated}",
                        "Correct the date to today or earlier")]
    return []


def check_filename(page: Page) -> list[Finding]:
    if VALID_FILENAME_RE.match(page.name):
        return []
    return [Finding("error", "filename", page.name, None,
                    f"Filename violates convention: `{page.name}`",
                    "Rename to lowercase letters/digits, hyphen-separated, `.md` extension")]


def check_wikilinks(
    page: Page,
    stems: set[str],
    headings_by_stem: dict[str, set[str]],
) -> list[Finding]:
    findings: list[Finding] = []
    for link in page.outbound:
        if not link.target:
            if link.anchor and slugify(link.anchor) not in headings_by_stem.get(page.stem, set()):
                findings.append(Finding("error", "wikilink", page.name, link.line,
                                        f"Broken self-anchor `[[#{link.anchor}]]` — no matching heading on this page"))
            continue
        if link.target not in stems:
            findings.append(Finding("error", "wikilink", page.name, link.line,
                                    f"Broken wiki-link `[[{link.target}]]` — no page `{link.target}.md` exists"))
            continue
        if link.anchor and slugify(link.anchor) not in headings_by_stem.get(link.target, set()):
            findings.append(Finding("error", "wikilink", page.name, link.line,
                                    f"Broken section anchor `[[{link.target}#{link.anchor}]]` — no matching heading in `{link.target}.md`"))
    return findings


def check_sources_on_disk(page: Page, repo_root: Path) -> list[Finding]:
    # Meta pages carry a "(meta-page; …)" marker instead of backticked raw/ files;
    # their Sources line is prose and has nothing to verify on disk.
    if is_meta_page(page.name):
        return []
    findings: list[Finding] = []
    for src in page.sources_files:
        if not src.startswith("raw/"):
            findings.append(Finding("warning", "sources", page.name, page.sources_line,
                                    f"`**Sources**` entry does not start with `raw/`: `{src}`",
                                    "Use the form `raw/<book>/<chapter>.md`"))
            continue
        if not (repo_root / src).exists():
            findings.append(Finding("error", "sources", page.name, page.sources_line,
                                    f"`**Sources**` entry does not exist on disk: `{src}`"))
    return findings


def check_related_pages_labels(page: Page) -> list[Finding]:
    """Typed `## Related pages` prefix allowance.

    The redesign permits (but does not require) relationship-type prefixes:
    `**Prerequisite:**`, `**Generalizes:**`, `**Alternative:**`, `**Contrast:**`,
    `**See also:**`. A bullet that uses a `**Label:**` prefix must use one of
    these canonical labels; legacy flat-bullet lists (no `**Label:**` prefix)
    continue to pass silently.
    """
    if page.related_pages_line is None:
        return []
    findings: list[Finding] = []
    for offset, line in enumerate(page.lines[page.related_pages_line:]):
        if HEADING_RE.match(line):
            break
        m = RELATED_BULLET_LABEL_RE.match(line)
        if not m:
            continue
        label = m.group(1).strip()
        if label not in CANONICAL_RELATED_LABELS:
            line_no = page.related_pages_line + 1 + offset
            findings.append(Finding(
                "warning", "related-pages", page.name, line_no,
                f"Non-canonical Related-pages label `**{label}:**`",
                f"Use one of: {', '.join(CANONICAL_RELATED_LABELS)}"))
    return findings


def check_inline_sources(
    page: Page,
    raw_files_by_name: dict[str, list[Path]],
    repo_root: Path,
) -> list[Finding]:
    findings: list[Finding] = []
    for line_no, citation in page.inline_sources:
        # A citation may hold multiple files separated by `,` or `;`
        for part in re.split(r"[;,]", citation):
            ref = part.strip()
            if not ref.endswith(".md"):
                continue
            exists = (
                (repo_root / ref).exists() if "/" in ref
                else ref in raw_files_by_name
            )
            if not exists:
                findings.append(Finding("warning", "inline-source", page.name, line_no,
                                        f"Inline citation `(source: {ref})` — no such file under `raw/`"))
    return findings


def check_orphans(pages: list[Page], inbound: dict[str, set[str]]) -> list[Finding]:
    """Orphan policy after the MOC redesign:

    - Concept pages (anything that isn't a meta-page) must be linked from at
      least one MOC (`moc-*.md`). Concept-page-to-concept-page links don't
      rescue an orphan — the MOC layer is the navigational contract, and an
      unreachable concept page is one that the question-patterns → MOC path
      can never surface.
    - MOCs and `question-patterns.md` are exempt — they're linked from
      `index.md`; the `index` check covers them.
    """
    findings: list[Finding] = []
    for page in pages:
        if is_meta_page(page.name):
            continue
        sources = inbound.get(page.stem, set())
        moc_sources = {s for s in sources if is_moc_page(s)}
        if not moc_sources:
            findings.append(Finding("warning", "orphan", page.name, None,
                                    "Orphan concept page — no inbound `[[wikilinks]]` from any MOC "
                                    "(`moc-*.md`). Concept-page-to-concept-page links do not count.",
                                    "Link this page from the relevant `moc-<topic>.md` with a "
                                    "one-sentence `why` / `when`"))
    return findings


def check_index_sync(index_page: Page | None, pages: list[Page]) -> list[Finding]:
    """A page counts as "indexed" if any of the navigational entry points links it:
    `index.md` itself, or any `moc-*.md`. The A–Z appendix in `index.md` is the
    belt-and-braces guarantee, but a page reachable only through its MOC is
    still findable by the agent walking the navigation graph.

    Duplicate-link detection still runs only on `index.md` — that's where
    catalog hygiene matters.
    """
    findings: list[Finding] = []
    if index_page is None:
        findings.append(Finding("error", "index", "index.md", None,
                                "No `index.md` found in the wiki directory"))
        return findings

    index_refs: dict[str, list[int]] = {}
    for link in index_page.outbound:
        if link.target:
            index_refs.setdefault(link.target, []).append(link.line)

    moc_linked: set[str] = set()
    for p in pages:
        if not is_moc_page(p.name):
            continue
        for link in p.outbound:
            if link.target:
                moc_linked.add(link.target)

    indexed_stems = set(index_refs.keys()) | moc_linked
    actual_stems = {p.stem for p in pages if p.name not in IGNORED_PAGES}

    for stem in sorted(actual_stems - indexed_stems):
        findings.append(Finding("warning", "index", "index.md", None,
                                f"Page `{stem}.md` is not reachable from `index.md` or any MOC",
                                "Add an entry in the appropriate section of `index.md`, or link "
                                "it from the relevant `moc-<topic>.md`"))

    for stem, line_nos in index_refs.items():
        if len(line_nos) > 1:
            findings.append(Finding("warning", "index", "index.md", line_nos[0],
                                    f"`[[{stem}]]` listed {len(line_nos)} times in `index.md` "
                                    f"(lines {', '.join(str(n) for n in line_nos)})",
                                    "Deduplicate to a single entry in the most appropriate section"))

    return findings


def load_raw_files(raw_dir: Path) -> dict[str, list[Path]]:
    result: dict[str, list[Path]] = {}
    if not raw_dir.exists():
        return result
    for p in raw_dir.rglob("*.md"):
        result.setdefault(p.name, []).append(p)
    return result


def render_text(findings: list[Finding], summary: dict) -> str:
    by_sev: dict[str, list[Finding]] = {"error": [], "warning": [], "info": []}
    for f in findings:
        by_sev[f.severity].append(f)

    out: list[str] = [
        "# Wiki lint report",
        "",
        f"**Wiki**: `{summary['wiki']}`  ",
        f"**Raw**:  `{summary['raw']}`  ",
        f"**Pages scanned**: {summary['page_count']}  ",
        f"**Findings**: {len(by_sev['error'])} errors, "
        f"{len(by_sev['warning'])} warnings, "
        f"{len(by_sev['info'])} info",
        "",
    ]

    for sev in ("error", "warning", "info"):
        bucket = by_sev[sev]
        if not bucket:
            continue
        out.append(f"## {sev.capitalize()}s ({len(bucket)})")
        out.append("")
        for idx, f in enumerate(bucket, start=1):
            loc = f"`{f.page}`" + (f":{f.line}" if f.line is not None else "")
            out.append(f"{idx}. **[{f.check}]** {loc} — {f.message}")
            if f.suggestion:
                out.append(f"   → {f.suggestion}")
        out.append("")

    if not findings:
        out.append("No findings. ✓")
        out.append("")
    return "\n".join(out)


def render_json(findings: list[Finding], summary: dict) -> str:
    return json.dumps(
        {"summary": summary, "findings": [f.__dict__ for f in findings]},
        indent=2,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Deterministic linter for the sw-eng-llm-wiki.")
    parser.add_argument("wiki_dir", nargs="?", default="../wiki",
                        help="Path to the wiki/ directory (default: ../wiki)")
    parser.add_argument("--raw-dir", default=None,
                        help="Path to the raw/ directory (default: <wiki_dir>/../raw)")
    parser.add_argument("--format", choices=["text", "json"], default="text",
                        help="Report format (default: text)")
    parser.add_argument("--severity", choices=["error", "warning", "info"], default="info",
                        help="Minimum severity to include in the report (default: info)")
    args = parser.parse_args()

    wiki_dir = Path(args.wiki_dir).resolve()
    if not wiki_dir.is_dir():
        print(f"Error: wiki directory not found: {wiki_dir}", file=sys.stderr)
        return 1

    repo_root = wiki_dir.parent
    raw_dir = Path(args.raw_dir).resolve() if args.raw_dir else (repo_root / "raw").resolve()

    page_paths = sorted(wiki_dir.glob("*.md"))
    pages = [parse_page(p) for p in page_paths]
    stems = {p.stem for p in pages}
    index_page = next((p for p in pages if p.name == "index.md"), None)

    headings_by_stem: dict[str, set[str]] = {
        p.stem: {slugify(text) for _, _, text in p.headings} for p in pages
    }

    inbound: dict[str, set[str]] = {}
    for p in pages:
        if p.name in INBOUND_EXCLUDED_SOURCES:
            continue
        for link in p.outbound:
            if link.target and link.target != p.stem:
                inbound.setdefault(link.target, set()).add(p.stem)

    raw_files_by_name = load_raw_files(raw_dir)

    findings: list[Finding] = []
    today = date.today()
    for p in pages:
        if p.name in IGNORED_PAGES:
            # Still run wikilink checks on index.md (log.md is append-only, skip)
            if p.name == "index.md":
                findings += check_wikilinks(p, stems, headings_by_stem)
            continue
        findings += check_page_format(p)
        findings += check_last_updated(p, today)
        findings += check_filename(p)
        findings += check_wikilinks(p, stems, headings_by_stem)
        findings += check_sources_on_disk(p, repo_root)
        findings += check_inline_sources(p, raw_files_by_name, repo_root)
        findings += check_related_pages_labels(p)

    findings += check_orphans(pages, inbound)
    findings += check_index_sync(index_page, pages)

    min_sev = SEVERITY_ORDER[args.severity]
    findings = [f for f in findings if SEVERITY_ORDER[f.severity] <= min_sev]
    findings.sort(key=lambda f: (SEVERITY_ORDER[f.severity], f.check, f.page, f.line or 0))

    summary = {
        "wiki": str(wiki_dir),
        "raw": str(raw_dir),
        "page_count": len(pages),
    }
    output = render_json(findings, summary) if args.format == "json" else render_text(findings, summary)
    print(output)

    return 1 if any(f.severity == "error" for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
