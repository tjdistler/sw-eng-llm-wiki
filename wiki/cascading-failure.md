# Cascading Failure

**Summary**: A failure that grows over time through positive feedback: a portion of the system fails, which increases the probability that other portions fail, which causes still more to fail, until the whole service is down. SRE Chapter 22 (Mike Ulrich) is the canonical treatment — overload is the dominant cause, resource exhaustion is the mechanism, retries and health-check loops are the amplifiers, and recovery often requires dropping load to a small fraction of normal (not just back to pre-failure levels) because fresh tasks are bombarded as soon as they start. Also called "meltdown" and, in its traffic-shaped variant, a "thundering herd."

**Sources**: `raw/site-reliability-engineering/chapter-22-addressing-cascading-failures.md`

**Last updated**: 2026-04-17

---

## The definition

Chapter 22 opens with the definition (source: chapter-22-addressing-cascading-failures.md):

> A cascading failure is a failure that grows over time as a result of positive feedback. It can occur when a portion of an overall system fails, increasing the probability that other portions of the system fail. For example, a single replica for a service can fail due to overload, increasing load on remaining replicas and increasing their probability of failing, causing a domino effect that takes down all the replicas for a service.

The key word is **positive feedback**: the consequence of one failure is more failures, not fewer. A resilient system has negative feedback (redundancy absorbs faults, reducing their effect); a cascading-prone system has the opposite.

## The canonical worked example

The chapter's opening worked example (source: chapter-22-addressing-cascading-failures.md):

1. The frontend in cluster A is handling 1,000 QPS. Cluster B is also handling 1,000 QPS.
2. Cluster B fails. Requests to A increase to 1,200 QPS.
3. The frontends in A cannot handle 1,200 QPS. They run out of resources, crash, miss deadlines, or otherwise misbehave.
4. The rate of *successfully* handled requests in A drops *below* 1,000 QPS — even though the total request rate is now 1,200 QPS.
5. The load balancer notices A is failing, sends requests elsewhere, overloading still more clusters.
6. Service-wide overload within minutes.

The critical observation is in step 4: overload doesn't cause the service to serve more slowly — it causes the service to serve **less**. The rate of useful work drops as the rate of incoming work climbs. That inversion is what turns a capacity shortfall into a cascade.

## Causes

Chapter 22 catalogues four categories of cause:

- [[server-overload]] — the dominant cause; most other cascades are variations or extensions of this one.
- [[resource-exhaustion]] — CPU, memory, threads, file descriptors. The *mechanism* by which overload kills tasks, with specific named failure modes including the [[gc-death-spiral]].
- **Service unavailability** — once some tasks crash, the load on survivors increases, causing more crashes, and the problem snowballs. Restarting doesn't help: fresh tasks are bombarded immediately and fail before stabilising. The chapter's memorable example — a service healthy at 10,000 QPS and crashing at 11,000 QPS may need load dropped to **1,000 QPS** before it can recover, not 9,000.
- Health-check-driven lame-duck and crash loops that look to the load balancer like capacity disappearing.

## Preventing cascading failure

Chapter 22's prevention strategies compose rather than substitute. In rough priority order (source: chapter-22-addressing-cascading-failures.md):

1. **Load test to failure and beyond.** Without real data on where the service breaks and how it breaks, no other defence can be calibrated. See [[testing-for-cascading-failures]].
2. **[[graceful-degradation|Serve degraded results]]** rather than refusing entirely.
3. **[[load-shedding|Instrument servers to reject when overloaded]]**, failing early and cheaply.
4. **Instrument higher-level systems to reject early**, via rate limiting at reverse proxies, load balancers, and individual tasks.
5. **[[capacity-planning|Capacity planning]]** — reduces the probability, but is never sufficient on its own.

Plus six design-level disciplines the chapter develops in detail, each on its own page:

- [[queue-management]] — short queues relative to thread-pool size; [[load-shedding|shed]] rather than queue indefinitely.
- [[load-shedding]] and [[graceful-degradation]] — the per-task safety valves Chapter 21 developed; Chapter 22 reinforces them as cascading-failure prevention.
- [[retry-amplification]] — the retries mechanism naïve clients implement is one of the most reliable ways to turn a transient problem into a cascade.
- [[latency-and-deadlines]] — the deadline set by the client caps how much a server can waste on work that will be thrown away; propagate deadlines through the stack so deep backends don't do work the top of the stack has already given up on.
- [[bimodal-latency]] — a fraction of requests that never complete can consume capacity far out of proportion to their share, turning a 5% problem into an 80% error rate.
- [[slow-startup-and-cold-caching]] — restart-after-crash is exactly the condition under which the task is *least* able to serve its normal load; fresh caches and cold JIT make capacity temporarily much lower.
- [[intra-layer-communication]] — backends that proxy to other backends to "help" each other are a reliable cause of distributed deadlock and sudden mode switches under load. Always go downward in the stack.

## Triggering conditions

A cascade requires both a vulnerable system and a trigger. Chapter 22 catalogues five classes of trigger on [[cascading-failure-triggers]] — process deaths, process updates, new rollouts, organic growth, and planned changes or drains. None of these is inherently catastrophic on a resilient system; each is reliably catastrophic on a system with any of the vulnerabilities above.

## Addressing an ongoing cascade

Once the cascade is happening, Chapter 22's eight immediate-steps are on [[addressing-ongoing-cascading-failure]]:

1. Increase resources (if you have idle capacity).
2. Stop health-check failures and death loops (possibly by temporarily disabling health checks).
3. Restart servers (only after identifying why they are stuck; don't just shift load).
4. Drop traffic (the big hammer — may need to go to 1% of normal before the service can recover).
5. Enter degraded modes.
6. Eliminate batch load.
7. Eliminate bad traffic (queries of death).
8. Escalate and use the incident-management protocol.

The underlying directive: identify and address the *triggering condition* before dropping load, because otherwise the cascade will just start again as soon as traffic returns.

## The Shakespeare narrative

Chapter 22 closes with a short worked scenario (source: chapter-22-addressing-cascading-failures.md) — a Japanese documentary about Shakespeare causes a traffic surge to Google's Asian datacenter that coincides with a service update. [[graceful-degradation|Graceful degradation]] strips pictures and maps, [[retry-budget|retries use exponential backoff]], but tasks still fail one by one and Borg restarts them, driving healthy-task count down faster than it recovers. SREs add capacity to the cluster manually; post-incident, [[gslb|GSLB]] is configured to redirect to neighbours, and autoscaling is turned on. The story demonstrates the chapter's thesis: every individual safeguard helps, but cascading failure is a *system* property, and the defence is a cooperating stack.

## The closing thesis

Chapter 22's one-paragraph summary is worth preserving (source: chapter-22-addressing-cascading-failures.md):

> When systems are overloaded, something needs to give in order to remedy the situation. Once a service passes its breaking point, it is better to allow some user-visible errors or lower-quality results to slip through than try to fully serve every request. Understanding where those breaking points are and how the system behaves beyond them is critical for service owners who want to avoid cascading failures. Without proper care, some system changes meant to reduce background errors or otherwise improve the steady state can expose the service to greater risk of a full outage. Retrying on failures, shifting load around from unhealthy servers, killing unhealthy servers, adding caches to improve performance or reduce latency: all of these might be implemented to improve the normal case, but can improve the chance of causing a large-scale failure. Be careful when evaluating changes to ensure that one outage is not being traded for another.

The warning in the second half is the one that is easiest to miss: **the changes that improve steady-state reliability often worsen cascading-failure risk**. Adding retries reduces transient error rates at the cost of retry amplification. Adding caches improves latency at the cost of cold-cache vulnerability. Automatic failover reduces MTTR at the cost of health-check death loops. Every one of these is a valid engineering choice; none of them is *free*.

## Relationship to other wiki concepts

### Cascading failure and Chapter 21

[[handling-overload|Chapter 21]] is the mechanism-level treatment: how a single backend task defends itself against overload. Chapter 22 is the system-level treatment: how those defences compose (or fail to compose) into a service that doesn't cascade. The Chapter 21 mechanisms are *preconditions* for Chapter 22's prevention strategies — without per-task [[load-shedding]] and [[adaptive-throttling|client-side throttling]], the domino effect in Chapter 22's opening example is unavoidable.

### Cascading failure and [[fault-tolerance]]

Cascading failure is a failure mode specific to fault-tolerant systems. A system without redundancy can't cascade — it just fails. Cascading requires that the failure of one replica shifts load to another, which then fails, which shifts load again. The mechanism that makes the system fault-tolerant in the steady state (load balancing, retries, failover) is the mechanism that amplifies a small failure into a large one. Chapter 22 is fault-tolerance engineering specifically concerned with the feedback loops that fault-tolerance mechanisms introduce.

### Cascading failure and [[failover]]

[[failover]] is one of the specific triggers Chapter 22 flags: automatic failover can declare nodes dead under load, transfer their traffic to peers, overload the peers, and trigger a cascade. Kleppmann's [[failover]] page lists this under "dangers of premature declaration of death"; Chapter 22 is the detailed operational development of the same warning.

### Cascading failure and [[circuit-breaker]] / [[bulkhead]]

Newman's [[circuit-breaker|circuit breakers]] and [[bulkhead|bulkheads]] are two of the named patterns designed specifically to break cascading-failure feedback loops. The circuit breaker prevents retries from amplifying a downstream outage (the [[retry-amplification]] mechanism). The bulkhead prevents thread-pool exhaustion from one dependency affecting calls to others. Both are discussed in Chapter 22 without the names — the "retries" section is the circuit-breaker discussion, and the "always go downward in the stack" section is the bulkhead discussion applied to communication topology.

### Cascading failure and [[emergency-response]]

Chapter 22 explicitly names cascading failure as "a good opportunity to use your incident management protocol" (source: chapter-22-addressing-cascading-failures.md). The combination of rapid escalation, high cognitive load, and the need to make counterintuitive decisions (dropping traffic to 1% of normal is hard to justify in the moment) is exactly what the [[incident-management-framework]] is designed for.

## Related pages

- [[server-overload]]
- [[resource-exhaustion]]
- [[gc-death-spiral]]
- [[queue-management]]
- [[retry-amplification]]
- [[latency-and-deadlines]]
- [[deadline-propagation]]
- [[bimodal-latency]]
- [[slow-startup-and-cold-caching]]
- [[intra-layer-communication]]
- [[cascading-failure-triggers]]
- [[testing-for-cascading-failures]]
- [[addressing-ongoing-cascading-failure]]
- [[handling-overload]]
- [[load-shedding]]
- [[graceful-degradation]]
- [[adaptive-throttling]]
- [[retry-budget]]
- [[circuit-breaker]]
- [[bulkhead]]
- [[fault-tolerance]]
- [[failover]]
- [[emergency-response]]
- [[site-reliability-engineering]]
