"""
extract.py — PDF chapter extractor

Usage:
    uv run python extract.py <path-to-pdf> <output-dir>

Each chapter becomes its own markdown file in <output-dir>.
The book index becomes index.md with Obsidian wikilinks replacing page numbers.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

import fitz  # PyMuPDF


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class Section:
    title: str
    slug: str          # heading anchor slug
    filename: str      # output filename (no extension)
    start_page: int    # 0-based
    end_page: int      # 0-based, inclusive
    level: int         # 1=chapter, 2=section, 3=subsection
    children: list[Section] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Slugification
# ---------------------------------------------------------------------------

def slugify(text: str) -> str:
    """Obsidian-compatible anchor slug: lowercase, spaces→hyphens, strip punctuation."""
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = text.strip("-")
    return text


def chapter_filename(num: int, title: str) -> str:
    """e.g. chapter-03-storage-and-retrieval"""
    slug = slugify(title)
    return f"chapter-{num:02d}-{slug}"


# ---------------------------------------------------------------------------
# TOC parsing
# ---------------------------------------------------------------------------

SKIP_TITLES = {"copyright", "table of contents", "colophon"}
SPECIAL_L1 = {"preface", "foreword", "glossary", "index", "about the author",
              "self-assessment questions"}

# Require a period after the chapter number ("Chapter 1." or "1.") to avoid matching
# self-assessment subsections that use a colon ("Chapter 1: Introduction").
# The "Chapter " prefix is optional — some books list chapters as "1. Title".
_CHAPTER_RE = re.compile(r"^(?:chapter\s+)?\d+\.", re.IGNORECASE)
_APPENDIX_RE = re.compile(r"^appendix\s+([a-z0-9]+)[.\s]+(.*)$", re.IGNORECASE)
# Bare-letter appendix form used by some books (e.g. "A. Serialization…"). Only
# safe to apply once we've seen a numbered chapter — before then, a bare "I."
# could be a Roman-numeral part label.
_APPENDIX_BARE_RE = re.compile(r"^([A-Z])\.\s+(.+)$")


def _appendix_filename(title: str, allow_bare: bool = False) -> str | None:
    """Return `appendix-a-bibliography` for 'Appendix A. Bibliography', else None.

    When `allow_bare` is True, also matches the bare form 'A. Bibliography'
    used by books that omit the 'Appendix' prefix in their TOC.
    """
    s = title.strip()
    m = _APPENDIX_RE.match(s)
    if not m and allow_bare:
        m = _APPENDIX_BARE_RE.match(s)
    if not m:
        return None
    letter = m.group(1).lower()
    rest = slugify(m.group(2))
    return f"appendix-{letter}-{rest}" if rest else f"appendix-{letter}"


def _match_special_l1(low: str) -> str | None:
    """Return canonical SPECIAL_L1 term if title matches (e.g. 'Preface: Foo' → 'preface')."""
    base = low.split(":", 1)[0].strip()
    return base if base in SPECIAL_L1 else None


def build_toc(doc: fitz.Document) -> list[Section]:
    """
    Parse doc.get_toc() into a flat list of sections to extract.

    Handles two common layouts:
      - DDIA-style: L1 = Part, L2 = "Chapter N. Title"
      - Newman-style: L1 = "Chapter N. Title" directly (no Parts)

    We extract:
      - L1 specials: Preface, Foreword, Glossary, Index, About the Author
      - "Chapter N. Title" entries at L1 or L2
      - "Appendix X. Title" entries at L1 or L2
    """
    raw = doc.get_toc(simple=False)  # [level, title, page, ...]
    total_pages = doc.page_count

    # Collect all entries we want to turn into files, in page order
    candidates: list[tuple[str, int]] = []  # (filename, start_page 0-based)

    chapter_num = 0
    for level, title, page, *_ in raw:
        low = title.lower().strip()
        start = page - 1

        if level == 1 and (low in SKIP_TITLES or re.match(r"part\s+[ivxlcdm\d]+", low)):
            continue

        if level in (1, 2) and _CHAPTER_RE.match(low):
            chapter_num += 1
            clean = re.sub(r"^(?:chapter\s+)?\d+[.\s]+", "", title, flags=re.IGNORECASE).strip()
            candidates.append((chapter_filename(chapter_num, clean), start))
            continue

        if level in (1, 2):
            appendix = _appendix_filename(title, allow_bare=chapter_num > 0)
            if appendix:
                candidates.append((appendix, start))
                continue

        if level == 1 and (special := _match_special_l1(low)):
            candidates.append((slugify(special), start))

    # Derive end pages: each section ends one page before the next starts
    sections: list[Section] = []
    for i, (filename, start_page) in enumerate(candidates):
        end_page = candidates[i + 1][1] - 1 if i + 1 < len(candidates) else total_pages - 1
        sections.append(Section(
            title=filename,
            slug=slugify(filename),
            filename=filename,
            start_page=start_page,
            end_page=end_page,
            level=1,
        ))

    return sections


def build_page_index(doc: fitz.Document) -> dict[int, tuple[str, str]]:
    """
    Build a mapping: page_number (0-based) → (chapter_filename, section_slug)
    Uses the full TOC (all levels) to map each page to its deepest section.
    """
    raw = doc.get_toc(simple=False)
    entries: list[tuple[int, str, int]] = []  # (page 0-based, title, level)
    for level, title, page, *_ in raw:
        entries.append((page - 1, title, level))

    entries.sort(key=lambda x: x[0])

    current_chapter = ""
    current_section = ""
    chapter_num = 0
    section_map: dict[int, tuple[str, str]] = {}

    for page, title, level in entries:
        low = title.lower().strip()
        if level in (1, 2) and _CHAPTER_RE.match(low):
            chapter_num += 1
            clean = re.sub(r"^(?:chapter\s+)?\d+[.\s]+", "", title, flags=re.IGNORECASE).strip()
            current_chapter = chapter_filename(chapter_num, clean)
            current_section = slugify(title)
        elif level in (1, 2) and (appendix := _appendix_filename(title, allow_bare=chapter_num > 0)):
            current_chapter = appendix
            current_section = slugify(title)
        elif level == 1 and (special := _match_special_l1(low)):
            current_chapter = slugify(special)
            current_section = slugify(special)
        elif level >= 2:
            current_section = slugify(title)

        if current_chapter:
            section_map[page] = (current_chapter, current_section)

    # Fill gaps: pages not in TOC inherit from the last known entry
    result: dict[int, tuple[str, str]] = {}
    last: tuple[str, str] = ("", "")
    for p in range(doc.page_count):
        if p in section_map:
            last = section_map[p]
        result[p] = last

    return result


# ---------------------------------------------------------------------------
# Font classification
# ---------------------------------------------------------------------------

MONOSPACE_HINTS = {"courier", "mono", "code", "consolas", "menlo", "monaco",
                   "inconsolata", "anonymous", "sourcecodepro", "jetbrains"}

# Display fonts used for headings. Different O'Reilly books use different fonts
# — add new ones here as you encounter them. Any span whose font name contains
# one of these substrings (case-insensitive, spaces/dashes stripped) is treated
# as a heading candidate.
HEADING_FONTS = ("myriadpro", "helvetica", "arialbold")


def is_monospace(font_name: str) -> bool:
    name = font_name.lower().replace(" ", "").replace("-", "")
    return any(hint in name for hint in MONOSPACE_HINTS)


def is_heading_font(font_name: str) -> bool:
    name = font_name.lower().replace(" ", "").replace("-", "")
    return any(hf in name for hf in HEADING_FONTS)


def classify_line(spans: list[dict]) -> str:
    """
    Classify a line using exact font name + size thresholds measured from DDIA:
      chapter_title : MyriadPro ≥ 22pt  (actual: 25.2)
      h2            : MyriadPro 17–22pt  (actual: 18.9)
      h3            : MyriadPro 13–17pt  (actual: 15.8)
      strip         : MyriadPro ≤ 10pt   (running headers/footers at 9pt)
      code          : monospace font
      caption       : avg size < 8.5
      body          : everything else (MinionPro Regular/Italic)
    """
    if not spans:
        return "body"

    text = "".join(s["text"] for s in spans).strip()
    if not text:
        return "body"

    sizes = [s["size"] for s in spans]
    max_size = max(sizes)
    avg_size = sum(sizes) / len(sizes)
    monospace = all(is_monospace(s["font"]) for s in spans)
    heading = all(is_heading_font(s["font"]) for s in spans)

    if monospace:
        return "code"

    if heading:
        if max_size <= 10:
            return "strip"           # running page headers/footers
        if max_size >= 22:
            return "chapter_title"   # 25.2pt — chapter title
        if max_size >= 17:
            return "h2"              # 18.9pt — major section
        if max_size >= 13:
            # 16.8pt = "CHAPTER N" label (strip), 15.8pt = H3 subsection
            if re.match(r"^chapter\s+\d+$", text, re.IGNORECASE):
                return "strip"
            return "h3"

    if avg_size < 8.5:
        return "caption"

    return "body"


# ---------------------------------------------------------------------------
# Header/footer detection
# ---------------------------------------------------------------------------

_HEADER_RE = re.compile(
    r"^(\d+|www\.it-ebooks\.info|\|)$", re.IGNORECASE
)


def is_header_footer(text: str) -> bool:
    """Catch any remaining structural artifacts not handled by font-based stripping."""
    return bool(_HEADER_RE.match(text.strip()))


# ---------------------------------------------------------------------------
# Page → markdown
# ---------------------------------------------------------------------------

def page_to_lines(page: fitz.Page) -> list[tuple[str, str]]:
    """
    Extract (classification, text) pairs from a page.
    sort=True handles multi-column by reading top-to-bottom, left-to-right.
    """
    data = page.get_text("dict", sort=True)
    results: list[tuple[str, str]] = []

    for block in data["blocks"]:
        if block["type"] != 0:  # skip image blocks
            continue
        for line in block["lines"]:
            spans = line["spans"]
            if not spans:
                continue
            text = "".join(s["text"] for s in spans)
            if is_header_footer(text):
                continue
            cls = classify_line(spans)
            results.append((cls, text))

    return results


_INLINE_REF_RE = re.compile(r"\s*\[\d+(?:,\s*\d+)*\]")


def strip_inline_refs(text: str) -> str:
    """Remove inline citation markers like [2] or [1, 3] from body text."""
    return _INLINE_REF_RE.sub("", text)


def lines_to_markdown(lines: list[tuple[str, str]]) -> str:
    """Convert classified lines to a markdown string."""
    out: list[str] = []
    in_code = False
    in_references = False   # suppress the References section entirely
    paragraph_buf: list[str] = []
    title_buf: list[str] = []  # accumulate multi-line chapter titles

    def flush_paragraph() -> None:
        if paragraph_buf:
            joined = " ".join(paragraph_buf)
            # Re-join hyphenated line-breaks (ASCII hyphen or U+2010 non-breaking hyphen)
            # e.g. "configu‐ ration" → "configuration"
            joined = re.sub(r"[\u002D\u2010]\s+([a-z])", r"\1", joined)
            out.append(joined)
            out.append("")
            paragraph_buf.clear()

    def flush_title() -> None:
        if title_buf:
            out.append(f"# {' '.join(title_buf)}")
            out.append("")
            title_buf.clear()

    for cls, text in lines:
        text = text.strip()
        if cls == "strip":
            continue  # skip page headers/footers without breaking the paragraph

        if not text:
            if in_code:
                out.append("")
            else:
                flush_paragraph()
            continue

        if cls == "code":
            if in_references:
                continue
            if not in_code:
                flush_paragraph()
                flush_title()
                out.append("```")
                in_code = True
            out.append(text)
        else:
            if in_code:
                out.append("```")
                out.append("")
                in_code = False

            if cls == "chapter_title":
                in_references = False
                flush_paragraph()
                title_buf.append(text)  # may span multiple lines
            elif cls == "h2":
                in_references = False
                flush_paragraph()
                flush_title()
                out.append(f"## {text}")
                out.append("")
            elif cls == "h3":
                if text.strip().lower() == "references":
                    in_references = True
                    flush_paragraph()
                    flush_title()
                else:
                    in_references = False
                    flush_paragraph()
                    flush_title()
                    out.append(f"### {text}")
                    out.append("")
            elif cls == "caption":
                if in_references:
                    continue
                flush_paragraph()
                flush_title()
                out.append(f"> *{text}*")
                out.append("")
            else:  # body
                if in_references:
                    continue
                flush_title()
                paragraph_buf.append(strip_inline_refs(text))

    if in_code:
        out.append("```")
        out.append("")
    flush_paragraph()
    flush_title()

    return "\n".join(out)


# ---------------------------------------------------------------------------
# Chapter extraction
# ---------------------------------------------------------------------------

def extract_section(doc: fitz.Document, section: Section) -> str:
    """Extract and convert a section's pages to a markdown string.

    All pages are gathered into a single line list before conversion so that
    state (in_references flag, paragraph accumulation, hyphen rejoining) works
    correctly across page boundaries.
    """
    all_lines: list[tuple[str, str]] = []
    for page_num in range(section.start_page, section.end_page + 1):
        all_lines.extend(page_to_lines(doc[page_num]))
    return lines_to_markdown(all_lines)


# ---------------------------------------------------------------------------
# Index extraction
# ---------------------------------------------------------------------------

def parse_page_refs(text: str) -> list[int]:
    """Extract all page numbers from an index entry's reference string."""
    pages: list[int] = []
    for token in re.split(r"[,;]", text):
        token = token.strip()
        range_match = re.match(r"(\d+)[–—-](\d+)", token)
        if range_match:
            start, end = int(range_match.group(1)), int(range_match.group(2))
            pages.extend(range(start, end + 1))
        elif re.match(r"^\d+$", token):
            pages.append(int(token))
    return pages


def build_index_md(
    doc: fitz.Document,
    index_section: Section,
    page_index: dict[int, tuple[str, str]],
) -> str:
    """
    Extract the index pages and replace page numbers with Obsidian wikilinks.
    """
    lines_raw: list[tuple[str, str]] = []
    for page_num in range(index_section.start_page, index_section.end_page + 1):
        page = doc[page_num]
        for cls, text in page_to_lines(page):
            lines_raw.append((cls, text.strip()))

    # Rejoin hyphenated line-breaks (U+2010 non-breaking hyphen or ASCII hyphen
    # followed by a continuation on the next line starting with a lowercase letter).
    joined: list[tuple[str, str]] = []
    i = 0
    while i < len(lines_raw):
        cls, text = lines_raw[i]
        if text and re.search(r"[\u2010-]\s*$", text) and i + 1 < len(lines_raw):
            next_cls, next_text = lines_raw[i + 1]
            if next_text and next_text[0].islower():
                # Strip the trailing hyphen, merge with next line's text
                merged = re.sub(r"[\u2010-]\s*$", "", text) + next_text.strip()
                joined.append((cls, merged))
                i += 2
                continue
        joined.append((cls, text))
        i += 1
    lines_raw = joined

    out: list[str] = ["# Index", ""]

    # Pattern: optional indent + "Term, 12, 34–36" or "Term, 12"
    entry_pattern = re.compile(
        r"^(\s*)(.*?),\s*([\d,\s–—\-]+)$"
    )

    for cls, text in lines_raw:
        if not text or cls == "strip":
            continue
        if cls in ("chapter_title", "h2"):
            # Skip headings that just repeat "Index" — the file already has # Index
            if text.strip().lower() == "index":
                continue
            out.append(f"## {text}")
            out.append("")
            continue

        m = entry_pattern.match(text)
        if not m:
            indent = "  " if text[0] == " " else ""
            out.append(f"{indent}- {text.strip()}")
            continue

        indent_ws, term, refs_str = m.group(1), m.group(2).strip(), m.group(3)
        page_nums = parse_page_refs(refs_str)

        seen: set[str] = set()
        links: list[str] = []
        for pdf_page in page_nums:
            zero_based = pdf_page - 1
            if zero_based in page_index:
                ch_file, sec_slug = page_index[zero_based]
                if ch_file:
                    link = f"[[{ch_file}#{sec_slug}]]"
                    if link not in seen:
                        seen.add(link)
                        links.append(link)

        depth = len(indent_ws) // 2
        indent_md = "  " * depth
        if links:
            out.append(f"{indent_md}- **{term}** — {', '.join(links)}")
        else:
            out.append(f"{indent_md}- **{term}**")

    return "\n".join(out)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract PDF chapters to individual markdown files."
    )
    parser.add_argument("pdf", help="Path to source PDF")
    parser.add_argument("output_dir", help="Directory to write markdown files")
    args = parser.parse_args()

    pdf_path = Path(args.pdf)
    output_dir = Path(args.output_dir)

    if not pdf_path.exists():
        print(f"Error: PDF not found: {pdf_path}", file=sys.stderr)
        sys.exit(1)

    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Opening {pdf_path.name} …")
    doc = fitz.open(str(pdf_path))

    print("Parsing table of contents …")
    sections = build_toc(doc)
    page_index = build_page_index(doc)

    index_section: Section | None = None
    written = 0

    for section in sections:
        if section.filename == "index":
            index_section = section
            continue

        print(f"  {section.filename}  (pp {section.start_page + 1}–{section.end_page + 1})")
        content = extract_section(doc, section)
        out_path = output_dir / f"{section.filename}.md"
        out_path.write_text(content, encoding="utf-8")
        written += 1

    if index_section:
        print("  index  (building wikilinks …)")
        index_content = build_index_md(doc, index_section, page_index)
        (output_dir / "index.md").write_text(index_content, encoding="utf-8")
        written += 1

    print(f"\nDone — {written} files written to {output_dir}/")


if __name__ == "__main__":
    main()
