---
name: Designing Data-Intensive Applications
description: Summary page for the book by Martin Kleppmann — concepts, organization, and ingestion status
type: source-summary
---

# Designing Data-Intensive Applications

**Summary**: A comprehensive guide to the principles, tradeoffs, and practicalities of data systems — databases, queues, caches, stream processors, and batch processors — by Martin Kleppmann.

**Sources**: `raw/designing-data-intensive-applications/`

**Last updated**: 2026-04-15

---

## About the book

The book examines what different data tools have in common, what distinguishes them, and how they achieve their characteristics. It covers both principles and practicalities, organized into three parts:

- **Part I** — Foundations of data systems (chapters 1–4)
- **Part II** — Distributed data (chapters 5–9)
- **Part III** — Derived data (chapters 10–12)

The central framing: most applications today are **data-intensive** (constrained by data volume, complexity, and velocity) rather than **compute-intensive** (constrained by raw CPU). Standard building blocks — databases, caches, search indexes, stream processors, batch processors — are the vocabulary of data-intensive application design.

## Ingestion status

| Chapter | Title | Status |
|---|---|---|
| 1 | Reliable, Scalable, and Maintainable Applications | Ingested 2026-04-15 |
| 2 | Data Models and Query Languages | Ingested 2026-04-15 |
| 3 | Storage and Retrieval | Ingested 2026-04-15 |
| 4 | Encoding and Evolution | Ingested 2026-04-15 |
| 5 | Replication | Ingested 2026-04-15 |
| 6 | Partitioning | Re-ingested 2026-04-15 |
| 7 | Transactions | Ingested 2026-04-15 |
| 8 | The Trouble with Distributed Systems | Ingested 2026-04-15 |
| 9 | Consistency and Consensus | Ingested 2026-04-15 |
| 10 | Batch Processing | Ingested 2026-04-15 |
| 11 | Stream Processing | Ingested 2026-04-15 |
| 12 | The Future of Data Systems | Ingested 2026-04-15 |

## Chapter 1 concepts

Chapter 1 establishes the three fundamental properties all data systems should aim for:

- [[reliability]] — correct behavior despite faults
- [[scalability]] — coping with load growth
- [[maintainability]] — sustainability over time

Supporting concepts:

- [[fault-tolerance]] — preventing faults from becoming failures
- [[load-parameters]] — quantifying system load
- [[response-time-percentiles]] — measuring performance correctly
- [[scaling-approaches]] — vertical, horizontal, elastic, manual
- [[accidental-complexity]] — complexity to eliminate, vs essential complexity to accept

## Chapter 2 concepts

Chapter 2 covers the landscape of data models and query languages — the central thesis being that the choice of data model shapes everything above it.

- [[data-models]] — the layered abstraction; every application stacks data models
- [[relational-model]] — SQL, tables, joins, history, query optimizer insight
- [[document-model]] — JSON documents, schema flexibility, locality advantage
- [[graph-data-models]] — property graphs, triple-stores, Cypher, SPARQL, Datalog
- [[nosql]] — the movement, driving forces, polyglot persistence
- [[object-relational-mismatch]] — impedance mismatch between OOP code and relational tables
- [[normalization]] — removing duplication with IDs; cost: joins
- [[schema-on-read-vs-write]] — enforcing schema at write vs read time
- [[declarative-vs-imperative-queries]] — why SQL and CSS beat imperative APIs
- [[data-locality]] — adjacent storage for faster full-document reads

## Chapter 3 concepts

Chapter 3 covers how databases store and retrieve data internally — the storage engine layer that sits below the data model. Two families of storage engines serve two different workload types.

OLTP-oriented indexing structures:
- [[storage-engines]] — the two families: log-structured vs update-in-place
- [[indexes]] — what an index is; the read/write tradeoff; types of indexes
- [[hash-indexes]] — append-only log + in-memory hash map (Bitcask)
- [[sstables-and-lsm-trees]] — sorted segments, memtable, LSM-tree, compaction
- [[b-trees]] — fixed-size pages, WAL, the dominant OLTP index structure
- [[write-amplification]] — why one write causes many disk writes; SSD impact

Analytics-oriented storage:
- [[oltp-vs-olap]] — the fundamental access pattern distinction
- [[data-warehousing]] — ETL, star/snowflake schemas, fact and dimension tables
- [[column-oriented-storage]] — store by column; compression, vectorized processing, OLAP cubes

## Chapter 4 concepts

Chapter 4 covers encoding (serialization) formats and how data flows between processes — the infrastructure layer that sits beneath service APIs, databases, and message queues. The central concern is maintaining [[backward-forward-compatibility]] as systems evolve.

Encoding:
- [[backward-forward-compatibility]] — new code reads old data (backward); old code reads new data (forward); both required for rolling upgrades
- [[encoding-formats]] — three categories: language-specific (avoid), textual (JSON/XML/CSV), binary schema-driven (Thrift, Protobuf, Avro)
- [[schema-evolution]] — field tags (Thrift/Protobuf) and writer's/reader's schema (Avro) as mechanisms for safe schema change
- [[avro]] — no field tags; schema resolution by field name; ideal for dynamically generated schemas

Modes of dataflow:
- [[data-outlives-code]] — database records outlast the code that wrote them; old rows and new rows coexist
- [[rpc]] — remote procedure calls; why the local-call abstraction leaks; REST as the honest alternative; gRPC and modern RPC
- [[message-brokers]] — async message passing; decoupling, buffering, fan-out; the actor model

## Chapter 5 concepts

Chapter 5 covers replication — keeping a copy of the same data on multiple machines. The central thesis: replication seems simple but is extraordinarily hard because of the need to handle *changes* to replicated data under network delays, node failures, and concurrency.

Three replication architectures:
- [[leader-based-replication]] — single leader accepts writes; followers replicate; reads can go anywhere
- [[multi-leader-replication]] — multiple leaders accept writes; required for multi-datacenter and offline-first scenarios
- [[leaderless-replication]] — any node accepts writes; quorums provide probabilistic recency (Dynamo-style)

Replication lag and consistency guarantees:
- [[replication-lag]] — the gap between a write on the leader and its appearance on a follower; produces three anomalies
- [[read-after-write-consistency]] — users always see their own writes
- [[monotonic-reads]] — reads never go backward in time
- [[consistent-prefix-reads]] — causally related writes appear in causal order
- [[eventual-consistency]] — the weakest useful guarantee: convergence with no time bound

Failover and conflicts:
- [[failover]] — promoting a new leader; the many failure modes including split brain
- [[write-conflicts]] — detection and resolution: LWW, merge, CRDTs, custom logic, tombstones
- [[quorums]] — w+r>n overlap; sloppy quorums; the edge cases that undermine quorum safety
- [[version-vectors]] — tracking happens-before relationships across replicas

## Chapter 6 concepts

Chapter 6 covers partitioning (sharding) — splitting a dataset across multiple machines for scalability. Two key-based strategies (key-range and hash) trade off range query efficiency against load distribution. Secondary indexes interact with partitioning through local (document-partitioned) and global (term-partitioned) approaches. Rebalancing strategies handle cluster topology changes. Request routing and service discovery complete the picture.

- [[partitioning]] — splitting datasets across nodes; terminology across systems
- [[partitioning-strategies]] — key-range vs hash partitioning trade-offs
- [[hot-spots]] — skewed load on a single partition; causes and mitigation
- [[consistent-hashing]] — hash-based boundaries; why the term is misleading for databases
- [[partitioning-secondary-indexes]] — local (document-partitioned) vs global (term-partitioned) indexes
- [[rebalancing-partitions]] — fixed count, dynamic splitting, proportional to nodes
- [[request-routing]] — service discovery: routing tiers, client awareness, ZooKeeper
- [[service-discovery]] — general problem of locating services across redundant machines

## Chapter 7 concepts

Chapter 7 covers transactions as the primary abstraction for simplifying concurrency and fault tolerance. It systematically builds a hierarchy of isolation levels, characterizes five key race conditions (dirty reads/writes, read skew, lost updates, write skew, phantoms), and compares three approaches to serializability: actual serial execution, two-phase locking, and serializable snapshot isolation.

- [[transactions]] — grouping reads and writes into all-or-nothing logical units
- [[acid]] — Atomicity, Consistency, Isolation, Durability — and how each varies in practice
- [[isolation-levels]] — the spectrum from weak to strong isolation
- [[read-committed]] — prevents dirty reads and dirty writes
- [[snapshot-isolation]] — MVCC-based consistent snapshots; vulnerable to write skew
- [[mvcc]] — multi-version concurrency control for lock-free consistent reads
- [[dirty-reads-and-dirty-writes]] — seeing or overwriting uncommitted data
- [[read-skew]] — nonrepeatable read anomaly
- [[lost-updates]] — concurrent read-modify-write overwriting; prevention strategies
- [[write-skew]] — cross-object invariant violation from concurrent transactions
- [[phantoms]] — search results changed by another transaction's write
- [[serializability]] — strongest isolation; three implementation approaches
- [[two-phase-locking]] — pessimistic serializability via shared/exclusive locks
- [[serializable-snapshot-isolation]] — optimistic serializability (2008); conflict detection at commit
- [[actual-serial-execution]] — single-threaded with stored procedures; feasible when data fits in memory

## Chapter 8 concepts

Chapter 8 catalogs everything that can go wrong in a distributed system — the foundational "trouble" that Chapters 9–12 build solutions for. The core insight: distributed systems suffer *partial failures* that are nondeterministic, unlike single-machine programs that either work or crash completely.

- [[partial-failures]] — the defining characteristic of distributed systems
- [[unreliable-networks]] — asynchronous packet networks with no delivery guarantees
- [[network-faults]] — real-world prevalence of network problems and fault detection
- [[timeouts]] — the only sure fault detection mechanism; adaptive approaches
- [[unreliable-clocks]] — time-of-day vs monotonic; why timestamps are dangerous for ordering
- [[clock-synchronization]] — NTP, GPS, TrueTime; monitoring clock offsets
- [[process-pauses]] — GC, VM suspension, disk I/O; the lease expiry problem
- [[truth-and-leadership-in-distributed-systems]] — why nodes can't trust their own judgment
- [[fencing-tokens]] — monotonically increasing tokens to reject stale lock holders
- [[byzantine-faults]] — nodes that lie; where BFT matters vs doesn't
- [[system-models]] — timing and failure models for reasoning about algorithms
- [[safety-and-liveness]] — nothing bad happens vs something good eventually happens

## Chapter 9 concepts

Chapter 9 builds the solution to Chapter 8's problems: from linearizability (the strongest single-object guarantee) through causal consistency (the strongest without coordination) to consensus (the fundamental agreement primitive). It shows that linearizability, total order broadcast, and consensus are equivalent problems, and that ZooKeeper provides a practical implementation.

- [[linearizability]] — strongest single-object consistency; atomic recency guarantee
- [[causal-consistency]] — preserving cause-and-effect ordering without coordination
- [[lamport-timestamps]] — sequence numbers consistent with causality
- [[total-order-broadcast]] — reliable + totally ordered delivery; equivalent to consensus
- [[consensus]] — agreement problem; FLP impossibility; Paxos/Raft/Zab
- [[two-phase-commit]] — distributed atomic commit; coordinator failure and blocking
- [[distributed-transactions]] — XA, database-internal vs heterogeneous, operational problems
- [[cap-theorem]] — linearizability vs availability during partitions
- [[state-machine-replication]] — deterministic replicas, same order, same state
- [[zookeeper]] — coordination service with consensus-based primitives

## Chapter 10 concepts

Chapter 10 covers batch processing — the third type of system (alongside online services and stream processors). It traces a lineage from Unix pipes through MapReduce to modern dataflow engines, showing how the same principles (immutable inputs, no side effects, composable operators) scale from a single machine to a cluster.

- [[batch-processing]] — the three system types; Unix-to-MapReduce-to-dataflow lineage
- [[unix-philosophy]] — do one thing well; uniform interface; separation of logic and wiring
- [[mapreduce]] — map, sort, reduce; distributed execution; fault tolerance; limitations
- [[distributed-filesystems]] — HDFS architecture; NameNode; replication; data locality
- [[sort-merge-joins]] — reduce-side joins; shuffle by key; skew handling
- [[map-side-joins]] — broadcast, partitioned, and merge join variants
- [[dataflow-engines]] — Spark/Tez/Flink; flexible DAGs; pipelining; RDD lineage
- [[materialization-of-intermediate-state]] — why MapReduce's full materialization is expensive
- [[batch-workflow-outputs]] — search indexes, key-value stores, immutable inputs philosophy
- [[hadoop-vs-mpp-databases]] — schema-on-read vs modeling; processing diversity; fault tolerance
- [[graph-batch-processing]] — Pregel/BSP; vertex-centric message passing

## Chapter 11 concepts

Chapter 11 covers stream processing — treating data as unbounded, continuously arriving events rather than fixed-size batches. It traces transport mechanisms from direct messaging through traditional message brokers to log-based brokers (Kafka), then covers three sources of streams (user activity, sensor data, and derived streams via CDC and event sourcing), and finally addresses stream processing patterns (joins, windowing) and fault tolerance.

- [[stream-processing]] — hub page: bounded vs unbounded data, core concepts, processing patterns
- [[event-streams]] — what events are; producers, consumers, topics; delivery mechanisms
- [[log-based-message-brokers]] — Kafka/Kinesis: partitioned append-only logs with consumer offsets
- [[change-data-capture]] — making one database the leader for all derived systems via binlog/WAL parsing
- [[event-sourcing]] — storing application-level intent events; deriving state; CQRS
- [[stream-joins]] — three join types: stream-stream, stream-table, table-table
- [[windowing]] — event time vs processing time; tumbling, hopping, sliding, session windows
- [[stream-processing-fault-tolerance]] — microbatching, checkpointing, idempotent writes, atomic commits

## Chapter 12 concepts

Chapter 12 synthesizes the book's themes into a vision for the future of data systems. It argues for composing specialized tools via derived data pipelines rather than relying on monolithic databases, and pushes correctness guarantees to the application level via end-to-end arguments.

- [[data-integration]] — making data available in the right form across multiple specialized systems
- [[unbundling-databases]] — decomposing database features into composable systems connected by event logs
- [[lambda-architecture]] — running batch and stream in parallel; problems and successors
- [[derived-data]] — data created by transforming a system of record; write path vs read path
- [[end-to-end-argument]] — infrastructure guarantees are insufficient; application-level operation IDs needed
- [[exactly-once-semantics]] — effectively-once via idempotence and end-to-end operation identifiers
- [[timeliness-and-integrity]] — two requirements conflated under "consistency"; decoupling them
- [[coordination-avoidance]] — maintaining integrity without synchronous coordination
- [[data-ethics]] — predictive analytics bias, surveillance, privacy, consent, engineer responsibility

## Related pages

- [[reliability]]
- [[scalability]]
- [[maintainability]]
- [[data-models]]
- [[storage-engines]]
- [[backward-forward-compatibility]]
- [[encoding-formats]]
