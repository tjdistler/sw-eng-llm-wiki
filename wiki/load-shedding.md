# Load Shedding

**Summary**: The action a backend task takes when it cannot serve every request it receives: reject some requests quickly so that the ones it does accept can complete. SRE Chapter 21 treats shedding as the per-task safety valve that complements global mechanisms like [[per-customer-quotas]] and [[adaptive-throttling]]: even when both upstream defences work, a task can become locally overloaded by imperfect balancing, expensive queries, or neighbour interference, and needs its own last-resort defence. The shed-or-serve decision combines a [[utilization-signals|utilisation signal]] with the incoming request's [[request-criticality|criticality]]: low-criticality traffic is shed first at low utilisation, critical traffic is preserved until utilisation is very high.

**Sources**: `raw/site-reliability-engineering/chapter-21-handling-overload.md`, `raw/site-reliability-engineering/chapter-22-addressing-cascading-failures.md`

**Last updated**: 2026-04-17

---

## Why shedding is necessary

Chapter 21's closing restates the principle that motivates shedding (source: chapter-21-handling-overload.md):

> It's a common mistake to assume that an overloaded backend should turn down and stop accepting all traffic. However, this assumption actually goes counter to the goal of robust load balancing. We actually want the backend to continue accepting as much traffic as possible, but to only accept that load as capacity frees up. A well-behaved backend, supported by robust load balancing policies, should accept only the requests that it can process and reject the rest gracefully.

The alternatives to shedding are worse:

- **Accept everything.** The task queues up work it cannot complete; request latency climbs; eventually memory or thread limits are hit and the task crashes, taking all in-flight requests with it.
- **Refuse everything.** The task pretends to be dead, so [[weighted-round-robin|load balancing]] shifts traffic to peers — which may already be overloaded themselves, propagating failure. Cascading failure is exactly what shedding is designed to prevent.

The middle path — accept what the task can serve, reject the rest quickly — preserves the task's usefulness while avoiding death-spiral collapse.

## The shedding decision

Chapter 21 combines two inputs into the decision (source: chapter-21-handling-overload.md):

- The task's [[utilization-signals|utilisation signal]] (typically the executor load average).
- The incoming request's [[request-criticality|criticality]].

The policy shape: for each criticality, a utilisation threshold at which requests of that criticality start being rejected. Higher criticalities have higher thresholds. This produces a **graceful degradation curve** rather than a cliff: as the task gets busier, progressively higher-criticality traffic starts being shed.

At the extreme, even `CRITICAL_PLUS` traffic is shed — this is the response Chapter 21 calls "serve errors" in its opening. It's the worst case, not the design target.

## The chapter's explicit corollaries

Chapter 21 closes with two statements that sharpen what "graceful" shedding means (source: chapter-21-handling-overload.md):

> To state this simply: a backend task provisioned to serve a certain traffic rate should continue to serve traffic at that rate without any significant impact on latency, regardless of how much excess traffic is thrown at the task. As a corollary, the backend task should not fall over and crash under the load. These statements should hold true up to a certain rate of traffic — somewhere above 2x or even 10x what the task is provisioned to process.

Two concrete promises:

1. **Latency is preserved for served traffic** even under extreme excess. The task doesn't let its response times degrade for the requests it *does* serve; it simply serves fewer of them.
2. **The task survives** at 2-10x its provisioned load. Shedding is the mechanism that makes this possible — without it, the extra work would consume memory, thread handles, or other finite resources until something breaks.

Above some breakdown point (the chapter acknowledges the point exists and is hard to push higher) the task eventually does fail. But the goal is to push that breakdown point as high as possible.

## Rejecting cheaply

A rejection is not free, but it must be significantly cheaper than serving, or shedding itself becomes the load (source: chapter-21-handling-overload.md):

> When a customer is out of quota, a backend task should reject requests quickly with the expectation that returning a "customer is out of quota" error consumes significantly fewer resources than actually processing the request and serving back a correct response.

The implicit design requirement: the shedding path has to short-circuit as much of the request processing pipeline as possible — don't parse the body, don't look up the row, don't authenticate if you don't need to. Ideally the rejection happens before any expensive work begins.

For services where rejection is almost as expensive as serving (the RAM-lookup example Chapter 21 cites), even cheap rejection doesn't solve the problem. That is precisely the case that motivates [[adaptive-throttling]]: push the rejection back to the client so the backend doesn't see the request at all.

## Shedding's place in the Chapter 21 stack

Shedding is one layer in the overall defence:

1. **[[per-customer-quotas]]** prevent one customer from consuming everyone's capacity.
2. **[[adaptive-throttling]]** makes clients stop sending when they are being rejected.
3. **Load shedding** is the per-task local defence when the global mechanisms haven't caught a spike yet, or when the task is over-subscribed for reasons unrelated to any single customer.
4. **[[graceful-degradation]]** is the layer above shedding: where possible, serve a cheaper response instead of rejecting entirely.
5. **[[retry-budget|Retry budgets]]** cap the amplification that retries would otherwise cause once a task starts shedding.

The mechanisms compose; shedding alone is insufficient, but without it nothing else matters at the task level.

## Relationship to existing wiki concepts

### Shedding and [[graceful-degradation]]

Shedding and graceful degradation are complementary responses to the same condition. Shedding says "I can't serve this, reject it now." Graceful degradation says "I can serve a cheaper version of this." A mature service uses both: when a cheap response path exists, degrade; when it doesn't (or the task is too overloaded even for the cheap path), shed. The distinction is whether the caller gets something useful back.

### Shedding and [[rate-limiting]]

[[rate-limiting]] is shedding at the edge by rate, without looking at utilisation. Chapter 21's shedding is driven by *actual* resource state rather than a pre-configured cap. The two compose:

- Edge rate limits catch DoS and runaway clients early.
- Per-task shedding catches the cases where rate-limited traffic is still too much for this specific task right now.

### Shedding and Newman's [[circuit-breaker]]

A circuit breaker is shedding applied *by the caller* based on observed failure of a downstream. Chapter 21's shedding is applied *by the callee* based on observed utilisation of itself. Both drop traffic that the system is not currently able to handle, but they sit on opposite ends of the RPC and use different signals. A full Chapter-21-plus-Newman defence has both.

### Shedding and [[fault-tolerance]]

Shedding is a textbook [[fault-tolerance]] mechanism: the system survives overload by gracefully refusing the work it cannot do, instead of failing in a way that affects the work it *can* do. The general pattern is "partial degradation beats total failure"; shedding is how that principle is realised at the request-admission level.

### Shedding as cascade prevention (Chapter 22)

Chapter 22 reframes Chapter 21's shedding as a cascading-failure defence: without shedding, an overloaded task consumes memory and thread pool until it crashes, the load balancer shifts its traffic elsewhere, and peers experience the same overload and crash in turn (source: chapter-22-addressing-cascading-failures.md). Shedding is what breaks the domino effect at the single-task level — the task accepts what it can serve, rejects the rest quickly, survives, and peers see no additional load.

Chapter 22's "Instrument the server to reject requests when overloaded" prescription is shedding in its cascading-failure-prevention framing: the chapter lists it as the third priority (after load testing and graceful degradation) in the ordered list of overload defences. The chapter also notes that rejecting cheaply is essential — if rejection is nearly as expensive as serving, shedding itself becomes the load, and the task cannot stabilise.

The connection to [[queue-management]] is explicit in the chapter: limiting queue length is a form of shedding, rejecting requests that would otherwise queue past a threshold.

### Shedding and [[operational-overload]]

[[operational-overload]] is Chapter 11's human version of the same condition — an on-call rotation receiving more incidents than it can sustain. Giving back the pager is the human analogue of shedding: refuse the work you cannot do, so that the work you *do* pick up receives full attention. The structural parallel is intentional.

## Related pages

- [[handling-overload]]
- [[utilization-signals]]
- [[request-criticality]]
- [[graceful-degradation]]
- [[adaptive-throttling]]
- [[per-customer-quotas]]
- [[rate-limiting]]
- [[circuit-breaker]]
- [[fault-tolerance]]
- [[operational-overload]]
- [[cascading-failure]]
- [[queue-management]]
- [[site-reliability-engineering]]
