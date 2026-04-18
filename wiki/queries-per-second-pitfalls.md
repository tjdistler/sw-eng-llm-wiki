# Queries Per Second Pitfalls

**Summary**: SRE Chapter 21's opening argument against modelling service capacity as "queries per second" (or any static proxy like "keys read per request"). Different queries have vastly different resource costs, and the ratio of cost to QPS changes with client mix, time of day, software version, and feature flags. Google's preferred alternative is to measure capacity directly in available resources — typically **CPU** — and to normalise the "cost of a request" as CPU-time across hardware generations.

**Sources**: `raw/site-reliability-engineering/chapter-21-handling-overload.md`

**Last updated**: 2026-04-17

---

## Why QPS is a moving target

Chapter 21's indictment is direct (source: chapter-21-handling-overload.md):

> Modeling capacity as "queries per second" or using static features of the requests that are believed to be a proxy for the resources they consume (e.g., "how many keys are the requests reading") often makes for a poor metric. Even if these metrics perform adequately at one point in time, the ratios can change. Sometimes the change is gradual, but sometimes the change is drastic.

The reasons the ratio moves:

- **Different clients issue different mixes of queries.** A backend used by many clients sees a distribution that shifts as client deployments roll out new versions.
- **Time of day matters.** Home-user traffic has a different query shape than work-user traffic; interactive traffic differs from batch traffic.
- **Software updates change the cost per query.** A new version of the backend might make a common feature significantly cheaper (or more expensive), breaking the old conversion rate overnight.

A capacity plan and a load balancer that rely on QPS are therefore chasing a moving target. The fleet that can handle 10,000 QPS today might handle 7,000 or 15,000 tomorrow.

## The alternative: measure capacity in resources

Chapter 21's recommendation (source: chapter-21-handling-overload.md):

> It works much better to use those numbers directly to model a datacenter's capacity. We often speak about the cost of a request to refer to a normalized measure of how much CPU time it has consumed (over different CPU architectures, with consideration of performance differences).

The mechanism:

- Know how many **CPU cores** and how much **memory** are reserved for the service in each datacenter (e.g., "500 CPU cores and 1 TB memory").
- Compute the **CPU time** consumed by each individual request, normalised across hardware generations.
- Use CPU as the load signal for provisioning, [[per-customer-quotas|quota enforcement]], [[utilization-signals|local shedding]], and [[weighted-round-robin|load balancing]].

The choice of CPU as the single signal is justified in the chapter (source: chapter-21-handling-overload.md):

- **In platforms with garbage collection, memory pressure naturally translates into increased CPU consumption.** So CPU already indirectly reflects memory load.
- **In other platforms, it is possible to provision the remaining resources so that they are very unlikely to run out before CPU does.** Over-provisioning memory modestly is cheap insurance.
- **Where over-provisioning non-CPU resources is prohibitively expensive,** each resource is tracked separately.

CPU as the primary signal with per-resource exceptions is the working rule. It is why [[weighted-round-robin]] uses CPU utilisation as its capability input, and why [[utilization-signals|task-local overload protection]] defaults to a CPU-derived load signal.

## Why "keys read" and similar proxies don't work

The "number of keys read per request" heuristic is called out as an example of a static feature of the request that is mistaken for a cost estimator. The problem is that the same key-count can correspond to cheap cache hits on one version of the backend and expensive cold reads on the next — or to a value-size distribution that skews the actual bytes touched. The cost of a request is an *emergent* property of how the request interacts with the whole system, not a derivable function of the request's inputs.

Trying to estimate cost from request shape is the kind of local reasoning that [[queries-per-second-pitfalls|QPS-style metrics]] encourage; measuring cost empirically from CPU is the structural fix.

## Real-time cost computation

Chapter 21 notes a subtlety for servers that don't use a thread-per-request model (source: chapter-21-handling-overload.md):

> An interesting part of the puzzle is computing in real time the amount of resources — specifically CPU — consumed by each individual request. This computation is particularly tricky for servers that don't implement a thread-per-request model, where a pool of threads just executes different parts of all requests as they come in, using nonblocking APIs.

In other words: even with CPU as the right signal, attributing CPU-time to the request that caused it requires non-trivial bookkeeping. Google has "written significant code" to do this in its backend tasks. The point is that CPU is the right answer *and* a non-trivial thing to measure, not a free lunch.

## Consequences for the rest of the chapter

Once CPU is the accepted capacity unit, the rest of Chapter 21 follows:

- [[per-customer-quotas]] are expressed in **CPU seconds per second** (effectively the number of CPU cores a customer is allowed to consume), not in requests per second.
- [[adaptive-throttling]] still counts request acceptance rates because the *rejection* decision is per-request, but the rejection is itself driven by CPU-denominated quota exhaustion upstream.
- [[utilization-signals]] use CPU utilisation (active threads relative to processor count) as the primary input.
- [[weighted-round-robin|Chapter 20's Weighted Round Robin]] uses reported CPU utilisation as the capability score input for exactly the same reason: requests-in-flight is a poor proxy for load, CPU is not.

The QPS-pitfalls argument is therefore foundational to the rest of the overload-handling machinery. It is also the single idea most directly transferable to other systems: if a service's capacity is measured in QPS, the first improvement is usually to switch to CPU.

## Relationship to existing wiki concepts

### And [[load-parameters]]

Kleppmann's discussion of [[load-parameters]] makes the same observation at a more general level: the right load parameter for a system depends on the system, and picking the wrong one makes capacity planning meaningless. Chapter 21 is this argument specialised to serving systems at Google scale, with the concrete answer: **CPU-time per request**.

### And [[capacity-planning]]

[[capacity-planning]] is the activity that *consumes* a capacity metric. Chapter 21's argument is that if the capacity metric is QPS, the plan is wrong in a way that will be exposed every time the client mix shifts. Switching the metric to CPU makes the plan stable under workload-shape changes, which is a precondition for [[auxon|intent-based capacity planning]] to work at all.

### And [[weighted-round-robin]]

Weighted Round Robin uses the same "CPU is the right signal" decision as its core. The backend reports CPU utilisation; the client uses that to weight routing. Chapter 21's arguments are the justification for why utilisation (not request count, not request-keys-read) is the input to the balancing policy.

### And [[monitoring-resolution]]

The CPU signal is most useful when sampled at high enough frequency to catch transient spikes; this is an application of [[monitoring-resolution|Chapter 6's "match granularity to the question"]] principle. CPU sampled once a minute misses the seconds-long spikes that actually cause rejection decisions.

## Related pages

- [[handling-overload]]
- [[per-customer-quotas]]
- [[utilization-signals]]
- [[weighted-round-robin]]
- [[capacity-planning]]
- [[load-parameters]]
- [[auxon]]
- [[site-reliability-engineering]]
