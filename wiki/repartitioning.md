# Repartitioning

**Summary**: Repartitioning is the act of producing a new event stream that differs from its source in partition count, event key, or partitioner algorithm. It is the mechanism that establishes [[data-locality]] for downstream stateful stream processors.

**Sources**: `raw/building-event-driven-microservices/chapter-05-event-driven-processing-basics.md`

**Last updated**: 2026-04-17

---

## What repartitioning changes

Event streams are partitioned according to the event key and the [[partitioning-strategies|partitioner]] logic. For each event, the partitioner is applied and a partition is selected for the event to be written to (source: chapter-05-event-driven-processing-basics.md).

Repartitioning produces a new stream that differs in one or more of the following dimensions (source: chapter-05-event-driven-processing-basics.md):

- **Different partition count** — increase to raise downstream parallelism or to match another stream for [[copartitioning]].
- **Different event key** — change the key so that events that belong together land in the same partition.
- **Different event partitioner** — change the hash/routing logic used to pick a partition for a given key.

The partitioner algorithm deterministically maps an event's key to a specific partition, typically via a hash function. This ensures that all events with the same key end up in the same partition (source: chapter-05-event-driven-processing-basics.md).

## Why repartition

The central motivation is **data locality for stateful processing**. If downstream consumers want all events belonging to a given user to be processed by the same consumer instance — so that per-user state can be materialized locally — then every event for that user must land in the same partition. Repartitioning keyed on `user_id` provides exactly this guarantee (source: chapter-05-event-driven-processing-basics.md).

Bellemare's worked example: a stream of user actions comes in from a web endpoint with an arbitrary source partitioning. Consumers need all events for a given user co-located in one partition. A stateless repartitioning stage emits a new stream keyed on `user_id`, and a downstream consumer can now scale out to many instances, each owning a partition and holding a complete stateful account of its users (source: chapter-05-event-driven-processing-basics.md).

## Stateless processors as the natural repartitioner

A purely stateless processor rarely needs to repartition its own output — except to increase the partition count for downstream parallelism. However, a [[stateless-stream-processing|stateless microservice]] is often exactly the right place to repartition events consumed by a downstream stateful processor (source: chapter-05-event-driven-processing-basics.md). This is the canonical stateless-in-front-of-stateful topology.

## Repartitioning vs rebalancing

Do not confuse repartitioning (in the streaming sense) with [[rebalancing-partitions|rebalancing]] in a database. Repartitioning produces a **new stream** with a different partitioning scheme; the source stream is unchanged. Rebalancing a partitioned database moves partitions between nodes but does not change the logical partition-to-key mapping.

## Related pages

- [[copartitioning]]
- [[stateless-stream-processing]]
- [[partition-assignor]]
- [[partitioning]]
- [[partitioning-strategies]]
- [[consumer-group]]
- [[data-locality]]
- [[microservice-topology]]
- [[event-streams]]
- [[stream-joins]]
