# Entity Event

**Summary**: The second of Bellemare's three event types — an event keyed on the **unique ID of an entity** (a thing in the business context) whose value carries the entity's properties and state at a point in time. Entity events are the foundation of [[table-stream-duality|materializing state]] in event-driven microservices: the latest entity event per key determines the current state.

**Sources**: `raw/building-event-driven-microservices/chapter-02-event-driven-microservice-fundamentals.md`

**Last updated**: 2026-04-17

---

## Shape

An entity event is keyed on the entity's unique identifier; its value contains all properties needed to describe the entity (source: chapter-02-event-driven-microservice-fundamentals.md):

```
Key: ISBN 372719
Value: { Author: "Adam Bellemare", Title: "...", ... }
```

Bellemare's example is a book entity keyed on ISBN — whenever the book's state changes, a new entity event is emitted with the full new value.

## Why entity events matter

Entity events are "particularly important in event-driven architectures" because they serve two distinct roles at once (source: chapter-02-event-driven-microservice-fundamentals.md):

- **Historical record.** The stream of entity events for a given key is a continual history of the entity's state over time.
- **Current-state generator.** **Only the latest entity event is needed** to determine the current state of that entity — which makes them compatible with [[log-compaction]] and with the [[table-stream-duality]] pattern that lets any consumer materialize a local table from the stream.

## Materializing state

By applying entity events in order from the stream and **upserting** each one into a key/value table, a consumer ends up with a current-state representation of all entities (source: chapter-02-event-driven-microservice-fundamentals.md). Deletion is signalled with a [[tombstone]] — a keyed event whose value is null — instructing consumers to remove the key from their materialized store.

This is the mechanism by which microservices share state through events alone, without any direct coupling between producer and consumer services.

## Comparison with CDC and event sourcing

An entity event carrying the full current state is the same shape as what [[change-data-capture|CDC]] produces when extracting row-level changes from a database — the Chapter 11 framing in DDIA explicitly contrasts this with [[event-sourcing]], where events encode **intent** rather than **state** (source: raw/designing-data-intensive-applications/chapter-11-stream-processing.md). Entity events are therefore structurally closer to CDC-style records than to event-sourcing records, which matters because log compaction works for entity events (the latest one wins) but does not for event-sourced events (the history is needed).

## Relationship to other event types

- An [[unkeyed-event]] has no key at all — useful for standalone facts that need no aggregation.
- A [[keyed-event]] has a key but does not describe an entity — useful for partitioning or aggregation but not for direct materialization.

## Related pages

- [[event-structure]]
- [[unkeyed-event]]
- [[keyed-event]]
- [[table-stream-duality]]
- [[tombstone]]
- [[log-compaction]]
- [[change-data-capture]]
- [[event-sourcing]]
- [[event-streams]]
- [[event-driven-microservices]]
