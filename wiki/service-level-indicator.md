# Service Level Indicator

**Summary**: An SLI is a carefully defined quantitative measure of some aspect of the level of service being provided — request latency, error rate, throughput, availability, durability. The SLI is the *metric*; the [[service-level-objective|SLO]] is a target on that metric; the [[service-level-agreement|SLA]] is the contract around the SLO.

**Sources**: `raw/site-reliability-engineering/chapter-04-service-level-objectives.md`

**Last updated**: 2026-04-17

---

## Definition

> An SLI is a service level indicator — a carefully defined quantitative measure of some aspect of the level of service that is provided. (source: chapter-04-service-level-objectives.md)

Most services treat **request latency** as a key SLI. Other common SLIs:

- **Error rate** — typically a fraction of all received requests.
- **Throughput** — typically requests per second.
- **Availability** — the fraction of time the service is usable, often defined as the fraction of well-formed requests that succeed (sometimes called **yield**); see [[availability-measurement]].
- **Durability** — the likelihood data is retained over a long period of time; equally important for data storage systems.
- **Correctness** — was the right answer returned? Often a property of the data rather than the infrastructure, so frequently outside SRE's remit, but still worth tracking as a system-health indicator.

## Direct vs proxy SLIs

Ideally the SLI directly measures the service level of interest. In practice a proxy is often needed because the desired measure is hard to obtain or interpret. Example from the chapter: **client-side latency** is more user-relevant than server-side latency, but may not be measurable — so server-side latency is used as a proxy (source: chapter-04-service-level-objectives.md).

## Collection: server-side vs client-side

Many SLIs are most naturally gathered on the **server side** using a monitoring system (Prometheus and its internal-Google ancestor) or periodic log analysis (for example, HTTP 500 responses as a fraction of all requests). But some systems need **client-side collection** because server-side metrics miss whole classes of user-visible problems. The chapter's illustrative case: concentrating on the Shakespeare search backend's response latency can miss slow page-render caused by the page's JavaScript — measuring *time to page usability in the browser* is a better proxy for user experience (source: chapter-04-service-level-objectives.md).

## What SLIs matter by service type

The chapter groups services into four categories with characteristic SLI sets (source: chapter-04-service-level-objectives.md):

| Service type | Typical SLIs |
|---|---|
| User-facing serving | availability, latency, throughput |
| Storage | latency, availability, durability |
| Big data / pipelines | throughput, end-to-end latency |
| All systems | correctness |

## Pick a handful, not everything

Don't use every metric your monitoring system can track as an SLI. Too many indicators dilute attention; too few leave parts of the system unexamined. **A handful of representative indicators is enough** to reason about a system's health (source: chapter-04-service-level-objectives.md). This is the indicator-level analogue of "have as few SLOs as possible" (see [[service-level-objective]]).

## Nines

High availability is commonly expressed as the number of **"nines"** — 99% is "2 nines," 99.999% is "5 nines," and Google Compute Engine's published target of 99.95% is "three and a half nines" (source: chapter-04-service-level-objectives.md). The dual view of this number — both time-based and request-success-rate — is covered on [[availability-measurement]].

## Aggregation

Raw SLI measurements are almost always **aggregated** over a measurement window into a rate, average, or percentile. The choice of window and statistic matters enormously: averages hide burstiness and tail latencies alike. See [[sli-aggregation]] for the full discussion.

## Standard definitions

Reusable templates for common SLIs save effort and make it easier for everyone to understand what a specific SLI means. See [[sli-standardization]].

## Related pages

- [[service-level-objective]]
- [[service-level-agreement]]
- [[sli-aggregation]]
- [[sli-standardization]]
- [[availability-measurement]]
- [[response-time-percentiles]]
- [[error-budget]]
- [[sre-monitoring-outputs]]
