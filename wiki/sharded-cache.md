# Sharded Cache

**Summary**: Burns's primary worked example of the [[sharded-service-pattern]]. A caching tier placed between users and a backend service where each cache replica holds only a fraction of the keyspace, maximising the effective cache size at the cost of making each shard a single point of failure for its subset of keys. Contrasts with the replicated [[caching-layer]] of Chapter 5, where every replica held the same working set.

**Sources**: `raw/designing-distributed-systems/chapter-06-sharded-services.md`

**Last updated**: 2026-04-16

---

## Why a sharded cache

Chapter 5 covered the replicated [[caching-layer]]: Varnish sitting in front of an application tier, every replica caching the same content. That works when the working set fits in a single cache's memory. When it doesn't, every replica fights for the same small slice of the keyspace and the hit rate collapses.

The sharded cache is the fix. Each cache instance holds **unique** keys; together they cache a much larger fraction of the total working set (source: raw/designing-distributed-systems/chapter-06-sharded-services.md).

## The memory-utilisation argument

Burns works a specific example (source: raw/designing-distributed-systems/chapter-06-sharded-services.md):

- 200 GB of total possible cached results.
- Each cache has 10 GB RAM and serves 100 RPS.
- Expected load: 1,000 RPS.

You need 10 replicas to serve 1,000 RPS either way. The question is how much of the 200 GB they can actually cache.

| Deployment | Cache size | Coverage of working set |
|---|---|---|
| Replicated (Ch 5 pattern) | 10 × 10 GB where all replicas hold the same data ≈ **10 GB** | 5% |
| Sharded (Ch 6 pattern) | 10 × 10 GB of unique data = **100 GB** | 50% |

A tenfold increase in effective cache storage at the same operational cost. This is the entire economic case for sharding a cache.

The general rule: for caches, **memory utilisation scales with the number of shards**; for stateless serving, memory utilisation is independent of replica count. Mixing these concerns in a replicated cache wastes most of the memory you paid for. See [[caching-layer#Why not deploy the cache as a sidecar]] for the related sizing rule in the replicated setting.

## Role of cache criticality

Sharding makes cache failures more consequential than in the replicated case. Because each request is deterministically mapped to a specific shard, **if that shard fails, every request for those keys misses the cache until the shard is restored** (source: raw/designing-distributed-systems/chapter-06-sharded-services.md).

Burns frames the key operational question this way: "If the cache were to fail, what would the impact be for your users and your service?"

The answer depends on the **hit rate** — the percentage of requests that find data already cached.

### Hit rate as a capacity multiplier

Burns's RPS example (source: raw/designing-distributed-systems/chapter-06-sharded-services.md):

- Application tier: max 1,000 RPS before returning HTTP 500.
- Add a cache with 50% hit rate.
- Effective capacity: 2,000 RPS (half served from cache, half reaching the app).

If the cache fails, the system can still only serve 1,000 RPS. Rating the service at the full 2,000 RPS makes cache failure catastrophic. **Rating it at 1,500 RPS leaves enough headroom that half the cache can fail without cascading into application-tier overload.** This is the classic sharded-cache sizing discipline: capacity planning must include the degraded-mode post-shard-failure case.

### Hit rate as a latency reducer

Burns also shows the latency math (source: raw/designing-distributed-systems/chapter-06-sharded-services.md):

- Application-tier request: 100 ms.
- Cache hit: 10 ms.
- 25% hit rate.
- Weighted average: 0.25 × 10 + 0.75 × 100 = **77.5 ms**.

Unlike throughput, latency-oriented caches are more forgiving of shard failure: a shard outage just means some fraction of requests are slower than ideal — not that the system collapses. But in systems with tight request queues, even that slowdown can cause timeouts and pile-ups. Burns recommends load-testing both with and without the cache to understand the failure-mode impact.

## Upgrade and rollout penalty

A subtler consequence: **deploying a new version of a sharded cache temporarily loses capacity.** Unlike a replicated cache, where a new replica can warm up from peers, a sharded cache shard starts empty, and the keys it owns all miss until it warms up (source: raw/designing-distributed-systems/chapter-06-sharded-services.md).

Two responses:

- **Schedule rollouts during quiet traffic periods.** Works but constrains release cadence.
- **Replicate each shard.** See [[replicated-sharded-service]]: the shard becomes a [[replicated-load-balanced-service]] internally, and rollouts upgrade one replica at a time. Rollouts during peak traffic become safe.

## Hands-on: twemproxy + memcached on Kubernetes

Burns's worked example deploys memcached as a Kubernetes `StatefulSet` of three replicas, each with its own DNS name (`memcache-0.memcache`, etc.), fronted by a twemproxy ambassador that hashes each memcache key via `fnv1a_64` / `ketama` and routes to one of the three shards (source: raw/designing-distributed-systems/chapter-06-sharded-services.md).

The deployment mirrors the Chapter 3 sharded-Redis example ([[client-side-sharding]]) — it is the same pattern with a different backend protocol. The chapter provides both variants:

- **Per-pod ambassador.** Twemproxy listens on `127.0.0.1:11211`; every application pod runs its own twemproxy container.
- **Shared shard-router service.** Twemproxy listens on `0.0.0.0:11211`, runs as a multi-replica `Deployment`, and is fronted by a Kubernetes `Service`. Clients connect to the service's DNS name.

See [[sharded-service-pattern#Deployment variants: ambassador vs shared routing service]] for the trade-off.

## Relationship to existing wiki concepts

### Sharded cache vs replicated cache

[[caching-layer]] (Chapter 5) and this page describe two different deployments of the same high-level idea: put cache between users and the application. Choose based on working-set size:

- Working set fits in one cache's memory → **replicated** cache layer. Simpler; failures are trivial; all replicas cache everything.
- Working set exceeds one cache's memory → **sharded** cache. Higher effective capacity; failures hurt the specific keys on the failed shard.

### Sharded cache and DDIA partitioning

The sharded cache is a [[partitioning|partitioned]] datastore where the data happens to be ephemeral. All the DDIA partitioning concerns apply:

- [[partitioning-strategies]] — hash-partitioning (via the sharding function) is the default; key-range partitioning is rare for cache keys.
- [[hot-spots]] — one key getting a disproportionate share of requests is a hot shard; see [[hot-sharding]] for Burns's response.
- [[consistent-hashing]] — ketama is the classic consistent-hashing algorithm used here; minimises key remapping when shard count changes.
- [[rebalancing-partitions]] — re-sharding a cache is essentially a cache-flush event; see [[consistent-hashing]] for the mitigation.

### Sharded cache and Chapter 3 ambassadors

Burns's Chapter 3 already sharded Redis via an ambassador; Chapter 6 asks what the sharded service itself should look like. The two chapters are complementary: Chapter 3 is the client connecting to a sharded backend; Chapter 6 is the sharded backend being built (source: raw/designing-distributed-systems/chapter-06-sharded-services.md).

## Related pages

- [[sharded-service-pattern]]
- [[replicated-sharded-service]]
- [[hot-sharding]]
- [[shard-key-selection]]
- [[caching-layer]]
- [[client-side-sharding]]
- [[consistent-hashing]]
- [[partitioning]]
- [[partitioning-strategies]]
- [[hot-spots]]
- [[replicated-load-balanced-service]]
- [[response-time-percentiles]]
- [[designing-distributed-systems]]
