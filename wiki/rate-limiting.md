# Rate Limiting

**Summary**: Capping the rate of requests a client can make, enforced at the edge (typically by an HTTP reverse proxy like Varnish or nginx) to defend against denial-of-service — whether malicious, accidental misconfiguration, or a runaway load test pointed at production by mistake. Burns frames it as a standard pluggable feature of the [[caching-layer]] tier in the replicated-load-balanced serving pattern.

**Sources**: `raw/designing-distributed-systems/chapter-05-replicated-load-balanced-services.md`

**Last updated**: 2026-04-16

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
