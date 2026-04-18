# Testing for Cascading Failures

**Summary**: SRE Chapter 22's prescription that services be deliberately load-tested to and beyond their breaking point, so that the failure mode is characterised before a production incident forces the characterisation. The chapter's testing strategy has three arcs: **test to failure and beyond** (how does the service behave after it breaks? can it recover automatically?), **test popular clients** (do they back off on errors, or pound the service harder?), and **test noncritical backends** (does their unavailability degrade the service gracefully, or does it cause critical-path failures?). Production tests are needed because synthetic load has different characteristics from real traffic.

**Sources**: `raw/site-reliability-engineering/chapter-22-addressing-cascading-failures.md`

**Last updated**: 2026-04-17

---

## The chapter's framing

From Chapter 22 (source: chapter-22-addressing-cascading-failures.md):

> The specific ways in which a service will fail can be very hard to predict from first principles. This section discusses testing strategies that can detect if services are susceptible to cascading failures. You should test your service to determine how it behaves under heavy load in order to gain confidence that it won't enter a cascading failure under various circumstances.

The core argument: cascading behaviour is emergent and system-specific. No amount of design review tells you how your particular service fails under load. The only reliable way to know is to push it there and observe.

## Test until failure and beyond

The canonical load-testing discipline from the chapter (source: chapter-22-addressing-cascading-failures.md):

> Understanding the behavior of the service under heavy load is perhaps the most important first step in avoiding cascading failures. Knowing how your system behaves when it is overloaded helps to identify what engineering tasks are the most important for long-term fixes; at the very least, this knowledge may help bootstrap the debugging process for on-call engineers when an emergency arises.

The target behaviour:

> As load increases, a component typically handles requests successfully until it reaches a point at which it can't handle more requests. At this point, the component should ideally start serving errors or degraded results in response to additional load, but not significantly reduce the rate at which it successfully handles requests. A component that is highly susceptible to a cascading failure will start crashing or serving a very high rate of errors when it becomes overloaded; a better designed component will instead be able to reject a few requests and survive.

The signature of a cascading-prone service: "total failure" shape on the graph. The signature of a resilient service: "plateau" shape — throughput tops out and stays there even as offered load grows.

## Gradual vs impulse load

The chapter calls out that ramp shape matters (source: chapter-22-addressing-cascading-failures.md):

> Because of caching effects, gradually ramping up load may yield different results than immediately increasing to expected load levels. Therefore, consider testing both gradual and impulse load patterns.

Gradual load gives caches time to warm, JITs time to optimise, and connection pools time to stabilise. Impulse load — from 0 to full in a second — is the traffic shape that mimics a datacenter failover or a CDN-triggered stampede. The two shapes test different failure modes.

## Recovery testing

The chapter's two specific questions about post-overload behaviour:

> - If a component enters a degraded mode on heavy load, is it capable of exiting the degraded mode without human intervention?
> - If a couple of servers crash under heavy load, how much does the load need to drop in order for the system to stabilize?

Both questions matter for real-incident response. The first determines whether a brief overload produces a lasting degraded state. The second quantifies the "drop to 1,000 QPS to recover from 11,000 QPS" phenomenon from [[server-overload]] — knowing the drop-rate required is the difference between a five-minute recovery and a fifty-minute one.

## Stateful services and concurrency bugs

The chapter adds a specific warning for stateful services (source: chapter-22-addressing-cascading-failures.md):

> If you're load testing a stateful service or a service that employs caching, your load test should track state between multiple interactions and check correctness at high load, which is often where subtle concurrency bugs hit.

Race conditions, lock contention, and write-write conflicts that don't appear under synthetic uniform traffic tend to emerge under real-traffic-shaped load. Testing at correctness — not just throughput — catches this.

## Per-component testing

The chapter prescribes testing breaking points per-component (source: chapter-22-addressing-cascading-failures.md):

> Keep in mind that individual components may have different breaking points, so load test each component separately. You won't know in advance which component may hit the wall first, and you want to know how your system behaves when it does.

The service's effective capacity is determined by its weakest component. Testing end-to-end finds *one* number (the overall capacity) but not *which* component is responsible. Component-level tests find the bottleneck, which is where engineering attention should focus.

## Production testing

Synthetic tests have limits. Chapter 22's production-test recommendations (source: chapter-22-addressing-cascading-failures.md):

> If you believe your system has proper protections against being overloaded, consider performing failure tests in a small slice of production to find the point at which the components in your system fail under real traffic. These limits may not be adequately reflected by synthetic load test traffic, so real traffic tests may provide more realistic results than load tests, at the risk of causing user-visible pain.

The three named production tests:

> - Reducing task counts quickly or slowly over time, beyond expected traffic patterns
> - Rapidly losing a cluster's worth of capacity
> - Blackholing various backends

These test cascade-adjacent scenarios explicitly: sudden capacity loss (drain trigger), cluster-scale failure (process-death trigger), and downstream unavailability.

The caveat:

> Be careful when testing on real traffic: make sure that you have extra capacity available in case your automatic protections don't work and you need to manually fail over.

Production testing assumes the defences *work*. When they don't, manual mitigation has to kick in fast. The test blueprint needs a rollback plan.

## Test popular clients

A distinct dimension of cascade risk (source: chapter-22-addressing-cascading-failures.md):

> Understand how large clients use your service. For example, you want to know if clients:
>
> - Can queue work while the service is down
> - Use randomized exponential backoff on errors
> - Are vulnerable to external triggers that can create large amounts of load (e.g., an externally triggered software update might clear an offline client's cache)

A service cannot fully defend itself from clients that retry aggressively, synchronise their retries, or launch traffic stampedes from external triggers. Testing means **staging failures against the real clients** (or the largest of them) and observing the client-side response. A client that back-off-and-retries cleanly is a good citizen; a client that amplifies an outage into a bigger one needs a code change before the service's defences matter.

The external-trigger case is particularly insidious: a software update rolled out to many offline clients all at once will cause them to come online, cache-empty, at the same moment. No per-server shedding discipline defends against a million clients simultaneously requesting the same resource.

## Test noncritical backends

The third arc (source: chapter-22-addressing-cascading-failures.md):

> Test your noncritical backends, and make sure their unavailability does not interfere with the critical components of your service. For example, suppose your frontend has critical and noncritical backends. Often, a given request includes both critical components (e.g., query results) and noncritical components (e.g., spelling suggestions). Your requests may significantly slow down and consume resources waiting for noncritical backends to finish.

The warning extends to blackholed backends:

> In addition to testing behavior when the noncritical backend is unavailable, test how the frontend behaves if the noncritical backend never responds (for example, if it is blackholing requests). Backends advertised as noncritical can still cause problems on frontends when requests have long deadlines. The frontend should not start rejecting lots of requests, running out of resources, or serving with very high latency when a noncritical backend blackholes.

A noncritical backend that hangs indefinitely (because of bimodal latency or a deadlock) can consume the frontend's thread pool even though the work it does is optional. Testing that the frontend stays healthy when the noncritical backend blackholes is as important as testing that it stays healthy when the noncritical backend returns errors.

## Relationship to existing wiki concepts

### Testing for cascading failures and [[testing-for-reliability]]

Chapter 17's testing discipline lives at the smaller scale — [[unit-tests]], [[integration-tests]], [[system-tests]]. Chapter 22's testing lives at the load-and-failure scale, and connects to Chapter 17's [[stress-tests|stress testing]] and [[statistical-testing-techniques|chaos-engineering-adjacent]] categories specifically. The same philosophy — testing is the mechanism for quantifying confidence in change — extends from the unit level to the service-wide cascading-failure level.

### Testing for cascading failures and [[stress-tests]]

[[stress-tests]] (Chapter 17) "find the catastrophic-failure cliff before production does." That is precisely what Chapter 22 prescribes, with the addition of post-overload-recovery behaviour and the component-level test granularity.

### Testing for cascading failures and [[canary-test]]

[[canary-test|Canary rollouts]] are a specific production-testing discipline that catches the *new rollouts* trigger. A good canary tests the new binary against real traffic in a way that exposes cascade behaviour before the rollout reaches full production. See the mathematical framing in [[canary-test]] for the exponential-rollout rationale.

### Testing for cascading failures and [[statistical-testing-techniques]]

Chaos engineering — Chaos Monkey, Gremlin, Netflix's Simian Army — is the industry incarnation of Chapter 22's production-test prescriptions. The overlap is substantial: blackhole backends, kill tasks, drain capacity. Chapter 22 frames these as deliberate exercises; chaos engineering frames them as a permanent cultural practice.

### Testing for cascading failures and [[load-parameters]]

Kleppmann's [[load-parameters]] discussion — picking the right metric to characterise load — is the prerequisite for load testing. A test that scales the wrong parameter (pure QPS when the real bottleneck is payload size) won't find the real breaking point. See [[queries-per-second-pitfalls]] for the specific warning that QPS is often the wrong parameter.

### Testing for cascading failures and [[capacity-planning]]

Load testing is explicitly a [[capacity-planning]] input. The chapter calls this out:

> Load testing also reveals where the breaking point is, knowledge that's fundamental to the capacity planning process. It enables you to test for regressions, provision for worst-case thresholds, and to trade off utilization versus safety margins.

A capacity plan without measured breaking-point data is a guess; one with breaking-point data is a calibration.

### Testing for cascading failures and [[dirt|DiRT exercises]]

Google's DiRT (Disaster Recovery Testing) exercises are the cross-organisational form of Chapter 22's production-testing directives: deliberately fail a datacenter, a network, or a service, and observe whether the rest of the system degrades gracefully. DiRT extends the single-service testing discipline into cross-team readiness.

## Related pages

- [[cascading-failure]]
- [[server-overload]]
- [[cascading-failure-triggers]]
- [[addressing-ongoing-cascading-failure]]
- [[capacity-planning]]
- [[stress-tests]]
- [[statistical-testing-techniques]]
- [[canary-test]]
- [[testing-for-reliability]]
- [[queries-per-second-pitfalls]]
- [[load-parameters]]
- [[site-reliability-engineering]]
