# Eventual Consistency

**Summary**: The weakest useful replication consistency guarantee: if writes to a replicated system stop, all replicas will *eventually* converge to the same value — but with no bound on when, and no guarantees about intermediate states.

**Sources**: `raw/designing-data-intensive-applications/chapter-05-replication.md`, `raw/designing-data-intensive-applications/chapter-08-the-trouble-with-distributed-systems.md`, `raw/designing-data-intensive-applications/chapter-12-the-future-of-data-systems.md`, `raw/monolith-to-microservices/chapter-04-decomposing-the-database.md`, `raw/site-reliability-engineering/chapter-23-managing-critical-state-distributed-consensus-for-reliability.md`, `raw/fundamentals-of-data-engineering/chapter-06-storage.md`, `raw/software-architecture-the-hard-parts/chapter-09-data-ownership-and-distributed-transactions.md`, `raw/software-architecture-the-hard-parts/chapter-12-transactional-sagas.md`

**Last updated**: 2026-04-19

---

## What it means

Eventual consistency says: given enough time without new writes, all replicas will converge to the same state. The word "eventually" is deliberately vague — there is no specified time bound. A better name for eventual consistency may be **convergence**, as we expect all replicas to eventually converge to the same value. (source: designing-data-intensive-applications, chapter 9)

In practice, on a healthy system with no network problems, [[replication-lag]] may be milliseconds and eventual consistency feels like strong consistency. Under load or network partition, lag can stretch to minutes or hours, and the "eventual" guarantee becomes painfully visible to users.

Eventual consistency was coined by Douglas Terry et al. and popularized by Werner Vogels (Amazon CTO). It became the battle cry of many NoSQL projects. However, it is not unique to NoSQL: asynchronous followers in any relational database have the same characteristic.

## Position in the consistency hierarchy

Eventual consistency is the weakest useful guarantee. Stronger models include (source: designing-data-intensive-applications, chapter 9):

- **[[causal-consistency]]**: preserves cause-and-effect ordering while allowing concurrent operations to be unordered. The strongest model that does not sacrifice availability or performance during network faults.
- **[[linearizability]]**: the strongest single-object guarantee, making the system appear as if there is only one copy of the data. Comes at a cost to performance and availability.

Systems with stronger guarantees may have worse performance or be less fault-tolerant, but they are easier to use correctly. The choice depends on the application's needs. (source: designing-data-intensive-applications, chapter 9)

## What it does NOT guarantee

Eventual consistency alone does not provide:
- [[read-after-write-consistency]] — you may not see your own writes
- [[monotonic-reads]] — you may see data go backward in time
- [[consistent-prefix-reads]] — you may see effects before their causes

These are separate, stronger guarantees that can be layered on top of eventual consistency through careful routing and coordination.

## The operability problem

"Eventually" is not a useful quantity for operations. If a replica falls hours behind, the system is behaving badly — but eventual consistency provides no metric to detect this. Better operational practice requires measuring **replication lag** concretely and alerting on it. Research has been done on bounding the probability of stale reads given parameters n, w, r in quorum systems; formalising this was historically not standard, though cloud vendors have since made replication-lag observability routine.

## Transactions as the honest alternative

The deeper insight from the book: eventual consistency became popular partly because distributed transactions were considered too expensive. But this was overstated. Rather than pretending asynchronous replication is synchronous (a recipe for subtle bugs), systems should provide honest guarantees. Transactions are the database's mechanism for giving applications stronger promises so application code stays simple. The chapter foreshadows that transactions and consensus (Chapters 7 and 9) will revisit these tradeoffs more rigorously.

## Eventual consistency as a liveness property

Chapter 8 classifies eventual consistency as a **[[safety-and-liveness|liveness property]]**: it says "something good eventually happens" (replicas converge), but it may not hold at any given point in time. This is in contrast to safety properties (e.g., uniqueness of a fencing token), which must hold at all times and whose violation is permanent. The word "eventually" in the definition is the giveaway. (source: designing-data-intensive-applications, chapter 8)

This classification matters because liveness properties are allowed caveats in [[system-models]]: for example, convergence may only be guaranteed if a majority of nodes have not crashed and the network eventually recovers. Safety properties, by contrast, must hold even during total failures.

## Eventual consistency in microservice migrations

Sam Newman frames eventual consistency as the natural consequence of database decomposition. Patterns like [[tracer-write]] and [[synchronize-data-in-application]] explicitly maintain two sources of truth during a migration, with synchronisation between them — and "however long this window of inconsistency is, such synchronization gives us what is called eventual consistency." (source: chapter-04-decomposing-the-database.md)

Newman emphasises a practical operational requirement that mirrors the operability problem above: "It's important that when maintaining two sources of truth like this that you have some kind of reconciliation process to ensure that the synchronization is working as intended. This may be something as simple as a couple of SQL queries you can run against each database. But without checking that the synchronization is working as expected, you may end up with inconsistencies between the two systems and not realize it until it is too late." (source: chapter-04-decomposing-the-database.md)

The same principle reappears in [[saga|sagas]]: sub-transactions across services are not atomic, so observers can briefly see inconsistent intermediate states. The shorter the inconsistency window you require, the more difficult the implementation becomes — pick a tolerance you can live with and build your synchronisation accordingly.

## The operator burden (SRE Chapter 23)

Laura Nolan's *Site Reliability Engineering* Chapter 23 is blunter still about the cost of eventual consistency to downstream teams. She quotes Jeff Shute:

> We find developers spend a significant fraction of their time building extremely complex and error-prone mechanisms to cope with eventual consistency and handle data that may be out of date. We think this is an unacceptable burden to place on developers and that consistency problems should be solved at the database level.

(source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md)

Nolan reinforces the point with two specific operational failure modes that Multimaster-replication systems with BASE semantics are vulnerable to:

- **Clock drift** — multimaster conflict resolution commonly uses "latest timestamp wins," which fails silently under [[unreliable-clocks|clock skew]].
- **Network partitioning** — partitions produce divergent histories whose reconciliation depends on the specific LWW / CRDT / merge rules, which are easy to get wrong.

Kyle Kingsbury's Jepsen series is cited as the canonical body of evidence for what can go wrong in practice. The chapter's framing: eventual consistency is appropriate for some workloads but is not a generic substitute for correctness on critical state — and critical state is exactly what [[consensus]] is for. See [[managing-critical-state]] and the [[cap-theorem|CAP theorem reframing]] in the same chapter.

## Eventual consistency as a timeliness violation

Chapter 12 clarifies the relationship between eventual consistency and [[timeliness-and-integrity|integrity]]. Violations of timeliness are "eventual consistency" -- temporary and self-healing. Violations of integrity are "perpetual inconsistency" -- permanent and requiring explicit repair. In most applications, integrity is far more important than timeliness. Event-based dataflow systems decouple the two, providing strong integrity guarantees (via [[exactly-once-semantics|idempotent processing]]) while accepting weak timeliness (asynchronous updates). This enables [[coordination-avoidance|coordination-avoiding systems]] that scale better than systems requiring [[linearizability]] (source: chapter-12-the-future-of-data-systems.md).

## FoDE Ch 6 — BASE and object storage

Chapter 6 of *Fundamentals of Data Engineering* gives the engineering view of BASE/eventual-consistency trade-offs in distributed storage (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md):

> BASE stands for basically available, soft-state, eventual consistency. Think of it as the opposite of ACID.
>
> - **Basically available** — consistency is not guaranteed, but efforts at database reads and writes are made on a best-effort basis.
> - **Soft-state** — the state of the transaction is fuzzy, and it's uncertain whether the transaction is committed or uncommitted.
> - **Eventual consistency** — at some point, reading data will return consistent values.

Chapter 6 also gives a worked example: **Amazon S3 was eventually consistent until recently**. "After a new version of an object was written under the same key, the object store might sometimes return the old version of the object. The eventual part of eventual consistency means that after enough time has passed, the storage cluster reaches a state such that only the latest version of the object will be returned" (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md). AWS made S3 strongly consistent for read-after-write and list operations in December 2020.

The practical recipe Chapter 6 describes for layering strong consistency on top of an eventually-consistent object store:

1. Write the object.
2. Write the returned object-version metadata (hash or timestamp + key) to a **strongly consistent database** (e.g. PostgreSQL).
3. To read: fetch the latest metadata, query the object by (key, version), retry if mismatch.

This is essentially what [[lakehouse-table-formats|Delta Lake, Iceberg, and Hudi]] do to get ACID transactions over eventually-consistent object storage.

## Hard Parts Ch 9: three eventual-consistency patterns for distributed transactions

*Software Architecture: The Hard Parts* Chapter 9 gives the clearest catalogue of eventual-consistency patterns an architect can reach for once a business request crosses service boundaries and [[distributed-transactions|loses ACID]]. The three main patterns (source: raw/software-architecture-the-hard-parts/chapter-09-data-ownership-and-distributed-transactions.md):

1. **[[background-synchronization-pattern]]** — an external process (batch job or periodic service) reconciles data sources after the fact. Best user-visible response time; **breaks bounded contexts** because the sync process must write every participating service's tables. Appropriate only for closed heterogeneous systems, not microservices.

2. **[[orchestrated-request-based-pattern]]** — an orchestrator drives the distributed transaction to completion during the user's request. Strong consistency by response time; poor responsiveness; complex error handling via [[compensating-update|compensating updates]]; "compensation of compensation fails" is a real failure mode that ends in human intervention.

3. **[[event-based-consistency-pattern]]** — the primary service commits, publishes an event, and returns. Subscribers align asynchronously in parallel. Short consistency window; good decoupling; error handling via durable subscribers, retries, and dead letter queues. The book names this "one of the most popular and reliable" patterns for modern distributed architectures.

The three patterns cleanly match the three trade-off axes: user-visible latency, service coupling, and data freshness. Chapter 9's default recommendation is the event-based pattern; choose others only when specific constraints demand it.

The vocabulary BA + S + E — [[base-properties|BASE]] — is how the book summarises what these patterns actually deliver.

## Hard Parts Ch 12: saga state machines as the eventual-consistency error-handling primitive

Chapter 12 adds a specific technique for eventual-consistency sagas: **[[saga|saga state machines]]**. Rather than issue a [[compensating-update|compensating update]] on partial failure, the saga transitions to an explicit error state (the book's example: the Fairy Tale saga moves to `NO_SURVEY` when the Survey Service is unavailable) and the orchestrator retries or escalates to human operators asynchronously. The end user gets a successful response immediately; the system takes responsibility for eventual alignment (source: raw/software-architecture-the-hard-parts/chapter-12-transactional-sagas.md).

State machines dominate compensating updates inside eventual-consistency sagas because they align with the consistency model: if the saga is not trying to be atomic, rolling back partially-committed state is structurally the wrong shape. Track progress, retry, converge.

The full eight-pattern catalogue is at [[saga]]; the four eventual-consistency sagas are [[fairy-tale-saga]], [[time-travel-saga]], [[parallel-saga]], and [[anthology-saga]].

## Three places to make consistency decisions

Chapter 6 crystallises the design space into three choice points data engineers actually have (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md):

1. **The database technology itself** sets the consistency ceiling.
2. **Configuration parameters** tune within that ceiling.
3. **Per-query consistency options.** Example: DynamoDB supports eventually-consistent reads and strongly-consistent reads as per-request flags. Strong reads are slower and cost more; use them sparingly, but use them when correctness demands it.

The framing matters for ingestion and CDC: the engineer must know which mode a source system operates in, because the consistency mode determines what invariants hold across a snapshot scan or a streamed change feed.

## Related pages

- [[replication]]
- [[replication-lag]]
- [[read-after-write-consistency]]
- [[monotonic-reads]]
- [[consistent-prefix-reads]]
- [[quorums]]
- [[leaderless-replication]]
- [[causal-consistency]]
- [[linearizability]]
- [[cap-theorem]]
- [[safety-and-liveness]]
- [[timeliness-and-integrity]]
- [[coordination-avoidance]]
- [[exactly-once-semantics]]
- [[tracer-write]]
- [[synchronize-data-in-application]]
- [[saga]]
- [[database-decomposition]]
- [[consensus]]
- [[managing-critical-state]]
- [[object-storage]]
- [[lakehouse-table-formats]]
- [[acid]]
- [[base-properties]]
- [[background-synchronization-pattern]]
- [[orchestrated-request-based-pattern]]
- [[event-based-consistency-pattern]]
- [[compensating-update]]
- [[data-ownership]]
- [[software-architecture-the-hard-parts]]
- [[fairy-tale-saga]]
- [[time-travel-saga]]
- [[parallel-saga]]
- [[anthology-saga]]
