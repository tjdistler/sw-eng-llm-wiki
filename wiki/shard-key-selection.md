# Shard Key Selection

**Summary**: Choosing which property of a request to feed into the sharding function. Burns argues that selecting the right shard key is "vital to designing your sharded system well" and that both over-generalising (grouping together non-equivalent requests) and over-specialising (splitting equivalent requests across shards) produce a bad sharding. The key must capture exactly the dimensions on which responses differ, and no more.

**Sources**: `raw/designing-distributed-systems/chapter-06-sharded-services.md`

**Last updated**: 2026-04-16

---

## What the sharding function is

A **sharding function** maps each request to the shard that should handle it (source: raw/designing-distributed-systems/chapter-06-sharded-services.md):

```
Shard = ShardingFunction(Req)
```

In practice, this is a hash function applied to some key derived from the request, reduced modulo the shard count:

```
Shard = hash(key(Req)) % N
```

The hash function must be:

- **Deterministic** — the same input always produces the same output, so the same request always lands on the same shard.
- **Uniform** — outputs are evenly distributed across the output range, so load spreads evenly across shards.

Modern language-provided hash functions satisfy both properties. Note that **process-local hash functions like Java's `Object.hashCode()` are unsafe** (different values in different processes) — this is the same caution DDIA makes in [[partitioning-strategies#Hash partitioning|its hash partitioning discussion]].

## The shard key is the interesting decision

The hash function is almost never where the design work happens. What matters is **what to hash** — the shard **key** extracted from the request.

Burns uses an HTTP request with three fields as the running example (source: raw/designing-distributed-systems/chapter-06-sharded-services.md):

- The timestamp of the request
- The client's source IP address
- The HTTP request path (e.g. `/some/page.html`)

The naïve choice — hash the whole request object — is wrong: the timestamp and IP make every request unique, so every request misses the cache.

### Option 1: `shard(request.path)` — too general

Hashing only the path groups all requests for the same URL onto one shard. This is great for a generic cache: two users asking for `/home.html` hit the same cache shard and share the result (source: raw/designing-distributed-systems/chapter-06-sharded-services.md).

But if the response depends on **client geography** (localised content, language), this is wrong: a French user and a US user land on the same shard and one of them gets the wrong language. The sharding function is treating non-equivalent requests as equivalent — a correctness bug, not just a performance one.

### Option 2: `shard(request.ip, request.path)` — too specific

Including the client IP means two French IPs now go to different shards — wasting cache capacity by storing the same French response multiple times. The function has drifted from sharding by "response variant" to sharding by "client identity." Throughput is fine but the cache hit rate suffers.

### Option 3: `shard(country(request.ip), request.path)` — just right

Derive the country from the IP, then use `(country, path)` as the key (source: raw/designing-distributed-systems/chapter-06-sharded-services.md). All French IPs map to the same shard for a given path; US IPs map to a (possibly) different shard for the same path.

> "Determining the appropriate key for your sharding function is vital to designing your sharded system well. Determining the correct shard key requires an understanding of the requests that you expect to see." (source: raw/designing-distributed-systems/chapter-06-sharded-services.md)

## The underlying principle

The shard key should capture **exactly the request dimensions that determine the response**, no fewer and no more:

- **Fewer**: distinct-response requests land on the same shard ⇒ correctness bug or serving stale content.
- **More**: equivalent-response requests land on different shards ⇒ cache-capacity waste, poor hit rate.

Burns's general-purpose HTTP-proxy example (the nginx consistent-hashing config at the end of the chapter) uses `$request_uri` — path + query string + fragment. This is the default when responses don't vary by user or location. Personalisation, language, or geo-aware systems must add the appropriate dimensions to the key (source: raw/designing-distributed-systems/chapter-06-sharded-services.md).

## Non-HTTP examples

Burns's sharded-game-world example (source: raw/designing-distributed-systems/chapter-06-sharded-services.md) uses a **player's in-world location** as the shard key, not any part of the network request. Because players far apart in the virtual world don't interact, location-based sharding keeps interacting players on the same machine and non-interacting players on different machines. This is the same principle — pick the dimension that determines response equivalence — applied to a context where the key isn't in the HTTP request at all.

## Relationship to existing wiki concepts

### Hash uniformity and partitioning strategies

The uniformity requirement maps directly onto [[partitioning-strategies#Hash partitioning|hash partitioning]]. The shard key equivalent in DDIA's vocabulary is the "partition key" — and the same hash-function concerns apply: avoid process-local hashes, use MD5 / FNV / similar, and expect uniformity to hold only if input keys are themselves distinct.

### Hot keys are a separate problem

Shard key selection assumes the key space is broad enough that requests distribute across many distinct keys. When one specific key gets a disproportionate share of requests (a viral photo, a celebrity user), no shard-key choice helps: the function correctly routes all those requests to the same shard. That is [[hot-spots]] at the database layer and [[hot-sharding]] at the service layer.

### Key choice and re-sharding cost

If a shard key later proves wrong (e.g. geography added to the product and the key didn't include it), fixing it requires redeploying with a new sharding function — which [[consistent-hashing|consistent hashing]] does *not* help with, because it is a different function entirely, not the same function with a changed shard count. Getting the shard key right up front is cheaper than changing it later.

## Related pages

- [[sharded-service-pattern]]
- [[sharded-cache]]
- [[consistent-hashing]]
- [[partitioning-strategies]]
- [[hot-spots]]
- [[hot-sharding]]
- [[request-routing]]
- [[client-side-sharding]]
- [[designing-distributed-systems]]
