# sw-eng-llm-wiki

A personal, Claude-maintained knowledge base for software engineering design and best practices. Inspired by Andrej Karpathy's LLM Wiki pattern: the human curates sources and asks questions; Claude reads the sources, writes interlinked wiki pages, and answers from them.

The wiki is a plain folder of markdown files with `[[wiki-link]]` syntax, so it works as an [Obsidian](https://obsidian.md) vault.

Currently ~990 interlinked pages distilled from eight books (see **Sources** below).

## Layout

```
raw/                      source documents — immutable, never edited by Claude
raw/<book-name>/          per-chapter markdown extracted from a PDF book
wiki/                     Claude-maintained pages (~990 markdown files)
wiki/index.md             master hub: start-here pointer, MOC table, books table, A–Z appendix
wiki/question-patterns.md router from question archetypes to the MOCs that ground an answer
wiki/moc-*.md             16 Maps-of-Content — narrative topic clusters
wiki/<book-name>.md       8 per-book summary pages with chapter-anchored wikilinks
wiki/log.md               append-only record of ingests and edits
pdf-extractor/            uv project that converts PDFs to per-chapter markdown
wiki-linter/              uv project that lints the wiki for structural issues
wiki-mcp/                 uv project exposing a read-only MCP server over wiki/
.mcp.json                 wires wiki-mcp into Claude Code automatically
.claude/skills/           Claude Code skills that drive the workflows below
.claude/settings.json     project-scoped Claude Code settings
.obsidian/                Obsidian vault config (so the repo opens as a vault)
CLAUDE.md                 operational spec Claude follows in this repo
ARCHITECTURE.md           human-facing explanation of the wiki's navigation design
```

## Workflows

The first two are implemented as Claude Code skills under `.claude/skills/`:

- **convert-pdf** — run the extractor on a PDF in `raw/`, producing per-chapter markdown.
- **ingest-book** — read a source (or a chapter) in `raw/`, discuss takeaways, then create/update wiki pages, update `wiki/index.md`, and append to `wiki/log.md`.
- **lint** — ask Claude to "lint the wiki" and it runs `wiki-linter` and offers to fix anything it flags. Read-only structural checks only; semantic review stays with the human.

A single source typically touches 10–15 wiki pages; a full book runs into the hundreds.

## pdf-extractor

Standalone [`uv`](https://docs.astral.sh/uv/) project. From the repo root:

```bash
cd pdf-extractor
uv sync
uv run python extract.py "../raw/Book Title.pdf" "../raw/book-title/"
```

Output is one `.md` file per chapter plus an `index.md` that replaces page numbers with `[[chapter-file#section-slug]]` wikilinks. If headings look wrong on a new book, tune the font-size thresholds in `classify_line()` in `pdf-extractor/extract.py`. Details in `pdf-extractor/README.md`.

## wiki-linter

Standalone [`uv`](https://docs.astral.sh/uv/) project that runs deterministic structural checks on `wiki/` — page format, wiki-link integrity, orphan pages, index sync, citation validity, filename convention. From the repo root:

```bash
cd wiki-linter
uv sync
uv run python lint.py ../wiki
```

Emits a numbered markdown report. Semantic judgements (contradictions, outdated claims) are out of scope. Details in `wiki-linter/README.md` and `wiki-linter/REQUIREMENTS.md`.

## Using the wiki

- Open the repo as an Obsidian vault, or browse `wiki/index.md` on GitHub.
- Ask Claude questions. For non-trivial multi-cluster questions, Claude routes through `wiki/question-patterns.md` to match the closest archetype, reads every Map-of-Content (`wiki/moc-*.md`) the pattern names, then follows the MOCs into concept pages and raw book chapter sections before drafting — the MOCs carry the cross-cluster narrative that a flat index can't. For targeted single-concept lookups, the A–Z appendix at the bottom of `wiki/index.md` is the direct route. Claude offers to file valuable answers back as new pages. See `ARCHITECTURE.md` for the design rationale.
- Ask Claude to lint the wiki to surface broken wikilinks, orphan pages, malformed pages, missing citations, and index drift.

## Architecture

See [`ARCHITECTURE.md`](ARCHITECTURE.md) for the *why* and *how* of the wiki's navigation design — the four-layer structure (question-patterns → MOCs → concept pages → raw chapters), the design premises (flat pages, narrative MOCs, meta-pages instead of frontmatter), page types and conventions, how to extend, and what's intentionally out of scope.

## Sources

Ingested books, each with its own summary page under `wiki/`:

- [*Designing Data-Intensive Applications*](wiki/designing-data-intensive-applications.md) — Martin Kleppmann
- [*Monolith to Microservices*](wiki/monolith-to-microservices.md) — Sam Newman
- [*Designing Distributed Systems*](wiki/designing-distributed-systems.md) — Brendan Burns
- [*Fundamentals of Software Architecture*](wiki/fundamentals-of-software-architecture.md) — Mark Richards & Neal Ford
- [*Building Event-Driven Microservices*](wiki/building-event-driven-microservices.md) — Adam Bellemare
- [*Site Reliability Engineering*](wiki/site-reliability-engineering.md) — Beyer, Jones, Petoff & Murphy (eds.)
- [*Fundamentals of Data Engineering*](wiki/fundamentals-of-data-engineering.md) — Joe Reis & Matt Housley
- [*Software Architecture: The Hard Parts*](wiki/software-architecture-the-hard-parts.md) — Ford, Richards, Sadalage & Dehghani

## Conventions

- Page names are lowercase with hyphens (`machine-learning.md`).
- Every factual claim cites its source: `(source: filename.pdf)`.
- Contradictions between sources are noted explicitly rather than resolved silently.
- PDFs in `raw/` are gitignored; the extracted markdown is committed.

See `CLAUDE.md` for the full page format, citation rules, and ingest/lint procedures.
