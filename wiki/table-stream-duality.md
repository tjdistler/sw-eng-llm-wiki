# Table-Stream Duality

**Summary**: The foundational pattern for state in event-driven microservices: a stateful key/value **table** can be materialized by upserting [[entity-event|entity events]] from a keyed stream, and conversely every update to a table can be emitted as an event on a stream. Bellemare treats this duality as "fundamental to the creation of state in an event-driven microservice" and the mechanism by which services share state through events alone.

**Sources**: `raw/building-event-driven-microservices/chapter-02-event-driven-microservice-fundamentals.md`

**Last updated**: 2026-04-17

---

## The two directions

Two operations, each the inverse of the other (source: chapter-02-event-driven-microservice-fundamentals.md):

- **Stream → Table.** Apply entity events from a stream in order. Upsert each event into a key/value table — insert if the key is new, update if it already exists. After consuming the full stream, the table contains the most recent value per key.
- **Table → Stream.** Publish every insert/update/delete on a table as an event to an event stream. Replaying the stream reconstructs the table exactly.

Bellemare's canonical example: a relational database table is created and populated through a series of insert/update/delete commands. If those commands are produced as events to an append-only log — a local binary log (e.g. MySQL's binlog) or an external event stream — the table can be **exactly reconstructed** by replaying the log (source: chapter-02-event-driven-microservice-fundamentals.md). This is the same mechanism underlying [[change-data-capture]].

## Why it matters for EDM

Every consumer client can independently read a stream of [[entity-event|entity events]] and materialize it into its own local state store. Bellemare calls this "a simple yet powerful pattern [that] allows microservices to share state through events alone, without any direct coupling between producer and consumer services" (source: chapter-02-event-driven-microservice-fundamentals.md).

Consequences (source: chapter-02-event-driven-microservice-fundamentals.md):

- **No shared database.** Two services can each hold up-to-date state without talking to each other and without reading each other's databases.
- **Independent schemas.** Each consumer models the state however it wants — different indexes, different derived fields, different storage engines.
- **Replay is a first-class capability.** Any consumer can rebuild its materialized view from scratch by rewinding to offset zero.

## Deletion via tombstones

Because the log is append-only, deletion of an entity is expressed by producing a **[[tombstone]]** — a keyed event with its value set to null. By convention, consumers interpret a tombstone as an instruction to **remove the key from the materialized table** (source: chapter-02-event-driven-microservice-fundamentals.md).

## Log compaction keeps the duality cheap

Raw streams of entity events grow without bound. [[log-compaction|Log compaction]] retains only the latest event per key, shrinking disk usage and reducing the work a new consumer does to rebuild state (source: chapter-02-event-driven-microservice-fundamentals.md). Tombstones and their predecessors for the same key are eventually deleted during compaction, so compacted streams converge to "just the current state, expressed as events".

Compaction only preserves the current-state view — the history of intermediate values is lost. That is appropriate for entity events but not for [[event-sourcing]]-style intent events, where earlier records carry unique information that the latest does not.

## Relationship to the wiki's existing coverage

The duality idea is not new to Bellemare — Pat Helland's "The truth is the log; the database is a cache of a subset of the log" (quoted in [[event-sourcing]]) and Kleppmann's discussion of derived data all express the same underlying pattern. What Chapter 2 does is stake out this pattern as the **load-bearing mechanism for inter-microservice state sharing** in an event-driven architecture. See:

- **[[change-data-capture]]** — the Stream → Table direction applied at the database level: one database's log becomes many systems' state.
- **[[event-sourcing]]** — an adjacent pattern that stores *intent* events rather than state-carrying events; log compaction does not apply.
- **[[log-based-message-brokers]]** — Kafka-style compaction is the substrate that makes the duality cheap.
- **[[derived-data]]** — the general "write path vs read path" framing.

## Related pages

- [[entity-event]]
- [[tombstone]]
- [[log-compaction]]
- [[log-based-message-brokers]]
- [[change-data-capture]]
- [[event-sourcing]]
- [[event-streams]]
- [[derived-data]]
- [[state-machine-replication]]
- [[event-driven-microservices]]
- [[stateful-stream-processing]]
- [[materialized-state]]
- [[state-store]]
- [[changelog-stream]]
