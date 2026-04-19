# Shuffle Hash Join

**Summary**: The default distributed join strategy when neither side fits on a single node. Both tables are repartitioned across the cluster by a hash of the join key, and each node joins its local slices. More expensive than [[broadcast-join]] because both sides move over the network.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md`

**Last updated**: 2026-04-18

---

## The idea

If neither table is small enough for broadcast, the query engine uses a shuffle hash join (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md):

1. Initial partitioning of the two tables across the nodes has no particular relation to the join key.
2. A hashing scheme maps the join key to a target node — say, hash mod N for N nodes.
3. Both tables are **reshuffled**: every record is sent to the node that owns its key bucket.
4. On each node, the local slices of A and B are joined.

This is the pattern behind every distributed join system — MapReduce, BigQuery, Snowflake, Spark — though the details of intermediate storage (disk or memory) vary (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).

## Why it's expensive

Both sides traverse the network. For a join on a table of size S, you're paying up to 2× S in network shuffle before a single row is joined. [[query-performance-tuning|Pre-filtering]] and avoiding unnecessary columns cuts that cost directly.

## How it relates to MapReduce

The shuffle-hash-join pattern is structurally identical to [[mapreduce|MapReduce]]'s [[sort-merge-joins|reduce-side join]]: map tasks emit `(join_key, record)` pairs, the shuffle repartitions by key, and the reducer receives all records with the same key and joins them. Dataflow engines (Spark, Flink) retain the same primitive but keep intermediate state in memory rather than on disk where possible.

## Cross-book connections

- [[mapreduce]] — the canonical ancestor; shuffle-partitioning by hash of key is core to both.
- [[sort-merge-joins]] — DDIA's reduce-side join; the MapReduce-era name for essentially this operation.
- [[map-side-joins]] — the broadcast analogue in the MapReduce/Spark world.

## Related pages

- [[broadcast-join]]
- [[query-optimizer]]
- [[query-performance-tuning]]
- [[mapreduce]]
- [[sort-merge-joins]]
