# Rate Limiting

**Summary**: Capping the rate of requests a client can make, enforced at the edge (typically by an HTTP reverse proxy like Varnish or nginx) to defend against denial-of-service — whether malicious, accidental misconfiguration, or a runaway load test pointed at production by mistake. Burns frames it as a standard pluggable feature of the [[caching-layer]] tier in the replicated-load-balanced serving pattern.

**Sources**: `raw/designing-distributed-systems/chapter-05-replicated-load-balanced-services.md`, `raw/site-reliability-engineering/chapter-21-handling-overload.md`

**Last updated**: 2026-04-17

---

## Why rate limit

Denial-of-service doesn't require a motivated attacker. The more common cases Burns flags (source: raw/designing-distributed-systems/chapter-05-replicated-load-balanced-services.md):

- **A developer misconfiguring a client** — an infinite retry loop, a mistaken poll interval, a fan-out query that multiplies beyond what was intended.
- **A site-reliability engineer accidentally running a load test against a production installation.**

These look indistinguishable from a DoS to the service. A rate limit at the edge protects the application and the database behind it from being brought down by one bad deploy on the client side.

Rate limiting is therefore a *standard hygiene feature* for any public API, not only a security control.

## Where to enforce it

Burns's recommendation is the edge layer of the [[replicated-load-balanced-service]] stack — the same tier that runs the HTTP reverse proxy for caching and SSL termination (source: raw/designing-distributed-systems/chapter-05-replicated-load-balanced-services.md). Varnish, for example, ships with a **throttle module** that can rate-limit by:

- Source IP address.
- Request path.
- Whether the user is logged in (authenticated users get a higher quota).

This placement is convenient: the edge tier already parses HTTP, already knows the source IP (or the real IP carried in `X-Forwarded-For`), and runs independently of application-tier scaling.

## Authenticated vs anonymous limits

A good practice Burns highlights: **a small rate limit for anonymous access, a larger one for authenticated users** (source: raw/designing-distributed-systems/chapter-05-replicated-load-balanced-services.md). Two benefits:

1. **Accountability.** Authenticated requests are attributable. If a user is generating unusual load you can tell them to stop, revoke their key, or investigate their integration.
2. **Attacker friction.** Mounting a serious attack at the higher authenticated rate requires obtaining many distinct identities, which is a much higher bar than spoofing IPs.

This is a general pattern: raise the quota in exchange for accountability, not in exchange for a secret.

## The client contract: 429 and `X-RateLimit-Remaining`

Over-limit clients need to be told clearly what happened. The standard HTTP response code is `429 Too Many Requests` (source: raw/designing-distributed-systems/chapter-05-replicated-load-balanced-services.md).

Clients that behave well usually want to *avoid* hitting the limit, not just recover after it. The convention — there is no formal standard — is to return current quota state in headers on every response, not just on rejections. Burns notes the common variant `X-RateLimit-Remaining`; other APIs also return `X-RateLimit-Limit` (total quota) and `X-RateLimit-Reset` (when the window resets).

A well-designed client reads these headers and backs off proactively rather than driving itself into 429s.

## Rate limiting and the wider pattern

The rate-limit module is one of several reasons Burns puts Varnish or nginx in front of the application tier rather than exposing the application directly (source: raw/designing-distributed-systems/chapter-05-replicated-load-balanced-services.md). Other edge-tier features composed alongside:

- **[[caching-layer|Caching]]** — pluggable cache logic absorbs repeated reads.
- **[[ssl-termination]]** — offload TLS from the application tier.
- **Access logging, request rewriting, IP allowlists.**

All are feature modules on a replicated, load-balanced HTTP reverse-proxy tier. Adding rate limiting is a configuration change to an already-present tier, not a new deployment.

## Relationship to existing wiki concepts

### Rate limiting and fault tolerance

Rate limiting is a specific instance of load shedding — choosing which requests to reject when load exceeds safe capacity, rather than letting the whole system fail. It complements the other [[fault-tolerance]] mechanisms (circuit breakers, time-outs, bulkheads) Newman catalogues under [[robustness-and-resiliency-at-scale]].

### Rate limiting and the edge proxy

The edge proxy is itself a [[replicated-load-balanced-service]]: many reverse-proxy replicas behind a load balancer, each enforcing the limit. For the limit to be consistent across replicas, the counter state must be shared — usually via a shared store (Redis) or approximated by partitioning clients across replicas consistently. Simple per-instance counters are fine for modest traffic but drift under scale.

### Rate limiting and API design

A published rate-limit contract — which headers, which status code, how the quota is scoped — is part of an API's interface. Clients depend on it; changing it is a breaking change in the sense of [[breaking-changes]].

### Rate limiting and monitoring

Rate-limit decisions are a strong signal to log and monitor: a spike in 429s often precedes or accompanies a real incident, whether on the client side or in an abuse scenario. See [[monitoring-and-observability]].

## Internal rate limiting: per-customer quotas and adaptive throttling

SRE Chapter 21 describes the internal-services version of rate limiting, which differs from Burns's public-API-edge version in two important ways (source: chapter-21-handling-overload.md):

- **CPU, not QPS.** Internal quotas are expressed in **CPU seconds per second** rather than requests per second. The [[queries-per-second-pitfalls|argument against QPS as a capacity metric]] applies especially to internal services, where the request mix changes as client services ship new versions. A CPU-denominated quota is stable across client evolution in a way a QPS-denominated one is not.
- **Global, not per-instance.** The limit is enforced against aggregated *cross-datacenter* usage, pushed as per-task effective limits. Edge rate limiters typically enforce per-instance rates and accept modest inconsistency; Google's internal quota system computes a globally aggregated view in real time.

See [[per-customer-quotas]] for the mechanism and [[adaptive-throttling]] for the client-side cooperation that stops clients from continuing to hammer a backend that is rejecting them. The layering is explicit: Burns's edge rate limiting catches abusive and runaway *external* clients; Chapter 21's per-customer quotas catch misbehaving *internal* clients; per-task [[utilization-signals|load shedding]] catches what both miss when local conditions change faster than either can react.

## Rate limiting's place in the Chapter 21 stack

Chapter 21's overall defence layers rate limiting at three different granularities:

| Layer | Mechanism | Enforcer | Measure |
|---|---|---|---|
| Edge | [[rate-limiting]] (this page) | HTTP reverse proxy | QPS by IP / user / path |
| RPC ingress | [[per-customer-quotas]] | Backend task | CPU-sec/sec per customer |
| Client-side | [[adaptive-throttling]] | Client task | Accept ratio |
| Per-task | [[load-shedding]] | Backend task | [[utilization-signals|Utilisation]] |

Each layer catches cases the others cannot. Edge limits stop DoS before it reaches the application; internal quotas stop one internal customer starving another; client-side throttling stops an over-quota client from wasting backend CPU on rejections; per-task shedding stops a locally overloaded task from dying regardless of why it became overloaded.

## Related pages

- [[caching-layer]]
- [[ssl-termination]]
- [[replicated-load-balanced-service]]
- [[fault-tolerance]]
- [[robustness-and-resiliency-at-scale]]
- [[monitoring-and-observability]]
- [[breaking-changes]]
- [[circuit-breaker]]
- [[bulkhead]]
- [[designing-distributed-systems]]
- [[handling-overload]]
- [[per-customer-quotas]]
- [[adaptive-throttling]]
- [[load-shedding]]
- [[utilization-signals]]
- [[queries-per-second-pitfalls]]
