# Microservice Topology

**Summary**: Adam Bellemare's term for the **event-driven topology internal to a single microservice** — the data-driven operations it performs on incoming events, including transformation, materialization, storage, and emission. Contrasts with [[business-topology]], which describes the graph-like relationships *between* microservices.

**Sources**: `raw/building-event-driven-microservices/chapter-02-event-driven-microservice-fundamentals.md`, `raw/building-event-driven-microservices/chapter-05-event-driven-processing-basics.md`

**Last updated**: 2026-04-17

---

## Definition

A microservice topology describes the inner workings of a single [[event-driven-microservices|event-driven microservice]] — what it does with the events it consumes and emits (source: chapter-02-event-driven-microservice-fundamentals.md). It is the unit-of-processing view.

Typical operations inside a microservice topology (source: chapter-02-event-driven-microservice-fundamentals.md):

- **Ingest** events from one or more input [[event-streams]].
- **Materialize** entity-keyed streams into local state stores (see [[table-stream-duality]]).
- **Filter** events by predicate.
- **Transform** events via business logic.
- **Join** streams against stored state or against each other.
- **Emit** results to one or more output event streams.

Bellemare's canonical illustration: a microservice ingests event stream A and materializes it into a data store; it ingests event stream B, filters out uninteresting events, transforms the rest, joins them against the stored state, and emits results to a new output stream (source: chapter-02-event-driven-microservice-fundamentals.md).

## Stateless vs stateful

A microservice topology may be [[stateless-stream-processing|stateless]] or **stateful**. Stateful topologies maintain local state — typically materialized from an entity event stream — and use it to answer queries, enrich events, or drive business logic. Maintaining state is "an extremely common pattern in an event-driven architecture" because past business decisions influence current ones (source: chapter-02-event-driven-microservice-fundamentals.md). Retail stock levels, accounts payable, and customer email lists are all examples of state that must be materialized from the event log.

Chapter 5 elaborates the stateless case as the basic building block: consume, transform, emit, with each event processed independently (source: chapter-05-event-driven-processing-basics.md). The per-event operators — [[event-transformations|filter, map, mapValue, custom]] — together with [[stream-branching-and-merging|branching and merging]] compose the skeleton of any topology, stateless or otherwise. Stateful behavior is layered on top by [[repartitioning]], [[copartitioning]], and materialization (Chapter 7).

## Relationship to business topology

A microservice topology zooms *in* to the logic of one service. The [[business-topology]] zooms *out* to the relationships between many services, streams, and APIs. Both views coexist; the business topology treats each microservice as a black box whose internal topology is not visible (source: chapter-02-event-driven-microservice-fundamentals.md).

## Relationship to existing wiki coverage

- **[[stream-processing]]** — the wider family of dataflow-style processing topologies. A microservice topology is the microservice-sized realization.
- **[[table-stream-duality]]** — the mechanism by which an entity event stream becomes queryable local state inside the topology.
- **[[event-driven-architecture]] / [[broker-topology]]** — Richards & Ford's overloaded use of "topology" refers to the inter-service shape; Bellemare's microservice topology is the intra-service shape.

## Related pages

- [[event-driven-microservices]]
- [[business-topology]]
- [[event-streams]]
- [[table-stream-duality]]
- [[stream-processing]]
- [[stateless-stream-processing]]
- [[event-transformations]]
- [[stream-branching-and-merging]]
- [[repartitioning]]
- [[copartitioning]]
- [[event-driven-architecture]]
- [[bounded-context]]
