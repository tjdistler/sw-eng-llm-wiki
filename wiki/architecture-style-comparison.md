# Architecture Style Comparison

**Summary**: Cross-cutting comparison of the eight Part II architecture styles from Richards and Ford's *Fundamentals of Software Architecture* on their standard set of characteristics (partitioning, quantum count, and the ten-or-so -ilities that each style chapter closes with). This is the hub the [[choosing-architecture-style|style-selection process]] draws on — the same information distributed across the eight style pages, consolidated in one place.

**Sources**: `raw/fundamentals-of-software-architecture/chapter-10-layered-architecture-style.md`, `raw/fundamentals-of-software-architecture/chapter-11-pipeline-architecture-style.md`, `raw/fundamentals-of-software-architecture/chapter-12-microkernel-architecture-style.md`, `raw/fundamentals-of-software-architecture/chapter-13-service-based-architecture-style.md`, `raw/fundamentals-of-software-architecture/chapter-14-event-driven-architecture-style.md`, `raw/fundamentals-of-software-architecture/chapter-15-space-based-architecture-style.md`, `raw/fundamentals-of-software-architecture/chapter-16-orchestration-driven-service-oriented-architecture.md`, `raw/fundamentals-of-software-architecture/chapter-17-microservices-architecture.md`, `raw/fundamentals-of-software-architecture/chapter-18-choosing-the-appropriate-architecture-style.md`

**Last updated**: 2026-04-16

---

## How to read the scorecard

Each Part II style chapter closes with a **star rating** (one to five) along a standard characteristic set. One star = poorly supported (or actively costly); five stars = one of the style's strongest features. Ratings are *relative across styles*, not absolute targets — every style has a shape, and the shape is what the architect picks.

Two caveats Richards and Ford repeat across chapters:

- Scorecards assume a **reasonably-sized** application. Ratings degrade as any style gets bigger — most visibly for [[layered-architecture]] and [[orchestration-driven-soa]] (source: chapters 10, 16).
- Scorecards are for *pure* style instances. Many real systems are **hybrids** (event-driven microservices, event-driven space-based, event-driven microkernel). Hybrid shapes inherit ratings from both sides of the mix (source: chapter-14-event-driven-architecture-style.md).

## Structural shape

| Style | Partitioning | Typical quantum count | Class |
|---|---|---|---|
| [[layered-architecture\|Layered]] | Technical | 1 | [[monolithic-vs-distributed\|Monolithic]] |
| [[pipeline-architecture\|Pipeline]] | Technical (by filter role) | 1 | Monolithic |
| [[microkernel-architecture\|Microkernel]] | **Both** (core = technical; plug-ins = domain) | 1 | Monolithic |
| [[service-based-architecture\|Service-based]] | Domain | 1 to a few (typ. 1, up to several with UI/DB federation) | Distributed |
| [[event-driven-architecture\|Event-driven]] | Technical (event-partitioned) | 1 to many | Distributed |
| [[space-based-architecture\|Space-based]] | Both | Driven by UI-to-processing-unit associations and sync PU coupling | Distributed |
| [[orchestration-driven-soa\|Orchestration-driven SOA]] | Technical (enterprise-wide taxonomy) | **1** (despite being distributed) | Distributed |
| [[microservices\|Microservices]] | Domain (service = [[bounded-context]]) | Many | Distributed |

**Structural observations**:

- Microkernel is the only style that is **simultaneously technically and domain partitioned** — its core is technical, its plug-ins are domain.
- SOA is the only distributed style with a **quantum count of one** — the shared DB and the orchestration engine / ESB both act as giant coupling points that collapse the architecture to a single characteristic scope.
- Microservices is the only style that is *inherently* many-quantum. Service-based and event-driven can be one or several; microservices is the style where each service *is* a quantum by design.

## Full scorecard

The ten-to-twelve characteristics Richards and Ford track vary slightly across chapters. The table below includes every characteristic that appears on at least one of the eight scorecards. Blank cells mean the chapter did not list that characteristic explicitly (not that it is zero); fill from the adjacent style's profile when inferring.

| Characteristic | Layered | Pipeline | Microkernel | Service-based | Event-driven | Space-based | SOA | Microservices |
|---|---|---|---|---|---|---|---|---|
| **Overall cost** | ★★★★★ | ★★★★★ | ★★★★★ | ★★★ | ★★ | ★ | ★ (inverted; high cost) | ★ |
| **Simplicity** | ★★★★★ | ★★★★★ | ★★★★★ | ★★★ | ★★ | ★ | ★ | ★ |
| **Modularity** | ★ | (strong) | ★★★ | ★★★★ | ★★★ | — | ★★ | (implied high) |
| **Deployability** | ★★ | ★★★ | ★★★ | ★★★★ | ★★★★ | — | ★ | ★★★★★ |
| **Testability** | ★★ | ★★★ | ★★★ | ★★★★ | ★★ | ★ | ★ | ★★★★★ |
| **Performance** | ★★ | — | ★★★ | ★★★ | ★★★★★ | ★★★★★ | ★ | ★★ |
| **Scalability** | ★ | ★ | ★ | ★★★ | ★★★★★ | ★★★★★ | ★★★ | ★★★★★ |
| **Elasticity** | ★ | ★ | ★ | ★★ | ★★★★★ | ★★★★★ | ★★★ | ★★★★★ |
| **Fault tolerance** | ★ | ★ | ★ | ★★★★ | ★★★★★ | — | ★★★ | ★★★★ |
| **Availability** | ★★ | ★★ | ★★ | ★★★★ | ★★★★ | — | ★★★ | (high; via redundancy) |
| **Reliability** | ★★★ | ★★★ | ★★★ | ★★★★ | — | — | ★★ | ★★★★ |
| **Extensibility** | — | — | ★★★ | — | — | — | — | — |
| **Evolvability / evolutionary** | — | — | — | — | ★★★★★ | (tricky) | ★★ | ★★★★★ |
| **Agility** | — | — | — | ★★★★ | — | — | — | ★★★★★ |
| **Abstraction** | — | — | — | — | — | — | ★★★★★ | — |

(Each cell is cited from the scorecard table on the corresponding style page; see the *Sources* line above for the specific chapter.)

## Reading the shapes

Four distinct **scorecard shapes** emerge from the table, and choosing a style is largely choosing a shape.

### Shape 1 — "Cheap and simple, low ceiling"

Layered, pipeline, microkernel. Five stars on cost and simplicity; one-to-three stars on every operational characteristic (scalability, elasticity, fault tolerance). One quantum; ratings degrade as the app grows. These are the styles to start with when the scale requirements are modest, the team is small, or the architectural analysis isn't complete yet.

Pipeline edges out layered on modularity / deployability / testability (filter-level granularity beats layer-level). Microkernel edges out both on extensibility (plug-ins *are* the unit of extension) and is the only one with a domain-axis partitioning available. But all three share the monolithic ceiling.

### Shape 2 — "Pragmatic middle"

Service-based. No five-star ratings, but seven four-star ratings (agility, testability, deployability, fault tolerance, availability, reliability, modularity) and three-star on simplicity / cost / scalability / performance. The rhetorical framing from Chapter 13 is that this is *enough* for most business applications — and going further (microservices, event-driven, space-based) is a Ferrari in rush-hour traffic. [[acid|ACID]] transactions still work because the coarse-grained services share one DB; that is the property the distributed styles to the right give up.

### Shape 3 — "Five-star operational, costly"

Event-driven, space-based, microservices. Five stars on scalability / elasticity and (for event-driven and space-based) performance. One star on simplicity and cost. These are the styles to reach for when operational characteristics are non-negotiable — auction bursts, concert-ticket drops, independent global scale — and where the organisation has the engineering / DevOps maturity to absorb the operational complexity.

Within this shape:

- **Event-driven** is the async-first, decoupled-processor shape. Five stars on fault tolerance and evolutionary; four on deployability and availability. Two stars on testability (nondeterminism is hard to test exhaustively).
- **Space-based** is specifically the *extreme-variable-concurrent-load* shape — ticketing, auctions, booking. Five on elasticity/scalability/performance; one on simplicity/testability/cost. The database is off the synchronous path, replaced by an in-memory replicated data grid; persistence is eventually consistent by construction.
- **Microservices** is the domain-partitioned, many-quantum, operationally-reused-via-[[sidecar-pattern|sidecars]] shape. Five on scalability/elasticity/evolutionary/agility/testability/deployability. Two stars on performance (network + security checks). One on simplicity and cost. The inverse shape of layered.

### Shape 4 — "Historical cautionary tale"

SOA is the odd one out. One star on deployability, testability, performance, simplicity, cost. Five stars only on abstraction — the taxonomy *does* produce strong abstraction, which is what the style was sold on — and three-star on elasticity, scalability, and availability, but those were vendor-driven (session replication across app servers, enterprise-grade middleware). *The SOA scorecard is the inverse of the modern ideal*: high on the characteristics large enterprises cared about in the 2000s, low on everything engineering teams care about today.

Single quantum despite being distributed is the structural reason for the scorecard shape — the shared DB and the orchestration engine both act as giant coupling points. Every microservices discipline (domain partitioning, independent deployability, database-per-service, sagas over distributed transactions, choreography over orchestration, many quanta) is the direct negation of a specific SOA failure mode. See [[orchestration-driven-soa]] for the full treatment.

## Cross-characteristic observations

- **Cost and simplicity move together** — every style above three stars on cost also has three-or-more stars on simplicity, and vice versa. There is no "cheap and complex" or "expensive and simple" shape.
- **Elasticity and scalability move together** — they are driven by the same structural property (independent deployability of the unit of concurrency). No style in the table scores materially differently on the two.
- **Fault tolerance lags scalability in the distributed styles** — event-driven hits five on both; microservices hits five on scalability but four on fault tolerance (excessive inter-service communication can degrade it); service-based hits four on fault tolerance but three on scalability (coarse services don't scale as finely). Fault tolerance requires *deliberate* design (circuit breakers, bulkheads, redundancy) on top of the basic shape.
- **Testability tracks deployability** in every style except event-driven — which drops to two stars on testability because of the nondeterminism of async event flows despite four stars on deployability.
- **Performance is the microservices weak point** — not scalability. Microservices scales beautifully (five stars) but per-request performance suffers from network hops, per-endpoint auth, and fan-out latency (two stars).

## What the comparison does not capture

The scorecard is a navigational aid, not a decision. Three inputs that matter for style selection are *not* on the table:

- **Domain-to-architecture isomorphism.** Microkernel fits per-jurisdiction / per-form / per-device domains; space-based fits genome-analysis / bursty-concurrent-load domains; microservices fits highly decoupled domains with clear bounded contexts. These fits do not show up as scorecard stars — a two-star scalability rating on microkernel is irrelevant if the domain does not need scalability, and a five-star rating on microservices is irrelevant if the domain is genuinely coupled.
- **Team, process, and operational maturity.** The distributed styles all assume Agile engineering, CI/CD, observability, and DevOps competence. Scoring a style against an organisation that does not have those is misleading — the five stars on deployability for microservices becomes zero-stars-in-practice without the surrounding discipline.
- **Data architecture.** Which quanta own what data, how cross-quantum workflows happen, how existing data architecture constrains the new system — none of this is in the scorecard. The [[database-decomposition|database decomposition]] work is orthogonal to style selection and has to happen alongside it.

This is why [[choosing-architecture-style|Chapter 18's selection process]] has six inputs and three decisions before the style question becomes answerable.

## Related pages

- [[choosing-architecture-style]] — the Chapter 18 decision process this hub supports
- [[monolithic-vs-distributed]] — the top-level classification (Class column above)
- [[technical-vs-domain-partitioning]] — the Partitioning column above
- [[architectural-quantum]] — the Quantum-count column above
- [[architecture-characteristics]] — what the -ilities are as a dimension
- [[layered-architecture]]
- [[pipeline-architecture]]
- [[microkernel-architecture]]
- [[service-based-architecture]]
- [[event-driven-architecture]]
- [[space-based-architecture]]
- [[orchestration-driven-soa]]
- [[microservices]]
- [[fundamentals-of-software-architecture]]
