# Checkpointing (Stream Processing)

**Summary**: The mechanism heavyweight streaming frameworks use to make [[internal-state-store|internal state]] recoverable after failure or rescaling. A **checkpoint** is a snapshot of the application's current state written to external durable storage (HDFS, object storage, an HA key-value store). On failure, tasks reload their partitioned state from the most recent checkpoint and resume, with no need to replay the input stream from scratch. Checkpointing is the heavyweight-framework analogue of snapshotting an [[external-state-store]] (source: chapter-11-heavyweight-framework-microservices.md).

**Sources**: `raw/building-event-driven-microservices/chapter-11-heavyweight-framework-microservices.md`

**Last updated**: 2026-04-17

---

## Why checkpoints exist

Heavyweight frameworks favor internal state — RocksDB-style local stores, in-memory hash tables with spill-to-disk — for throughput. The risks of internal state (disk failures, node failures, aggressive CMS-driven evictions) are acceptable only if a durable recovery path exists (source: chapter-11-heavyweight-framework-microservices.md).

Checkpointing provides that path: write state to durable storage periodically, so that a restarted or rescaled task can reload the assigned partition's state and continue.

## What gets checkpointed

Two state categories must be captured together for correctness (source: chapter-11-heavyweight-framework-microservices.md):

- **Operator state** — the pairs `<partitionId, offset>`. For every input-topic partition the task reads from, where in the stream it has consumed to. `partitionId` is unique across all input topics.
- **Key state** — the pairs `<key, state>`. The domain-level state keyed by business entity: aggregation accumulators, windowed buffers, join-side materializations, reduction state, and so on.

Both must be recorded **synchronously** so that the keyed state accurately reflects exactly the events marked as consumed by the operator state. Recording one without the other risks events being processed twice (on replay) or not at all (if consumed but not reflected in state). See [[effectively-once-processing]] for the correctness framing.

## Restore semantics

On restart — whether after a failure or after a configuration change such as increased parallelism — each task (source: chapter-11-heavyweight-framework-microservices.md):

1. Fully loads its assigned partitions' key state from the checkpoint **before** accepting any new events.
2. Verifies that operator state and keyed state are mutually consistent for each partition (right partition assigned to the right task).
3. Resumes consumption from the checkpointed offsets.

Restoring from a checkpoint is **functionally equivalent to restoring an external state store from a snapshot**: the contents are the authoritative state, and processing picks up where it left off (source: chapter-11-heavyweight-framework-microservices.md).

## Where checkpoints are stored

Durable, external, highly-available storage — **external to the worker nodes themselves** so that a full cluster loss doesn't lose state (source: chapter-11-heavyweight-framework-microservices.md):

- Hadoop Distributed File System (HDFS) — the common legacy option.
- Cloud object stores (S3, GCS).
- Highly-available key/value stores.

The specifics of how each framework writes and coordinates checkpoints differ (Spark's RDD lineage plus checkpoints, Flink's asynchronous barrier snapshots, etc.). Consult the framework documentation for the particulars.

## Relationship to DDIA coverage

[[stream-processing-fault-tolerance]] (Kleppmann) covers the same territory from the DDIA angle: **microbatching** (Spark Streaming) and **operator checkpointing** (Flink) as the two recovery primitives for stream processing. See also [[dataflow-engines]] for how Flink's checkpointing differs from Spark's RDD-lineage approach for batch recovery.

## Related pages

- [[heavyweight-framework-microservice]]
- [[stream-processing-cluster]]
- [[stream-processing-scaling-strategies]]
- [[internal-state-store]]
- [[external-state-store]]
- [[stateful-stream-processing]]
- [[state-store-rebuilding-vs-migrating]]
- [[stream-processing-fault-tolerance]]
- [[effectively-once-processing]]
- [[dataflow-engines]]
