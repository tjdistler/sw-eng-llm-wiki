# Stream Time

**Summary**: Stream time is Kafka Streams' approach to tracking [[event-timestamps|event-time]] progress: a single monotonically non-decreasing value per subtopology that equals the **highest timestamp ever processed**. It is the counterpart to [[watermarks]] but does not require explicit watermark messages or a dedicated cluster.

**Sources**: `raw/building-event-driven-microservices/chapter-06-deterministic-stream-processing.md`

**Last updated**: 2026-04-17

---

## How stream time advances

Each consumer instance buffers events from every partition it owns. The [[event-scheduling|event scheduler]] selects the buffered event with the smallest timestamp, dispatches it through the topology, and — if the event's timestamp is greater than the current stream time — advances stream time to that value (source: chapter-06-deterministic-stream-processing.md).

Two invariants (source: chapter-06-deterministic-stream-processing.md):

- Stream time **never decreases**.
- Stream time advances **per processed event**, not per watermark signal.

Example: buffers hold events at times 20 and 30. The scheduler dispatches 20 (smallest), then 30. Stream time moves 20 → 30 after the second dispatch.

## Depth-first processing

Kafka Streams processes **one event at a time through a subtopology**. The event completes every node in the subtopology before the next event is selected. This contrasts with [[watermarks|watermark-based]] frameworks, where events can sit in per-node input buffers while watermarks independently advance each node's event time (source: chapter-06-deterministic-stream-processing.md).

The depth-first model is simpler to reason about and is part of what makes Kafka Streams library-friendly (embed in any JVM app, no cluster to run).

## Subtopologies split by repartition

When a topology contains a [[repartitioning|repartition]] step, Kafka Streams uses an **internal repartition event stream** rather than an in-cluster shuffle. The repartition stream physically cuts the topology in half: everything before the repartition is one subtopology, everything after is another. Each subtopology has its own independent stream time, because each subtopology has its own source (source: chapter-06-deterministic-stream-processing.md).

Crucially, the **original event time is preserved** through the repartition stream — rewriting it to the current wall clock would destroy the temporal ordering that stream time depends on (source: chapter-06-deterministic-stream-processing.md).

## Stream time in parallel processing

Each consumer instance maintains its own stream time, and **there is no synchronization between instances** (source: chapter-06-deterministic-stream-processing.md). This is convenient — no coordination overhead — but has a direct consequence: repartitioned output streams can contain [[out-of-order-events|out-of-order events]] because two instances advance their stream times independently.

Instance 0 might already be at stream time 95 while instance 1 is still at 80; when instance 1's event with timestamp 90 arrives at the repartition stream, it lands after instance 0's event of timestamp 95 — out of order by the time the downstream subtopology sees it.

This skew is worsened by unbalanced partition sizes, unequal processing rates, or large backlogs. Handle it with the same tools as any other late-event case — see [[late-arriving-events]].

## When a stream-time event is late

An event with timestamp `t'` is **late** when it arrives after stream time has advanced past `t'` (source: chapter-06-deterministic-stream-processing.md). Each operator in the subtopology then applies its own policy — drop, update, or record the late event.

## Stream time vs watermarks

See the comparison table in [[watermarks]]. In short: stream time is simpler, single-valued, and propagates implicitly; watermarks are per-node, propagate explicitly, and coordinate parallel shuffles more precisely. Bellemare notes that Apache Samza offers a standalone (Kafka-Streams-style) deployment that nonetheless uses watermarking — the two axes (library vs cluster, stream-time vs watermark) are independent (source: chapter-06-deterministic-stream-processing.md).

## Related pages

- [[watermarks]]
- [[deterministic-stream-processing]]
- [[event-timestamps]]
- [[event-scheduling]]
- [[out-of-order-events]]
- [[late-arriving-events]]
- [[repartitioning]]
- [[microservice-topology]]
- [[stream-processing]]
