# Tombstone

**Summary**: A **keyed event with a null value** that signals to consumers that the entity with that key has been **deleted**. Tombstones are the deletion mechanism in append-only event logs — you cannot delete a prior record, but you can add a null-valued record that tells downstream consumers to remove the key from their materialized state.

**Sources**: `raw/building-event-driven-microservices/chapter-02-event-driven-microservice-fundamentals.md`, `raw/designing-data-intensive-applications/chapter-11-stream-processing.md`

**Last updated**: 2026-04-17

---

## What a tombstone is

In an immutable, append-only event log, you cannot modify or delete prior records. To express deletion, the producer writes a **tombstone**: a keyed event whose value is null (source: chapter-02-event-driven-microservice-fundamentals.md).

By convention, a consumer that reads a tombstone interprets it as an instruction to **remove the entity with that key from its materialized data store** (source: chapter-02-event-driven-microservice-fundamentals.md). This is how [[table-stream-duality|table-stream duality]] handles deletion without violating the immutability of the log.

## Role in log compaction

Tombstones interact with [[log-compaction]] in a specific way. When a topic is compacted, all earlier events with the same key are discarded — only the latest event per key is retained. If the latest event is a tombstone, eventually the tombstone itself is also deleted, completing the removal (source: chapter-02-event-driven-microservice-fundamentals.md) (source: chapter-11-stream-processing.md).

Bellemare's Figure 2-5 shows the final state after compaction: all tombstones *and their predecessors of the same key* are gone, leaving only live entities (source: chapter-02-event-driven-microservice-fundamentals.md).

## Consumer obligations

Downstream consumers must be coded to **recognize** null values as tombstones rather than as missing or malformed data. Schema systems like [[avro]] accommodate this by permitting union-with-null value types; the application logic then branches on null and deletes the corresponding record from local state.

## Relationship to CDC and event sourcing

- **[[change-data-capture]]** — CDC streams use tombstones to represent row deletes at the database source. Log compaction can reduce the stream to the current-state image of the table.
- **[[event-sourcing]]** — event-sourced logs typically do *not* use tombstones in this sense; deletion is expressed as a domain event ("OrderCancelled") that another consumer interprets. Compaction does not safely apply to event-sourced streams because the full history is needed.

## Related pages

- [[table-stream-duality]]
- [[log-compaction]]
- [[entity-event]]
- [[log-based-message-brokers]]
- [[change-data-capture]]
- [[event-sourcing]]
- [[event-streams]]
- [[avro]]
