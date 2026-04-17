# Hot Sharding

**Summary**: Burns's name for dynamically re-scaling individual shards of a [[replicated-sharded-service]] in response to organic traffic skew. When one shard becomes "hot" — a single photo goes viral, one user is a celebrity — that shard's replica count is autoscaled upward, while cold shards can be packed onto fewer machines. The service-level analogue of DDIA's [[hot-spots|hot-spot mitigation]], enabled by the per-shard replication described in [[replicated-sharded-service]].

**Sources**: `raw/designing-distributed-systems/chapter-06-sharded-services.md`

**Last updated**: 2026-04-16

---

## The problem: organic skew

An evenly sharded service assumes roughly uniform load per shard. Real workloads frequently violate that assumption (source: raw/designing-distributed-systems/chapter-06-sharded-services.md):

> "Ideally the load on a sharded cache will be perfectly even, but in many cases this isn't true and 'hot shards' appear because organic load patterns drive more traffic to one particular shard."

Burns's example: a sharded cache for user photos. When a photo goes viral, every request for it maps — correctly — to the same shard. That shard is now serving orders of magnitude more traffic than its siblings.

Hash uniformity does not save you here. A good hash function distributes **distinct keys** uniformly across shards, but if most requests hit **the same key**, they all land on the same shard. This matches DDIA's [[hot-spots#Hash partitioning with a single dominant key|celebrity-key problem]] exactly.

## Burns's response: hot sharding

Given a [[replicated-sharded-service|replicated sharded service]] where each shard is an autoscalable [[replicated-load-balanced-service]]:

> "When this happens, with a replicated, sharded cache, you can scale the cache shard to respond to the increased load. Indeed, if you set up autoscaling for each cache shard, you can dynamically grow and shrink each replicated shard as the organic traffic to your service shifts around." (source: raw/designing-distributed-systems/chapter-06-sharded-services.md)

The mechanism Burns illustrates (Figure 6-3 in the chapter):

1. Start with three shards (A, B, C) each on one machine, evenly loaded.
2. Traffic shifts: Shard A now receives 4× the traffic of B and C.
3. Shard A is replicated onto a second machine.
4. Shards B and C are **combined onto a single machine** to free up the capacity.
5. Traffic is again equally shared per machine, even though shard load is unequal.

Two operations at once: **replicate the hot shard** (scale out) and **compact cold shards** (scale in). Per-shard autoscaling drives both; the operational assumption is that the root can follow the new shard-to-machine mapping as it changes.

## Why this works only with shard replication

Hot sharding is the payoff for deploying each shard as a replicated sub-service. Without per-shard replication, the only response to a hot shard is to re-shard the entire service (remap the sharding function) — an expensive operation that invalidates cache state across the fleet. With per-shard replication, scaling is *additive*: another replica joins the hot shard's internal load balancer and starts taking traffic. No keys move, no routing changes at the root level.

See [[replicated-sharded-service]] for the structural pattern and [[hot-spots]] for the equivalent treatment at the database layer.

## Hot sharding vs DDIA hot-spot mitigation

The database and service responses to skew have different costs:

| Approach | Level | Mechanism |
|---|---|---|
| [[hot-spots#Application-level mitigation for extreme hot spots|Write-side key splitting]] | Database / application | Add a random suffix to the hot key; reads must query all suffixes. Application tracks which keys have been split. |
| Compound-key partitioning | Database | Choose a partition key that naturally distributes one-to-many relationships. Prevents some skew structurally. |
| **Hot sharding** | Service (Burns) | Scale the replica count of the hot shard up; let the per-shard load balancer fan requests across the replicas. No key changes; no application changes. |

Service-level hot sharding is appealing when the hot shard can tolerate more replicas serving the same data — which is exactly the cache case. It does *not* help when the shard is stateful in a way that prevents straightforward replication (e.g. single-writer semantics), in which case DDIA's structural techniques apply.

## Dependence on fast, trustworthy autoscaling

Burns treats hot sharding as something you *set up* — per-shard autoscaling, presumably driven by per-shard load metrics — rather than a manual operation. The prerequisites are:

- Per-shard load metrics that the autoscaler can read.
- A stable per-shard service abstraction (Kubernetes `Service`-per-shard, not pod-per-shard) so that replica count can change transparently.
- A root that does not need to be reconfigured when a shard's replica count changes — it sees the per-shard service name, not individual replicas.

Kubernetes's `HorizontalPodAutoscaler` on a per-shard `Deployment` is the natural implementation, though Burns does not walk through the YAML.

## Relationship to rebalancing

Hot sharding is one flavour of [[rebalancing-partitions|rebalancing]]: moving load from overloaded shards to underloaded ones. It is distinct from re-sharding (changing the sharding function and remapping keys) — hot sharding keeps the sharding function constant and only changes per-shard capacity. This is structurally similar to DDIA's "fixed number of partitions" strategy, where partition count is constant and rebalancing redistributes partitions to nodes. In the cache case Burns describes, there are no partitions moving — just replicas being added to or removed from individual shards.

## Related pages

- [[replicated-sharded-service]]
- [[sharded-service-pattern]]
- [[sharded-cache]]
- [[hot-spots]]
- [[rebalancing-partitions]]
- [[scaling-approaches]]
- [[scalability]]
- [[replicated-load-balanced-service]]
- [[designing-distributed-systems]]
