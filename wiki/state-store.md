# State Store

**Summary**: The **mutable** storage where a stateful microservice keeps its business state and intermediate computations. Bellemare distinguishes a state store (mutable, business-driven) from [[materialized-state]] (immutable, stream-derived), though in practice they frequently share the same KV engine. A state store lives either [[internal-state-store|inside]] the service's container or [[external-state-store|outside]] it; the choice drives throughput, cost, and recovery mechanics.

**Sources**: `raw/building-event-driven-microservices/chapter-07-stateful-streaming.md`

**Last updated**: 2026-04-17

---

## Definition

From Chapter 7's definition split: a state store is "where your service's business state is stored (mutable)", in contrast with [[materialized-state]] which is "a projection of events from the source event stream (immutable)" (source: chapter-07-stateful-streaming.md). Both are needed in most real services: the materialized state feeds lookups; the state store holds the output of business logic that is not a pure function of one input event.

## The internal / external split

Every state store is one of two shapes (source: chapter-07-stateful-streaming.md):

| | [[internal-state-store]] | [[external-state-store]] |
|---|---|---|
| **Location** | Same container/VM as the processor | Separate service over the network |
| **Typical tech** | RocksDB, in-memory KV | RDBMS, document DB, Lucene, KV cluster |
| **Data locality** | Per-partition (owned by the instance) | Full (every instance can read everything) |
| **Scaling** | Offloaded to broker + compute cluster | Independently managed; team's responsibility |
| **Latency** | Microseconds (local SSD or RAM) | Milliseconds (network hop) |
| **Cost model** | Pay for disk you provisioned | Pay per byte / per transaction |
| **Recovery source** | [[changelog-stream]] or input stream | Snapshots, changelog, or input stream |
| **Sharing state** | Impossible by construction | Possible — and an anti-pattern |

The single largest hidden trade-off: **"local" does not necessarily mean physically attached.** Modern cloud deployments often mount network-attached disk that *logically* behaves like local disk. A 1 ms round-trip to such a disk drops RocksDB's single-thread ceiling from ~15.4k req/s to ~939 req/s — a 16x hit that changes whether the service can meet SLA (source: chapter-07-stateful-streaming.md).

## Do not share a state store across services

Bellemare is emphatic: "Do not share direct state access with other microservices. Instead, all microservices must materialize their own copy of state" (source: chapter-07-stateful-streaming.md). Sharing a state store couples otherwise-unrelated services together on a schema that neither owns. Even if the underlying tech is a shared cluster, the *data set* must remain logically isolated per service.

This is the external-state-store version of the [[shared-database-antipattern]].

## Durability via the changelog

The state store is typically volatile (local disk, in-memory, or ephemeral container storage). Durability is achieved by mirroring every state change to a [[changelog-stream]] in the broker. If the instance dies, a replacement reloads its partitions from the changelog and resumes (source: chapter-07-stateful-streaming.md).

See [[changelog-stream]] for mechanics and [[hot-replicas]] for the zero-downtime variant.

## Choosing between internal and external

The decision is driven by (source: chapter-07-stateful-streaming.md):

- **Throughput requirements.** High-throughput services (100k+ events/s) almost always want internal + local SSD.
- **Query patterns.** Foreign-key joins, geospatial queries, and relational queries over large cross-partition sets favor external.
- **Team composition.** External means the team now runs a database. Internal means the team is limited to whatever KV operations the embedded engine supports.
- **Cost profile.** Bursty, cyclical workloads can waste disk on internal stores; external pay-per-byte services absorb the cycles better.
- **Recovery SLA.** Internal-with-changelog recovers at broker bandwidth. External recovery is a database-admin problem.

## Related pages

- [[materialized-state]]
- [[internal-state-store]]
- [[external-state-store]]
- [[changelog-stream]]
- [[stateful-stream-processing]]
- [[hot-replicas]]
- [[state-store-rebuilding-vs-migrating]]
- [[table-stream-duality]]
- [[shared-database-antipattern]]
