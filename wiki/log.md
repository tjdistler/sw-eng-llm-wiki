# Wiki Log

Append-only record of all operations.

---

## 2026-04-19 — Wiki redesign fix-up: convert stale `(forthcoming)` MOC pointers to wikilinks

Re-verification of Phase 2-7 PRs surfaced one missed check: each MOC was committed with `*moc-X* (forthcoming)` italic prose pointers to siblings that hadn't yet landed, and no later PR went back to upgrade those pointers as the sibling MOCs landed. Result: 72 stale "(forthcoming)" references across 12 MOCs, telling the agent to wait for handoffs that already exist on disk.

This commit converts every stale pointer to a `[[moc-X]]` wikilink, removes the now-obsolete "Once the corresponding MOCs land, the handoffs below become wikilinks…" preamble paragraph from 10 `## Sibling MOCs` sections, and cleans up trailing modifiers ("once it lands"). Also fixes the `*Consistency and Transactions* material (MOC forthcoming)` reference at `moc-decomposition.md:115` to point at the now-existing `[[moc-consistency-and-transactions]]`.

Untouched: the single legitimate `forthcoming` reference at `moc-reliability-and-operations.md:385`, which references Phase 8's not-yet-landed `question-patterns.md`.

Linter: 0 errors, 1 pre-existing unrelated warning. All 783 unique concept-page wikilinks across the 16 MOCs resolve; all 85 raw-chapter anchors resolve.

---

## 2026-04-19 — Wiki redesign Phase 7: ops/security MOCs (3)

Added the three Phase 7 Map-of-Content pages — `moc-container-and-serving-patterns`, `moc-reliability-and-operations`, `moc-security-and-privacy` — completing the 16-MOC layer. Deployment patterns (blue/green, canary, progressive delivery, feature flags) are dual-owned: mechanics in container-and-serving, safety practice in reliability-and-operations, with explicit framing sentences in each. Platform topics (service discovery, load balancing, capacity planning) cluster under named sub-sections in reliability-and-operations. Security-and-privacy documents known gaps (no auth/IAM, privacy-regulation-specific, or app-security concept pages yet) for future ingests to fill.

---

## 2026-04-19 — Wiki redesign Phase 6: distributed + events MOCs (3)

Added the three Phase 6 Map-of-Content pages — distributed systems, consistency and transactions, and events and streaming — following the voice template established in Phase 2 and carried through Phases 3–5. Each MOC opens with the jurisdictional rule so that shared pages (saga, outbox, CDC, Kafka/log-based brokers, linearizability, CAP, single-writer principle) are framed under different lenses in different MOCs rather than duplicated or arbitrated at retrieval time.

- `moc-distributed-systems` — owns the *systems* layer: partial failures, unreliable networks/clocks, process pauses, fencing, replication, partitioning, consensus (Paxos/Raft), coordination services (ZooKeeper/etcd/Chubby), ownership election at container granularity, distributed scheduling (SRE cron), Google production infrastructure as the concrete case.
- `moc-consistency-and-transactions` — owns the *guarantees* layer: ACID, isolation levels and anomalies, consistency models (linearizability/causal/eventual/CAP), 2PC vs sagas, the full Hard Parts dynamic-coupling cube of eight saga variants, compensations, outbox as the correctness bridge across a saga step, effectively-once via idempotence and end-to-end operation IDs.
- `moc-events-and-streaming` — owns events as the *integration substrate*: request-based vs event-based framing, brokers (log-based vs traditional) as infrastructure, broker vs mediator topology, event design and contracts (schema registry, Avro/Protobuf), data liberation (CDC, outbox, eventification), EDM implementation styles, request-response integration patterns, supportive tooling, testing, and deployment.

Saga, outbox, and CDC now appear in all three new MOCs (and `moc-data-processing`) with different framing sentences that state each MOC's lens explicitly. Phase 6 review check (per plan): the events-vs-processing boundary is named at the top of the events MOC; saga placement is cross-linked (taxonomy depth in consistency; integration placement in events); outbox's three-MOC home is called out in each of them.

Files touched:

- `wiki/moc-distributed-systems.md` — new
- `wiki/moc-consistency-and-transactions.md` — new
- `wiki/moc-events-and-streaming.md` — new
- `wiki/index.md` — added three MOC entries to the `## Maps of Content (MOCs)` section
- `wiki/log.md` — this entry
- `WIKI-REDESIGN-PLAN.md` — marked Phase 6 complete

Phase 6 of `WIKI-REDESIGN-PLAN.md` complete. All ten of sixteen MOCs now exist; Phase 7 (ops/security MOCs) remains before the design is feature-complete for the planned narrative layer.

---

## 2026-04-19 — Wiki redesign Phase 5: data MOCs (3)

Added the three data Map-of-Content pages, modelled on the Phase 2-4 voice template (narrative voice, every wikilink earning a "why"/"when", explicit jurisdictional handoffs, raw chapter anchors for deeper reading). Each MOC opens with the jurisdictional rule that names which MOC owns what so the CDC/Kafka/outbox overlap is resolved at the top of each page rather than arbitrated at retrieval time.

- `moc-data-models-and-storage` — owns model / engine / encoding / storage-layer replication+partitioning / warehouse-lake-lakehouse / DB type selection / per-service data ownership (target-side shape).
- `moc-data-processing` — owns execution mechanics: ingestion (with CDC as the source-capture mechanism), batch engines, stream processing, stateful streaming, pipeline architectures (Lambda/Kappa/Dataflow), pipeline operations (Google Workflow, periodic vs continuous), query/transformation, serving mechanics, and pipeline-side data integrity.
- `moc-data-engineering` — owns the FoDE discipline view: role, lifecycle (five stages + six undercurrents), data architecture patterns, technology selection, governance, stakeholder map, future-of-DE predictions. Routes security deep material to the forthcoming `moc-security-and-privacy`; routes SRE/observability deep material to `moc-reliability-and-operations`.

Files touched:

- `wiki/moc-data-models-and-storage.md` — new
- `wiki/moc-data-processing.md` — new
- `wiki/moc-data-engineering.md` — new
- `wiki/index.md` — added three MOC entries to the `## Maps of Content (MOCs)` section

Linter: 0 errors. The three new MOCs are not orphan-flagged because they mutually link to one another in their jurisdictional-rule and sibling-MOC sections, and also inbound-link to existing MOCs (`moc-decomposition`, `moc-microservices`, `moc-domain-driven-design`, `moc-architecture-fundamentals`) — each picks up inbound wikilinks from at least one non-`index.md` page. One pre-existing warning in `idempotence.md` (unrelated to Phase 5).

---

## 2026-04-19 — Wiki redesign Phase 4: service-design MOCs (2)

Added the two service-design Map-of-Content pages. Both follow the Phase 2/3 voice template (narrative, every wikilink earns a "why"/"when", explicit jurisdictional handoffs). Decomposition ↔ microservices boundary is made explicit in each MOC's "when to read this" section: `moc-decomposition` owns *getting to* microservices from a monolith; `moc-microservices` owns *running* them; `moc-domain-driven-design` owns the modelling craft that both of the others borrow from.

Files touched:

- `wiki/moc-microservices.md` — new (defining properties, is-this-the-right-style gate, independent deployability, granularity, data ownership, communication sync/async/event-driven, reuse, platform substrate and microservice tax, growing pains, Conway/organisation, sibling MOCs)
- `wiki/moc-domain-driven-design.md` — new (core vocabulary, ubiquitous-language placeholder, workshop techniques including event storming, modelling-enough discipline, domain-partitioning consequence, microservices bridge, data-ownership bridge, when DDD isn't a fit, sibling MOCs)
- `wiki/index.md` — added both MOC entries to the `## Maps of Content (MOCs)` section

Linter: 0 errors. One pre-existing warning in `idempotence.md` (unrelated to Phase 4).

---

## 2026-04-19 — Wiki redesign Phase 3: architecture-core MOCs (4)

Added the four architecture-core Map-of-Content pages, modelled on the Phase 2 `moc-decomposition` template (narrative voice, every wikilink earning a "why"/"when", explicit jurisdictional handoffs to sibling MOCs, raw chapter anchors for deeper reading). Sibling-MOC handoffs to forthcoming Phase 4–7 MOCs are still noted in prose, but the four new MOCs and `moc-decomposition` cross-link to each other where the boundary already exists.

Files touched:

- `wiki/moc-architecture-fundamentals.md` — new (definition, laws, characteristics, the quantum, fitness functions, evolution, ADRs, trade-off discipline, the architect's stance)
- `wiki/moc-risk-and-communication.md` — new (risk matrix and risk storming, diagramming, presentation, ADRs as communication artefact, leadership, providing guidance, negotiation, career path)
- `wiki/moc-architecture-styles.md` — new (monolithic-vs-distributed, the eight Part II styles, choosing-style procedure, comparison scorecard, cross-style coupling concepts)
- `wiki/moc-components-and-partitioning.md` — new (components, technical-vs-domain partitioning, modularity / cohesion / coupling / connascence triad, granularity drivers and integrators, *Hard Parts*'s six-pattern component-decomposition playbook, deeper coupling axes)
- `wiki/index.md` — added four MOC entries to the `## Maps of Content (MOCs)` section

Linter: 0 errors. Warnings: the four new MOC files and `moc-decomposition` flagged as orphans (expected — MOCs are only linked from `index.md` which the orphan check excludes; Phase 10 updates the linter to exempt MOCs).

---

## 2026-04-19 — Wiki redesign Phase 2: MOC pilot (moc-decomposition)

Added the first Map-of-Content page, `wiki/moc-decomposition.md`, covering service extraction from a monolith end-to-end: decision frame, seam-finding, extraction patterns, database decomposition, correctness across the split, organisational pressure, and the operational step-up. Sibling MOC handoffs are noted in prose (not wikilinks) pending Phases 3–7. Added a new `## Maps of Content (MOCs)` section at the top of `wiki/index.md` with the single MOC entry.

Files touched:

- `wiki/moc-decomposition.md` — new
- `wiki/index.md` — new `## Maps of Content (MOCs)` section with `moc-decomposition` entry

Linter: 0 errors. Warnings: `moc-decomposition.md` flagged as orphan (expected — MOCs are only linked from `index.md` which the orphan check excludes; Phase 10 updates the linter to exempt MOCs).

---

## 2026-04-19 — Wiki redesign Phase 1: per-book H2 chapter renames

Renamed per-book summary H2 chapter headings to `## Chapter N: <Full Chapter Title>` so `[[book-name#chapter-N-title]]` wikilink anchors resolve via the linter's slug match. Prerequisite for MOCs introduced in later phases.

Files touched:

- `wiki/monolith-to-microservices.md` — 5 H2s (`## Chapter N concepts` → titled)
- `wiki/designing-data-intensive-applications.md` — 12 H2s
- `wiki/designing-distributed-systems.md` — 11 H2s (Chapters 2–12)
- `wiki/fundamentals-of-software-architecture.md` — 24 H2s
- `wiki/fundamentals-of-data-engineering.md` — 11 H2s (em-dash → colon; slugs unchanged but form normalised)
- `wiki/site-reliability-engineering.md` — 34 chapter H2s converted from `## <Topic> (Chapter N)` to `## Chapter N: <Title>`; two additional Chapter 1 H2s demoted to H3 subsections
- `wiki/building-event-driven-microservices.md` — 15 chapter H2/H3 headings converted; `## Foundations (Chapters 1–2)` split into Chapter 1 and Chapter 2 H2s; `## Microservice implementation styles (Chapters 9–12)` umbrella retained with chapter H3s retitled
- `wiki/software-architecture-the-hard-parts.md` — no per-chapter H2 sections exist; unchanged

Linter green (0 errors; 1 pre-existing warning unrelated to this change).
