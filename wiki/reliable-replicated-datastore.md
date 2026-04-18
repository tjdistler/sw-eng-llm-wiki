# Reliable Replicated Datastore

**Summary**: An application of a [[replicated-state-machine]] that holds key-value or configuration data, with a [[consensus]] algorithm in the critical path of every write. Throughput, performance, and read-scaling trade-offs matter enormously here because the consensus cost is paid per operation. Contrast with the leader-election pattern, where consensus runs at election time, not per request.

**Sources**: `raw/site-reliability-engineering/chapter-23-managing-critical-state-distributed-consensus-for-reliability.md`

**Last updated**: 2026-04-17

---

## Consensus in the critical path

Chapter 23's distinction: "Replicated datastores use consensus algorithms in the critical path of their work. Thus, performance, throughput, and the ability to scale are very important in this type of design" (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md).

Every state-changing operation runs a consensus round. That makes the four Chapter 23 performance-optimisation techniques — [[stable-leader]]s, [[quorum-leases]], batching, pipelining — essential rather than optional for this pattern. A [[reliable-distributed-queue]] and a reliable replicated datastore are structurally similar (both are RSMs with consensus per operation), but the datastore case tends to face lower-latency requirements and richer read-scaling workloads.

## Read consistency semantics

A reliable replicated datastore can offer different consistency semantics for reads, which dramatically affect how it scales (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md). The menu is:

- **Consensus read** — a read-only consensus operation; provides the strongest guarantee at full consensus latency.
- **Leader read** — in a [[stable-leader]] system, the leader has the most up-to-date state and can serve [[linearizability|linearizable]] reads.
- **Replica read with [[quorum-leases]]** — the lease grants some replicas the right to serve strongly-consistent local reads for the duration of the lease.
- **Replica read without lease** — stale reads; acceptable in some workloads (Google's Photon uses this because stale data causes only extra work, not incorrect results).

This is the operational form of the [[leader-based-replication]] read-from-follower trade-off, applied in a consensus context.

## Why not timestamps

Other (non-consensus-based) replicated datastores often rely on **timestamps** to provide bounds on the age of data being returned. Chapter 23 is sharp about this being a dead end in general distributed systems: "Timestamps are highly problematic in distributed systems because it's impossible to guarantee that clocks are synchronized across multiple machines" (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md).

[[spanner|Spanner]] is the canonical exception — it addresses this by **modelling the worst-case uncertainty involved** (via TrueTime) and slowing down processing where necessary to resolve that uncertainty. For systems without that infrastructure, timestamps are not a safe substitute for consensus-based consistency.

This is the same point [[unreliable-clocks]] and [[clock-synchronization]] make from the DDIA side: wall-clock ordering across machines is not a reliable primitive, and any design that depends on it has hidden correctness bugs.

## Packaging

[[zookeeper|ZooKeeper]], etcd, Consul, and [[chubby|Chubby]] are all reliable replicated datastores in this sense, as well as being coordination services. Their datastore API is the consumer-facing surface; the RSM-over-consensus implementation is what makes the API safe.

## Related pages

- [[managing-critical-state]]
- [[consensus]]
- [[replicated-state-machine]]
- [[stable-leader]]
- [[quorum-leases]]
- [[consensus-performance]]
- [[consensus-disk-access]]
- [[linearizability]]
- [[leader-based-replication]]
- [[zookeeper]]
- [[chubby]]
- [[spanner]]
- [[unreliable-clocks]]
