# Slow Startup and Cold Caching

**Summary**: Processes are slower at responding to requests immediately after starting than they will be in steady state. SRE Chapter 22 identifies this as a specific cascading-failure amplifier: a service restarting after a crash comes up with cold caches, uninitialised connections, unoptimised JIT code, and a fraction of its steady-state throughput. If the crash was caused by load, the fresh process faces that same load with reduced capacity and fails almost immediately — the very condition Chapter 22 names when discussing why a service healthy at 10,000 QPS may need load dropped to 1,000 QPS to recover. The key distinction Chapter 22 draws: **latency caches** let the service handle expected load from a cold start (more slowly); **capacity caches** do not — the service cannot sustain its expected load on an empty cache. Capacity caches are hard dependencies masquerading as optimisations.

**Sources**: `raw/site-reliability-engineering/chapter-22-addressing-cascading-failures.md`

**Last updated**: 2026-04-17

---

## Why startup is slow

From Chapter 22 (source: chapter-22-addressing-cascading-failures.md):

> Processes are often slower at responding to requests immediately after starting than they will be in steady state. This slowness can be caused by either or both of the following:
>
> - **Required initialization**: Setting up connections upon receiving the first request that needs a given backend
> - **Runtime performance improvements in some languages, particularly Java**: Just-In-Time compilation, hotspot optimization, and deferred class loading

Plus the cache effect: a process that serves most requests from cache in steady state serves most requests from the canonical store when the cache is empty, and the canonical store is much more expensive. Chapter 22 (source: chapter-22-addressing-cascading-failures.md):

> Other services might employ caches to keep a user's state in RAM... In steady-state operation with a warm cache, only a few cache misses occur, but when the cache is completely empty, 100% of requests are costly.

## When cold caching hits

Chapter 22's four scenarios (source: chapter-22-addressing-cascading-failures.md):

- **Turning up a new cluster.** Empty caches on every task; external requests will hit the canonical store.
- **Returning a cluster to service after maintenance.** Caches are stale, and keyspace ownership may have shifted during the drain.
- **Task restarts.** After a binary push, a crash, or scheduled eviction, each task comes up with an empty cache.

The first and third are the most common. The second is subtler — caches may be present but invalid, which can be worse than empty (invalidating and refilling is work the service pays twice).

## The latency cache vs capacity cache distinction

Chapter 22 draws what is arguably the chapter's most important line (source: chapter-22-addressing-cascading-failures.md):

> It's important to note the distinction between a latency cache versus a capacity cache: when a latency cache is employed, the service can sustain its expected load with an empty cache, but a service using a capacity cache cannot sustain its expected load under an empty cache. Service owners should be vigilant about adding caches to their service, and make sure that any new caches are either latency caches or are sufficiently well engineered to safely function as capacity caches. Sometimes caches are added to a service to improve performance, but actually wind up being hard dependencies.

The distinction:

| Kind | Steady-state role | Cold-start behaviour |
|---|---|---|
| Latency cache | Makes responses faster | Service still serves, just slowly |
| Capacity cache | Provides throughput the backend can't alone | Service fails under normal load |

A service designed around a latency cache is resilient: lose the cache, degrade, recover. A service designed around a capacity cache has a hidden dependency on the cache being warm; lose the cache, and the service is down until the cache is refilled — but the cache can only be refilled by traffic the service is now unable to serve.

This distinction is what separates a cache that *helps* from a cache that *lies about capacity*.

## Why cold caches fuel cascades

The cascading-failure connection is immediate: Chapter 22's memorable "10,000 QPS healthy, dropped to 1,000 QPS needed to recover" example depends on this mechanism. When tasks crash under load and restart, they face the full production traffic with fresh caches. Requests fall through to backends at much higher rates than steady state. The backends, already struggling, see still more load. Tasks fail to fill caches before being overloaded again. The crash-restart loop has no attractor that leads back to healthy operation; only aggressive load shedding breaks it.

## Mitigations

Chapter 22 lists several (source: chapter-22-addressing-cascading-failures.md):

### Overprovision

> Overprovision the service.

Have enough headroom that cold tasks can handle their share of load (slowly) while warming up. A service provisioned exactly at 100% of steady-state load has no margin for a cold start.

### Move caching to a separate binary

> It may be worthwhile to move caching from a server to a separate binary like memcache, which also allows cache sharing between many servers, albeit at the cost of introducing another RPC and slight additional latency.

When caches live in a separate tier, task restarts don't cold-start the cache. The trade-off is the extra RPC hop — more latency in the steady state, but dramatic improvement in resilience to task restarts.

### Employ general overload defences

> Employ general cascading failure prevention techniques. In particular, servers should reject requests when they're overloaded or enter degraded modes, and testing should be performed to see how the service behaves after events such as a large restart.

Specifically: [[load-shedding]] so a cold task rejects what it can't handle, [[graceful-degradation]] so a cold task serves something cheaper while it warms up.

### Gradual traffic ramp

> When adding load to a cluster, slowly increase the load. The initially small request rate warms up the cache; once the cache is warm, more traffic can be added. It's a good idea to ensure that all clusters carry nominal load and that the caches are kept warm.

The lesson here applies to many situations: adding a cluster that immediately takes full production traffic is a cold-start disaster waiting to happen. Ramping traffic gradually lets caches warm and JITs optimise before the cluster is stressed.

## The slow-startup side

JIT-based runtimes (Java, .NET CLR) have specific cold-start costs unrelated to caching:

- The JIT has not yet compiled hot paths to native code; methods run interpreted for a while.
- Class loading is deferred; first-hit class loads pay disk/network time.
- Garbage collection ergonomics haven't calibrated to the workload.

These produce a period — sometimes minutes for complex Java services — where the process is running but at substantially reduced throughput. The mitigations are similar: gradual traffic ramp, overprovisioning, and tooling like AOT compilation (GraalVM native-image, .NET ReadyToRun) that reduces the JIT warmup cost.

## Relationship to other wiki concepts

### Cold caching and [[addressing-ongoing-cascading-failure]]

The "restart servers" remedy in Chapter 22's immediate-steps section has a specific cold-cache caveat: "your actions may amplify an existing cascading failure if the outage is actually due to an issue like a cold cache." Restarting a wedged Java process is good; restarting a task whose crash was caused by cold-cache load is often bad — it just restores the same condition.

### Cold caching and [[canary-test]]

One of the reasons Chapter 17's [[canary-test]] works is that it ramps traffic gradually to a new binary, so cold-start effects become visible before full production traffic exposes them. Canary is the testing discipline that answers the Chapter 22 gradual-ramp recommendation.

### Cold caching and [[cold-start-warm-start]]

Bellemare's [[cold-start-warm-start]] page covers the FaaS-specific form of cold start: a function that hasn't been invoked recently pays a container-launch and connection-setup cost. The Chapter 22 framing is the server-side analogue — the same physics, applied to long-running services rather than ephemeral function invocations.

### Cold caching and [[caching-layer]]

Burns's [[caching-layer]] pattern (Varnish as an HTTP caching tier) is a *capacity cache* in Chapter 22's terminology if the backend can't handle full cache-miss rates. The sizing question "how big must the backend be?" turns on whether losing the cache is a degradation or an outage.

### Cold caching and [[failover]]

[[failover]] to a cold replica has cold-start cost by definition. Fast failover with warm replicas is much better than fast failover to a cold start; Chapter 22's [[intra-layer-communication]] section specifically warns about primary-to-secondary proxying designs that increase work under load.

### Cold caching and [[sharded-cache]]

Burns's [[sharded-cache]] page develops the memory-utilisation math that Chapter 22 implicitly relies on. The "hit rate as capacity multiplier" framing in Burns is exactly what Chapter 22 means by "capacity cache" — the service's effective capacity is not the backend's raw capacity, but the backend's capacity times (1 / (1 - hit_rate)). Lose the cache and the capacity shrinks by that factor.

## Related pages

- [[cascading-failure]]
- [[addressing-ongoing-cascading-failure]]
- [[load-shedding]]
- [[graceful-degradation]]
- [[canary-test]]
- [[cold-start-warm-start]]
- [[caching-layer]]
- [[sharded-cache]]
- [[failover]]
- [[intra-layer-communication]]
- [[site-reliability-engineering]]
