# N + 2 Redundancy

**Summary**: The sizing rule Google applies to a fleet of tasks serving peak load: provision enough replicas to lose **two** at the same time and still serve peak. N is the number required for peak load; +2 covers *one task being down for an update* plus *one task failing during that update*.

**Sources**: `raw/site-reliability-engineering/chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md`

**Last updated**: 2026-04-17

---

## The derivation

The Chapter 2 Shakespeare example works through the numbers explicitly (source: chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md):

- A backend handles **100 QPS**. Peak load is projected at **3,470 QPS**. So N = 35 tasks.
- During updates, **one task at a time is unavailable**, leaving 34.
- A **machine failure during the update** could take a second task, leaving 33 — **not enough** to serve peak.
- Therefore size at **N + 2 = 37** tasks.

The two extra tasks are the cost of doing updates without an availability dip when a failure coincides with the rollout.

## Per-region sizing

When the service is globally distributed, N + 2 is applied **per region** after regional traffic is broken out (source: chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md):

- USA: 1,430 QPS → 15 + 2 = **17 tasks**
- Europe and Africa: 1,400 QPS → 14 + 2 = **16 tasks**
- Asia and Australia: 350 QPS → 4 + 2 = **6 tasks**
- South America: 290 QPS → 3 + 1 = **4 tasks** (see below)

## When N + 1 is OK

The South American region uses **N + 1** instead of N + 2, accepting the risk that if a task fails during an update there is a small chance of capacity overrun. If that happens, [[gslb|GSLB]] redirects traffic to another continent, incurring higher latency. The justification: saving 20% of the regional hardware cost (source: chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md).

This is the [[error-budget]] philosophy in miniature: N + 1 admits a measurable reliability risk, in exchange for quantified resource savings. It is a product-level decision, not a blanket rule.

## The hidden assumption

N + 2 assumes that the probability of two *simultaneous* task failures is low enough to ignore. Chapter 2's footnote warns this may not hold when **correlated failure** is a risk — a [[google-datacenter-topology|top-of-rack switch]] or power distribution unit is a single point of failure for every task on its rack (source: chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md). [[borg]]'s failure-domain-aware binpacking (not placing all of a job's tasks on one rack) is the mechanism that keeps the assumption valid.

## Also: spread across clusters

For large regions, Google spreads tasks across two or three clusters for extra resiliency (source: chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md). Same principle, one level up: don't put all tasks in one failure domain.

## Cross-book connections

- [[capacity-planning]] — N + 2 is the redundancy side of the capacity calculation; Chapter 1 defines the demand-forecast and load-test side.
- [[provisioning]] — the execution step of turning "we need 37 tasks" into actual running capacity.
- [[error-budget]] — N + 1 for South America is a budget-spending decision, framed against hardware cost.
- [[replicated-load-balanced-service]] (Burns) — the container-level pattern; N + 2 is the specific sizing discipline to apply to it.
- [[dynamic-worker-scaling]] (Burns) — the worker-pool version of the same calculation (`P > processing_time / interarrival_time`).

## Related pages

- [[capacity-planning]]
- [[provisioning]]
- [[gslb]]
- [[borg]]
- [[replicated-load-balanced-service]]
- [[site-reliability-engineering]]
