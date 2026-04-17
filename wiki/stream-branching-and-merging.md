# Stream Branching and Merging

**Summary**: Branching routes events from one input stream to multiple output streams based on a predicate; merging combines events from multiple input streams into one. Both are compositional primitives for [[stateless-stream-processing|stateless]] [[microservice-topology|microservice topologies]].

**Sources**: `raw/building-event-driven-microservices/chapter-05-event-driven-processing-basics.md`

**Last updated**: 2026-04-17

---

## Branching

A consumer application may need to apply a logical operator to each event and emit it to a new stream based on the result. Two common scenarios (source: chapter-05-event-driven-processing-basics.md):

- **Firehose routing** — consuming a single high-volume stream and splitting it by a property of the event: country, time zone, origin, product, or any other feature.
- **Dead-letter routing** — emitting successful results to one output stream and failures to a dead-letter stream, rather than dropping failed events outright.

Branching is the streaming analogue of the container-level [[splitter-pattern]] (route by criterion) and, when the criterion is a filter predicate, of the [[filter-pattern]].

## Merging

Merging consumes events from multiple input streams, optionally processes them, and emits to a single output stream. In practice merges are less common than branches — microservices typically consume from as many input streams as their business logic requires, without needing to unify them into one (source: chapter-05-event-driven-processing-basics.md).

When merges are used, a deliberate unified schema for the merged stream is mandatory. Bellemare's warning: *if a unified schema for the merged domain does not make sense, leave the streams unmerged and reconsider the system design* (source: chapter-05-event-driven-processing-basics.md). A merge that cannot justify its own [[data-contract]] is a design smell.

## Relationship to ordering

Merging multiple input streams raises the question of *which event to process first* when events arrive on different streams. Ordering, late events, and out-of-order events are the subject of Chapter 6 of *Building Event-Driven Microservices* (source: chapter-05-event-driven-processing-basics.md).

## Related pages

- [[stateless-stream-processing]]
- [[event-transformations]]
- [[microservice-topology]]
- [[event-streams]]
- [[splitter-pattern]]
- [[filter-pattern]]
- [[merger-pattern]]
- [[data-contract]]
