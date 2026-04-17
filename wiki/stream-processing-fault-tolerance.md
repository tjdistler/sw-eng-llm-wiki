# Stream Processing Fault Tolerance

**Summary**: Achieving [[fault-tolerance]] in [[stream-processing]] is harder than in [[batch-processing]] because streams are infinite -- you cannot simply restart from the beginning or wait until a task finishes before revealing output. Techniques include microbatching, checkpointing, atomic commits, and idempotent writes.

**Sources**: `raw/designing-data-intensive-applications/chapter-11-stream-processing.md`

**Last updated**: 2026-04-15

---

## The challenge

In [[batch-processing]], fault tolerance is straightforward: failed tasks are restarted from the beginning, partial output is discarded, and input files are immutable. The visible effect is as if every record was processed exactly once. This is called **exactly-once semantics** (or more precisely, **effectively-once**) (source: chapter-11-stream-processing.md).

Stream processing cannot use the same approach because (source: chapter-11-stream-processing.md):
- A stream is infinite -- restarting from the beginning after a crash is not viable for a job that has been running for years
- Output is produced continuously -- you cannot wait until the task "finishes" to reveal output, because it never finishes

## Microbatching

Break the stream into small blocks and treat each as a miniature batch process. Used by **Spark Streaming** (source: chapter-11-stream-processing.md).

- Typical batch size: ~1 second (a compromise: smaller batches add scheduling overhead, larger batches increase output latency)
- Implicitly provides a [[windowing|tumbling window]] equal to the batch size (by processing time, not event time)
- Jobs needing larger windows must explicitly carry state across microbatches
- Within the framework, provides exactly-once semantics like batch processing

## Checkpointing

Periodically generate rolling checkpoints of operator state and write them to durable storage. Used by **Apache Flink** (source: chapter-11-stream-processing.md).

- If an operator crashes, it restarts from the most recent checkpoint
- Output generated between the last checkpoint and the crash is discarded
- Checkpoints are triggered by **barriers** in the message stream, similar to microbatch boundaries but without forcing a particular window size
- Provides exactly-once semantics within the framework

This approach is related to Flink's fault tolerance mechanism for [[dataflow-engines]], where operator state snapshots are written to durable storage like HDFS (source: chapter-11-stream-processing.md).

## The external side-effect problem

Both microbatching and checkpointing provide exactly-once semantics **within the stream processing framework**. However, once output leaves the framework -- writing to a database, sending an email, pushing to an external message broker -- the framework cannot discard the output of a failed batch or roll back to a checkpoint. Restarting a failed task causes the external side effect to happen twice (source: chapter-11-stream-processing.md).

## Atomic commit

To achieve exactly-once semantics including external effects, all outputs and side effects of processing an event must take effect atomically: messages sent downstream, database writes, operator state changes, and input acknowledgments must all happen together or not at all (source: chapter-11-stream-processing.md).

This is the same problem as [[two-phase-commit|distributed transactions]], but stream processing frameworks implement a more efficient version (source: chapter-11-stream-processing.md):

| Aspect | Traditional XA | Stream processing atomic commit |
|---|---|---|
| Scope | Heterogeneous technologies | Internal to the framework |
| Performance | High overhead | Amortized over many messages per transaction |
| Examples | XA/JTA | Google Cloud Dataflow, VoltDB, Apache Kafka (planned at time of writing) |

The key difference: stream processing atomic commits do not attempt transactions across heterogeneous systems. They keep state changes and messaging within the framework (source: chapter-11-stream-processing.md).

## Idempotence

An alternative to distributed transactions: make operations **idempotent** -- performing them multiple times has the same effect as performing them once (source: chapter-11-stream-processing.md).

- **Naturally idempotent**: setting a key-value pair to a fixed value (writing the same value again is harmless)
- **Not idempotent**: incrementing a counter (incrementing twice gives a different result)
- **Made idempotent with metadata**: include the Kafka message offset with each database write. Before writing, check whether the offset has already been applied. Storm's Trident uses a similar approach.

Requirements for idempotence-based fault tolerance (source: chapter-11-stream-processing.md):
- Failed tasks must replay the same messages in the same order ([[log-based-message-brokers]] provide this)
- Processing must be deterministic
- No other node may concurrently update the same value
- [[fencing-tokens|Fencing]] may be needed during failover to prevent interference from a node thought dead but actually alive

Despite these caveats, idempotent operations can be an effective way to achieve exactly-once semantics with low overhead (source: chapter-11-stream-processing.md).

## Rebuilding state after failure

Stream processors that maintain state (windowed aggregations, join tables, indexes) must ensure state survives failures. Options (source: chapter-11-stream-processing.md):

| Approach | How it works | Example |
|---|---|---|
| Remote replicated store | Keep state in a remote database | Simple but slow (network round-trip per message) |
| Periodic snapshots | Capture local state periodically, write to durable storage | Flink snapshots to HDFS |
| State change replication | Send state changes to a dedicated Kafka topic with log compaction | Samza, Kafka Streams |
| Redundant processing | Process each input on multiple nodes | VoltDB |
| Rebuild from input | Replay input events to reconstruct state | Fast only for short [[windowing|windows]] |
| Rebuild from CDC | Reconstruct from [[change-data-capture|log-compacted change stream]] | When state is a local database replica |

The best approach depends on infrastructure characteristics: in some systems network delay is lower than disk latency, in others disk bandwidth exceeds network bandwidth. There is no universally ideal trade-off (source: chapter-11-stream-processing.md).

## Related pages

- [[stream-processing]]
- [[fault-tolerance]]
- [[batch-processing]]
- [[dataflow-engines]]
- [[log-based-message-brokers]]
- [[two-phase-commit]]
- [[distributed-transactions]]
- [[change-data-capture]]
- [[windowing]]
- [[fencing-tokens]]
- [[idempotence]]
