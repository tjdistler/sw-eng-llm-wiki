# Time-Series Database

**Summary**: A database optimized for retrieving and statistically processing **time-indexed data** — stock ticks, sensor measurements, event logs, metrics. Time-series databases serve both as a storage layer for IoT/metrics/ad-tech use cases and, from the [[source-systems|source-system]] perspective, as an increasingly common upstream of analytics pipelines.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md`, `raw/software-architecture-the-hard-parts/chapter-06-pulling-apart-operational-data.md`

**Last updated**: 2026-04-19

---

## What counts as time-series data

"A time series is a series of values organized by time" (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md). Anything recorded over time — regularly or sporadically — qualifies. Canonical examples:

- Stock trade prices throughout a trading day.
- Weather-sensor atmospheric temperature every minute.
- Application logs, event traces, and metrics feeds.
- IoT device readings.

Reis and Housley distinguish two flavours (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md):

- **Measurement data.** Generated regularly — temperature sensors, air-quality monitors. Regular cadence; predictable volume.
- **Event-based data.** Generated whenever something happens — motion sensors firing, a user clicking a button. Irregular cadence; bursty.

The distinction matters because a time-series database tuned for uniform-cadence measurement data may behave differently when fed bursty event data, and vice versa.

## Why a specialised database

Time-series data has lived in relational databases for decades, but modern volumes and velocities have driven specialised systems. Reis and Housley: "as data grew faster and bigger, new special-purpose databases were needed. Time-series databases address the needs of growing, high-velocity data volumes from IoT, event and application logs, ad tech, and fintech, among many other use cases" (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md).

Specific design properties common to time-series DBs:

- **Write-heavy.** Workloads are far more write than read; many use memory buffering to absorb the write rate.
- **Timestamp-ordered storage.** Data is laid out on disk in time order, enabling efficient range scans by time.
- **Sparse schema.** Typical schema: a timestamp, a small number of tag/label columns, and one or a few measured values. Wide-column shapes are uncommon.
- **Few joins.** The workload is aggregation-by-time, not multi-table joins. Some newer engines (Apache Druid) support joins, but most don't.
- **Compression friendly.** Time-sorted data with limited cardinality per column compresses extremely well.

Because of these properties, time-series DBs are "suitable for operational analytics but not great for BI use cases" (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md).

## As a source system

From a data engineer's perspective, a time-series DB is a common source for:

- **Metrics exports** — forwarding collected metrics into a broader analytics platform.
- **IoT ingest pipelines** — the TSDB is the primary store; downstream systems pull aggregated rollups for ML or BI.
- **Ad-tech reporting** — impressions and events arrive event-by-event and are aggregated for reporting.

Engineering considerations particular to TSDB sources:

- **Tag cardinality.** Most TSDBs degrade badly when a tag's cardinality explodes (e.g., a per-user ID tag). Source-system owners often have cardinality budgets; the engineer must understand them.
- **Downsampling and retention.** Old data is typically downsampled (minute → hour → day) to keep size manageable; the engineer must know the downsampling schedule because it changes query results.
- **Cold tier.** Many deployments tier old data to cheap storage — an in-memory hot arena plus an external historical TSDB is the common shape.

## Connection to monitoring-system arenas

Production time-series monitoring systems (both Prometheus and its pre-open-source Google precursor) use an in-memory time-series arena as the hot store, with an external TSDB for historical data. This is a concrete instance of the "write-heavy, time-sorted, memory-buffered" shape described here.

## Cross-book connections

- [[column-oriented-storage]] (DDIA) — time-series stores are a specialised cousin: sparse per-label columns optimised for range scans by time.
- [[sstables-and-lsm-trees]] (DDIA) — common on-disk layouts in time-series engines (Prometheus, many commercial TSDBs) resemble LSM trees.
- [[iot-architecture]] — the IoT lifecycle that produces much time-series source data.

## Hard Parts positioning

Chapter 6 of *Software Architecture: The Hard Parts* includes time-series databases in its eight-family [[database-type-selection]] matrix. Headline notes (source: raw/software-architecture-the-hard-parts/chapter-06-pulling-apart-operational-data.md):

- **Learning curve — easy.** Timestamped data with a tag-and-value shape is intuitive. The mental shift is **append-only** — errors can't be fixed by `UPDATE`, they must be compensated.
- **Data modelling — tag design dominates.** Bad tagging ("one tag for multiple facts" — `ticket_info=Open.374737`) kills queryability; good tagging ("one fact per tag" — `ticket_status=Open`, `ticket_id=374737`) keeps it.
- **Scalability / throughput — high.** TimescaleDB inherits PostgreSQL's patterns; InfluxDB clusters via meta and data nodes with replication factor control.
- **Availability / partition tolerance — configurable.** Replication factors and meta/data node separation give operators dials to turn.
- **Consistency — varies.** TimescaleDB (relational-backed) gets ACID; others tune consistency via `any`/`one`/`quorum` levels. Higher consistency → lower availability.
- **Community — growing.** SQL-like query languages (InfluxQL, FluxQL, SQL) lower the entry barrier.
- **Read/write priority — read-biased.** Append-only writes are optimised, but the workload shape is "aggregate over a time window" — read-heavy in practice.

The book's explicit caveat: time-series databases are **not general-purpose**. They're optimised for one specific question shape ("what happened between T1 and T2"). A data domain whose queries don't fit that shape should pick a different family.

## Related pages

- [[source-systems]]
- [[nosql]]
- [[iot-architecture]]
- [[column-oriented-storage]]
- [[sstables-and-lsm-trees]]
- [[data-temperature]]
- [[database-type-selection]]
- [[polyglot-persistence]]
