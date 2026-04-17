# Sharder Pattern

**Summary**: The fourth of Burns's five linking patterns for [[event-driven-batch-pattern|event-driven batch workflows]]. A **sharder** is a generalisation of the [[splitter-pattern|splitter]] that evenly distributes work items across N downstream queues using a hash-based sharding function. The motivation is not semantic routing but **reliability and load distribution** — the workflow tolerates failures and spreads work across independent resources.

**Sources**: `raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md`

**Last updated**: 2026-04-16

---

## What it does

A sharder applies a hash function to each item and routes it to exactly one of N output queues based on the hash (source: raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md). Unlike a [[splitter-pattern|splitter]], the destination is chosen **uniformly at random** (statistically) rather than by a semantic predicate; unlike a [[copier-pattern|copier]], each item goes to exactly one downstream queue.

Burns calls this "a slightly more generic form of splitter" and ties it explicitly to the [[sharded-service-pattern|sharded service pattern]] from Chapter 6 — the same shard-and-route mechanic, applied at the batch-workflow layer rather than the serving layer (source: raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md).

## Why shard a work queue

Burns gives two motivations (source: raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md):

### Reliability via staged rollouts

If one monolithic queue processes all work, any failure — a bad worker-image update, an infrastructure outage, a poisoned message — affects **all users**. Sharding the queue four ways limits the blast radius of a bad rollout to one quarter of users during a staged rollout:

> "If you push a bad update to your worker container, which causes your workers to crash and your queue to stop processing work items. If you only have a single work queue that is processing items, then you will have a complete outage for your service with all users affected. If, instead, you have sharded your work queue into four different shards, you have the opportunity to do a staged rollout of your new worker container. Assuming you catch the failure in the first phase of the staged rollout, sharding your queue into four different shards means that only one quarter of your users would be affected" (source: raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md).

This is the batch-workflow counterpart to [[replicated-sharded-service|replicated-sharded serving]] — the blast radius argument for sharding is identical in both regimes.

### Load distribution across regions

A sharder can evenly spread work across datacenters or regions when the items don't care which region processes them. "You can use a sharder to evenly spread work across multiple datacenters to even out utilization of all datacenters/regions. As with updates, spreading your work queue across multiple failure regions also has the benefit of providing reliability against datacenter or region failures" (source: raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md).

## Dynamic adjustment under shard failure

When a shard fails (the target queue or worker pool goes unhealthy), "the sharding algorithm dynamically adjusts to send work to the remaining healthy work queues, even if only a single queue remains" (source: raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md). The workflow degrades but continues — the system chooses "work still gets processed" over "work stays perfectly distributed."

This is the healthy-subset sharding mechanic that recurs throughout Burns's book and DDIA alike:

- [[sharded-service-pattern|Chapter 6 sharded services]] route around dead shards.
- [[consistent-hashing]] is the mechanism that keeps this cheap under scale-in and scale-out.
- [[rebalancing-partitions]] covers the DDIA treatment at the storage layer.

## Worked example: user-signup verification

In Burns's chapter-length workflow example, new-user signup events are sharded across multiple geographic failure zones before being handed to the verification-email worker (source: raw/designing-distributed-systems/chapter-11-event-driven-batch-processing.md). The shard function is by user region; the downstream workers in each zone send the verification email.

The motivation is reliability, not load-balancing: if one region fails, the others keep processing signups, and the system continues "even in the presence of partial failures."

## Relationship to the sharded-service pattern

Chapter 6's [[sharded-service-pattern]] shards a *stateful serving tier* — each shard holds disjoint state, and a root routes read/write requests by key. Chapter 11's sharder pattern shards a *stateless batch workflow stage* — each shard holds nothing, and the sharder routes items by hash for distribution.

Both share the sharding function as the design lever and both face [[shard-key-selection]] as the interesting design question. The difference is that the batch sharder has no state — shards are interchangeable, and a failed shard's work can be routed to any peer, which is why Burns's "even if only a single queue remains" works here but would be a data-loss catastrophe in a stateful sharded service.

## Relationship to DDIA partitioning

The sharder at the batch-workflow layer is a container-level implementation of DDIA's [[partitioning]] mechanic. The shard function plays the same role, and [[partitioning-strategies|hash vs range partitioning]] applies. [[hot-spots]] are a concern here too — a badly chosen shard function will pile work onto one downstream queue.

## Related pages

- [[event-driven-batch-pattern]]
- [[splitter-pattern]]
- [[copier-pattern]]
- [[filter-pattern]]
- [[merger-pattern]]
- [[sharded-service-pattern]]
- [[shard-key-selection]]
- [[replicated-sharded-service]]
- [[partitioning]]
- [[partitioning-strategies]]
- [[consistent-hashing]]
- [[hot-spots]]
- [[work-queue-pattern]]
- [[publisher-subscriber-infrastructure]]
- [[designing-distributed-systems]]
