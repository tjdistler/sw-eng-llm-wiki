# Wiki Index

## Source summaries

| Page | Description |
|---|---|
| [[designing-data-intensive-applications]] | Book by Martin Kleppmann — concepts, organization, and ingestion status |
| [[monolith-to-microservices]] | Book by Sam Newman — concepts, organization, and ingestion status |

## Core system properties

| Page | Description |
|---|---|
| [[reliability]] | Systems that work correctly even when faults occur |
| [[scalability]] | Coping with increased load while maintaining performance |
| [[maintainability]] | Keeping systems workable for engineers and operators over time |

## Microservices fundamentals

| Page | Description |
|---|---|
| [[microservices]] | Independently deployable services modeled around a business domain, owning their own data |
| [[monolith]] | Single-process, modular, distributed, and third-party black-box variants; advantages and challenges |
| [[modular-monolith]] | Single-deployable application with stable internal module boundaries; the cheaper alternative Newman invokes throughout |
| [[independent-deployability]] | The central discipline: change and deploy one service without touching any other |
| [[conways-law]] | Systems mirror the communication structure of the organizations that build them |

## Microservice migration

| Page | Description |
|---|---|
| [[why-microservices]] | The three-question test; legitimate motivations and a cheaper alternative for each |
| [[when-microservices-are-a-bad-idea]] | Unclear domain, true startups, customer-installed software, no clear reason |
| [[incremental-migration]] | Chip away one service at a time; production is what counts |
| [[reversible-vs-irreversible-decisions]] | Bezos's two-way / one-way doors applied to migration choices |
| [[cost-of-change]] | Push experiments toward the whiteboard; database splits are the expensive end |
| [[extraction-prioritization]] | Two-axis effort/benefit model for picking the first service to extract |
| [[event-storming]] | Brandolini's collaborative bottom-up domain modelling technique |
| [[robustness-vs-resilience]] | David Woods's distinction; microservices give you neither for free |
| [[measuring-microservice-transition]] | Quantitative + qualitative; checkpoints; the sunk cost fallacy |

## Migration patterns

| Page | Description |
|---|---|
| [[migration-pattern-selection]] | Choosing among the patterns; can-you-change-the-monolith; copy vs reimplement |
| [[strangler-fig-pattern]] | Intercept calls at the perimeter; new service grows alongside the monolith |
| [[branch-by-abstraction]] | In-place migration via abstraction + alternative implementation; for deep functionality |
| [[parallel-run-pattern]] | Run both implementations on every call; compare results; high-risk verification |
| [[decorating-collaborator-pattern]] | Proxy triggers new-service calls based on monolith's request/response |
| [[ui-composition]] | Splice UI from old and new at page, widget, or micro-frontend level |
| [[seams-and-legacy-code]] | Feathers's seam concept; the refactoring unit inside the monolith |
| [[deployment-vs-release]] | The separation that makes all the patterns possible |
| [[feature-toggle]] | Runtime switches for cutover and rollback |
| [[progressive-delivery]] | Umbrella for parallel run, canary, dark launch, feature toggles |
| [[service-mesh]] | Per-service local proxies; avoids the shared-smart-pipe problem |

## Database decomposition

| Page | Description |
|---|---|
| [[database-decomposition]] | Hub page: why split the database; the pattern catalogue and Newman's sequencing guidance |
| [[shared-database-antipattern]] | Multiple services on one schema; what's wrong, where it's acceptable |
| [[database-view-pattern]] | Read-only projection from a shared schema; coping pattern |
| [[database-wrapping-service]] | Thin service in front of a tangled schema; converts DB dependencies to service dependencies |
| [[database-as-a-service-interface]] | Expose a separate read-only DB as a managed endpoint; generalised reporting database |
| [[aggregate-exposing-monolith]] | New service calls back to monolith for data the monolith still owns |
| [[change-data-ownership]] | Move data into the new service; invert the dependency |
| [[synchronize-data-in-application]] | Three-step pattern for migrating data with rollback safety; Trifork medical-records example |
| [[tracer-write]] | Incrementally move source of truth; tolerate two sources during migration; Square Fulfillments |
| [[split-the-database-first]] | Sequencing — schema-first vs code-first vs both-at-once; physical vs logical separation |
| [[repository-per-bounded-context]] | Factor data-access code along context lines as a first step |
| [[database-per-bounded-context]] | Separate schemas inside a modular monolith; preserves future extraction options |
| [[monolith-as-data-access-layer]] | Expose an API on the monolith; JustSocial's pattern |
| [[multischema-storage]] | New service holds its own schema for new data while still reading from the monolith |
| [[split-table-pattern]] | Separate a table whose columns belong to different bounded contexts |
| [[move-foreign-key-to-code]] | Replace a cross-service DB join with a service call; handle referential-integrity fallout |
| [[shared-static-data]] | Four patterns for country-code-style reference data: duplicate, dedicated schema, library, service |
| [[saga]] | Coordinate multi-service operations without distributed locks; orchestrated vs choreographed; compensating actions |

## Team and organization

| Page | Description |
|---|---|
| [[team-autonomy]] | Gore, Timpsons, two-pizza teams; how microservices amplify (and don't grant) autonomy |
| [[reorganizing-teams]] | Moving from competency silos to product teams; don't copy the Spotify model |
| [[skills-self-assessment]] | Private 1-5 self-rating; anonymised aggregate informs team-level investment |
| [[kotters-change-model]] | Eight-step process for organisational change applied to microservice adoption |
| [[code-ownership-models]] | Strong, weak, collective; collective stops working past ~20 devs; strong "almost universal" past 100 |
| [[global-vs-local-optimization]] | Local team decisions compose into global duplication; cross-cutting forums without centralising |

## Microservices at scale

| Page | Description |
|---|---|
| [[breaking-changes]] | Eliminate accidental contract breakage or the architecture becomes untenable; structural vs semantic; three rules |
| [[consumer-driven-contracts]] | Pact-style consumer-written specifications; replace cross-service tests; "poorly underused" |
| [[end-to-end-testing]] | Large cross-team suites become slow and flaky; limit scope, use CDCs, lean on progressive delivery |
| [[cross-service-analytics]] | Split databases break single-schema analytics; push to a dedicated analytics database |
| [[local-developer-experience]] | JVM hits the laptop ceiling; stubbing, hybrid setups, Telepresence; ongoing investment |
| [[running-too-many-things]] | Manual deployment doesn't scale; serverless-first on cloud; Kubernetes when needed |
| [[desired-state-management]] | Declarative spec + continuous reconciliation; the operational counterpart to many small services |
| [[robustness-and-resiliency-at-scale]] | Two questions per call; isolation, time-outs, circuit breakers; document what you learn |
| [[orphaned-services]] | Services running for years with no owner; FT's Biz Ops and the System Operability Score |

## Observability

| Page | Description |
|---|---|
| [[monitoring-and-observability]] | From monitoring (known causes) to observability (open-ended questions); the murder-mystery quote |
| [[log-aggregation]] | Newman's "do this first" recommendation; ELK and Humio; an organisational litmus test |
| [[correlation-ids]] | Single ID propagated through call chains; the prerequisite for distributed tracing |
| [[distributed-tracing]] | Jaeger and friends; latency attribution where logs can't help |
| [[synthetic-transactions]] | Test in production via scripted fake users; the 200-washing-machines warning |

## Domain-driven design

| Page | Description |
|---|---|
| [[domain-driven-design]] | Eric Evans's discipline for modeling the problem domain in software |
| [[bounded-context]] | A larger organizational boundary with explicit responsibilities and hidden internals |
| [[aggregate]] | A real domain entity (Order, Invoice) with a self-governing state-machine life cycle |

## Coupling and cohesion

| Page | Description |
|---|---|
| [[coupling]] | Four types relevant to microservices: implementation, temporal, deployment, domain |
| [[cohesion]] | "The code that changes together, stays together"; business cohesion vs technology cohesion |
| [[information-hiding]] | Parnas's principle: stable interfaces hide what changes; the engine of independent deployability |

## Reliability concepts

| Page | Description |
|---|---|
| [[fault-tolerance]] | Preventing component faults from becoming system-wide failures |

## Scalability concepts

| Page | Description |
|---|---|
| [[load-parameters]] | Quantitative metrics describing current system load |
| [[response-time-percentiles]] | Why percentiles beat averages for measuring service performance |
| [[scaling-approaches]] | Vertical, horizontal, elastic, and manual scaling tradeoffs |

## Maintainability concepts

| Page | Description |
|---|---|
| [[accidental-complexity]] | Complexity from implementation choices, not the problem itself |

## Data models

| Page | Description |
|---|---|
| [[data-models]] | The layered abstraction concept; overview of the three dominant models |
| [[relational-model]] | SQL, tables, joins, history, and the query optimizer insight |
| [[document-model]] | JSON documents, schema flexibility, and data locality advantages |
| [[graph-data-models]] | Property graphs, triple-stores, Cypher, SPARQL, and Datalog |
| [[nosql]] | The NoSQL movement, driving forces, and polyglot persistence |

## Data modeling concepts

| Page | Description |
|---|---|
| [[object-relational-mismatch]] | Impedance mismatch between OOP code and relational tables |
| [[normalization]] | Removing duplication with IDs; the join trade-off |
| [[schema-on-read-vs-write]] | Enforcing schema at write time (relational) vs read time (document) |
| [[declarative-vs-imperative-queries]] | Why declarative languages (SQL, CSS) beat imperative APIs |
| [[data-locality]] | Adjacent storage for faster full-document reads; trade-offs |

## Storage engines

| Page | Description |
|---|---|
| [[storage-engines]] | Two families (log-structured vs update-in-place) and OLTP vs OLAP split |
| [[indexes]] | What an index is; read/write tradeoff; clustered, covering, multi-column, fuzzy |
| [[hash-indexes]] | Append-only log + in-memory hash map (Bitcask); segment compaction |
| [[sstables-and-lsm-trees]] | Sorted segments, memtable, LSM-tree, compaction strategies, Bloom filters |
| [[b-trees]] | Fixed-size pages, WAL, branching factor, comparison to LSM-trees |
| [[write-amplification]] | One logical write causing multiple physical writes; SSD impact |

## Analytics and warehousing

| Page | Description |
|---|---|
| [[oltp-vs-olap]] | OLTP (many small key lookups) vs OLAP (few huge scans for aggregates) |
| [[data-warehousing]] | ETL, star/snowflake schemas, fact and dimension tables |
| [[column-oriented-storage]] | Store by column not row; compression, vectorized processing, OLAP cubes |

## Encoding and compatibility

| Page | Description |
|---|---|
| [[backward-forward-compatibility]] | New code reads old data (backward); old code reads new data (forward); the two directions required for rolling upgrades |
| [[encoding-formats]] | Three categories: language-specific (avoid), textual (JSON/XML/CSV), binary schema-driven (Thrift/Protobuf/Avro) |
| [[schema-evolution]] | Field tags (Thrift/Protobuf) and writer's/reader's schema (Avro) as mechanisms for safe schema change over time |
| [[avro]] | Binary format with no field tags; writer's/reader's schema resolution; ideal for dynamically generated schemas |
| [[data-outlives-code]] | Database records encoded under old schemas persist long after the code that wrote them is gone |

## Service communication

| Page | Description |
|---|---|
| [[rpc]] | Remote procedure calls, why the local-call abstraction leaks, REST as the honest alternative, gRPC and modern RPC |
| [[message-brokers]] | Async message passing; buffering, fan-out, decoupling; the actor model and distributed actor frameworks |

## Replication

| Page | Description |
|---|---|
| [[replication]] | Hub page: why replicate, three architectures, sync vs async, the fundamental tension |
| [[leader-based-replication]] | Single-leader mechanics, sync vs async, WAL/statement/row-based/trigger replication methods |
| [[failover]] | Promoting a new leader; split brain; lost writes; the many ways automatic failover goes wrong |
| [[replication-lag]] | Async replication lag: the three anomalies and why they matter at scale |
| [[read-after-write-consistency]] | Guarantee that users always see their own writes; implementation strategies |
| [[monotonic-reads]] | Guarantee that reads never go backward in time; sticky replica approach |
| [[consistent-prefix-reads]] | Guarantee that causally related writes appear in order; the causality anomaly |
| [[eventual-consistency]] | The weakest useful guarantee: convergence with no time bound; operability implications |
| [[multi-leader-replication]] | Multiple leaders accept writes; multi-datacenter, offline-first, collaborative editing use cases |
| [[write-conflicts]] | Conflict detection and resolution: LWW, merge, CRDTs, custom logic, tombstones |
| [[leaderless-replication]] | Dynamo-style; any replica accepts writes; read repair; anti-entropy; sloppy quorums |
| [[quorums]] | w+r>n overlap guarantee; tuning; sloppy quorums; the many edge cases that break quorum safety |
| [[version-vectors]] | Per-replica version numbers; happens-before vs concurrent; sibling merging |

## Partitioning

| Page | Description |
|---|---|
| [[partitioning]] | Splitting datasets across nodes for scalability; terminology across systems |
| [[partitioning-strategies]] | Key-range vs hash partitioning and their trade-offs for range queries and load distribution |
| [[hot-spots]] | Disproportionate load on a single partition; skew causes and mitigation |
| [[consistent-hashing]] | Hash-based partition boundaries for CDNs; why the term is misleading for databases |
| [[partitioning-secondary-indexes]] | Document-partitioned (local) vs term-partitioned (global) secondary indexes across partitions |
| [[rebalancing-partitions]] | Strategies for redistributing partitions: fixed count, dynamic splitting, proportional to nodes |
| [[request-routing]] | Service discovery for partitioned databases: routing tiers, client-side awareness, ZooKeeper coordination |
| [[service-discovery]] | General problem of locating services across redundant machines; DNS, coordination services, gossip |

## Transactions

| Page | Description |
|---|---|
| [[transactions]] | Grouping reads and writes into all-or-nothing logical units for simplified error handling |
| [[acid]] | The four safety guarantees: Atomicity, Consistency, Isolation, Durability — and how each varies in practice |
| [[isolation-levels]] | The spectrum from weak to strong isolation; what each level prevents and allows |
| [[read-committed]] | Prevents dirty reads and dirty writes; the most basic useful isolation level |
| [[snapshot-isolation]] | MVCC-based consistent snapshots; valuable for backups and analytics but vulnerable to write skew |
| [[mvcc]] | Multi-version concurrency control: multiple committed versions for lock-free consistent reads |
| [[dirty-reads-and-dirty-writes]] | Two race conditions where transactions see or overwrite uncommitted data |
| [[read-skew]] | Nonrepeatable read anomaly: seeing the database at different points in time |
| [[lost-updates]] | Concurrent read-modify-write cycles silently overwriting each other; prevention strategies |
| [[write-skew]] | Two transactions read the same data but write different objects, violating a cross-object invariant |
| [[phantoms]] | One transaction's write changes another's search query results; predicate locks and index-range locks |
| [[serializability]] | Strongest isolation: serial-equivalent execution; three implementation approaches |
| [[two-phase-locking]] | Pessimistic serializability via shared/exclusive locks; readers and writers block each other |
| [[serializable-snapshot-isolation]] | Optimistic serializability (2008) atop snapshot isolation; detects conflicts at commit time |
| [[actual-serial-execution]] | Single-threaded execution with stored procedures; feasible when datasets fit in memory |

## Distributed systems challenges

| Page | Description |
|---|---|
| [[partial-failures]] | The defining characteristic of distributed systems: nondeterministic, partial breakdowns |
| [[unreliable-networks]] | Shared-nothing asynchronous networks; no delivery guarantees; queueing and congestion |
| [[network-faults]] | Practical prevalence of network problems; partitions; fault detection mechanisms |
| [[timeouts]] | The only sure fault detection mechanism; the long-vs-short dilemma; adaptive timeouts |
| [[unreliable-clocks]] | Time-of-day vs monotonic clocks; drift; why timestamps are dangerous for ordering |
| [[clock-synchronization]] | NTP limitations; GPS/PTP/atomic clocks; Google TrueTime; monitoring offsets |
| [[process-pauses]] | GC, VM suspension, disk I/O — causes of unpredictable delays; real-time systems |
| [[truth-and-leadership-in-distributed-systems]] | Why a node cannot trust its own judgment; quorum-based truth |
| [[fencing-tokens]] | Monotonically increasing tokens to reject stale lock holders; ZooKeeper implementation |
| [[byzantine-faults]] | Nodes that lie; Byzantine Generals Problem; where BFT matters and where it doesn't |
| [[system-models]] | Timing models and failure models for reasoning about distributed algorithm correctness |
| [[safety-and-liveness]] | Two categories of properties: safety (nothing bad) vs liveness (something good eventually) |

## Consistency and consensus

| Page | Description |
|---|---|
| [[linearizability]] | Strongest single-object consistency: atomic recency guarantee; cost and implementation |
| [[causal-consistency]] | Preserving cause-and-effect ordering; strongest model without coordination |
| [[lamport-timestamps]] | Sequence numbers consistent with causality; piggyback-maximum mechanism; limitations |
| [[total-order-broadcast]] | Reliable + totally ordered message delivery; equivalent to consensus |
| [[consensus]] | The fundamental agreement problem; FLP impossibility; Paxos/Raft/Zab; epoch numbering |
| [[two-phase-commit]] | Distributed atomic commit; coordinator failure and in-doubt blocking; not fault-tolerant |
| [[distributed-transactions]] | Transactions spanning nodes; XA; database-internal vs heterogeneous; operational problems |
| [[cap-theorem]] | Linearizability vs availability during partitions; historically important but practically limited |
| [[state-machine-replication]] | Deterministic replicas processing same operations in same order stay consistent |
| [[zookeeper]] | Coordination service: consensus-based primitives, failure detection, leader election |

## Batch processing

| Page | Description |
|---|---|
| [[batch-processing]] | The three system types (online, batch, stream); Unix-to-MapReduce-to-dataflow lineage |
| [[unix-philosophy]] | Do one thing well; uniform interface; separation of logic and wiring; transparency |
| [[mapreduce]] | Map, sort, reduce; distributed execution; fault tolerance; limitations |
| [[distributed-filesystems]] | HDFS architecture; NameNode; fault tolerance via replication; data locality |
| [[sort-merge-joins]] | Reduce-side joins: shuffle by key, secondary sort, skew handling techniques |
| [[map-side-joins]] | Broadcast hash join, partitioned hash join, map-side merge join |
| [[dataflow-engines]] | Spark/Tez/Flink: flexible DAGs, pipelining, in-memory state, RDD lineage |
| [[materialization-of-intermediate-state]] | Why MapReduce's full materialization is expensive; how dataflow engines improve it |
| [[batch-workflow-outputs]] | Search indexes, key-value stores, immutable inputs / replaceable outputs philosophy |
| [[hadoop-vs-mpp-databases]] | Schema-on-read vs up-front modeling; diversity of processing; fault tolerance design |
| [[graph-batch-processing]] | Pregel/BSP model: vertex-centric message passing in synchronized rounds |

## Stream processing

| Page | Description |
|---|---|
| [[stream-processing]] | Hub page: bounded vs unbounded data, core concepts, processing patterns |
| [[event-streams]] | What events are; producers, consumers, topics; delivery mechanisms |
| [[log-based-message-brokers]] | Kafka/Kinesis: partitioned append-only logs with consumer offsets and replay |
| [[change-data-capture]] | Making one database the leader for all derived systems via binlog/WAL parsing |
| [[event-sourcing]] | Storing application-level intent events; deriving state; CQRS |
| [[stream-joins]] | Three join types: stream-stream, stream-table, table-table |
| [[windowing]] | Event time vs processing time; tumbling, hopping, sliding, session windows |
| [[stream-processing-fault-tolerance]] | Microbatching, checkpointing, idempotent writes, atomic commits |

## Future of data systems

| Page | Description |
|---|---|
| [[data-integration]] | Making data available in the right form across multiple specialized systems |
| [[unbundling-databases]] | Decomposing database features into composable systems connected by event logs |
| [[lambda-architecture]] | Running batch and stream in parallel; problems and successors |
| [[derived-data]] | Data created by transforming a system of record; write path vs read path |
| [[end-to-end-argument]] | Infrastructure guarantees are insufficient; application-level operation IDs needed |
| [[exactly-once-semantics]] | Effectively-once via idempotence and end-to-end operation identifiers |
| [[timeliness-and-integrity]] | Two requirements conflated under "consistency"; decoupling them |
| [[coordination-avoidance]] | Maintaining integrity without synchronous coordination |
| [[data-ethics]] | Predictive analytics bias, surveillance, privacy, consent, engineer responsibility |
