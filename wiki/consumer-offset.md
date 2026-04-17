# Consumer Offset

**Summary**: The **per-consumer, per-partition index** into an append-only event log that records how far a consumer has read. Each consumer maintains its own offsets, which lets many independent consumers read the same stream at their own paces; the gap between a consumer's offset and the tail is its **consumer lag**, a first-class scaling signal.

**Sources**: `raw/building-event-driven-microservices/chapter-02-event-driven-microservice-fundamentals.md`, `raw/building-event-driven-microservices/chapter-14-supportive-tooling.md`, `raw/designing-data-intensive-applications/chapter-11-stream-processing.md`

**Last updated**: 2026-04-17

---

## What an offset is

When an event is appended to a partition, the [[event-broker]] assigns it a **monotonically increasing index**. A consumer reads events in order and advances its offset. Because the offset belongs to the consumer rather than the event itself, many consumers can read the same partition independently, each tracking its own progress (source: chapter-02-event-driven-microservice-fundamentals.md).

Consumers can also **rewind** by setting their offset to an earlier value, enabling replay of historical events — a property log-based brokers support natively and traditional queue brokers do not (source: chapter-11-stream-processing.md).

## Consumer lag

**Consumer lag** is the difference between a consumer's current offset and the tail (latest written) offset on a partition (source: chapter-02-event-driven-microservice-fundamentals.md). It has three important uses:

- **Autoscaling input.** When lag grows, scale up consumer instances; when lag is small, scale them down.
- **Function triggering.** [[functions-as-a-service|FaaS-based]] event handlers can be awakened when lag is non-zero and scale to zero when the stream is drained.
- **Operational monitoring.** Persistent lag or unbounded lag growth is a reliable alert that a consumer is unhealthy or misconfigured.

See [[consumer-lag-monitoring]] for Chapter 14's discussion of how lag is measured as a first-class autoscaling signal, including the Burrow-style historical-deviation approach for spiky workloads (source: chapter-14-supportive-tooling.md).

## Offset management as a platform tool

Chapter 14 identifies three offset operations that need self-serve tooling: reset-to-earliest (reprocess), advance-to-latest (skip history), and set-to-specific-point (multicluster failover). All three are destructive and must be gated by the owning team — see [[application-reset-tool]] (source: chapter-14-supportive-tooling.md).

## Offsets in Bellemare's broker framing

Bellemare positions offsets as one of the minimum required features of an [[event-broker]] alongside partitioning, strict ordering, immutability, infinite retention, and replayability (source: chapter-02-event-driven-microservice-fundamentals.md). Without per-consumer offsets, multiple consumers cannot share a stream without interference, and none of the EDM patterns that depend on replay would work.

## Relationship to the wiki's existing coverage

- **[[log-based-message-brokers]]** — already describes offsets in the DDIA (Kafka-centric) idiom, including the broker-as-leader / consumer-as-follower analogy.
- **[[consumer-group]]** — the mechanism for horizontally scaling offset-based consumption.
- **[[leader-based-replication]]** — the **log sequence number** in leader-based replication is structurally the same idea as a broker offset.

## Related pages

- [[event-broker]]
- [[consumer-group]]
- [[log-based-message-brokers]]
- [[event-streams]]
- [[partitioning]]
- [[leader-based-replication]]
- [[functions-as-a-service]]
- [[consumer-lag-monitoring]]
- [[application-reset-tool]]
