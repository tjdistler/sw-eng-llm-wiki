# Storage Engines

**Summary**: Storage engines are the component of a database responsible for storing data and retrieving it. They fall into two families based on design philosophy — log-structured and update-in-place — and are further split by workload type: OLTP vs OLAP.

**Sources**: `raw/designing-data-intensive-applications/chapter-03-storage-and-retrieval.md`

**Last updated**: 2026-04-15

---

## Two design families

All storage engines make a fundamental choice about how to write data to disk:

**Log-structured** engines only append to files and periodically compact or merge them. They never overwrite data in place. Examples: Bitcask, LevelDB, RocksDB, Cassandra, HBase, Lucene.

**Update-in-place** engines treat disk as a set of fixed-size pages that can be overwritten. The primary example is [[b-trees]], used in virtually every major relational database.

The practical consequence:
- Log-structured engines convert random writes into sequential writes, enabling high write throughput.
- Update-in-place engines provide predictable read latency and strong transactional semantics (each key exists in exactly one place).

## Two workload types

Storage engines are also shaped by the workload they serve:

**OLTP** (online transaction processing) — user-facing applications that touch a small number of records per query, using an index to look up data by key. The bottleneck is typically disk seek time. See [[oltp-vs-olap]].

**OLAP** (online analytic processing) — analytical queries that scan millions or billions of rows but read only a few columns. The bottleneck is disk bandwidth, not seek time. These workloads are served by [[data-warehousing]] systems and [[column-oriented-storage]].

The indexing structures discussed in [[hash-indexes]], [[sstables-and-lsm-trees]], and [[b-trees]] are primarily OLTP-optimized.

## Choosing a storage engine

Application developers typically choose a database, not a storage engine directly, but understanding engine internals helps:

- Know your access patterns: point lookups vs range queries vs aggregations
- Know your workload ratio: read-heavy vs write-heavy
- Understand [[write-amplification]] — it affects both performance and SSD longevity
- Benchmark with your actual data: no single engine wins all workloads

## Related pages

- [[indexes]]
- [[hash-indexes]]
- [[sstables-and-lsm-trees]]
- [[b-trees]]
- [[write-amplification]]
- [[oltp-vs-olap]]
- [[data-warehousing]]
- [[column-oriented-storage]]
