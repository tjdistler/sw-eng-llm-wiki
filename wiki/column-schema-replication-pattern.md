# Column Schema Replication Pattern

**Summary**: A [[distributed-data-access]] pattern that solves cross-service reads by **copying the columns** into the reading service's own table. The Wishlist Service gets an `item_desc` column in its wishlist table, kept in sync asynchronously from the Catalog Service. Reads are local SQL joins again — fast, fault-tolerant, independently scalable — at the cost of staleness, sync machinery, and fuzzy governance of the copied data.

**Sources**: `raw/software-architecture-the-hard-parts/chapter-10-distributed-data-access.md`

**Last updated**: 2026-04-19

---

## The mechanics

The Catalog Service owns the `item_desc` column. The Column Schema Replication pattern adds the same column to the Wishlist table, and whenever the Catalog Service creates/updates/deletes a product, it **pushes the change asynchronously** — via queue, topic, or event stream — to the Wishlist Service (and every other consumer) (source: raw/software-architecture-the-hard-parts/chapter-10-distributed-data-access.md).

The Wishlist Service then serves reads with a plain local SQL query. No network call, no owner-service dependency at read time.

## Why async sync is usually right

The book recommends **asynchronous** replication over synchronous propagation:

- Responsiveness — the writer doesn't wait on the replicator.
- Availability — the Wishlist Service's replica doesn't depend on the Catalog Service being up at the moment of the write.

Synchronous replication is only justified when **immediate transactional consistency** is required — which, if it is, probably disqualifies this pattern in favour of [[data-domain-pattern]].

See also [[replication]] (Kleppmann's treatment of leader-based and broker-based replication) and [[change-data-capture]] as a mechanical substrate.

## The governance problem

Because the `item_desc` column now lives *inside* the Wishlist Service's schema, the Wishlist Service is **technically able** to write to it — even though the Catalog Service is the official owner. Chapter 10 flags this as a first-class weakness: nothing at the database layer enforces the ownership rule ([[data-ownership]]) once the column has been replicated (source: raw/software-architecture-the-hard-parts/chapter-10-distributed-data-access.md).

Chapter 9's writer-owns rule now has to be enforced by **application-layer policy and review**, which is weaker than the DB-level enforcement the original bounded context provided.

## Data consistency

Two inherent lags:

- **Change propagation delay** — the window between a Catalog update and the Wishlist replica reflecting it.
- **Schema drift** — if the Catalog Service changes the shape of `item_desc` (length, encoding, semantic meaning), every replica has to catch up, which means multi-service coordination.

Staleness is tolerable for slow-changing reference data (product descriptions, categorical codes). It is **not** tolerable for inventory counts, prices, or balances — see [[replicated-caching-pattern]] for the analogous caveat and [[data-domain-pattern]] for the consistency-preserving alternative.

## Trade-offs summary (Table 10-2)

| Dimension | Rating |
|---|---|
| Service dependency | **Medium** — async sync coupling |
| Response time | **Excellent** — local SQL |
| Data currency | **Poor** — replication lag |
| Fault tolerance | Good — local reads survive owner outage |
| Data volume | Any |
| Scalability | Independent |
| Complexity | Medium — replication tooling, schema coordination |
| Contract versioning | Table schema is the contract, per-replica |

(source: raw/software-architecture-the-hard-parts/chapter-10-distributed-data-access.md, Table 10-2)

## When to use it

Chapter 10 is explicit: this is **not the default**. The governance softness is a genuine cost. But it wins in:

- **Data aggregation and reporting** where queries need to join across many sources.
- **Large data volumes** where [[replicated-caching-pattern]] is ruled out by memory footprint.
- **Very high responsiveness or fault-tolerance requirements** where a cache is unavailable (too volatile, too big) and service calls are too slow.

See also [[cross-service-analytics]] for the Newman framing of the reporting use case and [[derived-data]] for Kleppmann's broader treatment.

## Related pages

- [[distributed-data-access]]
- [[interservice-communication-pattern]]
- [[replicated-caching-pattern]]
- [[data-domain-pattern]]
- [[data-ownership]]
- [[replication]]
- [[change-data-capture]]
- [[derived-data]]
- [[materialized-view]]
- [[cross-service-analytics]]
- [[eventual-consistency]]
- [[software-architecture-the-hard-parts]]
