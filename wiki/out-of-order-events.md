# Out-of-Order Events

**Summary**: An event is **out of order** when its [[event-timestamps|timestamp]] is smaller than that of an event preceding it in an [[event-streams|event stream]]. Out-of-order events are the normal state of affairs in real stream processing, and every serious [[microservice-topology|topology]] must decide how to handle them.

**Sources**: `raw/building-event-driven-microservices/chapter-06-deterministic-stream-processing.md`

**Last updated**: 2026-04-17

---

## Definition

Given events A, B, C appearing consecutively in a partition with timestamps `t_A < t_C < t_B`, event B is out of order — its timestamp is smaller than the preceding C's (source: chapter-06-deterministic-stream-processing.md). Note the difference from [[late-arriving-events|late events]]: out-of-order is a property of the stream; late is a property of how a specific consumer interprets that out-of-orderness relative to its [[watermarks|watermark]] or [[stream-time|stream time]].

Events from a single partition are always processed in **offset order**, so an out-of-order event *stays* out of order through downstream processing (source: chapter-06-deterministic-stream-processing.md). [[event-scheduling|Event scheduling]] reorders across partitions, not within them.

## Bounded vs unbounded data

- **Bounded batch inputs**: mostly resilient to out-of-order data — the entire batch is effectively one large window and a late record by minutes or hours is irrelevant if processing hasn't started yet. The trade-off is latency measured in hours (source: chapter-06-deterministic-stream-processing.md).
- **Unbounded streams**: the developer must choose between latency and [[deterministic-stream-processing|determinism]] explicitly, because you cannot wait indefinitely for all events to arrive.

## How out-of-order events arise

Bellemare identifies three common causes (source: chapter-06-deterministic-stream-processing.md):

### 1. Sourcing from an already-out-of-order stream
If an upstream producer publishes out-of-order records (e.g., it sources from an external system with unreliable timestamps), every downstream consumer inherits the problem.

### 2. Multiple producers writing to multiple partitions
A producer fleet writing concurrently to multiple partitions has no global ordering guarantee — each producer only orders its own writes to its own destination.

### 3. Repartitioning with independent stream times
The most common in practice. When two consumer instances [[repartitioning|repartition]] an event stream, each maintains its own [[stream-time|stream time]] with no synchronization. A small skew — instance 0 at event time 95 while instance 1 is still at 90 — means instance 1's event of time 90 lands in the repartitioned stream **after** instance 0's event of time 95. The skew compounds with unbalanced partitions, unequal processing rates, and large backlogs (source: chapter-06-deterministic-stream-processing.md).

A **single-threaded producer** drawing from an in-order source will not introduce out-of-order events in normal operation (source: chapter-06-deterministic-stream-processing.md).

## Impact

The main impact: you cannot count on event times being monotonically non-decreasing within a partition. This affects (source: chapter-06-deterministic-stream-processing.md):

- **[[windowing|Windowed aggregations]]** — a late event may arrive after the window is considered complete.
- **Time-triggered logic** — "emit a summary 5 minutes after the last event in this session" can be falsely triggered if a later event then appears.
- **Downstream [[watermarks]] / [[stream-time]]** — advancing past a timestamp and then seeing an older one forces late-event policy to engage.

How aggressively you must mitigate depends entirely on business requirements — see [[late-arriving-events]] for the drop / wait / grace-period decision.

## Design implications

- Use **event time** not processing time for anything temporal; processing time makes reprocessing nondeterministic.
- Design [[keyed-event|keys]] and [[copartitioning|partitioning]] so that events that must be ordered together actually stay on the same partition.
- For data where temporal correctness matters more than latency (financial transactions), use longer grace periods or [[reprocessing-event-streams|reprocess]] overnight when more complete data is available.

## Related pages

- [[late-arriving-events]]
- [[event-timestamps]]
- [[event-scheduling]]
- [[watermarks]]
- [[stream-time]]
- [[windowing]]
- [[repartitioning]]
- [[deterministic-stream-processing]]
- [[reprocessing-event-streams]]
