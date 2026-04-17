# Consistent Hashing

**Summary**: A technique originally designed for distributing load across internet-wide caches (CDNs) by using randomly chosen partition boundaries, avoiding the need for central control or distributed consensus. In practice, the term is misleading in a database context and "hash partitioning" is preferred.

**Sources**: `raw/designing-data-intensive-applications/chapter-06-partitioning.md`, `raw/designing-distributed-systems/chapter-03-ambassadors.md`, `raw/designing-distributed-systems/chapter-05-replicated-load-balanced-services.md`, `raw/designing-distributed-systems/chapter-06-sharded-services.md`

**Last updated**: 2026-04-16

---

## Origin and definition

Consistent hashing was defined by Karger et al. for evenly distributing load across a system of caches such as a content delivery network (CDN). The key idea is to use randomly chosen partition boundaries so that adding or removing a node only redistributes a small fraction of keys, without requiring central coordination or [[consensus|distributed consensus]].

The word "consistent" here has nothing to do with replica consistency (see [[eventual-consistency]]) or ACID consistency. It refers specifically to the property that most keys stay mapped to the same partition when the number of nodes changes.

## Why databases avoid the term

Although some database documentation still refers to "consistent hashing," the technique as originally defined does not work well for databases in practice (source: chapter-06-partitioning.md). The random partition boundaries can produce uneven data distribution, and the approach is rarely used as-is. Modern systems use fixed or dynamic partition counts with hash-based key assignment instead.

To avoid confusion, it is better to use the term **hash partitioning** when discussing database [[partitioning-strategies]].

## Relationship to rebalancing strategies

The "partitioning proportionally to nodes" strategy (used by Cassandra and Ketama) is the closest modern analogue to the original consistent hashing definition. New nodes randomly split a fixed number of existing partitions and take ownership of half of each split. This requires hash-based partitioning so boundaries can be drawn from the hash function's range. The randomization can produce unfair splits, but averaged over many partitions (Cassandra defaults to 256 per node), the result is reasonably fair. Cassandra (since 3.0) uses an alternative rebalancing algorithm that avoids unfair splits (source: chapter-06-partitioning.md). Newer hash functions can achieve a similar effect with lower metadata overhead.

See [[rebalancing-partitions]] for details on how this compares to fixed and dynamic partition counts.

## Consistent hashing in client-side sharding ambassadors

The memcached/Redis world continues to use consistent-hashing variants directly. Burns's Chapter 3 worked example (source: raw/designing-distributed-systems/chapter-03-ambassadors.md) deploys the **twemproxy** sharding ambassador in front of a three-shard Redis cluster with `distribution: ketama` — **ketama** is a well-known consistent-hashing scheme originally popularised by memcached clients. The ambassador applies the hash to each key and maps it to one of the configured shard servers; the application sees a single local Redis endpoint. See [[client-side-sharding]] and [[ambassador-pattern]].

## Consistent hashing and re-sharding a service

Burns's Chapter 6 of *Designing Distributed Systems* makes the re-sharding argument explicit in the service context (source: raw/designing-distributed-systems/chapter-06-sharded-services.md). Consider a [[sharded-service-pattern|sharded cache]] using the naive sharding function `hash(Req) % 10`. Scaling to 11 shards changes the function to `hash(Req) % 11`, which remaps *most* keys to a different shard. For a cache, that is "equivalent to a complete cache failure" — the miss rate spikes until the cache repopulates.

A consistent-hashing sharding function keeps that remapping down to roughly `#keys / #shards`, i.e. less than 10% of keys when scaling from 10 to 11 shards. That turns a catastrophic re-sharding into a tolerable one.

This is the same mathematical property as the CDN and session-affinity use cases below — applied this time to a sharded backend service, with re-sharding playing the role that adding or removing a node plays in CDNs. Ketama's popularity in the memcached / Redis world is precisely because those systems are sharded services where re-sharding has to be cheap.

### nginx as a consistent-hashing HTTP shard router

Burns's chapter also shows a vanilla nginx configuration acting as a consistent-hashing sharding proxy for HTTP (source: raw/designing-distributed-systems/chapter-06-sharded-services.md):

```
upstream backend {
  hash $request_uri consistent;
  server web-shard-1.web;
  server web-shard-2.web;
  server web-shard-3.web;
}
```

The `hash ... consistent` directive configures nginx's consistent-hashing module. `$request_uri` is the shard key — the full path plus query string plus fragment (see [[shard-key-selection]] for why this key is chosen). Adding a fourth backend remaps only ~25% of URLs rather than all of them.

## Consistent hashing for session affinity

The same minimum-remapping property is what makes consistent hashing the default choice for session stickiness in a [[replicated-load-balanced-service]]. When a load balancer assigns users to replicas via `hash(user) % N`, any change in `N` (adding or removing a replica) re-hashes almost every user, invalidating all in-memory caches and long-running sessions. A consistent-hashing scheme remaps only a small fraction of users, so warm caches and sessions largely survive scaling events (source: raw/designing-distributed-systems/chapter-05-replicated-load-balanced-services.md). This is conceptually the same CDN use case Karger et al. defined — users as "keys," replicas as "nodes" — rather than anything database-specific. See [[session-tracked-services]] for the full treatment and the caveats around IP hash vs cookie/header hash.

## Related pages

- [[partitioning-strategies]]
- [[partitioning]]
- [[rebalancing-partitions]]
- [[hot-spots]]
- [[client-side-sharding]]
- [[ambassador-pattern]]
- [[session-tracked-services]]
- [[replicated-load-balanced-service]]
- [[sharded-service-pattern]]
- [[shard-key-selection]]
- [[sharded-cache]]
