# Operational vs Analytical Data

**Summary**: Ford, Richards, Sadalage, and Dehghani's Chapter 1 split between **operational data** — the transactional data the business runs on (OLTP) — and **analytical data** — the derived, often non-relational data that feeds predictions, trends, and business intelligence. The distinction is load-bearing for architecture decisions in distributed systems because the two kinds of data impose different consistency, transactionality, and coupling constraints.

**Sources**: `raw/software-architecture-the-hard-parts/chapter-01-what-happens-when-there-are-no-best-practices.md`

**Last updated**: 2026-04-19

---

## The two kinds

### Operational data

Data used for the day-to-day operation of the business — sales, transactional data, inventory, customer records, orders. This is the data the company *runs on*: if something interrupts it, the organization stops functioning (source: chapter-01-what-happens-when-there-are-no-best-practices.md).

Operational data is the domain of **Online Transactional Processing (OLTP)** — small, frequent inserts, updates, and deletes against a database, typically relational, usually demanding ACID semantics. The authoritative state of the business lives here.

### Analytical data

Data used by data scientists and analysts for predictions, trending, and business intelligence. Not transactional, often not relational — it may be stored as a graph, a snapshot in a different shape than its transactional form, or a denormalized warehouse/lake format (source: chapter-01-what-happens-when-there-are-no-best-practices.md).

Analytical data is not critical for day-to-day operation; it supports the long-term strategic direction of the company.

## Why the distinction matters for architecture

Ford et al.'s point is that architecture choices differ sharply by which kind of data is in play:

- **Coupling and transactions** — operational data usually needs ACID transactionality and tight consistency guarantees; analytical data tolerates eventual consistency and asynchronous replication. The same service that serves both ends up serving neither well.
- **Storage shape** — relational row-oriented for OLTP; column-oriented, denormalized, or graph-shaped for analytics. Trying to satisfy both in one store forces compromises on both.
- **Availability requirements** — operational data outages stop the business; analytical outages delay insight. Different SLAs flow from that asymmetry.
- **Ownership** — operational data belongs to the service that writes it (bounded-context principle). Analytical data is copied, denormalized, and aggregated — belonging more to the data platform than to any one service.

This is a precondition for many of the book's later trade-off discussions around data ownership, transaction boundaries, and service granularity.

## Relationship to the wider data-engineering vocabulary

The Ford et al. split maps cleanly onto vocabulary established in other wiki sources:

- **OLTP vs OLAP** — the classical name for the same division (see [[data-warehousing]], [[hadoop-vs-mpp-databases]]).
- **[[data-lake]], [[data-lakehouse]], [[data-warehousing]]** — architectural homes for analytical data.
- **[[data-gravity]]** and **[[data-liberation]]** — forces that shape whether analytical data can be derived from operational data without constraining the operational system.
- **[[change-data-capture]]** — the operational-to-analytical bridge, preserving operational transaction ordering while freeing analytical consumers from direct coupling.
- **[[data-mesh]]** — Dehghani's reframing that treats analytical data as a *product* published by the teams that own the corresponding operational data.
- **[[kappa-architecture]], [[lambda-architecture]]** — stream-first approaches that unify operational and analytical processing.
- **[[monolith-vs-modular-data]]** — the modern tension in data architecture that *The Hard Parts* is implicitly speaking to.

## Relationship to microservices and bounded contexts

Microservices' adherence to [[bounded-context]] decomposition breaks up what used to be a shared relational schema. Ford et al. observe in Chapter 1 that this is why modern distributed architecture feels harder to reason about than the older distributed systems the authors built decades ago: *"back in the early days of distributed architecture, we mostly still persisted data in a single relational database."* Once data has to move to an architectural concern — along with transactionality — the operational-vs-analytical split is a major piece of the resulting complexity (source: chapter-01-what-happens-when-there-are-no-best-practices.md).

See [[database-decomposition]], [[split-the-database-first]], and [[change-data-ownership]] for the decomposition techniques that have to respect this split.

## Related pages

- [[data-architecture]]
- [[data-outlives-code]]
- [[data-warehousing]]
- [[data-lake]]
- [[data-lakehouse]]
- [[change-data-capture]]
- [[data-mesh]]
- [[data-liberation]]
- [[database-decomposition]]
- [[microservices]]
- [[bounded-context]]
- [[software-architecture-the-hard-parts]]
