# wiki-linter

Deterministic linter for the `wiki/` knowledge base. Runs structural and link-integrity checks that a Python script can verify reliably, and emits a numbered markdown report.

## Usage

```bash
cd wiki-linter
uv sync                          # first run only
uv run python lint.py ../wiki
```

### Options

- `--raw-dir PATH` — override raw source directory (default: `../raw`, resolved relative to the wiki dir's parent)
- `--format {text,json}` — report format (default: `text`)
- `--severity {error,warning,info}` — minimum severity to include in the report (default: `info`)

## Exit codes

- `0` — no error-severity findings (warnings/info may still be present)
- `1` — at least one error-severity finding, or a runtime problem

## What it checks

See `REQUIREMENTS.md` for the full list and rationale. In short: page format, wiki-link integrity, orphan pages, index sync, citation validity, filename convention, `**Last updated**` parseability.

## What it does not check

Semantic judgements — contradictions between pages, outdated claims, which concepts should have their own page — are out of scope. The linter is read-only and deterministic.
