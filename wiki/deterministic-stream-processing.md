# Deterministic Stream Processing

**Summary**: A [[stream-processing|stream processor]] is **deterministic** when rewinding its consumer offsets and re-running it produces the same output as the original run. Because real networks, clocks, and producers are imperfect, the practical goal is **best-effort determinism**: results that are reproducible whenever all inputs are eventually available.

**Sources**: `raw/building-event-driven-microservices/chapter-06-deterministic-stream-processing.md`

**Last updated**: 2026-04-17

---

## Why determinism matters

An [[event-driven-microservices|event-driven microservice]] has two modes of operation (source: chapter-06-deterministic-stream-processing.md):

- **Near–real-time processing** — consuming events as they arrive.
- **Catch-up / reprocessing** — consuming historical events from an earlier [[consumer-offset|offset]], possibly the beginning of the stream.

The overarching goal: the microservice should produce **the same output in both modes**. Bugs, logic changes, new consumers, and scaling all require [[reprocessing-event-streams|reprocessing]], so reproducibility is a first-class concern.

## What makes full determinism impossible

Full determinism would require every event to arrive on time with zero latency, no producer/consumer failures, and no network issues — which no real system achieves (source: chapter-06-deterministic-stream-processing.md). Additional inherently nondeterministic sources include:

- **Wall-clock time** — topologies keyed on the current time cannot be reproduced.
- **External service queries** — the response depends on when the query is issued. See also [[synchronous-microservices]] caveats.
- **Custom [[event-scheduling|event schedulers]] keyed on non-event data** — prioritization schemes based on wall clock, content, or external state.

If a topology does any of these, determinism guarantees must be explicitly scoped.

## Ingredients of best-effort determinism

Five components work together (source: chapter-06-deterministic-stream-processing.md):

1. **Consistent [[event-timestamps|timestamps]]** — synchronized across producers via NTP.
2. **Well-selected event keys** — so related events land in the same partition. See [[keyed-event]], [[copartitioning]].
3. **Partition assignment** — stable, understood by all instances. See [[partition-assignor]].
4. **[[event-scheduling|Event scheduling]]** — pick the next event by timestamp, not by offset alone, when consuming multiple partitions.
5. **[[late-arriving-events|Late-event handling]]** — drop / wait / grace-period strategies chosen per business requirement.

Mechanisms like [[watermarks]] and [[stream-time]] exist specifically to track event-time progress and decide when an event is late.

## Determinism and the partition rule

Events from a **single partition** must always be processed in offset order, regardless of timestamp (source: chapter-06-deterministic-stream-processing.md). Determinism does not mean re-sorting within a partition; it means choosing **which partition to pull from next** such that the global processing order is reproducible.

## Implications for microservice design

- Prefer event time over processing time for any time-based logic ([[windowing]], aggregations, triggers).
- Beware side effects that are nondeterministic on replay: emails, external API calls, wall-clock-based decisions. See the impact-on-reprocessing discussion in [[reprocessing-event-streams]].
- Document which parts of the topology are deterministic and which are not — business requirements will decide how much nondeterminism is acceptable.

## Related pages

- [[event-timestamps]]
- [[event-scheduling]]
- [[watermarks]]
- [[stream-time]]
- [[out-of-order-events]]
- [[late-arriving-events]]
- [[reprocessing-event-streams]]
- [[windowing]]
- [[stream-processing]]
- [[stream-processing-fault-tolerance]]
- [[idempotence]]
- [[exactly-once-semantics]]
