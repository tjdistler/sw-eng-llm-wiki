# Dead-Letter Queue

**Summary**: A separate queue or topic where the ingestion or consumer layer routes events it cannot successfully process — bad schemas, oversize messages, events sent to nonexistent topics, events that have expired past their [[data-retention|TTL]]. Without a DLQ, problematic events block the queue and prevent everything behind them from being ingested; with one, errors are segregated, visible, and available for later diagnosis and selective reprocessing.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-07-ingestion.md`

**Last updated**: 2026-04-18

---

## Why a DLQ exists

Reis and Housley's framing: "Sometimes events aren't successfully ingested. Perhaps an event is sent to a nonexistent topic or message queue, the message size may be too large, or the event has expired past its TTL. Events that cannot be ingested need to be rerouted and stored in a separate location called a dead-letter queue. A dead-letter queue segregates problematic events from events that can be accepted by the consumer" (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md).

The critical operational reason: **if events are not rerouted to a dead-letter queue, these erroneous events risk blocking other messages from being ingested** (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md). A poison message in an ordered log stops all forward progress for that partition until the consumer either acknowledges or moves past it. The DLQ is how you move past without losing the record.

## Typical failure modes it catches

Ch 7 names four categories of event that end up in a DLQ:

- **Routing errors.** The event was published to a nonexistent topic or queue.
- **Size violations.** The event exceeds the broker's maximum message size (see [[message-brokers]] limits — Kinesis defaults to 1 MB, Kafka to about 1 MB with 20 MB configurable).
- **TTL expiry.** The event sat in the queue past its configured retention and was never acknowledged.
- **Schema / deserialization failure** (implied). An event that the consumer cannot decode — usually due to a broken [[schema-evolution|schema evolution]] or a missing schema in the [[schema-registry]] — is also a DLQ candidate. Ch 7 lists DLQ as a recommended tool **specifically for investigating issues with events that are not properly handled** due to schema change (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md).

## What engineers do with the DLQ

Two uses (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md):

- **Diagnosis.** Engineers use the DLQ contents to figure out why event ingestion errors are happening and what pipeline problem needs fixing.
- **Reprocessing.** Once the underlying cause is fixed, some messages in the DLQ can be replayed — either by publishing them back to the main topic or by running them through the consumer directly.

The DLQ is therefore both an **error log** and a **replay staging area**, not a black hole.

## DLQ as part of the schema-evolution playbook

Ch 7 calls out the DLQ as one of three defenses against schema-evolution damage (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md):

1. Use a [[schema-registry]] to version schema changes.
2. Use a DLQ to investigate events that are not properly handled.
3. Communicate with upstream stakeholders about schema changes proactively.

The first prevents; the second contains; the third is the low-fidelity but "most effective" human control.

## Relation to error handling in stream consumers

A DLQ is the standard consumer-side response to unprocessable events in a stream. Without it, the consumer has only two bad options: block on the bad event, or silently drop it. The DLQ gives it a third: park the bad event somewhere inspectable, advance the offset, and keep going.

This is also the usual pattern for event-driven microservices: a consumer that cannot process an event routes it to a DLQ topic rather than blocking its [[consumer-offset|consumer offset]]. The failed-event topic can then be operated independently — monitored, alerted on, drained.

## Related pages

- [[data-ingestion]]
- [[message-brokers]]
- [[event-streams]]
- [[schema-evolution]]
- [[schema-registry]]
- [[late-arriving-events]]
- [[reprocessing-event-streams]]
- [[consumer-offset]]
- [[exactly-once-semantics]]
- [[idempotence]]
