# Graceful Degradation

**Summary**: Under overload, serving a **less accurate** or **less complete** response that is *cheaper to compute*, rather than rejecting the request entirely. SRE Chapter 21 names this as the first preferred response to overload: search a subset of the corpus instead of everything, serve from a local cache instead of going to the canonical store, return a simpler result. When even the cheap path is unavailable, the system falls back to [[load-shedding|rejection]]. Degradation preserves partial usefulness where shedding gives nothing.

**Sources**: `raw/site-reliability-engineering/chapter-21-handling-overload.md`, `raw/site-reliability-engineering/chapter-22-addressing-cascading-failures.md`, `raw/site-reliability-engineering/chapter-27-reliable-product-launches-at-scale.md`

**Last updated**: 2026-04-17

---

## The chapter's framing

Chapter 21 opens with graceful degradation as the first overload response (source: chapter-21-handling-overload.md):

> One option for handling overload is to serve degraded responses: responses that are not as accurate as or that contain less data than normal responses, but that are easier to compute. For example:
>
> - Instead of searching an entire corpus to provide the best available results to a search query, search only a small percentage of the candidate set.
> - Rely on a local copy of results that may not be fully up to date but that will be cheaper to use than going against the canonical storage.
>
> However, under extreme overload, the service might not even be able to compute and serve degraded responses. At this point it may have no immediate option but to serve errors.

Three things are worth pulling out.

### Degradation is designed, not emergent

A service that can gracefully degrade has the degraded-path built as a first-class feature. Serving a partial search requires indexing that supports fast coarse results; falling back to a local cache requires the cache to exist and to be kept fresh enough. Graceful degradation can't be bolted on during the incident — it is architectural work done in advance.

### Degradation beats rejection, rejection beats failure

Chapter 21's implicit ordering for what a service should do under overload, from best to worst:

1. **Serve correctly.** The normal path.
2. **Serve degraded.** Cheaper response, less accurate or less complete. User gets *something*.
3. **Reject the request** ([[load-shedding]]). User gets an error but the service survives to serve other requests.
4. **Crash / queue-and-drop** (what the chapter calls "serving errors"). Worst case — the service is unavailable entirely.

The first three are cooperative failures; the fourth is a failure mode the rest of the chapter is designed to prevent.

### Even degraded paths can be overloaded

The chapter's caveat is important: the cheap path is also cheap *at scale*. If the degraded response path is, say, 10% of the cost of the full path, the service can serve degraded responses at 10x the rate — but if overload is 20x, even degradation saturates. At that point the task has to shed. Degradation is a multiplier on capacity, not an unlimited lifeline.

## Examples from the chapter

The two Chapter 21 examples are representative of two degradation patterns:

### Search a subset instead of the full corpus

Full search is expensive because it examines many candidates. A degraded response searches a small percentage of the candidates — fewer correct results, but answers come back fast and cheap. This is the **reduce-fidelity** pattern: produce a lower-quality answer using less work.

Use cases: ranking, recommendation, full-text search, analytics.

### Serve from a local cache instead of canonical storage

The canonical store may be the bottleneck (especially if every request goes there). A local cache has lower freshness guarantees but is fast and doesn't contribute load to the canonical store. Serving from the cache under overload trades staleness for availability. This is the **stale-is-okay** pattern.

Use cases: user profiles, reference data, feature flags, anything where "last value seen" is nearly as good as "current value."

## The design work

Building a service that can degrade gracefully typically involves:

- **Explicit alternate computation paths.** Not just "serve the cache" but a conditional in the code that checks whether the system is under pressure and routes through the cheaper path when it is. The pressure signal is typically the same [[utilization-signals|utilisation signal]] that drives [[load-shedding|shedding]] — higher thresholds to downgrade, higher still to shed entirely.
- **Acceptable-partial responses that clients can parse.** If the response envelope includes a field like "this result is partial; retry later for full accuracy," clients can choose whether to retry. Otherwise degraded responses look indistinguishable from full ones and clients may act on bad data.
- **Monitoring of the degradation rate.** A service that spends most of its time in degraded mode is under-provisioned and the team needs to know. Degradation rate is an SLI of its own.
- **Tests that exercise the degraded path.** The degraded path is used rarely, which means it rots. Chapter 13's lessons about exercising rarely-used paths apply.

## Graceful degradation in the Chapter 21 stack

Degradation sits above [[load-shedding]] as a preferred alternative:

- If utilisation is high but the degraded path is cheap enough, degrade.
- If utilisation is high and even degradation would overload the task, shed.
- If the degraded response isn't defined for this request type, shed.

So a task with graceful degradation has a wider range of useful operation before it becomes useless — it serves correctly up to 100%, degraded up to some higher multiple, sheds above that, and finally fails. Without degradation the curve is sharper.

## Relationship to existing wiki concepts

### Degradation and [[fault-tolerance]]

Graceful degradation is one of the canonical fault-tolerance patterns. The system remains useful in the presence of a fault (the fault being "we don't have enough capacity right now") by partially serving rather than fully failing. This generalises beyond overload: a service might degrade when a dependency is down (skip the personalisation step but still render the page), when a datacenter is draining, or when a shard is unavailable.

### Degradation and [[circuit-breaker]] fallbacks

Newman and Nygard's [[circuit-breaker]] page lists "graceful degradation — serve a cached or stale value, return a default, show a 'we couldn't personalise this page' banner" as the first-choice fallback behaviour when the breaker is open. This page is the Chapter 21 statement of the same idea applied to the *own-task-is-overloaded* case rather than the *downstream-is-broken* case. Structurally identical: a planned cheaper path the system can fall back to.

### Degradation and [[ssl-termination]] / [[caching-layer]]

Burns's edge-tier [[caching-layer]] is a standing degradation mechanism: serving from cache absorbs load that would otherwise go to the canonical store. If the cache is always warm, every request benefits; if the cache is consulted only under load, it is graceful degradation made explicit. The architectural question is which mode you want — cache-always as a capacity multiplier, or cache-as-fallback as a degradation path.

### Degradation and [[error-budget]]

A request served with degraded quality is not the same as a fully-successful request for SLO purposes. Chapter 4's SLI standardisation work is what lets a service distinguish the two: "availability-as-yield" can count a degraded response differently from a full one. If degradation is accidentally indistinguishable from success, the SLO obscures the degradation rate — the wrong incentive.

### Degradation as cascade prevention (Chapter 22)

Chapter 22 names graceful degradation as the second-priority overload defence, after load testing (source: chapter-22-addressing-cascading-failures.md). The chapter's framing is that a service capable of degrading gracefully has *a larger range of useful operation* before it needs to reject entirely — it serves correctly at 100% of capacity, degrades between 100% and some higher multiple, sheds above that, and only then starts failing.

Chapter 22 also includes the warning that degraded code paths, being rarely used, tend to rot (source: chapter-22-addressing-cascading-failures.md):

> Remember that the code path you never use is the code path that (often) doesn't work. In steady-state operation, graceful degradation mode won't be used, implying that you'll have much less operational experience with this mode and any of its quirks, which increases the level of risk. You can make sure that graceful degradation stays working by regularly running a small subset of servers near overload in order to exercise this code path.

And a further caveat about degraded-mode complexity:

> Complex load shedding and graceful degradation can cause problems themselves — excessive complexity may cause the server to trip into a degraded mode when it is not desired, or enter feedback cycles at undesired times. Design a way to quickly turn off complex graceful degradation or tune parameters if needed.

The Shakespeare narrative at the chapter's close is the worked example: graceful degradation strips pictures and maps when the Asian datacenter is overloaded, buying the SREs time to respond with capacity additions. Degradation didn't prevent the cascade but kept the service partially useful during it.

### Degradation and [[request-criticality]]

Criticality and degradation compose: under pressure, `SHEDDABLE` traffic might be degraded or shed, while `CRITICAL_PLUS` traffic still gets the full path. The degradation curve and the criticality ladder layer on top of each other — higher criticality gets the full response longer before being degraded, and gets the degraded response longer before being shed.

### Make-children-cry switches ([[norad-tracks-santa|NORAD Tracks Santa]])

SRE Chapter 27 names the kill switches that degrade a user-facing experience to protect backend services "**Make-children-cry switches**" — deliberately dark humour, so on-call engineers remember activation has a real user cost and shouldn't be first-resort. The 2011 NORAD Tracks Santa launch (Keyhole at 25x normal peak) is the case study. Graceful degradation paths are the structural form of the same trade-off: let a feature become partial or unavailable so the infrastructure survives the event.

## Related pages

- [[handling-overload]]
- [[load-shedding]]
- [[utilization-signals]]
- [[request-criticality]]
- [[circuit-breaker]]
- [[caching-layer]]
- [[fault-tolerance]]
- [[error-budget]]
- [[cascading-failure]]
- [[addressing-ongoing-cascading-failure]]
- [[norad-tracks-santa]]
- [[reliable-product-launches]]
- [[site-reliability-engineering]]
