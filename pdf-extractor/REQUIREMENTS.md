# Requirements & Design Decisions

## Goals

- Extract each chapter of a PDF book into its own markdown file
- Preserve heading hierarchy (H1/H2/H3), code blocks, and paragraph structure
- Replace the book's page-number index with Obsidian wikilinks pointing to the correct chapter and section
- Output files are named consistently for use as an Obsidian vault source

## Non-goals

- Table extraction (tables are treated as body text)
- Image/figure extraction (replaced with a caption placeholder)
- Perfect footnote placement (footnotes detected by font size, appended as blockquotes)

## Heading detection thresholds

These were tuned for *Designing Data-Intensive Applications* (Antenna House PDF, font sizes: body ≈ 9pt, H3 ≈ 10–11pt bold, H2 ≈ 13pt bold, chapter title ≈ 18–24pt). Adjust in `classify_line()` for other books:

| Class         | Rule                                      |
|---------------|-------------------------------------------|
| chapter_title | font size ≥ 18                            |
| h2            | font size ≥ 13 AND (bold OR avg ≥ 13) AND line < 120 chars |
| h3            | font size ≥ 10 AND bold AND line < 120 chars |
| code          | all spans use a monospace font            |
| caption       | average font size < 8.5                   |
| body          | everything else                           |

## Index linking strategy

1. Build a `page → (chapter_file, section_slug)` map from the PDF's bookmark outline (`get_toc()`).
2. Extract raw text from the index pages.
3. Parse each entry with a regex: `optional-indent + term + "," + page-refs`.
4. For each page reference, look up the chapter file and section slug, emit `[[chapter-file#section-slug]]`.
5. Deduplicate links that resolve to the same section.
6. Page ranges (e.g. `83–87`) are expanded to individual pages before lookup.

Anchor slugs follow Obsidian's default: lowercase, spaces→hyphens, punctuation stripped.

## Known limitations

- Multi-column layouts: handled by PyMuPDF's `sort=True` flag, which reads blocks top-to-bottom. Complex layouts may still interleave columns.
- Running headers/footers: stripped by regex matching common patterns (bare page number, book title, chapter label). New books may need additional patterns added to `RUNNING_HEADERS` in `extract.py`.
- Hyphenated line-breaks: re-joined when a line ends with `-` followed by a lowercase letter on the next line. False positives possible with intentionally hyphenated compound words.
- Index entries without page refs (e.g. cross-references like "see also X") are emitted as plain list items without links.
