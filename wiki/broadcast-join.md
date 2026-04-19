# Broadcast Join

**Summary**: A distributed join strategy in which the query engine sends a small table to every node in the cluster, where it is joined against the local portion of a large table. Dramatically cheaper than a [[shuffle-hash-join]] when one side fits on a single node.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md`

**Last updated**: 2026-04-18

---

## The idea

A broadcast join is generally **asymmetric**: one large table is distributed across nodes, and one small table is small enough to fit on a single node. The query engine broadcasts the small table (table A) to every node, where it gets joined against the local part of the large table (table B). The large table never moves (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).

Broadcast joins are far less compute-intensive than shuffle hash joins — no network shuffle of the big table, no repartitioning on the join key.

## When it applies

The small side must fit in memory on a single node. In practice, table A is often a **down-filtered larger table** — the optimizer applies predicates and realizes the surviving rows are small enough to broadcast. One of the top priorities of a modern [[query-optimizer]] is **join reordering** that creates broadcast opportunities: apply filters early, push small tables to the left of left-joins, and re-examine size after each filter (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).

## Practical tuning

[[query-performance-tuning]]: pre-filtering to create broadcast joins where possible can dramatically improve performance and reduce resource consumption. If you can't get below the broadcast threshold, the engine falls back to [[shuffle-hash-join]].

## Cross-book connections

- [[map-side-joins]] — DDIA's broadcast-hash-join variant in the batch world: the small dataset is loaded into every mapper's memory and the large one is streamed past it. Same idea, different vocabulary.
- [[sort-merge-joins]] — the alternative strategy when neither side is small.

## Related pages

- [[shuffle-hash-join]]
- [[query-optimizer]]
- [[query-performance-tuning]]
- [[map-side-joins]]
- [[sort-merge-joins]]
