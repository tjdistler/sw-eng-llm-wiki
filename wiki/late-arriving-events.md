# Late-Arriving Events

**Summary**: A **late event** is an [[out-of-order-events|out-of-order event]] that arrives after the consumer's notion of time has already moved past it — past a [[watermarks|watermark]] `W(t)` or past the current [[stream-time|stream time]] `t`. How to handle late events is a **business decision first, engineering decision second**, and Bellemare frames three canonical strategies: drop, wait, and grace period.

**Sources**: `raw/building-event-driven-microservices/chapter-06-deterministic-stream-processing.md`

**Last updated**: 2026-04-17

---

## Late is consumer-relative

There is no objective "late" — only "late relative to a specific consumer." One microservice may treat any out-of-order event as late; another may tolerate hours of skew before it stops accepting them (source: chapter-06-deterministic-stream-processing.md). The framework mechanism differs:

- **[[watermarks|Watermark]] model**: event `t'` is late when it arrives after watermark `W(t)` with `t' < t`.
- **[[stream-time]] model**: event `t'` is late when it arrives after stream time has advanced past `t'`.

Either way, the operator (not the framework) decides what to do.

## Three handling strategies

Bellemare's canonical options (source: chapter-06-deterministic-stream-processing.md):

### Drop
Discard the event. The window is closed, aggregations are emitted, and the late data is simply lost. Lowest latency, lowest state cost, worst determinism. Appropriate for approximate analytics where one stray measurement doesn't matter.

### Wait
Hold the window's output until a fixed wait period has passed beyond the window's end. Higher determinism, higher latency. Old windows remain in memory/state until their wait clock elapses. Good when downstream consumers cannot handle retractions but can tolerate some extra delay.

### Grace period
Emit the window result as soon as the window closes, **then keep the window alive** for a grace interval. Any late event arriving within the grace period triggers an **updated** output (a retraction + re-emission, or an incremental update). Low initial latency with eventual correctness. Requires downstream consumers that can cope with updates to previously reported results.

Regardless of strategy, events arriving **after** the chosen tolerance are always discarded — waiting indefinitely is never an option (source: chapter-06-deterministic-stream-processing.md).

## Business questions that drive the choice

Bellemare's checklist (source: chapter-06-deterministic-stream-processing.md):

- How likely are late events to occur?
- How long does the service need to guard against them?
- What is the business impact of dropping them?
- What is the business benefit of waiting for them?
- How much disk or memory is needed to keep the windows open?
- Do waiting costs outweigh benefits?

Critical events (financial transactions, fraud signals, safety alerts) usually justify a long grace period. Measurement-style telemetry (one temperature reading out of thousands) may be fine to drop.

The book's bank-account example illustrates: a deposit followed by an immediate withdrawal must be processed in correct order regardless of lateness, because an out-of-order processing causes a bogus overdraft charge. A one-hour grace window might be the explicit policy.

## Connection to intermittent failures

A recurring real-world source of "late" events: a producer cannot reach the [[event-broker]] for some minutes, then uploads a backlog of records with correct event times but delayed publication (source: chapter-06-deterministic-stream-processing.md). Near–real-time consumers will have already advanced their watermark / stream time past those events, marking them late — even though during a full [[reprocessing-event-streams|reprocess]] the same events would be in-order.

Mitigations:

- **Pre-processing wait**: delay advancing event time by a fixed amount, giving producers a chance to catch up. Incurs latency tax proportional to the guard window.
- **Robust late-event logic** at every stateful operator — effectively a grace-period policy covering expected producer/broker outage durations.

This asymmetry — late during live processing, in-order during replay — is an argument for reprocessing over trusting that live output was ever fully correct.

## Windowing caveat

[[windowing|Windowed operators]] (tumbling, sliding, session) are the canonical place where late handling matters, because "window closed" is exactly the deadline against which lateness is measured. Without a late policy, windowing over an unbounded stream has no defined semantics for the trailing edge (source: chapter-06-deterministic-stream-processing.md).

## Related pages

- [[out-of-order-events]]
- [[watermarks]]
- [[stream-time]]
- [[windowing]]
- [[event-timestamps]]
- [[deterministic-stream-processing]]
- [[reprocessing-event-streams]]
- [[stream-processing-fault-tolerance]]
- [[event-scheduling]]
