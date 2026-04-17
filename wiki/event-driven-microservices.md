# Event-Driven Microservices

**Summary**: Adam Bellemare's name for microservices that communicate asynchronously by producing and consuming durable events on shared [[event-streams|event streams]], rather than synchronously via request/response APIs. Event-driven microservices (EDM) combine small, purpose-built services with an event-log substrate that becomes the organization's [[communication-structures|data communication structure]] and single source of truth.

**Sources**: `raw/building-event-driven-microservices/chapter-01-why-event-driven-microservices.md`, `raw/building-event-driven-microservices/chapter-02-event-driven-microservice-fundamentals.md`, `raw/building-event-driven-microservices/chapter-08-building-workflows-with-microservices.md`, `raw/building-event-driven-microservices/chapter-13-integrating-event-driven-and-request-response-microservices.md`, `raw/building-event-driven-microservices/chapter-15-testing-event-driven-microservices.md`, `raw/building-event-driven-microservices/chapter-17-conclusion.md`

**Last updated**: 2026-04-17

---

## Definition

In a modern event-driven microservices architecture, systems communicate by issuing and consuming events. Unlike classic message-passing systems, these events are **not destroyed upon consumption** — they remain readily available for other consumers to read as they require (source: chapter-01-why-event-driven-microservices.md). That persistence is what distinguishes EDM from older event-based integration styles and enables the patterns the rest of Bellemare's book develops.

Services themselves are small and purpose-built — Bellemare offers the folk definition "no more than two weeks to write" and "small enough to fit in one's own head" (source: chapter-01-why-event-driven-microservices.md). They consume events from input streams, apply business logic, and may emit output events, serve request/response access, call third-party APIs, or perform other required actions. Services can be stateful or stateless, simple or complex, long-running or realized as functions (see [[functions-as-a-service]]).

Chapter 2 sharpens the producer/consumer framing: a **consumer** microservice consumes and processes events from one or more input event streams; a **producer** microservice produces events to event streams for other services to consume. Most microservices are both — a consumer of some set of input streams and a producer of some set of output streams. Communication between EDMs is **completely asynchronous**; event streams are served by a shared [[event-broker]] (source: chapter-02-event-driven-microservice-fundamentals.md).

## What makes EDM possible

Three modern-infrastructure shifts make the style practical where older message-passing architectures struggled (source: chapter-01-why-event-driven-microservices.md):

- **Durable events at scale** — events can be persisted indefinitely and re-read by any consumer as many times as necessary.
- **On-demand compute** — services are cheap to create and manage on cloud-elastic infrastructure.
- **Per-service storage** — each microservice can choose a storage technology appropriate to its own needs, at a scale that was previously limited to batch-based big-data systems.

Together these turn the humble event from a transient signal into a first-class data asset.

## The three communication structures

Bellemare's chief conceptual contribution in Chapter 1 is a three-part decomposition of how information flows through an organization — see [[communication-structures]] for the full treatment (source: chapter-01-why-event-driven-microservices.md):

- **Business communication structure** — teams and departments and how responsibilities flow between them.
- **Implementation communication structure** — the data and logic of subdomain models; where business processes are realized in code.
- **Data communication structure** — how data moves across the business, especially between implementations. Historically ad hoc, and the piece EDM formalizes.

Traditional architectures overload the implementation communication structure to play the data-communication role as well, producing the chain of pathologies Bellemare's worked team-scenario demonstrates (shared databases, point-to-point copies, stale replicas, coupled schemas). EDM replaces the ad hoc data flow with a durable event log — the data communication structure becomes a first-class, explicitly designed layer.

## Events are the basis of communication

All shareable data is published to a set of event streams, forming "a continuous, canonical narrative detailing everything that has happened in the organization" (source: chapter-01-why-event-driven-microservices.md). Key properties:

- **Events are the data.** They are not merely signals that data is ready elsewhere, nor a transport wrapping a direct handoff. Events are simultaneously *data storage* and *a means of asynchronous communication*.
- **Event streams are the single source of truth.** Each event is a statement of fact; together they form the authoritative narrative. If teams put conflicting data in other locations, the event stream's authority is diminished.
- **Consumers model and query for themselves.** The event-driven data communication structure provides no query or lookup layer. Each consumer pulls the events it needs, builds its own model, and satisfies its own query requirements. See [[event-streams]] and [[event-sourcing]] for the mechanics.

## Two topologies: microservice and business

Chapter 2 introduces a load-bearing distinction between the two scales at which the word "topology" is used (source: chapter-02-event-driven-microservice-fundamentals.md):

- **[[microservice-topology]]** — the internal processing graph of a single service: ingestion, materialization, filtering, transformation, joining, and emission.
- **[[business-topology]]** — the external graph of services, event streams, and request/response APIs that together fulfill complex business functions.

The distinction keeps the architecture tractable — you can reason about one service's internals without needing to know every other service's, and you can reason about the business-level flow without knowing any one service's internals.

## Events and state

Events in EDM are key/value records; Bellemare classifies them as [[unkeyed-event|unkeyed]], [[entity-event|entity]], or [[keyed-event|keyed]] (see [[event-structure]]). [[entity-event|Entity events]] are particularly important because the **latest event per key fully describes the entity's current state**, which underpins [[table-stream-duality|table-stream duality]] — the pattern by which any microservice can materialize its own local state store from an entity event stream (source: chapter-02-event-driven-microservice-fundamentals.md). [[tombstone|Tombstones]] express deletion; [[log-compaction]] lets broker storage stay bounded.

This is the mechanism by which services share state through events alone, without any direct coupling between producers and consumers — the concrete realization of the Chapter 1 claim that events are simultaneously data storage and communication.

## The single writer principle

Each event stream has exactly one producing microservice. That microservice is the authoritative owner of every event on the stream, which is what makes data lineage tractable and the stream usable as a single source of truth. See [[single-writer-principle]] (source: chapter-02-event-driven-microservice-fundamentals.md).

## Consequences for service design

Services are **loosely coupled on domain data**, not on a specific implementation API (source: chapter-01-why-event-driven-microservices.md). That changes the trade-offs in several well-known directions (see [[coupling]]):

- **Producers** shrink to publishing well-defined data to their event streams. They do not run cross-team APIs, replication jobs, or query services on behalf of downstream consumers.
- **Consumers** grow to handle their own modeling, joining, caching, and querying. Any required mixing across multiple event streams is the consumer's responsibility.
- **Data schemas** — not API signatures — become the primary stable contract. Chapter 3 develops the schema-evolution story; the Chapter 1 preview is that schemas give change-management properties that APIs alone cannot match.

## Primary benefits

Bellemare lists the top-level benefits EDM aims to deliver (source: chapter-01-why-event-driven-microservices.md):

- **Granularity** — services map neatly to [[bounded-context|bounded contexts]] and can be rewritten when requirements change.
- **Scalability** — individual services scale independently.
- **Technological flexibility** — each service picks appropriate languages and technologies; prototyping is easy.
- **Business-requirement flexibility** — granular services are easy to re-own; fewer cross-team dependencies mean faster response to business change.
- **Loose coupling** — coupling is on domain data via schemas, not on implementation APIs.
- **Continuous delivery** — small, modular services are easy to ship and roll back.
- **High testability** — fewer dependencies make mocking and coverage tractable.

## The team scenario, retold

Chapter 1's worked example contrasts two versions of the same organizational story. In the traditional version, a single team backed by a single datastore faces a choice for a new business requirement: (1) spin up a new service and build a stale, fragile data copy from the old store, or (2) graft the new functionality onto the existing service, eroding boundaries over time (source: chapter-01-why-event-driven-microservices.md). Most teams pick option 2. A year later, when the team must split, the tangled implementation communication structure cannot be cleanly divided, and reorganization stalls.

In the event-driven version, the team spins up a new microservice and ingests the necessary data from existing event streams — "all the way back to the beginning of time if needed." Common data can be mixed in from other streams without creating direct service-to-service coupling. When the team later splits, ownership of services and their producing event streams can be reassigned independently, and cross-team communication drops to the level dictated by the business rather than by the implementation (source: chapter-01-why-event-driven-microservices.md).

The moral: most of the pain in the traditional version was caused by a missing or weak data communication structure, not by anything intrinsic to microservices. Formalizing that structure changes the economics of service decomposition.

## The platform underneath: broker and CMS

Chapter 2 makes the infrastructure dependencies explicit. Two platform pieces are non-negotiable for production EDM:

- **[[event-broker|Event broker]].** The distributed, durable, partitioned, replayable log system that holds all event streams. Bellemare contrasts it with a traditional [[message-brokers|message broker]] — an event broker can replace a message broker, but a message broker cannot substitute for an event broker because it deletes messages after consumption and cannot give every consumer its own replayable view (source: chapter-02-event-driven-microservice-fundamentals.md).
- **[[container-management-system]].** Kubernetes, Docker Engine, Mesos Marathon, Amazon ECS, or Nomad — the system that deploys, scales, and manages the containerized services at scale.

The combined cost of standing up and operating these platforms is what Bellemare calls the **[[microservice-tax]]**. It is unavoidable; the organizational question is whether it is paid once centrally or ten times over across teams (source: chapter-02-event-driven-microservice-fundamentals.md). Small organizations usually do better with a [[modular-monolith]] than with paying the tax.

Chapter 14 catalogs the **self-serve DevOps tooling** that rides on top of these two pieces — ownership tracking, ACLs, schema notifications, offset resets, cluster bringup, topology visualization. See [[edm-supportive-tooling]] for the hub (source: chapter-14-supportive-tooling.md).

## Testability

EDMs are unusually easy to test compared to larger, more tangled services. Each microservice has narrow inputs (event streams, request-response API), narrow outputs (its own output streams, its own state store), and a small surface area of business logic between them (source: chapter-15-testing-event-driven-microservices.md). Chapter 15 stacks up four layers of testing that map directly onto this structure: [[unit-testing-topology-functions|unit-testing topology functions]], [[topology-testing]] of the whole business logic as a single function, [[local-integration-testing]] of the microservice against a dev-controlled broker + registry + store, and [[remote-integration-testing]] for load, performance, and recovery tests at production scale. [[test-data-strategies|Test data]] is a separate axis with its own trade-offs, and [[hosted-service-mocks]] fills the gap when a production dependency is a proprietary cloud service with no emulator.

## Composing services into workflows

Individual microservices operate on only a small portion of an organization's business processes. Most meaningful business operations are *workflows* — sets of actions, branches, and compensations that span several microservices, each within its own [[bounded-context]]. Bellemare's Chapter 8 names two canonical patterns for composing services into workflows (source: chapter-08-building-workflows-with-microservices.md):

- **Choreography** — no central coordinator; services react to input events and emit output events; the workflow is emergent from the services' relationships.
- **Orchestration** — a central orchestrator microservice holds the workflow logic and issues commands to subordinate workers; workers respond; the orchestrator advances state.

When a workflow must succeed or fail atomically across multiple services, it becomes a [[saga|distributed transaction / saga]] — implementable in either style, but always with the same warning: avoid distributed transactions when possible. When strict rollback is inappropriate, a [[compensation-workflow]] completes what it can and remediates the rest by business policy.

See [[workflows-in-edm]] for the full treatment, including the direct-call vs event-driven orchestration comparison and the tip that an orchestrator's bounded context must stay strictly limited to workflow logic (the "God service" anti-pattern).

## Synchronous vs asynchronous

EDM is not a universal replacement for [[synchronous-microservices|synchronous microservices]]. Bellemare argues EDM offers "unparalleled flexibility" for most cross-domain data flows, but concedes that certain patterns — authentication, A/B-test reporting, user-facing web/mobile responses, third-party HTTP integrations — fit request/response naturally. **Hybrid architectures are the norm**: synchronous and asynchronous solutions deployed side-by-side where each is best suited (source: chapter-01-why-event-driven-microservices.md). See [[synchronous-microservices]] for the drawbacks Chapter 1 cites as motivation for the event-driven default.

Chapter 13 goes deeper on the integration seams between EDM and request-response: [[external-events-ingestion|ingesting external events]] (autonomous analytical events), [[third-party-api-integration|calling third-party APIs]], [[serving-state-from-edm|serving materialized state over REST]] (with the [[smart-load-balancer]] optimization), [[request-as-event|turning requests into events]] with an [[asynchronous-ui]], and [[micro-frontends]] as the frontend counterpart. See the hub at [[event-driven-request-response-integration]].

## Closing framings (Chapter 17)

Bellemare's conclusion distills the book into a few reusable one-liners (source: chapter-17-conclusion.md):

- **A mature data communication layer decouples the ownership and production of data from the access and consumption of it.** Applications stop doing double duty — serving internal business logic *and* feeding other services' queries — and focus only on their own bounded context.
- **Failure-mode decoupling.** A failed producer no longer means its data is inaccessible; it only means new data is delayed. Consumers continue reading from the broker during producer outages. The broker's durability becomes the service's durability, including for services that store changelogs of their own internal state (see [[changelog-stream]], [[hot-replicas]]).
- **Composition over integration.** Once important domain events are in the broker, a new service is built by *subscribing to the streams it needs* rather than opening direct connections to each system that owns the data. This is the concrete payoff of [[data-liberation]].
- **Not all microservices need be "micro".** An organization mid-journey may run several larger services and still get most of the EDM benefit — see [[service-granularity]] for the three principles Bellemare offers for evolving large services: (1) put important business entities/events into the event broker, (2) use the broker as the single source of truth, (3) avoid direct calls between services.
- **Avoid technical alignment.** Microservices should align with business [[bounded-context|bounded contexts]], not technical boundaries. A "technical" microservice (e.g., "the notification service for three unrelated workflows") couples itself to every workflow that uses it and collapses their failure modes together. See [[technical-vs-domain-partitioning]].
- **Final word.** "The data communication layer extends the power of an organization's data to any service or team that requires it, eliminates access boundaries, and reduces unnecessary complexity related to the production and distribution of important business information" (source: chapter-17-conclusion.md).

## Relationship to existing wiki coverage

EDM is the microservice-architecture-level expression of concepts covered elsewhere in the wiki:

- **[[event-driven-architecture]]** (Richards & Ford) — EDM is a specific, microservices-shaped realization of the event-driven architecture style, typically in the [[broker-topology]] with pub/sub event streams.
- **[[stream-processing]] / [[event-streams]] / [[log-based-message-brokers]]** (Kleppmann) — the data-substrate mechanics EDM depends on.
- **[[event-sourcing]] / [[change-data-capture]]** — two complementary ways to ensure that state transitions show up on the event streams.
- **[[microservices]]** (Newman, Richards & Ford) — EDM inherits the three defining properties (independent deployability, business-domain alignment, owning your own data) and adds the "communicate via durable events" constraint on top.
- **[[saga]]** — the orchestrated/choreographed distinction maps onto EDM's synchronous/asynchronous mix.

## Related pages

- [[building-event-driven-microservices]] — source-book overview and ingestion status
- [[communication-structures]]
- [[synchronous-microservices]]
- [[event-driven-architecture]]
- [[broker-topology]]
- [[mediator-topology]]
- [[event-streams]]
- [[event-sourcing]]
- [[change-data-capture]]
- [[log-based-message-brokers]]
- [[stream-processing]]
- [[microservices]]
- [[monolith]]
- [[bounded-context]]
- [[domain-driven-design]]
- [[coupling]]
- [[cohesion]]
- [[conways-law]]
- [[independent-deployability]]
- [[saga]]
- [[microservice-topology]]
- [[business-topology]]
- [[event-structure]]
- [[entity-event]]
- [[keyed-event]]
- [[unkeyed-event]]
- [[table-stream-duality]]
- [[tombstone]]
- [[log-compaction]]
- [[event-broker]]
- [[single-writer-principle]]
- [[consumer-offset]]
- [[consumer-group]]
- [[container-management-system]]
- [[microservice-tax]]
- [[workflows-in-edm]]
- [[compensation-workflow]]
- [[basic-producer-consumer-microservice]]
- [[gating-pattern]]
- [[hybrid-bpc-stream-processing]]
- [[heavyweight-framework-microservice]]
- [[lightweight-framework-microservice]]
- [[edm-supportive-tooling]]
- [[unit-testing-topology-functions]]
- [[topology-testing]]
- [[local-integration-testing]]
- [[remote-integration-testing]]
- [[test-data-strategies]]
- [[hosted-service-mocks]]
