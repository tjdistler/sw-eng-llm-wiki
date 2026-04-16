# Write Amplification

**Summary**: Write amplification is the ratio of data actually written to disk to the data the application logically wrote. It is a key performance concern for both SSDs and write-heavy database workloads.

**Sources**: `raw/designing-data-intensive-applications/chapter-03-storage-and-retrieval.md`

**Last updated**: 2026-04-15

---

## Definition

When an application writes one record to a database, the storage engine may perform many more physical disk writes: to a write-ahead log, to index pages, during compaction or merging, and possibly again due to page splits.

**Write amplification** is the factor by which physical writes exceed logical writes. A write amplification of 10× means every 1 byte of application data causes 10 bytes of disk writes.

## Where it comes from

**In [[b-trees]]**:
- Every write goes to the WAL (write-ahead log) first
- Then to the tree page itself
- A page split additionally writes two new pages and updates the parent page
- Some engines write each page twice to avoid partially-updated-page corruption
- Result: each logical write causes at least 2–3 physical writes, often more

**In [[sstables-and-lsm-trees|LSM-trees]]**:
- Each write is first appended to the WAL and the memtable
- When the memtable flushes to disk as an SSTable, that's another write
- During compaction, segments are merged and written to new files — the same data is rewritten repeatedly across the database's lifetime
- Result: write amplification varies with compaction strategy and workload, but is often lower than B-trees for write-heavy loads

## Why it matters

**SSD longevity**: SSDs can only overwrite blocks a limited number of times before the storage cells wear out. High write amplification directly reduces an SSD's usable lifetime.

**Throughput ceiling**: In write-heavy applications, the bottleneck is often the rate at which data can be written to disk. Higher write amplification means fewer logical writes per second fit within the available disk I/O bandwidth.

**Compaction falling behind**: In LSM-trees, if incoming write throughput exceeds the compaction rate, unmerged segments accumulate on disk. This causes read performance to degrade (more segments to check) and can eventually exhaust disk space. SSTable-based engines typically don't throttle incoming writes, so this requires explicit monitoring.

## Tradeoffs

Neither B-trees nor LSM-trees eliminate write amplification — they trade different shapes of it:
- B-trees have more predictable write amplification per write but higher per-write overhead
- LSM-trees have lower average write amplification for write-heavy workloads but can spike during heavy compaction

On SSDs, the firmware also internally uses a log-structured algorithm to manage flash cells, so the storage engine's write pattern interacts with the SSD's own write amplification. Lower write amplification at the engine level still helps, as it allows more requests within the available I/O bandwidth.

## Related pages

- [[storage-engines]]
- [[b-trees]]
- [[sstables-and-lsm-trees]]
