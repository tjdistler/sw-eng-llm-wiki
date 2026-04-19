# Data Contract

**Summary**: Adam Bellemare's term for the agreement between an event producer and its consumers about the shape *and* meaning of the events on a stream. A data contract has two components — the **data definition** (fields, types, structures) and the **triggering logic** (the business condition that causes an event to be produced). Both must be preserved across evolution, with special care not to break consumers.

**Sources**: `raw/building-event-driven-microservices/chapter-03-communication-and-data-contracts.md`, `raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md`, `raw/software-architecture-the-hard-parts/chapter-13-contracts.md`

**Last updated**: 2026-04-19

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

## The FoDE source-system framing

Reis and Housley's Chapter 5 of *Fundamentals of Data Engineering* reaches for the same concept but from the opposite end of the pipeline — not producer/consumer event-stream communication, but the **source-system extraction** contract between a data team and the upstream system that owns the data. They quote James Denmore's formulation (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md):

> A data contract is a written agreement between the owner of a source system and the team ingesting data from that system for use in a data pipeline. The contract should state what data is being extracted, via what method (full, incremental), how often, as well as who (person, team) are the contacts for both the source system and the ingestion.

The Reis-and-Housley recommendations on how to operate it:

- **Store contracts in a well-known location** — a GitHub repo or internal documentation site, so consumers can find them without asking.
- **Use a standardized format where possible** so contracts can be integrated into the development process or queried programmatically.
- **Pair with an [[service-level-agreement|SLA]] and [[service-level-objective|SLO]]** — a data contract states the shape of the data; the SLA/SLO states the availability and quality expectations against it.

If a formal contract feels too heavy, Reis and Housley fall back to an informal requirement: verbally set expectations for source-system uptime, data quality, and anything else of importance (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md).

This source-system-extraction contract and Bellemare's producer-consumer event contract are not the same artefact, but they serve the same purpose — **make the interface between teams explicit so changes don't silently break downstream work**. In a mature [[data-liberation|data-liberated]] organisation, the two collapse: the source team publishes events per the same contract the data team consumes, and the extraction-side contract becomes redundant.

## The broader Hard Parts definition

Ford, Richards, Sadalage, and Dehghani in Chapter 13 of *Software Architecture: The Hard Parts* deliberately *widen* the word "contract" beyond the Bellemare-style producer/consumer event contract and beyond the Reis/Housley source-system extraction agreement. Their definition (source: raw/software-architecture-the-hard-parts/chapter-13-contracts.md):

> The format used by parts of an architecture to convey information or dependencies.

Under this definition, a data contract between a producer and a consumer is one instance of a general category that also includes REST/gRPC endpoints, method signatures across modules, transitive library dependencies, cached values, hardcoded URLs, and any other coupling point. The specific decisions an architect makes about a data contract — strictness, versioning strategy, validation layer — are instances of the strict-to-loose design choice covered in [[contracts]], [[strict-contract]], and [[loose-contract]].

The convergence point across all three framings: **the contract is the primary lever for managing coupling between independently-deployed parts**, and its shape determines whether the interface tightens or loosens over time.

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
- [[source-systems]]
- [[source-system-considerations]]
- [[service-level-agreement]]
- [[service-level-objective]]
- [[contracts]]
- [[strict-contract]]
- [[loose-contract]]
- [[stamp-coupling]]
- [[software-architecture-the-hard-parts]]
