# Data Storage (Lifecycle Stage)

**Summary**: The storage stage of the [[data-engineering-lifecycle|data engineering lifecycle]] — where data lives at rest at every step between source and consumer. Storage is not a single step like the others; it **underpins** the lifecycle, appearing alongside ingestion, transformation, and serving. The choice of storage system (object store, warehouse, lake, lakehouse, streaming log) shapes every other stage.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md`, `raw/fundamentals-of-data-engineering/chapter-06-storage.md`

**Last updated**: 2026-04-18

---

## Why storage is the tricky stage

Storage is more complicated to reason about than the other lifecycle stages because (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md):

1. **Architectures layer multiple storage systems.** A single pipeline may touch object storage, a warehouse, a streaming log, and a cache.
2. **"Pure" storage is rare.** Many storage systems also query or transform. Even [[distributed-filesystems|object storage]] like S3 supports SQL-like querying (Amazon S3 Select); [[data-warehousing|cloud data warehouses]] store and transform and serve from the same engine; [[log-based-message-brokers|Kafka and Pulsar]] ingest, store, and query streams.
3. **Storage touches every other stage.** Ingestion lands data in storage; transformation reads and writes storage; serving reads storage.

In practice, *how* data is stored shapes *how* it can be used at every other stage.

## Key engineering considerations

Chapter 2 lists a starting set of evaluation questions (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md):

- **Compatible with read/write speeds?** Will storage bottleneck downstream?
- **Do you understand how it works?** Are you using it optimally, or committing "unnatural acts" — e.g., high-rate random-access updates on object storage (an antipattern)?
- **Future scale?** Total available storage, read rate, write volume.
- **SLA retrieval?** Can consumers retrieve in time?
- **Metadata capture?** Schema evolution, data flows, [[data-lineage|lineage]]. Metadata is an "investment in the future, dramatically enhancing discoverability and institutional knowledge."
- **Pure storage vs query system?** A warehouse supports complex queries; object storage does not.
- **Schema enforcement?** Schema-agnostic (object store), flexible (Cassandra), or enforced (cloud DW)?
- **[[master-data-management|Master data]], golden records, lineage for governance?**
- **Compliance and data sovereignty?** Geographic constraints on where data may sit.

## Data temperature — hot, warm, cold

Not all data is accessed the same way. The frequency of access determines its "temperature" (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md):

| Temperature | Access frequency | Typical storage |
|---|---|---|
| Hot | Many times per day, perhaps per second | Low-latency stores serving user traffic |
| Lukewarm | Every week or month | Standard warehouse or lake tables |
| Cold | Seldom queried; retained for compliance or disaster recovery | Archival object-storage tiers (S3 Glacier, etc.) — cheap storage, expensive retrieval |

See [[data-temperature]] for detail.

## No one-size-fits-all

Chapter 2 is emphatic: "There is no one-size-fits-all universal storage recommendation. Every storage technology has its trade-offs" (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md). The choice depends on volume, ingestion frequency, format, size, and use case.

## Storage that spans stages

Several modern systems collapse what used to be separate lifecycle stages into a single engine (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md):

- **Cloud data warehouses** (BigQuery, Snowflake, Redshift) — store, transform, and serve data in one platform. See [[data-warehousing]].
- **Streaming frameworks** (Kafka, Pulsar) — act as ingestion path, persistent storage, and query system for event streams. See [[log-based-message-brokers]] and [[stream-processing]].
- **Data lakes and lakehouses** — object storage as the foundation, with query engines layered on top. See [[data-lake]], [[data-lakehouse]].

## Ch 6 — the three-layer model

Chapter 6 is the deep dive on storage. It structures the topic in **three layers** (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md):

1. **Raw ingredients** — magnetic disk, SSD, RAM, networking, CPU, [[encoding-formats|serialization]], [[compression-algorithms|compression]], caching. See [[storage-raw-ingredients]].
2. **Storage systems** — single-machine vs distributed storage; [[eventual-consistency|consistency models]]; [[file-storage]], [[block-storage]], [[object-storage]]; [[cache-memory-storage|in-memory stores]]; [[distributed-filesystems|HDFS]]; [[streaming-storage]]; [[indexes]], [[partitioning]], clustering.
3. **Storage abstractions** — [[data-warehousing]], [[data-lake]], [[data-lakehouse]], [[data-platform]], [[stream-to-batch-storage]].

### Ch 6 — big ideas

Chapter 6 names several cross-cutting "big ideas" on top of the layer model (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md):

- **[[data-catalog|Data catalog]]** — centralised metadata store; foundation of the lakehouse and of organisational discoverability.
- **[[data-sharing|Data sharing]]** — multitenant cloud capability for interorganisational collaboration.
- **[[schema-on-read-vs-write|Schema]]** — schema-on-write (warehouse style) vs. schema-on-read (lake style); the file format and metastore choices.
- **[[storage-compute-separation|Separation of compute and storage]]** — the architectural move behind the cloud data platform.
- **Zero copy cloning** — pointer-based table clones on object storage; see [[storage-compute-separation]].
- **[[data-retention|Data retention]] and [[data-temperature|hot/warm/cold]]** — the economics of access frequency.
- **Single-tenant vs multitenant storage** — isolation vs shared resources; see [[multischema-storage]] and related data-mesh discussion.

### Ch 6 — undercurrents for storage

Chapter 6 runs the storage stage through the six lifecycle undercurrents (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md):

- **Security** — least privilege; column/row/cell-level access control.
- **Data management** — catalogs, metadata, versioning; privacy compliance (GDPR deletion, anonymisation, masking).
- **DataOps** — FinOps monitoring, security monitoring, active data observability.
- **Data architecture** — design for durability; understand upstream and downstream data models; prefer fully managed systems.
- **Orchestration** — "storage allows data to flow through pipelines, and orchestration is the pump."
- **Software engineering** — storage infrastructure as code; ephemeral compute resources.

## Cross-book connections

- [[storage-engines]] (DDIA) covers the *internal* mechanics of storage — [[b-trees]], [[sstables-and-lsm-trees|LSM trees]], [[column-oriented-storage]]. This page is about the *lifecycle role* of storage; storage-engines is about how a single engine works internally.
- [[oltp-vs-olap]] names the two dominant internal optimisation regimes.
- [[data-warehousing]], [[data-lake]], [[data-lakehouse]] are the three architectural shapes most commonly considered for the analytical-storage layer.

## Related pages

- [[data-engineering-lifecycle]]
- [[data-temperature]]
- [[data-retention]]
- [[data-warehousing]]
- [[data-lake]]
- [[data-lakehouse]]
- [[data-platform]]
- [[storage-engines]]
- [[storage-raw-ingredients]]
- [[object-storage]]
- [[block-storage]]
- [[file-storage]]
- [[cache-memory-storage]]
- [[streaming-storage]]
- [[stream-to-batch-storage]]
- [[storage-compute-separation]]
- [[lakehouse-table-formats]]
- [[oltp-vs-olap]]
- [[column-oriented-storage]]
- [[compression-algorithms]]
- [[log-based-message-brokers]]
- [[distributed-filesystems]]
- [[metadata]]
