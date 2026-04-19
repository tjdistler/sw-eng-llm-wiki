# Lambda Architecture

**Summary**: An influential data architecture that runs batch and stream processing in parallel over an immutable event log -- the batch layer produces correct results while the stream layer produces fast approximate results -- later superseded by unified batch/stream processing systems.

**Sources**: `raw/designing-data-intensive-applications/chapter-12-the-future-of-data-systems.md`, `raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md`

**Last updated**: 2026-04-18

---

## Core idea

Incoming data is recorded by appending immutable events to an always-growing dataset (similarly to [[event-sourcing]]). Read-optimized views are derived from these events. The system runs two parallel processing paths (source: chapter-12-the-future-of-data-systems.md):

1. **Batch layer** (e.g., Hadoop [[mapreduce|MapReduce]]): consumes the full event history and produces a corrected, exact version of the derived view. Simpler and less prone to bugs.
2. **Stream layer** (e.g., Storm): consumes events in real time and quickly produces an approximate update to the view. Can use fast approximate algorithms.

The two outputs must be **merged** to serve user requests.

## Influence

The lambda architecture popularized two important principles (source: chapter-12-the-future-of-data-systems.md):

- **Deriving views onto streams of immutable events** rather than mutating state in place
- **Reprocessing events when needed** to rebuild or correct views

These ideas shaped the design of modern [[data-integration]] architectures.

## Practical problems

Despite its influence, the lambda architecture has significant operational drawbacks (source: chapter-12-the-future-of-data-systems.md):

1. **Dual maintenance**: maintaining the same logic in both a batch and a stream framework is significant additional effort. Libraries like Summingbird abstract over both, but the operational complexity of debugging, tuning, and maintaining two systems remains.
2. **Output merging**: merging batch and stream outputs is easy for simple tumbling-window aggregations, but becomes significantly harder for complex operations like joins, sessionization, or non-time-series outputs.
3. **Incremental batch processing**: reprocessing the entire historical dataset is expensive, so the batch pipeline often processes incremental batches (e.g., one hour's worth). This reintroduces the complexity of handling stragglers and cross-batch window boundaries, making the batch layer as complex as the stream layer.

## Successor: unified batch and stream processing

More recent systems achieve the benefits of the lambda architecture without its downsides by allowing both batch and stream computations in the **same system**. Requirements for unification (source: chapter-12-the-future-of-data-systems.md):

- **Replay historical events** through the same processing engine that handles live events. [[log-based-message-brokers]] support message replay; some stream processors can read from [[distributed-filesystems|HDFS]].
- **[[exactly-once-semantics]]**: ensuring the output is the same as if no faults occurred, by discarding partial output of failed tasks.
- **[[windowing]] by event time**, not processing time, since processing time is meaningless when reprocessing historical events.

Apache Beam provides an API for expressing such computations, runnable on Apache Flink or Google Cloud Dataflow. Spark breaks streams into microbatches, while Flink performs batch processing atop its stream engine (source: chapter-12-the-future-of-data-systems.md).

## Reprocessing for application evolution

Reprocessing existing data with new derivation code provides a powerful mechanism for system evolution. Without reprocessing, schema evolution is limited to simple changes (adding optional fields). With reprocessing, you can restructure a dataset into a completely different model. Derived views allow **gradual migration**: maintain old and new schemas side by side, shift users gradually, and roll back if something goes wrong -- analogous to converting railway gauges via a third rail (source: chapter-12-the-future-of-data-systems.md).

## Chapter 3 (FoDE) framing

Reis and Housley reinforce the DDIA framing and add historical context (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md):

- Lambda emerged in the early-to-mid 2010s alongside Kafka, Apache Storm, and Samza, as engineers needed to reconcile batch and streaming into a single architecture
- The **serving layer** combines query results from the batch and speed layers
- Chapter 3's verdict is bluntly practical: "Managing multiple systems with different codebases is as difficult as it sounds, creating error-prone systems with code and data that are extremely difficult to reconcile"
- Lambda still dominates search results for data architecture; it still shapes how people think about batch/stream reconciliation. But Chapter 3's recommendation is **don't start here**

Chapter 3 situates the successor patterns in sequence:

- [[kappa-architecture]] — Jay Kreps's 2014 response: use one stream-processing backbone and replay as needed
- [[dataflow-model]] — Google/Beam: treat batch as a special case of streaming at the programming-model level; the current default thinking

## Related pages

- [[kappa-architecture]]
- [[dataflow-model]]
- [[data-integration]]
- [[batch-processing]]
- [[stream-processing]]
- [[derived-data]]
- [[event-sourcing]]
- [[exactly-once-semantics]]
- [[windowing]]
- [[mapreduce]]
- [[dataflow-engines]]
- [[unbundling-databases]]
- [[data-architecture]]
