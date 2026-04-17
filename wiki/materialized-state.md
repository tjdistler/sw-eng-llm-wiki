# Materialized State

**Summary**: A **projection of events from the source event stream into a point-in-time view of current state** — immutable in the sense that it is fully derivable from its input stream. Materialized state is the "table" side of the [[table-stream-duality]], and in [[stateful-stream-processing]] it is what a microservice consumes as a lookup structure for [[stream-joins|stream-table joins]] and enrichments.

**Sources**: `raw/building-event-driven-microservices/chapter-07-stateful-streaming.md`, `raw/building-event-driven-microservices/chapter-13-integrating-event-driven-and-request-response-microservices.md`

**Last updated**: 2026-04-17

---

## Definition

Bellemare's Chapter 7 pins the term down precisely: materialized state is "a projection of events from the source event stream (immutable)" (source: chapter-07-stateful-streaming.md). It contrasts with a [[state-store]], which is "where your service's business state is stored (mutable)".

The distinction matters because the two are often colocated in the same physical KV store but they have different guarantees:

- Materialized state is **derived** — if lost, it is rebuilt by replaying the source stream. Its correctness is a pure function of the input events.
- State-store state is **mutable business state** — updates are driven by processing logic, not by an input event one-to-one.

## How it is built

The process is straightforward: consume [[entity-event|entity events]] from a keyed input stream and **upsert** each into a local KV store keyed by the event's key (tombstones delete the key). This is exactly the Stream → Table direction of the [[table-stream-duality]] (source: chapter-07-stateful-streaming.md).

Each microservice instance materializes **only the partitions assigned to it** by the [[partition-assignor]]. Rebalancing drops revoked partitions' state and rebuilds the new partitions' state from the [[changelog-stream]] or input stream.

For the special case where every instance materializes every partition, see [[global-state-store]].

## Why it is load-bearing for EDM

Materialized state is how an EDM avoids the shared-database anti-pattern. Each consumer reads the producer's entity event stream and builds its own local view — no synchronous call to the producer's database, no coupling on the producer's schema. Two services can each hold a fresh view of the same customer-master data without ever talking to each other (source: chapter-07-stateful-streaming.md; see [[table-stream-duality]]).

## Partition locality

Because materialized state lives per-partition per-instance, any lookup against it requires that the lookup key be colocated with the input event's partition. This is what drives [[copartitioning]]: the input stream and the materialized stream must be partitioned on the same key with the same partition count, so the instance that owns partition *P* of the input also owns partition *P* of the materialized table.

For cross-partition lookups, either repartition the input ([[repartitioning]]) or materialize globally ([[global-state-store]]).

## Serving materialized state over a request-response API

Chapter 13 develops the pattern of exposing materialized state via a synchronous API so UIs and external systems can query it directly (source: chapter-13-integrating-event-driven-and-request-response-microservices.md). See [[serving-state-from-edm]] for the design space. When state is materialized in an [[internal-state-store]], routing a key's request to the owning instance typically uses a [[smart-load-balancer]] with an in-service redirect fallback. When state is in an [[external-state-store]], any instance can serve any key.

## Related pages

- [[state-store]]
- [[stateful-stream-processing]]
- [[table-stream-duality]]
- [[changelog-stream]]
- [[entity-event]]
- [[stream-joins]]
- [[global-state-store]]
- [[copartitioning]]
- [[partition-assignor]]
- [[log-compaction]]
- [[tombstone]]
- [[serving-state-from-edm]]
- [[smart-load-balancer]]
