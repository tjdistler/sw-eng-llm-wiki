# Event Transformations

**Summary**: A transformation is a per-event operation inside a [[microservice-topology]] that consumes one event and emits zero or more output events. Transformations are the building blocks of [[stateless-stream-processing|stateless topologies]] and carry most of a service's business logic.

**Sources**: `raw/building-event-driven-microservices/chapter-05-event-driven-processing-basics.md`

**Last updated**: 2026-04-17

---

## Definition

A transform processes a single event and emits zero or more output events. Transforms provide the bulk of the business-logic operations performed by an [[event-driven-microservices|event-driven microservice]] (source: chapter-05-event-driven-processing-basics.md).

Some transformations change the event key. When that happens, the output stream may need to be [[repartitioning|repartitioned]] to preserve data locality for any downstream stateful processor (source: chapter-05-event-driven-processing-basics.md).

## Common transformations

Bellemare's baseline catalogue (source: chapter-05-event-driven-processing-basics.md):

- **Filter** — propagate the event if it meets a criterion; drop it otherwise. Emits zero or one event. Conceptually related to the [[filter-pattern]] at the container level.
- **Map** — change the key and/or value of the event. Emits exactly one event. Because the key may change, downstream consumers may need the stream to be repartitioned.
- **MapValue** — change only the value, not the key. Emits exactly one event. Repartitioning is **not** required — events stay in the same partition they arrived on.
- **Custom transforms** — apply arbitrary logic, look up state, or even communicate synchronously with other systems. These are the escape hatch for business logic that does not fit the pure functional catalogue.

## Relationship to the Unix/batch lineage

The transformation catalogue mirrors well-known patterns from functional programming and [[mapreduce|MapReduce]]-style batch engines — [[unix-philosophy|Unix pipelines]], [[pipeline-architecture|pipes-and-filters]], and [[dataflow-engines]] all compose similar per-item operators. Stream processing reuses the vocabulary on unbounded data (source: chapter-05-event-driven-processing-basics.md).

## Related pages

- [[stateless-stream-processing]]
- [[microservice-topology]]
- [[stream-branching-and-merging]]
- [[repartitioning]]
- [[stream-processing]]
- [[filter-pattern]]
- [[pipeline-architecture]]
- [[mapreduce]]
