# Sort-Merge Joins

**Summary**: Sort-merge joins (also called reduce-side joins) are the default join strategy in MapReduce. Mappers extract join keys, the framework sorts and partitions the data, and reducers merge the sorted streams to perform the actual join — bringing all related data to the same place.

**Sources**: `raw/designing-data-intensive-applications/chapter-10-batch-processing.md`, `raw/designing-distributed-systems/chapter-12-coordinated-batch-processing.md`

**Last updated**: 2026-04-16

---

## How it works

In a sort-merge join, the join is performed in the reducer. Mappers prepare the data; sorting and partitioning bring related records together (source: designing-data-intensive-applications, chapter 10):

1. **Map phase**: Separate mappers process each input dataset. All mappers extract the same join key (e.g., user ID) and emit it along with the relevant value.
2. **Shuffle**: The MapReduce framework partitions mapper output by key (hash of the join key) and sorts within each partition.
3. **Reduce phase**: The reducer receives all records with the same key, from both datasets, adjacent in the sorted input. It performs the join logic.

### Secondary sort

The framework can arrange records so that within a given key, records appear in a controlled order. For example, the user database record always appears before the activity events. This is called **secondary sort** — the reducer sees the dimension record first, stores it in a local variable, then iterates over the fact records (source: designing-data-intensive-applications, chapter 10).

### Performance characteristics

The reducer only needs to keep one record (from the small side of the join) in memory at a time. It never makes network requests. This makes it a simple, single-threaded, high-throughput operation (source: designing-data-intensive-applications, chapter 10).

## The "bringing related data together" pattern

Sort-merge joins are an instance of a broader pattern: using mappers as message senders and the sort/partition process as a delivery mechanism. A key-value pair emitted by a mapper is like a message addressed to a reducer — all pairs with the same key arrive at the same destination (source: designing-data-intensive-applications, chapter 10).

This pattern also applies to **GROUP BY** operations: set the mapper's key to the grouping key, and the reducer receives all records in each group. Common aggregations include COUNT, SUM, and top-k ranking (source: designing-data-intensive-applications, chapter 10).

**Sessionization** is another application: group all activity events for a user session by using a session cookie or user ID as the grouping key (source: designing-data-intensive-applications, chapter 10).

## Handling skew (hot keys)

The pattern breaks down when a single key has disproportionately many records (e.g., a celebrity on a social network). One reducer processes far more data than others, causing the entire job to stall. This is the same skew problem described in [[partitioning]] (source: designing-data-intensive-applications, chapter 10).

Compensation algorithms:

| Technique | Tool | How it works |
|---|---|---|
| Skewed join | Pig | A sampling job identifies hot keys. Records for hot keys are sent to random reducers (not deterministic hash). The other join input is replicated to all reducers handling the hot key. |
| Sharded join | Crunch | Same idea, but hot keys are specified explicitly rather than discovered by sampling. |
| Skewed join optimization | Hive | Hot keys declared in table metadata. Records for hot keys stored in separate files and joined using a [[map-side-joins\|map-side join]]. |
| Two-stage aggregation | General | First stage: send to random reducers for partial aggregation. Second stage: combine partial results into final aggregates. |

(source: designing-data-intensive-applications, chapter 10)

## Note on two uses of "join"

DDIA's "join" here is the relational-algebra operator: match records from two datasets by a common key and combine them. Burns's [[join-pattern|Chapter 12 join pattern]] uses the word differently — it is a **barrier synchronization** that waits for every upstream parallel worker to complete before releasing downstream work (source: raw/designing-distributed-systems/chapter-12-coordinated-batch-processing.md). Both legitimately carry the name because both "bring parallel work together," but they describe different mechanisms: a sort-merge join is what the reducer *does* with paired records, while a Burns barrier-join is about *when* the downstream stage may start. MapReduce's implicit "wait for every mapper before any reducer starts" semantics is an instance of Burns's barrier-join sitting above the relational join that the reducer eventually performs.

## Comparison to map-side joins

Sort-merge joins make **no assumptions** about the input data — they work regardless of data properties. The cost is sorting, shuffling, and merging across the network. [[map-side-joins]] avoid this cost by exploiting properties of the input (small size, co-partitioning, pre-sorting), but require those properties to hold (source: designing-data-intensive-applications, chapter 10).

## Related pages

- [[batch-processing]]
- [[mapreduce]]
- [[map-side-joins]]
- [[partitioning]]
- [[partitioning-strategies]]
- [[dataflow-engines]]
- [[join-pattern]]
- [[coordinated-batch-pattern]]
