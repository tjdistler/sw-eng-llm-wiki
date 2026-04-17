# Event Timestamps

**Summary**: Every event in an [[event-streams|event stream]] has both an offset (consumer bookkeeping) and a timestamp (when it happened). Bellemare distinguishes four timestamps that arise along a produce-consume pipeline — event time, broker ingestion time, consumer ingestion time, and processing time — only two of which are stable enough to use for [[deterministic-stream-processing|deterministic processing]].

**Sources**: `raw/building-event-driven-microservices/chapter-06-deterministic-stream-processing.md`

**Last updated**: 2026-04-17

---

## Offset vs timestamp

In a log-based [[event-broker]] record, the **offset** tells a consumer which events it has already read; the **timestamp** tells it *when* the event occurred relative to other events (source: chapter-06-deterministic-stream-processing.md). Offsets alone can order events within a single partition; timestamps are required to order events **across** partitions and streams.

See [[consumer-offset]] for offset semantics and [[log-based-message-brokers]] for the underlying storage model.

## The four timestamps

| Timestamp | When assigned | Source of time |
|---|---|---|
| **Event time** | Locally by the producer when the event occurred | Producer system clock |
| **Broker ingestion time** | By the [[event-broker]] when the record is appended | Either copy of event time *or* broker's local clock (configurable) |
| **Consumer ingestion time** | When the consumer reads the record | Event-time field in record *or* consumer's wall clock |
| **Processing time** | When the consumer finishes processing the event | Consumer wall clock |

(source: chapter-06-deterministic-stream-processing.md)

Event time and broker ingestion time are each assigned **once** per record. Consumer ingestion and processing time change every time the consumer runs, which is why they can't anchor reproducible results (source: chapter-06-deterministic-stream-processing.md).

## Which timestamp to use

For the most accurate picture of the real world, use **event time** — the producer-assigned timestamp that travels with the record (source: chapter-06-deterministic-stream-processing.md). This is the timestamp [[watermarks]] and [[stream-time]] propagate.

Fall back to **broker ingestion time** when producers cannot be trusted to assign reliable timestamps (old systems, unsynchronized clocks, tamper concerns). This is almost as accurate except when the producer cannot reach the broker for a while — see [[late-arriving-events]] for the connectivity-outage failure mode.

Avoid wall-clock (consumer ingestion / processing) time for business logic whenever the topology may be replayed, since it makes the output depend on when the code happens to run — breaking [[deterministic-stream-processing|determinism]].

## Timestamp extraction

At consumer ingestion, a **timestamp extractor** pulls the event-time value from the record (source: chapter-06-deterministic-stream-processing.md). It can read the event key, value, or metadata — wherever the producer stored the canonical time. Once extracted, this timestamp drives [[event-scheduling|scheduling]], [[windowing]], and [[watermarks|watermark]] / [[stream-time]] advancement for the rest of the topology.

## Synchronizing distributed clocks

Timestamps from different producers are comparable only to the extent their clocks agree. Bellemare's practical guidance (source: chapter-06-deterministic-stream-processing.md):

- **NTP within a LAN** keeps drift in the low-millisecond range with frequent resync (often sub-millisecond with modern NTP + GPS).
- **NTP across the open internet** is roughly ±100 ms and should inform business tolerances.
- Cloud providers (AWS, GCP) expose satellite / atomic-clock time sources in each region.
- NTP synchronization itself can fail — network outages, misconfig, or a bad upstream server will let clocks drift silently.

For most business cases, frequent NTP sync is "good enough"; remaining out-of-order issues are handled by [[late-arriving-events|late-event strategies]]. See [[clock-synchronization]] and [[unreliable-clocks]] for the deeper distributed-systems angle from DDIA.

## Related pages

- [[deterministic-stream-processing]]
- [[event-scheduling]]
- [[watermarks]]
- [[stream-time]]
- [[windowing]]
- [[event-structure]]
- [[event-streams]]
- [[clock-synchronization]]
- [[unreliable-clocks]]
- [[log-based-message-brokers]]
- [[consumer-offset]]
