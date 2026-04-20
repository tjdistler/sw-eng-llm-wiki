# Handling Overload

**Summary**: SRE Chapter 21 (Alejandro Forero Cuervo) is the companion to Chapter 20's [[datacenter-load-balancing|datacenter balancing]]: even with perfect balancing, some part of the system will eventually be overloaded, and every layer of the stack needs its own response so the system degrades gracefully rather than collapsing. The chapter develops eight cooperating mechanisms — drop [[queries-per-second-pitfalls|QPS as a capacity metric]] in favour of CPU, set [[per-customer-quotas|per-customer CPU quotas]], layer [[adaptive-throttling|client-side throttling]] on top, classify requests by [[request-criticality|criticality]], shed load locally based on [[utilization-signals]], return [[graceful-degradation|degraded responses]] when possible, bound [[retry-budget|retries]], and account for [[connection-level-load|connection-level load]].

**Sources**: `raw/site-reliability-engineering/chapter-21-handling-overload.md`

**Last updated**: 2026-04-17

---

## The thesis

Chapter 21 opens with a bluntly operational framing (source: chapter-21-handling-overload.md):

> At the end of the day, it's best to build clients and backends to handle resource restrictions gracefully: redirect when possible, serve degraded results when necessary, and handle resource errors transparently when all else fails.

The chapter's closing restates the same point from the other direction: an overloaded backend should **not** turn down and stop accepting traffic; it should continue accepting as much traffic as it can serve and reject the rest cleanly. The goal is a service that remains useful up to 2-10x its provisioned traffic rate rather than falling over at 1.01x.

The consequence is that overload handling is *not a single mechanism*. It is a cooperating stack, with each layer sized to catch the cases the layers above and below miss.

## The three failure modes the chapter defends against

Chapter 21 frames each mechanism as a defence against one of three failure modes (source: chapter-21-handling-overload.md):

1. **A misbehaving customer** consumes resources that belong to everyone else. Defence: [[per-customer-quotas]], plus [[adaptive-throttling]] so the client stops sending once it is out of quota.
2. **A task becomes locally overloaded** even though its customers are within quota — because traffic has shifted, or the task is small, or [[weighted-round-robin|balancing]] isn't perfect. Defence: [[utilization-signals]] plus [[load-shedding]] driven by [[request-criticality|criticality]].
3. **Retries amplify a transient problem into a sustained one**. Defence: [[retry-budget|per-request and per-client retry budgets]], plus the "overloaded; don't retry" response that propagates up stack layers.

The closing admission is important: all three defences can be defeated at sufficient load, and the ultimate escape valve is [[graceful-degradation|degraded responses]] — and if that fails too, error responses, which are still preferable to a crashed task.

## The eight mechanisms

Chapter 21 develops eight mechanisms, each catalogued on its own page:

- [[queries-per-second-pitfalls]] — why modelling capacity as QPS breaks down at Google scale; use CPU (or available resources directly) instead. The "cost of a request" as normalised CPU time.
- [[per-customer-quotas]] — provision the backend for negotiated usage, set per-customer CPU limits that may sum to more than the fleet has, compute real-time global usage, push effective limits to each task.
- [[adaptive-throttling]] — client-side self-regulation using the `max(0, (requests − K × accepts) / (requests + 1))` formula; typical `K = 2`; the client shares half the work of rejection even in the worst case.
- [[request-criticality]] — four values (`CRITICAL_PLUS`, `CRITICAL`, `SHEDDABLE_PLUS`, `SHEDDABLE`) propagated automatically through the RPC stack; criticality is orthogonal to latency and QoS; set at the entry point, overridden only where necessary.
- [[utilization-signals]] — task-local utilisation (typically CPU) drives per-task overload protection; the **executor load average** (smoothed count of ready threads) as Google's preferred signal; rejection thresholds per criticality.
- [[load-shedding]] — what happens when utilisation is too high for a given criticality: reject the request; higher criticalities tolerate higher thresholds.
- [[graceful-degradation]] — serving *something* instead of nothing: a partial search corpus, a local stale cache, a simpler response. The layer above [[load-shedding]] when shedding is unavoidable but a cheaper response is possible.
- [[retry-budget]] — per-request budget of 3 attempts; per-client ratio of at most 10% retries; the retry-counter histogram at the backend that turns "task overloaded" into "overloaded; don't retry" when most tasks are overloaded; the "only retry at the layer immediately above" rule that avoids combinatorial retry explosion.
- [[connection-level-load]] — the CPU and memory cost of maintaining and churning connections; the health-check-dominates-work pathology at large fan-in; the batch-proxy fuse pattern for bursty batch jobs.

## The integration argument

Chapter 21's closing is the integration thesis: none of these mechanisms is sufficient on its own, but together they produce a system that degrades gracefully under severe overload (source: chapter-21-handling-overload.md).

- Without [[per-customer-quotas]], one customer can starve another; with quotas alone, the backend burns CPU rejecting out-of-quota requests.
- Without [[adaptive-throttling]], rejection itself becomes the load; with throttling alone, a task still has no local defence when its clients are within quota but the task got a spike.
- Without [[utilization-signals]] and [[load-shedding]], a task can't defend itself; without [[request-criticality]], shedding can't prefer important work over unimportant work.
- Without [[retry-budget|retry budgets]], a small subset of overloaded tasks becomes a datacenter-wide outage via 3x request amplification; without the "don't retry" signal, the retry budget itself is insufficient when the *whole* datacenter is overloaded.
- Without [[connection-level-load]] accounting, a batch job's connection storm can overload tasks whose request-handling capacity is fine.
- Without [[graceful-degradation]], the best a healthy system can do under extreme load is serve errors; with degradation, it can still serve something useful.

The mechanisms compose by design. Each is the defence for the exact case the others don't cover.

## Relationship to existing wiki concepts

### Chapter 21 and Chapter 20

[[datacenter-load-balancing|Chapter 20]] is about *spreading* work evenly across backends; Chapter 21 is about *what each backend does when spreading isn't enough*. They are complementary: good balancing reduces the rate at which any task becomes overloaded, and good overload handling ensures that when balancing fails (as it eventually must), the task's response is graceful rather than catastrophic. The closing of Chapter 21 makes this explicit — individual tasks need their own protection because distributed-state propagation is always imperfect.

### Chapter 21 and Chapter 22

The chapter closes by pointing at Chapter 22 on cascading failures: left unchecked, local overload propagates, because failing tasks increase load on remaining tasks, which then also fail. The Chapter 21 mechanisms are the preconditions that keep local overload from cascading — they are the "pressure-relief valves" that make each layer of the stack independent. See [[cascading-failure]] for the Chapter 22 hub and the extended catalogue of design-level disciplines ([[queue-management]], [[retry-amplification]], [[latency-and-deadlines]], [[bimodal-latency]], [[slow-startup-and-cold-caching]], [[intra-layer-communication]]) that Chapter 22 adds on top of Chapter 21's per-task mechanisms.

### Chapter 21 and Newman's robustness moves

Newman's [[robustness-and-resiliency-at-scale|resilience checklist]] names [[timeouts]], [[circuit-breaker|circuit breakers]], [[bulkhead|bulkheads]], and [[rate-limiting]] as the core robustness patterns. Chapter 21 covers the same territory at a deeper level of specificity:

- [[rate-limiting]] → [[per-customer-quotas]] (server-side) + [[adaptive-throttling]] (client-side)
- [[circuit-breaker]] → [[adaptive-throttling]] (probabilistic rather than binary) + the "overloaded; don't retry" signal (classical circuit-break behaviour at the retry layer)
- [[bulkhead]] → [[per-customer-quotas]] is a bulkhead across customers; [[utilization-signals]] is a bulkhead around an individual task's CPU
- [[timeouts]] → not Chapter 21's subject directly, but the precondition for [[retry-budget|retries]] to have a well-defined failure signal to count

Chapter 21 is what these patterns look like when built into the RPC framework rather than as a per-service library layer.

### Chapter 21 and [[request-criticality]]

Criticality deserves special mention as Google's solution to the "which request gets rejected" problem. Newman's robustness patterns leave this implicit — a circuit breaker doesn't care whether the call was important. Chapter 21 makes priority a first-class part of the RPC envelope and propagates it automatically, which means every shed-vs-serve decision has a semantically meaningful input rather than being "first in, first dropped."

## Related pages

- [[queries-per-second-pitfalls]]
- [[per-customer-quotas]]
- [[adaptive-throttling]]
- [[request-criticality]]
- [[utilization-signals]]
- [[load-shedding]]
- [[graceful-degradation]]
- [[retry-budget]]
- [[connection-level-load]]
- [[datacenter-load-balancing]]
- [[weighted-round-robin]]
- [[rate-limiting]]
- [[circuit-breaker]]
- [[bulkhead]]
- [[cascading-failure]]
- [[site-reliability-engineering]]
