# Wide-Column Database

**Summary**: A [[nosql]] database optimized for storing massive volumes of data with high write throughput and sub-10ms latency per row. Wide-column databases trade query expressiveness (only one index — the row key) for extreme scale; they are the natural substrate for ecommerce, fintech, ad-tech, IoT, and real-time personalization workloads.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md`, `raw/software-architecture-the-hard-parts/chapter-06-pulling-apart-operational-data.md`

**Last updated**: 2026-04-19

---

## Characteristics

Reis and Housley catalogue the scale envelope: **petabytes of data, millions of requests per second, sub-10ms latency** (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md). These numbers drive the shape of the rest of the design:

- **Single index.** Only the row key is indexed. There are no secondary indexes.
- **Rapid scans.** The storage layout supports fast range scans over the row-key space.
- **No complex queries.** Joins, `GROUP BY`, and ad-hoc filters must be pushed to a downstream analytics system.
- **Row-key design dominates performance.** The engineer must "set up a suitable configuration, design the schema, and choose an appropriate row key to optimize performance and avoid common operational issues" (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md).

Prominent implementations: Apache Cassandra, [[bigtable|Google Bigtable]], Amazon Keyspaces, HBase.

## Why "wide" column

The column axis is open — each row can have a different set of columns, and column families are sparsely populated. This is the opposite of a relational table's uniform-schema assumption.

The "wide" part also refers to the practical use pattern: a single row may carry thousands of columns (time-series readings, event fragments, version history), which is efficient because storage is sparse.

## As a source system

A data engineer pulling from a wide-column source faces the same constraint the application has: only the row key is indexed. Two extraction strategies (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md):

- **Full or range scan.** Extract everything (or a row-key range) and send to a secondary analytics system for the real queries. Works but is expensive on large datasets.
- **[[change-data-capture|CDC]].** Capture the change stream as events and land them in a downstream stream or warehouse. Most modern wide-column stores expose CDC as a first-class feature (Bigtable Change Streams, Cassandra CDC).

Neither approach allows ad-hoc complex queries against the source — those must run in the downstream system.

## Row-key hotspotting

The single-index design means an unfortunate row-key choice creates hotspots. Common failure mode: choosing a monotonically-increasing row key (timestamp, sequence number) makes every new write land on the same partition, starving the rest of the cluster. The engineer must design keys to distribute writes uniformly — prefixing with a hash, bucketing by tenant, salting, or similar. This echoes the stream-partition hotspotting warning in [[event-streams]] and the [[partitioning-strategies]] treatment more broadly.

## Cross-book connections

- [[bigtable]] (SRE) — Google's flagship wide-column store; the archetypal reference.
- [[sstables-and-lsm-trees]] (DDIA) — the on-disk layout most wide-column stores use.
- [[partitioning-strategies]] / [[hot-sharding]] — the row-key hotspotting problem generalises.
- [[column-oriented-storage]] (DDIA) — distinct from wide-column despite the name overlap: column-oriented storage is an OLAP technique (Parquet, ClickHouse); wide-column is an OLTP-shaped NoSQL technique.

## Hard Parts ratings and positioning

Chapter 6 of *Software Architecture: The Hard Parts* calls this family "column family databases" or "big table databases" and rates it as follows (source: raw/software-architecture-the-hard-parts/chapter-06-pulling-apart-operational-data.md):

- **Learning curve — steep.** Understanding rows of varying name-value pairs, super columns (maps of columns nested inside a column), and row-key design takes practice and time.
- **Data modelling — hard.** Rows are name-value pair groups keyed by a row identifier; designing the row key takes multiple iterations. Cassandra Query Language (CQL) has improved accessibility by giving modellers a SQL-shaped surface.
- **Scalability — maximum.** All column-family databases are highly scalable; they are the go-to choice for high write or high read throughput. They scale horizontally in both directions.
- **Availability / partition tolerance — very high.** Built for clustered operation; a default replication factor of three gives at least three copies of every row. Failures of cluster nodes are transparent to the client.
- **Consistency — tunable.** Like other NoSQL families, per-operation consistency levels (`ANY`, `ONE`, `QUORUM`, `ALL`). High-consistency writes reduce availability and partition tolerance; low-consistency writes maximise throughput at the risk of data loss.
- **Community — active and growing.** Cassandra, Scylla, and HBase have active communities; SQL-like query languages (CQL) have widened adoption.
- **Read/write priority — write-biased.** SSTables, commit logs, and memtables are designed for high write volume. Sparse data (columns present only when there's a value) is handled far better than in a relational schema.

### When Hard Parts picks this family

Extreme write volumes, sparse schemas, natural time-bucketed data, multi-DC replication needs. The recipe's cost is modelling effort and a narrower query surface — anything beyond row-key lookup and range scan needs to be pushed to a downstream analytics store. See [[database-type-selection]] for the full comparison.

## Related pages

- [[nosql]]
- [[key-value-store]]
- [[bigtable]]
- [[sstables-and-lsm-trees]]
- [[partitioning-strategies]]
- [[column-oriented-storage]]
- [[source-systems]]
- [[change-data-capture]]
- [[database-type-selection]]
- [[polyglot-persistence]]
