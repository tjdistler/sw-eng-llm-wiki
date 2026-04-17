# Data Contract

**Summary**: Adam Bellemare's term for the agreement between an event producer and its consumers about the shape *and* meaning of the events on a stream. A data contract has two components — the **data definition** (fields, types, structures) and the **triggering logic** (the business condition that causes an event to be produced). Both must be preserved across evolution, with special care not to break consumers.

**Sources**: `raw/building-event-driven-microservices/chapter-03-communication-and-data-contracts.md`

**Last updated**: 2026-04-17

---

## The two components

A well-defined data contract has two parts (source: chapter-03-communication-and-data-contracts.md):

1. **Data definition** — *what* will be produced: the fields, types, and structures of the event.
2. **Triggering logic** — *why* it is produced: the specific business logic that caused the event's creation.

Both are followed by producer and consumer alike. The contract is what gives the event meaning and form beyond the context in which it is produced — it extends the usability of the data to downstream consumers that have no other way to ask the producer "what did you mean by this?".

## The ratio of change

Changes happen to both components as business requirements evolve, but **data-definition changes are far more common than triggering-logic changes** (source: chapter-03-communication-and-data-contracts.md). Altering the trigger often changes what the event *means*, which silently breaks consumer logic even when the schema still validates. The data contract therefore deserves the same change-management discipline for the triggering logic as for the schema itself.

This is the EDM-shaped analogue of Newman's [[breaking-changes|structural vs semantic]] split: a schema diff will catch data-definition breakage; only communication and testing catch triggering-logic breakage.

## The contract is explicit or implicit

Any producer/consumer pair that omits an [[explicit-vs-implicit-schemas|explicit schema]] still has a data contract — it is just implicit. Implicit contracts are brittle, rely on tribal knowledge, and scale poorly once more than a few teams are involved (source: chapter-03-communication-and-data-contracts.md). Bellemare's whole chapter treats the explicit, schematized data contract as the foundation that makes EDM viable at organizational scale.

## Why this matters for EDM

In [[event-driven-microservices|event-driven microservices]], the data contract is the *primary* contract between services. There is no REST API signature, no shared library, no cross-team meeting where ambiguity can be cleared up on demand. The events on the stream are all the consumer gets. If the contract is wrong or unclear, each consumer re-invents an interpretation — and they will disagree. Bellemare calls this the inconsistent-views-of-the-single-source-of-truth problem (source: chapter-03-communication-and-data-contracts.md).

This is also why Bellemare warns against the "common interpretation library" shortcut: trying to encapsulate the data contract in a shared library creates problems with multiple language formats, event evolutions, and independent release cycles, and does not remove the underlying interpretation risk (source: chapter-03-communication-and-data-contracts.md).

## How the contract is enforced

Three mechanisms compose into a usable contract enforcement story:

- **[[explicit-vs-implicit-schemas|Explicit schemas]]** — the producer commits to a typed definition; the consumer builds against it.
- **[[schema-evolution]]** — the rules under which the schema can change without breaking consumers.
- **[[schema-registry]]** — a shared store of schemas with pre-deployment compatibility checking.
- **[[code-generation]]** — turning the schema into typed classes so the producer cannot ship code that violates the contract.

Together they are what [[independent-deployability|independent deployability]] looks like when the interface is data rather than a function call.

## Related pages

- [[explicit-vs-implicit-schemas]]
- [[schema-evolution]]
- [[schema-registry]]
- [[code-generation]]
- [[event-design-guidelines]]
- [[breaking-changes]]
- [[consumer-driven-contracts]]
- [[event-structure]]
- [[event-driven-microservices]]
- [[coupling]]
