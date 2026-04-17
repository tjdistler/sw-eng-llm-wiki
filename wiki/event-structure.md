# Event Structure

**Summary**: Adam Bellemare's breakdown of how events are represented — a **key/value** record where the value stores the full details of what happened and the key (when present) is used for identification, routing, and aggregation. Bellemare distinguishes three event types: [[unkeyed-event|unkeyed]], [[entity-event|entity]], and [[keyed-event|keyed]].

**Sources**: `raw/building-event-driven-microservices/chapter-02-event-driven-microservice-fundamentals.md`, `raw/building-event-driven-microservices/chapter-03-communication-and-data-contracts.md`

**Last updated**: 2026-04-17

---

## Events as key/value records

Events in an [[event-driven-microservices|event-driven microservice]] architecture are typically represented using a **key/value format** (source: chapter-02-event-driven-microservice-fundamentals.md):

- The **value** stores the complete details of the event.
- The **key** is used for identification, routing, and aggregation operations on events with the same key.
- The key is **not required** for all event types.

The key field is structurally important because it drives [[partitioning]] — events with the same key land on the same partition, which is the lever that provides per-entity ordering guarantees and data locality in [[log-based-message-brokers|log-based brokers]] like Kafka.

## What an event contains

An event is a **recording of what happened**, similar to an application log entry but elevated to the status of single source of truth (source: chapter-02-event-driven-microservice-fundamentals.md). Because other services will reconstruct their own state from events alone, an event **must contain all the information required to accurately describe what happened** — callers cannot go back to the producer and ask for more context.

Anything important to the business can be an event: receiving an invoice, booking a meeting room, requesting a cup of coffee, hiring a new employee, or successfully completing arbitrary code (source: chapter-02-event-driven-microservice-fundamentals.md).

## The three event types

Bellemare names three event types that recur throughout the book and in real-world domains (source: chapter-02-event-driven-microservice-fundamentals.md):

| Type | Has key? | Purpose |
|---|---|---|
| [[unkeyed-event]] | No | A singular statement of fact (e.g. user viewed product) |
| [[entity-event]] | Yes — ID of the entity | Describes the state of a unique thing at a point in time |
| [[keyed-event]] | Yes — not an entity ID | Partitioning for locality/ordering; may aggregate into an entity |

The distinctions matter because only [[entity-event|entity events]] support [[table-stream-duality|materialization into a current-state table]], which is the mechanism most event-driven stateful logic depends on.

## Schemas

Because events are simultaneously storage and communication, producers and consumers must share a **common understanding** of their contents. Bellemare positions event schemas as **analogous to an API definition** between synchronous services and argues for schematization tools (Apache Avro, Google Protobuf) that provide two key benefits (source: chapter-02-event-driven-microservice-fundamentals.md):

1. An **evolution framework** — safe schema changes that do not require downstream code changes.
2. **Typed class generation** — turning schema-defined events into plain objects in the consumer's language of choice.

See [[schema-evolution]], [[backward-forward-compatibility]], [[avro]], and [[encoding-formats]] for the wiki's detailed treatment of these mechanisms.

## Schema-definition comments

Bellemare's Chapter 3 treats integrated comments and arbitrary metadata as an essential, first-class part of the event definition — not a nicety (source: chapter-03-communication-and-data-contracts.md). The knowledge surrounding the production and consumption of an event should live as close as possible to the event's schema, because that is the one artifact every consumer has access to. Two places matter in particular:

- **A block header at the top of the schema** specifying the **triggering logic** — *why* an event is generated. This is half of the [[data-contract]] and would otherwise become tribal knowledge.
- **Per-field comments** giving context on ambiguous types. Bellemare's canonical example: a `datetime` field's comments should say whether it is UTC, ISO-8601, or Unix seconds.

Comments reduce the chance of misinterpretation by consumers and are cheap to produce at the time the schema is authored.

## Narrowest data types

The [[event-design-guidelines|design guideline]] that pairs directly with the key/value shape: use the narrowest type that fits the field, so that code generators, language type checkers, and serialization unit tests do the boundary-checking for you (source: chapter-03-communication-and-data-contracts.md). Bellemare's anti-examples:

- **String-for-number** — parsing errors, null/empty ambiguity. Common with GPS coordinates.
- **Integer-for-boolean** — what does `2` mean? What does `-1` mean? There is no way to answer.
- **String-for-enum** — producers must remember to match an accepted pseudo-enum list that is not enforced anywhere. Typos are inevitable. Consumers who care about the field must discover the range of values out of band. This is an implicit schema hiding inside an explicit one.

On enums specifically: both Avro and Protobuf have elegant ways of handling unknown enum tokens, and should be used when either is selected for the event format. The consumer's responsibility is to decide whether an unrecognized token should be handled with a default or should halt processing — not to pretend it cannot happen.

## Related pages

- [[unkeyed-event]]
- [[entity-event]]
- [[keyed-event]]
- [[table-stream-duality]]
- [[event-streams]]
- [[partitioning]]
- [[schema-evolution]]
- [[avro]]
- [[backward-forward-compatibility]]
- [[encoding-formats]]
- [[event-driven-microservices]]
- [[data-contract]]
- [[event-design-guidelines]]
- [[explicit-vs-implicit-schemas]]
