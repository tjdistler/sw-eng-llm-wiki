# Distributed Data Access

**Summary**: Chapter 10 of *Software Architecture: The Hard Parts* catalogues the four patterns a service can use to **read data it does not own**. [[data-ownership]] (Ch 9) solved the write side; once a table has one owner, every other service that needs to read from it has a distributed-data-access problem. The four patterns: [[interservice-communication-pattern]], [[column-schema-replication-pattern]], [[replicated-caching-pattern]], and [[data-domain-pattern]]. Each trades service coupling, response time, data currency, fault tolerance, volume, and complexity differently.

**Sources**: `raw/software-architecture-the-hard-parts/chapter-10-distributed-data-access.md`

**Last updated**: 2026-04-19

---

## Why this is a problem

In a monolith with a single database, reading data is free: SQL joins pull whatever the query needs in one call. Once data is split across service-owned schemas (see [[database-decomposition]], [[data-domain]], [[data-sovereignty]]), the query can no longer cross the boundary. The reading service now has to **pick an access pattern** — and each pattern has different failure modes (source: raw/software-architecture-the-hard-parts/chapter-10-distributed-data-access.md).

The chapter's worked example (from Ch 9): a `Wishlist Service` needs to display items a customer has saved. The wishlist table stores `customer_id`, `item_id`, and date-added; the **item description** lives in the Catalog Service's product table. The Wishlist Service has to get those descriptions somehow without owning the product table.

## The four patterns

| Pattern | One-liner | Data lives where? |
|---|---|---|
| [[interservice-communication-pattern]] | Call the owning service over the network on every request | Only in the owner's DB |
| [[column-schema-replication-pattern]] | Copy the needed columns into the reader's own table | In both DBs; sync'd async |
| [[replicated-caching-pattern]] | In-memory cache replicated into each reader; owner writes, readers read | In RAM in every service |
| [[data-domain-pattern]] | Put the shared tables into a jointly-owned schema both services read | In a shared schema |

All four solve the Wishlist/Catalog problem. Which to pick is a trade-off analysis, not a best-practice choice (source: raw/software-architecture-the-hard-parts/chapter-10-distributed-data-access.md).

## Trade-off matrix

The chapter compiles Tables 10-1 through 10-4 into an implicit head-to-head. Ratings below use the book's language (good / fair / poor):

| Dimension | Interservice comm | Column schema replication | Replicated cache | Data domain |
|---|---|---|---|---|
| Service dependency | **High** (static + semantic coupling) | Medium (async sync) | Medium (startup only) | **None** |
| Response time | **Poor** (network + security + data latency; up to ~1s) | **Excellent** (local SQL join) | **Excellent** (in-memory) | **Excellent** (local SQL join) |
| Data volume | Any | Any | **Poor** above ~500 MB per cache × instances | Any |
| Data currency | **Excellent** (always fresh) | Stale (sync lag) | Stale (sync lag; poor for volatile data) | **Excellent** (one table, no copy) |
| Fault tolerance | **Poor** (reader down when owner down) | Good | **Excellent** (cache survives owner outage) | Good |
| Contract versioning | Contract = API (tight) | Table = contract, but per-owner | Contract = cache DTO | Table = contract, **broad** bounded context |
| Service scalability | Reader scales ⇒ owner must scale | Independent | Independent | Independent |
| Complexity / setup | Low | Medium (replication tooling) | High (cluster + TCP discovery) | Low |

(source: raw/software-architecture-the-hard-parts/chapter-10-distributed-data-access.md, Tables 10-1 to 10-4)

## Picking a pattern

The chapter's rubric, walked through on the Wishlist/Catalog example:

1. **Start with [[interservice-communication-pattern]]** — simplest. Accept it unless one of its weaknesses (slow, fragile, static coupling) is disqualifying.
2. **If response time or fault tolerance matters** → [[replicated-caching-pattern]], provided the data volume is small (< ~500 MB), the change rate is low, and the infra can support cluster discovery.
3. **If data volume is too large for a cache** and responsiveness still matters → [[column-schema-replication-pattern]], accepting staleness and weakened governance.
4. **If none of the above fit** (large data, hard consistency, hard responsiveness, hard fault-tolerance all at once) → [[data-domain-pattern]]. Accept a broader bounded context as the price.

The chapter frames (4) as "the last resort that has the most benefits" — decoupling, consistency, responsiveness, integrity — but at the cost of widening the bounded context across two services and losing the schema-as-abstraction.

## Relationship to Ch 9

Chapter 9 ([[data-ownership]]) answers *who writes this table*. Chapter 10 answers *how everyone else reads it*. The two chapters share vocabulary (bounded context, joint ownership, data domain) because one access pattern — [[data-domain-pattern]] — is literally the joint-ownership **data domain technique** reused on the read side (source: raw/software-architecture-the-hard-parts/chapter-10-distributed-data-access.md).

A clean ownership decision plus a well-chosen access pattern is what lets a decomposed system stay decomposed.

## Related pages

- [[interservice-communication-pattern]]
- [[column-schema-replication-pattern]]
- [[replicated-caching-pattern]]
- [[data-domain-pattern]]
- [[data-ownership]]
- [[joint-ownership-techniques]]
- [[data-domain]]
- [[data-sovereignty]]
- [[database-decomposition]]
- [[bounded-context]]
- [[eventual-consistency]]
- [[shared-database-antipattern]]
- [[synchronous-microservices]]
- [[cache-memory-storage]]
- [[software-architecture-the-hard-parts]]
