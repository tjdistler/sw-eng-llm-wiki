# Circuit Breaker

**Summary**: A stability pattern (Michael Nygard, *Release It!*) that short-circuits calls to a failing downstream dependency so that a slow or broken service does not consume upstream resources and propagate failure. The breaker watches the failure rate, opens when it crosses a threshold, and after a cool-down probes with a single request before closing again.

**Sources**: `raw/monolith-to-microservices/chapter-05-growing-pains.md`

**Last updated**: 2026-04-16

---

## The problem

A slow downstream dependency is more dangerous than a fast failure. When service A calls service B and B is sick, A's threads block on B's response. New requests arriving at A pile up behind the blocked threads; A's thread pool exhausts; A stops serving *anything*, not just requests that needed B. Back pressure propagates to A's callers, and the original B outage becomes a region-wide outage. Newman names this as a consequence of service growth: "as the number of services increases, and the number of service calls increase, you'll become more and more vulnerable to resiliency issues. The more interconnected your services are, the more likely you'll suffer from things like cascading failures and back pressure" (source: raw/monolith-to-microservices/chapter-05-growing-pains.md).

Newman phrases the operational rule verbatim: "do I know the way in which this call might fail? Second, if the call does fail, do I know what I should do?" (source: raw/monolith-to-microservices/chapter-05-growing-pains.md). A bare synchronous call has no answer to either question; a circuit breaker supplies a sharp answer to both.

## A note on sources

Newman (*Monolith to Microservices*, Chapter 5) treats circuit breakers as one item in a short resilience checklist and points readers to Michael Nygard's *Release It!* (Pragmatic Bookshelf, 2018) for depth (source: raw/monolith-to-microservices/chapter-05-growing-pains.md). *Release It!* is the canonical primary source for the pattern but is not in `raw/`, so the three-state machine, thresholds, and library catalogue below are synthesis from widely-known public material — not direct quotes from a source file in this wiki.

## Nygard's three-state machine

The pattern is from Michael Nygard's *Release It!* (Pragmatic Bookshelf; Newman's recommended deeper reference — see the [[#a-note-on-sources|note on sources]] above). The breaker is a state machine wrapped around each outbound dependency:

| State | Behaviour | Transition trigger |
|---|---|---|
| **Closed** | Calls pass through normally. Failures are counted. | Failure rate crosses threshold → **Open**. |
| **Open** | Calls fail immediately without contacting the downstream. The caller sees a fast error. | Cool-down timer elapses → **Half-open**. |
| **Half-open** | A single probe request is permitted through. | Probe succeeds → **Closed**. Probe fails → **Open** (timer restarts). |

The closed→open transition is what protects the upstream: once the breaker trips, further calls fail in microseconds instead of stalling on a timeout. The half-open probe is what allows automatic recovery without a human restarting the service.

### Typical thresholds

There is no universal configuration — the right numbers depend on the downstream's failure profile and the caller's tolerance. Common starting points:

- Trip when more than *N* failures occur in *M* seconds, or when the rolling error rate exceeds a percentage (e.g., 50% of the last 20 calls).
- Cool-down for 10–60 seconds before the first probe.
- Tune by looking at real incident data rather than guessing.

### What counts as a failure?

Not just exceptions. Timeouts, non-2xx HTTP responses, and sometimes slow successes (p99 above a budget) should all count. Conversely, 4xx client errors usually should *not* trip the breaker — they indicate a bad request, not a failing downstream.

## Interaction with timeouts

The circuit breaker and [[timeouts]] are a pair. Newman treats them as one move: "Using sensible time-outs can avoid resource contention with slow downstream services, and in conjunction with patterns like circuit breakers, you can start failing fast to avoid problems with back pressure" (source: raw/monolith-to-microservices/chapter-05-growing-pains.md). Each solves a different half of the slow-call problem:

- **Timeouts** bound how long a single call can block. Without a timeout, a hung downstream holds a caller thread forever.
- **Circuit breakers** prevent further calls once the pattern of timeouts is established. Without a breaker, every new call still burns a timeout's worth of resources before failing.

The usual sequencing: timeouts detect the slow call; timeouts feed the breaker's failure counter; the breaker opens and future calls skip the timeout entirely. A short timeout without a breaker still wastes thread-pool capacity on every attempt; a breaker without a timeout never accumulates the failure signal it needs to trip.

## Newman's wider resilience checklist

Newman places circuit breakers inside a wider set of moves for a service receiving too many slow calls. From Chapter 5: "Isolating services more from each other can help, perhaps including the introduction of asynchronous communication to avoid temporal coupling… Running multiple copies of services can help with instances dying, as can a platform that can implement [[desired-state-management|desired state management]] (which can ensure that services get restarted if they crash)" (source: raw/monolith-to-microservices/chapter-05-growing-pains.md). Circuit breakers address synchronous resource contention; async messaging, redundancy, and orchestrator-level restart handle the failure modes that a breaker does not.

## Isolation is complementary, not redundant

Three resilience patterns sit next to each other in Nygard's and Newman's catalogues, and each handles a different failure shape:

| Pattern | What it does | When it helps |
|---|---|---|
| [[timeouts]] | Bounds the duration of a single call | Slow call |
| Circuit breaker (this page) | Skips calls once failure rate is high | Sustained downstream outage |
| [[bulkhead]] | Partitions resources so one workload cannot starve another | Cross-workload contamination |
| [[rate-limiting]] | Caps inbound request rate at the edge | DoS / runaway client |

A production system typically uses all four: rate limiting at the edge, bulkheads to isolate thread pools per downstream, circuit breakers around each outbound dependency, and timeouts on every call. Each layer's protection is weakest on its own; they compose into something useful. (Newman's Chapter 5 names timeouts, circuit breakers, and isolation as complementary; the defence-in-depth framing is widely shared in the pattern literature that Newman points to — see the [[#a-note-on-sources|note on sources]].)

## Fallback behaviour

When the breaker is open, the caller needs a plan for "what happens now". Options, in rough order of desirability:

- **Graceful degradation**: serve a cached or stale value, return a default, show a "we couldn't personalise this page" banner.
- **Queue for later**: write the request to a durable queue, process when the downstream recovers. Good for writes that tolerate eventual consistency.
- **Fail fast to the caller**: return an error immediately so the caller can retry or surface a message to the user. Better than hanging.

The pattern's benefit is partly that the open breaker *forces* the design conversation about fallback. A bare synchronous call hides the question; the breaker makes it explicit.

## Libraries and platforms

Well-known implementations:

- **Netflix Hystrix** — the canonical Java library; popularised the pattern in the microservice era. Now in maintenance mode; Netflix migrated off it internally.
- **Resilience4j** — JVM-era successor to Hystrix; functional, lightweight, modular (breakers, retries, bulkheads, rate limiters in separate modules).
- **Polly** — the .NET equivalent; combines breakers with retries, fallbacks, and timeouts in a fluent DSL.
- **Envoy / Istio / Linkerd** — [[service-mesh]] data planes implement circuit-breaking at the sidecar proxy, so application code does not need to depend on a library. This moves the policy to infrastructure the platform team controls.

Mesh-based breakers are a natural fit for a polyglot microservice estate: a single control-plane configuration applies the same failure semantics to every service regardless of its language or framework.

## Relationship to other wiki concepts

### And the serving tier

Burns's Chapter 5 [[replicated-load-balanced-service]] stack does not name circuit breaking explicitly, but the same failure shape motivates load-balancer health-probe dropping: an unhealthy replica is effectively "circuit-broken" by the load balancer until probes succeed again. See [[health-probes]].

### And the saga

In a multi-service workflow implemented as a [[saga]], a circuit breaker on an outbound call can determine whether to trigger a compensating action or to queue the step for later. The breaker provides the fast binary signal — "this dependency is unavailable" — that the saga's orchestration logic can react to.

### And robustness vs resilience

Newman places circuit breakers firmly on the **robustness** side of the [[robustness-vs-resilience]] distinction: they handle a known, anticipated failure mode. He puts this bluntly in the same section: "resiliency is more than just implementing a few patterns. It's about a whole way of working—building an organization that not only is ready to handle the unforeseeable problems that will inevitably crop up, but also evolves working practices as necessary" (source: raw/monolith-to-microservices/chapter-05-growing-pains.md). The resilience side — learning from incidents, evolving the configuration, running game days — is what keeps the breaker's thresholds useful over time.

## Related pages

- [[timeouts]]
- [[bulkhead]]
- [[rate-limiting]]
- [[robustness-and-resiliency-at-scale]]
- [[robustness-vs-resilience]]
- [[service-mesh]]
- [[fault-tolerance]]
- [[health-probes]]
- [[saga]]
- [[partial-failures]]
- [[desired-state-management]]
