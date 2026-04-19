# ACID

**Summary**: The four safety guarantees of database [[transactions]] -- Atomicity, Consistency, Isolation, and Durability -- coined in 1983 by Theo Harder and Andreas Reuter, though in practice the meaning varies significantly between database implementations.

**Sources**: `raw/designing-data-intensive-applications/chapter-07-transactions.md`, `raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md`, `raw/fundamentals-of-data-engineering/chapter-06-storage.md`

**Last updated**: 2026-04-18

---

## Overview

ACID stands for Atomicity, Consistency, Isolation, and Durability. The acronym was coined in 1983 to establish precise terminology for fault-tolerance mechanisms in databases. In practice, one database's implementation of ACID does not equal another's -- the term has become partly a marketing label. (source: chapter-07-transactions.md)

Systems that do not meet ACID criteria are sometimes called BASE (Basically Available, Soft state, Eventual consistency), which is even vaguer -- it essentially means "not ACID." (source: chapter-07-transactions.md)

## Atomicity

In the ACID context, atomicity does **not** mean concurrency-related atomicity (as in multi-threaded programming). It means: if a transaction cannot be completed due to a fault, all writes made so far in that transaction are discarded. The database undoes partial changes so the application can safely retry. (source: chapter-07-transactions.md)

The defining feature: the ability to abort a transaction on error and have all its writes discarded. A better name might be "abortability." (source: chapter-07-transactions.md)

## Consistency

The word "consistency" is overloaded across at least four different meanings in data systems (source: chapter-07-transactions.md):

1. **Replica consistency** -- [[eventual-consistency]] in [[replication]]
2. **Consistent hashing** -- a [[partitioning]] technique
3. **Linearizability** -- as used in the CAP theorem
4. **ACID consistency** -- application-defined invariants are preserved

ACID consistency means the database is always in a "valid state" according to application-defined invariants (e.g., credits and debits must balance). This is the application's responsibility, not the database's. The database provides atomicity and isolation as tools, but the application must define correct transactions. As Joe Hellerstein remarked, the C in ACID was "tossed in to make the acronym work." (source: chapter-07-transactions.md)

## Isolation

Concurrently executing [[transactions]] are isolated from each other. The textbook definition is [[serializability]]: the result is the same as if transactions ran serially, one at a time. (source: chapter-07-transactions.md)

In practice, serializable isolation is rarely used due to its performance cost. Most databases default to weaker [[isolation-levels]] such as [[read-committed]] or [[snapshot-isolation]]. (source: chapter-07-transactions.md)

## Durability

Once a transaction has committed, its data will not be lost even if hardware fails or the database crashes. (source: chapter-07-transactions.md)

Implementation varies by context:

- **Single-node**: data written to nonvolatile storage (hard drive or SSD), typically with a write-ahead log for crash recovery
- **Replicated database**: data successfully copied to some number of nodes before reporting commit

Perfect durability does not exist. Risks include correlated faults (power outages affecting all replicas), SSD firmware bugs, gradual data corruption, and storage media degradation. In practice, durability is achieved through a combination of writing to disk, replicating to remote machines, and backups. (source: chapter-07-transactions.md)

## FoDE framing: relaxing ACID at the source

Reis and Housley's Chapter 5 of *Fundamentals of Data Engineering* emphasises an operational consequence of the DDIA framing above: ACID properties "are not required to support application backends, and relaxing these constraints can be a considerable boon to performance and scale" — but ACID compliance "dramatically [simplifies] the app developer's task" by maintaining a consistent picture of the world (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md).

The data-engineer implication: every [[source-systems|source system]] has an *ACID posture* — fully ACID, relaxed in specific ways, or [[eventual-consistency|eventually consistent]]. The engineer must know which, because the posture affects:

- **Extraction correctness.** A non-ACID source may present inconsistent rows during a snapshot scan — half-updated joins, missing foreign keys, ghost rows that get rolled back.
- **CDC semantics.** [[change-data-capture|Log-based CDC]] on an ACID source gives a causally consistent event stream; on a non-ACID distributed store (e.g. many NoSQL stores) the stream may be ordered within but not across partitions.
- **Query behaviour.** Distributed NoSQL stores offer optional consistency modes (strong-consistency reads, quorum reads). The engineer must pick the right one for the workload.

Reis and Housley: "all engineers (data or otherwise) must understand operating with and without ACID. Understanding the consistency model you're working with helps you prevent disasters" (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md).

## FoDE Ch 6 — ACID on object storage via the lakehouse

Chapter 6 treats ACID as the feature that makes [[data-lakehouse|lakehouses]] meaningfully different from classic [[data-lake|data lakes]] (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md):

> The lakehouse [...] supports atomicity, consistency, isolation, and durability (ACID) transactions, a big departure from the original data lake.

Mechanically, lakehouse [[lakehouse-table-formats|table formats]] (Delta Lake, Iceberg, Hudi) achieve ACID over [[eventual-consistency|eventually-consistent]] [[object-storage]] by layering a transaction log — a strongly-ordered sequence of commit metadata — on top of the Parquet files. Readers consult the log to determine which files belong to a given table version; writes append a new log entry atomically. This is the same **strongly-consistent-database-over-weaker-store** recipe described in [[eventual-consistency|Chapter 6's consistency discussion]]. [[mvcc|MVCC]] underlies the isolation story: old file versions are retained until garbage-collected, so concurrent readers see consistent snapshots.

Cloud warehouses like Snowflake and BigQuery provide the same ACID guarantees internally; the open lakehouse formats provide them portably across engines.

## Related pages

- [[transactions]]
- [[isolation-levels]]
- [[serializability]]
- [[reliability]]
- [[fault-tolerance]]
- [[replication]]
- [[eventual-consistency]]
- [[source-systems]]
- [[application-database-as-source]]
- [[data-lakehouse]]
- [[lakehouse-table-formats]]
- [[mvcc]]
- [[object-storage]]
