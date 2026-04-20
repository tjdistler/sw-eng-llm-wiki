# Black-Box vs White-Box Monitoring

**Summary**: Black-box monitoring tests externally visible behaviour as a user would see it; white-box monitoring inspects the internals via logs, stats endpoints, or profiling interfaces. Google SRE uses *heavy* white-box with *modest but critical* black-box.

**Sources**: `raw/site-reliability-engineering/chapter-06-monitoring-distributed-systems.md`, `raw/site-reliability-engineering/chapter-10-practical-alerting-from-time-series-data.md`

**Last updated**: 2026-04-17

---

## Definitions

From Chapter 6's glossary (source: chapter-06-monitoring-distributed-systems.md):

- **White-box monitoring** — based on metrics exposed by the *internals* of the system: logs, JVM profiling interfaces, an HTTP handler that emits internal statistics.
- **Black-box monitoring** — testing externally visible behaviour *as a user would see it*: probes, synthetic requests, end-to-end checks.

## What each one is good for

### Black-box: active, symptom-oriented

Chapter 6's framing:

> The system isn't working correctly, right now.

Black-box checks are by construction symptom-oriented — they exercise user-visible behaviour. That makes them excellent for **paging discipline**: a black-box check that fails means a user would see the same failure. You can't page on a cause if you have no idea whether it's actually manifesting as a symptom.

What black-box can't do: detect *imminent* problems (nothing has failed yet), or see problems *masked by retries*. A system that's flaky internally but succeeds after three retries looks fine from the outside.

### White-box: predictive and diagnostic

White-box can:

- Detect **imminent problems** — "the disk will be full in 4 hours"
- See **failures masked by retries** — error rates inside the system, not just success at the edge
- Supply debugging telemetry — per-component latency, cache hit rates, queue depths, GC pauses

White-box is essential for *debugging*. If a web request is slow and only the web server is instrumented, you cannot tell whether the database is slow or the network between them is slow. You need both sides instrumented to pin down where the time went.

## Symptom/cause status depends on layer

White-box is **sometimes symptom-oriented and sometimes cause-oriented** — it depends on the observer's layer (source: chapter-06-monitoring-distributed-systems.md). "Slow database reads" is a symptom for the DB SRE (whose white-box monitoring fires) and a cause for the frontend SRE (whose white-box monitoring reports it alongside the actual symptom of slow user requests). This is covered more thoroughly in [[symptoms-vs-causes]].

Black-box is always symptom-oriented. That's the point.

## Google's mix

The Chapter 6 recipe:

- **Heavy white-box** — every server exposes internal metrics scraped by a central time-series monitoring system; dashboards, debugging, and most alerting rely on it.
- **Modest but critical black-box** — the discipline backstop that ensures a page is only triggered when a problem is actually manifesting externally.

The "modest" part matters: you don't need hundreds of black-box probes. You need a small set of them hitting the user-critical paths, plus extensive white-box for everything else.

## The concrete tools (Chapter 10)

Chapter 10 supplies the concrete realisation of each side (source: chapter-10-practical-alerting-from-time-series-data.md):

- **White-box**: a time-series monitoring system scrapes a text metrics endpoint on every server, stores the series in an in-memory arena, and evaluates rules. Inspects the internal state of the target with knowledge of the internals in mind.
- **Black-box: [[prober]]** — runs a protocol check against a target and reports success or failure. Validates response payload, extracts values as time-series, can alert directly or feed its own metrics back to the monitoring system.

Chapter 10 also gives the pointed white-box limitation that makes Prober necessary:

> You only see the queries that arrive at the target; the queries that never make it due to a DNS error are invisible, while queries lost due to a server crash never make a sound. You can only alert on the failures that you expected.

Prober closes that gap by checking from outside the service — including both in front of and behind the load balancer, so that localised failures can be distinguished from user-visible ones.

## The page-source framing

Chapter 6's [[alert-philosophy]] section argues that once you enforce *"every page should be about a novel, urgent, actionable, user-visible problem"*, it becomes irrelevant whether the triggering signal is white-box or black-box — a good page meets the criteria regardless. What matters is signal quality, not monitoring style.

## Cross-book connections

- [[synthetic-transactions]] (Newman) — Newman's synthetic transactions are exactly Google's critical black-box probes: scripted fake users exercising end-to-end behaviour against production.
- [[monitoring-and-observability]] — the monitoring half of Newman's monitoring-vs-observability distinction; white-box metrics and black-box probes are two complementary ways of populating it.
- [[health-probes]] (Burns) — Kubernetes liveness and readiness probes are the container-orchestrator's black-box mechanism.
- [[health-check-adapter]] (Burns) — the adapter-pattern realisation of richer application-aware black-box checks.

## Related pages

- [[symptoms-vs-causes]]
- [[four-golden-signals]]
- [[alert-philosophy]]
- [[synthetic-transactions]]
- [[health-probes]]
- [[health-check-adapter]]
- [[monitoring-and-observability]]
- [[sre-monitoring-outputs]]
- [[prober]]
- [[site-reliability-engineering]]
