# Weighted Round Robin

**Summary**: The top rung of SRE Chapter 20's [[load-balancing-policies|policy ladder]]. Each backend reports its current QPS, error rate, and CPU utilisation in *every response* (including responses to health checks). Each client maintains a per-backend **capability score** and distributes requests round-robin but weighted by the scores; failed requests apply a penalty that shapes future decisions. Chapter 20's Figure 20-6 shows the CPU distribution tightening dramatically when a service switches from Least-Loaded to Weighted — the most and least loaded backends converge. The policy works because it replaces the poor proxies used by [[simple-round-robin|Simple]] and [[least-loaded-round-robin|Least-Loaded]] with direct backend-reported state that reflects actual load including traffic from every other client.

**Sources**: `raw/site-reliability-engineering/chapter-20-load-balancing-in-the-datacenter.md`

**Last updated**: 2026-04-17

---

## The policy

Chapter 20's description in essence (source: chapter-20-load-balancing-in-the-datacenter.md):

1. **Each backend reports, in every response:** current observed QPS, errors per second, and utilisation (typically CPU).
2. **Each client keeps a capability score per backend in its [[subsetting|subset]]**, updated periodically from the reported data.
3. **Requests are distributed round-robin but weighted by capability score.** A backend with 2x the score of its peers gets roughly 2x the traffic.
4. **Failed requests penalise the score**, so a backend that has started failing is de-prioritised even if its utilisation still looks low.

The backend is the source of truth; the client is the adjuster. The feedback loop closes within the response latency of the next request (or the next health check), so the policy tracks load changes closely.

## What makes it work

### Real backend state, not a proxy

[[simple-round-robin|Simple Round Robin]] uses no information. [[least-loaded-round-robin|Least-Loaded]] uses active-request count, which as Chapter 20 notes is a poor proxy — it is skewed by I/O-bound waiting and blind to traffic from other clients. Weighted Round Robin uses **the backend's own measurement of its own load**, which has neither problem:

- **Capability differences are visible.** A backend with a faster CPU will report lower utilisation at the same QPS, so its capability score stays high and the client sends more traffic to it. Least-Loaded could not tell fast and slow backends apart when requests were I/O-bound.
- **Aggregate load is visible.** The backend sees *all* traffic, not just one client's share. A backend heavily loaded by others reports high utilisation, so every client backs off — not just the ones that happened to have sent recent traffic.

### The signal is free

The utilisation report piggybacks on the response, which is already being sent. There are no extra round trips, no scraping, no coordination service. The UDP health checks that [[backend-task-states|propagate state changes]] carry the same report for currently-idle clients. So the signal costs almost nothing to collect.

### Errors as a first-class signal

The penalty for failed requests is not an afterthought: it is what stops the Least-Loaded sinkhole from recurring here. A fast-failing backend reports low utilisation, but its error count is high; the penalty dominates and the capability score drops. Weighted Round Robin inherits the error-counting lesson and uses it directly in the score.

## The result

Chapter 20's Figure 20-6 shows the CPU utilisation of a random subset of backend tasks across the switch from Least-Loaded to Weighted. The spread before: the usual ~2x range from least to most loaded. The spread after: a much tighter band. The chapter's understated language: *"In practice, Weighted Round Robin has worked very well and significantly reduced the difference between the most and the least utilised tasks"* (source: chapter-20-load-balancing-in-the-datacenter.md).

Tightened spread means less wasted capacity. A service reserving 1,000 CPUs that previously could only use 700 with Simple Round Robin can use closer to its reservation with Weighted — the promise of the [[datacenter-load-balancing|ideal-case]] framing Chapter 20 opens with.

## What it doesn't solve

The policy is about *distributing* a given workload fairly across a given fleet. It cannot change the workload or the fleet:

- **Varying query costs still vary.** A 10-second outlier query still spikes the one backend that gets it.
- **Antagonistic neighbours still degrade.** Utilisation reports will reflect the degradation (the affected backend reports higher utilisation), so the policy routes around it — but the degradation itself is an environmental fact.
- **Task restarts still take time.** Post-restart warmup remains a fleet-level concern; the policy can observe that a warming task reports high utilisation for low QPS and send less traffic there, but it doesn't accelerate the warm-up.

For these, the solutions are elsewhere: cap per-request work ([[simple-round-robin|Chapter 20 pagination discussion]]), [[borg|failure-domain-aware scheduling]], post-restart [[lame-duck-state|prewarming via lame duck]]. Weighted Round Robin handles the distribution side; the workload and environment sides need their own levers.

## Relationship to existing wiki concepts

### Weighted and a control loop

The score-update cycle is a closed-loop controller: observe (utilisation, errors), decide (weights), act (route), observe again. This is the same pattern that [[desired-state-management]] runs at the orchestrator level and that [[architecture-fitness-function|architecture fitness functions]] formalise. Weighted Round Robin is what this pattern looks like when applied per-request inside the RPC client.

### Weighted and backend telemetry

Weighted Round Robin depends on backends having accurate self-measurement of QPS, error rate, and CPU utilisation. The telemetry infrastructure Google describes in [[borgmon|Chapter 10]] and the [[varz-endpoints|/varz conventions]] are the plumbing that makes this cheap: a backend *already* exposes these numbers for monitoring, so the same numbers ride on every response as a routing signal.

### Weighted and the Maglev balancer

The [[network-load-balancer|Chapter 19 packet balancer]] uses connection-tracking plus consistent-hashing, not capability scoring — because it operates per-packet, with no response stream to piggyback utilisation on. Weighted Round Robin is specifically an *application-layer, stateful-RPC* policy; the packet-level layer has its own machinery. The two layers compose: the packet balancer picks a frontend, the frontend's Weighted Round Robin client picks a backend.

### Weighted and capacity planning

Good balancing is a precondition for honest [[capacity-planning]]. If the planner reserves N CPUs on the assumption that the service can use them, and the balancer produces an uneven distribution that caps usable capacity at 0.7N, the plan is structurally wrong. Weighted Round Robin is the mechanism that lets the plan be taken at face value — which is why [[auxon|Chapter 18's capacity planner]] works better with Weighted than with Simple Round Robin on its target services.

### Weighted and Bellemare's smart load balancer

Bellemare's [[smart-load-balancer]] operates on partition-aware EDM state stores: it routes a request to the instance currently hosting the relevant partition. That's a different routing problem (semantic routing, not capacity balancing), but the pattern is the same: the client uses runtime state from the backend to route. Weighted Round Robin routes on utilisation; Smart Load Balancer routes on partition ownership; both avoid the dumb-router degenerate case.

## Related pages

- [[load-balancing-policies]]
- [[simple-round-robin]]
- [[least-loaded-round-robin]]
- [[datacenter-load-balancing]]
- [[backend-task-states]]
- [[borgmon]]
- [[varz-endpoints]]
- [[capacity-planning]]
- [[auxon]]
- [[smart-load-balancer]]
- [[site-reliability-engineering]]
