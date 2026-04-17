# Replicated Sharded Service

**Summary**: A combination of Burns's first two serving patterns: a [[sharded-service-pattern|sharded service]] where each individual shard is itself implemented as a [[replicated-load-balanced-service]]. Each shard becomes resilient to failures, independently scalable for load, and safe to roll out during peak traffic — at the cost of a more complex deployment.

**Sources**: `raw/designing-distributed-systems/chapter-06-sharded-services.md`, `raw/designing-distributed-systems/chapter-07-scattergather.md`

**Last updated**: 2026-04-16

---

## Why combine the two patterns

A plain sharded service has a per-shard single point of failure: lose shard `i` and every request routed to shard `i` fails (or misses, in the cache case) until the shard is restored (source: raw/designing-distributed-systems/chapter-06-sharded-services.md). For a system whose latency or load profile cannot tolerate that — Burns's example is a cache the application is deeply dependent on — the answer is to **replace each shard with a replicated, load-balanced sub-service**:

```
             ┌──────────┐
             │   Root   │
             └─────┬────┘
    ┌────────┬─────┴─────┬────────┐
    ▼        ▼           ▼        ▼
┌──────┐ ┌──────┐    ┌──────┐ ┌──────┐
│Shard0│ │Shard0│    │Shard1│ │Shard1│  ... etc.
│ rep1 │ │ rep2 │    │ rep1 │ │ rep2 │
└──────┘ └──────┘    └──────┘ └──────┘
  └── LB ──┘            └── LB ──┘
    Shard 0               Shard 1
```

The root sharding function still picks the correct shard; that shard is then served by a load-balanced cluster of replicas (source: raw/designing-distributed-systems/chapter-06-sharded-services.md).

## What the combination buys you

Burns's list of payoffs (source: raw/designing-distributed-systems/chapter-06-sharded-services.md):

1. **Shard failures become degraded performance, not outages.** A replica can fail without taking the shard offline. If the system relied on the cache's latency improvement, that improvement survives.
2. **Safe rollouts during peak traffic.** In a plain sharded cache, deploying a new version temporarily loses shard capacity as the new instance starts empty. With replication, you roll forward one replica at a time; the shard as a whole stays warm.
3. **Per-shard scaling to absorb load.** Each shard's load is independent of the others. A shard that gets more traffic can be scaled up **independently** — other shards keep their original replica count. This is the substrate that makes [[hot-sharding]] possible: autoscale the replica count per shard in response to organic traffic shifts.

## The complexity cost

The deployment is noticeably more complex than either of the constituent patterns (source: raw/designing-distributed-systems/chapter-06-sharded-services.md):

- Each shard is now a `Deployment` + `Service` pair (in Kubernetes terms), not just a single pod.
- The root needs to resolve per-shard service names rather than per-shard pod DNS.
- Capacity planning must consider shard count **and** per-shard replica count as independent knobs.
- Observability spans two levels: per-shard totals and per-replica-within-shard detail.

For low-stakes caches, the plain sharded pattern is often simpler and good enough. Burns recommends the replicated-sharded combination specifically when *"your system is so dependent on a cache for latency or load that it is not acceptable to lose an entire cache shard."*

## Relationship to DDIA replication-plus-partitioning

This combination is the service-layer analogue of what DDIA calls "combining replication with partitioning" — a database typically replicates each partition across multiple nodes, and [[partitioning]] already notes that partitioning and replication are almost always used together. Burns arrives at the same conclusion from the service side: sharding a stateful serving tier benefits from shard-level replication for the same reliability and load-distribution reasons that database partitions do. See:

- [[partitioning]] for the general point.
- [[replication]] for the three replication architectures (leader-based, multi-leader, leaderless). A replicated cache shard is usually leaderless in the weak sense — any replica can serve a read; writes (cache inserts on misses) can be handled independently and eventually converge because cache content is derivable.
- [[leader-based-replication]] applies when shards must provide a stronger consistency story than caches do.

## Relationship to the base serving patterns

This pattern is purely compositional: it is [[replicated-load-balanced-service]] nested inside [[sharded-service-pattern]]. Both constituent patterns have their own pages covering their mechanics; this page exists to name the combination and capture Burns's reasons for using it.

## Relationship to scatter/gather

The same "replicate each shard" construction is the canonical fix for the reliability and scale limitations of the [[scatter-gather-pattern]]: each scatter/gather leaf becomes a replicated load-balanced sub-service rather than a single node, so the root's fan-out is resilient to leaf failures and safe to upgrade under load (source: raw/designing-distributed-systems/chapter-07-scattergather.md). The shape is identical to this page's diagram, with the difference being **how the root dispatches**: a sharded service's root routes each request to one shard, while a scatter/gather root fans it out to all shards.

## Related pages

- [[sharded-service-pattern]]
- [[sharded-cache]]
- [[hot-sharding]]
- [[replicated-load-balanced-service]]
- [[replication]]
- [[partitioning]]
- [[fault-tolerance]]
- [[scalability]]
- [[scaling-approaches]]
- [[scatter-gather-pattern]]
- [[tail-latency-amplification]]
- [[designing-distributed-systems]]
