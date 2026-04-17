# Explicit vs Implicit Schemas

**Summary**: Every producer/consumer pair has a schema — the question is whether it is written down. Bellemare argues that an **explicit** schema (a typed definition the producer publishes alongside events) is a prerequisite for event-driven microservices at organizational scale; the **implicit** alternative, where consumers infer structure from sample data, collapses under the weight of independent teams.

**Sources**: `raw/building-event-driven-microservices/chapter-03-communication-and-data-contracts.md`

**Last updated**: 2026-04-17

---

## The claim

> "Any implementation of event-based communication between a producer and consumer that lacks an explicit predefined schema will inevitably end up relying on an implicit schema." (source: chapter-03-communication-and-data-contracts.md)

There is no "no schema" option. The only question is whether the schema is written down and enforced, or reverse-engineered by each consumer from the events they happen to see.

## Why implicit schemas fail

Implicit schemas break in three characteristic ways (source: chapter-03-communication-and-data-contracts.md):

1. **Brittleness under change.** A producer may "accidentally" alter the event format — rename a field, change a type, tighten a range — with no tool detecting it. Their unit tests pass. Downstream consumers fail at runtime.
2. **Tribal knowledge doesn't scale.** Resolving interpretation ambiguity requires interteam communication and back-channel emails. As the organization grows, the communication cost grows super-linearly. Cross-team coordination becomes the bottleneck.
3. **Divergent interpretation.** Each consumer independently decides what the fields mean. Two consumers looking at the same event reach different conclusions, and the "single source of truth" stops being a single anything.

## Why the "common interpretation library" is not the answer

A tempting shortcut is to share a library that every consumer imports, which owns the parsing and interpretation logic. Bellemare explicitly warns against it (source: chapter-03-communication-and-data-contracts.md):

- **Language fragmentation** — services are written in different languages; one library cannot serve them all.
- **Evolution conflicts** — the library has its own release cycle that must be coordinated with every consumer, which is exactly the coupling EDM is trying to remove.
- **Duplicated effort** — keeping the library consistent across services is non-trivial and never complete.

Implicit-schema + shared-library is not a lighter-weight alternative to explicit schemas; it is the same problem re-labeled, with worse tooling.

## What an explicit schema provides

An explicit schema gives both sides of the [[data-contract]] something to build against (source: chapter-03-communication-and-data-contracts.md):

- **Producers** are guarded by the compiler or serializer against mis-populating or forgetting required fields.
- **Consumers** can build business logic confidently against typed structures rather than untyped maps.
- **Change** becomes visible: a diff of the schema makes structural change a review-able artifact.
- **Documentation** is colocated: schema comments (triggering logic, field semantics, datetime formats) live alongside the definition — see [[event-structure]].

## Requirement, not nicety

For Bellemare, explicit schemas are not a "nice to have" polish layer — they are the mechanism by which [[event-driven-microservices|EDM]] remains scalable beyond a handful of services. Without them, the implicit coupling between producer and consumer reappears at a level no tool can see, and the architecture regresses toward the shared-database pathologies it was meant to replace.

This is also why Bellemare recommends strongly-typed formats like Avro or Protobuf over JSON — see [[encoding-formats]] — and why [[schema-registry|schema registries]] exist as shared infrastructure.

## Related pages

- [[data-contract]]
- [[schema-evolution]]
- [[schema-registry]]
- [[code-generation]]
- [[event-structure]]
- [[encoding-formats]]
- [[avro]]
- [[event-driven-microservices]]
- [[breaking-changes]]
- [[coupling]]
