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
| `sources` | error (missing file), warning (malformed) | `**Sources**:` backtick entries (``` `raw/book/file.md` ```) must exist on disk. Entries not starting with `raw/` are flagged as warnings. |
| `inline-source` | warning | Inline `(source: filename.md)` citations where `filename.md` does not exist anywhere under `raw/`. Citations not ending in `.md` (e.g. "chapter 9") are ignored. |
| `orphan` | warning | Pages with zero inbound `[[wikilinks]]` from any other wiki page. `index.md` and `log.md` are excluded as link sources because catalog/audit references don't represent real cross-linking. |
| `index` | warning (missing/duplicate), error (no index.md) | Every wiki page appears in `index.md` exactly once. Broken `[[links]]` in `index.md` are caught by the `wikilink` check. |

## Exit codes

- `0` — no `error`-severity findings.
- `1` — at least one `error` finding, or a runtime problem.

Warnings and info do not fail the run — this keeps the lint workflow non-blocking while still surfacing the issues.

## Design notes

- **Anchor matching** uses a simple slugifier: lowercase, non-alphanumeric → hyphen, collapse, strip. Both the anchor text in `[[page#Anchor Text]]` and the heading text in `## Heading Text` are normalised the same way before comparison. Obsidian's own anchor resolution is roughly equivalent.
- **Fenced code blocks** are zeroed out before wikilink scanning so that `[[…]]` inside ``` ``` ``` fences does not produce false positives. Line numbers are preserved by substituting blank lines rather than removing them.
- **`index.md` and `log.md`** are excluded from `page-format`, `filename`, `date`, `sources`, and `inline-source` checks. Their structure differs from content pages. `index.md` is still scanned for wikilink integrity.
- **Severity choice** prioritises actionability: "something is broken" is `error`; "something looks off but doesn't break anything" is `warning`. This keeps exit-code semantics useful for future CI hookup without making the MVP noisy.

## Tunable thresholds

None currently. Behaviour is fully deterministic. If false-positive rates grow (e.g. anchor slugification mismatches for unusual heading punctuation), tune inside the relevant check function.
