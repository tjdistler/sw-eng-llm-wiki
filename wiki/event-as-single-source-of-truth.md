# Event as Single Source of Truth

**Summary**: Bellemare's guideline that an event must carry the complete description of what happened, not a signal that something happened elsewhere. An event is the full and final record, not a pointer to it. This is the concrete rule behind two of his Chapter 3 design guidelines: "tell the whole truth" and "avoid events as semaphores or signals."

**Sources**: `raw/building-event-driven-microservices/chapter-03-communication-and-data-contracts.md`, `raw/building-event-driven-microservices/chapter-01-why-event-driven-microservices.md`, `raw/building-event-driven-microservices/chapter-04-integrating-event-driven-architectures-with-existing-systems.md`

**Last updated**: 2026-04-17

---

## The whole-truth principle

> "A good event definition is not simply a message indicating that something happened, but rather the complete description of everything that happened during that event." (source: chapter-03-communication-and-data-contracts.md)

The event is the single source of truth for the occurrence it describes. Consumers must not have to look anywhere else — no companion database query, no callback to the producer, no lookup in a side channel — to understand what happened.

This is the contract-level statement of the Chapter 1 claim that [[event-streams|events are the data]], not a transport wrapping a handoff (source: chapter-01-why-event-driven-microservices.md).

## The semaphore anti-pattern

The failure mode is an event that says "work completed" without including the result of the work (source: chapter-03-communication-and-data-contracts.md). The consumer now has two problems:

1. It has to locate where the result actually lives (a database? a file? another service?).
2. It has to handle the race/consistency question of whether the result is visible yet when the event arrives.

Two sources of truth now exist for the same piece of data, and every consumer is responsible for reconciling them. This is exactly the implementation-communication-structure pathology that [[event-driven-microservices|EDM]] is supposed to eliminate.

## Why this matters structurally

A well-formed event means consumers can be [[coupling|loosely coupled on domain data]] instead of on the producer's implementation. The moment an event becomes a semaphore, the consumer must know *where the producer stores its results* — tightly coupling the consumer to the producer's storage layout, language, deployment, and release cadence. The architecture regresses toward a shared-database model with extra steps.

## The acceptable exception

Bellemare allows one narrow case for data *outside* the event: genuinely large payloads (e.g., large images, reports) that cannot fit in a broker message (source: chapter-03-communication-and-data-contracts.md). A pointer to the artifact is acceptable in that scenario, but:

- use it sparingly,
- accept that the ledger's immutability guarantee no longer extends to the payload, and
- treat payload mutability as a risk to design around rather than a free feature.

This is a tactical exception to the rule, not a general license.

## The legacy-integration compromise: publish-first vs unidirectional liberation

Chapter 4 extends the principle into the messy territory of integrating existing systems. Two postures (source: chapter-04-integrating-event-driven-architectures-with-existing-systems.md):

- **Publish-first (ideal).** A service publishes state changes to the event broker **before** materializing them back to its own local store. The event is genuinely the single source of truth — even the producing service reads its own state from the stream. This is Bellemare's recommended pattern for new and refactored services.
- **Unidirectional liberation (compromise).** A legacy system continues to keep its internal state as the authoritative store; [[data-liberation|liberation]] mechanisms export changes to the event stream; the legacy system never reads back. The stream becomes the single source of truth **for downstream consumers** while the legacy system remains its own internal source of truth, kept in sync through strictly controlled publishing.

The compromise is pragmatic — refactoring complex legacy systems to a publish-first posture is often prohibitively expensive. The correctness guarantee is weaker (eventual consistency between the internal store and the stream) but still preserves the property that downstream consumers see a single canonical source for the data (source: chapter-04-integrating-event-driven-architectures-with-existing-systems.md).

See [[data-liberation]] for the full compromise analysis and the three patterns ([[query-based-cdc]], [[change-data-capture|log-based]], [[outbox-table-pattern]]) used to keep the stream in sync with the internal store.

## Relationship to other guidelines

The whole-truth principle is paired with [[single-purpose-events]] and [[singular-event-definition-per-stream]] in the [[event-design-guidelines]] set. Together they describe what a well-formed event looks like: a single business occurrence, on its own stream, carrying its full result as data.

## Related pages

- [[event-design-guidelines]]
- [[data-contract]]
- [[event-streams]]
- [[event-driven-microservices]]
- [[single-purpose-events]]
- [[singular-event-definition-per-stream]]
- [[coupling]]
- [[event-structure]]
- [[data-liberation]]
- [[outbox-table-pattern]]
- [[change-data-capture]]
