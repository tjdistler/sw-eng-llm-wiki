# Requirements & Design Decisions

## Goals

- Replace the ad-hoc scripts Claude used to write when asked to "lint the wiki" with a persistent, version-controlled tool.
- Cover the deterministic subset of the CLAUDE.md lint spec: page format, wikilink integrity, orphan pages, index sync, citation validity, filename convention, date parseability.
- Produce a numbered, reviewable markdown report.

## Non-goals

- **No semantic checks.** Contradiction detection, "outdated claim" judgements, and evaluating which concepts deserve a page are outside this tool's scope. Concepts are curated from the books in `raw/`, not inferred from wiki text.
- **No auto-fix.** The linter only reports; the user decides on fixes.
- **No LLM calls.** Runs offline with only the Python standard library.

## Checks

| Check | Severity | Notes |
|-------|----------|-------|
| `page-format` | error | Each page (except `index.md`, `log.md`) must have `# Title`, `**Summary**:`, `**Sources**:`, `**Last updated**:`, a `---` divider, and a `## Related pages` section. Presence only — order is not enforced. |
| `date` | error | `**Last updated**` must parse as `YYYY-MM-DD` and not be in the future. |
| `filename` | error | Filenames match `^[a-z0-9]+(-[a-z0-9]+)*\.md$`. |
| `wikilink` | error | Every `[[target]]`, `[[target#anchor]]`, `[[target\|label]]` resolves to an existing `target.md`. Section anchors resolve to an `##`/`###` heading after slugification. Self-anchors `[[#anchor]]` also validated. |
| `sources` | error (missing file), warning (malformed) | `**Sources**:` backtick entries (``` `raw/book/file.md` ```) must exist on disk. Entries not starting with `raw/` are flagged as warnings. Meta-pages (`index.md`, `log.md`, `question-patterns.md`, `moc-*.md`) are exempt — their Sources line carries a `(meta-page; …)` marker instead of backticked files. |
| `inline-source` | warning | Inline `(source: filename.md)` citations where `filename.md` does not exist anywhere under `raw/`. Citations not ending in `.md` (e.g. "chapter 9") are ignored. |
| `orphan` | warning | Concept pages (anything that is not a meta-page) must be linked from at least one MOC (`moc-*.md`). Concept-page-to-concept-page links do not rescue an orphan — the MOC layer is the navigational contract, and an unreachable page cannot be surfaced by a question-patterns → MOC walk. Meta-pages (`index.md`, `log.md`, `question-patterns.md`, `moc-*.md`) are exempt; `index.md` coverage for MOCs and `question-patterns.md` is caught by the `index` check. |
| `index` | warning (missing/duplicate), error (no index.md) | Every wiki page is reachable from `index.md` or from at least one `moc-*.md`. The A–Z appendix in `index.md` is the belt-and-braces guarantee, but a page linked only from its MOC is still considered indexed. Duplicate-link detection still runs only on `index.md`. |
| `related-pages` | warning | Inside `## Related pages`, a bullet that uses a `**Label:**` prefix must use a canonical relationship type: `Prerequisite`, `Generalizes`, `Alternative`, `Contrast`, `See also`. Legacy flat-bullet lists (no `**Label:**` prefix) continue to pass silently. |

## Exit codes

- `0` — no `error`-severity findings.
- `1` — at least one `error` finding, or a runtime problem.

Warnings and info do not fail the run — this keeps the lint workflow non-blocking while still surfacing the issues.

## Design notes

- **Anchor matching** uses a simple slugifier: lowercase, non-alphanumeric → hyphen, collapse, strip. Both the anchor text in `[[page#Anchor Text]]` and the heading text in `## Heading Text` are normalised the same way before comparison. Obsidian's own anchor resolution is roughly equivalent.
- **Fenced code blocks** are zeroed out before wikilink scanning so that `[[…]]` inside ``` ``` ``` fences does not produce false positives. Line numbers are preserved by substituting blank lines rather than removing them.
- **`index.md` and `log.md`** are excluded from `page-format`, `filename`, `date`, `sources`, and `inline-source` checks. Their structure differs from content pages. `index.md` is still scanned for wikilink integrity.
- **Meta-pages** (`index.md`, `log.md`, `question-patterns.md`, `moc-*.md`) are navigational, not source-derived. They are exempt from the `sources` on-disk check (their `**Sources**:` line carries a `(meta-page; …)` marker instead of backticked files) and from the `orphan` check (MOCs and `question-patterns.md` are reached from `index.md`; index-sync covers that).
- **MOC-aware `orphan`**: concept pages must be linked from at least one MOC. This is intentionally stricter than "linked from any page": an orphan under this policy is a concept page unreachable from the question-patterns → MOC navigation graph, which is the contract Claude Code uses to ground expert-level answers. Landing this tighter check only makes sense once the MOC layer is complete (sequencing matches the wiki redesign plan).
- **MOC-aware `index`**: "indexed" is the union of `index.md` outbound links and every MOC's outbound links. The A–Z appendix in `index.md` is still the belt-and-braces default, but a page reachable through its MOC alone does not trigger a warning.
- **Typed `## Related pages`**: the five canonical relationship labels (`Prerequisite`, `Generalizes`, `Alternative`, `Contrast`, `See also`) are allowed and encouraged but not required. A bullet without a `**Label:**` prefix is treated as legacy flat-bullet format and passes silently; a bullet that *does* prefix with `**Something:**` must use a canonical label, otherwise it warns.
- **Severity choice** prioritises actionability: "something is broken" is `error`; "something looks off but doesn't break anything" is `warning`. This keeps exit-code semantics useful for future CI hookup without making the MVP noisy.

## Tunable thresholds

None currently. Behaviour is fully deterministic. If false-positive rates grow (e.g. anchor slugification mismatches for unusual heading punctuation), tune inside the relevant check function.
