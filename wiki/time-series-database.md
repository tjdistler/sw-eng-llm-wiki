# Time-Series Database

**Summary**: A database optimized for retrieving and statistically processing **time-indexed data** — stock ticks, sensor measurements, event logs, metrics. Time-series databases serve both as a storage layer for IoT/metrics/ad-tech use cases and, from the [[source-systems|source-system]] perspective, as an increasingly common upstream of analytics pipelines.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md`

**Last updated**: 2026-04-18

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
- **Cold tier.** Many deployments tier old data to cheap storage (see [[time-series-arena]] for the Borgmon/TSDB example).

## Connection to Borgmon's arena

Google's [[borgmon]] uses an in-memory [[time-series-arena|time-series arena]] as its hot store, with an external TSDB for historical data. This is a concrete instance of the "write-heavy, time-sorted, memory-buffered" shape described here; the SRE-book treatment is the deeper reference.

## Cross-book connections

- [[time-series-arena]] (SRE book) — Borgmon's in-memory time-series store and the hot-memory-plus-cold-TSDB tiering story that most time-series platforms implement.
- [[column-oriented-storage]] (DDIA) — time-series stores are a specialised cousin: sparse per-label columns optimised for range scans by time.
- [[sstables-and-lsm-trees]] (DDIA) — common on-disk layouts in time-series engines (Prometheus, many commercial TSDBs) resemble LSM trees.
- [[iot-architecture]] — the IoT lifecycle that produces much time-series source data.

## Related pages

- [[source-systems]]
- [[nosql]]
- [[iot-architecture]]
- [[time-series-arena]]
- [[column-oriented-storage]]
- [[sstables-and-lsm-trees]]
- [[data-temperature]]
