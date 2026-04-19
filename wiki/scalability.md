# Scalability

**Summary**: Scalability describes a system's ability to cope with increased load — in data volume, traffic volume, or complexity — and the strategies available for handling that growth.

**Sources**: `raw/designing-data-intensive-applications/chapter-01-reliable-scalable-and-maintainable-applications.md`, `raw/software-architecture-the-hard-parts/chapter-03-architectural-modularity.md`

**Last updated**: 2026-04-19

---

## Scalability is not a binary property

"X is scalable" and "Y doesn't scale" are not meaningful statements. Scalability is about asking:

- If load grows in a specific way, what are our options?
- How much additional resource is needed to keep performance constant under higher load?

The answers are always specific to a particular application's [[load-parameters]].

## Describing load

Before reasoning about scale, you must quantify current load with **load parameters** — numbers that characterize what the system is doing. See [[load-parameters]] for detail.

## Describing performance

Two ways to investigate what happens when load increases:

1. Keep resources fixed, increase load — how does performance degrade?
2. Keep performance fixed, increase load — how much more resource is needed?

Key performance metrics differ by system type:

- **Batch systems** (e.g. Hadoop): care about **throughput** — records processed per second, or total job duration for a given dataset size
- **Online systems**: care about **response time** — time between client sending a request and receiving a response

For measuring response time correctly, see [[response-time-percentiles]].

## Fan-out: a concrete scalability challenge

Twitter's home timeline is a canonical example of a load-driven design decision. (source: chapter-01)

**The problem**: each tweet must be delivered to all followers. With some users having 30+ million followers, a single tweet could require 30 million writes.

**Approach 1 — read-time fan-out**: Store tweets in a global collection; compute each user's timeline at read time via a JOIN query. Simple writes, expensive reads. Struggled at Twitter's 300k timeline reads/sec.

**Approach 2 — write-time fan-out**: Maintain a pre-computed timeline cache per user. On tweet post, write to every follower's cache. Cheap reads, expensive writes (~345k cache writes/sec for average fan-out of 75). Breaks down for users with millions of followers.

**Twitter's hybrid**: Most users use write-time fan-out. Celebrities (very high follower counts) are excluded; their tweets are fetched and merged at read time. The distribution of followers per user is the key load parameter driving this design.

## Approaches for coping with load

See [[scaling-approaches]] for detail. In brief:

- **Scale up** (vertical): move to a more powerful machine — simpler but expensive at the high end
- **Scale out** (horizontal): distribute load across many smaller machines (shared-nothing architecture)
- **Elastic scaling**: automatically add resources when load increases; useful for unpredictable load
- **Manual scaling**: simpler operationally, fewer surprises

Architecture must match the application's specific load parameters. There is no generic "magic scaling sauce" — a system handling 100,000 × 1 kB requests/sec looks entirely different from one handling 3 × 2 GB requests/min, even at the same total throughput. (source: chapter-01)

## Scalability vs elasticity (Hard Parts framing)

Chapter 3 of *Software Architecture: The Hard Parts* distinguishes scalability from [[elasticity]] along a time-scale axis (source: raw/software-architecture-the-hard-parts/chapter-03-architectural-modularity.md):

- **Scalability** — responsiveness as user load *gradually* increases over time. Driven by normal company growth.
- **Elasticity** — responsiveness during *instantaneous* spikes. The concert-ticket-on-sale example: 20 to 3,000 concurrent users in seconds.

Both are functions of the number of concurrent requests, but they require different architectural support. Ford and Richards argue:

> Elasticity is more a function of **granularity** (the size of a deployment unit), whereas scalability is more a function of **modularity** (the breaking apart of applications into separate deployment units).

A large monolith with ten instances behind a load balancer has some scalability but no elasticity — each instance's mean time to startup (MTTS) is too long to respond to a burst. Fine-grained [[microservices]] have both. See [[architectural-modularity]] for the full five-driver treatment and [[elasticity]] for the MTTS mechanism.

The star-rating table the chapter uses (Figure 3-9):

| Architecture | Scalability | Elasticity |
|---|---|---|
| [[layered-architecture]] (monolithic) | low | low |
| [[service-based-architecture]] | moderate | low–moderate |
| [[microservices]] | high | high |

Service-based scales at the **domain** level (each domain service can scale independently), but its coarse grain keeps MTTS high enough that elasticity lags. Microservices achieve **function-level** scalability and elasticity because each service is fine-grained and quick to start.

### The chatter caveat

As with all five modularity drivers in Chapter 3, scalability benefits collapse under synchronous service-to-service chatter (source: raw/software-architecture-the-hard-parts/chapter-03-architectural-modularity.md):

> The more services communicate with one other to complete a single business transaction, the greater the negative impact on scalability and elasticity. For this reason, it is important to keep synchronous communication among services to a minimum when requiring high levels of scalability and elasticity.

A fan-out of ten synchronous calls per request amplifies load ten-fold and gates end-to-end latency on the slowest peer. The prescriptions mirror those on [[architectural-modularity]]: prefer asynchronous integration; if synchronous chatter is unavoidable, fix granularity (bundle chatty services).

## Related pages

- [[load-parameters]]
- [[response-time-percentiles]]
- [[scaling-approaches]]
- [[partitioning]]
- [[replication]]
- [[reliability]]
- [[maintainability]]
- [[replicated-load-balanced-service]]
- [[elasticity]]
- [[architectural-modularity]]
- [[microservices]]
- [[service-based-architecture]]
