# SLOs Set Expectations

**Summary**: Publishing [[service-level-objective|SLOs]] sets expectations for how a service will perform, which reduces unfounded complaints and helps prospective users decide if a service fits their use case. Two tactics keep those expectations aligned with reality: a safety-margin between internal and advertised SLOs, and deliberately not overachieving.

**Sources**: `raw/site-reliability-engineering/chapter-04-service-level-objectives.md`

**Last updated**: 2026-04-17

---

## Why expectations matter

Without an explicit SLO, users develop their own beliefs about desired performance. Those beliefs may bear no relation to what the designers of the service intended (source: chapter-04-service-level-objectives.md). Two failure modes follow:

- **Over-reliance** — users believe the service will be more available than it actually is, and design their own system assuming that.
- **Under-reliance** — prospective users believe the system is flakier than it really is, and don't adopt it.

The chapter calls out a concrete over-reliance episode: [[chubby]]. Global Chubby's true failures were so rare that service owners added dependencies as if it could never go down. When it did, the dependents couldn't cope (source: chapter-04-service-level-objectives.md).

## Tactic 1: keep a safety margin

Use a **tighter internal SLO** than the one advertised externally. The buffer gives you room to:

- Respond to chronic problems before they become externally visible.
- Absorb reimplementations that trade some performance for cost or maintainability without disappointing users.

The external number is what users build against; the internal number is what the team engineers against.

## Tactic 2: don't overachieve

Users build on the **reality** of what you offer, not what you say you'll supply — particularly for infrastructure services. If actual performance substantially exceeds the advertised SLO, users come to rely on the actual performance (source: chapter-04-service-level-objectives.md). Later degradation back toward the advertised number then looks like an outage.

Three techniques to avoid over-dependence:

1. **Deliberate planned outages** — Google's Chubby introduced planned outages specifically in response to being overly available. A controlled outage is synthesized in any quarter where a true failure hasn't dropped availability below target, flushing out unreasonable dependencies shortly after they are added (source: chapter-04-service-level-objectives.md).
2. **Throttle some requests** — cap the service so it cannot exceed its SLO even when capacity exists.
3. **Design for no bonus under light load** — don't let the system be faster at 10% capacity than at 80%.

## Connection to failure injection

Deliberate planned outages are *not* the same thing as [[robustness-and-resiliency-at-scale|chaos-style failure injection]], though they can both help set expectations. The book's Ch 4 footnote: failure injection [Ben12] "serves a different purpose, but can also help set expectations" (source: chapter-04-service-level-objectives.md).

## The "as both floor and ceiling" framing

This page is the practical expression of the Chapter 3 claim that **the SLO is both a minimum and a maximum** (see [[service-level-objective]] and [[risk-management-sre]]). If you consistently exceed target, the message is not "great job" — it is either that the target is too loose or that you are over-spending reliability effort that could go into velocity.

## Related pages

- [[service-level-objective]]
- [[error-budget]]
- [[risk-management-sre]]
- [[chubby]]
- [[service-level-agreement]]
