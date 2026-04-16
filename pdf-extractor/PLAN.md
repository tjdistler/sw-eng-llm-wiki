# Plan: PDF Chapter Extraction — Designing Data-Intensive Applications

## Context

Convert "Designing Data Intensive Applications.pdf" (613 pages, 12 chapters) into individual
markdown files. Output is organized under a per-book subdirectory inside `raw/` so additional
books can be added later. All extraction code lives in a standalone `pdf-extractor/` project
managed by `uv`.

---

## Directory layout

```
ServiceDesignWiki/
├── raw/
│   ├── Designing Data Intensive Applications.pdf   ← unchanged
│   └── designing-data-intensive-applications/      ← NEW: one dir per book
│       ├── preface.md
│       ├── chapter-01-reliable-scalable-maintainable.md
│       ├── chapter-02-data-models-query-languages.md
│       ├── chapter-03-storage-and-retrieval.md
│       ├── chapter-04-encoding-and-evolution.md
│       ├── chapter-05-replication.md
│       ├── chapter-06-partitioning.md
│       ├── chapter-07-transactions.md
│       ├── chapter-08-trouble-with-distributed-systems.md
│       ├── chapter-09-consistency-and-consensus.md
│       ├── chapter-10-batch-processing.md
│       ├── chapter-11-stream-processing.md
│       ├── chapter-12-future-of-data-systems.md
│       └── index.md
└── pdf-extractor/                                  ← NEW: uv project
    ├── pyproject.toml
    ├── PLAN.md
    ├── README.md
    ├── REQUIREMENTS.md
    └── extract.py
```

---

## pdf-extractor project

### `pyproject.toml` (uv managed)
```toml
[project]
name = "pdf-extractor"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = ["pymupdf>=1.27"]

[project.scripts]
extract = "extract:main"
```

Run with: `uv run extract <path-to-pdf> <output-dir>`

### `README.md`
Usage, how to add a new book, example command.

### `REQUIREMENTS.md`
Documents the extraction design decisions and known limitations for future reference
(heading detection thresholds, index linking strategy, page range for each book, etc.).

---

## Library

**PyMuPDF (fitz)** — declared as a `uv` dependency in `pyproject.toml`; installed
automatically on first `uv run`. Not pre-installed on the system.

Provides per-span font name + size, enabling reliable detection of heading levels,
code blocks (monospace font), captions, and body text.

---

## Chapter boundary detection

Use `doc.get_toc()` — the PDF has a complete 3-level bookmark outline with page numbers.
Map: chapter name → (start_page, end_page). End page = start page of next top-level item - 1.

Sections to extract (from outline):
- Preface (p.15)
- Ch 1–12 (p.25–574)
- Index (p.581–612) ← special handling

---

## Text extraction strategy (per page)

Use `page.get_text("dict")` → blocks → lines → spans, each span having:
- `text`, `font`, `size`, `flags` (bold/italic)

**Line classification:**
- **Chapter title**: size ≥ 20 or matches "CHAPTER \d+"
- **H2**: size in [14, 20) or bold + short line
- **H3**: size in [11, 14) + bold + short line
- **Code block**: monospace font (Courier, Menlo, Consolas, etc.)
- **Caption/footnote**: size < 9
- **Body**: everything else

**Paragraph reconstruction**: merge consecutive body lines unless separated by blank line
or a line that looks like a heading. Re-join hyphenated line-breaks (e.g. `config-\nuration`).

**Strip headers/footers**: remove lines matching page number patterns or running book title.

---

## Index special handling

Goal: replace page numbers with wikilinks to the correct section in the correct chapter file.

1. **Build `page_to_section` lookup** from `doc.get_toc()`:
   - Every page number maps to the deepest outline entry whose start_page ≤ page
   - Stores: `(chapter_filename, section_heading)`

2. **Extract index text** from pages 581–612.

3. **Parse entries** (format: `Term, 83, 84–87` with indented sub-entries).

4. **Emit wikilinks** per resolved section:
   ```markdown
   **B-Trees** — [[chapter-03-storage-and-retrieval#b-trees]], [[chapter-03-storage-and-retrieval#comparing-b-trees-and-lsm-trees]]
   ```
   - Deduplicate links resolving to the same section
   - Anchor slugs: lowercase, spaces→hyphens, strip punctuation (Obsidian default)
   - Preserve indented sub-entries as nested list items
   - Expand page ranges (e.g. `83–87`) to individual pages for lookup

---

## Script structure (`extract.py`)

```
main(pdf_path, output_dir)
├── open_doc()
├── build_toc()             — chapter/section boundaries from get_toc()
├── build_page_index()      — page_number → (file, heading) lookup
├── classify_span(span)     — body | h2 | h3 | code | caption
├── page_to_markdown(page)  — convert one page to markdown string
├── extract_chapter(start, end) — concatenate pages, clean artifacts
├── write_chapter_files()   — loop chapters, write .md files
├── extract_index()         — parse index pages
├── build_index_md()        — replace page refs with wikilinks
```

---

## Known challenges & mitigations

| Challenge | Mitigation |
|-----------|-----------|
| Multi-column layout | Detect via x-coordinate of blocks; sort left column first |
| Figures / images | Placeholder: `> [Figure X.Y: caption text]` |
| Footnotes mixed into body | Detect by small font; move to bottom of section as blockquote |
| Hyphenated line-breaks | Re-join when line ends with `-` and next char is lowercase |
| Headers/footers | Strip lines matching page-number or running-title patterns |
| Index page ranges | Expand to individual pages for section lookup |

---

## Verification

1. `cd pdf-extractor && uv run extract ../raw/"Designing Data Intensive Applications.pdf" ../raw/designing-data-intensive-applications/`
2. Confirm 14 `.md` files created in `raw/designing-data-intensive-applications/`
3. Spot-check Ch. 1 heading structure matches TOC
4. Open `index.md` and verify a few entries link to correct chapter + section
5. Grep for ` ``` ` in output to confirm code blocks are fenced
