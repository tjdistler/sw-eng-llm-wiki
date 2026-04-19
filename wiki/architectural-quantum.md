# Architectural Quantum

**Summary**: An independently deployable artifact with high functional cohesion and synchronous connascence. Coined by Neal Ford, Rebecca Parsons, and Patrick Kua in *Building Evolutionary Architectures* as the unit that finally gives [[architecture-characteristics|architecture characteristics]] a proper **scope**: instead of asking "how scalable is the system?", architects ask "how scalable is this quantum?" — and different quanta in the same architecture can legitimately have different -ilities.

**Sources**: `raw/fundamentals-of-software-architecture/chapter-07-scope-of-architecture-characteristics.md`, `raw/fundamentals-of-software-architecture/chapter-08-component-based-thinking.md`, `raw/software-architecture-the-hard-parts/chapter-02-discerning-coupling-in-software-architecture.md`, `raw/software-architecture-the-hard-parts/chapter-14-managing-analytical-data.md`

**Last updated**: 2026-04-19
---

## Why the unit had to be invented

Richards and Ford open Chapter 7 with a short intellectual history. A prevailing axiomatic assumption had traditionally placed the scope of architecture characteristics at the **system level** — when architects said "scalability", they meant the scalability of the *entire* system. That was safe a decade ago, when virtually all systems were monolithic. Modern engineering techniques (containers, service meshes, CI/CD) and the architecture styles they enabled (especially microservices) narrowed the scope considerably. The system-level assumption became an outdated axiom (source: chapter-07-scope-of-architecture-characteristics.md).

The authors hit the concrete need while writing *Building Evolutionary Architectures*: they wanted a measure for the structural evolvability of particular architecture styles and found that none of the existing measures were at the right level of detail. Code-level metrics like [[coupling-metrics|afferent and efferent coupling]] and [[cyclomatic-complexity]] reveal low-level details about the code but *cannot evaluate dependent components outside the code base* — databases, message brokers, caches — that still impact many architecture characteristics, especially operational ones. Their example: no matter how performant or elastic the code is, if the database doesn't match those characteristics, the application won't be successful (source: chapter-07-scope-of-architecture-characteristics.md).

So the authors needed a new unit — one that included *everything the system needs to function*, not just the code. That unit is the architecture quantum.

## Definition

> **Architecture quantum**: an independently deployable artifact with high functional cohesion and synchronous connascence. (source: chapter-07-scope-of-architecture-characteristics.md)

The word is from Latin *quantum* — "how great" or "how much" — via the physics sense of "the minimum amount of any physical entity involved in an interaction." An architecture quantum is the minimum unit at which characteristics can be meaningfully scoped.

The definition has three parts, and all three must hold.

### 1. Independently deployable

An architecture quantum includes *all the necessary components to function independently* from other parts of the architecture. If the application uses a database, that database is part of the quantum — the system won't function without it (source: chapter-07-scope-of-architecture-characteristics.md).

This requirement has an immediate consequence: **virtually all legacy systems deployed using a single shared database by definition form a quantum of one**. It doesn't matter how many services front the database — if they all share it, the database ties them into a single deployable unit, and the whole system is one quantum.

In the microservices style, each service includes its own database (the [[bounded-context]] driving philosophy — see Chapter 17 of the book), creating multiple quanta within that architecture.

See [[independent-deployability]] for the operational discipline this part of the definition rests on.

### 2. High functional cohesion

[[cohesion|Cohesion]] in component design refers to how unified in purpose the contained code is. A `Customer` component with properties and methods all pertaining to a Customer entity exhibits high cohesion; a `Utility` component with a random collection of miscellaneous methods does not. High *functional* cohesion means an architecture quantum does something **purposeful** — one business-meaningful thing, not a technical layer (source: chapter-07-scope-of-architecture-characteristics.md).

This distinction matters little in traditional monolithic applications with a single database — everything is lumped into one quantum regardless. But in microservices architectures, developers typically design each service to match a single workflow (a [[bounded-context]]), thus exhibiting high functional cohesion by construction.

### 3. Synchronous connascence

This is the most architecturally important part of the definition and the part that revises Page-Jones's 1996 [[connascence]] framework for distributed systems.

> Synchronous connascence implies synchronous calls within an application context or between distributed services that form this architecture quantum. (source: chapter-07-scope-of-architecture-characteristics.md)

The key insight: **synchronous calls create dynamic connascence for the length of the call** — if one service is waiting for another, their operational architecture characteristics must be the same for the duration of the call. If the caller is much more scalable than the callee, timeouts and reliability problems will occur. Two services locked in a synchronous call cannot, in practice, have different scalability or availability profiles — they act as one quantum whether the architect intended it or not.

This is the piece that Chapter 3 explicitly promised and deferred: the original connascence taxonomy (name, type, meaning, position, algorithm; execution, timing, values, identity) didn't address synchronous-vs-asynchronous in the distributed-services sense. Chapter 7 adds **communication connascence** — synchronous and asynchronous — as a new axis and extends the unified coupling-and-connascence diagram with it.

The worked example: a microservices architecture with a Payment service and an Auction service. When an auction ends, the Auction service sends payment information to the Payment service. Suppose the Payment service can only handle one payment per 500 ms — what happens when a large number of auctions end at once?

- **Synchronous design**: the first call goes through and the rest time out. The Auction and Payment services are in the same quantum for the length of each call and must share operational characteristics they cannot realistically share.
- **Asynchronous design**: a message queue buffers differences between the services. Asynchronous connascence creates a more flexible architecture and lets each service have its own operational characteristics. (Covered in detail in Chapter 14 on event-driven architecture.) (source: chapter-07-scope-of-architecture-characteristics.md)

## The payoff: architecture characteristics are now *scoped*

The headline consequence is that architecture characteristics are no longer system-level:

> The architecture quantum concept provides the new scope for architecture characteristics. In modern systems, architects define architecture characteristics at the quantum level rather than system level. (source: chapter-07-scope-of-architecture-characteristics.md)

By looking at a narrower scope for important operational concerns, architects may identify architectural challenges early, leading to **hybrid architectures** — systems where different quanta deliberately use different styles to serve different characteristics.

### Monolith = 1 quantum; microservices = many

A monolith with a single shared database is a quantum of one. Every characteristic applies to the whole thing at once; trade-offs are whole-system trade-offs.

A microservices architecture with per-service databases is many quanta. Each quantum can have its own scalability profile, its own availability SLA, its own security posture. The Payment quantum can be high-security, low-throughput; the Catalog quantum can be high-performance, eventually consistent; the Notification quantum can be fire-and-forget asynchronous.

This is why the microservices style enables what Richards and Ford call the hybrid-architecture design mindset: once you accept that characteristics are scoped to quanta, you stop trying to pick one architecture for the whole system and start picking the right architecture per quantum.

## Going, Going, Gone — the worked kata

Chapter 7 closes with an architecture kata, *Going, Going, Gone*, that makes the scope point concrete (source: chapter-07-scope-of-architecture-characteristics.md). An online auction company wants nationwide-scale real-time auctions with live video. Requirements include scalability to thousands of simultaneous participants, real-time bid ordering, credit-card payments, a reputation index, and live streaming.

The kata illustrates the futility of treating architecture characteristics as a system-wide evaluation. Consider **availability** alone: is it uniform throughout the architecture? The availability of the auctioneer is more critical than the availability of any one bidder — if the auctioneer cannot access the site, *nobody* can bid. Treating availability as a single system-level requirement papers over this.

Using the quantum measure, the architect identifies three quanta with different characteristics:

| Quantum | Scope | Characteristics |
|---|---|---|
| **Bidder feedback** | Bid stream and video stream of bids | Availability, scalability, performance |
| **Auctioneer** | The live auctioneer | Availability, reliability, scalability, elasticity, performance, security |
| **Bidder** | Online bidders and bidding | Reliability, availability, scalability, elasticity |

The auctioneer quantum needs *reliability* and *security* (credit-card tie-ins, past fraud lawsuit) that the bidder-feedback quantum doesn't need; the bidder-feedback quantum needs streaming performance that the auctioneer quantum is less concerned with. A single architecture style optimising for all of these simultaneously would be wasteful in some dimensions and inadequate in others. Scoping per quantum lets the architect pick the right style for each — a hybrid architecture emerging from the analysis rather than being imposed.

## Relationship to bounded context

The architecture quantum concept inherits from DDD's [[bounded-context]] but is not identical to it. A bounded context is a *logical* boundary — everything related to a domain is visible internally and opaque externally — and recognises that each entity works best inside a localised context rather than as a holistically-reused shared artifact. The architecture quantum is a *physical* boundary: the deployable unit that includes the code, the data, and any dependent infrastructure needed to run.

In a well-designed microservices architecture the two align: one bounded context, one quantum, one service + database. This alignment is not automatic — a bounded context that depends synchronously on a shared database in another context isn't a quantum of its own. The quantum test is sharper: *can this thing actually run on its own, without requiring another deployable's up-time for its own correctness?*

See [[bounded-context]] for the DDD-side treatment (Evans), and [[microservices]] for how the alignment shows up in the Newman-framed microservice definition.

## What this does to coupling analysis

Chapter 3's [[connascence]] page closed with a "Limits of the 1996 framework" section that explicitly flagged two problems:

1. Page-Jones's framework operates at code-quality level, not architectural-structure level.
2. It predates microservices and doesn't address synchronous-vs-asynchronous as a distributed-architecture question.

The architectural quantum addresses both at once. The *quantum boundary* is the architectural-structure unit Chapter 3 was missing — connascence analysis inside a quantum is fine, connascence that crosses quantum boundaries needs a second look. And synchronous communication connascence is now an explicit axis of the framework, sitting above the original 1996 static and dynamic types in the unified diagram (Figure 7-1 in the book).

In practice: architects should minimise connascence across quantum boundaries, prefer asynchronous connascence where cross-quantum communication is needed, and reserve synchronous cross-quantum calls for cases where the operational characteristics genuinely align.

## The Hard Parts refinement: static + dynamic coupling

*Software Architecture: The Hard Parts* Chapter 2 updates the definition with a more precise vocabulary (source: raw/software-architecture-the-hard-parts/chapter-02-discerning-coupling-in-software-architecture.md):

> An architecture quantum is an independently deployable artifact with high functional cohesion, **high static coupling**, and **synchronous dynamic coupling**.

The three parts of the original *Fundamentals* definition remain (independent deployability, high functional cohesion, synchronous connascence), but the third is now decomposed into the two orthogonal axes the later book makes load-bearing:

- **[[static-coupling|High static coupling]]** — the dependencies required to *bootstrap and run* the quantum: OS, frameworks, libraries, databases, message brokers, URLs, contracts. *How services are wired together.*
- **Synchronous [[dynamic-coupling]]** — the runtime communication characteristic that, when present across services, fuses them into one quantum. *How services call one another at runtime.*

The reframe makes explicit something Chapter 7 of *Fundamentals* only hinted at: the quantum's envelope is defined by *two* kinds of coupling, not one, and they answer different questions. Static coupling asks "what must be running for this thing to function at all?" Dynamic coupling asks "what runtime calls fuse this thing's operational characteristics with another thing's?"

### Worked topology enumeration

Chapter 2 walks the architecture styles from *Fundamentals* and shows how the static-coupling measure assigns a quantum count to each (source: raw/software-architecture-the-hard-parts/chapter-02-discerning-coupling-in-software-architecture.md):

| Architecture | Quanta | Why |
|---|---|---|
| Monolith (any style) | 1 | Single deployment unit; single DB |
| [[service-based-architecture]] | 1 | Separate services but one shared relational DB |
| Mediated [[event-driven-architecture]] | 1 | DB + request orchestrator both couple everything |
| Broker EDA with one DB | 1 | Shared DB collapses the quantum even with async messaging |
| Broker EDA with separate data stores, no shared static deps | Many | Each subsystem can bootstrap independently |
| [[microservices]] with per-service DBs, decoupled UI | Many | Full independence — the archetype |
| Microservices coupled through a monolithic UI | 1 | UI is a static coupling point across the backend |
| Micro-frontend + microservices | Many | Each service + UI fragment forms its own quantum |
| Two systems sharing a DB | 1 | Shared DB is a coupling point even across system boundaries |

The **bootstrap test** is the sharp question: *Is this dependency necessary to bootstrap this service?* If yes, it's inside the quantum's static coupling envelope. Even in a broker EDA where some services don't directly touch the DB, if they rely on services that do, the transitive static coupling pulls them into the same quantum.

### A quantum diagram is a static-coupling diagram

Chapter 2 names an emerging architect technique: draw a **static quantum diagram** of a legacy system — the operational substrate wired to the services wired to the UIs — to make change-blast-radius visible (source: raw/software-architecture-the-hard-parts/chapter-02-discerning-coupling-in-software-architecture.md). The diagram is the legacy-archaeology tool; the quantum count is its headline output.

### Synchronous dynamic coupling = fused quanta

The Chapter 7 *Fundamentals* insight — that synchronous calls fuse operational characteristics for the length of the call — survives intact and is renamed: this is synchronous dynamic coupling. The Chapter 2 crispening: quanta are meant to be *independent*; synchronous dynamic coupling across a quantum boundary silently re-fuses them. Architects who want separate quanta must keep inter-quantum communication asynchronous (or accept that the "two" quanta are effectively one whenever the sync calls are in flight). See [[dynamic-coupling]] for the three dimensions (communication × consistency × coordination) this opens up.

## Granularity is the architect's per-quantum sizing decision

Chapter 7 of *The Hard Parts* makes the connection between [[architectural-modularity|modularity]], granularity, and quantum count explicit (source: raw/software-architecture-the-hard-parts/chapter-07-service-granularity.md). Modularity choices set *how many quanta* the architecture has; granularity choices set *how big each quantum is*. The [[granularity-disintegrators]] and [[granularity-integrators]] frameworks decide both — every disintegrator-justified split adds a quantum, every integrator-justified consolidation removes one.

This means the quantum count is not chosen directly. It emerges from per-service trade-off analyses: split when disintegrators outweigh integrators, consolidate when integrators outweigh disintegrators. The static-coupling diagram (above) is the visualisation; the [[service-granularity|granularity analysis]] is the decision procedure that produces it.

The corollary the Ch 7 framing makes sharp: **a quantum that's too small is one whose creation was justified by disintegrators while ignoring the integrators.** Those integrators don't disappear — they reappear as ACID-transaction-becomes-saga, as inter-service chatter, as shared-library lockstep deployments, as data round-trips. The quantum count grew but the *real* operational quantum count didn't, because the new quanta are still fused by integrator forces the architect didn't pay attention to.

## The Hard Parts Ch 14 extension: the data product quantum

Chapter 14 of *Hard Parts* extends the quantum concept to analytical data by introducing the [[data-product-quantum]] (DPQ) — the unit of a [[data-mesh]] (source: raw/software-architecture-the-hard-parts/chapter-14-managing-analytical-data.md). The DPQ is a quantum in its own right — independently deployable, functionally cohesive (serving a domain's analytical data), with its own coupling envelope. Architecturally, it sits next to a domain microservice quantum as a **cooperative quantum**:

> An operationally separate quantum that communicates with its cooperator via asynchronous communication and eventual consistency, yet features tight contract coupling with its cooperator and generally looser contract coupling to the analytics quantum.

The DPQ is the data-side analogue of the [[sidecar-pattern]] in a [[service-mesh]]: it handles analytical data as an [[orthogonal-coupling|orthogonal concern]] to the operational domain, without entangling the domain service's implementation. From a static-coupling view, the DPQ is part of the domain quantum's static-coupling envelope — the architecture requires it the same way it requires a message broker. From a dynamic-coupling view, the DPQ must communicate with its cooperator asynchronously and under eventual consistency ([[parallel-saga]] or [[anthology-saga]]) — a transactional requirement across the boundary would defeat the point of the separation.

Ch 14 also catalogues three DPQ types — **source-aligned (native)**, **aggregate**, and **fit-for-purpose** — each a quantum with its own role in the analytical plane. See [[data-product-quantum]] for the full treatment.

## Uses of the quantum measure

Richards and Ford summarise the uses of the architecture-quantum concept (source: chapter-07-scope-of-architecture-characteristics.md):

- **Deployment unit** — what's the minimum thing you can ship on its own.
- **Coupling analysis** — where does the synchronous connascence reach.
- **Data residency** — which quantum owns which data; avoid shared-database quanta-collapsing.
- **Communication styles** — synchronous inside a quantum, asynchronous between them.
- **Architecture-characteristic scope** — different quanta can have different -ilities.

All five uses trace back to the same insight: the quantum is the unit at which architectural decisions actually bind, and treating the system as monolithic when it isn't (or as many quanta when it's really one) produces bad trade-offs.

## Where the quantum decision lives in the design process

Chapter 8 closes with an explicit hand-off: the monolith-vs-distributed decision is taken *at the end of* the [[component-identification-cycle|component identification cycle]], not the start (source: chapter-08-component-based-thinking.md). Once [[components]] have been identified and their [[architecture-characteristics|characteristics]] have been analysed per component (step 4 of the cycle), the architect can count quanta: one characteristic profile across all components → a monolith is viable; systematically different profiles → a distributed architecture to accommodate the differences.

The *Going, Going, Gone* split of `BidCapture` into `BidCapture` + `AuctioneerCapture` is the worked example. Functionally, capturing bids is capturing bids. Characteristic-wise, the auctioneer's reliability and availability needs exceed any individual bidder's. That divergence is exactly what forces the split into separate quanta, and separate quanta are exactly what forces distributed architecture.

## Related pages

- [[architecture-characteristics]]
- [[connascence]]
- [[bounded-context]]
- [[independent-deployability]]
- [[cohesion]]
- [[coupling]]
- [[microservices]]
- [[monolith]]
- [[evolutionary-architecture]]
- [[components]]
- [[component-identification-cycle]]
- [[technical-vs-domain-partitioning]]
- [[static-coupling]]
- [[dynamic-coupling]]
- [[software-architecture-the-hard-parts]]
- [[fundamentals-of-software-architecture]]
- [[service-granularity]]
- [[granularity-disintegrators]]
- [[granularity-integrators]]
- [[architectural-modularity]]
- [[data-product-quantum]]
- [[data-mesh]]
