# Availability Measurement

**Summary**: To manage [[risk-management-sre|risk]] quantitatively, SRE reduces "how reliable is this service?" to an objective metric. Chapter 3 contrasts the traditional time-based availability formula with Google's preferred request-success-rate formulation, which generalises better to globally distributed systems and non-serving workloads.

**Sources**: `raw/site-reliability-engineering/chapter-03-embracing-risk.md`

**Last updated**: 2026-04-17

---

## Why one metric

Service failures can hurt in many ways — user dissatisfaction, loss of trust, direct or indirect revenue loss, brand damage, bad press. Most of these are hard or impossible to measure directly (source: chapter-03-embracing-risk.md). To keep risk tractable and consistent across the many services Google runs, SRE **focuses on unplanned downtime** and expresses risk as the acceptable level of it.

Unplanned downtime is usually expressed as **nines of availability** — 99.9%, 99.99%, 99.999% — where each additional nine is an order-of-magnitude improvement toward 100%.

## Time-based availability

The textbook formula treats availability as a fraction of clock time:

> availability = uptime / (uptime + downtime)

Over a year, a 99.99% target permits **52.56 minutes of downtime** (source: chapter-03-embracing-risk.md). Appendix A of the book provides the full table.

This formulation assumes the service is either "up" or "down" at any given moment, which works for single-location systems but breaks down for globally distributed ones.

## Request-success-rate (aggregate) availability

At Google, time-based availability is usually not meaningful because services are globally distributed and almost always serving at least some traffic somewhere:

> Our approach to fault isolation makes it very likely that we are serving at least a subset of traffic for a given service somewhere in the world at any given time (i.e., we are at least partially "up" at all times).

So SRE defines availability as the **request success rate** over a rolling window:

> availability = successful requests / total requests

Example: a system serving 2.5M requests/day with a 99.99% daily target can serve up to **250 errors** and still hit the target (source: chapter-03-embracing-risk.md).

This yield-based metric approximates the end-user experience of unplanned downtime — from the user's perspective, a failed request looks like downtime regardless of whether some other request somewhere else succeeded.

## Not all requests are equal

Chapter 3 acknowledges the obvious caveat: failing a new-user sign-up request is materially different from failing a background poll for new email. Aggregate success rate smooths over this distinction, and in most cases that smoothing is an acceptable approximation. When it is not, the practice is to measure sub-streams separately (e.g., authentication success rate as a distinct SLI).

## Generalising to non-serving systems

Because the metric is about successful units of work rather than clock time, it extends cleanly to batch, pipeline, storage, and transactional systems:

- A batch ETL moving a customer database into a warehouse has a well-defined notion of "records successfully/unsuccessfully processed".
- A pipeline has per-message success/failure.
- A storage system has per-operation success/failure.

The same availability-as-success-rate formula applies (source: chapter-03-embracing-risk.md).

## Tracking cadence

Google usually sets **quarterly availability targets** and tracks performance against them on a weekly or daily basis. This lets the team manage to a high-level objective by spotting and fixing meaningful deviations as they arise (source: chapter-03-embracing-risk.md). Chapter 4 of the book develops SLI/SLO practice in more depth.

## Relationship to the error budget

The availability number is the denominator; the [[error-budget]] is what's left of it after actual failures consume some. The request-success-rate framing is what makes the budget computable at a rolling cadence — you can look at the last day and know exactly how much budget you burned.

## Related pages

- [[service-level-objective]]
- [[error-budget]]
- [[risk-management-sre]]
- [[risk-tolerance]]
- [[reliability]]
- [[response-time-percentiles]]
