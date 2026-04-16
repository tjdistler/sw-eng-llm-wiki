# ACID

**Summary**: The four safety guarantees of database [[transactions]] -- Atomicity, Consistency, Isolation, and Durability -- coined in 1983 by Theo Harder and Andreas Reuter, though in practice the meaning varies significantly between database implementations.

**Sources**: `raw/designing-data-intensive-applications/chapter-07-transactions.md`

**Last updated**: 2026-04-15

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

## Related pages

- [[transactions]]
- [[isolation-levels]]
- [[serializability]]
- [[reliability]]
- [[fault-tolerance]]
- [[replication]]
