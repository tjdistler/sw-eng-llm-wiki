# Singular Event Definition per Stream

**Summary**: Bellemare's guideline that an event stream should carry events of exactly one logical type. Mixing multiple event types in a single stream muddles the stream's identity, makes schema validation harder, and couples unrelated concerns through a shared subscription.

**Sources**: `raw/building-event-driven-microservices/chapter-03-communication-and-data-contracts.md`

**Last updated**: 2026-04-17

---

## The rule

An event stream should contain events representing a **single logical event** (source: chapter-03-communication-and-data-contracts.md). The vast majority of event streams in an EDM architecture should each have a strict, single definition. Bellemare allows that special circumstances can justify exceptions, but they should be rare and deliberate.

## Why

Three properties collapse when multiple event types share a stream (source: chapter-03-communication-and-data-contracts.md):

- **Stream identity.** A stream's name and meaning become ambiguous. "What's on `user-events`?" should have a one-sentence answer; it doesn't when the stream is a union.
- **Validation.** A [[schema-registry]] can only enforce compatibility per schema. New schemas can appear dynamically in a shared stream, and the registry's job becomes ambiguous.
- **Consumer filtering.** Every consumer must filter for the subset of events it cares about, even if that subset is a single type — wasted compute and a bug surface.

## Relationship to single-purpose events

This guideline pairs with [[single-purpose-events]]. One is about the *definition* of an event (no overloaded `type` field); the other is about the *placement* of events (one type per stream). They compose: the refactor of one overloaded schema into three single-purpose schemas should produce three streams, not three types coexisting on one stream.

## Relationship to breaking-change accommodation

The rule also governs how Bellemare recommends handling [[breaking-changes|breaking schema changes for events]] (source: chapter-03-communication-and-data-contracts.md): create a **new stream** for the new event definition rather than introducing the incompatible schema into the existing stream. Old consumers keep reading the old stream until its retention period elapses, then unregister. New consumers register against the new stream. The two event types never mix.

> "Don't mix different event types in an event stream, especially event types that are evolutionarily incompatible. Event stream overhead is cheap, and the logical separation is important in ensuring that consumers have full information and explicit definitions when dealing with the events they need to process." (source: chapter-03-communication-and-data-contracts.md)

## The cheap-stream economic argument

Bellemare is explicit that event-stream overhead on a modern [[event-broker]] is cheap. The historical instinct to conserve streams (or topics, or queues) comes from older message-broker systems where each was expensive. Under Kafka/Pulsar-class infrastructure, more streams is almost always the right call when in doubt.

## Related pages

- [[event-design-guidelines]]
- [[single-purpose-events]]
- [[data-contract]]
- [[breaking-changes]]
- [[schema-evolution]]
- [[event-broker]]
- [[event-structure]]
- [[event-streams]]
