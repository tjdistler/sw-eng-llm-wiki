# Distributed Transactions

**Summary**: Transactions that span multiple nodes or heterogeneous systems, using protocols like [[two-phase-commit]] to ensure atomic commit -- powerful for maintaining cross-system consistency, but carrying significant operational and performance costs. In microservice architectures, both Kleppmann and Newman recommend avoiding them entirely; Newman's preferred alternative is the [[saga]].

**Sources**: `raw/designing-data-intensive-applications/chapter-09-consistency-and-consensus.md`, `raw/designing-data-intensive-applications/chapter-12-the-future-of-data-systems.md`, `raw/monolith-to-microservices/chapter-04-decomposing-the-database.md`

**Last updated**: 2026-04-16

---

## Two types

There are two quite different kinds of distributed transactions that are often conflated (source: designing-data-intensive-applications, chapter 9):

### Database-internal distributed transactions

All participants run the same database software (e.g., VoltDB, MySQL Cluster NDB). The database can use any internal protocol and apply technology-specific optimizations. These often work quite well. (source: designing-data-intensive-applications, chapter 9)

### Heterogeneous distributed transactions

Participants are different technologies: different database vendors, message brokers, or non-database systems. These must use a common protocol (typically XA) and are much more challenging. (source: designing-data-intensive-applications, chapter 9)

## XA transactions

X/Open XA (eXtended Architecture) is the standard for [[two-phase-commit]] across heterogeneous technologies, introduced in 1991. Supported by PostgreSQL, MySQL, DB2, SQL Server, Oracle, ActiveMQ, HornetQ, MSMQ, and IBM MQ. (source: designing-data-intensive-applications, chapter 9)

XA is a C API (with bindings for other languages, e.g., Java Transaction API / JTA) for interfacing with a transaction coordinator. The coordinator is typically a library loaded into the application process, tracking participants and managing prepare/commit/abort via callbacks into database drivers. (source: designing-data-intensive-applications, chapter 9)

## Exactly-once message processing

A key use case for heterogeneous distributed transactions: atomically committing a message acknowledgment and the database writes triggered by processing that message. If either fails, both are rolled back, and the message broker can safely redeliver. This achieves effectively exactly-once processing semantics. (source: designing-data-intensive-applications, chapter 9)

This only works if all affected systems support the same atomic commit protocol. Side effects that cannot participate in 2PC (like sending email) may be duplicated on retry. (source: designing-data-intensive-applications, chapter 9)

## Problems in practice

**Performance**: distributed transactions in MySQL are reported to be over 10x slower than single-node transactions, due to additional disk forcing (fsync) for crash recovery and extra network round-trips. (source: designing-data-intensive-applications, chapter 9)

**Coordinator as single point of failure**: if the coordinator crashes, participants with prepared-but-uncommitted transactions are stuck in doubt, holding locks. The coordinator's transaction log on the application server's disk becomes critical durable state. (source: designing-data-intensive-applications, chapter 9)

**Holding locks while in doubt**: participants hold row-level locks (exclusive for writes, shared for [[two-phase-locking]]) throughout the in-doubt period. If the coordinator is down for 20 minutes, locks are held for 20 minutes. If the log is lost, locks are held forever until manual intervention. Other transactions that need the same data are blocked. (source: designing-data-intensive-applications, chapter 9)

**Orphaned in-doubt transactions**: when the coordinator cannot determine the outcome (e.g., corrupted log), transactions remain in doubt permanently, holding locks across database restarts. The only escape is manual resolution by an administrator or "heuristic decisions" (unilateral commit/abort by participants, which breaks atomicity). (source: designing-data-intensive-applications, chapter 9)

**Stateful application servers**: the coordinator's log makes the application server stateful, undermining the stateless application model common in HTTP-based services. (source: designing-data-intensive-applications, chapter 9)

**Lowest common denominator**: XA cannot detect cross-system deadlocks or support [[serializable-snapshot-isolation]] across different systems, since those would require standardized protocols for exchanging lock or conflict information. (source: designing-data-intensive-applications, chapter 9)

**Amplifying failures**: 2PC requires all participants to respond for a commit to succeed. If any part of the system is broken, the transaction fails. This runs counter to the goal of [[fault-tolerance]]. (source: designing-data-intensive-applications, chapter 9)

## Alternatives

The book notes that the same cross-system consistency goals can be achieved through alternative approaches without the pain of heterogeneous distributed transactions, to be explored in later chapters (event-based architectures, idempotent operations). (source: designing-data-intensive-applications, chapter 9)

## Log-based derived data as an alternative

Chapter 12 articulates the full alternative to distributed transactions: **log-based [[derived-data]]** with [[exactly-once-semantics|idempotent consumers]]. The comparison (source: chapter-12-the-future-of-data-systems.md):

| | Distributed transactions | Log-based derived data |
|---|---|---|
| Ordering | Locks (mutual exclusion) | Event log ordering |
| Atomicity | Atomic commit (2PC) | Deterministic retry + idempotence |
| Consistency | [[linearizability]] (synchronous) | Asynchronous (eventual) |
| Failure mode | Amplifies failures (any participant failing aborts all) | Contains failures (faulty consumer catches up later) |

Within a single storage or [[stream-processing]] system, transactions work well. But when data crosses technology boundaries, an asynchronous event log with idempotent writes is more robust than trying to coordinate heterogeneous systems with XA. End-to-end request IDs passed from client through all processing stages provide [[exactly-once-semantics]] without atomic commit across partitions. See [[end-to-end-argument]] and [[coordination-avoidance]] (source: chapter-12-the-future-of-data-systems.md).

## Newman's microservice perspective: sagas as the alternative

Sam Newman addresses distributed transactions in the context of decomposing a monolith's database. When a previously single-database operation now spans services, teams reflexively reach for 2PC; Newman's chapter exists in part to push them toward [[saga|sagas]] instead. (source: chapter-04-decomposing-the-database.md)

His framing aligns with Pat Helland: "In most distributed transaction systems, the failure of a single node causes transaction commit to stall. This in turn causes the application to get wedged. In such systems, the larger it gets, the more likely the system is going to be down. When flying an airplane that needs all of its engines to work, adding an engine reduces the availability of the airplane." — Pat Helland, *Life Beyond Distributed Transactions* (source: chapter-04-decomposing-the-database.md)

Newman's three options when an old transaction boundary is being broken (source: chapter-04-decomposing-the-database.md):

1. **Don't split.** If the data really must be ACID-atomic together, leave it together — in one service or in the monolith.
2. **Defer the split.** Work on other parts of the system first; come back when you have more clarity.
3. **Model the operation as a [[saga]]**: a sequence of local transactions with compensating actions and explicit reasoning about state.

What Newman likes about the saga path beyond avoiding 2PC's pitfalls: it forces you to model your business processes **explicitly**, where they were previously implicit and scattered across the codebase.

## Related pages

- [[two-phase-commit]]
- [[saga]]
- [[transactions]]
- [[acid]]
- [[consensus]]
- [[fault-tolerance]]
- [[serializability]]
- [[two-phase-locking]]
- [[derived-data]]
- [[exactly-once-semantics]]
- [[idempotence]]
- [[end-to-end-argument]]
- [[coordination-avoidance]]
- [[data-integration]]
- [[database-decomposition]]
