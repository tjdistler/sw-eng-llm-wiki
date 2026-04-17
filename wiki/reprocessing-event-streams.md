# Reprocessing Event Streams

**Summary**: Because [[event-streams|event streams]] retained in a [[log-based-message-brokers|log-based broker]] are immutable and replayable, an [[event-driven-microservices|event-driven microservice]] can **rewind its consumer offsets and re-run**. Reprocessing is how bug fixes, schema changes, new business logic, and new consumers are rolled out — but it only produces correct results when the topology is [[deterministic-stream-processing|deterministic]].

**Sources**: `raw/building-event-driven-microservices/chapter-06-deterministic-stream-processing.md`

**Last updated**: 2026-04-17

---

## Why reprocessing is a first-class operation

Every event-driven microservice must be designed for reprocessing, not just near–real-time operation (source: chapter-06-deterministic-stream-processing.md). Reasons to reprocess:

- Bug in business logic — need correct output for the whole history.
- New business rule introduced — need to retroactively apply it.
- A new microservice joins the platform and needs to build state from the beginning of time.
- Autoscaling / recovery — an [[consumer-group|instance]] that has fallen far behind is effectively reprocessing.

Reprocessing is only meaningful for topologies that use **[[event-timestamps|event time]]**. A topology keyed on wall-clock time or external-service responses cannot be reprocessed — the output depends on when the code runs (source: chapter-06-deterministic-stream-processing.md).

## Bellemare's five-step checklist

When you decide to reprocess a stream (source: chapter-06-deterministic-stream-processing.md):

### 1. Determine the starting point
Stateful consumers should typically reset to the **beginning** of each subscribed stream. Starting mid-history risks ending up with wrong state (the bank-balance-missing-paychecks warning).

### 2. Determine which offsets to reset
Every stream feeding into stateful processing must be reset to the beginning. Non-stateful side streams can sometimes be left alone. [[consumer-offset]] mechanics determine how you do this.

### 3. Consider the volume of data
Some streams are massive. Reprocessing may take hours. Apply [[event-broker]] quotas if you risk overwhelming the broker with I/O. Notify downstream consumers so they can scale up to absorb the burst of output.

### 4. Consider the time to reprocess
Scale up to maximum parallelism while reprocessing; scale back when caught up. Estimate downtime up front and confirm downstream consumers can tolerate stale data during the catch-up window.

### 5. Consider the business impact
Replay can cause bad side effects — an "order shipped" notification service should not **re-email** users during reprocessing. Flag every externally visible action in the topology and suppress or dedupe on replay. This is the usual argument for [[idempotence|idempotent]] outputs and the reason event-driven side-effect code should use [[exactly-once-semantics|effectively-once]] patterns.

## The event-scheduling dependency

Reprocessing produces correct results only if events are dispatched in the same order they were during live processing. This is precisely what [[event-scheduling|event scheduling]] by timestamp guarantees — the same timestamps, the same merge order, the same output (source: chapter-06-deterministic-stream-processing.md).

A broken scheduler (e.g., a custom scheduler that uses wall-clock time) means reprocessing ≠ live processing. Likewise, [[out-of-order-events|out-of-order events]] introduced by [[repartitioning|repartition]] with independent [[stream-time|stream times]] must be handled identically in both modes via [[late-arriving-events|late-event policies]].

## Why reprocessing can produce *better* output than live

During live processing, a short [[event-broker]] connectivity outage at a producer makes events that arrive later look late; during reprocessing, the same events are already in-order in the stored log (source: chapter-06-deterministic-stream-processing.md). Reprocessing the historical record therefore produces more complete, more deterministic results than the original near–real-time run — one more reason it is a routine operation, not an emergency one.

## Related pages

- [[deterministic-stream-processing]]
- [[event-scheduling]]
- [[event-timestamps]]
- [[out-of-order-events]]
- [[late-arriving-events]]
- [[watermarks]]
- [[stream-time]]
- [[consumer-offset]]
- [[consumer-group]]
- [[log-based-message-brokers]]
- [[idempotence]]
- [[exactly-once-semantics]]
- [[event-sourcing]]
