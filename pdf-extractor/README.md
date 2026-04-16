# pdf-extractor

Converts a technical PDF book into per-chapter markdown files, with an index file that uses Obsidian wikilinks instead of page numbers.

## Usage

```bash
uv run python extract.py <path-to-pdf> <output-dir>
```

### Example — Designing Data-Intensive Applications

```bash
cd pdf-extractor
uv run python extract.py \
  "../raw/Designing Data Intensive Applications.pdf" \
  "../raw/designing-data-intensive-applications/"
```

This produces one `.md` file per chapter plus `index.md` in the output directory.

## Adding a new book

1. Place the PDF in `../raw/`
2. Create a subdirectory named after the book (lowercase, hyphen-separated)
3. Run the extractor pointing at the new PDF and subdirectory
4. Review the output — heading detection thresholds may need tuning for books with different font sizes (see `REQUIREMENTS.md`)

## Dependencies

Managed by `uv`. Run `uv sync` to install. No system-level dependencies required.
