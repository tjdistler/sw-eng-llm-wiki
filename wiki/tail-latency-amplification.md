# Tail Latency Amplification

**Summary**: In any system where one user request fans out into N parallel backend calls and the response must wait for all of them, the overall latency is bounded below by the **slowest** of the N calls. High percentiles of the backend distribution therefore determine typical percentiles of the user-facing distribution — often by orders of magnitude. The same compounding applies to availability. This is the defining performance pathology of the [[scatter-gather-pattern]].

**Sources**: `raw/designing-distributed-systems/chapter-07-scattergather.md`, `raw/designing-data-intensive-applications/chapter-01-reliable-scalable-and-maintainable-applications.md`

**Last updated**: 2026-04-16

---

## The core arithmetic

Suppose a single backend has a p99 latency of 2 seconds — meaning 1 request in 100 is slow (source: raw/designing-distributed-systems/chapter-07-scattergather.md). Seen from one user's perspective that is a perfectly tolerable SLA. But what happens when a single user request has to consult N such backends in parallel and wait for all of them before returning?

The user sees the slow path whenever *any one* of the N calls is slow. The probability that all N calls are fast is `0.99^N`; the probability that at least one is slow is `1 - 0.99^N`:

| Fan-out N | P(all N fast) = 0.99^N | P(at least one slow) |
|---:|---:|---:|
| 1 | 0.990 | 1% |
| 5 | 0.951 | 5% |
| 10 | 0.904 | 10% |
| 100 | 0.366 | 63% |
| 1000 | 4.3 × 10⁻⁵ | 99.996% |

Burns's framing: the backend's p99 of 2 s becomes the **scatter/gather system's p95** at 5 leaves, and by 100 leaves is essentially guaranteed that every user request sees a 2-second slow leaf (source: raw/designing-distributed-systems/chapter-07-scattergather.md).

The rare tail of the backend becomes the typical experience of the user.

## Why this is called "amplification"

The latency that a single request in isolation would hit 1% of the time is the latency a fanned-out request hits a much larger fraction of the time. The distribution's shape is **amplified** upward — percentiles that were outliers become norms. DDIA uses the same term for the same mechanism whenever a single end-user request fans out to multiple backend calls (source: raw/designing-data-intensive-applications/chapter-01-reliable-scalable-and-maintainable-applications.md).

## The straggler problem

A related framing from Burns's chapter: every scatter/gather call has a **straggler**, the slowest leaf. The user's latency is the straggler's latency. Stragglers come from ordinary sources of variation — noisy neighbours competing for resources, GC pauses, TCP retransmissions, disk I/O hiccups, context switches — and they cannot be eliminated, only made statistically less painful.

Because stragglers are probabilistic, scattering to more leaves makes it more likely that *at least one* is currently striking a bad moment, which is the straggler problem's restatement of the amplification arithmetic above (source: raw/designing-distributed-systems/chapter-07-scattergather.md).

## Availability amplification

The same compounding applies to per-leaf failures. If each leaf has a 1% chance of failing on any given request and the system has 100 leaves, the probability that at least one leaf fails is `1 - 0.99^100 ≈ 63%` — effectively, every request fails unless each leaf is itself replicated (source: raw/designing-distributed-systems/chapter-07-scattergather.md).

This is why the robust form of scatter/gather always pairs with leaf replication — see [[scatter-gather-pattern]] and [[replicated-sharded-service]].

## Consequences for system design

Burns draws three explicit conclusions (source: raw/designing-distributed-systems/chapter-07-scattergather.md):

1. **Parallelism does not always speed things up**, because of per-leaf overhead that grows with leaf count.
2. **Parallelism does not always speed things up**, because of the straggler problem.
3. **The 99th percentile matters more than in other systems** — every user request becomes many subrequests, so the tail of the subrequest distribution *is* the main distribution.

The operational implication is that a scatter/gather service's leaf tier must be engineered for **consistent** performance, not just average or median performance. Median p99 alignment is table stakes; p999 alignment is where the engineering investment lands.

## Mitigations

### Leaf replication and hedged requests

Running each leaf as a [[replicated-load-balanced-service]] lets the root pick the fastest replica and ignore stragglers. Systems like Google's internal search fleet go further and issue **hedged requests** — send the request to two replicas, take whichever returns first, cancel the other. Hedging costs extra work but dramatically compresses the tail at the cost of doubled load.

Burns's chapter does not cover hedging explicitly, but the foundation it recommends — replicating each leaf — makes it straightforward to layer on. See [[scatter-gather-pattern]] for the broader reliability story.

### Bounded leaf count

Choosing a modest N rather than maximising parallelism directly limits how far the tail can amplify. At some leaf count, the benefit from more parallelism is smaller than the cost from tail amplification; beyond that point, more leaves make the system slower. See [[scatter-gather-pattern]].

### Per-leaf p99 budgets

Because the user-facing p50 is determined by backend p99-ish behaviour at fan-out levels of a few dozen, an explicit SLO on the leaf tier's p99 (not just its mean) is the lever. DDIA's treatment: [[response-time-percentiles]].

### Approximate gather — timeout and move on

Some systems tolerate missing a leaf's contribution and return an approximate answer when the gather phase times out. Search engines often do this: a query over a large sharded index may return slightly incomplete results under high load rather than blocking on a straggler. This requires the aggregation to degrade gracefully when inputs are incomplete.

## Relationship to existing wiki concepts

### DDIA's original framing

[[response-time-percentiles]] covers tail latency amplification as a general mechanism — any microservice call chain, any page rendered from many backend calls. Burns's contribution is to make it the **central** performance concern of a named serving pattern where the fan-out is by construction the whole point.

### Head-of-line blocking

A closely related but distinct pathology: when a backend is limited in how many requests it can process in parallel (CPU cores, threads), a burst of slow requests will hold up subsequent fast requests waiting in queue. [[response-time-percentiles]] discusses it; it combines multiplicatively with fan-out amplification on the leaf side of a scatter/gather system.

### Load parameters

A scatter/gather system has two loadish parameters that matter together: requests per second reaching the root, **and** fan-out — the mean number of leaves contacted per request. The system's performance envelope depends on their product, not just the first. See [[load-parameters]].

## Related pages

- [[scatter-gather-pattern]]
- [[response-time-percentiles]]
- [[replicated-load-balanced-service]]
- [[replicated-sharded-service]]
- [[sharded-service-pattern]]
- [[load-parameters]]
- [[fault-tolerance]]
- [[scalability]]
- [[designing-distributed-systems]]
