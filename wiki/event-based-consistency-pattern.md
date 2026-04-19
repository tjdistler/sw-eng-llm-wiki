# Event-Based Consistency Pattern

**Summary**: An [[eventual-consistency]] pattern where participants in a distributed transaction communicate via **pub/sub events on a message broker or event stream**. The primary service commits and publishes; other services subscribe and update their own data in parallel. *Software Architecture: The Hard Parts* Chapter 9 calls this "one of the most popular and reliable eventual consistency patterns for most modern distributed architectures" (source: raw/software-architecture-the-hard-parts/chapter-09-data-ownership-and-distributed-transactions.md).

**Sources**: `raw/software-architecture-the-hard-parts/chapter-09-data-ownership-and-distributed-transactions.md`

**Last updated**: 2026-04-19

---

## The shape

A primary service handles the end-user request, commits its own local transaction, **publishes an event** (or command message), and returns to the user. Downstream services subscribe to the event and perform their own local transactions asynchronously.

Chapter 9's worked example: the Customer Profile Service receives an unsubscribe request at 11:23:00, deletes the Profile row, publishes an `unsubscribed` event to a topic, and responds to the user one second later. Meanwhile, the Support Contract and Billing Payment Services receive the event and perform their own updates in parallel (source: raw/software-architecture-the-hard-parts/chapter-09-data-ownership-and-distributed-transactions.md).

## Why it works

- **Responsiveness.** The user-visible transaction is just the primary commit + event publish. Everything else happens in parallel, in the background.
- **Service decoupling.** The primary service doesn't know which services respond to the event. Consumers can be added without touching the producer.
- **Short time-to-consistency.** Unlike the [[background-synchronization-pattern]]'s nightly batch, events fire in near-real-time. The consistency window is typically milliseconds to seconds.

## Reliable delivery: durable subscribers and persistence

The pattern's reliability hinges on the messaging infrastructure. Chapter 9 emphasises two requirements (source: raw/software-architecture-the-hard-parts/chapter-09-data-ownership-and-distributed-transactions.md):

1. **Durable subscribers** (traditional pub/sub brokers like ActiveMQ, RabbitMQ, AmazonMQ) — subscribers are guaranteed to receive messages even if they were offline when the event was published.
2. **Event log persistence** (event-streaming brokers like Apache Kafka) — events are persisted in the topic for some retention period; subscribers can consume at their own pace and replay if needed.

Without one of these, a subscriber outage means lost updates and permanent inconsistency.

## Error handling: the dead letter queue

The same decoupling that makes the pattern responsive makes error handling tricky. Three cases (source: raw/software-architecture-the-hard-parts/chapter-09-data-ownership-and-distributed-transactions.md):

1. **Subscriber service down.** Durable subscription / event log holds the message. The subscriber catches up when it returns.
2. **Subscriber processing fails transiently.** The broker typically retries some number of times.
3. **Subscriber processing fails persistently.** After retry exhaustion, the message is moved to a **dead letter queue (DLQ)**.

The DLQ is a configurable destination where failed events accumulate. An automated process reads from it and tries to repair the problem (apply idempotent retry logic, patch the data, etc.). If programmatic repair isn't possible, the message is escalated for manual handling.

The DLQ mechanism is the reason this pattern works in practice: failures don't corrupt state silently; they get quarantined in a named place where they can be observed and dealt with.

## Trade-off summary

| | For | Against |
|---|---|---|
| **Event-based consistency** | Fast response to user; timely data consistency; good service decoupling; consumers added without touching producer | Error handling via DLQ + manual intervention; requires durable pub/sub or event log; broker becomes critical infrastructure; consistency window is short but not zero |

## Where it sits in the architecture

This pattern is the **natural consistency model** of [[event-driven-architecture|event-driven architectures]] using the [[broker-topology]] — precisely because the topology is built around pub/sub and the consistency pattern is just "use the topology for its intended purpose."

It also corresponds closely to **choreographed sagas** (see [[saga]]). In fact, a [[compensating-update|compensation step]] in a choreographed saga *is* an event-based consistency update, fired in reverse when something downstream fails.

## Relation to other patterns

- **[[background-synchronization-pattern]]** — similar in that both are async, but background sync has one external process writing every table, while the event-based pattern keeps each service as the writer of its own data. Bounded contexts stay intact.
- **[[orchestrated-request-based-pattern]]** — opposite trade-off: orchestrated buys stronger consistency at response time by paying the latency and complexity cost.

Chapter 9's recommendation: **prefer the event-based pattern** unless the business genuinely requires the caller to see end-to-end consistency before the response returns.

## Related pages

- [[eventual-consistency]]
- [[background-synchronization-pattern]]
- [[orchestrated-request-based-pattern]]
- [[base-properties]]
- [[event-driven-architecture]]
- [[broker-topology]]
- [[message-brokers]]
- [[event-streams]]
- [[saga]]
- [[compensating-update]]
- [[outbox-table-pattern]] — how producers atomically publish events + local commits
- [[software-architecture-the-hard-parts]]
