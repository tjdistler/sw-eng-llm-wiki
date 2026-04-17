# Internal State Store

**Summary**: A [[state-store]] that **coexists with the microservice instance** in the same container or VM. The canonical implementation is RocksDB on a local SSD, with every mutation mirrored to a [[changelog-stream]] for durability. Internal state is what lets a [[stateful-stream-processing|stateful]] microservice push throughput into the hundreds of thousands of events per second while keeping the operational burden on the broker and compute cluster rather than on a separate data service.

**Sources**: `raw/building-event-driven-microservices/chapter-07-stateful-streaming.md`, `raw/building-event-driven-microservices/chapter-13-integrating-event-driven-and-request-response-microservices.md`

**Last updated**: 2026-04-17

---

## Shape

The state store's lifetime is tied to the instance's lifetime: the store lives on the same hardware, its data is partitioned the same way as the consumer's input, and dropping a revoked partition after a [[consumer-group]] rebalance is as simple as deleting the partition's data from the local KV (source: chapter-07-stateful-streaming.md).

Each instance materializes **only the partitions assigned to it**. Partitions' data are kept logically separate within the store so that rebalancing does not force a wholesale teardown.

Typical implementation: **RocksDB** on a local SSD (source: chapter-07-stateful-streaming.md). Any KV or even relational engine can be embedded, but RocksDB dominates because its LSM-tree layout (see [[sstables-and-lsm-trees]]) is well suited to the high-write-rate, key-lookup pattern of stream-table joins.

## Advantages

**Scalability is offloaded to the platform** (source: chapter-07-stateful-streaming.md). Application teams add instances; the broker, [[partition-assignor]], and compute scheduler handle the rest. There is only one unit of scale — the instance count.

**Disk-based performance is high enough for most use cases.** A RocksDB random-access read on local SSD takes ~65 μs; a single processing thread tops out near 15.4k requests/second (source: chapter-07-stateful-streaming.md). In-memory is faster still — millions of operations per second.

**Network-attached volumes are an option.** Persistent cloud volumes can be reattached to a replacement instance, allowing state to survive an instance restart without a changelog rebuild. The trade-off is that a 1 ms network round-trip collapses the 15.4k/s ceiling to ~939/s, so network-attached only fits services that don't need the peak (source: chapter-07-stateful-streaming.md).

## Disadvantages

**Volume sizing is fixed at runtime.** Changing disk size or count usually means stopping the service, reconfiguring the volume, and restarting. Many cluster managers allow only growing a volume, not shrinking (source: chapter-07-stateful-streaming.md).

**Disk is wasted during troughs.** A cyclical workload (shopping site at 3 a.m. vs 3 p.m.) must reserve disk for peak; the trough bytes are paid for either way. Pay-per-byte external services avoid this (source: chapter-07-stateful-streaming.md).

**Queries are limited to the embedded engine's capabilities.** RocksDB gives you KV operations. Foreign-key joins, geospatial indexes, and full-text search usually push a service toward an [[external-state-store]].

## Durability and recovery

Internal state is not durable on its own. Durability comes from the [[changelog-stream]] — every state-store write is also produced to a compacted event-broker topic. A recovered or newly scaled instance rebuilds its partitions' state by consuming the changelog before processing new events (source: chapter-07-stateful-streaming.md).

Two alternative recovery paths (source: chapter-07-stateful-streaming.md):

- **[[hot-replicas]]** — a second (or Nth) instance already holds the partition's state; failover is immediate.
- **Rebuild from input streams** — if no changelog exists, replay the input. Slow, and any non-idempotent output events are re-emitted; consumers must [[idempotence|deduplicate]].

## Serving reads over a request-response API

Chapter 13 adds a serving dimension: an instance can expose a synchronous API over the partitions' state it holds (source: chapter-13-integrating-event-driven-and-request-response-microservices.md). Because each partition is on exactly one instance, requests must reach the right one. A round-robin load balancer has only a `1/N` hit rate for N instances; a [[smart-load-balancer]] applies the partitioner and consumer-group map to route directly. Mis-forwarded requests still need an in-service redirect fallback to cover rebalance races. See [[serving-state-from-edm]].

## Fit

Internal state stores are the default for high-throughput stateful streaming. The usual fit profile (source: chapter-07-stateful-streaming.md):

- Event volume is high enough that external latency would dominate.
- Queries are KV-shaped (point lookups, scans).
- State size per partition fits on affordable local SSD.
- The platform team provides a broker that handles changelogs natively (Kafka Streams does).

## Related pages

- [[state-store]]
- [[external-state-store]]
- [[global-state-store]]
- [[changelog-stream]]
- [[hot-replicas]]
- [[stateful-stream-processing]]
- [[consumer-group]]
- [[partition-assignor]]
- [[sstables-and-lsm-trees]]
- [[materialized-state]]
- [[serving-state-from-edm]]
- [[smart-load-balancer]]
