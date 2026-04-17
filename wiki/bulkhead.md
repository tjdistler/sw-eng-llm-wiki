# Bulkhead

**Summary**: A stability pattern (Michael Nygard, *Release It!*) that partitions resources — thread pools, connection pools, instances, whole services — so that a failure or exhaustion in one partition cannot consume resources belonging to another. Named after a ship's bulkheads, which compartmentalise the hull so a single breach does not sink the vessel.

**Sources**: `raw/monolith-to-microservices/chapter-05-growing-pains.md` (for the broader "isolate services" principle and the pointer to *Release It!*; the word *bulkhead* itself does not appear in any file under `raw/`).

**Last updated**: 2026-04-16

---

## A note on sources

The bulkhead pattern is from Michael Nygard's *Release It!* (Pragmatic Bookshelf, 2018), which Newman recommends at the end of his own resilience section (source: raw/monolith-to-microservices/chapter-05-growing-pains.md). *Release It!* is not in `raw/`, and the word *bulkhead* does not appear anywhere in our raw sources. What Newman *does* say, directly, is: "Isolating services more from each other can help, perhaps including the introduction of asynchronous communication to avoid temporal coupling" (source: raw/monolith-to-microservices/chapter-05-growing-pains.md). That sentence is the highest-specificity bulkhead-adjacent material available to this wiki. The naval metaphor, three-layer taxonomy, Hystrix details, and sizing rules below are synthesis from widely-known public material — not direct quotes.

## The naval metaphor

A ship's bulkhead is a watertight partition across the hull. If one compartment floods, the bulkhead keeps the water out of the others; the ship lists but does not sink. The pattern name preserves the motivation: compartmentalise so one breach does not become total loss.

In software, the "water" is resource exhaustion — threads stuck on a slow call, connections held open, memory consumed by a runaway workload — and the "bulkhead" is whatever mechanism prevents that exhaustion from spreading to unrelated workloads.

## The failure it prevents

Without bulkheads, a single slow downstream dependency can take out an entire caller, even for unrelated requests. The classic scenario:

1. Service A calls service B (slow/failing) and service C (healthy) from the same thread pool.
2. Threads calling B stall on timeout.
3. Thread pool fills with stuck calls to B.
4. Requests that only need C cannot get a thread; A's calls to C fail even though C is fine.
5. A's failure rate climbs for all its consumers. B's outage has become A's outage.

Newman describes this class of failure as "cascading failures and back pressure" and recommends isolation as one of several mitigations (source: raw/monolith-to-microservices/chapter-05-growing-pains.md). The bulkhead breaks step 3 → 4: if B's calls use a separate pool from C's calls, B's pool exhausts but C's remains available.

## Concrete forms

Bulkheads can be implemented at increasingly coarse granularities:

### Per-dependency thread pools

The classic Hystrix pattern: each outbound dependency gets its own bounded thread pool. Calls to B cannot consume threads reserved for C. When B's pool is saturated, further calls to B fail fast (which is a nice handoff into a [[circuit-breaker]]) while calls to C continue normally.

Per-dependency pools also cap the *maximum* blast radius per dependency: if B has 20 threads, at most 20 of A's in-flight requests can be stuck on B at any time.

### Per-dependency connection pools

Similar idea one layer down: separate HTTP or database connection pools per downstream, so a downstream that accepts connections but never responds cannot hold open every connection A has.

### Per-tenant or per-workload instances

In multi-tenant systems, run separate service instances per tenant (or per tenant class). A runaway tenant saturates their own instance but cannot affect others. This is the "cell" pattern AWS and others use for noisy-neighbour isolation.

### Process-per-tenant

Further still: a dedicated OS process per tenant. Memory leaks, segfaults, unbounded GC pauses are all contained within the tenant's process.

### Separate services

The coarsest form: extract a problematic workload into its own microservice. The service boundary is a bulkhead at the deployment level — the extracted service can crash, scale independently, or be rolled back without touching the rest of the system.

## Relationship to microservices

A microservice is itself a kind of bulkhead. Extracting functionality into its own deployable process with its own resource budget is an instance of the bulkhead principle at the process-and-network level. But the reverse is not true: just because you have [[microservices]] does not mean you have bulkheads *inside* each service. A service calling five dependencies from one thread pool has no bulkheads, even though it lives on the microservice side of the architectural line.

The distinction matters: a microservice architecture creates the *opportunity* for isolation, but does not guarantee it (see [[robustness-vs-resilience]] for Newman's broader framing, which is anchored in raw/monolith-to-microservices/chapter-05-growing-pains.md). Bulkheads are one of the explicit design moves that turn the opportunity into the outcome.

## Bulkhead vs timeout vs circuit breaker

The three Nygard patterns work in concert; each handles a different slice of the failure envelope. Newman groups timeouts, circuit breakers, and "isolating services more from each other" as distinct but cooperating moves in his Chapter 5 mitigation list (source: raw/monolith-to-microservices/chapter-05-growing-pains.md):

| Pattern | Scope | Role in the failure cascade |
|---|---|---|
| [[timeouts]] | A single call | Bounds how long one call can stall before giving up |
| [[circuit-breaker]] | A dependency | Stops making further calls once a dependency is observably broken |
| Bulkhead (this page) | A resource pool | Contains the blast radius while the breaker is tripping and beyond |

A useful sequencing: **timeout** fires to end the stuck call; the failure feeds the **circuit breaker**'s counter; the breaker opens and future calls skip the downstream. Meanwhile the **bulkhead** ensures that during the few seconds before the breaker trips, only *this* dependency's pool is affected, not the caller's entire thread pool. Bulkhead *contains* while the breaker *detects*.

## Bulkheads are about isolation, not detection

A subtle point: bulkheads don't know anything is wrong. They just prevent one workload from consuming resources belonging to another. Detection is the circuit breaker's job, timing is the timeout's job, graceful degradation is the fallback's job. The bulkhead is a purely structural protection that is in effect whether or not anything is actually failing.

That independence is what makes bulkheads so useful as a defence-in-depth layer. Even if you get the circuit breaker's thresholds wrong or the timeout's value wrong, the bulkhead still limits damage.

## Sizing bulkheads

A bulkhead that is too large provides weak isolation; one that is too small starves normal operation. Common starting points:

- Thread-pool size = expected concurrency × (1 + expected transient spike).
- Connection-pool size = p99 concurrency for that dependency.
- Cell size (tenants per instance) = small enough that losing one cell is not a headline incident.

Sizing is application-specific and iterated on real incident data, not guessed up front.

## Relationship to other wiki concepts

### And robustness at scale

Isolation — the category bulkheads fall into — sits firmly on the **robustness** side of the [[robustness-vs-resilience]] distinction: a designed-in mechanism that handles a known failure mode. Newman's Chapter 5 lists "isolating services" alongside timeouts, circuit breakers, and running multiple copies as concrete robustness moves (source: raw/monolith-to-microservices/chapter-05-growing-pains.md). See [[robustness-and-resiliency-at-scale]] for the broader framing.

### And rate limiting

[[rate-limiting]] is a bulkhead at the ingress layer: capping a single client's rate prevents that client from consuming capacity belonging to all the others. The mechanism is different (count tokens over a window) but the intent — resource partitioning to contain blast radius — is the same.

### And isolation in service meshes

[[service-mesh]] data planes (Envoy, Linkerd-proxy) typically implement per-upstream connection-pool limits as part of their default configuration — the outbound sidecar is a natural place to enforce a bulkhead because every outbound call already passes through it. Control-plane policy can set different limits per upstream service.

### And the pod boundary

The [[pod]] itself is a lightweight bulkhead: a container's resource limits cap how much CPU, memory, and file-descriptors it can consume, so a pod running away does not starve other pods on the same node. Node-level isolation (evictions, taints, limits) is the operating-system-layer version of the pattern.

## Libraries

Bulkheads are implemented in:

- **Hystrix** (deprecated) — per-dependency thread pools were the pattern's most visible surface.
- **Resilience4j** — modular `Bulkhead` and `ThreadPoolBulkhead` components.
- **Polly** (.NET) — `Bulkhead` policy alongside its other resilience policies.
- Service-mesh sidecars — connection-pool limits, pending-request limits, outlier detection.

As with [[circuit-breaker]], mesh-based bulkheads move the policy out of application code and into platform configuration, which is usually the right trade-off in a polyglot microservice estate.

## Related pages

- [[timeouts]]
- [[circuit-breaker]]
- [[microservices]]
- [[robustness-and-resiliency-at-scale]]
- [[robustness-vs-resilience]]
- [[rate-limiting]]
- [[service-mesh]]
- [[pod]]
- [[fault-tolerance]]
- [[partial-failures]]
