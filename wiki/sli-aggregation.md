# SLI Aggregation

**Summary**: Raw SLI measurements are almost always aggregated over a window into a rate, average, or percentile. The choice of window and statistic is load-bearing: poorly chosen aggregation hides burstiness, tail latencies, and the long-skewed distributions real systems actually produce.

**Sources**: `raw/site-reliability-engineering/chapter-04-service-level-objectives.md`

**Last updated**: 2026-04-17

---

## Why aggregation matters

Even the simplest-looking metric hides aggregation choices. "Requests per second" implicitly aggregates over *some* window — once-per-second sampling vs averaging over a minute produces different numbers (source: chapter-04-service-level-objectives.md).

The chapter's illustrative case: a system serving **200 requests/s in even-numbered seconds and 0 in odd-numbered seconds** has the same minute-averaged load as a system serving a constant 100 requests/s — but the instantaneous burst load is twice as large. A per-minute average erases that fact, and erases the capacity question it should be raising.

## Averages hide the tail

Averaging request latency seems attractive but obscures the long tail. Most requests can be fast while a minority are much slower. The chapter points to its Figure 4-1: **typical request 50 ms; top 5% run 20x slower** (1 s). Monitoring on average latency would show no change over the course of a day when in fact tail latency was changing significantly (source: chapter-04-service-level-objectives.md).

Most metrics are better thought of as **distributions rather than averages**.

## Use percentiles

Percentiles let you reason about distribution shape:

- A **high-order percentile** (p99, p999) shows a plausible worst-case value.
- The **median** (p50) shows the typical case.

The higher the variance in response times, the more typical user experience is affected by long-tail behaviour — an effect exacerbated at high load by queueing effects. User studies show people prefer a **slightly slower but steady** system to one with high variance (source: chapter-04-service-level-objectives.md). Some SRE teams therefore focus only on high percentiles: if p999 is good, the typical experience certainly is.

See [[response-time-percentiles]] for the broader treatment including Amazon's p999 rationale and tail latency amplification in fan-out systems.

## A note on statistical fallacies

Chapter 4 warns against assuming data is normally distributed without checking (source: chapter-04-service-level-objectives.md):

- Response times are **skewed by construction**: no request can respond in less than 0 ms, and a timeout at 1000 ms caps any successful response below that.
- **Mean and median are frequently far apart**, not close.
- A process that takes action on "outliers" (for example, restarting a server with high request latency) may act too often or not often enough if the underlying distribution isn't what was assumed.

Work with percentiles rather than means, and verify distribution assumptions before building alerting on them.

## Aggregation intervals, regions, frequency

Even within percentiles there are choices to make: over what **window** is the percentile computed (1 minute? 5 minutes? 1 hour?); over what **region** (one cluster? all clusters?); at what **frequency** are measurements sampled? These choices should be standardised — see [[sli-standardization]].

## Percentiles don't average

A mathematical pitfall worth naming: **percentiles cannot be averaged across machines or time windows**. The correct method is to add histograms and compute percentiles from the combined histogram. Approximation algorithms like forward decay, t-digest, and HdrHistogram handle this efficiently for rolling windows (source: [[response-time-percentiles]] from Kleppmann).

## Related pages

- [[service-level-indicator]]
- [[service-level-objective]]
- [[sli-standardization]]
- [[response-time-percentiles]]
- [[tail-latency-amplification]]
- [[availability-measurement]]
