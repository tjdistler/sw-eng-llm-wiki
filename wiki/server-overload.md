# Server Overload

**Summary**: SRE Chapter 22 names server overload as **the** most common cause of cascading failure: most cascades are either direct cases of overload or extensions of the overload pattern. When a server receives more requests than it can handle, its rate of *successful* responses falls below what it would handle at full capacity — not just below the incoming rate. That inversion turns a capacity shortfall into a feedback loop: load balancers shift traffic elsewhere, overload peers, and propagate the failure.

**Sources**: `raw/site-reliability-engineering/chapter-22-addressing-cascading-failures.md`

**Last updated**: 2026-04-17

---

## The chapter's framing

From Chapter 22 (source: chapter-22-addressing-cascading-failures.md):

> The most common cause of cascading failures is overload. Most cascading failures described here are either directly due to server overload, or due to extensions or variations of this scenario.

The causal chain is concrete and short:

1. A server receives more requests than it can handle.
2. It runs out of resources ([[resource-exhaustion|CPU, memory, threads, file descriptors]]).
3. Running out of resources causes it to crash, miss deadlines, or otherwise misbehave.
4. **The rate of successfully handled requests drops below the rate it could handle at full provisioning.**
5. Load balancers, noticing the server is unhealthy, shift traffic elsewhere — overloading other servers.
6. The failure propagates.

The critical step is 4: overload doesn't cause the server to degrade gracefully — it causes the server to *stop serving*. The rate of useful work falls as the rate of incoming work climbs.

## The Shakespeare worked example

Chapter 22's opening example makes the inversion concrete (source: chapter-22-addressing-cascading-failures.md):

- Cluster A handles 1,000 QPS, cluster B handles 1,000 QPS.
- Cluster B fails. All 2,000 QPS goes to A.
- A is provisioned for 1,000 QPS. At 1,200 QPS it starts failing.
- The *served* rate in A drops well below 1,000 QPS — possibly to zero if A crashes entirely.
- The load balancer sees A failing and shifts traffic elsewhere, potentially to clusters also near capacity.

The pattern is: one cluster fails, the remaining clusters are overloaded, the remaining clusters fail. The total service capacity drops faster than the incoming traffic, and the service is down.

## Why overload causes the inversion

The inversion in step 4 of the causal chain is not automatic — it requires specific resource-exhaustion failure modes. See [[resource-exhaustion]] for the catalogue; the short version:

- **CPU** starvation slows every request, which increases the number of concurrent in-flight requests, which increases memory pressure, which triggers more GC, which uses more CPU. Known as the [[gc-death-spiral]] in JVM-based services.
- **Memory** exhaustion causes tasks to be killed by the container manager, or causes cache hit rates to fall, increasing backend load.
- **Threads** starve, causing health checks to fail, causing the load balancer to drop the task from the pool.
- **File descriptors** exhaust, preventing new network connections.

Each of these failure modes converts "slow but still serving" into "not serving." A server that merely slowed down proportionally under overload would not cascade. A server that crashes under overload reliably cascades.

## Preventing overload

Chapter 22 lists five strategies in rough priority order (source: chapter-22-addressing-cascading-failures.md):

1. **Load test the server's capacity limits and test the failure mode for overload.** This is the most important step. Without realistic testing, it's impossible to predict which resource will run out first or how the failure will manifest. See [[testing-for-cascading-failures]].
2. **Serve [[graceful-degradation|degraded results]]** — lower-quality, cheaper-to-compute responses.
3. **Instrument the server to reject requests when overloaded** — [[load-shedding]]; fail early and cheaply.
4. **Instrument higher-level systems to reject early** — rate limiting at reverse proxies, load balancers, and individual tasks.
5. **Capacity planning** — reduces the probability of overload, but cannot prevent cascades on its own (load balancing quirks, network partitions, and unexpected traffic can create pockets of high load beyond what was planned).

These are cumulative, not substitutable. Capacity planning alone gives a mean-case defence; load shedding gives a worst-case defence; graceful degradation extends the working range before either of the others engages.

## Relationship to Chapter 21

[[handling-overload|Chapter 21]] is the detailed treatment of per-task overload defences — [[per-customer-quotas]], [[adaptive-throttling]], [[request-criticality]], [[utilization-signals]], [[load-shedding]], [[graceful-degradation]], [[retry-budget]], [[connection-level-load]]. Chapter 22 reframes those mechanisms as *cascading-failure prevention*: the reason Chapter 21 matters at the system level is that a task without those defences reliably triggers a cascade.

The two chapters are complementary:

- Chapter 21: how one task defends itself.
- Chapter 22: what happens across the whole service when tasks don't defend themselves, and how to prevent or recover from the resulting cascade.

## Service unavailability: the snowball effect

Chapter 22 develops a specific sub-case of overload worth flagging (source: chapter-22-addressing-cascading-failures.md):

> Resource exhaustion can lead to servers crashing... Once a couple of servers crash on overload, the load on the remaining servers can increase, causing them to crash as well. The problem tends to snowball and soon all servers begin to crash-loop. It's often difficult to escape this scenario because as soon as servers come back online they're bombarded with an extremely high rate of requests and fail almost immediately.

The memorable example:

> If a service was healthy at 10,000 QPS, but started a cascading failure due to crashes at 11,000 QPS, dropping the load to 9,000 QPS will almost certainly not stop the crashes.

The intuition: with only (say) 10% of servers healthy at any given moment, the service's effective capacity is only 10% of its provisioned capacity. To stabilise, load must drop below that 10%. The chapter's example needs load dropped from 11,000 QPS not to 9,000 but to **about 1,000 QPS** — an order of magnitude below normal — before the system can recover.

This asymmetry (easy to fall into, hard to climb out of) is why [[addressing-ongoing-cascading-failure|dropping traffic aggressively]] is a named recovery strategy, and why the drop must often go far below the "normal" rate the service handled a moment ago.

## Related pages

- [[cascading-failure]]
- [[resource-exhaustion]]
- [[gc-death-spiral]]
- [[load-shedding]]
- [[graceful-degradation]]
- [[handling-overload]]
- [[per-customer-quotas]]
- [[adaptive-throttling]]
- [[testing-for-cascading-failures]]
- [[addressing-ongoing-cascading-failure]]
- [[capacity-planning]]
- [[weighted-round-robin]]
- [[site-reliability-engineering]]
