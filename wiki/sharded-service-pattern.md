# Sharded Service Pattern

**Summary**: The second multi-node serving pattern in Burns's catalogue. Unlike a [[replicated-load-balanced-service]] where every replica can handle every request, a sharded service's replicas (shards) each handle only a subset of requests. A load-balancing **root** examines each request and distributes it to the appropriate shard or shards. Sharded services are generally used for **stateful** services whose state is too large for a single machine — Burns's canonical example is a sharded cache, but the pattern generalises to any service whose working set exceeds one machine.

**Sources**: `raw/designing-distributed-systems/chapter-06-sharded-services.md`

**Last updated**: 2026-04-16

---

## The shape of the pattern

A sharded service consists of two components (source: raw/designing-distributed-systems/chapter-06-sharded-services.md):

- **A set of shard replicas.** Each shard serves only a subset of requests. The subset is determined by the sharding function applied to some property of the request.
- **A root (load-balancing router).** Examines each request, applies the sharding function, and forwards the request to the shard that owns it.

```
           ┌───────────┐
           │   Root    │
           └─────┬─────┘
        ┌────────┼────────┐
        ▼        ▼        ▼
   ┌────────┐┌───────┐┌────────┐
   │Shard 0 ││Shard 1││Shard 2 │
   └────────┘└───────┘└────────┘
```

Contrast with [[replicated-load-balanced-service]], where every replica is interchangeable and the load balancer simply round-robins. The root is not a round-robin distributor — it is a sharding-aware router.

## Why shard at all

> "The primary reason for sharding the data is because the size of the state is too large to be served by a single machine. Sharding enables you to scale a service in response to the size of the state that needs to be served." (source: raw/designing-distributed-systems/chapter-06-sharded-services.md)

For an **application-level cache**, the pay-off is memory utilisation. Ten replicated cache instances with 10 GB each can only cache 10 GB of unique data (each replica holds a copy). Ten **sharded** cache instances with 10 GB each can cache **100 GB** of unique data — each key exists on exactly one shard (source: raw/designing-distributed-systems/chapter-06-sharded-services.md). See [[sharded-cache]] for the full walk-through.

For other stateful services — Burns cites a large multiplayer game world — sharding lets the system hold more state than any single node could. The game-world example shards by player location, so players physically near each other in the virtual world land on the same server (source: raw/designing-distributed-systems/chapter-06-sharded-services.md).

## The two essential design questions

Deploying a sharded service forces two decisions that do not arise in the replicated pattern (source: raw/designing-distributed-systems/chapter-06-sharded-services.md):

1. **How many shards?** This is a [[rebalancing-partitions|capacity planning]] question with a cost tied to it: reshading is expensive when the sharding function changes (see below).
2. **What is the shard key, and what is the sharding function?** See [[shard-key-selection]] for Burns's treatment of this, and [[consistent-hashing]] for the hashing technique that keeps re-sharding tolerable.

## Stateful, not stateless

Burns's framing (source: raw/designing-distributed-systems/chapter-06-sharded-services.md):

> "Replicated services are generally used for building stateless services, whereas sharded services are generally used for building stateful services."

The stateful-ness is the reason sharding is needed: the state is too large to replicate across all serving nodes. Once state is sharded, every other operational property — failure handling, rollout, scaling — is harder than in the replicated case, because each shard is effectively unique. See [[sharded-cache#Role of cache criticality]] for the specific "what if a shard fails" reasoning.

## Impact of shard failure

In a replicated load-balanced service, losing a replica costs some fraction of capacity but no functionality — every surviving replica can still serve every request. In a sharded service, losing shard `i` means **every request mapped to shard `i` fails** until the shard is restored (source: raw/designing-distributed-systems/chapter-06-sharded-services.md).

For caches this may be tolerable (miss, recalculate, move on — though with latency and upstream-load consequences). For a stateful service where the shard **owns** the data (not merely caches it), a shard outage is a full outage for those users or keys. Two mitigations:

- **Replicate each shard.** The shard is itself a [[replicated-load-balanced-service]]; shard failures become degraded performance rather than outages. See [[replicated-sharded-service]].
- **Overprovision.** Rate the system conservatively so it can absorb the cache-miss traffic when a shard is down.

## Deployment variants: ambassador vs shared routing service

Burns explicitly compares two ways to deploy the root (source: raw/designing-distributed-systems/chapter-06-sharded-services.md):

- **Per-pod [[client-side-sharding|sharding ambassador]].** Every client pod runs a twemproxy (or similar) container that routes to the shards. No shared routing tier; `localhost` call; minimum latency. Downside: every application pod must carry the ambassador.
- **Shared shard routing service.** A [[replicated-load-balanced-service]] of twemproxy replicas sits between all clients and the shards. Simpler per-client deployment (clients resolve one service name); must be scaled with demand; adds a network hop.

This is the same client-side-vs-server-side trade-off that appears in [[ambassador-pattern]]. Burns's Ch 6 hands-on deploys both variants.

## Relationship to existing wiki concepts

### Relationship to DDIA partitioning

The core idea is identical to database [[partitioning]]: split a larger state across multiple nodes so each holds a fraction. Burns's vocabulary:

| Burns (service-level) | DDIA (database-level) |
|---|---|
| shard | partition / shard |
| root | routing tier ([[request-routing]]) |
| sharding function | hash + modulo, or key-range lookup ([[partitioning-strategies]]) |
| re-sharding | [[rebalancing-partitions]] |
| hot shard | [[hot-spots|hot spot]] |

The mechanics described in [[partitioning-strategies]] (hash vs key-range), [[consistent-hashing]] (minimum remapping), [[rebalancing-partitions]] (three strategies), and [[request-routing]] (how clients find the right node) all apply to sharded services. What is new at the service level — and treated distinctly in Burns's chapter — is the **operational** story: what it means to upgrade a shard, what happens when traffic skew creates a hot shard in a cache, and how an [[ambassador-pattern]] factors the routing logic out of application code.

### Relationship to the replicated pattern

See [[replicated-load-balanced-service]] for the simpler pattern this one contrasts with. A shard can itself be a replicated load-balanced service — that is the [[replicated-sharded-service]] combination.

### Relationship to scatter/gather

When a request must consult *multiple* shards (not just one), the pattern evolves into the [[scatter-gather-pattern]] — Chapter 7 of Burns's book. A sharded service's root routes each request to exactly one shard; a scatter/gather root fans each request out to **all** leaves and recombines the partial results. The leaf-sharded variant of scatter/gather reuses this chapter's shard-count and shard-key design questions, and adds two new concerns specific to fan-out: [[tail-latency-amplification]] and the straggler problem. See [[scatter-gather-pattern]].

## Related pages

- [[replicated-load-balanced-service]]
- [[sharded-cache]]
- [[replicated-sharded-service]]
- [[hot-sharding]]
- [[shard-key-selection]]
- [[partitioning]]
- [[partitioning-strategies]]
- [[consistent-hashing]]
- [[hot-spots]]
- [[rebalancing-partitions]]
- [[request-routing]]
- [[client-side-sharding]]
- [[ambassador-pattern]]
- [[scalability]]
- [[scatter-gather-pattern]]
- [[tail-latency-amplification]]
- [[designing-distributed-systems]]
