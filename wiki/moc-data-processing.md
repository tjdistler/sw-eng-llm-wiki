# MOC: Data Processing

**Summary**: Entry point for questions about *data in motion* — getting it in, moving it around, transforming it, and serving it back out. Covers ingestion (batch and streaming, push and pull, CDC as source-capture), batch engines (MapReduce through Spark/Flink), stream engines (Kafka Streams / Flink / Beam), stateful streaming, pipeline architectures (Lambda / Kappa / Dataflow), the operational shape of running pipelines (periodic vs continuous, Google Workflow), querying and transformation mechanics, serving targets, and data-integrity defences. Start here when the question is "how should this data flow, compute, and land?" rather than "what does the store look like?"

**Sources**: (meta-page; aggregates concept pages and links to raw chapters)

**Last updated**: 2026-04-19

---

## When to read this

You have — or are about to have — data that moves. The design surface in front of you is one of *ingestion, transformation, pipeline topology, execution engine, or serving*: how data enters the system, how it is processed, what engine does the processing, how the pipeline survives partial failure, and how results get to consumers. This MOC is the execution-mechanics map.

The canonical shape of a question that lands here: *"Should this pipeline be batch or streaming?"*, *"We have a Spark job that keeps dying — is it the engine or the topology?"*, *"When should I use CDC vs Kafka Connect vs a nightly dump?"*, *"Our Lambda architecture is painful; should we go Kappa?"*, *"Our Airflow DAGs are flaky — is the problem the scheduler or our pipeline design?"*

Jurisdictional rule for this MOC:

- **This MOC** owns *execution mechanics* — batch and stream engines, pipeline topologies, schedulers, CDC as a *source-capture mechanism*, Lambda/Kappa/Dataflow as pipeline-architecture choices, ingestion and serving stages as FoDE frames them. It is the "how data flows and computes" MOC.
- [[moc-data-models-and-storage]] owns the *shape of the store* — data models, engines (LSM vs B-tree), encoding, replication, partitioning, warehouse/lake/lakehouse shape, per-service data ownership.
- [[moc-data-engineering]] owns the *discipline view* — lifecycle, undercurrents, governance, quality, data architecture patterns, the role of the data engineer.
- [[moc-events-and-streaming]] owns the *architectural use of events* — brokers as integration substrate, choreography vs orchestration between services, [[saga]], [[outbox-table-pattern]] as the publication pattern, event design.

Shared concepts that live in more than one MOC (CDC, Kafka, outbox, schema registry, log compaction) are linked here with a framing sentence that reflects the *execution-mechanics lens* — not the storage-shape or architectural-events lens.

## Ingestion — getting data in

Ingestion is the seam between source systems the data engineer doesn't control and the processing stack the data engineer does. Every ingestion choice is a trade between latency, completeness, load on the source, and schema discipline.

- [[data-pipeline]] — Reis and Housley's fluid definition; modern pipelines include ETL, ELT, reverse ETL, and data sharing as parts of one continuous flow. Start here for the framing.
- [[data-ingestion]] — the stage itself; batch vs streaming; push vs pull; the streaming-first checklist that flips the default for greenfield pipelines.
- [[ingestion-frequency]] — batch / micro-batch / real-time; why "real-time" is always near-real-time; how batch downstream defeats upstream streaming gains. The decision that sets the latency budget for everything after it.
- [[push-vs-pull-vs-poll]] — three directional patterns; who initiates; where each fits; why the lines blur once webhooks and CDC enter the picture.
- [[ingestion-payload]] — the five characteristics (kind, shape, size, schema/types, metadata) that determine whether a pipeline can process at all.
- [[snapshot-vs-differential-ingestion]] — full dump vs incremental delta; the "missing intermediate changes" pitfall that pushes the serious data engineer toward CDC.
- [[file-based-ingestion]] — the still-dominant pattern; object storage / SFTP / SCP / S3 drop-offs; CSV vs Parquet/Avro/ORC as the format choice.
- [[managed-connector]] — Fivetran, Airbyte, Matillion, Stitch. Outsource the undifferentiated plumbing; read the catalogue before writing your own adapter.
- [[dead-letter-queue]] — error-segregation topic; three schema-evolution defences; poison-message containment. The quiet discipline that keeps pipelines running under real-world input.
- [[data-migration]] — one-time bulk moves; schema subtleties; pipeline connection cut-over as the underappreciated hard part.
- [[web-scraping]] / [[edi]] / [[transfer-appliance]] — the long tail of ingestion: scraping, legacy EDI, physically shipped drives. Still relevant in 2026.

### Change data capture — the source-capture lens

CDC appears in three MOCs. Here its lens is *source capture*: a mechanism that turns a database's own change log into a stream of events the processing stack can consume without polling or transaction coupling.

- [[change-data-capture]] — making one database the leader for all derived systems via binlog/WAL parsing. The mechanism behind Debezium, Kafka Connect CDC connectors, and every modern data-lake ingestion pipeline that isn't a nightly snapshot. The structural complement to [[data-outlives-code]].
- [[query-based-cdc]] — periodic polling of source tables; simple, but lossy and load-bearing on the database. The shape most teams should leave behind.
- [[cdc-triggers]] — trigger-based CDC that inserts into a change table; precise but intrusive. Read-heavy DBAs refuse on principle; sometimes worth the principle-violation anyway.
- [[outbox-table-pattern]] — atomic write of business state plus a pending-event row; a poller streams it out. The CDC variant that gives *application semantics* rather than raw row events. Shared with *moc-events-and-streaming* (the publication pattern for event-driven microservices) and *moc-consistency-and-transactions* (the correctness bridge across a saga step). Here its lens is source-capture at the application layer.
- [[data-liberation]] — the broader Bellemare framing: extracting data from legacy siloed systems into event streams so downstream consumers (EDM, lakes, warehouses) can use it. CDC is one liberation mechanism among several.
- [[eventification]] — the act of turning request-response APIs or legacy data into first-class events. The umbrella above CDC when the source is an API rather than a database.

Deeper reading: [[fundamentals-of-data-engineering#chapter-7-ingestion]] for the full ingestion treatment; [[building-event-driven-microservices#chapter-4-integrating-event-driven-architectures-with-existing-systems]] for the CDC-liberation angle; [[designing-data-intensive-applications#chapter-11-stream-processing]] for the CDC-as-stream-source framing.

## Batch processing — bounded inputs, engines, and joins

Batch processing is the original shape of data engineering: bounded input, a long computation, durable output, retry on failure. The dominant engines changed (MapReduce → Spark / Flink / Beam) but the design vocabulary stayed largely the same.

- [[batch-processing]] — the hub: the three system types (online, batch, stream); the Unix-to-MapReduce-to-dataflow lineage. Start here.
- [[unix-philosophy]] — do one thing well, uniform interface, separation of logic from wiring, transparency. The design substrate Kleppmann traces forward through all of batch.
- [[mapreduce]] — map, sort, reduce; distributed execution; explicit materialisation between stages; the foundational programming model, and the one Google itself has mostly retired.
- [[distributed-filesystems]] — HDFS and successors; NameNode architecture; replication for fault tolerance; data locality as the historical performance lever.
- [[dataflow-engines]] — Spark, Tez, Flink. Flexible DAGs beat the MapReduce-stage straitjacket; pipelining beats full materialisation; in-memory state and RDD-style lineage beat write-everything-to-disk. The modern default.
- [[materialization-of-intermediate-state]] — the cost MapReduce paid that dataflow engines partially escape; why disk write-back dominates MapReduce runtime in real pipelines.
- [[batch-workflow-outputs]] — search indexes, key-value stores, immutable inputs / replaceable outputs philosophy. The discipline that makes batch idempotent and safely re-runnable.
- [[hadoop-vs-mpp-databases]] — schema-on-read vs up-front modelling; diversity of processing; fault-tolerance design. The architectural choice underneath "data lake vs warehouse."
- [[graph-batch-processing]] — Pregel / BSP model; vertex-centric message passing in synchronised rounds. The specialised case when the data is a graph and the computation is graph-shaped.

### Batch joins

- [[sort-merge-joins]] — reduce-side; shuffle by key; secondary sort; skew-handling techniques (salting, sampling, stragglers). The default when both sides are large.
- [[map-side-joins]] — broadcast hash join, partitioned hash join, map-side merge join. Cheap when you can arrange the inputs to co-locate; the right answer far more often than junior engineers reach for it.
- [[broadcast-join]] (re-cited from warehouse context) — the small-side-to-every-node strategy; applies in both SQL warehouses and dataflow engines.
- [[shuffle-hash-join]] — both sides repartitioned by hash of join key; the expensive default. Watching shuffle bytes is the primary batch-job performance lever.

Deeper reading: [[designing-data-intensive-applications#chapter-10-batch-processing]] for the end-to-end treatment.

## Stream processing — unbounded inputs, windows, and time

Stream processing is what batch becomes when you take the bounded-input assumption away. Everything gets harder: time, state, ordering, fault tolerance. The pay-off is latency that batch architectures cannot match.

- [[stream-processing]] — the hub: bounded vs unbounded data; core concepts; the processing-pattern catalogue. Start here.
- [[event-streams]] — what events are; producers, consumers, topics; delivery mechanisms. The primitive all stream processing stacks build on.
- [[log-based-message-brokers]] — Kafka, Kinesis, Pulsar. Partitioned append-only logs with consumer offsets, replay, and multi-consumer fan-out. The substrate that turned stream processing from a niche into the default for a whole class of workloads.
- [[message-brokers]] — the broader family; the non-log forms (RabbitMQ, ActiveMQ) and what they trade away for different properties.

### Event shape and partitioning

- [[event-structure]] — key + value + metadata + timestamp; the envelope every event is a specialisation of.
- [[unkeyed-event]] / [[keyed-event]] / [[entity-event]] — three event-type patterns. Unkeyed events are append-only facts; keyed events co-locate by ID; entity events carry full entity state as the compacted-stream payload.
- [[tombstone]] — null-valued event signalling deletion; the deletion mechanism under [[log-compaction]].
- [[log-compaction]] — broker-side retention by key; keep the latest value per key forever. The mechanism that turns an entity stream into a durable key-value store.
- [[table-stream-duality]] — every stream implies a table; every table implies a stream. The theoretical core of modern stream processing; once you internalise it, a lot of stateful-streaming design becomes obvious.
- [[repartitioning]] — rekeying and reshuffling a stream to co-locate data for joins and aggregations. The broker-as-shuffle move in lightweight frameworks; the network-shuffle move in heavyweight ones.
- [[copartitioning]] — partitioning two streams on the same key and partition count so matching keys land together. The prerequisite for efficient stream-stream and stream-table joins.
- [[single-writer-principle]] — one microservice, one stream: the write-ownership rule that keeps sources unambiguous and compacted streams durable. Framed here under its execution-mechanics lens; see also [[moc-microservices]] for the organisational lens.
- [[consumer-group]] — the mechanism that horizontally scales event consumers across processes while preserving per-partition order — each partition is owned by exactly one group member at a time. The primitive under "parallelise this consumer" in Kafka/Kinesis/Pulsar.
- [[consumer-offset]] — the per-consumer, per-partition cursor into a log; the thing that makes replay, at-least-once, and effectively-once semantics mechanically tractable. Storage of the offset (in the broker, in an external store) is a commit-atomicity decision, not a detail.
- [[partition-assignor]] — the component that decides which partitions each consumer-group member owns when membership changes. Range vs round-robin vs sticky assignors trade rebalance time against data-locality across restarts; picking one is an operational decision with latency consequences.

### Stream transformations

- [[stateless-stream-processing]] — transformations that need no accumulated state; map, filter, flatMap, branch, merge. The scalability default; reach for stateful only when the computation actually needs it.
- [[event-transformations]] — per-event functions; the workhorse operators in any stream framework.
- [[stream-branching-and-merging]] — predicate-based splitting; union / merge of streams into one. The routing primitives.
- [[stream-joins]] — stream-stream, stream-table, table-table. The three join shapes; each has different latency, state, and correctness properties.
- [[stream-table-table-join]] — the three-way enrichment pattern; the "enrich a live stream with two slowly-changing reference tables" shape.

### Time, determinism, and out-of-order events

- [[deterministic-stream-processing]] — same input streams → same output streams. The reprocessing prerequisite; the property that makes replay safe and debugging tractable.
- [[event-timestamps]] — event time vs ingestion time vs processing time. The clock the system uses is the correctness-critical choice; event time is usually the right answer.
- [[event-scheduling]] — the runtime discipline of picking which event to process next; how processors advance their internal clocks.
- [[watermarks]] — a progressing notion of "time has passed"; the signal that windows can close. Flink, Beam, Kafka Streams implementations all converge on this.
- [[stream-time]] — the processor's internal clock, derived from observed event timestamps.
- [[out-of-order-events]] / [[late-arriving-events]] — events whose timestamps go backwards relative to the stream. Grace periods, side outputs, and explicit handling are the design options.
- [[windowing]] — tumbling, hopping, sliding, session windows. The primary way stream processing carves unbounded input into bounded computations.
- [[reprocessing-event-streams]] — replay from the beginning to rebuild derived state or apply new logic. The operational capability that separates "stream as transport" from "stream as system of record."

Deeper reading: [[designing-data-intensive-applications#chapter-11-stream-processing]]. [[building-event-driven-microservices#chapter-5-event-driven-processing-basics]] for the stream-processor-engineering basics; [[building-event-driven-microservices#chapter-6-deterministic-stream-processing]] for the determinism discipline.

## Stateful streaming

Stateful streaming is where stream processing gets real — and where most of the hard operational work lives. State stores have to survive process crashes, rebalances, and scale events; the discipline is how to make that happen without inventing a new distributed database under every service.

- [[stateful-stream-processing]] — processors that accumulate state across events; aggregations, joins, enrichment. The hub page.
- [[materialized-state]] — a table view derived from a stream; the query surface for key lookups. The output shape of most stateful topologies.
- [[state-store]] — the abstraction for durable per-processor state; internal, external, or global.
- [[internal-state-store]] — state co-located with the processor; backed by a changelog stream; the recommended default (Kafka Streams style). Local SSD latency with broker-durable recovery.
- [[external-state-store]] — state held in a remote database; flexibility at the cost of network latency and fault-coupling.
- [[global-state-store]] — fully replicated on every processor instance; for small shared reference data (currency rates, feature flags, country codes).
- [[changelog-stream]] — the compacted stream that backs an internal state store; enables rebuilds and hot replicas.
- [[hot-replicas]] — standby processor instances tailing the changelog; the mechanism by which stateful services fail over quickly.
- [[state-store-rebuilding-vs-migrating]] — the restart trade-off: replay the changelog, or copy state from a peer. Recovery time vs network-traffic trade.
- [[effectively-once-processing]] — exactly-once semantics *in practice*: idempotence plus transactional offset commits. The name is a humility marker — the thing users want is almost-always effectively-once, and the engineering cost of true exactly-once often exceeds the value.
- [[stream-processing-fault-tolerance]] — microbatching, checkpointing, idempotent writes, atomic commits. The engine-internals survey.
- [[checkpointing-stream-processing]] — periodic durable snapshots of operator state and offsets; the recovery primitive under Flink and Spark Structured Streaming.
- [[stream-processing-scaling-strategies]] — two fundamentally different approaches: scale-while-running (online rebalance) vs scale-by-restart (checkpoint, stop, reconfigure, resume). State size and acceptable downtime decide which one the framework can even offer.

### Heavyweight framework execution — clusters, shuffles, multitenancy

These are the operational mechanics of running Spark / Flink / Kafka-Streams-at-scale. Distinct from the programming model; the place most production incidents actually live.

- [[stream-processing-cluster]] — the dedicated-pool execution model: master nodes schedule work, executor nodes run jobs. The shape the heavyweight streaming frameworks inherited from their batch ancestors.
- [[application-submission-modes]] — driver-in-client vs driver-in-cluster modes for submitting heavyweight streaming jobs. The choice that decides whether the client machine is a critical-path failure domain.
- [[external-shuffle-service]] — a sidecar service that holds shuffle data independent of executor lifetime, so an executor crash doesn't force a full stage recompute. The operational win that turns long streaming jobs from "fragile" into "recoverable."
- [[multitenancy-in-streaming-clusters]] — running many jobs on one shared pool: resource contention, noisy neighbours, per-tenant quotas. The engineering tax that buys hardware-cost efficiency; the reason dedicated clusters keep returning for latency-sensitive jobs.

Deeper reading: [[building-event-driven-microservices#chapter-7-stateful-streaming]] for the full stateful-streaming discipline.

## Pipeline architectures — Lambda, Kappa, Dataflow

At the architectural level, the pipeline-topology question is which of three shapes you commit to. Each was the consensus answer in its era; each still has live adherents.

- [[lambda-architecture]] — Marz's batch + speed + serving layers. Historically influential; operationally painful (two codepaths, two correctness stories). Most teams should understand it for legacy systems, and not reach for it on greenfield.
- [[kappa-architecture]] — Kreps's 2014 stream-only alternative. One codepath, reprocessing replaces the batch layer, serving derives from materialised state. The default for event-driven stacks.
- [[dataflow-model]] — Google's / Apache Beam's "batch as a special case of streaming" framing. The synthesis: one programming model, one set of time-and-windowing primitives, either execution mode from the same code. The direction the industry is converging on.
- [[stream-transform-load]] — STL: the streaming-era successor to ELT. Transformation happens *in the stream*, not after a load step. A FoDE Ch 11 prediction that has aged well.
- [[live-data-stack]] — the streaming-first successor to the modern data stack. Apps, analytics, and ML co-exist over shared streaming infrastructure. Still emerging as a consensus shape.

Cross-link: compare and contrast with [[iot-architecture]] — devices, gateways, constrained-network ingestion, reverse-ETL control loops — which has its own topology discipline.

Deeper reading: [[fundamentals-of-data-engineering#chapter-3-designing-good-data-architecture]] for the FoDE framing of the three; [[designing-data-intensive-applications#chapter-12-the-future-of-data-systems]] for Kleppmann's synthesis.

## Pipeline operations — periodic vs continuous, schedulers, correctness

The architecture is half the story; the operational shape of a running pipeline is the other half. Google's SRE Ch 25 is the key prose — the argument against periodic pipelines and the case for continuous processing.

- [[data-processing-pipelines]] — SRE Ch 25 hub: the operational pathology of large-scale periodic pipelines and Google's continuous-processing alternative. Start here.
- [[periodic-pipeline]] — cron-scheduled chained-program design pattern; the depth metric; stable when carefully tuned, fragile under organic growth.
- [[pipeline-uneven-work-distribution]] — the hanging-chunk problem; end-to-end runtime capped by the largest chunk; kill-and-restart wastes everything because pipelines have no checkpointing.
- [[pipeline-batch-scheduling-drawbacks]] — open-ended startup latency, preemption risk, execution-frequency floor. Why "just run it more often" fails past a certain point.
- [[pipeline-monitoring-problems]] — collect-during, report-on-completion is a structural blind spot. Mid-run failures produce no statistics. Continuous pipelines escape this by construction.
- [[pipeline-thundering-herd]] — synchronised worker spawn at cycle start; engineers add workers and make it worse. Only real fix is to stop being periodic.
- [[moire-load-pattern]] — multiple pipelines whose schedules drift into occasional alignment and produce aggregate spikes. Visible only in stacked plots.
- [[continuous-data-processing]] — the architectural alternative the chapter advocates. Workers never stop; work flows in continuously. Structurally avoids every periodic-pipeline failure mode.

### Google Workflow — a reference-grade continuous pipeline

- [[google-workflow]] — Google's 2003 system: leader-follower + system prevalence + MVC framing. Task Master as model, stateless workers as view.
- [[task-master]] — the in-memory model at the heart of Workflow; mutations synchronously journaled; bulk data in the distributed filesystem; only pointers in memory.
- [[system-prevalence-pattern]] — in-memory model + synchronous mutation journal + periodic snapshots. Conceptually identical to Redis AOF, event sourcing, and in-memory databases with WAL.
- [[workflow-correctness-guarantees]] — the four structural mechanisms for exactly-once semantics: configuration tasks as barriers, lease-bound commits, unique output filenames, server-token validation. Correctness *without* requiring idempotent payloads.
- [[workflow-business-continuity]] — multi-cluster survival pattern; local Workflows plus a global Workflow holding reference tasks; Spanner-backed with Chubby-elected writers.

### Pipeline scheduling

- [[orchestration]] — DAG-aware scheduling; Airflow and successors; strictly batch. Framed here under its pipeline-scheduler lens. [[moc-events-and-streaming]] carries the orchestration-vs-choreography framing at the architectural level — these are different things; don't conflate.
- [[distributed-cron]] — SRE Ch 24 hub: Google's datacenter-wide cron; Paxos-replicated state; Borg as the backing scheduler. The case study for scheduler reliability.
- [[cron-idempotency-and-skip-vs-double-launch]] — the fail-closed default: skip rather than double-launch, because skipped launches are usually recoverable while double launches often aren't.
- [[cron-partial-failure-resolution]] — precomputed job names + scheduled launch time embedded in the name; state lookup as the resolution mechanism.
- [[cron-thundering-herd]] — the `?` crontab extension; hashing job configuration to distribute launches stably. The midnight-MapReduce-spawn fix.

### Serverless / FaaS execution

Functions-as-a-service are a third execution substrate for data processing — distinct from long-running stream clusters and scheduled batch. The operational constraints (short-lived invocations, no native state, per-invocation billing) shape the pipeline design.

- [[cold-start-warm-start]] — the invocation lifecycle: first request pays for container provisioning and language-runtime init; subsequent requests hit a reused warm instance. Decides whether a pipeline is viable at latency SLO; often the single largest tuning lever for a FaaS-based stage.
- [[faas-batch-processing]] — tuning batch size, window, and per-invocation execution time when the processing unit is a function, not a long-running worker. The envelope that keeps per-record cost tractable; gets the balance wrong and the bill dominates.
- [[faas-function-composition]] — event-driven (function-writes-to-topic, next-function-consumes) vs direct-call (function-A-invokes-function-B) composition. The choice that decides whether back-pressure, retries, and deadlines compose; event-driven usually wins past two stages.

Deeper reading: [[site-reliability-engineering#chapter-25-data-processing-pipelines]] for the full continuous-vs-periodic argument; [[site-reliability-engineering#chapter-24-distributed-periodic-scheduling-with-cron]] for the cron-at-scale treatment.

## Query and transformation mechanics

Once data lands, it has to be queried and transformed. FoDE Chapter 8 is the engineering treatment of the query engine itself; this section collects the vocabulary a data engineer needs when a query is slow, a transformation misbehaves, or a warehouse bill spikes.

- [[life-of-a-query]] — parse, compile to bytecode, optimise, execute; what happens when you press Execute. Start here for the mental model.
- [[query-optimizer]] — reorders steps, picks join strategies; `EXPLAIN` as the lever. The single most important subsystem in any SQL-based pipeline.
- [[query-performance-tuning]] — scan less data, pick the right join, avoid row explosion, use CTEs, cache, vacuum, batch over single-row inserts. The practitioner's checklist.
- [[broadcast-join]] / [[shuffle-hash-join]] — re-cited for the query lens; same mechanisms appear in warehouses as in dataflow engines.
- [[common-table-expression]] — `WITH ... AS`; preferred over nested subqueries and temp tables; enables SQL DAGs. The structuring primitive for readable analytical SQL.
- [[window-functions]] — `OVER (PARTITION BY ... ORDER BY ...)`; declarative analytics the optimiser can push down. The right answer to "can I do this without a self-join?" more often than not.
- [[user-defined-function]] — extending the engine with custom code; deterministic vs not; the JS/Python-UDF performance trap. Use sparingly; almost always a stepping stone to a rewrite in SQL or a dedicated transformation job.
- [[nested-data]] — structs, arrays, maps as first-class column types; the semistructured escape hatch. Pair with [[wide-denormalized-table]] on [[moc-data-models-and-storage]] for the modelling side.
- [[streaming-queries]] — fast-follower CDC, Kappa queries, data-triggered computation; windows and triggers. The analytical-query shape on top of stream processing.

### Transformation patterns

- [[update-patterns]] — truncate-and-reload, insert-only, delete, upsert/merge, schema update. Each has different cost on row-based vs columnar engines.
- [[upsert]] — update-on-match, insert-on-no-match. Row-based engines handle it cheaply; columnar engines hate it. The CDC-merge anti-pattern is a standing trap.
- [[materialized-view]] — precomputed view refreshed on source change; optimiser rewrites; live-table composition. The discipline that makes warehouse serving cheap.
- [[federated-query]] — query external sources as if local; Snowflake external tables; Presto/Trino. Can become materialised views if the query is hot.
- [[data-virtualization]] — Trino, Presto, Dremio. Storage-less query engines; query pushdown; the data-mesh enabler.
- [[dbt]] — Git-managed templated SQL compiled to warehouse DAGs; analytics-engineering-as-code. The current standard for transformation at warehouse scale.
- [[feature-engineering]] — ML-targeted transformation; data scientists design, data engineers automate at production scale.
- [[data-wrangling]] — IDEs for malformed data; Reis and Housley's defence of no-code tools for the early stages.
- [[metrics-layer]] — authoritative business-logic definitions independent of the transformations. The antidote to "which dashboard's definition is right?"

Deeper reading: [[fundamentals-of-data-engineering#chapter-8-queries-modeling-and-transformation]] for the end-to-end query+modelling+transformation treatment.

## Serving — where the data lands

Serving is the stage where data becomes usable — analytics, ML, reverse ETL, embedded in product. The mechanics belong here; the discipline (trust, definitions, data products as an organisational stance) lives on [[moc-data-engineering]].

- [[data-serving]] — the stage itself; analytics / ML / reverse ETL; the "data vanity projects" anti-pattern.
- [[trust-in-data]] — the root consideration of serving; two dimensions (quality, SLA). The silent death knell once lost.
- [[data-product]] — Patil's definition; jobs-to-be-done; positive feedback loops; three build-time questions.
- [[self-service-analytics]] — mostly aspirational; succeeds only with the right audience; three classic blockers.
- [[data-definitions-and-logic]] — meaning vs derivation rules; tribal-knowledge failure; catalog + semantic layer as the fix.

### Analytics sub-varieties

- [[business-analytics]] — strategic decisions; dashboards, reports, ad-hoc.
- [[operational-analytics]] — immediate action; real-time monitoring; streaming-supplants-batch.
- [[embedded-analytics]] — customer-facing; three hard requirements (latency, performance, concurrency).
- [[real-time-olap]] — Druid, ClickHouse, Rockset, Firebolt. Purpose-built backends when warehouses don't meet latency or concurrency requirements.

### ML serving fundamentals (the parts data engineers own)

- [[model-drift]] — why models degrade; the data engineer's role in drift observability.
- [[training-test-sets]] — train/test/validation splits; point-in-time correctness; the leakage trap the data engineer has the unique vantage to prevent.
- [[feature-store]] — data-engineering × ML-engineering tool; feature history, sharing, backfill. The discipline surface between the two roles.

### Serving mechanisms

- [[semantic-layer]] — authoritative business definitions on top of the warehouse; Looker and dbt as examples.
- [[file-exchange-serving]] — ad-hoc file hand-off; when to use, when to migrate to data sharing.
- [[serving-in-notebooks]] — Jupyter as a serving target; credential hygiene; scaling off the laptop.
- [[reverse-etl]] — warehouse-to-source feedback; Hightouch, Census. The pattern that closes the loop between analytics and operations.
- [[etl-vs-elt]] — transform before load vs after; why ELT rose with cloud warehouses. Picks are usually a function of where compute is cheap.
- [[stream-to-batch-storage]] — the fan-out pattern where a stream's consumers include one that lands records into batch storage (warehouse, lake) for later analytics. The mechanism that makes the same stream serve both operational consumers (sub-second) and analytical ones (minute-to-hour) without duplicating producers.

Deeper reading: [[fundamentals-of-data-engineering#chapter-9-serving-data-for-analytics-machine-learning-and-reverse-etl]].

## Data integrity in pipelines

A pipeline that computes the wrong thing silently is worse than one that fails loudly. SRE Chapter 26 is the canonical treatment of data integrity — and it belongs in a pipeline MOC because the integrity failure modes are usually pipeline failure modes.

- [[data-integrity-sre]] — the SRE Ch 26 hub; user-perspective definition; the 24-hour "too long" threshold; three-layer defence; five closing principles.
- [[data-availability-vs-integrity]] — integrity is the means, availability is the goal; users can't distinguish loss, corruption, and extended unavailability.
- [[data-integrity-failure-modes]] — the 24 combinations (root cause × scope × rate); app-bug creeping loss dominates in Google's own data. The empirical finding that shapes the defence strategy.
- [[defense-in-depth-data]] — the three-layer architecture (soft deletion + backups + validators); replication as overarching optimisation, never a substitute.
- [[soft-deletion]] — trash folder / admin undelete / developer lazy deletion; 15-60 day retention windows.
- [[backups-vs-archives]] — the distinction (backups are loadable; archives aren't); the "nobody wants backups, they want restores" maxim.
- [[tiered-backup-strategy]] — local snapshots + distributed filesystem + offsite tape; retention and restore-time trade-offs; point-in-time recovery. Scale arithmetic (1T vs 1E) decides the shape.
- [[data-validation-pipelines]] — out-of-band validator jobs; Google Drive's 2013 auto-repair transformation as the case study.
- [[recovery-testing]] — the light-bulb analogy; why annual DiRT isn't enough; continuous automation as the only reliable discipline.

Deeper reading: [[site-reliability-engineering#chapter-26-data-integrity-what-you-read-is-what-you-wrote]].

## Sibling MOCs

- [[moc-data-models-and-storage]] — owns the shape of the store itself (models, engines, encoding, replication, partitioning, warehouse/lake shape). This MOC owns how data flows into and out of and between stores; the storage MOC owns what those stores look like.
- [[moc-data-engineering]] — owns the discipline view (lifecycle, undercurrents, governance, data architecture patterns, technology selection, the data-engineer role). This MOC owns the mechanics the discipline operates; the engineering MOC owns the practice around them.
- [[moc-events-and-streaming]] — owns the architectural use of events (brokers as integration substrate, choreography vs orchestration, [[saga]], [[outbox-table-pattern]] as a publication pattern, event design). This MOC shares [[change-data-capture]], [[log-based-message-brokers]], and [[outbox-table-pattern]] with that one under a *source-capture and execution* lens; the events MOC owns them as *architectural substrate*.
- [[moc-consistency-and-transactions]] — owns transactions, isolation levels, sagas, and the correctness-across-stores story. This MOC cites [[effectively-once-processing]] and [[workflow-correctness-guarantees]] as pipeline-execution correctness mechanisms; the consistency MOC owns cross-store correctness end to end.
- [[moc-reliability-and-operations]] — owns SLO/SLI, observability, on-call, incident response. This MOC cites the SRE Ch 25 and Ch 26 pipeline-operations material; the reliability MOC owns the operations playbook that surrounds it.
- [[moc-decomposition]] — owns the monolith-extraction playbook. This MOC owns the pipelines an extraction often needs (CDC bridge to the new service, dual-write synchronisation, migration backfill).
- [[moc-microservices]] — owns running microservices once they exist. This MOC's stream-processing section is the execution substrate for event-driven microservices; the microservices MOC owns the organisational and architectural frame.

## Related pages

- [[index]]
- [[fundamentals-of-data-engineering]]
- [[designing-data-intensive-applications]]
- [[building-event-driven-microservices]]
- [[site-reliability-engineering]]
- [[data-pipeline]]
- [[data-ingestion]]
- [[change-data-capture]]
- [[outbox-table-pattern]]
- [[batch-processing]]
- [[mapreduce]]
- [[dataflow-engines]]
- [[stream-processing]]
- [[log-based-message-brokers]]
- [[windowing]]
- [[watermarks]]
- [[stateful-stream-processing]]
- [[internal-state-store]]
- [[changelog-stream]]
- [[effectively-once-processing]]
- [[lambda-architecture]]
- [[kappa-architecture]]
- [[dataflow-model]]
- [[continuous-data-processing]]
- [[google-workflow]]
- [[dbt]]
- [[materialized-view]]
- [[data-integrity-sre]]
- [[defense-in-depth-data]]
