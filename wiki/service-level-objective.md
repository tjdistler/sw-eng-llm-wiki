# Service Level Objective

**Summary**: An SLO is the target reliability level for a service — the denominator from which an [[error-budget]] is derived. Picking the right SLO is a *product* decision, not a technical one, because 100% availability benefits nobody and costs a lot.

**Sources**: `raw/site-reliability-engineering/chapter-01-introduction.md`, `raw/site-reliability-engineering/chapter-03-embracing-risk.md`, `raw/site-reliability-engineering/chapter-04-service-level-objectives.md`, `raw/site-reliability-engineering/chapter-26-data-integrity-what-you-read-is-what-you-wrote.md`, `raw/site-reliability-engineering/chapter-30-embedding-an-sre-to-recover-from-operational-overload.md`

**Last updated**: 2026-04-17

---

## What an SLO is

A service level objective is a quantitative reliability target — for example, 99.99% availability over a 28-day window. It is the commitment the team is making and operating against; its complement (0.01% in the example) is the [[error-budget|error budget]] the team is allowed to spend on change and risk.

Chapter 1 introduces SLOs implicitly via the error-budget discussion: *a service that's 99.99% available is 0.01% unavailable. That permitted 0.01% unavailability is the service's error budget* (source: chapter-01-introduction.md). Later chapters develop SLOs, SLIs (service level indicators), and SLAs (service level agreements) in depth.

## Picking the target is not a technical question

The core Chapter 1 point: *what, then, is the right reliability target for the system? This actually isn't a technical question at all — it's a product question* (source: chapter-01-introduction.md). The product owner (or business) answers it with three considerations:

1. What level of availability will users be **happy with**, given how they use the product?
2. What **alternatives** exist for users dissatisfied with availability?
3. How does **usage** change at different availability levels?

Once the product makes this call, the SLO is locked and the SRE team derives its [[error-budget]] from it.

## Why not aim for 100%

**100% is the wrong reliability target for basically everything.** Exceptions Treynor Sloss calls out are safety-critical systems like pacemakers and anti-lock brakes (source: chapter-01-introduction.md). For ordinary software services, the marginal cost of reducing unavailability from 0.001% to 0% is enormous and the marginal user benefit is zero, because other systems in the path (laptop, home WiFi, ISP, power grid) collectively cap what the user can observe well below five nines.

## How the target is measured

Chapter 3 develops the measurement side in detail — see [[availability-measurement]]. The short version:

- The textbook **time-based formula** (`uptime / (uptime + downtime)`) is used industry-wide but breaks down for globally distributed services that are always partially up.
- Google instead defines availability as the **request success rate** (`successful requests / total requests`) over a rolling window, which generalises to non-serving systems (batch, pipeline, storage).

Google typically sets **quarterly availability targets** and tracks them weekly or daily so deviations can be spotted and fixed while there is still budget left (source: chapter-03-embracing-risk.md).

## The target as both minimum and maximum

Chapter 3 sharpens the "don't aim for 100%" point into a stronger claim:

> When we set an availability target of 99.99%, we want to exceed it, but not by much.

Substantially exceeding the target wastes opportunities to add features, pay down technical debt, or reduce operational cost. The SLO is therefore **both a floor and a ceiling** — the team should sit just above it, spending the rest of the [[error-budget]] on velocity. See [[risk-management-sre]] for the full argument.

## Picking the target per service

Chapter 3 walks through how the target is actually chosen for different service types — consumer services vs infrastructure services, with worked examples from Google Apps for Work, YouTube, Ads, and Bigtable. The framework (availability, failure shape, cost, other metrics) is catalogued on [[risk-tolerance]].

## Chapter 4: definition, shape, and target selection

Chapter 4 ("Service Level Objectives") develops SLO practice in detail and distinguishes the SLO from the [[service-level-indicator|SLI]] (the metric it is a target on) and the [[service-level-agreement|SLA]] (the contract around it).

### The shape of an SLO

> An SLO is a service level objective: a target value or range of values for a service level that is measured by an SLI. (source: chapter-04-service-level-objectives.md)

A natural structure for SLOs is therefore **SLI ≤ target** or **lower bound ≤ SLI ≤ upper bound**. Some SLOs are not yours to pick: incoming QPS from the outside world is determined by user demand, not engineering choice. Others — average request latency, for example — are under your control and the SLO serves as a forcing function for engineering investment.

### Objectives should specify how they're measured

Be explicit about what the SLO covers and under what conditions it's valid. The chapter's worked examples (source: chapter-04-service-level-objectives.md):

- `99% (averaged over 1 minute) of Get RPC calls will complete in less than 100 ms (measured across all the backend servers).`
- With SLI defaults (see [[sli-standardization]]) this shortens to `99% of Get RPC calls will complete in less than 100 ms.`

### Multiple targets for performance-curve shape

If the shape of the performance curve matters, specify **multiple SLO targets** (source: chapter-04-service-level-objectives.md):

- 90% of Get RPC calls will complete in less than 1 ms.
- 99% of Get RPC calls will complete in less than 10 ms.
- 99.9% of Get RPC calls will complete in less than 100 ms.

### Separate SLOs for heterogeneous workloads

If you have latency-sensitive interactive clients and throughput-oriented bulk clients sharing the same service, give each class its own SLOs (source: chapter-04-service-level-objectives.md):

- 95% of throughput clients' Set RPC calls will complete in < 1 s.
- 99% of latency clients' Set RPC calls with payloads < 1 kB will complete in < 10 ms.

This is the SLO-level expression of the service-tier strategy [[risk-tolerance]] describes for infrastructure services.

### Work from desired objectives backward to indicators

> Start by thinking about (or finding out!) what your users care about, not what you can measure. (source: chapter-04-service-level-objectives.md)

If you start with what's easy to measure you end up with less useful SLOs. Often what users care about is hard to measure, so the SLI ends up approximating it. Working from the desired objective backward to the SLI produces better outcomes than the reverse.

### Choosing targets — lessons

Chapter 4 names five rules for target selection (source: chapter-04-service-level-objectives.md):

1. **Don't pick a target based on current performance.** Doing so locks you into supporting a system that cannot be improved without significant redesign, and may require heroic effort to hit.
2. **Keep it simple.** Complicated SLI aggregations obscure performance changes and are hard to reason about.
3. **Avoid absolutes.** Infinite scale, zero latency, always-available — unrealistic, expensive, and probably better than what users would actually notice.
4. **Have as few SLOs as possible.** Defend each one: if you can't ever win a priority argument by quoting it, the SLO isn't worth having. Not every product attribute is amenable to an SLO ("user delight" isn't).
5. **Perfection can wait.** Start loose and tighten over time; the reverse (start strict, relax when you miss) is worse.

SLOs are a major driver in prioritising work for SREs and product developers — a good SLO is a legitimate forcing function, a bad one wastes engineering effort or produces a bad product. **SLOs are a massive lever: use them wisely** (source: chapter-04-service-level-objectives.md).

### Error budget as "an SLO for meeting other SLOs"

Chapter 4 restates the [[error-budget|error-budget]] idea in a compact way: it is **unrealistic and undesirable to insist that SLOs be met 100% of the time**, so allow an error budget (a rate at which SLOs can be missed) and track it at daily, weekly, and quarterly cadences. *An error budget is just an SLO for meeting other SLOs* (source: chapter-04-service-level-objectives.md).

### SLIs and SLOs in the control loop

SLIs and SLOs are elements of the control loop used to manage services (source: chapter-04-service-level-objectives.md):

1. Monitor and measure the system's SLIs.
2. Compare SLIs to SLOs; decide if action is needed.
3. If action is needed, figure out what.
4. Take that action.

Without the SLO, step 2 has no reference — you cannot tell whether action is required.

### Publishing SLOs sets expectations

Publishing SLOs sets expectations for users and prospective users. Without this, over-reliance and under-reliance both occur — see [[slo-expectations]] for the two tactics (safety margin, don't overachieve) and the [[chubby]] over-reliance case study.

## Data-integrity SLOs (Chapter 26)

Chapter 26 sharpens the "SLOs for availability" default by arguing that **every service has independent uptime and data-integrity requirements**, even when they're implicit (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md). The contrast is stark:

- 99.99% uptime leaves room for ~1 hour of downtime per year — a high bar.
- 99.99% of "good bytes" in a 2 GB artifact means up to 200 KB corruption — catastrophic for executables and databases.

From the user's perspective, data integrity must be effectively **100%** during the accessible lifetime of the object. So if the SLO framework is silent on data integrity, teams will under-invest in it and find out at recovery time.

Chapter 26 proposes defining data-availability SLOs **per failure-mode class** (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md):

> Teams define SLOs for data availability in a variety of failure modes. A team practices and demonstrates their ability to meet those SLOs.

Different [[data-integrity-failure-modes|failure modes]] warrant different recovery targets — a single user's accidental deletion should be recoverable in minutes, a site catastrophe in hours to days. The SLO is the contract with the user for each class; the [[recovery-testing|continuously-tested recovery pipeline]] is how the team proves it can meet each one. Availability of recovered data — not byte preservation — is the measurable outcome.

See [[data-availability-vs-integrity]] for the means-vs-goal framing and [[data-integrity-sre]] for the full Chapter 26 treatment.

## The SLO as the first lever for rescuing an overloaded team (Chapter 30)

Chapter 30's [[embedding-sre|embedded-SRE rescue pattern]] places the SLO at the very top of the Phase 3 "driving change" sequence, with an unusually strong claim (source: chapter-30-embedding-an-sre-to-recover-from-operational-overload.md):

> An SLO is probably the single most important lever for moving a team from reactive ops work to a healthy, long-term SRE focus. If this agreement is missing, no other advice in this chapter will be helpful.

The operative phrase is *if this agreement is missing, no other advice in this chapter will be helpful.* Chapter 30 is a twelve-step rescue playbook, and the chapter authors are willing to say that without an SLO, none of the subsequent steps land. The prescription: *if you find yourself on a team without SLOs, first read Chapter 4, then get the tech leads and management in a room and start arbitrating.*

The reasoning is consistent with the [[error-budget|error-budget]] argument but specific to the overloaded-team case: without an SLO there is no quantitative ground for *any* later decision — whether to push back on a release, whether an alert is legitimate, whether an incident's follow-up is worth prioritising, whether a "critical" system actually warrants the operational load it demands. Every later conversation devolves into intuition-vs-intuition, which is exactly the dynamic [[ops-mode]] runs on. The SLO is what makes principled reasoning (see [[explaining-reasoning]]) possible in the first place.

This also reframes Chapter 4's general "SLOs are a massive lever" statement: in the specific context of a team already in operational overload, the SLO is not *a* lever — it is the *prerequisite* lever for every other lever Chapter 30 describes.

## Connection to the error budget

SLO and error budget are two sides of the same coin:

- The **SLO** is the reliability floor.
- The **error budget** is the permitted distance below "perfect" (`1 − SLO`).

Pacing a service against its SLO means watching the error budget's burn rate: if you're spending it too quickly, slow down; if you have surplus, take more risk on launches. See [[error-budget]] for how the budget is spent.

## Related pages

- [[service-level-indicator]]
- [[service-level-agreement]]
- [[sli-aggregation]]
- [[sli-standardization]]
- [[slo-expectations]]
- [[error-budget]]
- [[risk-management-sre]]
- [[risk-tolerance]]
- [[availability-measurement]]
- [[sre-discipline]]
- [[sre-tenets]]
- [[reliability]]
- [[data-integrity-sre]]
- [[data-availability-vs-integrity]]
- [[data-integrity-failure-modes]]
- [[recovery-testing]]
- [[embedding-sre]]
- [[operational-overload]]
- [[ops-mode]]
- [[explaining-reasoning]]
