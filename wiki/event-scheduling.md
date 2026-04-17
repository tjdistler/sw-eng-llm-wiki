# Event Scheduling

**Summary**: When a consumer reads from multiple partitions (possibly across multiple [[event-streams|streams]]), it must decide **which buffered event to dispatch into the topology next**. Event scheduling is that decision — and choosing by [[event-timestamps|event time]] rather than arrival order is what gives a topology [[deterministic-stream-processing|deterministic]] results.

**Sources**: `raw/building-event-driven-microservices/chapter-06-deterministic-stream-processing.md`

**Last updated**: 2026-04-17

---

## The problem

Within a single partition, records are always consumed in offset order. But a typical [[microservice-topology]] reads from several partitions at once, and the events on those partitions are interleaved in time. A naive round-robin consumer could apply a withdrawal before its earlier-happening deposit, triggering a spurious overdraft — an incorrect answer that isn't even reproducible across runs (source: chapter-06-deterministic-stream-processing.md).

The fix is to **interleave by timestamp** across input partitions, not by arrival.

## The default scheduling rule

> The most common event-scheduling implementation selects and dispatches the event with the oldest timestamp from all assigned input partitions to the downstream processing topology (source: chapter-06-deterministic-stream-processing.md).

That is: peek the head of each partition's input buffer, pick the smallest timestamp, dispatch it. This is what [[watermarks]] and [[stream-time]] implementations assume.

Event scheduling is a built-in feature of most stream-processing frameworks (Kafka Streams, Flink, Samza, Beam, Spark). Hand-rolled consumer loops typically **do not** have it — if the order of events across partitions matters to your business logic, you must add it yourself (source: chapter-06-deterministic-stream-processing.md).

## The single-partition rule

Events from one partition are always dispatched in offset order, **even if their timestamps are out of order** (source: chapter-06-deterministic-stream-processing.md). Event scheduling reorders across partitions, not within them. This is why [[out-of-order-events|out-of-order events]] within a partition produce [[late-arriving-events|late events]] downstream — the scheduler has no license to reshuffle them.

## Custom event schedulers

Frameworks like Apache Samza let you implement a custom `MessageChooser` that picks the next event based on stream priority, wall-clock time, event content, metadata, or anything else you like (source: chapter-06-deterministic-stream-processing.md).

Warning: most custom schedulers are **nondeterministic**. If the next-event decision depends on wall-clock time or on external state, rerunning the topology from an earlier offset will dispatch events in a different order and produce different output. Reserve custom schedulers for cases where reproducibility genuinely does not matter, or where the selection criterion is itself deterministic on the input.

## Request-response calls are a separate hazard

Any non-event-driven request made from inside the topology (REST call, DB lookup against an external system) introduces nondeterminism independent of scheduling — the external state may differ on replay (source: chapter-06-deterministic-stream-processing.md). Scheduling makes input ordering reproducible; it cannot make external responses reproducible.

## Related pages

- [[deterministic-stream-processing]]
- [[event-timestamps]]
- [[watermarks]]
- [[stream-time]]
- [[out-of-order-events]]
- [[late-arriving-events]]
- [[microservice-topology]]
- [[consumer-offset]]
- [[stateless-stream-processing]]
