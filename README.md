# sw-eng-llm-wiki

A personal, Claude-maintained knowledge base for software engineering design and best practices. Inspired by Andrej Karpathy's LLM Wiki pattern: the human curates sources and asks questions; Claude reads the sources, writes interlinked wiki pages, and answers from them.

The wiki is a plain folder of markdown files with `[[wiki-link]]` syntax, so it works as an [Obsidian](https://obsidian.md) vault.

## Layout

```
raw/                     source documents — immutable, never edited by Claude
raw/<book-name>/         per-chapter markdown extracted from a PDF book
wiki/                    Claude-maintained pages
wiki/index.md            table of contents
wiki/log.md              append-only record of ingests and edits
pdf-extractor/           uv project that converts PDFs to per-chapter markdown
wiki-linter/             uv project that lints the wiki for structural issues
.claude/skills/          Claude Code skills that drive the workflows below
CLAUDE.md                full instructions Claude follows in this repo
```

## Workflows

Both are implemented as Claude Code skills under `.claude/skills/`:

- **convert-pdf** — run the extractor on a PDF in `raw/`, producing per-chapter markdown.
- **ingest-book** — read a source in `raw/`, discuss takeaways, then create/update wiki pages, update `wiki/index.md`, and append to `wiki/log.md`.

A single source typically touches 10–15 wiki pages.

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
- Ask Claude questions — it reads `wiki/index.md` first, synthesizes an answer from the relevant pages, and offers to file valuable answers back as new pages.
- Ask Claude to lint the wiki to surface contradictions, orphan pages, missing concepts, or stale claims.

## Conventions

- Page names are lowercase with hyphens (`machine-learning.md`).
- Every factual claim cites its source: `(source: filename.pdf)`.
- Contradictions between sources are noted explicitly rather than resolved silently.
- PDFs in `raw/` are gitignored; the extracted markdown is committed.

See `CLAUDE.md` for the full page format, citation rules, and ingest/lint procedures.
