# Hot Replicas

**Summary**: A high-availability pattern for [[internal-state-store|internal state stores]] in which **each stateful partition's state is materialized on more than one instance** — one as the leader, the others as hot replicas. On leader failure, the [[partition-assignor]] promotes a replica that already holds the full state, eliminating the changelog-rebuild downtime that would otherwise block the new partition owner. Kafka Streams ships this as a single configuration setting.

**Sources**: `raw/building-event-driven-microservices/chapter-07-stateful-streaming.md`

**Last updated**: 2026-04-17

---

## Why it exists

Normally, each stateful partition is materialized on exactly one instance. When that instance dies, whichever instance inherits the partition must rebuild state from the [[changelog-stream]] before it can process new events — potentially a significant outage if state is large (source: chapter-07-stateful-streaming.md).

A hot replica is a second (or Nth) instance that has **already materialized** a given partition's state, tailing the changelog to stay in sync with the leader. If the leader dies, a hot replica is promoted and resumes processing with zero state-rebuild delay (source: chapter-07-stateful-streaming.md).

## How it works

Configuration looks like "replication factor = N" (for N = 2, each partition is materialized twice: once as leader, once as replica). Chapter 7's example is a three-instance cluster with N = 2 for each partition:

- Instance 0 owns the leader for partition A-P0; instance 1 holds a hot replica of it.
- Instance 1 owns the leader for A-P1; instance 2 holds a hot replica.
- Instance 2 is otherwise idle (no leadership), just maintaining replicas.

Each replica manages its own offsets against the changelog to track how far it has caught up to the leader (source: chapter-07-stateful-streaming.md).

When instance 1 dies, the [[partition-assignor]] rebalances. It knows where the hot replicas are (it previously placed them) and **gives replica-holders priority** to claim the ownership of the partition they already have state for. Instance 2 takes over A-P1 and resumes processing immediately; instance 0 has no work change for A-P0 because it was already the leader.

## The rebuild-the-missing-replica step

Promotion fills the leader gap but drops the replica count. After the failover, new hot replicas must be built from the changelog on the remaining instances to restore N (source: chapter-07-stateful-streaming.md). During that catch-up window the system is at reduced redundancy, but processing is not blocked.

## Trade-off

Bellemare's note: "One of the main tradeoffs with a hot-replica approach is the use of additional disk to maintain the replicas in exchange for the reduction in downtime due to an instance failure" (source: chapter-07-stateful-streaming.md). N replicas means N× the disk, N× the network traffic to tail the changelog, and N× the cost — in exchange for near-zero-downtime failover.

## Seamless scale-up (lightweight frameworks)

Chapter 12 highlights a second use specific to [[lightweight-framework-microservice|lightweight-framework]] deployments: hot replicas can also smoothly *scale up* an application without the usual rematerialization pause. The baseline scale-up workflow is (source: chapter-12-lightweight-framework-microservices.md):

1. Start a new instance.
2. Join the consumer group and rebalance partition ownership.
3. Pause while state is materialized from the changelog (can be long for large state).
4. Resume processing.

The hot-replica-driven alternative (under development for Kafka Streams): pre-populate a replica of the state on the new instance, wait until it's caught up to the head of the changelog, *then* rebalance to assign it ownership of the input partitions. This trades a bit of extra broker bandwidth (tailing the changelog on the pre-warming replica) for a near-zero-downtime scale-up — the same replica mechanism serving both failover and graceful capacity increases.

## When to use it

- **Low-latency SLAs.** When a partition being offline for a minute to rebuild state from changelog is unacceptable.
- **Large state stores.** The bigger the state, the longer the rebuild, the bigger the win.
- **Event-driven services on critical paths.** User-visible latency budgets rule out changelog-rebuild outages.

For small state or cheap rebuilds, the extra disk and ops are usually not worth it; plain changelog-based recovery is simpler.

## Related pages

- [[internal-state-store]]
- [[changelog-stream]]
- [[stateful-stream-processing]]
- [[partition-assignor]]
- [[consumer-group]]
- [[fault-tolerance]]
- [[lightweight-framework-microservice]]
