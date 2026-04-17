# Choosing the Appropriate Architecture Style

**Summary**: Richards and Ford's closing Part II chapter — the decision process by which an architect picks one of the eight Part II styles (or a hybrid) for a specific system. The chapter refuses to give a recommendation and instead names the inputs (domain, [[architecture-characteristics|characteristics]], data, organisational factors, process / team / ops maturity, domain-to-architecture isomorphism) and the three structural decisions (monolith vs distributed, where data lives, sync vs async communication). It also names **shifting architecture fashion** as a permanent environmental force the architect must read but not blindly follow.

**Sources**: `raw/fundamentals-of-software-architecture/chapter-18-choosing-the-appropriate-architecture-style.md`

**Last updated**: 2026-04-16

---

## The opening disclaimer

Richards and Ford open Chapter 18 with a refusal:

> It depends! With all the choices available (and new ones arriving almost daily), we would like to tell you which one to use — but we cannot. Nothing is more contextual to a number of factors within an organization and what software it builds. (source: chapter-18)

Choosing a style is the culmination of trade-off analysis across [[architecture-characteristics|characteristics]], domain, strategic goals, and a long list of external forces — it is the applied form of the [[laws-of-software-architecture|First Law of Software Architecture]] (*everything is a trade-off*) at the highest level at which an architect reasons.

## Shifting architecture "fashion"

Preferred architecture styles shift over time. Chapter 18 names **six forces** driving that shift (source: chapter-18):

1. **Observations from the past** — new styles arise as responses to specific pain points in previous styles. The post-[[orchestration-driven-soa|SOA]] reassessment of enterprise-wide reuse is the book's running example: [[microservices]] are a direct backlash.
2. **Changes in the ecosystem** — the software ecosystem's rate of change is chaotic; Kubernetes went from nonexistent to industry standard in a few years.
3. **New capabilities** — sometimes a new tool is not a replacement but a paradigm shift. Docker / containers did this for deployment architecture.
4. **Acceleration** — the rate of change itself is rising. Architects live in constant flux.
5. **Domain changes** — business evolution, mergers, acquisitions all change what the architecture must support.
6. **Technology changes** — organisations try to keep up with technology shifts that have obvious bottom-line benefits.
7. **External factors** — licensing cost, vendor stability, regulatory shifts can force migrations regardless of engineering preference.

The architect's job is not to follow fashion, but to **understand current industry trends well enough to make intelligent decisions about when to follow and when to make exceptions** (source: chapter-18). This is the Chapter 2 [[technical-breadth-vs-depth|breadth-over-depth]] stance applied to style catalogues.

## The decision criteria

Before choosing a style, Richards and Ford name six inputs the architect must already understand (source: chapter-18):

- **The domain.** Not as a subject-matter expert, but with a good general understanding of the major aspects — particularly those that affect operational [[architecture-characteristics|characteristics]].
- **Architecture characteristics that impact structure.** The [[identifying-architecture-characteristics|Chapter 5]] work. Which -ilities must the system support, in what priority?
- **Data architecture.** Schema, persistence, and data-flow concerns. Especially important when the new system has to interact with older or in-use data architecture. (The book explicitly defers deep data-architecture treatment as a separate specialisation.)
- **Organisational factors.** Cloud-vendor cost; M&A strategy (which pushes toward open / integration-friendly designs); engineering budget.
- **Process, team, and operational concerns.** If the organisation lacks Agile engineering maturity, styles that depend on it (microservices in particular) will struggle. Operational maturity (DevOps, observability, automation) similarly gates the distributed styles.
- **Domain/architecture isomorphism.** Some domain shapes match some architecture shapes. [[microkernel-architecture|Microkernel]] fits problems with a clean axis of customisation (per-jurisdiction, per-device, per-form). [[space-based-architecture|Space-based]] fits genome-analysis / bursty-concurrent-load domains. Highly coupled, multi-page-form domains fit *badly* with highly decoupled architectures like [[microservices]] — [[service-based-architecture|service-based]] is the better match.

## The three structural decisions

Given those inputs, Chapter 18 names three decisions as the structural output of the selection process (source: chapter-18):

### 1. Monolith versus distributed

This is the Chapter 9 [[monolithic-vs-distributed|monolithic-vs-distributed split]] operationalised via the Chapter 7 [[architectural-quantum|quantum]] concept:

- **One set of characteristics fits the whole system** → a single quantum → [[monolith|monolith]] (one of [[layered-architecture]] / [[pipeline-architecture]] / [[microkernel-architecture]]).
- **Different parts of the system need materially different characteristics** → multiple quanta → a distributed style ([[service-based-architecture]] / [[event-driven-architecture]] / [[space-based-architecture]] / [[orchestration-driven-soa]] / [[microservices]]).

Other factors can still push toward distribution even when one characteristic set would suffice — budget, team-scaling, independent deployability. But the quantum-count analysis is the primary test.

### 2. Where should data live?

- In a **monolith**, the default is a single relational database (sometimes a handful).
- In a **distributed architecture**, the architect must decide *which services persist data* and *how data flows through the architecture to build workflows*. This is [[database-decomposition|database decomposition]] territory, and it ties tightly to bounded-context identification.

Structure and behaviour must be considered together; iteration is expected.

### 3. Sync versus async communication

Once data partitioning is decided, the next call is protocol style:

- **Synchronous** is more convenient in most cases but caps scalability, reliability, and fault isolation. The caller waits; a slow callee becomes a slow caller.
- **Asynchronous** buys performance and scale but opens a catalogue of headaches: data synchronisation, deadlocks, race conditions, debugging complexity.

Chapter 18 states the prescription as a one-liner: **use synchronous by default, asynchronous when necessary** (source: chapter-18). This is the same principle that sits under [[event-driven-architecture]]'s request-reply discussion and under Newman's sync-first-then-event-driven advice.

## Outputs of the decision process

The Chapter 18 process produces three artefacts (source: chapter-18):

1. **The architecture topology itself** — the style (possibly hybrid) the architect has chosen, with its component structure and communication patterns.
2. **Architecture Decision Records (ADRs)** — the captured reasoning for the decisions that required the most architect effort. Chapter 19 is the full treatment; they are the load-bearing mechanism the [[laws-of-software-architecture|Second Law]] ("why is more important than how") prescribes.
3. **[[architecture-fitness-function|Architecture fitness functions]]** — the automated checks that protect the important principles and operational characteristics from silent erosion.

These three — style + ADRs + fitness functions — are the *complete* output of an architectural selection, not just the picked style.

## Worked case studies

### Silicon Sandwiches (monolith case)

The [[architecture-katas|Silicon Sandwiches kata]] was the Chapter 5 example for deriving characteristics from requirements. Chapter 18 returns to it to make the style selection concrete (source: chapter-18).

The characteristics analysis concluded that **a single quantum was sufficient** — Silicon Sandwiches is simple, budget is modest, and no operational-characteristic separation is needed. That points at a monolith. Two monolithic designs are worked through:

**Modular monolith.** Domain-centric components, single database, single deployment, web UI with mobile considerations. Each identified domain is a component; a deliberate design discipline is to carve the database schema along the same domain boundaries so that a future migration to a distributed architecture stays cheap. Customisability — which the style doesn't natively support — becomes an explicit `Override` component every domain references. The `Override` reference is *itself* a good candidate for a [[architecture-fitness-function|fitness function]].

**Microkernel.** The customisability requirement matches the [[microkernel-architecture|microkernel]] style's domain-to-architecture isomorphism exactly. The core holds the domain components + single relational DB; common customisations live in one plug-in set (with its own database); local customisations live as per-locality plug-ins, each with its own data. Plug-ins stay decoupled because they never call each other. The design uses **Backends for Frontends (BFF)** as a thin microkernel adapter layer — one adapter per frontend device (iOS, web, etc.) translates generic backend output into device-optimal format. Communication can stay synchronous throughout; no performance or elasticity requirement forces async.

The two designs are both legitimate. The microkernel variant better matches the customisability requirement structurally; the modular monolith is simpler and cheaper. This is what the [[laws-of-software-architecture|First Law]] looks like at style-selection scale: two viable designs, different trade-offs, architect's job to name them.

### Going, Going, Gone (distributed case)

The [[architectural-quantum|Going, Going, Gone auction kata]] from Chapter 7 is the distributed counterpart (source: chapter-18). Characteristics analysis had already shown that different parts of the system need *different* architecture characteristics — auctioneer availability differs from bidder scalability, and ambitious levels of scale / elasticity / performance are explicit requirements.

That rules out monolithic styles and the single-quantum distributed styles. The candidates are [[event-driven-architecture|event-driven]] and [[microservices]]. Chapter 18's reasoning for picking microservices:

- Microservices better supports *differing operational characteristics per quantum*.
- Pure event-driven architectures distinguish parts by communication style (orchestrated vs choreographed) rather than by operational-characteristic profile.
- Microservices' weak point (performance) can be addressed with deliberate design — event-driven mechanics can be embedded where async buffering or decoupling is needed, without committing the whole system to event-driven shape.

The resulting design:

- **Three user interfaces**: Bidder (many), Auctioneer (one per auction), Streamer (read-only video-plus-bid feed — read-only allows optimisations unavailable to read-write paths).
- **Eight services**: BidCapture, BidStreamer, BidTracker (the unifier — both inbound connections asynchronous so message queues buffer between wildly different rates), Auctioneer Capture (separated from Bid Capture because of different characteristics), Auction Session (per-auction workflow), Payment (third-party), Video Capture, Video Streamer.
- **Five quanta**: Payment, Auctioneer, Bidder, Bidder Streams, Bid Tracker.
- **Async chosen deliberately** where different rates must be reconciled (bid-capture fan-in) or where downstream slowness would cascade (Payment can process every 500 ms; many simultaneous auction-ends would cause timeouts under sync).

Chapter 18 explicitly closes with:

> This isn't the "correct" design for GGG, and it's certainly not the only one. We don't even suggest that it's the best possible design, but it seems to have the least worst set of trade-offs. (source: chapter-18)

This is the book's [[architecture-characteristics|"least worst architecture"]] framing applied to style selection. There is no correct answer; there is the answer whose trade-offs you can defend.

## Relationship to the rest of the book

Chapter 18 is the structural closer of Part II. It assumes the reader has internalised:

- [[architecture-characteristics]] (Ch 4) — what a characteristic is.
- [[identifying-architecture-characteristics]] (Ch 5) — how to produce the short list.
- [[measuring-architecture-characteristics]] (Ch 6) — how to govern the short list.
- [[architectural-quantum]] (Ch 7) — the scope at which characteristics apply; the monolith-vs-distributed test.
- [[technical-vs-domain-partitioning]] (Ch 8) — the orthogonal partitioning axis.
- [[monolithic-vs-distributed]] (Ch 9) — the top-level split; the eight fallacies as the distribution cost.
- The eight style pages (Chapters 10–17).

The chapter produces the artefact the next chapters in Part III consume: Chapter 19 is the full treatment of [[architecture-decisions-vs-design-principles|architecture decisions]] and ADRs, Chapter 20 analyses architecture risk, and so on — every Part III technique operates on the output of the selection process Chapter 18 describes.

## Related pages

- [[architecture-style-comparison]] — the scorecard comparison across all eight Part II styles; the reference material a style-selection decision draws on
- [[architecture-characteristics]] — the -ilities a selection has to prioritise
- [[identifying-architecture-characteristics]] — how the short list gets produced
- [[architectural-quantum]] — the monolith-vs-distributed test
- [[monolithic-vs-distributed]] — the top-level style classification
- [[technical-vs-domain-partitioning]] — the orthogonal partitioning axis
- [[architecture-katas]] — Silicon Sandwiches and Going, Going, Gone in full
- [[laws-of-software-architecture]] — First Law as the driver of "it depends"; Second Law as the driver of ADRs
- [[trade-off-analysis]] — Chapter 2's general treatment; this page is Chapter 18's style-level specialisation
- [[architecture-fitness-function]] — the third deliverable of a selection
- [[fundamentals-of-software-architecture]]
