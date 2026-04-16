# SSTables and LSM-Trees

**Summary**: SSTables (Sorted String Tables) are log segments where keys are kept in sorted order. The LSM-tree (Log-Structured Merge-Tree) algorithm builds on SSTables to provide high write throughput with efficient reads and range queries.

**Sources**: `raw/designing-data-intensive-applications/chapter-03-storage-and-retrieval.md`

**Last updated**: 2026-04-15

---

## SSTable format

A Sorted String Table is a log-structured segment file with one additional constraint: key-value pairs are sorted by key. Each key appears at most once per merged segment.

Sorted order gives three advantages over unsorted [[hash-indexes]]:

1. **Efficient merging** — Merge sorted segments the same way mergesort merges sorted arrays: read files side by side, always pick the lowest key, advance that file's pointer. Even if files are larger than available memory. When the same key appears in multiple segments, keep the value from the most recent segment.

2. **Sparse in-memory index** — You no longer need every key in memory. Because keys are sorted, you only need to store one key per few kilobytes of segment data. To find a key, jump to the nearest known offset and scan from there. This scan is fast because a few kilobytes fit in memory and CPU cache.

3. **Compression** — Since reads scan a range of key-value pairs anyway, records in that range can be grouped into a compressed block. The sparse index points to the start of each compressed block, saving both disk space and I/O bandwidth.

## The LSM-tree algorithm

The challenge: incoming writes arrive in arbitrary order, but SSTables need sorted data. Sorting on disk is expensive; sorting in memory is easy.

The algorithm:
1. **Writes go to a memtable** — an in-memory balanced tree (e.g., red-black tree or AVL tree). The memtable accepts writes in any order and can return keys in sorted order.
2. **Flush to SSTable when the memtable grows large** (typically a few megabytes). The tree already has keys in sorted order, so writing the SSTable is efficient. A new memtable begins accepting writes while the flush proceeds.
3. **Reads check memtable first**, then the most recent on-disk segment, then older segments in order.
4. **Background compaction** merges and compacts segment files, discarding overwritten and deleted values.

**Crash recovery**: The memtable is lost on crash. To prevent losing recent writes, every write is also appended to a separate write-ahead log on disk (in unsorted order). When the memtable is flushed to an SSTable, that log can be discarded.

## Real-world implementations

This algorithm is used in:
- **LevelDB** and **RocksDB** (embeddable storage engine libraries)
- **Cassandra** and **HBase** (inspired by Google's Bigtable, which introduced the terms SSTable and memtable)
- **Lucene** (uses SSTable-like files for its term dictionary; the value is a postings list of document IDs)

The name "LSM-tree" comes from Patrick O'Neil et al.'s paper on Log-Structured Merge-Trees.

## Compaction strategies

Two main approaches for deciding when and how to compact:

**Size-tiered compaction** — Newer, smaller SSTables are successively merged into older, larger SSTables. Used by HBase and (as an option) Cassandra.

**Leveled compaction** — The key range is split into smaller SSTables distributed across "levels." Older data moves into deeper levels. Compaction proceeds more incrementally and uses less disk space at any given moment. Used by LevelDB, RocksDB, and (as an option) Cassandra.

## Bloom filters

Looking up a key that doesn't exist requires checking every segment, potentially reading from disk at each level. **Bloom filters** solve this: a memory-efficient probabilistic data structure that can definitively say "this key is NOT in this segment," saving unnecessary disk reads for nonexistent keys. (They can return false positives but never false negatives.)

## Performance characteristics

LSM-trees excel at write-heavy workloads:
- All writes are sequential appends (fast on both HDDs and SSDs)
- Lower [[write-amplification]] than [[b-trees]] in many configurations
- Better compression (no fragmentation from fixed-size pages)
- Efficient range queries (data is sorted)

Drawbacks:
- **Compaction can interfere with reads and writes** — disk bandwidth is shared between serving requests and background compaction. At high write rates, compaction may fall behind, causing unmerged segments to accumulate.
- **Reads check multiple structures** — memtable plus potentially several SSTable levels, each possibly requiring a disk read. B-trees are typically faster for reads.
- **A key may exist in multiple segments** — unlike B-trees where each key lives in exactly one place, making range locks for transactions harder to implement.

## SSTables in batch processing

The SSTable technique reappears in [[mapreduce]]: during the shuffle phase, each map task partitions its output by reducer and writes each partition as a sorted file on the mapper's local disk — using the same approach as SSTable creation. Reducers then fetch and merge these sorted files, just as LSM-tree compaction merges sorted segments. The mergesort access pattern (sequential reads) performs well on disk, whether in a storage engine or a batch processing shuffle (source: designing-data-intensive-applications, chapter 10).

The GNU `sort` utility uses the same principle for larger-than-memory datasets: sort chunks in memory, write sorted segments to disk, then merge — which is why Unix pipeline batch processing scales surprisingly well on a single machine (source: designing-data-intensive-applications, chapter 10).

## Related pages

- [[storage-engines]]
- [[indexes]]
- [[hash-indexes]]
- [[b-trees]]
- [[write-amplification]]
- [[mapreduce]]
- [[batch-processing]]
