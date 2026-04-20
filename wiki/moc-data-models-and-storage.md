# MOC: Data Models and Storage

**Summary**: Entry point for questions about *the shape of the store itself* — which data model fits the workload, which engine (LSM vs B-tree) fits the access pattern, how the schema will evolve without downtime, how the data replicates and partitions, and what the target storage looks like on the far side of a service extraction. Start here when the question is "what should this service's database actually look like?" rather than "how do we get data into or out of it?"

**Sources**: (meta-page; aggregates concept pages and links to raw chapters)

**Last updated**: 2026-04-19

---

## When to read this

You are designing — or inheriting — a system's system of record, and the question on the table is the *storage layer*: which database model, which engine internals, which schema shape, which replication topology, which partitioning strategy, which encoding format. This MOC is the target-side map. It is also the natural follow-up to [[moc-decomposition]] once the extraction has gotten past "can we split the code?" and landed at "what does the new service's database actually look like, and how does it change over time without breaking consumers?"

The canonical shape of a question that lands here: *"We need to pick a database for X"*, *"Our writes are getting slow — is it the engine?"*, *"We're sharding — key-range or hash?"*, *"We changed a field and deployments now break — how should we version?"*, *"What's the right target schema for a payments service pulled out of a shared Postgres?"* The answer is rarely one page; it is a combination of model + engine + encoding + replication + partitioning chosen for the workload.

Jurisdictional rule for this MOC:

- **This MOC** owns *model, engine, encoding, and storage-layer replication/partitioning*. It is the "what does the store look like" MOC.
- [[moc-data-processing]] owns *execution mechanics* — batch and stream engines, CDC as a source-capture mechanism, pipeline topology. It is the "how data moves through and is transformed" MOC.
- [[moc-data-engineering]] owns the *discipline view* — lifecycle, undercurrents, governance, data architecture patterns, the data-engineer role.
- *moc-consistency-and-transactions* (forthcoming) owns *correctness across stores* — ACID trade-offs, isolation levels, sagas, outbox, distributed transactions.

Shared concepts that live in more than one MOC (change-data-capture, Kafka, outbox, schema registry) are linked with a framing sentence here that reflects the *storage-layer* lens — not the execution or architectural lens.

## Data models — the first decision

Get the model right before arguing about the engine. A wrong model is the kind of mistake that no amount of index tuning fixes; a right model often makes the engine choice obvious.

- [[data-models]] — Kleppmann's layered-abstraction framing; application → database → disk; each layer's model hides the next. The starting page for the whole cluster. Read first.
- [[relational-model]] — tables, joins, query optimiser, the thirty-year monopoly-by-default. Still the right answer for most workloads most of the time; the cost of picking something else should be justified.
- [[document-model]] — JSON per record; schema flexibility; one-to-many natural fit; data locality for whole-document reads. Shines when a record is a coherent tree and querying rarely needs to join across trees.
- [[graph-data-models]] — property graphs and triple stores; Cypher, SPARQL, Datalog. The right answer when the relationships *are* the model (recommendation, social, knowledge graphs, fraud-ring detection) rather than decoration on top of entities.
- [[nosql]] — the movement itself; what it was reacting to; the split between document / wide-column / key-value / graph. Understand the motivation before you argue about the category.
- [[key-value-store]] — the simplest shape; cache, session, blob-keyed lookup. Redis, Memcached, DynamoDB in KV mode. Useful when the access pattern is truly "give me the thing keyed by this" and nothing else.
- [[wide-column-database]] — single-index row-key partitioning; Bigtable, Cassandra, HBase. The right shape for wide-tenant or high-cardinality keyed workloads where a row is the access unit and columns within it are sparse.
- [[search-database]] — Elasticsearch, Solr; text search, log analysis, full-text-plus-filters. Not an OLTP store — a derived one; feed it from the system of record.
- [[time-series-database]] — InfluxDB, TimescaleDB, Prometheus TSDB; write-heavy append-only with time as the dominant axis. IoT, metrics, ad-tech.
- [[polyglot-persistence]] — the payoff of per-workload model choice. Each service picks the storage technology that fits its workload; the overall architecture doesn't pay a global relational-schema tax for capabilities only one service needs. The natural end state of [[data-ownership]].

### Modelling concepts that cut across models

- [[object-relational-mismatch]] — the impedance mismatch between OOP objects and relational rows; the ORM exists because of it. Documents escape it at the cost of queryability; don't forget the trade.
- [[normalization]] — remove duplication with IDs, pay with joins. The relational default; the thing document models partially abandon.
- [[schema-on-read-vs-write]] — enforce schema at write time (relational) or at read time (document/lake). Write-time schemas catch errors early and pay migration costs; read-time schemas delay error discovery and pay it as runtime noise.
- [[declarative-vs-imperative-queries]] — why SQL beat hand-rolled traversal; what you lose when you reach for an imperative API on top of a declarative engine.
- [[data-locality]] — adjacent bytes read together. Document-shaped storage is fast for whole-document reads and slow for field-level reads; relational is the inverse.

Deeper reading: [[designing-data-intensive-applications#chapter-2-data-models-and-query-languages]] for the full model comparison. [[fundamentals-of-data-engineering#chapter-8-queries-modeling-and-transformation]] for modelling paradigms (Kimball, Inmon, data vault) on the analytical side.

## Storage engines — the second decision

The engine decides what the database is fast at. A B-tree store and an LSM store behave the opposite way under load; picking the wrong one is invisible at small scale and catastrophic at large scale.

- [[storage-engines]] — two families (log-structured, update-in-place); the OLTP vs OLAP split; the table stakes framing for the rest of this section. Read first.
- [[indexes]] — what an index *is*; every index is a read/write trade; clustered, covering, multi-column, fuzzy. The primary lever in the OLTP query plan.
- [[hash-indexes]] — Bitcask-style append-only log plus in-memory hash map; segment compaction; good when the working set fits in RAM and the key space is bounded. Mostly a pedagogical stepping stone to the LSM-tree.
- [[sstables-and-lsm-trees]] — sorted segments, memtable, compaction; Cassandra / RocksDB / LevelDB internals. Writes are fast; reads pay the compaction tax. Bloom filters cap the miss cost.
- [[b-trees]] — fixed-size pages, WAL, branching factor; the update-in-place incumbent behind InnoDB, Postgres, and every index-organised OLTP store since the 1970s. Reads are fast; writes pay the rewrite tax.
- [[write-amplification]] — the hidden cost; one logical write causes many physical writes. Decisive for SSDs; under-appreciated in "our writes are slow" incidents.
- [[oltp-vs-olap]] — many small key lookups vs few huge aggregate scans; the fault line that separates transactional from analytical engines. The right engine for one is the wrong engine for the other.
- [[column-oriented-storage]] — store by column, not row; compression collapses cardinalities; vectorised execution blows through scans. Parquet, ORC, Redshift, BigQuery, ClickHouse. The engine choice that makes warehouse-scale analytics tractable.

Deeper reading: [[designing-data-intensive-applications#chapter-3-storage-and-retrieval]] for the full LSM-vs-B-tree treatment; [[designing-data-intensive-applications#chapter-10-batch-processing]] for the column-storage-in-warehouses section.

## Database type selection — the Hard Parts rubric

When the choice is truly open — greenfield service, new workload, greenfield company — pick by trade-off rubric, not by reflex.

- [[database-type-selection]] — Ford and Richards's eight-family × eight-characteristic star-ratings matrix. The analytical alternative to "let's just use Postgres" and "let's just use DynamoDB." Shaped for the architect's objectivity stance; cross-links with [[trade-off-analysis]].
- [[newsql-database]] — CockroachDB, Spanner, YugabyteDB. NoSQL-scale with ACID semantics; the answer when you need both horizontal write scaling and strong consistency and aren't willing to compromise either. Historically expensive; increasingly viable.
- [[cloud-native-database]] — Snowflake, Redshift, BigQuery, Cosmos DB, Datomic. Storage/compute separation; elastic scaling; opex-shaped cost. The native cloud answer for analytics workloads and some operational ones.
- [[polyglot-persistence]] (re-cited here under selection) — the valid end state when one type isn't enough. Selection is *per service*, not *per organisation*.

## Encoding and schema evolution

Data outlives code. A field added today will be read by code written in a year. The encoding format and the schema discipline decide whether that is invisible or existential.

- [[encoding-formats]] — three families: language-specific (avoid), textual (JSON/XML/CSV — lowest common denominator), binary schema-driven (Thrift/Protobuf/Avro — the default for durable data). Each buys different compatibility properties.
- [[schema-evolution]] — field tags (Thrift/Protobuf) and writer's/reader's schemas (Avro) as the two mechanisms for safe change over time. Read the difference before you pick.
- [[backward-forward-compatibility]] — new code reads old data (backward), old code reads new data (forward). Rolling upgrades and mixed-version consumer fleets need both.
- [[avro]] — binary; no field tags; writer's and reader's schemas resolve at read time. The natural fit for dynamically generated schemas (CDC records, downstream of Kafka Connect); the first-choice encoding for event-driven systems.
- [[data-outlives-code]] — the motivating principle. Database records encoded under old schemas persist long after the code that wrote them is retired. Don't assume you'll get to migrate.
- [[data-contract]] — producer-consumer agreement enforced by format and registry; the decoupling mechanism under event-driven microservices. Storage-layer lens: the contract surface every durable write commits to forever.
- [[schema-registry]] — central store of schemas by subject and version; producers register; consumers fetch; compatibility modes are enforced at registration time, not at runtime. The operational prerequisite for binary schema-driven encodings at scale.
- [[code-generation]] — typed producer/consumer classes generated from schemas; compile-time safety at the cost of build-time ceremony. Refactor-friendliness is the under-appreciated benefit.
- [[explicit-vs-implicit-schemas]] — why explicit always beats implicit; the cost of implicit schemas is paid as consumer fragility the writer never sees.

Deeper reading: [[designing-data-intensive-applications#chapter-4-encoding-and-evolution]]. [[building-event-driven-microservices#chapter-3-communication-and-data-contracts]] for the event-driven angle on contracts and registries.

## Replication — copies for availability, latency, and survivability

You replicate because the single-node alternative is a single point of failure, a single point of saturation, and a single point of latency. Every replication choice is a trade between convergence speed and write performance; there is no neutral default.

- [[replication]] — the hub: why replicate, three architectures, sync vs async, the fundamental tension. Start here.
- [[leader-based-replication]] — single leader accepts writes; followers replicate asynchronously; the most common shape by far. WAL / statement / row / trigger-based methods, each with different semantics.
- [[failover]] — promoting a new leader; split-brain; lost writes; the automatic-failover bestiary of failure modes. The most common operational nightmare in leader-based systems.
- [[replication-lag]] — the price of async replication; the three user-visible anomalies.
- [[read-after-write-consistency]] — users see their own writes even under lag. Implementable per-user rather than system-wide.
- [[monotonic-reads]] — reads never go backwards in time. Sticky-replica is the cheap fix.
- [[consistent-prefix-reads]] — causally related writes appear in order. The subtle one; shows up in multi-shard reads.
- [[eventual-consistency]] — convergence with no time bound. The weakest useful guarantee; the right one for most cross-service reads; the wrong one for money at the moment of charge.
- [[multi-leader-replication]] — more than one leader accepts writes; multi-datacenter, offline-first apps, and collaborative editing use cases. Conflict is inherent.
- [[write-conflicts]] — detection and resolution: last-write-wins (bad for most cases), merge, CRDTs, custom logic, tombstones.
- [[leaderless-replication]] — Dynamo-style; any replica accepts writes; read repair; anti-entropy; sloppy quorums. Cassandra, DynamoDB.
- [[quorums]] — w + r > n overlap; sloppy quorums and their edge cases. The math is correct only under assumptions that production regularly violates.
- [[version-vectors]] — per-replica version numbers; happens-before vs concurrent; the mechanism that lets leaderless systems detect conflicts rather than silently resolve them.

Deeper reading: [[designing-data-intensive-applications#chapter-5-replication]] for the full treatment.

Cross-links to sibling MOCs: *moc-consistency-and-transactions* (forthcoming) owns [[linearizability]] and the consistency-model spectrum that replication choices force; *moc-distributed-systems* (forthcoming) owns [[partial-failures]] and [[unreliable-networks]] as the reason replication exists in the first place.

## Partitioning — splits for scale

Partitioning (sharding) is replication's sibling: replication gives you multiple copies of the same data; partitioning gives you one copy of different data on each node. You'll likely need both. Every partitioning choice is a trade between range-query friendliness and load balance.

- [[partitioning]] — the hub: why split, terminology across systems, the relationship to replication. Start here.
- [[partitioning-strategies]] — key-range vs hash partitioning; the first decision. Key-range keeps range scans cheap and risks hot spots on skewed keys; hash eliminates hot spots and ruins range scans.
- [[hot-spots]] — disproportionate load on one partition; skew causes (celebrity users, time-ordered keys, natural distributions); mitigation via salting, sub-partitioning, or choice of key.
- [[consistent-hashing]] — hash-based partition boundaries; the 1997 CDN algorithm often mis-applied to databases where its guarantees don't match the problem. Read the page; don't reach for the name by reflex.
- [[partitioning-secondary-indexes]] — document-partitioned (local, scatter-gather reads) vs term-partitioned (global, scatter-gather writes). The choice that decides which query shape is painful.
- [[rebalancing-partitions]] — fixed count, dynamic splitting, proportional to nodes. The second-hardest operational problem after failover.
- [[request-routing]] — service discovery for partitioned stores; client-side awareness, routing tier, ZooKeeper-coordinated topology. The question every client of a partitioned database answers one way or another.

Deeper reading: [[designing-data-intensive-applications#chapter-6-partitioning]].

See [[database-decomposition]] on [[moc-decomposition]] for the extraction-time partitioning story; this MOC's lens is steady-state shaping of the new store.

## Analytical storage — warehouses, lakes, lakehouses

Operational stores support the business as it runs; analytical stores support the business making sense of itself. The engines, models, and economics differ enough that the second needs its own design vocabulary.

- [[operational-vs-analytical-data]] — the first structural distinction; drives decomposition decisions and engine choices. OLTP boundaries are the operational dataset; analytics derive from them via pipelines.
- [[data-warehousing]] — the OLAP-dedicated database; Inmon's definition; the organisational vs technical frame; the cloud-warehouse reshaping. Still the workhorse.
- [[data-mart]] — refined warehouse subset per department; a deliberate trade that pays analyst-friendliness with storage duplication.
- [[data-lake]] — raw-first, schema-on-read; the 1.0 failures ("data swamp"); convergence with warehouses.
- [[data-lakehouse]] — lake foundation plus warehouse guarantees (ACID, schema, transactions); the 2020s-era convergent platform. Delta Lake, Iceberg, Hudi as the enabling table formats.
- [[lakehouse-table-formats]] — Delta, Iceberg, Hudi; ACID plus history over object storage. The specific mechanism under the lakehouse category.
- [[modern-data-stack]] — cloud plug-and-play; the current default assembly for a new data team.
- [[storage-compute-separation]] — object storage plus ephemeral compute; multitier caching; the economic shape of cloud analytical storage. The native pattern for all the above.

### Analytical modelling paradigms

- [[inmon-model]] — top-down 3NF integration; department marts downstream. Strong for regulated, multi-source environments.
- [[kimball-model]] — bottom-up facts and dimensions in star schemas. The analyst-legible default for most BI.
- [[star-schema]] — fact table centred; dimensions radiating; few joins; the canonical analytical shape.
- [[snowflake-schema]] — normalised star; less common in practice than the plain star.
- [[fact-table]] — immutable, append-only, numeric, long-and-narrow. Grain rule is the beating heart of dimensional modelling.
- [[dimension-table]] — descriptive, wide, short, surrogate-keyed. Conformed dimensions are the integration lever across marts.
- [[slowly-changing-dimensions]] — Type 0/1/2/3; Type 2 is the standard. Determinism technique for stream-table joins points back into [[moc-data-processing]].
- [[data-vault]] — Linstedt's hubs + links + satellites; insert-only, schema-stable; agile under change.
- [[wide-denormalized-table]] / [[one-big-table]] — the no-modelling extremes; fast to start, expensive to trust.
- [[streaming-data-modeling]] — the unsettled frontier; flexible schemas, nested columns, trust-the-source-system defaults.

Deeper reading: [[fundamentals-of-data-engineering#chapter-8-queries-modeling-and-transformation]] covers the paradigm catalogue. [[designing-data-intensive-applications#chapter-10-batch-processing]] covers the columnar-storage engine story that makes warehouses fast.

## Storage raw ingredients — the cloud layer underneath

Before the database, before the warehouse, there are bytes on disks in racks on networks. The modern data engineer lives one layer above these ingredients and is nonetheless accountable for the cost and latency shape they impose.

- [[storage-raw-ingredients]] — HDD vs SSD vs RAM; networking; CPU; serialisation; compression; caching hierarchy. The Reis–Housley base-layer tour.
- [[object-storage]] — S3, GCS, Azure Blob; immutable key-value blobs; eventual-to-strong consistency depending on the service; storage classes and lifecycle rules. The foundation of every cloud analytical stack.
- [[block-storage]] — raw blocks, RAID, SAN, EBS, instance volumes. What databases sit on; what object storage hides.
- [[file-storage]] — local filesystems, NAS, cloud filesystem services; the POSIX-like layer on top of blocks. Useful for shared read-write workloads that don't want to speak to object storage.
- [[compression-algorithms]] — gzip, bzip2, snappy, LZ4, LZMA, zstd. The speed-vs-ratio axis; picks are per-column in columnar formats.
- [[cache-memory-storage]] — Memcached, Redis as the RAM-tier store; the latency floor for operational reads.
- [[streaming-storage]] — Kafka, Pulsar, Kinesis, Pub/Sub as *long-retention storage*, not just transport. Durable logs as primary records, tiered offload to object storage. The mechanism that lets [[event-sourcing]] and [[event-as-single-source-of-truth]] work in production.
- [[data-retention]] — value, time, compliance, cost; the lifecycle-automation layer most organisations underinvest in.
- [[data-platform]] — vendor-curated ecosystem around a storage core; the walled-garden trade.

Deeper reading: [[fundamentals-of-data-engineering#chapter-6-storage]].

## Per-service data ownership — the target shape

When this MOC is entered from [[moc-decomposition]], the live question is *what should the new service's store actually look like?* The answer is the composition of every section above — plus a discipline that belongs here rather than on the extraction playbook.

- [[data-ownership]] — Ford and Richards's writer-owns rule. One service, one writer per table; reads do not confer ownership. The storage-layer consequence of [[independent-deployability]].
- [[data-sovereignty]] — the end-state outcome of a data decomposition: one owner per database. The antonym of [[shared-database-antipattern]] as a terminal state.
- [[data-domain]] — groups of tables forming the unit of ownership and extraction; the soccer-ball model. Ideally one bounded context per data domain; the alignment makes per-service data sovereignty actually achievable.
- [[data-decomposition-drivers-and-integrators]] — the six-vs-two rubric justifying a database split. The rubric lives here because it governs the shape of the new store on both sides of the split.
- [[database-decomposition]] — re-cited from [[moc-decomposition]] as the bridge. This MOC's lens: the target end state, not the migration.
- [[joint-ownership-techniques]] — four resolutions for legitimately-shared tables (table split, data domain, delegate, service consolidation). Pick by trade-off.
- [[table-split-technique]] / [[delegate-technique]] — two of the four resolutions worth calling out; the first splits columns across services, the second centralises writes through a single delegate.
- [[distributed-data-access]] — once data is per-service, *reads* across the fleet need a story. Four patterns trade latency, staleness, fault coupling, and storage cost differently.
- [[column-schema-replication-pattern]] / [[replicated-caching-pattern]] / [[data-domain-pattern]] / [[interservice-communication-pattern]] — the four *Hard Parts* Ch 10 patterns; each is a different answer to "I need data the other service owns."

Cross-link: see [[moc-microservices]]'s *Data ownership* section for the microservice-style framing of these patterns; this MOC carries the storage-shape detail.

## Sibling MOCs

Once the corresponding MOCs land, the handoffs below become wikilinks. For now they're plain pointers to where the jurisdictional boundary sits.

- [[moc-data-processing]] — owns batch and stream execution mechanics, pipelines, schedulers, CDC as a source-capture mechanism, Lambda/Kappa/Dataflow. This MOC owns the shape of the store; the processing MOC owns how data moves through and is transformed.
- [[moc-data-engineering]] — owns the discipline view: the data-engineering lifecycle, the six undercurrents (governance, security, data management, data modelling as a discipline, quality, observability), data architecture patterns (mesh, lakehouse, modern data stack), technology selection. This MOC owns the *what* of the store; the engineering MOC owns the *how we run the practice that builds on top of it*.
- *moc-consistency-and-transactions* (forthcoming) — owns ACID, isolation levels, serialisation, distributed transactions, sagas and outbox as the correctness-across-stores mechanism. This MOC names [[eventual-consistency]] as a replication outcome and [[transactions]] as what you lose when a database splits; the consistency MOC owns the deeper trade-offs.
- *moc-distributed-systems* (forthcoming) — owns [[partial-failures]], [[unreliable-networks]], [[unreliable-clocks]], [[consensus]]. This MOC's replication and partitioning sections cite those concepts; the distributed-systems MOC owns them end-to-end.
- *moc-events-and-streaming* (forthcoming) — owns event-driven architecture, broker topology, event design, schema evolution *for events*. This MOC shares [[avro]] and [[schema-registry]] with that one under a storage-layer lens; the events MOC owns the broker-as-integration-substrate view.
- [[moc-decomposition]] — owns the migration playbook for extracting a service from a monolith, including the database split itself. This MOC picks up *after* the split — the new store's steady-state shape.
- [[moc-microservices]] — owns the running-microservices view in which "own your own data" is a defining discipline. This MOC picks up where the microservices MOC hands off: the specifics of what that owned store should look like.
- [[moc-domain-driven-design]] — owns bounded contexts and aggregates as the modelling vocabulary. This MOC takes [[data-domain]] and [[bounded-context]] alignment as given; the DDD MOC owns how those boundaries are found.

## Related pages

- [[index]]
- [[designing-data-intensive-applications]]
- [[fundamentals-of-data-engineering]]
- [[software-architecture-the-hard-parts]]
- [[data-models]]
- [[relational-model]]
- [[document-model]]
- [[graph-data-models]]
- [[nosql]]
- [[storage-engines]]
- [[sstables-and-lsm-trees]]
- [[b-trees]]
- [[oltp-vs-olap]]
- [[column-oriented-storage]]
- [[encoding-formats]]
- [[schema-evolution]]
- [[avro]]
- [[schema-registry]]
- [[replication]]
- [[partitioning]]
- [[database-type-selection]]
- [[polyglot-persistence]]
- [[data-ownership]]
- [[data-domain]]
- [[data-warehousing]]
- [[data-lakehouse]]
- [[object-storage]]
