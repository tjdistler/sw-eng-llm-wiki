# Architecture

This document explains the *why* and *how* of the wiki's navigation design. `README.md` describes what the repo is and how to use the tooling; this file is what you read if you want to understand the structure, or if you're about to extend it. `CLAUDE.md` is the operational spec — it tells Claude what to do; this file tells humans why that spec exists.

## Goal

Ground expert-level, long-form, multi-cluster software-architecture answers in a curated corpus. The canonical failure mode we're designing against is a question like *"We need to extract the payments backend out of our Django monolith so we can scale 10x"* — one question that touches **decomposition patterns**, **database decomposition**, **consistency and transactions**, **distributed systems**, **organisational shape** (Conway's law, team topologies), and **reliability / operations**, all at once. Any retrieval that loads only one cluster produces a plan that stalls halfway through.

The wiki is **LLM-first** in its design choices: structure is tuned for an agent that can read dozens of files in parallel but benefits from a narrative that explains *why* concepts connect. Humans are a secondary audience via Obsidian — the vault opens and the graph view works, but keystroke affordances (folders, frontmatter, tags) are not the point.

Quality of answer is the sole optimisation target. Token cost is not.

## Design premises

**Flat concept pages, not a hierarchy.** ~990 concept pages live flat under `wiki/`. A folder hierarchy would force every concept into a single parent, but real concepts belong to several clusters at once (outbox-table-pattern is a data-processing mechanism, an events-and-streaming publication pattern, and a consistency-and-transactions correctness bridge — all true simultaneously). Grep-based agents get nothing from the hierarchy anyway; they find pages by name or wikilink. The MOC layer handles the "which cluster does this belong to" question without forcing a single assignment.

**Narrative MOCs beat tabular indexes for multi-concept questions.** The earlier shape of `index.md` was a tabular table of contents: 85 groupings, each a keyword-matched list. That works for *"what page is closest to X?"* but it does not tell the agent *"these six topics compose for extraction questions."* Narrative MOCs carry the connective prose the agent would otherwise have to infer — each wikilink earns a sentence of *why* or *when*, and each MOC hands off to its sibling MOCs explicitly. For a multi-cluster question, the agent reads 3–6 MOCs in parallel and gets the right cross-cluster framing before it opens any concept page.

**Meta-pages, not YAML frontmatter.** Tags, aliases, and relationship metadata could live in per-page frontmatter. We chose meta-pages (`moc-*.md`, `question-patterns.md`) instead: the routing logic is human-readable, editable in the same voice as the rest of the wiki, and reviewable as markdown diffs. Frontmatter is a second syntax for the same information, and it hides the routing behaviour from the page itself. Revisit if a concrete retrieval failure mode emerges that frontmatter would fix (singular/plural alias misses, for instance).

**Raw prose stays immutable and addressable.** The `raw/<book>/chapter-NN-*.md` files are the source of truth. Concept pages distill; MOCs link distillations *and* raw chapter sections where distillation would lose nuance. Chapter anchors (`[[book-name#chapter-N-title]]`) resolve against the per-book summary page so that the linter can check them, and so that Obsidian renders them as first-class wikilinks.

## The four layers

```
question-patterns.md   ← question archetype → MOC set
         ↓
index.md               ← master hub + A–Z appendix
         ↓
moc-*.md (16)          ← narrative topic clusters
         ↓
concept pages (~990)   ← one idea per page, flat in wiki/
         ↓
raw/<book>/chapter-*.md ← source prose (immutable)
```

**Layer 1 — `question-patterns.md`.** The router. Ten-ish real expert-level question archetypes (extract-a-service, scale-10x, pick-a-style, design event-driven communication, adopt SLOs, resolve Conway-friction, pick a database, evolve a schema, build a data platform, secure a data platform, respond to cascading failure), each mapped to the MOCs and key concept pages that ground a high-quality answer. Claude Code reads this page first for any non-trivial question, matches the closest archetype, and reads every MOC the pattern lists.

**Layer 2 — `index.md`.** The master hub. Section 1 points at `question-patterns.md` as the first stop. Section 2 is a 16-row MOC table with a one-sentence description for each. Section 3 is the 8-book table. Section 4 is an A–Z appendix of every concept page, collapsed under `<details>`. The A–Z is the belt-and-braces guarantee that every page is reachable; the MOC table is the intended entry point.

**Layer 3 — `moc-*.md` (16 files).** The narrative topic clusters. Each MOC:

- Opens with a "when to read this" frame.
- Walks the topic cluster in sections, linking to every relevant concept page with a sentence explaining *why* or *when*.
- Hands off to sibling MOCs explicitly (a decomposition MOC cites `moc-data-models-and-storage`, `moc-consistency-and-transactions`, `moc-microservices`, `moc-reliability-and-operations`, etc.).
- Cites raw book chapter sections (`[[book-name#chapter-N-title]]`) where the raw prose carries nuance beyond the distilled concept page.

The 16 MOCs are:

- `moc-architecture-fundamentals` — the definition, characteristics, quantum, fitness functions, ADRs, the architect's stance
- `moc-risk-and-communication` — the architect's soft-skills half
- `moc-components-and-partitioning` — inside-the-box partitioning view
- `moc-architecture-styles` — the catalogue of canonical styles
- `moc-microservices` — running microservices
- `moc-decomposition` — extracting a service from a monolith
- `moc-domain-driven-design` — the modelling discipline
- `moc-data-models-and-storage` — data models, storage engines, encoding, replication, partitioning
- `moc-data-processing` — data in motion: batch, stream, ingestion, pipelines
- `moc-distributed-systems` — fundamental problems of running computation across machines
- `moc-consistency-and-transactions` — correctness under concurrency and partial failure
- `moc-events-and-streaming` — events as integration substrate
- `moc-container-and-serving-patterns` — containerised service shape and lifecycle
- `moc-reliability-and-operations` — SLOs, monitoring, on-call, incident response, release engineering
- `moc-data-engineering` — the discipline view: lifecycle, undercurrents, governance
- `moc-security-and-privacy` — security mindset, technical primitives, privacy, governance

Some concept pages appear in multiple MOCs on purpose. `change-data-capture` is cited by `moc-data-processing` (execution mechanics), `moc-events-and-streaming` (publication substrate), and `moc-decomposition` (async bridge during an extraction) — each with a different framing sentence. The jurisdictional rule for this multi-homing is stated in each MOC's opening and keeps the framings distinct.

**Layer 4 — concept pages (~990).** One idea per page, flat in `wiki/`. Every concept page follows the page format (see below), carries inline `(source: …)` citations, and ends with a `## Related pages` section linking back to other concept pages. Every concept page must be reachable from at least one MOC — this is the linter's contract for "not an orphan."

**Layer 5 (not numbered, but load-bearing) — `raw/<book>/chapter-NN-*.md`.** The source prose, immutable. The extractor writes it once; Claude never edits it. Chapter anchors resolve via the per-book summary page at `wiki/<book>.md`, which carries H2 headings like `## Chapter 4: Decomposing the Database` — slugified to `chapter-4-decomposing-the-database` and cited as `[[monolith-to-microservices#chapter-4-decomposing-the-database]]`.

## Retrieval walkthrough

Worked example against the canonical payments-extraction question: *"I am working on a monorepo Django project containing (1) the public web API, (2) the web UI, and (3) the backend payments processing pipeline that handles billions of dollars a month. All payment transaction info and user data is stored in a single Postgres database. I need to extract the payments backend into a dedicated service so we can scale 10x over the next few years. Using the contents of the wiki, tell me about some approaches I could take and things I should consider."*

1. Claude reads `wiki/index.md` — sees the "Start here" pointer to `question-patterns.md`.
2. Claude reads `wiki/question-patterns.md` — the *Extract a service from a monolith* pattern matches. The pattern lists six MOCs to read: `moc-decomposition`, `moc-data-models-and-storage`, `moc-consistency-and-transactions`, `moc-microservices`, `moc-distributed-systems`, `moc-reliability-and-operations`. It also names a special note: for money-critical domains, `parallel-run-pattern` is not optional.
3. Claude reads all six MOCs in parallel. Each MOC lists 20–80 concept pages with framing sentences, and 3–8 raw chapter anchors.
4. From the MOCs, Claude opens the concept pages whose framing sentences match the question (extraction patterns, DB decomposition, CDC, outbox, saga, bounded context, Conway's law, SLOs, observability, parallel-run for money-critical, …) and the raw chapter sections the MOCs cite for depth (`[[monolith-to-microservices#chapter-3-splitting-the-monolith]]`, `[[monolith-to-microservices#chapter-4-decomposing-the-database]]`, `[[designing-data-intensive-applications#chapter-7-transactions]]`, and similar).
5. Claude drafts the answer, citing specific wiki pages and raw chapter anchors inline.

The expected breadth: 30+ distinct concept pages cited, 5–6 MOCs consulted, 3+ raw book chapter sections cited. The answer covers extraction patterns, DB decomposition sequencing, CDC/outbox for correctness, saga for cross-store transactions, Conway/team topologies, SLOs and observability for the extracted service, and parallel-run given the money-critical domain. If any of those are missing, the navigation layer failed — which is the retrieval-quality regression signal we test against (see `WIKI-REDESIGN-PLAN.md` Verification section).

## Page types and conventions

All pages — concept, MOC, per-book summary, `question-patterns.md` — share the same shell:

```markdown
# Page Title

**Summary**: One to two sentences describing this page.

**Sources**: List of `raw/<book>/<file>.md` references (or `(meta-page; …)` marker for meta-pages).

**Last updated**: YYYY-MM-DD

---

Main content.

## Related pages

- [[related-concept-1]]
- [[related-concept-2]]
```

**Concept page** — one idea, distilled from a specific set of raw chapters. Inline `(source: filename.md)` citations on every factual claim. `## Related pages` lists peer concept pages.

**MOC page** (`moc-*.md`) — meta-page. `**Sources**:` carries the `(meta-page; aggregates concept pages and links to raw chapters)` marker instead of backticked files. Narrative, second-person, no page-length ceiling. Every wikilink earns a sentence of *why* or *when*. Cross-links to sibling MOCs and raw chapter anchors.

**Per-book summary page** (`wiki/<book-name>.md`, 8 of them) — book-level MOC for the source. Opens with the book's thesis, has one H2 per chapter (`## Chapter N: <Full Chapter Title>` — the anchor target for `[[book#chapter-N-title]]` citations), lists the concept pages that chapter fed, and closes with `## Related pages`.

**`question-patterns.md`** — meta-page. The router; archetype → MOC-set mapping.

**`index.md`** — meta-page. Hub layout: Start here → MOC table → Books table → A–Z appendix. Excluded from the page-format check because its structure differs from content pages.

**`log.md`** — append-only change record. Excluded from most checks.

### Wikilink and citation rules

- `[[concept-page]]` — links a concept page by its filename stem (lowercase, hyphenated).
- `[[concept-page|display text]]` — renames the display.
- `[[book-name#chapter-N-title]]` — cites a raw chapter. Resolves against the per-book summary page's H2 heading, slugified. The slug on both sides uses the same normaliser (lowercase, non-alphanumeric → hyphen, collapse, strip). Zero-padding stays on the filename (`chapter-04-*.md`) but is dropped in the anchor (`chapter-4-*`).
- `(source: filename.md)` inline — cites a raw file. The linter resolves this against everything under `raw/`.

The linter (`wiki-linter/lint.py`) enforces:

- **Page format** — title, Summary, Sources, Last updated, divider, Related pages all present (except for meta-pages with carve-outs noted above).
- **Filename** — `^[a-z0-9]+(-[a-z0-9]+)*\.md$`.
- **Wikilink integrity** — every `[[target]]` and `[[target#anchor]]` resolves.
- **Sources existence** — `raw/<path>` referenced in the Sources line must exist on disk (meta-pages exempt).
- **Inline source existence** — `(source: filename.md)` must resolve somewhere under `raw/`.
- **Orphan** — concept pages must be linked from at least one MOC. Concept-page-to-concept-page links do not rescue.
- **Index sync** — every page reachable from `index.md` or from any MOC.
- **Related-pages label validity** — if a bullet uses a `**Label:**` prefix, the label must be one of `Prerequisite / Generalizes / Alternative / Contrast / See also`. Legacy flat-bullet format passes silently.
- **Date parseability** — `**Last updated**` must be `YYYY-MM-DD`, not in the future.

Semantic checks (contradictions, outdated claims, which concepts deserve pages) are out of scope — the human handles those on the linter's report.

## How to extend

**Adding a new book.** Run the `convert-pdf` skill on the PDF in `raw/` to produce per-chapter markdown. Run the `ingest-book` skill — it reads the book, discusses takeaways, creates a per-book summary page at `wiki/<book>.md`, creates/updates concept pages, adds wikilinks, and updates `wiki/index.md` and `wiki/log.md`. After ingest, walk the relevant MOCs (typically 3–5 of the 16) and integrate the new concept pages into the narrative — each addition earns its own *why*/*when* sentence. If the book introduces a genuinely new question archetype, add it as a new pattern in `question-patterns.md`.

**Adding a new concept page.** Create `wiki/<name>.md` with the page format. Add it to at least one MOC (if you don't, the linter flags it as an orphan). Add inline `(source: …)` citations on every factual claim. Update `wiki/log.md`.

**Adding a new MOC.** When a topic cluster grows dense enough that its coverage in existing MOCs becomes thin, split it out into a new `moc-<topic>.md`. Add the MOC to `index.md`'s MOC table. Decide which question-patterns should route to it and update `question-patterns.md`. If the new MOC overlaps with existing MOCs on shared concept pages, state the jurisdictional rule in each MOC's opening so the framings stay distinct.

**Adding a new question pattern.** When a recurring question type doesn't fit an existing pattern, add it as a new section in `question-patterns.md`: *Examples*, a short framing paragraph, the MOCs to read, the key concept pages, and the key raw chapter anchors. Keep the patterns broad — fuzzy matches are fine; over-narrow patterns fragment the router.

**Editing existing concept pages.** Update `**Last updated**` to today's date. Add an entry to `wiki/log.md`. Run the linter before committing.

After any of the above: `cd wiki-linter && uv run python lint.py ../wiki`. Zero errors is the bar; warnings are reviewed.

## What's intentionally out of scope

- **Subdirectory hierarchy for concept pages.** Grep/Glob-based retrieval gets nothing from it; every page belonging to one parent misrepresents real concepts.
- **YAML frontmatter with tags and aliases.** Second syntax for the same information; hides routing from the page. Revisit if a concrete retrieval failure mode would fix (singular/plural alias misses are the likely trigger).
- **`graph.json` sidecar.** Duplicates the implicit wikilink graph; staleness risk.
- **Subdirectory moves of per-book summary pages.** Would break inbound wikilinks for no agent-side gain.
- **Semantic linting.** Contradiction detection, outdated-claim judgements, "does this concept deserve a page" — all LLM-native, not deterministic. The human does this on the linter's report.
- **MCP retrieval design accommodations.** `wiki-mcp/` exists and exposes read-only search, but the current redesign is scoped to Claude Code's file-reading retrieval only. MCP naturally benefits from a better-structured wiki (MOCs are keyword-rich hub pages); revisit if MCP clients show different failure modes.

## Obsidian notes

The repo opens as an Obsidian vault — `.obsidian/` carries the minimal config needed. Caveats:

- **MOCs are very high-degree hubs in the graph view.** `moc-reliability-and-operations` alone carries ~300 outbound wikilinks; every MOC is dense by design. The graph view is readable but dominated by the 16 MOC nodes. This is a feature for agents (the MOCs are the intended entry points) and a visual quirk for humans — it confirms at a glance that the navigation layer is doing its job. Obsidian's "local graph" view on a single concept page is usually more useful than the global graph.
- **Chapter anchors work natively.** `[[monolith-to-microservices#chapter-4-decomposing-the-database]]` resolves in Obsidian's link hover and graph, because the slugifier matches Obsidian's own anchor resolution.
- **Orphans** are surfaced by the linter, not by Obsidian's own orphan view — Obsidian marks a page as orphaned if *nothing* links to it, but the wiki's stricter contract is "must be linked from at least one MOC." Run the linter for that signal.

## Related documents

- `README.md` — what the repo is, how to use the tooling.
- `CLAUDE.md` — operational spec for the Claude Code agent maintaining the wiki.
- `wiki/index.md` — the master hub.
- `wiki/question-patterns.md` — the router.
- `wiki-linter/REQUIREMENTS.md` — what the linter does and does not check.
- `WIKI-REDESIGN-PLAN.md` — the redesign plan that produced the current structure, preserved as context for why the layers exist.
