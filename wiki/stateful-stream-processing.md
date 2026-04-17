# Stateful Stream Processing

**Summary**: A [[microservice-topology]] is **stateful** when processing one event depends on information accumulated from prior events — a running total, a materialized [[entity-event|entity]] table, a deduplication set, a windowed aggregate, or a join partner loaded from a [[stream-joins|stream-table]] side. Bellemare frames stateful streaming as the spine of most real EDMs: "most applications will need to maintain some degree of state for their processing requirements" (source: chapter-07-stateful-streaming.md).

**Sources**: `raw/building-event-driven-microservices/chapter-07-stateful-streaming.md`

**Last updated**: 2026-04-17

---

## Two related but distinct concepts

Chapter 7 opens with a definition split that the rest of the chapter leans on heavily (source: chapter-07-stateful-streaming.md):

- **[[materialized-state]]** — an *immutable* projection of events from the source stream. Derived; reproducible by replay.
- **[[state-store]]** — the *mutable* storage in which the microservice keeps business state and intermediate computations.

Both are required; they are not interchangeable. Materialized state lets the service use common business entities as inputs; the state store is where new business state and working intermediates live.

## The two storage locations

Every stateful service must decide where its state store physically lives (source: chapter-07-stateful-streaming.md):

- **[[internal-state-store]]** — same container/VM as the processor; on local memory or disk. RocksDB is the canonical in-process key/value engine.
- **[[external-state-store]]** — separate service over the network; any technology (RDBMS, document DB, Lucene-backed search, distributed KV).

The choice is a trade-off in throughput, cost, operational burden, and what kinds of queries the service needs. Chapter 7 spends most of its pages contrasting the two.

## Durability via the changelog

Stateful services store local state in volatile-looking places. The durability contract is achieved by **writing every state change to a [[changelog-stream]]** in the event broker. The changelog is the stream half of the [[table-stream-duality]] — the state store is the table, and its mutations are published as events (source: chapter-07-stateful-streaming.md).

Changelog streams are [[log-compaction|compacted]] because only the most recent value per key is needed to rebuild state. A recovered or newly scaled-up instance reloads its assigned partitions from the changelog and resumes — no need to re-read the input streams and re-run business logic (source: chapter-07-stateful-streaming.md).

Kafka Streams provides changelogs automatically; basic producer/consumer clients do not, and the developer must implement the pattern by hand (source: chapter-07-stateful-streaming.md).

## Stateful topology primitives

Stateful topologies compose a handful of building blocks already covered elsewhere in the wiki:

- **[[materialized-state]] from an input stream** — the core operation; builds a keyed table from [[entity-event|entity events]].
- **[[stream-joins|Stream-table join]]** — enrich an incoming event by key-lookup into a materialized table.
- **Stream-stream window join** — buffer both sides within a [[windowing|window]] and emit matches.
- **Aggregation / windowed aggregation** — running totals, counts, sums over [[windowing|windows]].
- **[[global-state-store|Global state]]** — every instance materializes every partition for reference lookups.
- **Deduplication** — a small keyed state table of recently-seen event IDs; see [[effectively-once-processing]].

## Recovery and scaling

Because state lives off to the side of the input stream, adding instances and recovering failed ones are the same operation: the new instance joins the [[consumer-group]], is assigned some partitions, and **materializes state for those partitions before processing new events** (source: chapter-07-stateful-streaming.md). The three options for how it builds state:

1. Reload from the **changelog** (fastest, normal path when available).
2. Reload from the **[[hot-replicas|hot replica]]** — zero-downtime failover if a replica already holds that partition's state.
3. Reprocess from the **input streams** (slow; may emit duplicates downstream).

See [[internal-state-store]] for the concrete mechanics and [[hot-replicas]] for the HA variant.

## Stateful processing and effectively-once

Stateful processing is where [[exactly-once-semantics|exactly-once]] stops being a marketing slogan and becomes a concrete engineering problem. Applying an event twice to a running total is wrong; so is missing an event. The state store, the consumer offsets, and any output events must all commit atomically. Two strategies from the chapter:

- **Client-broker transactions** (Kafka) — offsets, changelog writes, and output events are wrapped in one atomic transaction (source: chapter-07-stateful-streaming.md).
- **Local dedup + offsets-in-state** — when the broker does not support transactions, the service stores offsets alongside state in the state store and guards against duplicate events with a deduplication table.

See [[effectively-once-processing]] for the full treatment.

## Migrating vs rebuilding

When business logic or schema changes, the existing state store must catch up — either by a full **[[state-store-rebuilding-vs-migrating|rebuild]]** from the input streams, or by an in-place **migration** of the existing data. Rebuilding is simpler and always correct; migration is cheaper but error-prone (source: chapter-07-stateful-streaming.md).

## Where this sits in the wiki

Chapter 7 is the stateful counterpart to Chapter 5, which covered [[stateless-stream-processing]]. The two chapters together define the vocabulary for what an [[event-driven-microservices|event-driven microservice]] actually does between `consume` and `produce`. Deeper context:

- **[[table-stream-duality]]** — the fundamental pattern behind every materialized state store.
- **[[stream-processing-fault-tolerance]]** — Kleppmann's treatment of the same recovery problem in DDIA.
- **[[exactly-once-semantics]]** / **[[idempotence]]** — the correctness primitives behind effectively-once.
- **[[checkpointing-stream-processing]]** — the [[heavyweight-framework-microservice|heavyweight-framework]] form of the same durability pattern: operator state + key state written to external durable storage, restored atomically on failure or rescaling.

## Related pages

- [[stateless-stream-processing]]
- [[materialized-state]]
- [[state-store]]
- [[internal-state-store]]
- [[external-state-store]]
- [[global-state-store]]
- [[changelog-stream]]
- [[hot-replicas]]
- [[state-store-rebuilding-vs-migrating]]
- [[effectively-once-processing]]
- [[table-stream-duality]]
- [[stream-joins]]
- [[windowing]]
- [[stream-processing-fault-tolerance]]
- [[checkpointing-stream-processing]]
- [[heavyweight-framework-microservice]]
- [[event-driven-microservices]]
- [[microservice-topology]]
