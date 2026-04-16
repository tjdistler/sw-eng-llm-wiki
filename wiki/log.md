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
