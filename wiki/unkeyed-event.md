# Unkeyed Event

**Summary**: The first of Bellemare's three event types — an event used to describe a **singular statement of fact** with no associated key. Typical for interaction events like "a user opened this book".

**Sources**: `raw/building-event-driven-microservices/chapter-02-event-driven-microservice-fundamentals.md`

**Last updated**: 2026-04-17

---

## Shape

An unkeyed event has no key; the value is the full record of what happened (source: chapter-02-event-driven-microservice-fundamentals.md).

```
Key: N/A
Value: { ISBN: 372719, Timestamp: 1538913600 }
```

Bellemare's example is a digital book platform emitting an event when a user opens a book: the event stands alone as a fact, with no need to aggregate it against any other event of the same key.

## When to use

Unkeyed events are appropriate when:

- The event is a **standalone fact** and does not describe the state of a unique thing.
- No **per-key ordering or locality** is required — producers and consumers do not need events for "the same thing" to land in the same [[partitioning|partition]].
- Downstream consumers will likely aggregate or batch-process the events rather than materialize them into per-entity state.

Because unkeyed events have no key, they are distributed across partitions using round-robin or random strategies, which maximizes write throughput at the cost of any per-entity ordering.

## Relationship to other event types

If an event describes the *current state* of a unique thing, use an [[entity-event]] instead. If multiple events should be guaranteed to land on the same partition for ordering but do not together represent an entity, use a [[keyed-event]].

## Related pages

- [[event-structure]]
- [[entity-event]]
- [[keyed-event]]
- [[event-streams]]
- [[partitioning]]
- [[event-driven-microservices]]
