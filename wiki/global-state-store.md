# Global State Store

**Summary**: A special form of [[internal-state-store]] in which **every microservice instance materializes every partition** of an input stream, rather than only its assigned partitions. Global state gives each instance a full copy of a reference dataset for cross-partition lookups, at the cost of replicating the data N times. It is appropriate for small, slowly-changing dimension tables; it is *not* appropriate as the driver of event-driven logic.

**Sources**: `raw/building-event-driven-microservices/chapter-07-stateful-streaming.md`

**Last updated**: 2026-04-17

---

## What makes it global

A normal [[materialized-state|materialized]] store only holds the partitions the instance owns (the ones assigned by the [[partition-assignor]]). A global state store ignores partition assignments and consumes the full stream on every instance, producing **a complete copy of the source dataset on every instance** (source: chapter-07-stateful-streaming.md).

That eliminates the partition-locality constraint that drives [[copartitioning]]: any instance can look up any key in the global store, regardless of how the *input* event was partitioned.

## When to use it

Three conditions should hold (source: chapter-07-stateful-streaming.md):

- The dataset is **small**. Every instance is paying the disk and memory cost.
- It is **slowly changing**. Currency rates, country codes, product categories, tax-jurisdiction tables.
- It is **widely referenced**. The cross-partition lookup actually buys you something compared to the alternative of [[repartitioning]] the input on the reference key.

Bellemare's summary phrase: "common data set lookup and dimension tables" (source: chapter-07-stateful-streaming.md).

## When *not* to use it

**Never use global materialization as the driver for event-driven logic.** Because every instance sees every event, if the logic is "on each event, do X," every instance will do X — producing duplicate outputs and nondeterministic results (source: chapter-07-stateful-streaming.md).

Global stores are strictly **passive** — they serve reads from the main partition-assigned processing loop. The processing loop is still driven by partition-assigned input streams.

## Relationship to other patterns

- A global KTable in Kafka Streams is the concrete instantiation of this pattern.
- The idea is adjacent to "broadcast hash join" in batch processing (see [[map-side-joins]]) — a small table is replicated to every worker to enable efficient per-record lookup.
- The opposite trade-off is to [[repartitioning|repartition]] the input stream on the reference key so that a partition-assigned materialization suffices. Repartitioning pays a one-time shuffle cost; global materialization pays an ongoing replication cost.

## Related pages

- [[internal-state-store]]
- [[materialized-state]]
- [[stateful-stream-processing]]
- [[copartitioning]]
- [[repartitioning]]
- [[partition-assignor]]
- [[map-side-joins]]
- [[stream-joins]]
