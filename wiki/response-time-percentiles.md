# Response Time Percentiles

**Summary**: Percentiles — not mean response time — are the correct way to reason about service performance, because they capture the distribution of user experience rather than a misleading aggregate.

**Sources**: `raw/designing-data-intensive-applications/chapter-01-reliable-scalable-and-maintainable-applications.md`, `raw/designing-distributed-systems/chapter-07-scattergather.md`, `raw/site-reliability-engineering/chapter-04-service-level-objectives.md`

**Last updated**: 2026-04-17

---

## Latency vs response time

These terms are often used interchangeably but are distinct:

- **Response time**: what the client observes — processing time + network delays + queuing delays
- **Latency**: the time a request spends *waiting* to be handled, before processing begins

Response time is the metric that matters from the user's perspective. (source: chapter-01)

## Why averages mislead

Response time is not a single number — it is a **distribution**. Even identical requests vary in response time due to: context switches, network packet loss and TCP retransmission, garbage collection pauses, page faults, mechanical server vibrations, and other random causes.

The arithmetic mean hides this distribution. It does not tell you how many users experienced a given delay. A single very slow request can inflate the mean without the median budging. (source: chapter-01)

## Percentiles

Sort all response times from fastest to slowest. The percentile is the value below which a given fraction of requests fall:

| Percentile | Meaning |
|---|---|
| **p50** (median) | Half of requests are faster than this, half are slower. The "typical" user experience. |
| **p95** | 95 of 100 requests are faster; 5 in 100 are slower |
| **p99** | 99 of 100 requests are faster; 1 in 100 are slower |
| **p999** | 999 of 1000 requests are faster; 1 in 1000 are slower |

High percentiles (p95, p99, p999) are called **tail latencies**.

## Why tail latencies matter

Amazon specifies internal service response time requirements at p999, even though it only affects 1 in 1,000 requests — because the slowest requests tend to come from the most valuable customers (those with the most data, i.e. the most purchases). Amazon observed that a 100 ms increase in response time reduces sales by 1%; a 1-second slowdown reduces a customer satisfaction metric by 16%. (source: chapter-01)

At p9999 (1 in 10,000), optimizing further was deemed too expensive and yielding diminishing returns.

## Tail latency amplification

In systems where a single end-user request fans out to multiple backend calls, tail latencies compound. Even if only 1% of individual backend calls are slow, the probability that *at least one* of N parallel calls is slow grows quickly with N. This effect — **tail latency amplification** — means that overall end-user latency worsens faster than individual service latency would suggest. (source: chapter-01)

Brendan Burns's *Designing Distributed Systems* Chapter 7 treats this as the central design concern of the [[scatter-gather-pattern]], with concrete arithmetic: a backend p99 of 2 s becomes the system's p95 at 5 leaves and is practically guaranteed at 100 leaves (source: raw/designing-distributed-systems/chapter-07-scattergather.md). The dedicated page [[tail-latency-amplification]] covers the math, the straggler framing, the availability-compounding parallel, and the common mitigations (hedged requests, bounded leaf count, leaf replication, approximate gather).

## Head-of-line blocking

A server can process only a limited number of requests in parallel (bounded by CPU cores). A small number of slow requests can hold up the processing of subsequent fast requests. From the client's perspective, those subsequent requests appear slow even though their own processing time is short. This is **head-of-line blocking**. It is why response time must be measured on the **client side**, not just the server side. (source: chapter-01)

## Load testing and measurement pitfalls

When load-testing scalability, the load-generating client must send requests independently of response time — not waiting for one request to complete before sending the next. Waiting artificially shortens queues in the test environment, producing optimistic measurements that don't reflect production behavior.

Percentiles should not be averaged across machines or time windows — averaging percentiles is mathematically meaningless. The correct method is to **add histograms** and compute percentiles from the combined histogram. Approximation algorithms (forward decay, t-digest, HdrHistogram) can compute percentiles efficiently over rolling windows without keeping every data point. (source: chapter-01)

## SLOs and SLAs

Percentiles are the standard language of service level objectives and agreements:

- **[[service-level-objective|SLO]]** — internal target, e.g. p50 < 200 ms and p99 < 1 s
- **[[service-level-agreement|SLA]]** — contractual commitment to clients; violations may entitle customers to refunds

SRE's Chapter 4 makes the case for percentiles directly: averages hide the tail, most metrics are better thought of as distributions, and user studies show people prefer a slightly slower *steady* system to one with high variance — so if p999 is good, the typical experience is certainly going to be (source: chapter-04-service-level-objectives.md). See [[sli-aggregation]] for the SRE-side aggregation discipline.

## Related pages

- [[scalability]]
- [[load-parameters]]
- [[scaling-approaches]]
- [[tail-latency-amplification]]
- [[scatter-gather-pattern]]
- [[service-level-indicator]]
- [[service-level-objective]]
- [[sli-aggregation]]
