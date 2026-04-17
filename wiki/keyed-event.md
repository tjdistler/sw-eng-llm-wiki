# Keyed Event

**Summary**: The third of Bellemare's three event types — a keyed event that **does not describe an entity**. Keyed events exist primarily to guarantee data locality and per-key ordering within a single [[partitioning|partition]]; downstream processing may later aggregate them into an [[entity-event]].

**Sources**: `raw/building-event-driven-microservices/chapter-02-event-driven-microservice-fundamentals.md`

**Last updated**: 2026-04-17

---

## Shape

A keyed event carries a key that is used for routing but whose value is not a full entity snapshot. Bellemare's example is a stream of book-interaction events keyed on ISBN (source: chapter-02-event-driven-microservice-fundamentals.md):

```
Key: ISBN 372719   Value: { UserId: A537FE }
Key: ISBN 372719   Value: { UserId: BB0012 }
```

The key is present so that events for the same book land on the same partition, which guarantees a single consumer sees them in order. Each event is still only a fact about one interaction, not a complete description of the book entity.

## Why the distinction from entity events matters

Because keyed events do not carry the full state of an entity, two consequences follow (source: chapter-02-event-driven-microservice-fundamentals.md):

- **[[log-compaction|Log compaction]] is not appropriate.** Compacting a keyed-event stream would discard earlier events of the same key, destroying the information the stream exists to carry.
- **Materialization requires aggregation.** To build a per-entity state from keyed events, a consumer must aggregate — for example, collect the list of users who interacted with each ISBN, then emit a single [[entity-event]] keyed on ISBN with the aggregated list as its value.

That keyed-to-entity aggregation pattern is common in stream-processing pipelines and is one of the main reasons keyed events exist as a distinct type.

## Partitioning as the primary motivation

The point of keying a non-entity event is to **exploit [[partitioning]] for data locality and ordering**. Bellemare is explicit that keyed events are "usually used for partitioning the stream of events to guarantee data locality within a single partition" (source: chapter-02-event-driven-microservice-fundamentals.md). Once events for the same key live on the same partition, a single consumer instance can process them in order without any cross-partition coordination.

## Relationship to other event types

- An [[entity-event]] is also keyed but carries full current state; its primary role is [[table-stream-duality|materialization]], not just locality.
- An [[unkeyed-event]] has no key at all and spreads across all partitions.

## Related pages

- [[event-structure]]
- [[entity-event]]
- [[unkeyed-event]]
- [[partitioning]]
- [[partitioning-strategies]]
- [[log-compaction]]
- [[event-streams]]
- [[event-driven-microservices]]
