# Stateless Stream Processing

**Summary**: A [[microservice-topology]] is **stateless** when each event is processed independently of any others — no accumulated state is required across events. Stateless topologies are the simplest case of event-driven processing: consume, transform, emit.

**Sources**: `raw/building-event-driven-microservices/chapter-05-event-driven-processing-basics.md`

**Last updated**: 2026-04-17

---

## The basic processing loop

Every [[event-driven-microservices|event-driven microservice]] sourced from streams follows three steps (source: chapter-05-event-driven-processing-basics.md):

1. Consume an event from an input [[event-streams|event stream]].
2. Process the event.
3. Produce any necessary output events.

In pseudocode, the instance registers a producer and a consumer client, joins its [[consumer-group]], and loops polling for events. Between `produceEventToStream` and `commitOffsets` lies the at-least-once guarantee — offsets are committed only after output is written (source: chapter-05-event-driven-processing-basics.md).

The `processEvent` function is the entry point to the [[microservice-topology|microservice's processing topology]]: a sequence of data-driven operations (filters, routers, transformations, joins, emissions) composed to express the bounded context's business logic (source: chapter-05-event-driven-processing-basics.md).

## Stateless vs stateful

In a stateless topology, events are processed independently. No accumulated state, no materialized tables, no [[stream-joins|stream-table joins]]. The topology is a pure per-event pipeline of [[event-transformations|transformations]], [[stream-branching-and-merging|branches, and merges]]. Stateful processing, by contrast, maintains local state (usually materialized via [[table-stream-duality]]) and is covered in depth on [[stateful-stream-processing]] (source: chapter-05-event-driven-processing-basics.md).

## Thinking in topologies

Building a microservice topology requires thinking in an event-driven way: the code executes in response to an event arriving at the consumer input. Those familiar with functional programming or map-reduce-style frameworks will recognize the style. A simple topology might apply a filter in stage 1 and a map in stage 2 — some events traverse the entire pipeline, while others are dropped partway (source: chapter-05-event-driven-processing-basics.md).

## Recovering from stateless instance failures

Recovering from a failed stateless instance is effectively the same as adding a new instance to the [[consumer-group]]. Because there is no state to restore, the replacement instance can immediately resume processing as soon as partitions are assigned and it establishes its stream time (source: chapter-05-event-driven-processing-basics.md). This is what makes stateless topologies cheap to scale and easy to recover.

## Repartitioning from a stateless processor

A purely stateless processor rarely needs to [[repartitioning|repartition]] its output, barring an increase in partition count for downstream parallelism. That said, a stateless microservice is a natural place to repartition events destined for a downstream **stateful** processor (source: chapter-05-event-driven-processing-basics.md).

## Related pages

- [[microservice-topology]]
- [[event-driven-microservices]]
- [[event-transformations]]
- [[stream-branching-and-merging]]
- [[repartitioning]]
- [[copartitioning]]
- [[partition-assignor]]
- [[consumer-group]]
- [[stream-processing]]
- [[table-stream-duality]]
- [[stateful-stream-processing]]
