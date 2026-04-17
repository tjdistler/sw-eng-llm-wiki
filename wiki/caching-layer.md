# Caching Layer

**Summary**: A replicated, load-balanced HTTP cache tier placed in front of a web-serving tier to absorb repeated requests without round-tripping to the application. Burns frames it as another instance of the [[replicated-load-balanced-service]] pattern — stateless, scalable, health-probed — but with sizing that deliberately differs from the application tier: **few large** cache replicas rather than many small ones, so memory isn't wasted duplicating cached content across replicas.

**Sources**: `raw/designing-distributed-systems/chapter-05-replicated-load-balanced-services.md`, `raw/designing-distributed-systems/chapter-06-sharded-services.md`

**Last updated**: 2026-04-16

---

## Why add a cache

Even a stateless application can be expensive to run per-request — it may hit a database, render a template, aggregate several backend responses. Putting a caching HTTP proxy between the user and the application lets repeated requests for the same content be served from memory without the backend ever seeing them (source: raw/designing-distributed-systems/chapter-05-replicated-load-balanced-services.md).

Burns walks through the canonical form: **Varnish**, an open-source web cache, sitting in front of the stateless dictionary-server tier from earlier in the chapter. When two users ask for `/dog`, one request goes to the application; the other is served from Varnish's in-memory cache.

## Why not deploy the cache as a sidecar

The simplest cache deployment is the [[sidecar-pattern]]: put a Varnish sidecar in every application pod, sharing the network namespace and caching responses locally (source: raw/designing-distributed-systems/chapter-05-replicated-load-balanced-services.md).

This is simple but wrong for most real deployments. Two coupled disadvantages:

1. **Forced co-scaling.** Cache replicas scale with application replicas. You cannot have few caches and many app servers, even if that is the right ratio.
2. **Memory duplication kills the hit rate.** Every cache replica stores its own copy of every hot page. Ten app pods with 1 GB caches can cache 1 GB of total content (ten copies of the same working set), not 10 GB. Two pods with 5 GB caches can hold 5 GB of working set — a much larger fraction of the real request distribution, with a correspondingly higher hit rate.

The hit rate directly determines the cache's value: every miss costs a full backend request. Burns's sizing rule is therefore **few large cache replicas, many small application replicas**. These have different optima and should be deployed as separate tiers.

## The cache as a separate replicated tier

The right deployment is a second [[replicated-load-balanced-service]] tier — Varnish replicas sitting behind their own load balancer, forwarding misses to the application tier's load balancer (source: raw/designing-distributed-systems/chapter-05-replicated-load-balanced-services.md).

In Kubernetes:

- A `Deployment` runs N Varnish replicas (Burns uses 2) with a memory-allocation matching a `requests.memory` quota (`malloc,2G` matched against `memory: 2Gi`).
- A `ConfigMap` carries the `default.vcl` file that points Varnish at the application tier's internal `Service` DNS name as its backend.
- A `Service` exposes the Varnish Deployment behind a load balancer.

Clients now resolve the Varnish `Service`; misses go through to the application `Service`. Both tiers are replicated, load-balanced, health-probed, independently scalable, and independently rollable. The whole stack is the replicated-load-balanced pattern applied twice, composed by pointing one tier's backend at the next tier's service name.

The app tier is often still sized wide-and-small — many replicas with modest memory each — because many runtimes (e.g. NodeJS) can only use one core per process and multi-replica deployment is how you get parallelism. Sizing for the cache tier and the app tier is therefore genuinely different, which is exactly why they want to be separate tiers.

## The session-tracking trap

Putting a cache tier in front of a [[session-tracked-services|session-tracked]] web tier is tricky. If the application-tier load balancer uses IP-based affinity, every request now arrives with the cache replica's IP — not the user's. With only two cache replicas, the application tier collapses to two source IPs and affinity falls apart (source: raw/designing-distributed-systems/chapter-05-replicated-load-balanced-services.md).

The fix: switch to application-level affinity (cookies or headers) once a cache layer is in play. Varnish can be configured to pass the cookie through and the application-tier load balancer reads it to pick a replica. See [[session-tracked-services]] for the full treatment.

## Beyond caching: what the layer can also do

Because the caching tier is an HTTP reverse proxy, Burns uses it to host additional edge-layer capabilities that benefit from being near the user (source: raw/designing-distributed-systems/chapter-05-replicated-load-balanced-services.md):

- **[[rate-limiting]]** — reject or slow down excess requests before they reach the application.
- **[[ssl-termination]]** — handled in practice by a third layer (nginx) because Varnish itself doesn't do SSL; see that page for the full three-tier composition.

These are all pluggable modules on mature reverse proxies (Varnish, nginx). Treating the cache layer as a reverse-proxy edge rather than a pure cache is a standard pattern.

## Relationship to existing wiki concepts

### Caching and the base replicated pattern

The cache layer is the first concrete example in Chapter 5 of composing replicated load-balanced services into stacks. It is structurally the same pattern as the app tier — a Deployment + a Service + health probes — applied to a different workload with different sizing. See [[replicated-load-balanced-service]].

### Caching and the sidecar alternative

The chapter's sidecar-vs-separate-tier discussion is a worked example of a design trade-off between the [[sidecar-pattern]] and the [[replicated-load-balanced-service]] at tier level. Both are viable; the sizing asymmetry between cache and application pushes the decision toward separate tiers. This is a useful case study on when *not* to reach for a sidecar.

### Caching and the ambassador pattern

Where a sharding [[client-side-sharding|sharding ambassador]] sits in front of its backend service per-pod to give the application a `localhost` endpoint, a cache tier lives as its own shared tier between clients and the application. Both absorb backend-topology complexity away from the application; they differ in whether the indirection is per-pod or fleet-wide.

### Caching and response-time percentiles

A high cache hit rate improves tail latency dramatically — misses pay the full backend cost, hits are fast. [[response-time-percentiles]] is the right frame for evaluating the cache's effect: the cache usually helps p50 modestly and p95/p99 a lot, because the worst-case hot-content requests go from expensive backend trips to in-memory reads.

### When replicated isn't enough: sharded caches

Chapter 5's replicated cache is the right default when the **working set fits in a single cache replica's memory**. Every replica caches the same hot pages; hit rate is high and failures are transient. But once the working set exceeds one replica's memory, the replicated pattern wastes memory: all replicas contend for the same small slice of the keyspace.

Chapter 6 introduces the **sharded** cache as the alternative (source: raw/designing-distributed-systems/chapter-06-sharded-services.md). Each cache replica holds a distinct partition of the keyspace; together they cache a much larger fraction of total content. Burns's worked example: 10 × 10 GB replicated caches cache 10 GB of unique content; 10 × 10 GB sharded caches cache 100 GB. The cost: losing a shard means missing on the keys that shard owned until it is restored. See [[sharded-cache]] for the full treatment, [[sharded-service-pattern]] for the general pattern, and [[replicated-sharded-service]] / [[hot-sharding]] for how to combine the two to get both large cache size and resilience.

### Caching and legacy modernization

Dropping a cache tier in front of a slow legacy service is one of the cheapest performance interventions available and requires no changes to the service. It fits the same "improve without modifying" discipline as [[sidecar-pattern|sidecars]] and [[adapter-pattern|adapters]] at Part I.

## Related pages

- [[replicated-load-balanced-service]]
- [[session-tracked-services]]
- [[rate-limiting]]
- [[ssl-termination]]
- [[sidecar-pattern]]
- [[health-probes]]
- [[scalability]]
- [[scaling-approaches]]
- [[response-time-percentiles]]
- [[ambassador-pattern]]
- [[sharded-cache]]
- [[sharded-service-pattern]]
- [[replicated-sharded-service]]
- [[hot-sharding]]
- [[designing-distributed-systems]]
