# Map-Side Joins

**Summary**: Map-side joins bypass the expensive sort-and-shuffle phase of MapReduce by exploiting known properties of the input data — small size, matching partitioning, or pre-sorting. They use a cut-down MapReduce job with no reducers.

**Sources**: `raw/designing-data-intensive-applications/chapter-10-batch-processing.md`

**Last updated**: 2026-04-15

---

## When to use map-side joins

[[sort-merge-joins|Reduce-side joins]] make no assumptions about input data but pay for sorting, copying, and merging. Map-side joins avoid that cost when the input data has known structural properties (source: designing-data-intensive-applications, chapter 10).

In a map-side join, each mapper reads an input file block and writes an output file — no reducers, no sorting.

## Three variants

### Broadcast hash join

**Condition**: One input is small enough to fit in memory (source: designing-data-intensive-applications, chapter 10).

**How it works**: Each mapper loads the small dataset into an in-memory hash table, then scans its partition of the large dataset, looking up each record's join key in the hash table.

The word "broadcast" reflects that the small input is sent to every mapper. The word "hash" reflects the use of a hash table.

**Alternative**: Instead of an in-memory hash table, store the small input in a read-only index on local disk. Frequently accessed parts stay in the OS page cache, providing near-memory-speed lookups without the memory constraint (source: designing-data-intensive-applications, chapter 10).

**Tool support**: Pig ("replicated join"), Hive ("MapJoin"), Cascading, Crunch, and data warehouse engines like Impala (source: designing-data-intensive-applications, chapter 10).

### Partitioned hash join

**Condition**: Both inputs are partitioned the same way — same key, same hash function, same number of partitions (source: designing-data-intensive-applications, chapter 10).

**How it works**: Each mapper loads only its partition of the small dataset into a hash table (not the entire dataset), then scans its corresponding partition of the large dataset. Since matching records are guaranteed to be in the same partition, this is sufficient.

**Advantage**: Each mapper's hash table is smaller than in a broadcast join — only one partition's worth of data.

**Tool support**: Hive ("bucketed map join") (source: designing-data-intensive-applications, chapter 10).

### Map-side merge join

**Condition**: Both inputs are partitioned the same way AND sorted by the same key (source: designing-data-intensive-applications, chapter 10).

**How it works**: The mapper reads both input files incrementally in ascending key order, merging them like a reducer would. No hash table needed — the data doesn't need to fit in memory.

This is the same merge operation a reducer performs in a [[sort-merge-joins|sort-merge join]], but it happens in the map phase because the data is already sorted (source: designing-data-intensive-applications, chapter 10).

## Output characteristics

The output of a map-side join is partitioned and sorted in the same way as the large input (one output file per input file block). This differs from reduce-side joins, whose output is partitioned and sorted by the join key. This distinction matters for downstream jobs that consume the output (source: designing-data-intensive-applications, chapter 10).

## Metadata requirements

Map-side joins require knowing more than just the encoding format and directory name of the input. You must also know (source: designing-data-intensive-applications, chapter 10):

- The number of partitions
- The key by which data is partitioned
- The key by which data is sorted (if applicable)

In the Hadoop ecosystem, this metadata is maintained in HCatalog and the Hive metastore (source: designing-data-intensive-applications, chapter 10).

## Related pages

- [[sort-merge-joins]]
- [[batch-processing]]
- [[mapreduce]]
- [[partitioning]]
- [[partitioning-strategies]]
- [[dataflow-engines]]
