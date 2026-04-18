# Monitoring Simplicity

**Summary**: Monitoring systems tend toward runaway complexity — alerts on every percentile, dashboards for every possible cause, dependency hierarchies everywhere. Google SRE deliberately pushes the other way: simple, fast, loosely-coupled monitoring with better post-hoc analysis tools alongside.

**Sources**: `raw/site-reliability-engineering/chapter-06-monitoring-distributed-systems.md`

**Last updated**: 2026-04-17

---

## The complexity trap

Chapter 6 lists the failure mode (source: chapter-06-monitoring-distributed-systems.md):

> Your system might end up with the following levels of complexity:
> - Alerts on different latency thresholds, at different percentiles, on all kinds of different metrics
> - Extra code to detect and expose possible causes
> - Associated dashboards for each of these possible causes

The result: "so complex that it's fragile, complicated to change, and a maintenance burden." Like any other software system, monitoring rots when over-engineered.

## The three simplicity guidelines

Chapter 6 offers three explicit rules for pruning a monitoring system:

1. **The rules that catch real incidents most often should be as simple, predictable, and reliable as possible.**
2. **Configuration that is rarely exercised (e.g. less than once a quarter)** is a candidate for removal. Rules that never fire aren't paying rent.
3. **Signals that are collected but not exposed in any prebaked dashboard nor used by any alert** are candidates for removal. Dead metrics are liabilities too.

## Avoid magic

The Chapter 6 stance on machine learning and causal inference in monitoring:

> We avoid "magic" systems that try to learn thresholds or automatically detect causality.

The counterexample they allow: rules that detect unexpected changes in end-user request rates — kept as simple as possible, but valuable because they give very quick detection of a very simple, severe anomaly. Other uses of monitoring data (capacity planning, traffic prediction) can tolerate more fragility and thus more complexity, because they're not on the paging critical path.

## Limit dependency hierarchies

Dependency-aware alerting ("if the database is slow, alert for a slow database; otherwise, alert for the slow website") sounds elegant but is rarely used at Google:

- Dependency rules work well only on very stable parts of the system (e.g. "if a datacenter is drained, don't alert on its latency").
- Broad dependency rules are eaten alive by continuous refactoring — the dependencies keep changing.

So Google keeps dependency-reliant rules to a minimum.

## Keep distinct systems distinct

A corollary simplicity rule: don't combine monitoring with adjacent concerns.

> It can be tempting to combine monitoring with other aspects of inspecting complex systems, such as detailed system profiling, single-process debugging, tracking details about exceptions or crashes, load testing, log collection and analysis, or traffic inspection. While most of these subjects share commonalities with basic monitoring, blending together too many results in overly complex and fragile systems.

The recommendation is **maintaining distinct systems with clear, simple, loosely coupled points of integration** — for example, using web APIs that pull summary data in a format that can remain constant over time.

Chapter 6 notes that in practice Google's monitoring is several binaries, but people typically learn about all of them — the loose coupling is structural, not a user-facing boundary.

## Keep the paging path especially simple

The elements of a monitoring system that direct to a pager need to be **very simple and robust**. Rules that generate alerts for humans should be simple to understand and represent a clear failure. This is why [[symptoms-vs-causes|symptom-oriented alerts]] are strongly preferred over cause-oriented ones: symptoms are a small, stable set; causes are many and churn with the code.

## The trend toward simpler systems

Chapter 6's overall direction:

> In general, Google has trended toward simpler and faster monitoring systems, with better tools for post hoc analysis.

The complement of simple alerting is *good debugging tools*: if a page fires and on-call needs to dig into causes, the tools for that dig can be as rich as you like — they're not on the alerting critical path.

## Cross-book connections

- [[sre-monitoring-outputs]] — the three-output taxonomy is itself a simplicity rule: there are only three things monitoring should produce.
- [[alert-philosophy]] — the actionable/urgent/novel/intelligence page criteria are the simplicity rule applied to pages specifically.
- [[accidental-complexity]] (Richards & Ford) — Brooks's framing; monitoring systems are a fertile source of accidental complexity.
- [[monitoring-and-observability]] (Newman) — observability tooling for unknown-unknowns is where the *post-hoc analysis* half of Chapter 6's stance lives.

## Related pages

- [[alert-philosophy]]
- [[symptoms-vs-causes]]
- [[sre-monitoring-outputs]]
- [[monitoring-resolution]]
- [[monitoring-and-observability]]
- [[accidental-complexity]]
- [[site-reliability-engineering]]
