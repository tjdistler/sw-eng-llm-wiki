# Data Sovereignty

**Summary**: The state in which **each service owns its own data** and no other service accesses the underlying database directly. The "nirvana state" for a distributed architecture in Ford, Richards, and Sadalage's framing, and the outcome of Step 3 of the five-step [[database-decomposition]] pattern.

**Sources**: `raw/software-architecture-the-hard-parts/chapter-06-pulling-apart-operational-data.md`

**Last updated**: 2026-04-19

---

## The concept

> Upon completion of this step, the database is in a state of data sovereignty per service, which occurs when each service owns its own data. Data sovereignty per service is the nirvana state for a distributed architecture. (source: raw/software-architecture-the-hard-parts/chapter-06-pulling-apart-operational-data.md)

The rule: **when a service needs data from another domain, it asks that domain's service — it does not reach into the database**. No cross-schema queries, no shared synonyms, no foreign keys that span services. Data is queried through a service contract.

This is the data-tier equivalent of the [[bounded-context]] principle: inside the boundary, all the relationships and invariants. Across the boundary, only explicit contracts.

## Why it's the end state

Data sovereignty is what makes other distributed-architecture guarantees meaningful:

- **Independent deployability.** A service whose data is read by another service can't evolve its schema freely. Sovereignty removes the hidden consumers.
- **[[architectural-quantum|Architectural quantum]] separation.** A shared database collapses multiple services into one quantum. Sovereignty enables per-quantum operational characteristics (scalability, availability, security).
- **Change control.** Schema changes blast-radius is limited to the one service that owns the schema.
- **Database type freedom.** Only with sovereignty can a service move its data to the database type that fits best — [[polyglot-persistence]].

## The benefits and shortcomings

The book is explicit that sovereignty has costs, not just benefits (source: raw/software-architecture-the-hard-parts/chapter-06-pulling-apart-operational-data.md):

**Benefits:**

- Teams can change the database schema without worrying about other domains.
- Each service can use the database technology and database type best suited to its use case.

**Shortcomings:**

- **Performance issues** occur when services need access to large volumes of data from another domain — a service call replaces what used to be a database join.
- **Referential integrity** cannot be maintained by the database; bad data quality becomes possible.
- **All database code** (stored procedures, functions) that accessed tables across domains must be moved to the service layer.

These trade-offs are why data sovereignty is an aspiration, not always a requirement. A [[service-based-architecture]], for example, deliberately trades sovereignty for ACID across a shared database.

## How to get there

The five-step [[database-decomposition]] pattern in Chapter 6 ends at data sovereignty:

1. Analyze the database and create [[data-domain|data domains]].
2. Assign tables to data domains (schemas).
3. Separate database connections to data domains — **the step that achieves sovereignty**.
4. Move schemas to separate database servers.
5. Switch to independent database servers.

Step 3 is where all cross-schema access is resolved at the service level and cross-schema synonyms are removed. Steps 4 and 5 are the physical realisation; Step 3 is the logical one.

## Sovereignty ≠ isolation

A service with data sovereignty still talks to other services. Sovereignty is about **the database is only accessed by its owner** — not about the service being isolated. Cross-service communication happens via APIs, message queues, or events; it just doesn't happen through the database.

## Related pages

- [[database-decomposition]]
- [[data-domain]]
- [[bounded-context]]
- [[architectural-quantum]]
- [[shared-database-antipattern]]
- [[change-data-ownership]]
- [[polyglot-persistence]]
- [[service-based-architecture]]
- [[microservices]]
- [[software-architecture-the-hard-parts]]
