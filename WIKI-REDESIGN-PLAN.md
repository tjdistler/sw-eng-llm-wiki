# Wiki redesign: MOC navigation layer for grounded expert answers

## Context

`sw-eng-llm-wiki/` is a graph-based knowledge base of software engineering concepts distilled from engineering books (currently 8). The user (Principal Software Engineer) wants Claude Code to answer **expert-level, long-form, multi-cluster architecture questions** grounded in this wiki — quality is the sole priority; token cost is not a concern.

**Canonical example question** (user-provided):
> "I am working on a monorepo Django project containing (1) the public web API, (2) the web UI, and (3) the backend payments processing pipeline that handles billions of dollars a month. All payment transaction info and user data is stored in a single Postgres database. I need to extract the payments backend into a dedicated service so we can scale 10x over the next few years. Using the contents of the wiki, tell me about some approaches I could take and things I should consider. Help me generate a plan."

A question like this touches at least six clusters: **decomposition patterns**, **database decomposition**, **consistency/transactions**, **distributed systems / scaling**, **organizational (Conway's, team topologies)**, **reliability / operations**. The ideal retrieval loads *all relevant MOCs at once* and then composes an answer from dozens of concept pages plus relevant raw book chapter sections.

**Current state** (verified):
- 989 concept pages flat under `wiki/`
- `wiki/index.md`: 1415 lines, 85 semantic groupings, purely tabular
- 8 books ingested: per-book summaries at `wiki/<book-name>.md`; chapters at `raw/<book-name>/`
- Topology: top 10 hub pages receive ~1160 inbound wikilinks
- Linter (`wiki-linter/lint.py`) enforces page format, wikilink resolution, kebab-case filenames, source existence, index completeness, orphans

**Why this change**: a flat tabular index gives Claude Code only keyword-matched entry points. For multi-cluster questions, the agent may miss entire topic areas because no narrative layer tells it "these six topics compose for extraction questions." The fix is a navigation layer that explains *why* concepts connect, plus a question-pattern meta-page that wires real archetypes to MOC combinations.

**Intended outcome**: for the payments-extraction question, Claude Code reads `index.md` → `question-patterns.md` → loads all six relevant MOCs in parallel → follows links to 30–60 concept pages and selected raw chapter sections → produces a plan that integrates extraction patterns, DB migration sequencing, consistency tradeoffs, sharding/scaling, team topologies, and operational concerns including SLOs/observability for the new service.

## Recommended approach

Keep 989 concept pages flat. Keep per-book summary pages at `wiki/<book-name>.md`. Add four things:

1. **A MOC layer** — 16 narrative Map-of-Content pages (one per topic cluster)
2. **A question-patterns meta-page** — `wiki/question-patterns.md` mapping common question archetypes (including the payments example) to MOC combinations
3. **Enhanced `index.md`** — a hub pointing at question-patterns, MOCs, books, and an A–Z appendix
4. **Typed "Related pages"** — upgrade the existing bullet list per concept page to relationship-typed (Prerequisite / Generalizes / Alternative / Contrast / See also)

### 1. Add 16 MOC pages at `wiki/moc-<topic>.md`

Rolled up from the 85 fine-grained index.md groupings into 16 topic clusters. Three clusters are additions on top of the original 13: `moc-reliability-and-operations` for SRE / observability; `moc-data-engineering` and `moc-security-and-privacy` for the data-engineering perspective introduced by *Fundamentals of Data Engineering*. FoDE's source→ingest→transform→serve lifecycle is folded into `moc-data-processing` (execution mechanics) and `moc-data-engineering` (discipline view) rather than getting its own MOC — an earlier draft proposed a separate `moc-ingestion-and-serving`, but the three-way overlap with `moc-data-processing` and `moc-events-and-streaming` on CDC, Kafka, outbox, and broker patterns risked choice-paralysis during retrieval. Hard Parts content slots into existing clusters (coupling taxonomy → components-and-partitioning, trade-off analysis → architecture-fundamentals, decomposition patterns → decomposition, sagas → consistency-and-transactions, reuse and contracts → microservices).

- `moc-architecture-fundamentals.md`
- `moc-risk-and-communication.md`
- `moc-components-and-partitioning.md`
- `moc-architecture-styles.md`
- `moc-microservices.md`
- `moc-decomposition.md`
- `moc-domain-driven-design.md`
- `moc-data-models-and-storage.md`
- `moc-data-processing.md` *(batch + stream execution, pipelines, schedulers, CDC as source-capture, Kappa/Lambda, Dataflow model; absorbs FoDE ingestion-and-serving stages)*
- `moc-distributed-systems.md`
- `moc-consistency-and-transactions.md`
- `moc-events-and-streaming.md` *(event-driven architecture: brokers, choreography, sagas, outbox as event publication, event structure/versioning)*
- `moc-container-and-serving-patterns.md`
- `moc-reliability-and-operations.md` *(new)*
- `moc-data-engineering.md` *(new — FoDE's discipline, lifecycle, undercurrents, data-architecture patterns, governance / quality / modeling)*
- `moc-security-and-privacy.md` *(new — FoDE Ch 10 plus SRE-adjacent security content)*

**Jurisdictional rule for the data-MOC overlap** (state this in each MOC's opening):

- `moc-data-processing` owns execution mechanics — Spark, Flink, Kafka Streams, Beam, schedulers, pipeline topologies — and CDC as a source-capture mechanism.
- `moc-events-and-streaming` owns the architectural use of events — brokers as integration substrate, choreography vs. orchestration, saga, outbox as publication pattern, event design, schema evolution for events.
- `moc-data-engineering` owns the discipline view — lifecycle, undercurrents, governance, data architecture, the data engineer's role.
- Shared concept pages (`change-data-capture.md`, `outbox-table-pattern.md`, `kafka.md`, etc.) are linked from **every MOC where they apply**, with a different framing sentence per MOC explaining the specific lens.

**MOCs should be rich and comprehensive.** No page-length ceiling. Each MOC should:
- Narratively introduce the topic (when to read, how to think about it)
- Link to **every relevant concept page** in that cluster with a sentence of *why* / *when*
- Heavily cross-link to **other MOCs** (a decomposition MOC cites moc-data-models-and-storage, moc-consistency-and-transactions, moc-microservices, moc-reliability-and-operations)
- Link to **relevant raw book chapter sections** (`[[monolith-to-microservices#chapter-4-decomposing-the-database]]`) where raw prose carries nuance beyond the distilled concept pages — these are useful for deep questions where the concept-page distillation may be too terse

**MOC page template** (exemplar sketch for `wiki/moc-decomposition.md`):

```markdown
# MOC: Decomposing a Monolith

**Summary**: Entry point for questions about pulling services out of a monolith —
sequencing, extraction patterns, database untangling, organizational pressure,
and the operational step-up required for the new service.

**Sources**: (meta-page; aggregates concept pages and links to raw chapters)

**Last updated**: 2026-04-17

---

## When to read this

You have a monolith. You suspect microservices might help. Start with
[[why-microservices]] and [[independent-deployability]] to
pressure-test the premise before reaching for any pattern below.

## Is extraction the right move?

[[when-microservices-are-a-bad-idea]], [[extraction-prioritization]],
[[architectural-quantum]]. If the answer is yes, read
[[domain-driven-design]] and [[bounded-context]] to find seam candidates,
and [[coupling]] + [[cohesion]] to judge which seams are real.
[[event-storming]] is the best workshop format for surfacing them with
domain experts.

## Extraction patterns (code)

- [[strangler-fig-pattern]] — the default; route-level interception.
- [[branch-by-abstraction]] — when you can't intercept at the edge.
- [[parallel-run-pattern]] — when correctness must be proven before cutover
  (critical for money / safety-critical domains).
- [[decorating-collaborator-pattern]] — minimal-code legacy integration.
- [[change-data-capture]] — async bridge that lets the new service read
  a projection of the monolith's state during transition.

Deeper reading: [[monolith-to-microservices#chapter-3-splitting-the-monolith]].

## Database decomposition (the hard part)

Projects stall here. The move is almost always [[change-data-capture]] plus
[[shared-database-antipattern]] as an *explicit transitional state*, not a
terminal one. Access-pattern options: [[database-view-pattern]],
[[database-wrapping-service]], [[database-as-a-service-interface]].
For the split itself: [[split-the-database-first]] vs.
[[split-the-code-first]] — read [[monolith-to-microservices#chapter-4-decomposing-the-database]].

See also: [[moc-consistency-and-transactions]] for how to preserve
correctness across the split; [[moc-data-models-and-storage]] for the
target schema shape.

## Correctness across the split

Once data spans two stores, you need [[saga]] (compensations, not 2PC) or
async via [[outbox-table-pattern]]. Read [[moc-consistency-and-transactions]]
end to end if the domain is money / safety-critical.

## Organizational pressure

[[conways-law]], [[team-topologies]]. Newman's *Growing Pains*
[[monolith-to-microservices#chapter-5-growing-pains]] catalogs what breaks
at scale. See [[moc-microservices]] for the ownership model.

## Operational step-up for the extracted service

A new service needs [[slo-expectations]], [[sli]], [[error-budget]], independent CI/CD
([[independent-deployability]]), observability
([[distributed-tracing]], [[structured-logging]]), and on-call readiness.
See [[moc-reliability-and-operations]] end to end before cutover.

## Related MOCs

- [[moc-microservices]]
- [[moc-domain-driven-design]]
- [[moc-data-models-and-storage]]
- [[moc-consistency-and-transactions]]
- [[moc-distributed-systems]]
- [[moc-reliability-and-operations]]

## Related pages

- [[index]]
- [[question-patterns]]
```

Voice: second person, narrative not tabular, no page-count limit, every wikilink earns a sentence of *why* or *when*.

### 2. Add `wiki/question-patterns.md`

A meta-entry-point mapping real multi-cluster question archetypes to a recommended MOC-reading plan and concept-page shortlist. Includes the user's payments-extraction example as a worked pattern.

**Skeleton**:

```markdown
# Question Patterns

**Summary**: A router from real expert-level questions to the MOCs and
concept pages most likely to ground a high-quality answer. When Claude Code
is asked a complex multi-cluster question, find the closest archetype here
and read every MOC it points to before drafting an answer.

**Sources**: (meta-page)

**Last updated**: 2026-04-17

---

## How to use this page

Match the question to a pattern (fuzzy matches are fine). Read the listed
MOCs in full. Follow into concept pages as each MOC suggests. Include raw
chapter sections (cited at the bottom of each MOC) when the distilled
concept page seems too terse for the depth the question requires.

## Pattern: Extract a service from a monolith
Examples: "Split the payments backend out of our Django monolith";
"Pull the notification system into its own service."

Read: [[moc-decomposition]], [[moc-data-models-and-storage]],
[[moc-consistency-and-transactions]], [[moc-microservices]],
[[moc-distributed-systems]], [[moc-reliability-and-operations]].

Key concept pages: [[strangler-fig-pattern]], [[branch-by-abstraction]],
[[parallel-run-pattern]], [[change-data-capture]], [[outbox-table-pattern]],
[[saga]], [[bounded-context]], [[coupling]], [[shared-database-antipattern]],
[[database-as-a-service-interface]], [[conways-law]], [[slo-expectations]],
[[error-budget]].

Key raw chapters: [[monolith-to-microservices#chapter-3-splitting-the-monolith]],
[[monolith-to-microservices#chapter-4-decomposing-the-database]],
[[designing-data-intensive-applications#chapter-7-transactions]].

## Pattern: Scale an existing service 10x
Examples: "Our checkout service needs to handle 10x traffic";
"We're sharding the orders table — what should we consider?"

Read: [[moc-data-models-and-storage]], [[moc-distributed-systems]],
[[moc-reliability-and-operations]], [[moc-architecture-styles]].
[… concepts and raw chapters …]

## Pattern: Pick an architecture style for a greenfield project
[…]

## Pattern: Design event-driven communication between services
[…]

## Pattern: Adopt SLOs / reliability practices for an existing system
[…]

## Pattern: Resolve a Conway-caused organizational friction
[…]
```

Aim for 8–12 patterns initially; add more as they emerge from actual usage.

### 3. Rewrite `wiki/index.md` as a hub

- Section 1: "**Start here**" — one-line pointer to `question-patterns.md` as the first stop for any complex question.
- Section 2: **MOCs by topic cluster** — table of the 16 MOCs with one-sentence descriptions.
- Section 3: **Books** — the 8 per-book summary pages.
- Section 4: **A–Z of concept pages** — collapsed under `<details>` to preserve the linter's "every page appears in index" invariant.

No target length — but in practice ~150–200 lines.

### 4. Upgrade `## Related pages` to typed relationships (phased)

Replace the flat bullet list with relationship-typed subgroups:

```markdown
## Related pages
- **Prerequisite:** [[bounded-context]], [[coupling]]
- **Generalizes:** [[saga]], [[choreography]]
- **Alternative:** [[two-phase-commit]]
- **Contrast:** [[shared-database-antipattern]]
- **See also:** [[conways-law]]
```

Rationale: when following a link, relationship type tells the agent whether to dive deep (Prerequisite) or note-and-move-on (Contrast). Also helps the agent structure its answer ("X is a specialization of Y, whereas Z is an alternative").

**Phasing**: this is 989 pages of mechanical edit. Land the MOC layer first, verify retrieval wins, then edit concept pages in batches (topic cluster at a time). The linter can enforce the canonical labels once any page has adopted the typed format — pages that still use the old flat-bullet format continue to pass.

### 5. Linter changes (`wiki-linter/lint.py`)

- Add `META_PAGES` class covering `moc-*.md`, `question-patterns.md`; exempt from `sources-existence` check (carry `(meta-page; …)` marker).
- Tighten the `orphan` check for concept pages: a concept page must be linked from **at least one MOC** (not just another concept page). MOCs themselves are exempt — they're linked from `index.md`.
- Update `check_index_sync` so pages listed in any `moc-*.md` count as "indexed"; the A–Z appendix in `index.md` remains the belt-and-braces guarantee.
- Allow relationship-type prefixes (`**Prerequisite:**`, `**Generalizes:**`, `**Alternative:**`, `**Contrast:**`, `**See also:**`) inside `## Related pages`. Warn on non-canonical labels; allow the legacy flat-bullet format to pass.
- No MOC size warning. Rich MOCs are desired.
- Update `wiki-linter/REQUIREMENTS.md` to document all new behavior.

**Sequencing**: all four changes land as one PR **after** Phase 7 (all 16 MOCs exist). Landing the orphan tightening earlier would flag every not-yet-MOC-linked concept page as a false-positive orphan.

### 6. Update `CLAUDE.md` question-answering guidance

Replace the current 5-step guidance with:

1. Read `wiki/index.md`. For any non-trivial question, read `wiki/question-patterns.md` next to find the closest archetype.
2. Read **every MOC** the pattern lists (in parallel when possible) — for complex questions, this will typically be 3–6 MOCs.
3. Follow MOC guidance into concept pages. Do not stop at the first keyword match; MOCs surface cross-cluster concepts the agent would otherwise miss.
4. Consult raw book chapter sections cited in MOCs when concept-page distillations seem too terse for the depth the question requires.
5. Cite specific wiki pages and raw chapter references in the answer.
6. If the answer is valuable and not already in the wiki, offer to save it.

### 7. Add `ARCHITECTURE.md` at the repo root + update `README.md`

Humans need a readable explanation of the wiki's design. Split responsibilities:

- `README.md` — stays focused on *what the repo is* and *how to use the tooling*. Add a short "Architecture" pointer paragraph linking to `ARCHITECTURE.md`.
- `ARCHITECTURE.md` — new file at the repo root, capturing the *why* and *how* of the wiki's navigation design. This is the document a new human collaborator (or future-self) reads to understand why the structure exists.

**`ARCHITECTURE.md` outline**:

1. **Goal** — grounded, expert-level answers to multi-cluster engineering questions. LLM-first design; humans are a secondary audience via Obsidian.
2. **Design premises** — why flat (not hierarchical); why narrative MOCs beat tabular indexes for multi-concept questions; why meta-pages instead of frontmatter.
3. **The four layers** — with a diagram:

   ```
   question-patterns.md   ← question archetype → MOC set
            ↓
   index.md               ← master hub + A–Z appendix
            ↓
   moc-*.md (16)          ← narrative topic clusters
            ↓
   concept pages (989)    ← one idea per page, flat in wiki/
            ↓
   raw/<book>/chapter-*.md ← source prose (immutable)
   ```

4. **Retrieval walkthrough** — worked example using the payments-extraction question, showing how the layers compose into a high-quality answer.
5. **Page types and conventions** — MOC pages, concept pages, per-book summaries, `question-patterns.md`, `index.md`, `log.md`. Format + purpose of each.
6. **Wikilink and citation rules** — `[[concept]]`, `[[book-name#chapter-anchor]]`, inline `(source: …)`. What the linter enforces.
7. **How to extend** — practical guidance:
   - Adding a new book (runs through `convert-pdf` → `ingest-book` → update relevant MOCs → maybe add a pattern to `question-patterns.md`)
   - Adding a new concept page (must be linked from a MOC)
   - Adding a new MOC (when cluster is large enough; update `index.md` and `question-patterns.md`)
   - Adding a new question pattern (when a real recurring question type doesn't fit existing patterns)
8. **What's intentionally out of scope** — subdirectory hierarchy, frontmatter, `graph.json`, semantic linting.
9. **Obsidian notes** — graph view caveats (MOCs are high-degree hubs); vault-level settings if any.

**`README.md` changes**:

- Update the Layout code block to include `moc-*.md`, `question-patterns.md`, `ARCHITECTURE.md`.
- Update "Using the wiki" section: replace "Claude reads `wiki/index.md` first" with a one-paragraph description of the question-patterns → MOCs → concept pages flow, linking to `ARCHITECTURE.md` for details.
- Add an "Architecture" heading with a one-line description and link to `ARCHITECTURE.md`.

Keep `README.md` short and usage-focused; push all design rationale to `ARCHITECTURE.md`.

## Critical files

- `wiki/index.md` — rewrite as hub
- `wiki/question-patterns.md` — new
- `wiki/moc-*.md` — 16 new MOCs
- `wiki/<book-name>.md` × 8 — per-book summary H2 chapter renames (Phase 1 prerequisite; enables `[[book#chapter-N-title]]` resolution)
- `wiki-linter/lint.py` — META_PAGES class, tightened orphan check, index-sync update, typed-Related-pages handling (one PR after Phase 7)
- `wiki-linter/REQUIREMENTS.md` — document new behavior
- `CLAUDE.md` — revised question-answering guidance
- `ARCHITECTURE.md` — new file at repo root, human-facing design doc
- `README.md` — update Layout, "Using the wiki", add Architecture pointer
- Concept pages (989) — typed Related pages rollout, phased and deferred pending Phase 13 verification

Per-book summary pages (`wiki/<book-name>.md`) stay at current paths — only chapter H2 headings change; no file renames, no moves.

## Reused conventions

- Page format (`# Title` / `**Summary**` / `**Sources**` / `**Last updated**` / `---` / body / `## Related pages`) applies to MOCs and `question-patterns.md` too, with `(meta-page; …)` as the Sources value.
- Wikilink format unchanged; MOCs use `[[concept]]` and `[[book-name#chapter-N-<title>]]` for raw chapter citations.
- Per-book summary pages (`wiki/monolith-to-microservices.md` etc.) already serve as book-level MOCs stylistically — use them as the voice template for topic MOCs.
- `[[book-name#chapter-N-<title>]]` anchors resolve against headings in the per-book summary page, **not** the raw file directly. Current summary headings read `## Chapter N concepts` (slug `chapter-N-concepts`) which does not match the intended citation format — Phase 1 renames these H2s to `## Chapter N: <Full Chapter Title>` so slugs match. Raw filenames stay zero-padded (`chapter-04-*.md` for file-sort stability); headings and wikilinks use `Chapter 4: <Title>` without the leading zero.
- Slugifier and wikilink regex: `wiki-linter/lint.py:76` (`slugify`), `wiki-linter/lint.py:26` (`WIKILINK_RE`). Anchors are slugified identically on both sides of the comparison.

## Phasing (committable, reviewable checkpoints)

13 committable phases plus one conditional. Each phase is independently `git revert`-able; no concept page is renamed or moved. Every phase appends an entry to `wiki/log.md` (not repeated below).

### Phase 1 — Per-book H2 rename (prerequisite) ✅ Complete (2026-04-19)

**Files**: `wiki/<book>.md` × 8.
Rename each `## Chapter N concepts` → `## Chapter N: <Full Chapter Title>` (titles taken from `raw/<book>/chapter-NN-*.md`). After this, anchors like `[[monolith-to-microservices#chapter-4-decomposing-the-database]]` resolve via the current linter's slug match — no linter change needed.
**Commit**: 1 (8 file edits). **Review**: summaries still read cleanly; `uv run python lint.py ../wiki` green. **Blocks**: every later MOC that cites raw chapters.

### Phase 2 — MOC pilot: `moc-decomposition` ✅ Complete (2026-04-19)

**Files**: `wiki/moc-decomposition.md` (new), `wiki/index.md` (add entry to keep linter happy).
Write per §1 template with these refinements folded in:
- Lead with "Is extraction the right move?" (decision frame) **before** the pattern catalogue, so the decomposition↔microservices handoff reads naturally.
- Use actual on-disk page names: `parallel-run-pattern`, `shared-database-antipattern`, `database-as-a-service-interface`, `conways-law` (no `inverse-conway-maneuver` page), `slo-expectations` (no `slo` page), `decorating-collaborator-pattern`, `why-microservices` (no `microservices-are-not-the-goal` page).
- Template also references `[[sli]]`, `[[structured-logging]]`, `[[split-the-code-first]]`, `[[team-topologies]]` — none of these exist on disk as of final-pass verification. The Phase 2 writer decides per page: either substitute with an existing page (e.g. drop `[[sli]]` if `slo-expectations` + `error-budget` cover the point) or add it as a new concept page if the wiki truly should carry the concept. Run the linter to confirm.
- Explicit jurisdictional handoffs to sibling MOCs (`moc-microservices`, `moc-data-models-and-storage`, `moc-consistency-and-transactions`, `moc-reliability-and-operations`).

**Commit**: 1. **Critical review checkpoint**: voice, density, every wikilink earns a "why"/"when", raw chapter anchors resolve, linter green. This is the template the remaining 15 MOCs copy — iterate here before Phase 3.

### Phase 3 — Architecture-core MOCs (4) ✅ Complete (2026-04-19)

`moc-architecture-fundamentals`, `moc-risk-and-communication`, `moc-architecture-styles`, `moc-components-and-partitioning`.
**Commits**: 1 per MOC, or bundled. **Review**: cluster-wide coherence; consistent terminology.

### Phase 4 — Service-design MOCs (2) ✅ Complete (2026-04-19)

`moc-microservices`, `moc-domain-driven-design` (decomposition already in Phase 2).
**Review — specific check**: decomposition ↔ microservices boundary. Where does the agent start for "should we extract?" vs. "how do we organize around services?"

### Phase 5 — Data MOCs (3) ✅ Complete (2026-04-19)

`moc-data-models-and-storage`, `moc-data-processing` (carries folded-in ingestion-and-serving content), `moc-data-engineering`.
**Review — specific check**: jurisdictional rule. CDC, Kafka, outbox framed differently in processing vs. engineering? Execution mechanics (processing) vs. discipline view (engineering) clean?

### Phase 6 — Distributed + events MOCs (3) ✅ Complete (2026-04-19)

`moc-distributed-systems`, `moc-consistency-and-transactions`, `moc-events-and-streaming`.
**Review — specific check**: events-vs-processing boundary; saga placement; outbox multi-home framing (capture in data-processing, publication in events-and-streaming, correctness bridge in consistency-and-transactions).

### Phase 7 — Ops/security MOCs (3) ✅ Complete (2026-04-19)

`moc-container-and-serving-patterns`, `moc-reliability-and-operations`, `moc-security-and-privacy`.
**Review — specific check**: deployment-pattern dual ownership (mechanics in container-and-serving, reliability lens in reliability-and-operations); platform topics (service discovery, load balancing, DNS, feature flags, capacity planning, incident response) cluster under named sub-sections in reliability.
**End of Phase 7**: all 16 MOCs exist. Optional cross-MOC coherence sweep before Phase 8.

### Phase 8 — Question patterns (router) ✅ Complete (2026-04-19)

**Files**: `wiki/question-patterns.md` (new), `wiki/index.md` (add entry).
8–12 archetypes including the payments example; each lists MOCs + key concept pages + raw chapter anchors.
**Commit**: 1. **Review**: fuzzy-matchable archetypes; MOC combos exhaustive, not redundant.

### Phase 9 — Index hub rewrite ✅ Complete (2026-04-19)

**Files**: `wiki/index.md` (full rewrite).
Start-here pointer to `question-patterns.md` → 16-MOC table → 8-book table → A–Z appendix under `<details>`.
**Commit**: 1. **Review**: reads as a hub, not a catalog.

### Phase 10 — Linter update

**Files**: `wiki-linter/lint.py`, `wiki-linter/REQUIREMENTS.md`.
`META_PAGES` class (exempt `moc-*.md`, `question-patterns.md` from sources-existence); tightened orphan check (concept pages must link from ≥1 MOC; MOCs themselves are exempt); MOC-aware index-sync (pages listed in any MOC count as indexed); typed Related-pages prefix allowance. Run lint; expect green.
**Must come after Phase 7** to avoid false orphan positives. **Commit**: 1.

### Phase 11 — `CLAUDE.md` guidance

Replace the question-answering section with the 6-step flow from §6. **Commit**: 1.

### Phase 12 — Human docs

**Files**: `ARCHITECTURE.md` (new, repo root), `README.md` (Layout, Using-the-wiki pointer, Architecture heading). **Commit**: 1.

### Phase 13 — Verification (gate, not a commit)

Run linter (zero errors). Run the 5-question regression suite (see Verification section) in fresh Claude Code sessions with no preamble. Diff against a pre-change worktree. Score against the rubric (correctness / depth / coverage / citations). Record findings in `wiki/log.md`.
**If rubric met → design is done.** If gaps surface → Phase 14.

### Phase 14 — Typed Related pages rollout *(deferred, conditional on Phase 13)*

989 concept pages, phased by topic cluster (~5–10 commits). Add `Prerequisite / Generalizes / Alternative / Contrast / See also` prefixes. **Only** start if Phase 13 shows a retrieval gap that typed relationships would plausibly close.

## Verification

End-to-end retrieval-quality check:

1. Run `cd wiki-linter && uv run python lint.py ../wiki` — zero errors; warnings reviewed.
2. In a fresh Claude Code session with no preamble beyond pointing at the repo, run the **canonical payments-extraction question** (from Context above). Record:
   - Distinct wiki pages cited (expect 30+)
   - Distinct MOCs consulted (expect 5–6)
   - Raw book chapter sections cited (expect 3+)
   - Whether the answer covers: extraction patterns, DB decomposition sequencing, CDC/outbox for correctness, saga for cross-store transactions, Conway/team topologies, SLOs and observability for the extracted service, parallel-run given money-critical domain
3. Run 4 additional questions spanning different archetypes in `question-patterns.md`:
   - "When is CDC the right choice vs. an outbox pattern, and how do they interact?"
   - "What are the tradeoffs between choreography and orchestration for sagas in a payment flow?"
   - "How should I think about architectural quantum when picking between event-driven microservices and a modular monolith?"
   - "We have no SLOs and want to start — what's a sensible adoption path?"
4. Compare against a pre-change git revision (stash or worktree) with the same prompts. Expect materially more cited pages, cross-cluster coverage, and no regressions in correctness (manual rubric: correctness, depth, coverage, citation integrity).

Retain the 5-question set as an ongoing retrieval-quality regression suite for future wiki additions.

## Out of scope (explicitly deferred)

- **Subdirectory reorganization** of the 989 concept pages — not doing. Grep/Glob-based agents don't benefit from hierarchy; it only adds churn.
- **YAML frontmatter with tags / aliases** — defer until a concrete retrieval failure mode emerges that would fix (e.g., singular/plural alias misses). Revisit after MOC + typed-Related-pages rollout.
- **`graph.json` sidecar** — not doing. Duplicates the implicit graph; staleness risk.
- **Moving per-book summary pages** into `wiki/books/` — not doing; breaks inbound wikilinks for no agent-side gain.
- **MCP retrieval design accommodations** — `wiki-mcp/` exists and exposes `wiki_search`, `wiki_list_pages`, `wiki_read_range`, `raw_list_chapters`, etc., but this redesign is scoped to Claude Code's file-reading retrieval only. MCP naturally benefits from a better-structured wiki (MOCs are keyword-rich hub pages); revisit if MCP-based clients show different failure modes.
