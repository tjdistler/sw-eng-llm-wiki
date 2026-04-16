# Transactions

**Summary**: An abstraction layer that groups multiple reads and writes into a logical unit with an all-or-nothing guarantee, simplifying error handling and concurrency control for applications accessing a database.

**Sources**: `raw/designing-data-intensive-applications/chapter-07-transactions.md`, `raw/designing-data-intensive-applications/chapter-12-the-future-of-data-systems.md`, `raw/monolith-to-microservices/chapter-04-decomposing-the-database.md`

**Last updated**: 2026-04-16

---

## Purpose

A transaction allows an application to group several reads and writes together so they execute as one operation: either the entire transaction succeeds (commit) or it fails (abort/rollback). This frees the application from worrying about partial failure -- the case where some operations succeed and some fail. (source: chapter-07-transactions.md)

Transactions are not a law of nature. They were created to simplify the programming model for applications. By using transactions, the application can ignore certain error scenarios and concurrency issues because the database handles them instead. (source: chapter-07-transactions.md)

## Safety guarantees: ACID

The safety guarantees provided by transactions are described by the acronym [[acid]]:

- **Atomicity**: If a fault occurs partway through, the transaction is aborted and all writes are discarded. The application can safely retry.
- **Consistency**: Application-defined invariants are preserved (this is actually the application's responsibility, not the database's).
- **Isolation**: Concurrently executing transactions cannot interfere with each other. Formally, this means [[serializability]] -- the result is the same as if transactions ran serially.
- **Durability**: Once committed, data is not lost even if hardware fails or the database crashes.

See [[acid]] for a detailed breakdown of each property.

## Single-object vs multi-object transactions

Storage engines provide atomicity and isolation at the single-object level (e.g., using crash-recovery logs and per-object locks). Some databases offer atomic increment and compare-and-set operations for single objects. These have been marketed as "lightweight transactions" but are not true transactions in the multi-object sense. (source: chapter-07-transactions.md)

Multi-object transactions are needed when several pieces of data must be kept in sync:

- Foreign key references across tables in a [[relational-model]]
- Denormalized data in a [[document-model]] that spans multiple documents
- Secondary [[indexes]] that must be updated alongside the data they reference

## Error handling and retries

A key feature of transactions is that aborted transactions can be safely retried. However, retries have caveats (source: chapter-07-transactions.md):

- If the transaction succeeded but the acknowledgment was lost over the network, retrying causes duplicate execution (need application-level deduplication).
- Retrying after overload errors can worsen the problem (use exponential backoff).
- Only transient errors are worth retrying; permanent errors (e.g., constraint violations) make retries pointless.
- Side effects outside the database (e.g., sending emails) may not be safe to repeat.

## Concurrency and isolation levels

Concurrency bugs are hard to find by testing because they depend on timing. Databases provide [[isolation-levels]] to protect against race conditions. In practice, most databases use weak isolation levels that protect against some but not all race conditions. See [[isolation-levels]] for a comparison.

Key race conditions that transactions help prevent:

- [[dirty-reads-and-dirty-writes]]
- [[read-skew]] (nonrepeatable reads)
- [[lost-updates]]
- [[write-skew]]
- [[phantoms]]

## Approaches to serializable isolation

Only [[serializability]] prevents all race conditions. Three implementation approaches exist:

1. **[[actual-serial-execution]]** -- execute transactions one at a time on a single thread
2. **[[two-phase-locking]]** -- readers and writers block each other via shared/exclusive locks
3. **[[serializable-snapshot-isolation]]** -- optimistic approach built on [[snapshot-isolation]] with conflict detection at commit time

## Distributed transactions

When transactions span multiple nodes or partitions, achieving atomicity requires a protocol for all nodes to agree on the outcome (commit or abort). This is the atomic commit problem, solved in practice by [[two-phase-commit]] (2PC). However, 2PC has significant operational downsides: coordinator failure can leave participants stuck holding locks indefinitely. See [[distributed-transactions]] for the full picture. (source: designing-data-intensive-applications, chapter 9)

The atomic commit problem is formally equivalent to [[consensus]]: if you can solve one, you can solve the other. Fault-tolerant consensus algorithms (Paxos, Raft, Zab) provide a better foundation than 2PC because they require only majority agreement rather than unanimity. (source: designing-data-intensive-applications, chapter 9)

## Losing transactions when splitting a database

When a monolith's database is split across services (see [[database-decomposition]]), an operation that was previously a single ACID transaction now spans two databases. Newman points out that this is one of the largest costs of microservice extraction — and the first ACID property you lose is **atomicity**. (source: chapter-04-decomposing-the-database.md)

You can still use ACID transactions for changes within a single service's schema. What you lose is the ability to atomically change state across services. Newman's preferred alternative is the [[saga]] — model the cross-service operation as a sequence of local transactions with compensating actions for rollback, instead of reaching for [[two-phase-commit|2PC]].

## The end-to-end argument and transactions

Chapter 12 argues that even serializable transactions are insufficient for application correctness. Application bugs, duplicate user requests after timeouts, and cross-system interactions all occur outside the scope of a single database transaction. True correctness requires [[end-to-end-argument|end-to-end measures]] such as passing unique operation IDs from the client through every processing stage. Transactions remain a valuable simplification (reducing many failure modes to commit/abort), but they are not the last word on correctness (source: chapter-12-the-future-of-data-systems.md).

## Timeliness vs integrity

Chapter 12 decomposes what transactions provide into two distinct properties. [[acid|ACID]] transactions typically deliver both, which is why the distinction is rarely made. But in event-based dataflow systems, they are decoupled: [[timeliness-and-integrity|timeliness]] (up-to-date reads, achieved by linearizability) can be relaxed while preserving integrity (no corruption, achieved through [[exactly-once-semantics|idempotent processing]]). This enables [[coordination-avoidance|coordination-avoiding systems]] that maintain correctness with much better performance and fault tolerance than distributed transactions (source: chapter-12-the-future-of-data-systems.md).

## Related pages

- [[acid]]
- [[isolation-levels]]
- [[serializability]]
- [[snapshot-isolation]]
- [[two-phase-locking]]
- [[serializable-snapshot-isolation]]
- [[fault-tolerance]]
- [[reliability]]
- [[replication]]
- [[partitioning]]
- [[distributed-transactions]]
- [[two-phase-commit]]
- [[saga]]
- [[database-decomposition]]
- [[consensus]]
- [[end-to-end-argument]]
- [[timeliness-and-integrity]]
- [[exactly-once-semantics]]
- [[coordination-avoidance]]
