# Wiki Log

Append-only record of all operations.

---

## 2026-04-15 — Initial ingest: DDIA Chapter 1

**Source**: `raw/designing-data-intensive-applications/chapter-01-reliable-scalable-and-maintainable-applications.md`

**Pages created**:
- `designing-data-intensive-applications.md` — source summary with ingestion status table
- `reliability.md` — fault vs failure distinction, hardware/software/human faults, chaos engineering
- `scalability.md` — load parameters, fan-out, performance metrics, scaling strategies
- `maintainability.md` — operability, simplicity, evolvability
- `fault-tolerance.md` — hardware redundancy, chaos engineering, systematic vs random faults
- `load-parameters.md` — what load parameters are, fan-out, Twitter example
- `response-time-percentiles.md` — mean vs percentiles, tail latencies, amplification, head-of-line blocking, SLOs/SLAs
- `scaling-approaches.md` — vertical vs horizontal, elastic vs manual, stateless vs stateful
- `accidental-complexity.md` — Moseley & Marks definition, abstraction as the cure

**Infrastructure created**:
- `index.md` — table of contents
- `log.md` — this file

---

## 2026-04-15 — Ingest: DDIA Chapter 2

**Source**: `raw/designing-data-intensive-applications/chapter-02-data-models-and-query-languages.md`

**Pages created**:
- `data-models.md` — layered abstraction concept; overview of the three dominant models and their convergence
- `relational-model.md` — SQL, tables, joins, Edgar Codd, history, query optimizer as the key insight
- `document-model.md` — JSON documents, schema flexibility, data locality, one-to-many trees, limits with many-to-many
- `graph-data-models.md` — property graphs (Neo4j/Cypher), triple-stores (RDF/SPARQL), Datalog foundations, contrast with CODASYL
- `nosql.md` — the movement's driving forces, polyglot persistence, what it didn't replace
- `object-relational-mismatch.md` — impedance mismatch, ORMs, the document model as partial solution
- `normalization.md` — IDs vs duplicated text, update consistency, join trade-off, denormalization
- `schema-on-read-vs-write.md` — static vs dynamic type-checking analogy, schema migration comparison, when each is right
- `declarative-vs-imperative-queries.md` — SQL vs imperative, CSS parallel, query optimizer, parallelism, MapReduce as hybrid
- `data-locality.md` — document storage locality, read vs write trade-offs, locality in non-document systems

**Pages updated**:
- `designing-data-intensive-applications.md` — chapter 2 marked ingested, chapter 2 concepts section added
- `index.md` — two new sections: Data models and Data modeling concepts

---

## 2026-04-15 — Ingest: DDIA Chapter 3

**Source**: `raw/designing-data-intensive-applications/chapter-03-storage-and-retrieval.md`

**Pages created**:
- `storage-engines.md` — two storage engine families (log-structured vs update-in-place) and the OLTP/OLAP split
- `indexes.md` — index concept, read/write tradeoff, clustered/covering/multi-column/fuzzy index types
- `hash-indexes.md` — append-only log + in-memory hash map (Bitcask), segment compaction, why append-only wins
- `sstables-and-lsm-trees.md` — SSTable format, memtable, LSM-tree algorithm, compaction strategies, Bloom filters
- `b-trees.md` — fixed-size pages, WAL, branching factor, B-tree vs LSM-tree comparison
- `write-amplification.md` — definition, sources in B-trees and LSM-trees, SSD impact
- `oltp-vs-olap.md` — access pattern comparison table, why separate systems emerged
- `data-warehousing.md` — ETL, star schema, snowflake schema, fact tables, dimension tables
- `column-oriented-storage.md` — column storage, bitmap/run-length compression, vectorized processing, sort order, materialized views, OLAP cubes

**Pages updated**:
- `designing-data-intensive-applications.md` — chapter 3 marked ingested, chapter 3 concepts section added
- `index.md` — two new sections: Storage engines and Analytics and warehousing

---

## 2026-04-15 — Ingest: DDIA Chapter 4

**Source**: `raw/designing-data-intensive-applications/chapter-04-encoding-and-evolution.md`

**Pages created**:
- `backward-forward-compatibility.md` — the two compatibility directions, why both are required, rolling upgrades as motivation
- `encoding-formats.md` — three categories of encoding; language-specific (avoid), textual (JSON/XML/CSV), binary schema-driven (Thrift/Protobuf/Avro)
- `schema-evolution.md` — field tags (Thrift/Protobuf), Avro writer's/reader's schema resolution, rules for adding/removing fields
- `avro.md` — no field tags; schema resolved by field name at read time; dynamically generated schemas; where writer's schema is transmitted
- `data-outlives-code.md` — database records encoded under old schemas persist long after code is replaced; the re-write problem; schema evolution in DBs
- `rpc.md` — the leaky RPC abstraction; 6 ways networks differ from local calls; REST vs SOAP; modern RPC frameworks; compatibility rules
- `message-brokers.md` — async message passing advantages; actor model; distributed actor frameworks (Akka, Orleans, Erlang OTP)

**Pages updated**:
- `designing-data-intensive-applications.md` — chapter 4 marked ingested, chapter 4 concepts section added
- `index.md` — two new sections: Encoding and compatibility, Service communication

---

## 2026-04-15 — Ingest: DDIA Chapter 5

**Source**: `raw/designing-data-intensive-applications/chapter-05-replication.md`

**Pages created**:
- `replication.md` — hub page: why replicate, three architectures, sync vs async tension, consistency guarantees
- `leader-based-replication.md` — single-leader mechanics, sync vs async, WAL/statement/row-based/trigger replication methods, follower setup
- `failover.md` — promoting a new leader, split brain, lost writes, GitHub incident, why teams prefer manual failover
- `replication-lag.md` — async lag problem, three anomalies (stale reads, time going backward, causal violations), monitoring
- `read-after-write-consistency.md` — guarantee definition, implementation strategies (leader routing, time-based, client timestamps), cross-device complexity
- `monotonic-reads.md` — guarantee definition, sticky replica implementation, relationship to other consistency properties
- `consistent-prefix-reads.md` — causality anomaly, partitioned database problem, causal dependency tracking solutions
- `eventual-consistency.md` — the vague guarantee, what it doesn't provide, operability problem, transactions as the honest alternative
- `multi-leader-replication.md` — use cases (multi-datacenter, offline-first, collaborative editing), topologies, causality in all-to-all
- `write-conflicts.md` — conflict detection, LWW (dangerous), merge strategies, CRDTs, operational transformation, tombstones, custom resolution
- `leaderless-replication.md` — Dynamo-style, read repair, anti-entropy, sloppy quorums, hinted handoff, multi-datacenter
- `quorums.md` — w+r>n math, fault tolerance, sloppy quorums, the many edge cases that undermine quorum guarantees
- `version-vectors.md` — happens-before relationship, concurrency definition, single-replica version numbers, multi-replica version vectors, sibling merging

**Pages updated**:
- `designing-data-intensive-applications.md` — chapter 5 marked ingested, chapter 5 concepts section added
- `index.md` — new section: Replication (13 pages)

---

## 2026-04-15 — Ingest: DDIA Chapter 6

**Source**: `raw/designing-data-intensive-applications/chapter-06-partitioning.md`

**Pages created**:
- `partitioning.md` — what partitioning/sharding is, terminology across systems, relationship to replication
- `partitioning-strategies.md` — key-range vs hash partitioning trade-offs, compound key strategies
- `hot-spots.md` — skewed load, causes (key distribution, celebrity keys), mitigation approaches
- `consistent-hashing.md` — CDN origin, why the term is misleading for databases, hash partitioning preferred
- `partitioning-secondary-indexes.md` — document-partitioned (local) with scatter/gather vs term-partitioned (global) with async writes
- `rebalancing-partitions.md` — fixed partition count, dynamic splitting/merging, proportional to nodes, automatic vs manual
- `request-routing.md` — node-forwarding, routing tiers, client-side awareness, ZooKeeper coordination, gossip protocols

**Pages updated**:
- `designing-data-intensive-applications.md` — chapter 6 marked ingested, chapter 6 concepts section added
- `index.md` — new section: Partitioning (7 pages)

---

## 2026-04-15 — Ingest: DDIA Chapter 7

**Source**: `raw/designing-data-intensive-applications/chapter-07-transactions.md`

**Pages created**:
- `transactions.md` — the transaction abstraction, purpose, single vs multi-object, error handling philosophy
- `acid.md` — Atomicity, Consistency, Isolation, Durability; how each property's meaning varies in practice
- `isolation-levels.md` — spectrum from weak to strong; what each level prevents
- `read-committed.md` — prevents dirty reads/writes; row-level locks and MVCC implementation
- `snapshot-isolation.md` — MVCC-based consistent snapshots; valuable for backups/analytics; vulnerable to write skew
- `mvcc.md` — multi-version concurrency control: multiple committed versions for lock-free reads
- `dirty-reads-and-dirty-writes.md` — two race conditions involving uncommitted data
- `read-skew.md` — nonrepeatable read anomaly; solved by snapshot isolation
- `lost-updates.md` — concurrent read-modify-write overwriting; atomic ops, explicit locking, automatic detection, CAS
- `write-skew.md` — cross-object invariant violation; requires serializable isolation
- `phantoms.md` — search results changed by concurrent writes; predicate locks, index-range locks, SSI
- `serializability.md` — strongest isolation; three implementation approaches compared
- `two-phase-locking.md` — pessimistic serializability; shared/exclusive locks; readers and writers block each other
- `serializable-snapshot-isolation.md` — optimistic 2008 algorithm; conflict detection at commit time; PostgreSQL and FoundationDB
- `actual-serial-execution.md` — single-threaded execution; stored procedures; feasible when data fits in memory

**Pages updated**:
- `designing-data-intensive-applications.md` — chapter 7 marked ingested, chapter 7 concepts section added
- `index.md` — new section: Transactions (15 pages)

---

## 2026-04-15 — Ingest: DDIA Chapter 8

**Source**: `raw/designing-data-intensive-applications/chapter-08-the-trouble-with-distributed-systems.md`

**Pages created**:
- `partial-failures.md` — the defining characteristic of distributed systems; cloud vs supercomputing philosophies
- `unreliable-networks.md` — shared-nothing asynchronous networks; no delivery guarantees; queueing and congestion
- `network-faults.md` — practical prevalence of network problems; partitions; fault detection mechanisms
- `timeouts.md` — the only sure fault detection mechanism; long-vs-short dilemma; adaptive timeouts; Phi Accrual
- `unreliable-clocks.md` — time-of-day vs monotonic; clock drift; LWW data loss; confidence intervals; TrueTime/Spanner
- `clock-synchronization.md` — NTP mechanics; GPS/PTP/atomic clocks; Google TrueTime API; monitoring
- `process-pauses.md` — GC, VM suspension, disk I/O, context switching; lease expiry; real-time systems
- `truth-and-leadership-in-distributed-systems.md` — why a node cannot trust its own judgment; quorum-based truth
- `fencing-tokens.md` — monotonically increasing tokens; server-side enforcement; ZooKeeper zxid/cversion
- `byzantine-faults.md` — nodes that lie; Byzantine Generals Problem; BFT relevance; weak forms of lying
- `system-models.md` — timing models (sync/partial/async); failure models (crash-stop/recovery/Byzantine)
- `safety-and-liveness.md` — two property categories; safety must always hold; liveness allows caveats

**Pages updated**:
- `fault-tolerance.md` — added sections on building reliable systems from unreliable components and distributed fault tolerance
- `failover.md` — added failure detection challenges from Chapter 8 (unreliable networks, process pauses, adaptive timeouts)
- `quorums.md` — added section on quorums for decision-making beyond read/write overlap
- `eventual-consistency.md` — added section classifying eventual consistency as a liveness property
- `designing-data-intensive-applications.md` — chapter 8 marked ingested, chapter 8 concepts section added
- `index.md` — new section: Distributed systems challenges (12 pages)

---

## 2026-04-15 — Ingest: DDIA Chapter 9

**Source**: `raw/designing-data-intensive-applications/chapter-09-consistency-and-consensus.md`

**Pages created**:
- `linearizability.md` — strongest single-object consistency; recency guarantee; relationship to serializability; cost
- `causal-consistency.md` — cause-and-effect ordering; partial vs total order; strongest without coordination
- `lamport-timestamps.md` — piggyback-maximum mechanism; comparison with version vectors; limitations
- `total-order-broadcast.md` — reliable + totally ordered delivery; equivalence with consensus; state machine replication
- `consensus.md` — formal properties; FLP impossibility; Paxos/Raft/Zab; epoch numbering; equivalent problems
- `two-phase-commit.md` — distributed atomic commit; system of promises; coordinator failure; blocking; 3PC limitations
- `cap-theorem.md` — linearizability vs availability during partitions; historically important but practically limited
- `distributed-transactions.md` — database-internal vs heterogeneous; XA; exactly-once messaging; operational problems
- `state-machine-replication.md` — deterministic replicas, same operations, same order, same state
- `zookeeper.md` — consensus primitives; linearizable ops; total ordering; ephemeral nodes; leader election

**Pages updated**:
- `eventual-consistency.md` — added convergence as alternative name; consistency hierarchy positioning
- `serializability.md` — added serializability vs linearizability distinction; strict serializability
- `quorums.md` — added quorums and linearizability; quorums in consensus algorithms
- `failover.md` — added consensus as the real solution for leader election
- `leader-based-replication.md` — added linearizability and consensus section
- `leaderless-replication.md` — added "linearizability: probably not" section
- `multi-leader-replication.md` — added "not linearizable" section; CAP advantage
- `version-vectors.md` — added version vectors vs Lamport timestamps comparison
- `fault-tolerance.md` — added consensus as foundation of fault-tolerant coordination
- `replication.md` — updated consistency guarantees with linearizability/consensus links
- `snapshot-isolation.md` — added snapshot isolation and linearizability section
- `transactions.md` — added distributed transactions section
- `consistent-prefix-reads.md` — added causal-consistency to related pages
- `designing-data-intensive-applications.md` — chapter 9 marked ingested, chapter 9 concepts section added
- `index.md` — new section: Consistency and consensus (10 pages)

---

## 2026-04-15 — Ingest: DDIA Chapter 10

**Source**: `raw/designing-data-intensive-applications/chapter-10-batch-processing.md`

**Pages created**:
- `batch-processing.md` — three system types (online, batch, stream); Unix-to-MapReduce-to-dataflow lineage
- `unix-philosophy.md` — four principles: do one thing well, uniform interface, separation of logic/wiring, transparency
- `mapreduce.md` — map, sort, reduce; distributed execution; shuffle; fault tolerance; limitations
- `distributed-filesystems.md` — HDFS architecture; NameNode; replication/erasure coding; data locality
- `sort-merge-joins.md` — reduce-side joins; secondary sort; sessionization; skew handling (Pig, Crunch, Hive)
- `map-side-joins.md` — broadcast hash join, partitioned hash join, map-side merge join
- `dataflow-engines.md` — Spark/Tez/Flink; flexible DAGs; pipelining; RDD lineage; high-level APIs
- `materialization-of-intermediate-state.md` — MapReduce's costly full materialization; dataflow engine improvements
- `batch-workflow-outputs.md` — search indexes, key-value stores, immutable inputs / replaceable outputs
- `hadoop-vs-mpp-databases.md` — storage diversity, processing diversity, fault tolerance design; convergence trend
- `graph-batch-processing.md` — Pregel/BSP; vertex-centric message passing; checkpointing; partitioning challenges

**Pages updated**:
- `data-warehousing.md` — added Hadoop and data lake section; sushi principle
- `declarative-vs-imperative-queries.md` — added batch processing evolution from imperative to declarative
- `column-oriented-storage.md` — added column storage in batch processing (Parquet, vectorized execution)
- `partitioning.md` — added partitioning in batch processing (MapReduce input/output partitioning)
- `graph-data-models.md` — added batch processing on graphs section (Pregel/BSP)
- `encoding-formats.md` — added encoding formats in batch processing (Avro, Parquet)
- `replication.md` — added replication in distributed filesystems (HDFS blocks)
- `sstables-and-lsm-trees.md` — added SSTables in batch processing (shuffle uses same technique)
- `designing-data-intensive-applications.md` — chapter 10 marked ingested, chapter 10 concepts section added
- `index.md` — new section: Batch processing (11 pages)

---

## 2026-04-15 — Re-ingest: DDIA Chapter 6

**Source**: `raw/designing-data-intensive-applications/chapter-06-partitioning.md`

**Pages created**:
- `service-discovery.md` — general problem of locating services across redundant machines

**Pages updated**:
- `partitioning.md` — added terminology table, parallel query execution (MPP), cross-partition operations
- `partitioning-strategies.md` — added "why not random assignment?" section, encyclopedia illustration, concatenated index usage
- `hot-spots.md` — added structural mitigation via Cassandra compound key approach
- `consistent-hashing.md` — added randomization unfair splits detail, Cassandra 3.0 improvements
- `partitioning-secondary-indexes.md` — added search server context, DIY index caution, term etymology, Oracle choice
- `rebalancing-partitions.md` — added Cassandra randomization detail, newer hash function approaches
- `request-routing.md` — added agreement challenge subsection, consensus link
- `replication.md` — added relationship to partitioning section
- `indexes.md` — added indexes and partitioning section
- `b-trees.md` — added B-tree splitting in other contexts section
- `zookeeper.md` — added partition-to-node tracking section
- `scalability.md` — added partitioning and replication to related pages
- `designing-data-intensive-applications.md` — chapter 6 marked re-ingested
- `index.md` — added service-discovery to Partitioning section

---

## 2026-04-15 — Ingest: DDIA Chapter 11

**Source**: `raw/designing-data-intensive-applications/chapter-11-stream-processing.md`

**Pages created**:
- `stream-processing.md` — hub page: bounded vs unbounded data, core concepts, processing patterns
- `event-streams.md` — events, producers/consumers, delivery mechanisms, fan-out, immutability
- `log-based-message-brokers.md` — Kafka/Kinesis: partitioned append-only logs, consumer offsets, replay
- `change-data-capture.md` — CDC makes one DB the leader; binlog parsing, initial snapshots, log compaction
- `event-sourcing.md` — application-level intent events, deriving state, CQRS, commands vs events
- `stream-joins.md` — stream-stream, stream-table, table-table joins; time-dependence
- `windowing.md` — event time vs processing time, tumbling/hopping/sliding/session windows
- `stream-processing-fault-tolerance.md` — microbatching, checkpointing, idempotent writes, atomic commits

**Pages updated**:
- `message-brokers.md` — added brokers vs databases comparison, consumer patterns, acknowledgments/redelivery
- `batch-processing.md` — added relationship to stream processing section
- `replication.md` — added replication logs as event streams section
- `fault-tolerance.md` — added fault tolerance in stream processing section
- `partitioning.md` — added partitioning in stream processing section
- `state-machine-replication.md` — added connection to event streams section
- `designing-data-intensive-applications.md` — chapter 11 marked ingested, chapter 11 concepts added
- `index.md` — new section: Stream processing (8 pages)

---

## 2026-04-15 — Ingest: DDIA Chapter 12

**Source**: `raw/designing-data-intensive-applications/chapter-12-the-future-of-data-systems.md`

**Pages created**:
- `data-integration.md` — combining specialized tools via batch/stream derived data pipelines
- `unbundling-databases.md` — decomposing database features into composable event-log-connected systems
- `lambda-architecture.md` — running batch and stream in parallel; problems and successors
- `derived-data.md` — data from transforming a system of record; write path vs read path
- `end-to-end-argument.md` — Saltzer/Reed/Clark principle: application-level operation IDs for correctness
- `exactly-once-semantics.md` — effectively-once via idempotence and end-to-end identifiers
- `timeliness-and-integrity.md` — two requirements conflated under "consistency"; decoupling them
- `coordination-avoidance.md` — maintaining integrity without synchronous coordination
- `data-ethics.md` — predictive analytics bias, surveillance, privacy, consent, engineer responsibility

**Pages updated**:
- `batch-processing.md` — added reprocessing for application evolution; unifying batch and stream
- `dataflow-engines.md` — added unifying batch and stream processing section (Beam, Flink)
- `distributed-transactions.md` — added log-based derived data as alternative section
- `transactions.md` — added end-to-end argument and timeliness vs integrity sections
- `total-order-broadcast.md` — added limits of total ordering at scale; uniqueness via log-based messaging
- `consensus.md` — added consensus, uniqueness, and coordination avoidance; scaling limitations
- `linearizability.md` — added linearizability as timeliness section
- `eventual-consistency.md` — added eventual consistency as timeliness violation section
- `fault-tolerance.md` — added trust-but-verify auditing section (Merkle trees, cryptographic integrity)
- `stream-processing.md` — added dataflow application design section
- `causal-consistency.md` — added capturing causality in practice section
- `batch-workflow-outputs.md` — added write path and read path section
- `designing-data-intensive-applications.md` — chapter 12 marked ingested, chapter 12 concepts added
- `index.md` — new section: Future of data systems (9 pages)

---

## 2026-04-16 — Ingest: Monolith to Microservices Chapter 1

**Source**: `raw/monolith-to-microservices/chapter-01-just-enough-microservices.md`

**Pages created**:
- `monolith-to-microservices.md` — source summary with ingestion status table; Newman's evolutionary stance
- `microservices.md` — definition, three defining properties, advantages, costs, size, history, SOA relationship
- `monolith.md` — three variants (single-process, modular, distributed, black-box); challenges and advantages
- `independent-deployability.md` — the central discipline; Newman's "if you take only one thing"
- `bounded-context.md` — DDD organizational boundary; coarse-grained service starting point
- `aggregate.md` — DDD domain entity with state-machine life cycle; aggregate-vs-context decomposition
- `domain-driven-design.md` — umbrella page covering Evans's discipline and the two ideas Newman highlights
- `information-hiding.md` — Parnas's 1971 principle; outside-in interface design; encapsulation contrast
- `coupling.md` — Newman's four-type taxonomy: implementation, temporal, deployment, domain
- `cohesion.md` — "code that changes together, stays together"; business vs technology cohesion
- `conways-law.md` — why three-tier architectures are everywhere; service ownership and the IT/business divide

**Pages updated**:
- `index.md` — added Monolith to Microservices to Source summaries; added three new sections (Microservices fundamentals, Domain-driven design, Coupling and cohesion)

---

## 2026-04-16 — Ingest: Monolith to Microservices Chapter 2

**Source**: `raw/monolith-to-microservices/chapter-02-planning-a-migration.md`

**Pages created**:
- `why-microservices.md` — the three-question test; legitimate motivations (autonomy, time to market, scaling, robustness, more developers, new tech) with cheaper alternatives; reuse as a bad goal; the slider exercise for trade-offs
- `when-microservices-are-a-bad-idea.md` — unclear domain (SnapCI story); true startups vs scale-ups; customer-installed software; no clear reason
- `modular-monolith.md` — Newman's repeatedly-cited cheaper alternative; where it stops short; brownfield as easier than greenfield
- `incremental-migration.md` — chip away one service at a time; production is what counts; "the only thing you're guaranteed of is a big bang"
- `reversible-vs-irreversible-decisions.md` — Bezos's two-way / one-way doors as a spectrum; don't deliberate on cheap decisions or rush expensive ones
- `cost-of-change.md` — whiteboard as the cheapest place; database splits as the most expensive; ordering of migration work
- `extraction-prioritization.md` — two-axis effort/benefit model; using domain dependencies as effort proxy; replan as you learn
- `event-storming.md` — Brandolini's bottom-up technique; logical events not implementation events; shared understanding as the real output
- `team-autonomy.md` — Gore/Timpsons/two-pizza examples; cheaper alternatives that don't require microservices
- `robustness-vs-resilience.md` — Woods/Allspaw distinction; microservices grant neither for free; British Airways 2017 outage example
- `kotters-change-model.md` — eight-step process applied to microservice adoption; the unnamed CEO counter-example
- `reorganizing-teams.md` — competency silos to product teams; don't copy Spotify; as-is/to-be mapping; the pager-flip warning
- `skills-self-assessment.md` — private 1-5 ratings; anonymised aggregate; The Guardian project example; hiring as alternative to growing
- `measuring-microservice-transition.md` — checkpoints; quantitative gotchas (gaming, regression); qualitative feedback; sunk cost / Concorde fallacy

**Pages updated**:
- `monolith-to-microservices.md` — Chapter 2 marked ingested; full Chapter 2 concepts section added
- `monolith.md` — added "When the monolith is the right choice" and "Brownfield is easier than greenfield" sections; sources updated
- `microservices.md` — added "Microservices are a means, not an end" section linking to Ch 2 pages; sources updated
- `domain-driven-design.md` — added "Domain modelling for migration prioritisation" and "How much modelling is enough?" sections; sources updated
- `bounded-context.md` — added "Bounded contexts as units of prioritization" section; sources updated
- `conways-law.md` — added "The reverse pressure: reorganising teams" section; sources updated
- `index.md` — added `modular-monolith` to Microservices fundamentals; added two new sections (Microservice migration with 9 pages, Team and organization with 4 pages)

---

## 2026-04-16 — Ingest: Monolith to Microservices Chapter 3

**Source**: `raw/monolith-to-microservices/chapter-03-splitting-the-monolith.md`

**Pages created**:
- `strangler-fig-pattern.md` — Newman's signature migration pattern; HTTP reverse proxy, FTP, message interception examples; protocol translation cautions
- `branch-by-abstraction.md` — five-step in-place migration; alternative when strangler fig can't reach; verify-branch-by-abstraction variant
- `parallel-run-pattern.md` — call both implementations and compare; credit derivative pricing example; Spies; GitHub Scientist; N-version programming relative
- `decorating-collaborator-pattern.md` — proxy triggers new-service calls based on monolith outcome; the information-availability constraint
- `ui-composition.md` — page composition (Guardian), widget composition (Orbitz), micro frontends, mobile considerations (Spotify)
- `migration-pattern-selection.md` — change-the-monolith-or-not; copy vs reimplement; pattern-fit table; don't-change-behaviour-during-migration
- `seams-and-legacy-code.md` — Michael Feathers's seam concept; the path from seams to modules to services
- `deployment-vs-release.md` — the foundational separation that all patterns rely on
- `feature-toggle.md` — runtime switches for cutover; toggle hygiene; Pete Hodgson reference
- `progressive-delivery.md` — James Governor's umbrella term covering canary, dark launch, parallel run, toggles
- `service-mesh.md` — per-service local proxies via sidecar + control plane; Square/Envoy example; Newman's tooling-stability caution

**Pages updated**:
- `change-data-capture.md` — added "CDC as a microservice migration pattern" section with loyalty cards example, implementation options, and selection guidance; sources updated
- `incremental-migration.md` — connected to all Chapter 3 patterns; added "Don't change behaviour during migration" section; sources updated
- `monolith-to-microservices.md` — Chapter 3 marked ingested; full Chapter 3 concepts section added
- `index.md` — added new section "Migration patterns" (11 pages)

---

## 2026-04-16 — Ingest: Monolith to Microservices Chapter 4

**Source**: `raw/monolith-to-microservices/chapter-04-decomposing-the-database.md`

**Pages created**:
- `database-decomposition.md` — hub page for chapter; pattern catalogue and sequencing guidance
- `shared-database-antipattern.md` — what's wrong, two acceptable cases (static reference data, deliberate public DB), credit-derivative anecdote
- `database-view-pattern.md` — read-only projection; materialized views; limitations and ownership
- `database-wrapping-service.md` — thin service in front of schema; Australian bank entitlements story
- `database-as-a-service-interface.md` — generalised reporting database; mapping engine; CDC vs batch
- `aggregate-exposing-monolith.md` — expose monolith aggregate via API for new service; pathway to next service
- `change-data-ownership.md` — move data into new service; invert dependency; FKs and transactions as the hard part
- `synchronize-data-in-application.md` — three-step Trifork pattern for Danish medical records
- `tracer-write.md` — incremental source-of-truth migration; Square Fulfillments service example
- `split-the-database-first.md` — schema-first vs code-first vs both-at-once; physical vs logical separation; Newman's hot take
- `repository-per-bounded-context.md` — factor data-access code along context lines; SchemaSpy for FK visualisation
- `database-per-bounded-context.md` — separate schemas inside modular monolith; ThoughtWorks Revenue example
- `monolith-as-data-access-layer.md` — expose API on monolith instead of pulling its data; JustSocial's pattern
- `multischema-storage.md` — new data in new schema while still reading old data from monolith
- `split-table-pattern.md` — separate Item/Customer.Status table along service boundaries
- `move-foreign-key-to-code.md` — Albums/Ledger join becomes service call; handle deletion gracefully (410 Gone); aggregate warning
- `shared-static-data.md` — four patterns for country codes: duplicate, dedicated schema, library, service; Stitch Fix and South Sudan examples
- `saga.md` — Garcia-Molina/Salem 1987; orchestrated vs choreographed; backward/forward recovery; semantic rollbacks; correlation IDs; reordering steps to reduce rollbacks; Pat Helland on distributed transactions

**Pages updated**:
- `two-phase-commit.md` — added Newman's microservice perspective; "Just Say No" framing; sources updated
- `distributed-transactions.md` — added saga as the alternative; Pat Helland airplane quote; Newman's three options; sources updated
- `transactions.md` — added section on losing transactions when splitting a database; sources updated
- `change-data-capture.md` — added "CDC's role in database decomposition" covering mapping engine, catch-up sync, tracer-write sync; sources updated
- `event-sourcing.md` — added section on event sourcing as an alternative to soft deletes (Newman's footnote in move-foreign-key-to-code); sources updated
- `eventual-consistency.md` — added section framing eventual consistency in microservice migrations; reconciliation as a practice; sources updated
- `information-hiding.md` — added cross-references to database-decomposition patterns; sources updated
- `monolith-to-microservices.md` — Chapter 4 marked ingested; full Chapter 4 concepts section added
- `index.md` — added new section "Database decomposition" (18 pages)

---

## 2026-04-16 — Ingest: Monolith to Microservices Chapter 5

**Source**: `raw/monolith-to-microservices/chapter-05-growing-pains.md`

**Pages created**:
- `code-ownership-models.md` — strong/weak/collective from Martin Fowler; the "colander architecture" anecdote; collective stops working past ~20 devs; strong "almost universal" past 100
- `breaking-changes.md` — eliminate accidental, think twice about deliberate, give consumers time to migrate; structural vs semantic; coexisting versions vs one-service-two-contracts
- `consumer-driven-contracts.md` — Pact-style consumer-written tests; replace cross-service test cases; "poorly underused practice for solving a really difficult problem"
- `cross-service-analytics.md` — Chapter 5 framing of [[database-as-a-service-interface]]; push from microservices into a dedicated analytics database
- `monitoring-and-observability.md` — Honest Status Page murder-mystery quote; from known-causes monitoring to open-ended observability
- `log-aggregation.md` — Newman's "do this first" recommendation; ELK, Humio; organisational litmus test
- `correlation-ids.md` — single ID propagated through call chains; generated at edge; prerequisite for distributed tracing
- `distributed-tracing.md` — Jaeger; latency attribution where logs can't help; service mesh inbound/outbound for free
- `synthetic-transactions.md` — Atomist onboarding example with Sylvain Hellegouarch's enrolment script; 200-washing-machines warning
- `local-developer-experience.md` — JVM laptop ceiling; stubbing, remote, hybrid, Telepresence, Azure Functions; ongoing investment
- `desired-state-management.md` — declarative spec + continuous reconciliation; Kubernetes/OpenShift; serverless-first on cloud
- `running-too-many-things.md` — operational counterpart; Newman's "don't adopt because everyone else is" warning
- `end-to-end-testing.md` — large suites become slow/flaky/ambiguous; four-part response (limit scope, CDCs, automated remediation, refine cycles)
- `global-vs-local-optimization.md` — three-databases example; cross-cutting groups; Monzo's free-form proposals; refuses to prescribe a balance
- `robustness-and-resiliency-at-scale.md` — Newman's two questions per call; circuit breakers, isolation, time-outs; document what you learn; pointer to Release It!
- `orphaned-services.md` — walled-up-servers anecdote; FT's Biz Ops and System Operability Score; service registries; collective ownership as untested mitigation

**Pages updated**:
- `independent-deployability.md` — added "What threatens independent deployability at scale" section linking to Ch 5 pain points; sources updated
- `microservices.md` — added "Growing pains as you scale" section indexing all Ch 5 pages; sources updated
- `progressive-delivery.md` — added automated release remediation section (Spinnaker); sources updated
- `robustness-vs-resilience.md` — added "Operationalising the distinction at scale" section; sources updated
- `team-autonomy.md` — added "The flip side: global vs local optimisation"; sources updated
- `database-as-a-service-interface.md` — added Chapter 5 framing as a pain remedy; sources updated
- `monolith-to-microservices.md` — Chapter 5 marked ingested; full Chapter 5 concepts section added
- `index.md` — added two new sections (Microservices at scale with 9 pages, Observability with 5 pages); added two pages to Team and organization

---

## 2026-04-16 — Ingest: Designing Distributed Systems — setup

**Source**: `raw/designing-distributed-systems/`

**Pages created**:
- `designing-distributed-systems.md` — source summary with ingestion status table for Brendan Burns's pattern catalogue

**Pages updated**:
- `index.md` — added Designing Distributed Systems to Source summaries

**Notes**: Chapter 1 (Introduction) and Chapter 13 (Conclusion) are skipped per the ingest instruction to focus on main-content chapters only. Chapters 2–12 are the substantive pattern chapters.

---

## 2026-04-16 — Ingest: Designing Distributed Systems Chapter 2

**Source**: `raw/designing-distributed-systems/chapter-02-the-sidecar-pattern.md`

**Pages created**:
- `sidecar-pattern.md` — the two-container single-node pattern; four worked examples (HTTPS, config sync, `topz` introspection, git-based PaaS); two motivations (legacy modernization and modular reuse); relationship to service-mesh, information-hiding, coupling
- `pod.md` — atomic container group with shared namespaces (network, filesystem, PID); why atomic coscheduling matters; pod as the unit of sidecar injection
- `modular-reusable-containers.md` — Burns's three-part design discipline: parameterize via env vars, define the full API surface (including subtle breaking changes like unit changes), document via Dockerfile directives (EXPOSE, ENV, LABEL) and the Label Schema project
- `legacy-modernization.md` — using sidecars to augment legacy apps without source changes; relationship to Newman's strangler-fig and related migration patterns; limits of the approach

**Pages updated**:
- `designing-distributed-systems.md` — Chapter 2 marked ingested; Chapter 2 concepts section added summarising thesis and listing new pages
- `service-mesh.md` — added "The sidecar as underlying primitive" section framing a service mesh as a fleet-wide sidecar deployment; sources updated
- `information-hiding.md` — added "Information hiding at the deployment layer" section connecting Burns's sidecar pattern to Parnas's principle; sources updated
- `index.md` — added new section "Single-node container patterns" with four new pages

---

## 2026-04-16 — Ingest: Designing Distributed Systems Chapter 3

**Source**: `raw/designing-distributed-systems/chapter-03-ambassadors.md`

**Pages created**:
- `ambassador-pattern.md` — the core pattern; a coresident container that brokers the application's outbound connections; three canonical uses (sharding, service brokering, request splitting); the client-side ambassador vs server-side proxy-tier trade-off; explicit comparison to sidecar-pattern
- `client-side-sharding.md` — using an ambassador to proxy to a sharded backend; twemproxy + Redis + ketama worked example; mapped onto DDIA's request-routing / client-side-awareness taxonomy
- `service-brokering.md` — ambassador as per-pod service-discovery client; MySQL-across-environments portability example; relationship to service mesh and legacy modernization
- `request-splitting.md` — ambassador for canary, dark launch, and tee / parallel-run traffic; nginx 10%-experiment worked example with ip_hash for user stickiness; client-side vs server-side proxy trade-off

**Pages updated**:
- `designing-distributed-systems.md` — Chapter 3 marked ingested; Chapter 3 concepts section added; Related pages extended
- `sidecar-pattern.md` — added "Sibling pattern: the ambassador" section distinguishing the two patterns by intent; sources updated
- `pod.md` — added ambassador-pattern to Related; sources updated
- `modular-reusable-containers.md` — summary extended to cover ambassadors; added "Applies to ambassadors too" section; sources updated
- `service-mesh.md` — added "The mesh as fleet-wide ambassador" section framing the mesh's outbound data-plane as the ambassador pattern industrialized; sources updated; Related pages extended
- `service-discovery.md` — added "Container-level implementations" section pointing to service-brokering and service-mesh; sources updated
- `request-routing.md` — extended the "client-side awareness" option to cover ambassador-container implementations; sources updated
- `consistent-hashing.md` — added "Consistent hashing in client-side sharding ambassadors" section documenting ketama + twemproxy; sources updated
- `partitioning.md` — added "Client integration via ambassadors" section; sources updated
- `parallel-run-pattern.md` — added "Teeing at the ambassador / proxy layer" section as an alternative to Scientist-style in-process libraries; sources updated
- `progressive-delivery.md` — added "Implementation via ambassadors" section; sources updated
- `index.md` — extended "Single-node container patterns" section with four new pages (ambassador-pattern, client-side-sharding, service-brokering, request-splitting)

**Notes**: No contradictions encountered. Chapter 3 framing of "client-side vs server-side proxy" maps directly onto the service-mesh-vs-shared-proxy tension already in the wiki from Newman's book, and this cross-link is now explicit in both directions. Client-side sharding is framed as a concrete implementation of the client-side-awareness routing option in DDIA's [[request-routing]] page. The ambassador pattern's request-splitting use is linked bi-directionally with [[progressive-delivery]], [[parallel-run-pattern]], and [[feature-toggle]].

---

## 2026-04-16 — Ingest: Designing Distributed Systems Chapter 4

**Source**: `raw/designing-distributed-systems/chapter-04-adapters.md`

**Pages created**:
- `adapter-pattern.md` — the core single-node pattern; a coresident container that transforms the application's outward interface to a fleet standard; full trilogy comparison with sidecar and ambassador; the heterogeneity argument; the "why not modify the application" discussion; the community-contribution closing note
- `unified-monitoring-interface.md` — adapter applied to monitoring; Redis + `oliver006/redis_exporter` + Prometheus worked example; why pull-style dovetails with the pattern
- `log-normalization.md` — adapter applied to logging; fluentd + `fluent-plugin-redis-slowlog` and `fluent-plugin-storm` worked examples; turning transient server state into queryable logs; relationship to log-aggregation and correlation-ids
- `health-check-adapter.md` — adapter applied to orchestrator health probes; the Go + MySQL worked example with full source; the modularity argument against a custom forked image; relationship to desired-state-management

**Pages updated**:
- `designing-distributed-systems.md` — Chapter 4 marked ingested; Chapter 4 concepts section added; Related pages extended; Last updated note bumped
- `sidecar-pattern.md` — "Sibling pattern: the ambassador" section generalised to "Sibling patterns: ambassador and adapter" with a three-row trilogy table; sources and Related extended
- `ambassador-pattern.md` — "Relationship to sidecars" section expanded into a three-row trilogy table; sources and Related extended
- `pod.md` — added adapter-pattern to Related; sources extended
- `modular-reusable-containers.md` — summary generalised to cover adapters; "Applies to adapters too" section added with explicit parameterize/API-surface/document guidance for adapter containers; sources and Related extended
- `monitoring-and-observability.md` — "The container-level mechanism: adapters" section added connecting Newman's observability toolbox to Burns's adapter-pattern examples; sources and Related extended
- `log-aggregation.md` — "Normalising logs before aggregation" section added framing log-normalization as the adapter-pattern answer to heterogeneous log formats; sources and Related extended
- `service-mesh.md` — "The mesh as fleet-wide adapter" section added covering the mesh's adapter-like uniform telemetry role; Related extended; sources updated
- `information-hiding.md` — deployment-layer section extended to cover adapters hiding native observability interfaces behind fleet-standard ones; sources and Related extended
- `legacy-modernization.md` — "Adapters for legacy observability" subsection added; three adapter pages added to Related; sources updated
- `index.md` — four new pages added to "Single-node container patterns" section

**Notes**: Chapter 4 completes the Part I trilogy. The trilogy table (pattern vs intent vs canonical examples) is now present on all three pattern pages with consistent phrasing. Adapters and sidecars share the "don't modify the upstream image" argument but apply it to different interface surfaces (inbound augmentation vs outward observability). The chapter's closing remark about adapters enabling community-contributed operational expertise is preserved on [[adapter-pattern]] and surfaces in [[modular-reusable-containers]]'s "Applies to adapters too" section. No contradictions with existing wiki pages were encountered.

---

## 2026-04-16 — Ingest: Designing Distributed Systems Chapter 5

**Source**: `raw/designing-distributed-systems/chapter-05-replicated-load-balanced-services.md`

**Pages created**:
- `replicated-load-balanced-service.md` — the first multi-node pattern; stateless replicas behind a load balancer; the two-replica-minimum SLA argument; composition into stacked application-layer tiers
- `health-probes.md` — the liveness vs readiness distinction (orchestrator-restart vs load-balancer-deregister); Kubernetes implementation; why you must deploy both; relation to Chapter 4's health-check adapter
- `session-tracked-services.md` — sticky sessions via IP hash inside the cluster and cookies/headers across NAT or upstream proxies; why consistent hashing is the default; the cache + session-tracking interaction
- `caching-layer.md` — Varnish as a replicated HTTP cache tier; the few-large-replicas sizing rule; why cache-as-sidecar is usually wrong; Kubernetes mechanics; IP-affinity trap
- `rate-limiting.md` — DoS defence at the edge; accidental vs malicious cases; 429 and X-RateLimit-Remaining; anonymous vs authenticated quotas; Varnish throttle module
- `ssl-termination.md` — the nginx edge tier; per-layer certificates for independent rollouts; the full nginx → Varnish → app three-tier stack; self-signed-cert caveat

**Pages updated**:
- `designing-distributed-systems.md` — Chapter 5 marked ingested; Chapter 5 concepts section added summarising the thesis and listing new pages; Related pages extended
- `scaling-approaches.md` — added paragraph framing Burns's replicated-load-balanced-service as the textbook container-level horizontal stateless scaling pattern; sources updated
- `consistent-hashing.md` — added "Consistent hashing for session affinity" section documenting the session-tracking use case and its CDN lineage; sources updated
- `sidecar-pattern.md` — added "A worked case of when not to use a sidecar" section capturing Burns's cache-tier-vs-cache-sidecar argument as a useful corrective; sources updated
- `service-mesh.md` — added "The mesh and serving-pattern cross-cutting concerns" section mapping session affinity, mTLS, rate limiting, and readiness-signal propagation onto the mesh proxy; sources updated
- `health-check-adapter.md` — added "Liveness vs readiness: which probe is this?" section framing the Chapter 4 Go/MySQL adapter as better-suited to readiness than liveness; sources updated
- `scalability.md` — added replicated-load-balanced-service to Related pages
- `fault-tolerance.md` — added replicated-load-balanced-service and health-probes to Related pages
- `index.md` — new section "Serving patterns" added below "Single-node container patterns" (6 pages)

**Notes**: Chapter 5 is the first multi-node pattern and opens Part II. The chapter mentions liveness checks only in passing ("health probes") but the distinction between liveness and readiness is substantive and load-bearing for the rest of the serving patterns, so the pair is captured on a single `health-probes.md` page with emphasis on readiness as the chapter does. The chapter's "consistent hashing minimises remapping during scaling" point for session affinity is now cross-linked bidirectionally with the existing `consistent-hashing.md` — the CDN origin story on that page and the session-tracking use case here are presented as the same property applied to different "keys." The chapter's interaction between caching tier IP-affinity and session tracking is captured on both `caching-layer.md` and `session-tracked-services.md`. No contradictions with existing wiki pages were encountered; the cache-as-sidecar anti-example is a rare explicit "don't use this pattern" moment in Burns's book and is now annotated on `sidecar-pattern.md`.

---

## 2026-04-16 — Ingest: Designing Distributed Systems Chapter 6

**Source**: `raw/designing-distributed-systems/chapter-06-sharded-services.md`

**Pages created**:
- `sharded-service-pattern.md` — the core Chapter 6 pattern; root + shards; stateful services whose state exceeds one machine; deployment-variants (ambassador vs shared routing service); DDIA-vocabulary mapping
- `sharded-cache.md` — Burns's deep-dive worked example; the 10×10 GB replicated-vs-sharded memory-utilisation math; hit-rate as capacity multiplier (2,000 RPS from 1,000 with 50% hit rate); criticality analysis; rollout penalty; twemproxy + memcached Kubernetes hands-on
- `replicated-sharded-service.md` — each shard is itself a Chapter 5-style replicated load-balanced service; shard-failure tolerance, safe rollouts during peak traffic, substrate for hot-sharding
- `hot-sharding.md` — dynamically rescaling per-shard replica count in response to organic traffic skew; Figure 6-3 walkthrough (replicate hot Shard A, compact cold Shards B+C); complement to DDIA's write-side key-splitting
- `shard-key-selection.md` — Burns's "too general / too specific / just right" discussion; `shard(request.path)` wrongly groups French and US users, `shard(request.ip, request.path)` wrongly splits two French users, `shard(country(request.ip), request.path)` is correct; generalisation principle

**Pages updated**:
- `designing-distributed-systems.md` — Chapter 6 marked ingested; Chapter 6 concepts section added; five new pages added to Related; Last updated bumped
- `partitioning.md` — "Partitioning applied to stateful serving tiers" section added framing Burns's Ch 6 as the service-layer analogue of DDIA partitioning; sources and Related extended
- `consistent-hashing.md` — "Consistent hashing and re-sharding a service" section added covering Burns's "equivalent to a complete cache failure" warning and the nginx `hash $request_uri consistent` example; sources and Related extended
- `hot-spots.md` — "Service-level mitigation: hot sharding" section added distinguishing write-side key-splitting (databases) from hot-sharding (services); sources and Related extended
- `rebalancing-partitions.md` — "Rebalancing at the service layer" section added with Burns's naive-`hash % N` warning and the shift to per-shard replica rebalancing in replicated-sharded services; sources and Related extended
- `request-routing.md` — routing-tier section extended with Burns's "root" terminology and the shared-shard-router deployment option; sources and Related extended
- `client-side-sharding.md` — Chapter 6 cross-reference section expanded to cover the per-pod-ambassador vs shared-shard-router trade-off as Chapter 6 presents it; sources and Related extended
- `caching-layer.md` — "When replicated isn't enough: sharded caches" section added connecting Chapter 5's replicated cache to Chapter 6's sharded cache; sources and Related extended
- `ambassador-pattern.md` — "Ambassadors and sharded services" section added clarifying that Ch 3 covers the client side and Ch 6 covers the service side of sharded services; sources and Related extended
- `replicated-load-balanced-service.md` — "Composing with sharding" section added; Related extended with the three new service-sharding pages
- `index.md` — five new pages added to "Serving patterns" section with one-line descriptions

**Notes**: The biggest design choice here was deciding what belongs on a new page vs an augmentation of an existing DDIA page. The DDIA partitioning corpus already covers the mechanics (hash vs key-range, consistent hashing, rebalancing strategies, routing) thoroughly. Burns's chapter adds five genuinely distinct things: (1) the explicit service pattern (root + shards) as a named architectural element — `sharded-service-pattern.md`; (2) the sharded-cache worked example with the memory-utilisation and hit-rate math — `sharded-cache.md`; (3) the replicated-sharded combination — `replicated-sharded-service.md`; (4) hot-sharding as an operational response to skew — `hot-sharding.md`; (5) the "what to hash" discussion with the too-general/too-specific framing — `shard-key-selection.md`. Everything else is treated as an augmentation of an existing DDIA page, with bidirectional cross-links. No contradictions with existing pages — Burns's hash-%-N anti-pattern is the same warning as DDIA's, just phrased in terms of cache miss rate rather than data movement. One ambiguity: Burns conflates "deploying a new version of a sharded cache" (code rollout) with "re-sharding" (changing the sharding function) when warning about capacity loss; the wiki pages separate these because they have different remedies (staggered rollout vs consistent hashing respectively). The chapter's hands-on YAML deployments are paraphrased rather than reproduced — the patterns and trade-offs are the interesting content.

---

## 2026-04-16 — Ingest: Designing Distributed Systems Chapter 7

**Source**: `raw/designing-distributed-systems/chapter-07-scattergather.md`

**Pages created**:
- `scatter-gather-pattern.md` — the third serving pattern; root fans request out to all leaves and combines partials; two variants (root-distributed work with intersection; leaf-sharded data with union); cat-and-dog distributed-document-search worked example for each variant; leaf count as a design knob; reliability via leaf replication; composes with the first two serving patterns; relationship to DDIA's scatter/gather coverage (document-partitioned secondary indexes, MPP parallel query, MapReduce, dataflow engines)
- `tail-latency-amplification.md` — Burns's 99th-percentile math worked through in a table (p99 of 2 s becomes p95 at 5 leaves, near-guaranteed at 100 leaves); the straggler framing; availability amplification via the same 0.99^N compounding; four mitigations (hedged requests, bounded leaf count, leaf replication, approximate gather); head-of-line-blocking and load-parameters cross-links

**Pages updated**:
- `response-time-percentiles.md` — tail-latency-amplification section extended with Burns's Chapter 7 framing and a cross-link to the dedicated page and scatter-gather-pattern; sources and Last updated bumped
- `partitioning-secondary-indexes.md` — document-partitioned (local) index reads named as a database-layer instance of the scatter-gather pattern; sources and Last updated bumped
- `partitioning.md` — parallel query execution paragraph extended with scatter-gather-pattern and hadoop-vs-mpp-databases links; scatter-gather-pattern and tail-latency-amplification added to Related; sources updated
- `sharded-service-pattern.md` — "Relationship to scatter/gather" section rewritten with a proper cross-link and the distinction between route-to-one vs fan-out-to-all semantics; Related extended
- `replicated-sharded-service.md` — added "Relationship to scatter/gather" section framing leaf replication as the same construction applied to scatter/gather reliability; sources and Related extended
- `replicated-load-balanced-service.md` — added "Composing with scatter/gather" section; Related extended
- `hadoop-vs-mpp-databases.md` — added "MPP query execution as scatter/gather" section connecting MPP parallel query optimisation to the Chapter 7 pattern; sources and Last updated bumped; Related extended
- `designing-distributed-systems.md` — Chapter 7 marked ingested; Chapter 7 concepts section added; two new pages added to Related; Last updated bumped
- `index.md` — two new pages added to "Serving patterns" section

**Notes**: The chapter is short (27 lines of extracted markdown) but introduces a named, architecturally distinct pattern with one heavyweight performance concern (tail amplification). Two new pages rather than one because the amplification math is substantive enough that the main pattern page would have become lopsided, and the existing DDIA coverage of tail amplification on `response-time-percentiles.md` was only a single paragraph — a dedicated page now serves both the DDIA context and the Burns context with proper treatment of the straggler framing, availability compounding, and mitigations. The chapter's two worked examples (distributed document search — root-distributed and leaf-sharded variants) are captured inline on the pattern page because they are inseparable from the variant definitions; both use the same "cat AND dog" query so the difference in aggregation step (intersection vs union) is especially clear. No contradictions encountered. The main judgement call was whether to break out "straggler problem" as a separate page — decided against, since Burns uses the term interchangeably with tail-latency amplification and the mitigations are the same; the straggler framing is instead a named section on the amplification page. MapReduce's own straggler mitigations (speculative execution) are already covered on `mapreduce.md` and were not updated here since Chapter 7 does not discuss them.

---

## 2026-04-16 — Ingest: Designing Distributed Systems Chapter 8

**Source**: `raw/designing-distributed-systems/chapter-08-functions-and-event-driven-processing.md`

**Pages created**:
- `functions-as-a-service.md` — the fourth serving pattern; developer-facing benefits; three operational/architectural/economic challenges (opaque dependencies with the cyclic-function-chain pathology, no background processing, no in-memory data, cost-curve inversion at high volume); fit/no-fit matrix; events-vs-requests distinction; two-factor-SMS worked example; relationship to the other three serving patterns as a composition table; relationship to [[event-streams]], [[message-brokers]], [[event-sourcing]], [[change-data-capture]] as event sources; relationship to Newman's [[running-too-many-things]] serverless-first framing as the complementary view
- `serverless-vs-event-driven.md` — Burns's opening terminological distinction; the four corners of the matrix (managed FaaS; container-as-a-service; self-hosted FaaS on Kubernetes; traditional servers); why developer-productivity benefits come from the serverless axis and architectural constraints come from the event-driven axis; practical implications for pricing, limits, and observability
- `faas-decorator-pattern.md` — Burns's first composition pattern; the Python-decorator analogy; the JSON default-filling worked example with Kubeless deployment commands; explicit FaaS-decorator-vs-adapter-container comparison (independent vs coscheduled scaling) and FaaS-vs-gateway-middleware comparison; common applications (validation, shimming, backward-compat); relationship to Newman's [[decorating-collaborator-pattern]] as a natural implementation substrate during migration
- `event-pipeline-pattern.md` — Burns's second composition pattern; directed graph of FaaS handlers connected by webhooks; the CI-with-human-approval worked example (code → build → analysis → Jira approval → production deploy); the new-user signup worked example with dispatcher + required/optional handler factoring; two load-bearing differences from microservices (event-driven-by-construction and heterogeneous-including-human participants); relationship to [[message-brokers]] (broker-mediated as the production form), [[stream-processing]] (same topology one level down), [[saga]] (pipeline with compensation), and [[change-data-capture]]/[[event-sourcing]] (event sources)

**Pages updated**:
- `designing-distributed-systems.md` — Chapter 8 marked ingested; Chapter 8 concepts section added; four new pages added to Related; Last updated bumped
- `running-too-many-things.md` — added Burns's catalogue of FaaS limits (sustained high-volume, large in-memory state, long-running work, hard-to-reason-about cross-function dependencies) as the complement to Newman's serverless-first default; cross-links to [[functions-as-a-service]] and [[serverless-vs-event-driven]]; sources and Last updated bumped
- `desired-state-management.md` — added Burns's Chapter 8 treatment as the serving-pattern companion to Newman's operations-frame discussion; [[serverless-vs-event-driven]] cited for the two-axis framing; sources and Last updated bumped
- `decorating-collaborator-pattern.md` — added "FaaS as the implementation substrate" section connecting Newman's migration pattern to Burns's [[faas-decorator-pattern]]; sources and Related extended
- `adapter-pattern.md` — added "Adapters vs FaaS decorators" section with Burns's scale-with-backend-vs-independent-scale rule of thumb; sources and Related extended
- `event-streams.md` — added "FaaS as an event consumer" section; broker-plus-FaaS noted as the common production substrate; sources, Related, and Last updated bumped
- `message-brokers.md` — added "FaaS as a broker consumer" section connecting broker-buffered-fan-out with FaaS-scale-to-zero; Related extended; sources and Last updated bumped
- `index.md` — four new pages added to "Serving patterns" section with one-line descriptions

**Notes**: Four new pages rather than two or three — Burns's chapter has distinct substantive content on the serverless-vs-event-driven distinction and on each of the two composition patterns, so splitting them gives cleaner cross-link targets than a single overloaded FaaS page would. The serverless-vs-event-driven page is short but load-bearing: the distinction is the first thing Burns teaches and it shapes the rest of the chapter's prescriptions (especially the escape hatch to self-hosted FaaS on Kubernetes when per-request pricing stops working). The adapter-pattern vs FaaS-decorator comparison is the most interesting cross-Chapter-trilogy observation — Burns handles it head-on in the text and it's the kind of detail that's easy to miss but practically useful, so it appears both on the new [[faas-decorator-pattern]] page and as a new section on [[adapter-pattern]]. No contradictions with existing pages — Newman's "serverless-first as default" and Burns's "here are the limits where serverless stops working" are genuinely complementary rather than competing. The main judgement call: whether to put the two-factor-auth and signup-pipeline hands-on code snippets inline or paraphrase them. Paraphrased the defaulting and signup examples for brevity but preserved the structural shape (dispatcher + required/optional handlers in the signup case) because that shape is the design teaching; the raw Kubeless deploy commands are included to show how light the lifecycle is. One ambiguity: Burns blurs "event" and "webhook" in places — he wires "pipelines" synchronously over HTTP in the worked examples, whereas production event pipelines almost always sit on a broker. Handled by writing the chapter's content faithfully (webhook-driven) and adding an explicit "broker-mediated is the common production form" section on [[event-pipeline-pattern]] so readers aren't left with only the fragile synchronous-HTTP mental model.

---

## 2026-04-16 — Ingest: Designing Distributed Systems Chapter 9

**Source**: `raw/designing-distributed-systems/chapter-09-ownership-election.md`

**Pages created**:
- `ownership-election-pattern.md` — Burns's fifth serving pattern; distributes *assignment*; master election over etcd/ZooKeeper/Consul; the two-replicas-briefly-both-master scenario; client self-check + server-side owner validation + resource-version defences; the applied container-level companion to DDIA's [[consensus]], [[fencing-tokens]], [[truth-and-leadership-in-distributed-systems]], [[failover]] coverage
- `singleton-pattern.md` — Burns's honest "do you even need this?" opening; one replica + orchestrator-backed restart; three-to-four nines of uptime arithmetic; the rollout-window SLA ceiling; background async work as the canonical fit; the generalisable thesis that "distributed" is sometimes unnecessarily complex
- `distributed-locks-on-kv-stores.md` — the applied construction: compare-and-swap + TTL + resource versions; derivation by sequentially fixing the naive implementation's bugs (stuck-on-crash → stale-unlock-after-pause → split-ownership); watchdog timers; hands-on etcdctl walkthrough; structural identity with [[fencing-tokens]] and [[linearizability]]
- `renewable-leases.md` — long-running ownership via short TTL + background refresh every `ttl/2`; `handleLockLost` implemented as process termination with orchestrator-backed restart; Kubernetes active-scheduler as canonical worked example; combined with owner validation for the pause-resistance story
- `operator-pattern.md` — CoreOS's application-specific controller; declarative custom-resource API; the etcd-operator-via-Helm walkthrough; relationship to [[desired-state-management]] as the application-specific specialisation and to [[modular-reusable-containers]] as packaged operational expertise

**Pages updated**:
- `zookeeper.md` — added "Container-level perspective (Burns)" section framing etcd/ZooKeeper/Consul as interchangeable at the pattern level and Burns's discouragement of implementing consensus yourself; Related extended with the four new Chapter 9 pages
- `fencing-tokens.md` — added "Applied container-level form (Burns)" section with the delayed-R1 scenario walk-through; Related extended; sources updated
- `truth-and-leadership-in-distributed-systems.md` — added "Applied form at the container level" section with Burns's overloaded-processor scenario; Related extended; sources updated
- `failover.md` — added "Failover at the container level" section laying out Burns's three-layer prescription (decide if you need it, outsource consensus, use renewable leases); Related extended; sources updated
- `consensus.md` — added Burns's "don't implement this yourself" statement as the applied echo of the DDIA outsource-to-dedicated-services point; Related extended; sources updated
- `process-pauses.md` — added Burns's CPU starvation on overscheduled machines as a concrete container-level process-pause scenario; sources updated
- `desired-state-management.md` — added "Application-specific desired state: the operator pattern" section; Related extended; sources updated
- `health-probes.md` — added "Health probes and the singleton pattern" section framing the liveness probe as load-bearing for the singleton's three-to-four-nines uptime; singleton-pattern added to Related; sources updated
- `designing-distributed-systems.md` — Chapter 9 marked ingested; Chapter 9 concepts section added; five new pages added to Related; Last updated bumped
- `index.md` — five new pages added to "Serving patterns" section

**Notes**: The DDIA coverage of this material is unusually deep — the theory of [[consensus]], [[fencing-tokens]], [[zookeeper]], [[truth-and-leadership-in-distributed-systems]], [[process-pauses]], and [[failover]] is all already in the wiki. Burns's chapter is genuinely complementary rather than duplicative: it contributes the applied container-level recipe (which KV store, what the lock/lease construction looks like in code, what the resource-version mitigation looks like in practice, how it all sits in Kubernetes via Helm and operators). So new pages are reserved for content that is substantively Burns's own, and existing pages are extended with focused "applied form" or "container-level perspective" sections that point back to the Chapter 9 pages. The most interesting cross-link is between [[fencing-tokens]] (DDIA's named mechanism) and [[distributed-locks-on-kv-stores]] (Burns's first-principles derivation of the same mechanism): Burns never uses the term "fencing," but the resource-version-per-request construction is identical. That cross-link is now explicit in both directions. The singleton-pattern is a rare "don't reach for the big pattern" moment in Burns's book and stands up well as an independent page. Kept the operator pattern as a small standalone page rather than folding it into [[desired-state-management]] because the custom-resource-API aspect and Burns's treatment of it as "a new direction for building reliable distributed systems" are distinctive enough to deserve their own target. One small ambiguity: Burns's Figure 9-1 and Figure 9-2 are referenced in the raw extract but the figures themselves are not present. The text describes them sufficiently for paraphrasing, and both scenarios are captured on the pattern page without relying on seeing the diagrams. No contradictions with existing pages encountered.

---

## 2026-04-16 — Ingest: Designing Distributed Systems Chapter 10 (Work Queue Systems)

**Source**: `raw/designing-distributed-systems/chapter-10-work-queue-systems.md`

Chapter 10 opens Part III of the book — the **Batch Computational Patterns** — with the **work queue**, the simplest batch pattern. Burns's thesis: for wholly independent work items (the embarrassingly parallel case), the machinery around them is almost entirely generic, and the application-specific parts collapse into two narrow interfaces: an ambassador-shaped **source container** that produces items, and a file-based, one-shot **worker container** that processes them. Between the two, a generic queue-manager loop plus Kubernetes Jobs-with-annotations provides reliable execution and durable state — the queue-manager itself stores nothing. The chapter also presents a queueing-theory-flavoured autoscaler rule (`P > processing_time / interarrival_time` for a stable queue) and the multi-worker pattern (adapter-pattern applied to batch pipelines).

**Pages created**:
- `work-queue-pattern.md` — the core Chapter 10 pattern; generic queue-manager; reusable-container thesis; the two-interface split; Kubernetes Jobs as durable state; video-thumbnailer worked example; relationship to MapReduce, message brokers, and FaaS
- `source-container-interface.md` — the ambassador-shaped producer interface; two-endpoint HTTP REST API on `localhost`; deliberate omission of "mark processed"; API versioning discipline; implementation patterns (cloud storage, NFS, Kafka/Redis)
- `worker-container-interface.md` — the file-based, one-shot consumer interface; `WORK_ITEM_FILE` env var and ConfigMap mount; Kubernetes Job as the reliability substrate; idempotence requirement; ffmpeg thumbnailer worked example
- `dynamic-worker-scaling.md` — the three regimes (uncapped, capped, dynamic); interarrival vs processing time math; Burns's three-example table (1/min vs 30s, 1/min, 2/min); `P > processing_time / interarrival_time` rule; the 90%-of-interarrival heuristic for scaling down
- `multi-worker-pattern.md` — adapter-pattern specialisation; aggregator container presenting the standard worker interface outward while delegating inward to reusable processing containers; the face-detect + identity-tag + blur worked example

**Pages updated**:
- `ambassador-pattern.md` — added "Ambassadors as work-queue sources" section (Chapter 10's new ambassador use: source ambassadors fronting cloud storage, NFS, or broker topics); Related extended; sources updated
- `adapter-pattern.md` — added "Adapters and batch worker composition" section (multi-worker aggregator as an adapter applied to batch pipelines); Related extended; sources updated
- `batch-processing.md` — added "Container-level perspective: Burns's work queue" section positioning the work queue as the dispatch primitive below MapReduce in the batch stack; Related extended; sources updated; Last updated bumped
- `message-brokers.md` — added "Brokers as a work-queue source" section covering source-ambassador-fronts-Kafka/Redis glue; Related extended; sources updated
- `designing-distributed-systems.md` — Chapter 10 marked ingested; Chapter 10 concepts section added; five new pages added to Related; Last updated bumped
- `index.md` — new "Batch computational patterns" section added below "Serving patterns"; five new pages listed with one-line descriptions

**Notes**: The DDIA batch coverage is well-developed in the wiki ([[batch-processing]], [[mapreduce]], [[dataflow-engines]], [[message-brokers]], [[log-based-message-brokers]], [[exactly-once-semantics]]), and Burns's Chapter 10 sits **below** it in the stack rather than duplicating it. The work queue is the dispatch-one-item-per-worker primitive that MapReduce composes with partitioning and that dataflow engines generalise into arbitrary DAGs. Burns's contribution is the container-level view: the reusable-queue-manager + two-interface split, and the orchestrator-as-durable-state trick (Kubernetes Jobs with annotations, no sidecar database). New pages therefore focus on that container-level material — the ambassador-shaped source interface, the file-based worker interface, the autoscaling math, the multi-worker adapter specialisation — and existing DDIA batch pages are extended with focused cross-reference sections rather than rewritten. The most interesting cross-link is between [[ambassador-pattern]] (already used for sharding, service brokering, request splitting) and [[source-container-interface]] (now a fourth canonical ambassador use — batch ingest), and between [[adapter-pattern]] and [[multi-worker-pattern]] (composing worker containers is adapter shape). One small ambiguity: Burns's Figures 10-1 through 10-5 are referenced in the raw extract but the figures themselves are not present — text descriptions suffice. The chapter's Python driver code is reproduced on the pattern page in paraphrase rather than verbatim because the chapter's narrative of "this is how we use Kubernetes Jobs as our queue state" matters more than the specific API calls. No contradictions with existing pages encountered.

---

## 2026-04-16 — Ingest: Designing Distributed Systems Chapter 11 (Event-Driven Batch Processing)

**Source**: `raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md`

Chapter 11 is Burns's second batch computational pattern, directly building on Chapter 10: chain individual [[work-queue-pattern|work queues]] into directed acyclic workflow graphs, where the output of each stage is the input to the next and stage-completions are the events that trigger downstream work. The chapter's load-bearing contribution is a small named vocabulary of five linking patterns (copier, filter, splitter, sharder, merger) that wire queues into workflows, with each linking pattern implemented as a narrow [[adapter-pattern|adapter]] or [[ambassador-pattern|ambassador]] at the seam between queues. Burns draws the parallel to [[event-pipeline-pattern|Chapter 8's FaaS event pipelines]] explicitly — same DAG-of-handlers-connected-by-events topology, at batch-stage granularity instead of per-event FaaS. The second substantive contribution is [[publisher-subscriber-infrastructure|pub/sub infrastructure]] (Kafka, EventGrid, SQS) as the workflow transport layer, with Burns's hands-on Kafka-on-Kubernetes-via-Helm walkthrough and the topic-per-output-shard convention.

**Pages created**:
- `event-driven-batch-pattern.md` — the hub page; chains [[work-queue-pattern]] instances into DAGs via named linking patterns over pub/sub; new-user-signup chapter-length worked example; topology-as-specification payoff; comparison tables with [[event-pipeline-pattern]] (FaaS cousin) and [[dataflow-engines]] (DDIA cousin); relationship to workflow schedulers (Airflow, Argo, Prefect, Luigi)
- `copier-pattern.md` — fan-out primitive; 1 → N identical streams; video-transcoding worked example (4K / 1080p / low-res / GIF thumbnail from one MP4); Unix `tee` analogy; comparison with splitter and sharder
- `filter-pattern.md` — drop items that don't meet a criterion; Burns's preferred implementation as a [[source-container-interface|source ambassador]] wrapping an upstream source (ambassador-on-ambassador composition); opt-in-user worked example; Unix `grep` analogy; equivalence with splitter + dropped branch
- `splitter-pattern.md` — route items to different queues by per-item criterion; shipping-notification worked example (email / text / both / neither); subsumes [[copier-pattern]] and [[filter-pattern]] as edge cases; Burns's equivalence with copier + two filters
- `sharder-pattern.md` — hash-based even distribution across N queues; motivated by reliability (staged rollouts, failure-zone spreading) not semantic routing; dynamically routes around unhealthy shards; container-level echo of [[sharded-service-pattern]] and DDIA [[partitioning]]
- `merger-pattern.md` — fan-in primitive; N streams → 1; multi-source adapter that adapts a *collection* of source containers into a single merged source; CI-across-many-repos worked example; structural mirror of [[multi-worker-pattern]]
- `publisher-subscriber-infrastructure.md` — the transport substrate; Kafka / EventGrid / SQS as interchangeable implementations at pattern level; Kafka-on-Kubernetes-via-Helm hands-on walkthrough; `--replication-factor` and `--partitions` parameters linked to DDIA [[replication]] and [[partitioning]]; topic-per-output-shard convention (`photos-1`, `photos-2`, `photos-3`)

**Pages updated**:
- `work-queue-pattern.md` — added "Composing work queues: event-driven batch workflows" section pointing at Chapter 11; seven new Chapter 11 pages added to Related; Chapter 11 added to Sources
- `event-pipeline-pattern.md` — added "Relationship to event-driven batch (Chapter 11)" section drawing Burns's explicit FaaS / batch parallel and the topology-as-specification shared payoff; [[event-driven-batch-pattern]] added to Related; Chapter 11 added to Sources
- `batch-processing.md` — extended the Burns container-level section with a paragraph on Chapter 11 positioning it as the container-level analogue of dataflow DAGs and workflow schedulers; seven new Chapter 11 pages added to Related; Chapter 11 added to Sources; Last updated bumped
- `dataflow-engines.md` — added "Container-level counterpart: Burns's event-driven batch" section with side-by-side comparison table (DAG unit, transport, scheduling, fault tolerance, DAG vocabulary); Related extended; Chapter 11 added to Sources; Last updated bumped
- `message-brokers.md` — added "Brokers as the workflow transport" section covering Chapter 11's pub/sub-as-transport framing; five linking patterns + hub + infrastructure added to Related; Chapter 11 added to Sources
- `source-container-interface.md` — added "Source ambassadors as filter primitives" subsection showing ambassador-on-ambassador composition; [[event-driven-batch-pattern]], [[filter-pattern]], [[merger-pattern]] added to Related; Chapter 11 added to Sources
- `multi-worker-pattern.md` — added "Merger pattern (Chapter 11)" subsection showing the source-side mirror of the multi-worker adapter; [[event-driven-batch-pattern]] and [[merger-pattern]] added to Related; Chapter 11 added to Sources
- `adapter-pattern.md` — extended the "Adapters and batch worker composition" section with Chapter 11's "every linking pattern is an adapter at the seam between queues" framing; five new Chapter 11 pages added to Related; Chapter 11 added to Sources
- `ambassador-pattern.md` — extended the "Ambassadors as work-queue sources" section with Chapter 11's filter pattern as ambassador-on-ambassador composition; [[event-driven-batch-pattern]] and [[filter-pattern]] added to Related; Chapter 11 added to Sources
- `designing-distributed-systems.md` — Chapter 11 marked ingested; Chapter 11 concepts section added; seven new pages added to Related; Last updated bumped
- `index.md` — seven new pages added to "Batch computational patterns" section with one-line descriptions

**Notes**: Chapter 11 is compact (the raw extract is only 81 lines) but the concepts are distinct enough that each of the five linking patterns gets its own page — mirroring how Chapter 6's sharded-service, sharded-cache, hot-sharding, replicated-sharded, and shard-key-selection each got their own pages despite being part of one chapter. The named-pattern-per-page discipline is a better fit here than bundling into one `workflow-building-blocks.md` page because (a) Burns names each pattern explicitly, (b) each has a distinct worked example, and (c) the cross-pattern comparison tables (copier vs splitter vs sharder, splitter vs copier + two filters, merger as mirror of multi-worker) are easier to read when each pattern has its own landing page to link to. The hub page `event-driven-batch-pattern.md` ties them together and covers the worked chapter-length signup example. The DDIA cross-links are structural: Chapter 11 is the **container-level** form of the [[dataflow-engines|dataflow DAG]] idea, with stages instead of operators and pub/sub instead of shuffles — that comparison table is now prominent on both the Burns hub page and the DDIA dataflow-engines page. The [[event-pipeline-pattern]] page now explicitly names the Chapter 11 cousin (same topology, different granularity), and the [[publisher-subscriber-infrastructure]] page explicitly names DDIA's [[replication]] and [[partitioning]] as what Kafka's `--replication-factor` and `--partitions` parameters control. The most interesting observation during ingestion: every one of Burns's five linking patterns turns out to be an [[adapter-pattern]] or [[ambassador-pattern]] instance — filter and merger as source ambassadors (filter wraps one source, merger wraps many), copier/splitter/sharder as worker-side adapters that publish to multiple topics. Burns is explicit about this for the merger ("another great example of the adapter pattern"); the observation that it applies to all five is now foregrounded on the hub page. One small ambiguity: Burns references Figures 11-1 through 11-9 but the figures themselves are not in the raw extract — text descriptions suffice for paraphrasing (e.g., Figure 11-6 on the sharder's reroute-to-healthy-shards behaviour is captured as the "dynamic adjustment under shard failure" subsection). No contradictions with existing pages encountered.

---

## 2026-04-16 — Ingest: Designing Distributed Systems Chapter 12 (Coordinated Batch Processing)

**Source**: `raw/designing-distributed-systems/chapter-12-coordinated-batch-processing.md`

Chapter 12 is the final substantive chapter of Burns's book (Chapter 13 is a short conclusion, skipped). It closes the batch-pattern trilogy with **coordinated batch processing** — the aggregation side of the batch pipeline that pulls parallel workflow outputs back together into a single result. Burns's thesis: the Chapter 11 linking patterns excel at splitting and chaining, but they offer no primitive for guaranteeing completeness or combining values, and the [[merger-pattern|merger]] alone is explicitly insufficient because "it does not ensure that a complete dataset is present prior to the beginning of processing." The chapter supplies two distinct coordination primitives — the **join** (barrier synchronization; wait for every upstream worker) and the **reduce** (associative pairwise combine; the container-level naming of MapReduce's reduce step) — and walks through a chapter-length image-tagging worked example that composes every batch pattern in the book. The chapter's unifying move is the explicit identity Burns draws between his patterns and MapReduce: map = [[sharder-pattern|sharder]] + [[work-queue-pattern|work queue]]; reduce = reduce-pattern; MapReduce's "wait for every mapper before reducing" = join-pattern. That identity closes the loop between Burns's container trilogy (Chapters 10–12) and DDIA's batch-processing theory.

**Pages created**:
- `coordinated-batch-pattern.md` — hub page; the two coordination primitives; three-way comparison table (merger vs join vs reduce) distinguishing stream-passthrough vs barrier vs value-combine semantics; the image-tagging chapter-length worked example composing sharder + multi-worker + join + copier + sharder + multi-worker + reduce; MapReduce identity table; relationship to [[dataflow-engines]], [[batch-processing]], and the DDIA join pages
- `join-pattern.md` — barrier synchronization; Burns's explicit contrast with [[merger-pattern]] (merger has no completeness guarantee); cost analysis (straggler-bound latency, same problem as [[scatter-gather-pattern]]); load-bearing use cases (destructive steps, global aggregates, phase fences); worked example (image-blur fence before deletion); relationship to MapReduce's map-to-reduce barrier and to DDIA's differently-named [[sort-merge-joins]]; workflow-scheduler parallel (Airflow/Argo/Prefect/Luigi join-all gates)
- `reduce-pattern.md` — associative pairwise combine; explicit identity with MapReduce's reduce half; Burns's three worked examples (word count, population sum, population-weighted histogram) worked through carefully to surface the associativity requirement; the three defining properties (associative/repeatable, parallel, pipelined with upstream); comparison with join (strictly more parallel when the combine is associative); relationship to [[scatter-gather-pattern]]'s gather step and to dataflow engines' reduce/aggregateByKey operators

**Pages updated**:
- `mapreduce.md` — added "Container-level perspective: map = sharder, reduce = reduce-pattern" section with the four-row identity table (input split + map tasks = work-queue; shuffle = sharder; "wait for all mappers" = join-pattern; reduce = reduce-pattern); Related extended with the Chapter 12 pages and Burns batch vocabulary; Chapter 12 added to Sources; Last updated bumped
- `sort-merge-joins.md` — added "Note on two uses of 'join'" section disambiguating DDIA's relational-operator join from Burns's barrier-synchronization join; Related extended with [[join-pattern]] and [[coordinated-batch-pattern]]; Chapter 12 added to Sources; Last updated bumped
- `merger-pattern.md` — added "Merger is not a join: the Chapter 12 distinction" section with Burns's explicit contrast ("merge does not ensure a complete dataset is present"); Related extended with [[join-pattern]], [[reduce-pattern]], [[coordinated-batch-pattern]]; Chapter 12 added to Sources
- `event-driven-batch-pattern.md` — added "Closing the loop: coordinated batch processing (Chapter 12)" section pointing to the two coordination primitives that Chapter 11's linking patterns lack; Related extended; Chapter 12 added to Sources
- `work-queue-pattern.md` — extended the "Composing work queues" section with a Chapter 12 paragraph positioning it as the third part of the trilogy (work queue = primitive, event-driven batch = composition, coordinated batch = aggregation); Related extended; Chapter 12 added to Sources
- `batch-processing.md` — added a Chapter 12 paragraph to the Burns container-level section, with the MapReduce identity (map = sharder, reduce = reduce-pattern, MapReduce barrier = join-pattern) and the framing that Burns's pattern-level choice between join and reduce is the coarse-grained form of dataflow engines' operator-level pipelining decisions; Related extended; Chapter 12 added to Sources; Last updated bumped
- `dataflow-engines.md` — added a paragraph to the Burns-counterpart section on the Chapter 12 pattern-level echo of the barrier-vs-pipelined-reduce operator-level choice; Related extended with the three new Chapter 12 pages; Chapter 12 added to Sources
- `designing-distributed-systems.md` — Chapter 12 marked ingested; Chapter 12 concepts section added (book-complete); three new pages added to Related; Last updated bumped to "Chapter 12 ingested — book complete"; short closing paragraph added to the About-the-book section framing Chapter 13 as the open-ended-catalogue conclusion
- `index.md` — three new pages added to "Batch computational patterns" section with one-line descriptions

**Notes**: Chapter 12 is short (86 lines in the raw extract) but the two coordination primitives are substantively distinct from Chapter 11's linking patterns — completeness and aggregation are different animals from fan-out, filtering, and routing — and they warrant separate pages. The most interesting editorial decision was how tightly to couple this chapter to [[mapreduce]]. Burns himself draws the identity explicitly in two places (map = sharder, reduce = reduce-pattern), so the decision was straightforward: [[mapreduce]] now carries a Container-level-perspective section with the four-row identity table, and each of `join-pattern.md` and `reduce-pattern.md` names the MapReduce correspondence as a top-level relationship rather than an aside. The second editorial call was how to handle the name collision on "join": DDIA's relational-operator join and Burns's barrier-synchronization join are distinct concepts that share the name, and both legitimately carry it because both "bring parallel work together." Rather than forcing disambiguation into the page names (e.g., `barrier-synchronization-join.md`), the name `join-pattern.md` matches Burns's own usage and the ambiguity is handled explicitly in a section on both sides — on [[sort-merge-joins]] and on [[join-pattern]] — with cross-references in each direction. I did not create a separate `coordinator-pattern.md` page because Burns does not treat "coordinator" as a named container-level primitive in this chapter; the coordination is the property of the join and the reduce, not of a separate container role. One small ambiguity: Burns references Figures 12-1 through 12-4 but the figures themselves are not in the raw extract — text descriptions of the worked image-tagging pipeline capture the structure sufficiently, and the staged worked example in `coordinated-batch-pattern.md` paraphrases Figures 12-3 and 12-4 via the numbered-stage walkthrough. No contradictions with existing pages encountered. With Chapter 12 ingested, *Designing Distributed Systems* is now fully represented in the wiki — 25 chapter-level pages across single-node, serving, and batch-computational patterns, with DDIA cross-references on every batch pattern and most serving patterns.

---

## 2026-04-16 — Wiki-wide lint pass

Ran parallel mechanical and content lint audits across all 243 pages; applied the resulting fixes in two phases.

**Pages created (3)**:
- `idempotence.md` — heavily referenced but previously undefined; natural/constructed techniques, op IDs, dedup tables, CAS, relationship to `[[exactly-once-semantics]]` and `[[fencing-tokens]]`
- `circuit-breaker.md` — Nygard's three-state machine; interaction with `[[timeouts]]`, `[[bulkhead]]`, `[[rate-limiting]]`; Hystrix/Resilience4j/Polly/service-mesh implementations
- `bulkhead.md` — compartmentalisation for failure isolation; thread-pool/process/service forms; companion to `[[circuit-breaker]]` and `[[timeouts]]`

**Pages updated — content fixes**:
- `service-mesh.md` — added 2026 editorial note superseding Newman's "let the space settle" caution (Istio/Linkerd/Envoy are stable)
- `desired-state-management.md` — added 2026 note that operator pattern, Helm, and IDPs have filled the "higher-order abstractions still being built" gap; linked to `[[operator-pattern]]`
- `consistent-hashing.md`, `rebalancing-partitions.md` — reworded "Cassandra 3.0 introduced…" to "Cassandra (since 3.0) uses…" to drop dated framing
- `eventual-consistency.md`, `quorums.md` — softened "not yet standard practice" on staleness metrics; noted cloud vendors have since made replication-lag observability routine
- `multi-leader-replication.md` — added paragraph explaining why "not linearizable" is categorical (no single serialisation point), distinguishing from `[[leaderless-replication]]`'s hedged framing
- `singleton-pattern.md` — clarified Kubernetes ~5-minute figure is node-death detection; contrasted with `[[renewable-leases]]` TTL-granularity handoff (10–15s) as motivation for `[[ownership-election-pattern]]`
- `faas-decorator-pattern.md`, `decorating-collaborator-pattern.md` — added symmetric "Not to be confused with" sections distinguishing the two similarly-named patterns
- `operator-pattern.md` — added `[[consensus]]` and `[[microservices]]` to Related
- `mapreduce.md` — added `[[graph-batch-processing]]` to Related

**Pages updated — cross-references**: `exactly-once-semantics.md`, `stream-processing-fault-tolerance.md`, `worker-container-interface.md`, `rpc.md`, `coordination-avoidance.md`, `end-to-end-argument.md`, `reduce-pattern.md`, `distributed-transactions.md`, `fencing-tokens.md` — added `[[idempotence]]` to Related. `timeouts.md`, `rate-limiting.md`, `robustness-vs-resilience.md`, `service-mesh.md` — added `[[circuit-breaker]]` and/or `[[bulkhead]]`. `robustness-and-resiliency-at-scale.md` — expanded one-line bulkhead and circuit-breaker mentions into substantive paragraphs. `microservices.md` — added `[[bulkhead]]`.

**Pages updated — mechanical cleanup**:
- Stripped legacy YAML frontmatter (`name`/`description`/`type` block) from 15 early-ingested DDIA pages: `reliability.md`, `scalability.md`, `fault-tolerance.md`, `maintainability.md`, `accidental-complexity.md`, `response-time-percentiles.md`, `scaling-approaches.md`, `load-parameters.md`, `rpc.md`, `message-brokers.md`, `encoding-formats.md`, `avro.md`, `schema-evolution.md`, `backward-forward-compatibility.md`, `data-outlives-code.md`. The three book-summary pages retain their frontmatter (intentional; they use `type: source-summary`).

**`index.md` restructured**:
- Merged single-page "Reliability concepts" section into "Core system properties" (now contains `reliability`, `scalability`, `maintainability`, `fault-tolerance`)
- Created new "Service communication infrastructure" section containing `service-discovery` (moved out of Partitioning), `service-mesh` (moved out of Migration patterns), `correlation-ids` (moved out of Observability) — these are cross-cutting infra, not topic-specific
- Added `idempotence` under Future of data systems, `circuit-breaker` and `bulkhead` under Microservices at scale

**Mechanical audit**: zero findings. All `[[links]]` resolve, every concept page passes the Summary/Sources/Last updated/Related format check, no orphans, naming consistently lowercase-hyphenated.

**Deferred (low-priority from the audit)**: a dedicated `kubernetes.md` / `container-orchestration.md` hub page remains un-created — the finding was "consider, not urgent." Can revisit if new material warrants it.

---

## 2026-04-16 — Source audit: idempotence, circuit-breaker, bulkhead

Searched `raw/` for passages that could augment the three pages and verified every source citation against the actual raw text.

**Source-audit findings**:
- `idempotence.md` cited `raw/designing-distributed-systems/chapter-10-work-queue-systems.md`, but that chapter does not contain the word *idempotence*. The Burns "item-keyed output path" phrasing was synthesis, not a quote. Citation removed; the `s3://bucket/{item_id}/output.png` example reframed as a worked idiom without the false attribution.
- `circuit-breaker.md` and `bulkhead.md` both cited `raw/monolith-to-microservices/chapter-05-growing-pains.md` for pattern details that are actually from Nygard's *Release It!* (not in `raw/`). Newman only mentions circuit breakers in one sentence and never uses the word *bulkhead* at all. His actual contribution is a high-level resilience checklist and a pointer to *Release It!*.

**Pages updated**:
- `idempotence.md` — Sources field rewritten (dropped the incorrect work-queue citation, added Ch 04 and glossary which now carry explicit quotes); added Kleppmann's direct definition quote; added Ch 04 RPC-retry quote as a third motivation bullet; rewrote the "naturally idempotent" examples to anchor each bullet in a Kleppmann quote where available; added the concrete $11 / Example 12-1 banking grounding; added the UUID-in-hidden-form-field recipe from Example 12-2; added the "requests table as event log" bonus insight; added the "distributed transactions vs idempotence" alternative-framings quote; added a new "Integrity, not timeliness" section drawing the distinction from Ch 12.
- `circuit-breaker.md` — added a "Note on sources" section clarifying that Newman Ch 5 is the only `raw/` source and that details beyond his one-sentence mention are synthesis from *Release It!* (not in `raw/`); added Newman's direct back-pressure quote; added a "Newman's wider resilience checklist" section containing his full isolation / async / multiple-copies / desired-state-management recommendation; added Newman's "resiliency is more than just implementing a few patterns" quote to the robustness-vs-resilience section.
- `bulkhead.md` — Sources field annotated to flag that the word *bulkhead* does not appear in any `raw/` file; added a "Note on sources" section explaining that the pattern is from *Release It!* (not in `raw/`) and that Newman's "Isolating services more from each other" sentence is the highest-specificity raw content; rewrote the "Newman names this" line and the "Newman lists bulkheads" claim to reflect what Newman actually says vs. pattern-literature synthesis.

**No new pages**. `index.md` unchanged (existing one-line descriptions still accurate). No cross-reference changes required in other pages; the additions were all source-fidelity and additional Kleppmann quotes, not new concepts.

**Note on raw-source coverage**: four PDFs in `raw/` (*Building Event-Driven Microservices*, *Fundamentals of Software Architecture*, *Fundamentals of Data Engineering*, *Site Reliability Engineering*) have not been extracted. Any of them might contain direct bulkhead/circuit-breaker content; if extracted later, these three pages should be re-audited.
