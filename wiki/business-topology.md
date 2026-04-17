# Business Topology

**Summary**: Adam Bellemare's term for the **graph-like relationship between microservices, event streams, and request-response APIs** that together fulfill complex business functions. The business-level companion to the finer-grained [[microservice-topology]].

**Sources**: `raw/building-event-driven-microservices/chapter-02-event-driven-microservice-fundamentals.md`, `raw/building-event-driven-microservices/chapter-14-supportive-tooling.md`

**Last updated**: 2026-04-17

---

## Definition

A business topology is an **arbitrary grouping of services, event streams, and APIs** that together fulfill complex business functionality (source: chapter-02-event-driven-microservice-fundamentals.md). Its scope is a matter of convenience — it may represent the services owned by a single team or department, or a superset of functionality spanning many teams.

The business [[communication-structures|communication structure]] from Chapter 1 composes the business topology: microservices implement business [[bounded-context|bounded contexts]], and [[event-streams]] provide the data communication mechanism for sharing cross-context domain data (source: chapter-02-event-driven-microservice-fundamentals.md).

## The black-box view

Unlike a [[microservice-topology]], the business topology does **not** describe the internal workings of any one microservice. Each service is a black box that consumes some streams and produces others (source: chapter-02-event-driven-microservice-fundamentals.md).

Bellemare's canonical illustration: three microservices and three streams.

- **Microservice 1** consumes and transforms data from event stream A, producing to event stream B.
- **Microservice 2** consumes from stream B and serves a synchronous REST API — it is strictly a consumer from the event-driven side.
- **Microservice 3** also consumes from stream B, performs bounded-context-specific transformations, and produces to event stream C.

New microservices and streams can be added as needed; services remain **asynchronously coupled through event streams** rather than through direct calls (source: chapter-02-event-driven-microservice-fundamentals.md).

## The topology as a concrete tool

Chapter 14 turns the business topology from a concept into an actual running piece of software: a visualizer that derives the graph from [[event-stream-acls|ACLs]], overlays team boundaries from [[microservice-to-team-assignment]], and supports queries like *"which team has the most cross-boundary dependencies?"* and *"where did this event come from?"* The worked 25-service / 4-team example in Chapter 14 uses the visualization to propose reassignments that net-reduce cross-team connections (source: chapter-14-supportive-tooling.md). See [[dependency-tracking-and-topology-visualization]] and [[data-lineage]].

## Why the distinction matters

Keeping the business topology separate from the microservice topology is what makes [[independent-deployability]] and team autonomy possible. You can reason about the business-level flow without every team needing to know every other team's internal logic; you can change any one service's internal topology without changing the business topology, provided the schemas on its output streams are preserved.

## Relationship to existing wiki coverage

- **[[broker-topology]] and [[mediator-topology]]** — Richards & Ford use "topology" to describe the two shapes a whole [[event-driven-architecture]] can take. Bellemare's business topology is the same idea: the inter-service shape of the system.
- **[[communication-structures]]** — the three structures (business / implementation / data) motivate why the business topology should be built on event streams rather than direct calls.
- **[[microservice-topology]]** — the zoomed-in companion view.

## Related pages

- [[event-driven-microservices]]
- [[microservice-topology]]
- [[event-streams]]
- [[broker-topology]]
- [[mediator-topology]]
- [[communication-structures]]
- [[bounded-context]]
- [[synchronous-microservices]]
- [[dependency-tracking-and-topology-visualization]]
- [[data-lineage]]
