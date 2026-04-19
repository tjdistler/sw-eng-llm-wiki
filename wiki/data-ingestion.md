# Data Ingestion

**Summary**: The third stage of the [[data-engineering-lifecycle|data engineering lifecycle]] — moving data from [[source-systems|source systems]] into storage. Reis and Housley name source systems and ingestion together as "the most significant bottlenecks of the data engineering lifecycle"; both are largely outside the engineer's control, and both can fail quietly in ways that ripple through every downstream stage.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md`, `raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md`, `raw/fundamentals-of-data-engineering/chapter-07-ingestion.md`

**Last updated**: 2026-04-18

---

## Why ingestion is so hard

Source systems are normally outside the engineer's direct control and might randomly become unresponsive or produce bad data. Ingestion services themselves break for all the usual distributed-systems reasons. When they break, data flow stops or delivers insufficient data — and the ripple propagates through storage, transformation, and serving (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

## Key engineering considerations

Chapter 2 offers a starting set of questions for the ingestion phase (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md):

- **Use cases.** What will this data be used for? Can I reuse the dataset rather than re-ingesting it in different shapes?
- **Reliability and timeliness.** Are the generating and ingesting systems reliable? Is data available when needed?
- **Destination.** Where does the data land after ingestion?
- **Access frequency.** How often will it be read downstream?
- **Volume.** Typical arrival rate.
- **Format.** Can downstream storage and transformation handle the native format?
- **Immediate usability.** Is the data good enough for direct downstream use, and for how long will it stay that way?
- **In-flight transformation.** For streaming sources, should transformation happen mid-stream before landing?

## Batch versus streaming

Chapter 2's striking framing: **virtually all data is inherently streaming**. Data is nearly always produced and updated continually at its source. Batch ingestion is simply a specialised, convenient way of processing this stream in large chunks — for example, handling a full day's worth of data at once (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

| | Batch | Streaming |
|---|---|---|
| Trigger | Fixed time interval or size threshold | Event-by-event, continuous |
| Latency | At least one batch interval (by construction) | Sub-second to seconds |
| Typical use | Analytics, reporting, ML model training | Real-time dashboards, fraud detection, low-latency feature serving |
| Cost/complexity | Lower | Higher |

Batch was the default "for a long time" because of the limitations of legacy systems. The separation of storage and compute in modern platforms, plus the ubiquity of event-streaming infrastructure, has made streaming ingestion far more accessible, but the choice still depends on the use case (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

### Should you go streaming-first?

Reis and Housley push back on streaming-first as a default. Questions to ask before picking streaming over batch (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md):

- Can downstream storage handle the rate?
- Do I really need millisecond latency, or would microbatching every minute do?
- What specific action can I take on real-time data that I couldn't take on batch?
- Cost/time/maintenance/downtime trade-off vs batch?
- Is my streaming pipeline reliable and redundant on infrastructure failure?
- Managed service (Kinesis, Pub/Sub, Dataflow) or self-hosted (Kafka, Flink, Spark, Pulsar)? Who operates it?
- For ML: do I gain from online predictions and continuous training?
- What is the load impact on the live production source?

Their recommendation: **batch is an excellent approach for many common use cases** (model training, weekly reporting); adopt true real-time streaming only after identifying a business use case that justifies the extra cost and complexity (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

See [[batch-processing]] and [[stream-processing]] for the deeper technical treatments.

## Push versus pull

An orthogonal axis to batch/streaming (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md):

- **Push.** A source system writes data out to a target — database, object store, filesystem, message queue.
- **Pull.** The ingestion system retrieves data from the source.

The line is blurry — data is often pushed and pulled at different stages of the same pipeline.

Examples (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md):

- **ETL extract** — the "E" in ETL is a pull. The ingestion system queries a snapshot of the source on a fixed schedule. See [[etl-vs-elt]].
- **Trigger-style [[change-data-capture|CDC]]** — a database trigger fires on row change and **pushes** a message to a queue; the ingestion system picks it up.
- **Log-based CDC** — the database pushes its binlog/WAL; the ingestion system reads that log asynchronously with little to no load on the source. Again, see [[change-data-capture]].
- **Timestamp-based batch CDC** — pull; the ingestion system queries for rows changed since the last poll.
- **Streaming ingestion (IoT)** — data bypasses a backend database and is **pushed directly** to an ingest endpoint, typically buffered by an event-streaming platform. This pattern "simplifies real-time processing, allows app developers to tailor messages for downstream analytics, and greatly simplifies the lives of data engineers."

## Connection to the rest of the lifecycle

Ingestion is the narrow neck of the whole pipeline. Bottlenecks here propagate everywhere:

- Upstream, ingestion is shaped by what [[source-systems]] can be coaxed into providing.
- Downstream, ingestion feeds [[data-storage-stage|storage]], then [[data-transformation|transformation]], then [[data-serving|serving]].

## Chapter 5 addition: ingestion from diverse source-system shapes

Chapter 5 of *Fundamentals of Data Engineering* expands what "ingestion" actually has to handle. Each [[source-systems|source-system]] category demands its own adapter (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md):

- **[[file-sources|Files]]** — object-storage polling, SFTP, email attachments. Implicit schemas; validate before loading.
- **APIs** — REST, [[graphql|GraphQL]], [[rpc|gRPC]], [[webhooks]]. Custom code for long-tail APIs; client libraries and SaaS connectors for the rest.
- **[[application-database-as-source|Application databases]]** — [[change-data-capture|CDC]], read replicas, or careful full scans.
- **[[message-brokers|Message queues]]** — consumer code; idempotent; handles out-of-order delivery.
- **[[event-streams|Event streams]]** — stream-processing consumer; partition-aware; replay-capable.
- **[[data-sharing]]** — cross-tenant query; no network plumbing at all.
- **[[nosql]] stores** — CDC streams where available; full scans otherwise.

The "narrow neck" framing above still applies: ingestion is where the source-system complexity collides with the pipeline's downstream expectations, and where most failures surface.

## Chapter 7 deep dive — ingestion as its own lifecycle stage

Chapter 7 of *Fundamentals of Data Engineering* is the expanded treatment of ingestion: what it is versus what it isn't, the full set of engineering considerations, batch vs streaming patterns, and the concrete ways to ingest data (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md).

### Ingestion vs integration vs internal movement

Three terms that are often conflated (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md):

- **Data ingestion** — moving data from one place to another, with ingestion being an intermediate step from source to storage in the lifecycle.
- **[[data-integration]]** — combining data from disparate sources into a new dataset (e.g., CRM + ad analytics + web analytics → unified user profile). Covered in Ch 8 as transformation.
- **Internal movement within a system** — copying data between tables in the same database, or caching a stream in memory. Treated as transformation, not ingestion.

Ingestion is the boundary-crossing movement: it ends when data lands in the target storage system.

See [[data-pipeline]] for Ch 7's deliberately fluid definition of the broader artefact.

### Eight engineering considerations

Ch 7 expands the original Ch 2 checklist into eight design axes (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md):

| Consideration | What to decide | Wiki page |
|---|---|---|
| **Bounded vs unbounded** | Is the data a continuous stream with artificial cutoffs, or genuinely finite? *"All data is unbounded until it's bounded."* | See [[batch-processing]], [[stream-processing]] |
| **Frequency** | Batch, micro-batch, or real-time? Every downstream batch process becomes a bottleneck | [[ingestion-frequency]] |
| **Synchronous vs asynchronous** | Tightly coupled lifecycle stages (older ETL) vs event-level decoupling with buffers (cloud-native) | below |
| **Serialization and deserialization** | Does the destination understand the source's wire format? | [[encoding-formats]] |
| **Throughput and scalability** | Design for burstiness, upstream backfills, and elastic scale; prefer managed services | below |
| **Reliability and durability** | Uptime for the ingestion system; ensuring data isn't lost (IoT and caches don't retain) | below |
| **Payload** | Kind, shape, size, schema/types, metadata | [[ingestion-payload]] |
| **Push vs pull vs poll** | Who initiates movement, and when | [[push-vs-pull-vs-poll]] |

### Synchronous vs asynchronous ingestion

Ch 7's warning — with a mini-case-study of a dozen-stage synchronous ETL that took 24 hours end-to-end and had to be restarted from scratch when any step failed:

- **Synchronous.** Each lifecycle stage directly depends on the previous one. A failure anywhere forces a full rerun of the whole pipeline. Common in older ETL (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md).
- **Asynchronous.** "Dependencies can now operate at the level of individual events, much as they would in a software backend built from microservices." Individual events become available in storage as soon as they are ingested; the streaming buffer acts as a shock absorber; spikes don't overwhelm downstream processing.

The canonical asynchronous shape: app → Kinesis stream (buffer) → Beam (parse/enrich) → Kinesis stream 2 → Kinesis Firehose → S3. The first Kinesis stream is the "shock absorber that moderates load so event-rate spikes do not overwhelm downstream processing."

### Throughput and scalability

"In theory, ingestion should never be a bottleneck. In practice, ingestion bottlenecks are pretty standard" (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md). Design principles:

- Scale up and down to match required throughput.
- Plan for **backfill bursts** — when an upstream source recovers from an outage and tries to catch up, can the ingestion pipeline keep up?
- Build in buffering for **bursty arrival** — event rates ebb and flow; buffers prevent loss during spikes.
- Use managed services for scaling rather than hand-rolling — "don't reinvent the data ingestion wheel."

### Reliability and durability

Reliability and durability are paired but distinct: reliability = uptime and failover; durability = data not lost or corrupted. Critical framing from Ch 7: **some sources do not retain data if it isn't correctly ingested**. IoT devices and caches in particular — "once lost, it is gone for good." The reliability of the ingestion system therefore directly determines the durability of generated data (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md).

Direct costs (cloud + labour) and indirect costs (on-call toll on the team) both rise with redundancy. Ch 7's balance point: "evaluate the risks and build an appropriate level of redundancy and self-healing based on the impact and cost of losing data" — not "build everything three-region-multicloud fully redundant." Even an infinite budget doesn't guarantee ingestion during the kind of failures where ingestion doesn't matter anyway (internet outage, power grid failure).

### Batch ingestion patterns

Ch 7 names five batch-specific patterns (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md):

- **Snapshot or differential extraction.** See [[snapshot-vs-differential-ingestion]].
- **File-based export and ingestion.** See [[file-based-ingestion]].
- **[[etl-vs-elt|ETL vs ELT]].** Covered in Ch 8 for the transform side; Ch 7 owns the E and L.
- **Inserts, updates, and batch size.** Batch-oriented systems perform badly on many small writes — columnar databases create many small files, and in-place updates are forced to scan whole column files. Know your tool: some (Druid, Pinot) are purpose-built for high insert rates; BigQuery is slow on vanilla single-row inserts but fast through its streaming buffer.
- **[[data-migration|Data migration]].** A special one-time bulk case.

### Message and stream ingestion patterns

Eight considerations specific to event-based ingestion (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md):

- **[[schema-evolution|Schema evolution]].** Fields added, removed, or retyped. Use a schema registry, a dead-letter queue, and above all upstream communication.
- **[[late-arriving-events|Late-arriving data]].** Set a cutoff beyond which late events are dropped; confusing ingestion time with event time leads to wrong reports.
- **[[out-of-order-events|Ordering]] and multiple delivery.** Streaming platforms are distributed; events can arrive out of order and can be delivered more than once (at-least-once).
- **[[reprocessing-event-streams|Replay]].** "A key capability in many streaming ingestion platforms." Particularly useful for re-ingesting a specific time range after a bug fix. Kafka, Kinesis, Pub/Sub support retention + replay; RabbitMQ does not by default.
- **Time-to-live (TTL).** Maximum message retention; unacknowledged events after TTL "automatically disappear." Too short drops messages before processing; too long creates backlog. Pub/Sub caps at 7 days; Kinesis up to 365; Kafka is configurable indefinitely (with tiered storage).
- **Message size.** Frameworks have limits — Kinesis 1 MB, Kafka 1 MB default up to 20 MB configurable.
- **Error handling and [[dead-letter-queue|dead-letter queues]].** Events that cannot be ingested must be rerouted, not left to block the queue.
- **Consumer pull vs push.** Kafka and Kinesis are pull-only; Pub/Sub and RabbitMQ support both. Pull is the default for data engineering; push for specialized cases. See [[push-vs-pull-vs-poll]].
- **Location.** Ingest close to where data is generated to reduce latency and egress. Balance against cross-region analytics costs.

### The ways to ingest data

Ch 7's enumeration of concrete ingestion mechanisms (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md):

| Mechanism | Notes | Wiki page |
|---|---|---|
| Direct DB connection | JDBC/ODBC; struggling with nested and columnar data; increasingly paired with file export | See [[oltp-vs-olap]] |
| [[change-data-capture|CDC]] | Batch-oriented (query-based) or continuous (log-based) | [[change-data-capture]] |
| APIs (REST, GraphQL, gRPC, webhooks) | No universal standard; favour client libraries and managed connectors | [[third-party-api-integration]], [[webhooks]], [[graphql]] |
| [[message-brokers\|Message queues]] and [[event-streams\|event streams]] | Real-time ingestion; messages transient, streams persistent | [[message-brokers]], [[event-streams]] |
| **Managed data connectors** (Fivetran, Airbyte, Matillion, Stitch) | The book's strong recommendation for undifferentiated plumbing | [[managed-connector]] |
| Moving data with object storage | "Most optimal and secure way to handle file exchange" | [[object-storage]] |
| **[[edi\|EDI]]** | Archaic email/flash-drive transport; automate around it | [[edi]] |
| Databases and file export | Bulk export to object storage; read replicas for load relief | [[file-based-ingestion]] |
| Shell / CLI tools | Fine for simple cases; move to orchestration as complexity grows | See [[orchestration]] |
| SSH / SFTP / SCP | Still practical reality for partner-business integrations; bastion-host pattern for DB access | [[file-based-ingestion]] |
| [[webhooks\|Webhooks]] | Reverse APIs; pair with a queue for durability | [[webhooks]] |
| Web interface | "Someone manually runs a report and downloads it" — automate away when possible | — |
| **[[web-scraping\|Web scraping]]** | Legal/ethical caution; maintenance-heavy | [[web-scraping]] |
| **[[transfer-appliance\|Transfer appliances]]** | One-time bulk migration for 100+ TB | [[transfer-appliance]] |
| **[[data-sharing\|Data sharing]]** | Not strictly ingestion — data stays with the provider | [[data-sharing]] |

### Stakeholders

Ingestion sits across organizational boundaries (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md):

- **Upstream** — software engineers and system owners who generate the data. The significant opportunity: inviting them to be stakeholders in data-engineering outcomes, via communication and product-manager involvement. Ideally software engineers act as "extensions of the data engineering team" for things like event-driven architecture for real-time analytics.
- **Downstream** — data scientists, analysts, CTOs, plus the wider business (marketing VPs, supply-chain heads, CEO). Ch 7's critique: data engineers pursuing "sophisticated projects" (real-time streaming) while a marketing manager next door is downloading Google Ads reports manually. "Basic ingestion work may seem tedious, but delivering value to these core parts of the company will open up more budget."

### Undercurrents applied to ingestion

Ch 7's selected highlights (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md):

- **Security** — encrypt in-flight; VPN or dedicated connection to on-prem; never allow data to leave the VPC without deliberate routing.
- **Data management** — ingestion is where lineage and cataloging **begin**; master data management, ethics, privacy, compliance all start here. For schema change, they propose a **Git-style branching** approach (teams maintain dev versions of a table in orchestration tools like Airflow, schema changes appear there before the main table). For sensitive data, the fundamental question: *do you need to ingest it at all?* Drop sensitive fields before storage when possible; tokenize or hash at ingestion; touchless-production as the ideal; watch out for ritualistic encryption.
- **DataOps** — ingestion is "the" stage where monitoring matters most; track event times, ingestion times, process times, processing times; "data is a silent killer" applies especially here. One FoDE case: an ingestion pipeline failure went undetected for **six months**.
- **Orchestration** — cron is brittle; "true orchestration" means scheduling task **graphs**, not individual tasks. See [[orchestration]].
- **Software engineering** — ingestion is "engineering intensive" and sits on the edge of the data-engineering domain. Use version control, code review, tests; use managed tools where possible; keep code **decoupled** — avoid monolithic systems with tight dependencies on source or destination.

## Cross-book connections

- [[change-data-capture]] (DDIA, Bellemare, Newman) is the single richest topic connected to ingestion; FoDE's push/pull framing is the lifecycle view on what DDIA and EDM cover in depth.
- [[event-driven-microservices|Event-driven microservices]] recast ingestion: rather than an external team pulling data out, the source team publishes a first-class event stream as a product. Bellemare's [[data-liberation]] is the transition path.
- [[data-processing-pipelines]] (SRE Ch 25) names the operational pathologies of large batch ingestion chains that periodic cron pipelines fall into.
- [[dead-letter-queue]] is a named pattern across DDIA and EDM; Ch 7 makes it an explicit part of the ingestion architecture rather than an afterthought.

## Related pages

- [[data-engineering-lifecycle]]
- [[source-systems]]
- [[source-system-considerations]]
- [[data-storage-stage]]
- [[data-pipeline]]
- [[batch-processing]]
- [[stream-processing]]
- [[change-data-capture]]
- [[etl-vs-elt]]
- [[data-liberation]]
- [[event-streams]]
- [[orchestration]]
- [[file-sources]]
- [[webhooks]]
- [[data-sharing]]
- [[ingestion-frequency]]
- [[push-vs-pull-vs-poll]]
- [[ingestion-payload]]
- [[snapshot-vs-differential-ingestion]]
- [[file-based-ingestion]]
- [[data-migration]]
- [[managed-connector]]
- [[dead-letter-queue]]
- [[web-scraping]]
- [[edi]]
- [[transfer-appliance]]
