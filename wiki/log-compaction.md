# Log Compaction

**Summary**: A background broker operation that **retains only the most recent event per key** in a compactable event stream, discarding older values and [[tombstone|tombstoned]] keys entirely. Log compaction lets append-only streams of [[entity-event|entity events]] double as durable storage for current state without growing without bound — the mechanism that makes [[table-stream-duality]] cheap in practice.

**Sources**: `raw/building-event-driven-microservices/chapter-02-event-driven-microservice-fundamentals.md`, `raw/designing-data-intensive-applications/chapter-11-stream-processing.md`

**Last updated**: 2026-04-17

---

## What compaction does

An event broker periodically rewrites a topic's log segments, keeping only the **latest event for each key** and deleting older events of the same key (source: chapter-02-event-driven-microservice-fundamentals.md). [[tombstone|Tombstones]] are retained long enough for consumers to process the deletion, then they and their predecessors of the same key are deleted as well.

Important properties (source: chapter-02-event-driven-microservice-fundamentals.md):

- **Event stream offsets are maintained** — consumers' recorded positions remain valid across compaction; no client changes are required.
- **Disk usage shrinks.** The compacted topic is just a snapshot of the latest value per key, encoded as events.
- **Replay cost shrinks.** A new consumer bootstrapping from offset zero processes fewer events to reach current state.
- **History is lost.** Intermediate values for each key are irretrievably gone. That is the trade.

## When compaction is appropriate

Compaction is designed for streams whose **latest event per key fully determines the current state** (source: chapter-02-event-driven-microservice-fundamentals.md) (source: chapter-11-stream-processing.md). That is true of:

- **[[entity-event|Entity events]]** — each event carries the full current state of the entity.
- **[[change-data-capture|CDC]] streams** — the most recent row value is what matters.

Compaction is **not** appropriate for (source: chapter-11-stream-processing.md):

- **[[event-sourcing|Event-sourced]] streams** — earlier events ("item added", "item removed") each carry unique information; only replaying the full history yields correct state.
- **[[keyed-event|Keyed events]] that are not entities** — aggregation relies on seeing multiple events per key.
- **[[unkeyed-event|Unkeyed events]]** — compaction is keyed, so there is nothing to compact.

## Bootstrapping new consumers

A major operational benefit of compaction: a new consumer can start from **offset 0 of a compacted topic** and obtain a full current-state image of the source data, without requiring a separate snapshot or bootstrapping mechanism (source: chapter-11-stream-processing.md). This is the trick that lets Kafka serve as durable primary storage for entity state, not just as transient messaging.

## Trade-off summary

Compaction reduces disk usage and the number of events that must be processed to reach the current state, at the expense of eliminating the history of events otherwise provided by the event stream (source: chapter-02-event-driven-microservice-fundamentals.md). If you need history, either disable compaction on that topic or pair a compacted topic with a separate, uncompacted audit topic.

## Relationship to the wiki's existing coverage

- **[[log-based-message-brokers]]** — already covers Kafka-level compaction mechanics. This page is the concept-level page that ties compaction to entity/keyed/unkeyed events.
- **[[hash-indexes]] / [[sstables-and-lsm-trees]]** — the same compaction idea appears at the storage-engine layer.
- **[[tombstone]]** — the mechanism compaction uses to represent and eventually erase deletions.
- **[[table-stream-duality]]** — the pattern log compaction makes affordable.

## Related pages

- [[log-based-message-brokers]]
- [[entity-event]]
- [[tombstone]]
- [[table-stream-duality]]
- [[change-data-capture]]
- [[event-sourcing]]
- [[event-streams]]
- [[hash-indexes]]
- [[sstables-and-lsm-trees]]
