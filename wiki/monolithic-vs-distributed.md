# Monolithic vs Distributed

**Summary**: The classification scheme Richards and Ford use to separate the eight architecture styles in Part II of *Fundamentals of Software Architecture*. A **monolithic** architecture deploys all code as a single unit; a **distributed** architecture consists of multiple deployment units connected through remote access protocols. The classification matters because all distributed styles share a common cost structure — the [[fallacies-of-distributed-computing|eight fallacies]] plus several named "other considerations" — that monolithic styles avoid by construction.

**Sources**: `raw/fundamentals-of-software-architecture/chapter-09-foundations.md`

**Last updated**: 2026-04-16

---

## The two classes

Richards and Ford classify every architecture style into one of two buckets (source: chapter-09-foundations.md):

| Monolithic (single deployment unit) | Distributed (multiple deployment units) |
|---|---|
| Layered architecture (Ch 10) | Service-based architecture (Ch 13) |
| Pipeline architecture (Ch 11) | Event-driven architecture (Ch 14) |
| Microkernel architecture (Ch 12) | Space-based architecture (Ch 15) |
| | Service-oriented architecture (Ch 16) |
| | [[microservices|Microservices architecture]] (Ch 17) |

The bucketing is deliberately at the architectural-quantum scale, not at "is there a network between the app and the database?" — in practice every non-trivial system is at least partially distributed. The distinction is whether the *architecture itself* is distributed: whether the units that make up the business-request path are separately deployable and communicate over remote protocols.

A monolith in this scheme is exactly what it is on [[monolith]]: one independently deployable artifact, one [[architectural-quantum|quantum]], one set of architecture characteristics. A distributed architecture is many quanta, many deployables, and many sets of characteristics.

## Why it's the useful top-level split

Richards and Ford give one blunt reason: *distributed architectures all share a common set of challenges and issues not found in the monolithic architecture styles, making this classification scheme a good separation between the various architecture styles* (source: chapter-09-foundations.md).

That is: the cost of distribution is so large and so coherent that any conversation about architecture style has to deal with the distribution axis *first*, before any style-specific trade-off can be weighed. The other axes (technical vs domain partitioning from Chapter 8, characteristic profiles from Chapter 4) sit underneath.

## What distribution buys

- **Performance at scale** — each quantum can be scaled independently.
- **Scalability** — horizontal scaling of the services whose load actually grew, not the whole system.
- **Availability** — fault isolation; a failure in one quantum doesn't automatically become a failure of the system.

Kleppmann's framing on [[scalability]] and [[fault-tolerance]] is the same argument from the data-systems side.

## What distribution costs

### The eight fallacies

The primary cost is the [[fallacies-of-distributed-computing|eight fallacies of distributed computing]] — network reliability, latency, bandwidth, security, topology stability, single-administrator, transport cost, and homogeneity. Every distributed style pays all eight; no monolithic style pays any of them (source: chapter-09-foundations.md).

The fallacies alone are enough to make "go distributed" a significant design commitment rather than a free upgrade.

### Distributed logging

Root-cause analysis in a monolith looks at one log. In a distributed architecture it looks at dozens to hundreds of logs in different places and different formats (source: chapter-09-foundations.md). Tools like Splunk help consolidate, but Richards and Ford call out that consolidation *scratches the surface*. The wiki's [[log-aggregation]] page captures Newman's parallel argument ("do this first" when adopting microservices).

### Distributed transactions

A monolith gets [[acid|ACID]] for free via its persistence framework. A distributed architecture gives that up and substitutes [[eventual-consistency|eventual consistency]], [[saga|sagas]] (event-sourced compensation or finite-state-machine orchestration), and **BASE transactions** — (B)asic availability, (S)oft state, (E)ventual consistency — which are a *technique*, not a framework (source: chapter-09-foundations.md). Soft state refers to in-flight data between source and target, and inter-source inconsistency, which eventually converges through architecture patterns and messaging.

This is the same trade-off Kleppmann documents across DDIA chapters 7–9 and that Newman decomposes in the database chapter of *Monolith to Microservices*. Full treatment: [[distributed-transactions]], [[saga]], [[eventual-consistency]].

### Contract maintenance and versioning

Decoupled services owned by different teams and departments make contract creation, maintenance, and versioning difficult. The communication required to coordinate version deprecation across teams is particularly hard (source: chapter-09-foundations.md).

The wiki has multiple prior treatments of this problem:

- [[schema-evolution]] — Kleppmann's field-tag and writer/reader-schema mechanisms
- [[backward-forward-compatibility]] — why both directions are required for rolling upgrades
- [[consumer-driven-contracts]] — Pact-style contracts as the microservices-era answer
- [[breaking-changes]] — Newman's structural-vs-semantic taxonomy and the three rules

Richards and Ford's contribution here is to name the *organizational* version of the problem: the cross-team deprecation communication is often harder than the technical contract mechanics.

### Distributed data access, performance, and the rest

Chapter 9 lists several other categories (distributed data access, distributed performance, distributed monitoring) as out-of-scope-but-named. The full treatment is in the wiki's distributed-systems pages sourced from DDIA and *Monolith to Microservices*: [[partial-failures]], [[unreliable-networks]], [[monitoring-and-observability]], [[distributed-tracing]], [[correlation-ids]].

## Relationship to partitioning

Distribution is orthogonal to [[technical-vs-domain-partitioning|technical vs domain partitioning]]. In practice:

- Monolithic + technical partitioning = layered monolith (Ch 10)
- Monolithic + domain partitioning = [[modular-monolith]] (Richards and Ford don't name this as one of the eight styles, but Chapter 8 establishes it)
- Distributed + technical partitioning = service-based or SOA (Ch 13, Ch 16)
- Distributed + domain partitioning = [[microservices]] (Ch 17), event-driven (Ch 14)

The Chapter 8 industry-drift argument — *toward* domain partitioning — applies on both sides of the distribution axis.

## Relationship to the architectural quantum

A monolithic style is a [[architectural-quantum|single quantum]]; a distributed style is multiple quanta. That's the Chapter 7 restatement of the same classification. The quantum view adds nuance around the **distributed monolith** anti-pattern: multiple deployables that are synchronously and deeply coupled are *operationally* one quantum even though they're packaged as several — paying the full distribution tax without gaining per-quantum characteristic scoping. See [[monolith]] for the distributed-monolith entry.

## The honest default

Richards and Ford don't explicitly prescribe "start monolithic, go distributed when you need to" in Chapter 9, but the structural argument they set up — distribution pays for *every* fallacy and inherits *every* named "other consideration" — lines up with Newman's [[incremental-migration]] advice, with the [[why-microservices]] three-question test, and with the Chapter 8 observation that domain-partitioned monoliths are a legitimate and often cheaper alternative to microservices. The Part II style chapters (10–17) are where each specific style's star-rating against characteristics makes the trade-off concrete.

## Related pages

- [[fallacies-of-distributed-computing]]
- [[monolith]]
- [[microservices]]
- [[modular-monolith]]
- [[architectural-quantum]]
- [[technical-vs-domain-partitioning]]
- [[distributed-transactions]]
- [[saga]]
- [[eventual-consistency]]
- [[schema-evolution]]
- [[consumer-driven-contracts]]
- [[breaking-changes]]
- [[log-aggregation]]
- [[partial-failures]]
- [[why-microservices]]
- [[fundamentals-of-software-architecture]]
