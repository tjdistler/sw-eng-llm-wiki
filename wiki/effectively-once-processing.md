# Effectively-Once Processing

**Summary**: Bellemare's Chapter 7 term (elsewhere in the literature called **exactly-once**) for the property that updates to a stateful microservice's single source of truth are applied **consistently**, regardless of producer, consumer, or broker failures. Two concrete implementation paths: a **client-broker transaction** that atomically commits input offsets, changelog writes, and output events (Kafka's model); or, when broker transactions are not available, a **local transaction between the consumer and its state store** plus explicit deduplication guards.

**Sources**: `raw/building-event-driven-microservices/chapter-07-stateful-streaming.md`

**Last updated**: 2026-04-17

---

## Effectively-once vs exactly-once

Bellemare is careful about the terminology: "effectively once processing is also sometimes described as exactly once processing, though this is not quite accurate" (source: chapter-07-stateful-streaming.md). A microservice may process the same event multiple times — due to failures and recoveries — but as long as the **committed effect on the single source of truth** is applied consistently, the outcome is correct. The literal execution count is not 1; the *observed effect* is.

This matches Kleppmann's framing (see [[exactly-once-semantics]]). For most brokers and most use cases, the two terms are used interchangeably.

## The stock-accounting worked example

Chapter 7 illustrates the problem with a stock-accounting service that tracks running inventory from a stream of additions and subtractions (sales, returns, damages, shipments received). Each input event must be applied **exactly one time** to the aggregate — applying twice gives wrong stock, skipping gives wrong stock. This is the canonical non-idempotent aggregation that motivates effectively-once (source: chapter-07-stateful-streaming.md).

## Path 1: Client-broker transactions

When the broker supports transactions (Kafka does; Pulsar is on its way), effectively-once is built from three writes wrapped in one atomic transaction (source: chapter-07-stateful-streaming.md):

- **The consumer offset update** — how far the input has been processed.
- **The changelog update** — the state mutation for this event.
- **The output events** — any downstream events this event caused.

All three live in event-broker topics. A transaction either commits all of them or none. Consumers of the output streams skip events in uncommitted transactions (they block until commit), so downstream never observes a partial result.

### Failure cases

- **Transient producer failure.** The producer retries the transaction; commits are idempotent.
- **Fatal producer failure.** A replacement instance rebuilds state from the changelog, resets input offsets to the last committed value, and begins new transactions. Any in-flight transactions the previous instance had are aborted and cleaned up by the broker.

This is the gold standard. Bellemare's note: "Transactions are extremely powerful and give Apache Kafka a significant advantage over its competitors. In particular, they can accommodate new business requirements that would otherwise require a complex refactoring to ensure atomic production" (source: chapter-07-stateful-streaming.md).

## Path 2: Effectively-once without broker transactions

When the broker does not support transactions, the service needs to build effectively-once itself. Two ingredients (source: chapter-07-stateful-streaming.md):

### Idempotent writes from upstream (preferred)

If upstream producers support idempotent writes (as Kafka and Pulsar do independently of full transactions), duplicates due to producer retry are suppressed at write time and never reach the downstream consumer. **"It is better to use an event broker and client that support idempotent writes than it is to try to solve deduplication after the fact."** The first method scales to all consumer apps; the second is expensive and hard to scale (source: chapter-07-stateful-streaming.md).

### Consumer-side deduplication (fallback)

When upstream duplicates are possible, the consumer must identify and filter them. The mechanism is a **dedup ID** attached to each event, and a local store of recently-seen IDs.

#### How duplicates happen without broker transactions

Two scenarios (source: chapter-07-stateful-streaming.md):

- **Producer fails to receive ack, retries.** The republished events may carry the same event-time timestamps and same data but get new broker offsets.
- **Producer crashes after writing, before updating its own consumer offsets.** On restart, it re-consumes and re-produces; downstream sees logically-identical-but-new-offset events, possibly with new creation timestamps if processing is non-deterministic.

Idempotent production handles both of these at the broker. Faulty business logic that *generates* duplicates is not something idempotent writes can fix.

#### Generating the dedup ID

Two options (source: chapter-07-stateful-streaming.md):

- **Producer generates** (preferred) — the ID is on the event from the start and is the same across all downstream consumers.
- **Consumer derives** on consumption — usually a hash of key, value, and creation timestamp.

The ID must be built from **high-cardinality** fields so distinct events are unlikely to collide. Chapter 7's examples:

- Bank transfer: source + destination + amount + date + time.
- Ecommerce order: product list + purchaser + date + time + total + payment provider.
- Stock debit for shipment: uses the existing `orderId` (already unique).

Events without a key are "extremely challenging" to dedupe because they have no partition locality — a duplicate may be assigned to a different partition than the original. Bellemare's rule: "Produce events with a key, respect partition locality, and use idempotent writes whenever possible" (source: chapter-07-stateful-streaming.md).

#### The dedup store

A keyed state table of recent dedup IDs. Before applying an event, the consumer checks the table; if the ID is present, it drops the event. Practicalities (source: chapter-07-stateful-streaming.md):

- **Bounded by TTL, size, or offset window.** Perfect dedup requires remembering every ID forever. Real systems use a rolling window (e.g., TTL = 8000 s in the chapter's figure) and accept that very-late duplicates may slip through.
- **Scoped to a single partition.** Cross-partition dedup requires global state and is usually prohibitive.
- **Durably backed.** The dedup store is itself a state store and must be rebuilt on failure just like any other; see [[changelog-stream]].

### Atomic state + offset commit via the data service

The second ingredient: instead of committing input offsets to the broker, **commit them to the state store in the same local transaction as the state update** (source: chapter-07-stateful-streaming.md). This moves consumer offsets into the state store's ACID boundary so that state mutation and offset advancement happen together.

On failure: abort the transaction, revert to the last known good state, halt consumption, reset offsets to those stored in the data service, resume.

This gives effectively-once **processing** but not effectively-once **production** — output events still use at-least-once producer semantics, because the broker-side production is not inside the state store's transaction. If output-side effectively-once is required, use an [[outbox-table-pattern]] to commit the output intent and the state update atomically, with a separate publisher draining the outbox.

## How this lands in the wiki

- **[[exactly-once-semantics]]** — Kleppmann's framing of the same property via end-to-end operation IDs.
- **[[idempotence]]** — the underlying primitive; the producer dedup ID is an operation ID.
- **[[changelog-stream]]** — the broker-side write that gets wrapped in the transaction.
- **[[outbox-table-pattern]]** — the complement for the "state and output events must commit together" case.
- **[[stream-processing-fault-tolerance]]** — the same atomic-commit-vs-idempotence split from DDIA Chapter 11.

## Related pages

- [[exactly-once-semantics]]
- [[idempotence]]
- [[stateful-stream-processing]]
- [[changelog-stream]]
- [[state-store]]
- [[external-state-store]]
- [[outbox-table-pattern]]
- [[stream-processing-fault-tolerance]]
- [[consumer-offset]]
- [[event-broker]]
- [[keyed-event]]
