# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# LLM Wiki

A personal knowledge base maintained by Claude Code.
Based on Andrej Karpathy's LLM Wiki pattern.

## Purpose

This wiki is a structured, interlinked knowledge base for software development design and best practices.
Claude maintains the wiki. The human curates sources, asks questions, and guides the analysis.

## Folder structure

```
raw/                        -- source documents (immutable -- never modify these)
raw/<book-name>/            -- per-chapter markdown extracted from a PDF book
wiki/                       -- markdown pages maintained by Claude
wiki/index.md               -- table of contents for the entire wiki
wiki/log.md                 -- append-only record of all operations
pdf-extractor/              -- uv project that converts PDF books into per-chapter markdown files
```

`wiki/index.md` and `wiki/log.md` do not exist until the first ingest — create them then.

## Ingest workflow

When the user adds a new source to `raw/` and asks you to ingest it:

1. Read the full source document
2. Discuss key takeaways with the user before writing anything
3. Create a summary page in `wiki/` named after the source
4. Create or update concept pages for each major idea or entity
5. Add wiki-links ([[page-name]]) to connect related pages
6. Update `wiki/index.md` with new pages and one-line descriptions
7. Append an entry to `wiki/log.md` with the date, source name, and what changed. Don't be verbose; keep it concise

A single source may touch 10-15 wiki pages. That is normal.

## Page format

Every wiki page should follow this structure:

```markdown
# Page Title

**Summary**: One to two sentences describing this page.

**Sources**: List of raw source files this page draws from.

**Last updated**: Date of most recent update.

---

Main content goes here. Use clear headings and short paragraphs.

Link to related concepts using [[wiki-links]] throughout the text.

## Related pages

- [[related-concept-1]]
- [[related-concept-2]]
```

## Citation rules

- Every factual claim should reference its source file
- Use the format (source: filename.pdf) after the claim
- If two sources disagree, note the contradiction explicitly
- If a claim has no source, mark it as needing verification

## Question answering

When the user asks a question:

1. Read `wiki/index.md` first to find relevant pages
2. Read those pages and synthesize an answer
3. Cite specific wiki pages in your response
4. If the answer is not in the wiki, say so clearly
5. If the answer is valuable, offer to save it as a new wiki page

Good answers should be filed back into the wiki so they compound over time.

## Lint

When the user asks you to lint or audit the wiki:

1. Run the linter: `cd wiki-linter && uv run python lint.py ../wiki`
2. Surface its report to the user.
3. Stop. If there are errors or warnings, offer to fix them but **WAIT FOR PERMISSION FIRST**.

See `wiki-linter/REQUIREMENTS.md` for what the linter does and does not check.

## Rules

- Never modify anything in the `raw/` folder
- Always update `wiki/index.md` and `wiki/log.md` after changes
- Keep page names lowercase with hyphens (e.g. `machine-learning.md`)
- Write in clear, plain language
- When uncertain about how to categorize something, ask the user

---

## pdf-extractor

A standalone `uv` project at `pdf-extractor/` that converts a PDF book into per-chapter markdown files with an Obsidian-compatible index.

### Commands

```bash
# Install dependencies
cd pdf-extractor && uv sync

# Extract a PDF (run from repo root or adjust paths accordingly)
cd pdf-extractor
uv run python extract.py "../raw/Book Title.pdf" "../raw/book-title/"
```

Output: one `.md` file per chapter/section plus `index.md` in the output directory. The index replaces page numbers with `[[chapter-file#section-slug]]` wikilinks.

### Converting a new book from PDF to Markdown

1. The book will be a PDF in `raw/`
2. Create a subdirectory under `raw/` named after the book (lowercase, hyphen-separated)
3. Run the extractor pointing at the new PDF and that subdirectory
4. If heading detection looks wrong, tune the font-size thresholds in `classify_line()` in `pdf-extractor/extract.py`

Current thresholds (calibrated for *Designing Data-Intensive Applications*, MyriadPro display font):

| Class         | Rule                                                        |
|---------------|-------------------------------------------------------------|
| chapter_title | font size ≥ 18                                              |
| h2            | font size ≥ 13 AND (bold OR avg ≥ 13) AND line < 120 chars |
| h3            | font size ≥ 10 AND bold AND line < 120 chars                |
| code          | all spans use a monospace font                              |
| caption       | average font size < 8.5                                     |
| body          | everything else                                             |

Running headers/footers are stripped via regex in `RUNNING_HEADERS` in `extract.py` — new books may need additional patterns added there.

### Architecture

Don't read files in `pdf-extractor/` unless explicitly asked to modify it or convert a new book. Full details are in `pdf-extractor/README.md` and `pdf-extractor/REQUIREMENTS.md`.
