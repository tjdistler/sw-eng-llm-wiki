# Event Sinking

**Summary**: The reverse direction of [[data-liberation]]: consuming events from an event stream and inserting them into a data store so that a non-event-driven application can read them through its ordinary query path. Sinking lets legacy applications participate in the event-driven ecosystem without being refactored to consume events natively.

**Sources**: `raw/building-event-driven-microservices/chapter-04-integrating-event-driven-architectures-with-existing-systems.md`

**Last updated**: 2026-04-17

---

## Mechanics

A sink process reads events from a topic on the [[event-broker]], tracks its own [[consumer-offset|consumption offset]], and writes event payloads into a target data store as they arrive. The sink is entirely independent of the destination application — the legacy application keeps issuing its normal queries against its database, unaware that the data is now maintained by an event-driven pipeline (source: chapter-04-integrating-event-driven-architectures-with-existing-systems.md).

Any event type can be sunk: [[entity-event|entity events]], [[keyed-event|keyed events]], or [[unkeyed-event|unkeyed events]].

## Why sink

Two canonical uses (source: chapter-04-integrating-event-driven-architectures-with-existing-systems.md):

- **Replacing point-to-point legacy couplings.** Once the producer's data is liberated into an event stream, the consumer's dependency can be severed by standing up a sink that writes the liberated data into the consumer's existing database. The consumer stops querying the producer directly; it reads from a locally sunk copy.
- **Batch analytics handoff.** Sinking event data into HDFS (or a cloud data lake, warehouse, or lakehouse) bridges live event streams to the batch-based big-data tools that analytics teams already use.

## Implementation options

Two choices, mirroring the producer-side choice in [[data-liberation]] (source: chapter-04-integrating-event-driven-architectures-with-existing-systems.md):

- **Centralized framework.** Kafka Connect's sink connectors are the canonical example — one framework team runs shared infrastructure, and other teams contribute simple configs. Low-cost on-ramp, shared with the source-side framework; see [[data-liberation-framework]] for the trade-offs.
- **Standalone microservice.** A purpose-built sink service, deployed and managed like any other microservice. More up-front effort but no cross-team framework dependency.

## When sinking is the wrong answer

Sinking is a **bootstrap**, not a destination. The same warning that applies to CDC producers applies symmetrically to sinks: if teams become content to let a sink ferry events into a legacy store that is then queried as before, the architecture has not actually moved toward event-driven. The legacy application remains ignorant of events, and the event broker becomes a glorified data-copying pipe (source: chapter-04-integrating-event-driven-architectures-with-existing-systems.md).

For actively developed consumers, the event-first posture is to refactor the consumer to read events directly, materialize its own state, and drop the sink. For maintenance-only legacy systems, a sink is a reasonable permanent compromise.

## Related pages

- [[data-liberation]]
- [[event-broker]]
- [[event-streams]]
- [[consumer-offset]]
- [[data-liberation-framework]]
- [[event-driven-microservices]]
- [[data-integration]]
- [[derived-data]]
