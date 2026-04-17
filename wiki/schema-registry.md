# Schema Registry

**Summary**: A shared service that stores event schemas by ID/version and serves them on demand to producers and consumers, so the schema does not have to be embedded in every message. Schema registries are how event-broker-based systems like Kafka and Pulsar support strongly-typed formats (Avro, Protobuf, JSON Schema) at scale, and how organizations enforce pre-deployment compatibility checks on schema changes.

**Sources**: `raw/building-event-driven-microservices/chapter-03-communication-and-data-contracts.md`, `raw/building-event-driven-microservices/chapter-14-supportive-tooling.md`, `raw/designing-data-intensive-applications/chapter-04-encoding-and-evolution.md`

**Last updated**: 2026-04-17

---

## The problem it solves

Formats like [[avro|Avro]] encode data against a schema but store no schema information inside the record itself. The reader needs the *writer's schema* to decode the bytes correctly. Two options exist (source: chapter-04-encoding-and-evolution.md):

1. **Embed the schema alongside each message.** Simple but prohibitively expensive at scale — the schema is often larger than the message.
2. **Store schemas centrally and reference them by ID.** Much cheaper per message, but requires a shared service.

A schema registry is option 2.

## How it fits into event-broker ecosystems

Bellemare's Chapter 3 positions the schema registry as a shared piece of infrastructure alongside the [[event-broker|event broker]] (source: chapter-03-communication-and-data-contracts.md). Both [[log-based-message-brokers|Apache Kafka]] and Apache Pulsar ship with (or integrate with) schema-registry support for JSON, Protobuf, and Avro.

The typical flow:

1. Producer registers its schema with the registry and receives a schema ID.
2. Producer writes events to the broker, prefixing each with the schema ID (a few bytes) rather than the full schema.
3. Consumer reads the event, extracts the schema ID, looks up the schema in the registry (usually with local caching), and decodes.

This keeps wire-format overhead low while preserving all the benefits of explicit, typed [[data-contract|data contracts]].

## Compatibility enforcement

The second load-bearing function of a schema registry is **pre-deployment compatibility checking**. Before a producer is allowed to register a new version of its schema, the registry evaluates the new schema against the existing ones under the configured compatibility rule (forward, backward, or full — see [[schema-evolution]]). If the change would break the rule, registration is rejected (source: chapter-04-encoding-and-evolution.md).

This turns a question that used to be "we'll find out in production" into a question that is answered before the producer ships. It is the enforcement point that makes [[backward-forward-compatibility|rolling upgrades]] of producers and consumers actually safe.

## Use within code generation

A schema registry complements [[code-generation]]: generated classes embed references to specific schema versions, and a consumer that reads an event encoded with a newer version can still decode it if the registry confirms the two versions are compatible. The registry turns "schemas" from a per-project artifact into a first-class organizational asset.

## Change notifications

Because schema evolutions can have a large but poorly-visible blast radius across consuming services, Chapter 14 recommends a **notification tool** that watches the schema stream, cross-references consumer [[event-stream-acls|ACLs]], and alerts the owning teams of all downstream consumers when a schema they depend on changes (source: chapter-14-supportive-tooling.md). See [[schema-change-notifications]].

## Related pages

- [[data-contract]]
- [[schema-evolution]]
- [[backward-forward-compatibility]]
- [[avro]]
- [[encoding-formats]]
- [[code-generation]]
- [[event-broker]]
- [[log-based-message-brokers]]
- [[explicit-vs-implicit-schemas]]
- [[schema-change-notifications]]
