# Long Tail Latency

**Summary**: The slowest few percent of requests — the tail — typically matter more than the average, because users depending on multiple backend services see the tail of each one compound. Measure distributions (histograms), not means.

**Sources**: `raw/site-reliability-engineering/chapter-06-monitoring-distributed-systems.md`

**Last updated**: 2026-04-17

---

## Why the tail matters

Chapter 6 opens with the canonical example (source: chapter-06-monitoring-distributed-systems.md):

> If you run a web service with an average latency of 100 ms at 1,000 requests per second, 1% of requests might easily take 5 seconds. If your users depend on several such web services to render their page, the 99th percentile of one backend can easily become the median response of your frontend.

Two consequences fall out of this:

1. **The mean is a poor predictor of user experience** when requests aren't uniformly distributed. 1% of requests at 10x the average means the rest of your requests are about twice as fast as the average; but if you don't measure the distribution, that is "just hopeful thinking."
2. **Latency compounds as fan-out increases.** A page backed by N backends sees the worst of N latencies; the p99 of a backend becomes something much worse than p99 in aggregate.

## Histograms, not means

The Chapter 6 instrumentation rule:

> The simplest way to differentiate between a slow average and a very slow "tail" of requests is to collect request counts bucketed by latencies (suitable for rendering a histogram), rather than actual latencies.

Bucket boundaries should be distributed **approximately exponentially** (e.g. factors of ~3): 0–10 ms, 10–30 ms, 30–100 ms, 100–300 ms, 300 ms – 1 s, and so on. Exponential buckets give you usable resolution across multiple orders of magnitude without exploding the bucket count.

## Leading indicator of saturation

The [[four-golden-signals]] page notes that **latency increases at high percentiles are often a leading indicator of saturation** — before CPU or memory metrics cross their thresholds. Measuring the p99 over a short window (1 minute, say) gives early warning of saturation that point-in-time resource metrics would miss.

This is the symptom/cause interaction: tail latency is a symptom that foreshadows a saturation cause.

## Measuring error latency separately

A related Chapter 6 rule (from the latency golden signal): **track latency of successful and failed requests separately**. A fast error (HTTP 500 returned in 1 ms after a backend-connection failure) would otherwise deflate the overall latency number; a slow error (timeout after 30 s) is worse than a fast one and must not be filtered out silently.

## The Bigtable case study

Chapter 6's Bigtable case study is a concrete illustration. For years Bigtable's SLO was based on *mean* client performance. Because the worst 5% of requests were much slower than the rest, the mean was driven by that tail, and email/paging alerts fired voluminously — many false, a few real, all consuming engineering time.

The remedy involved (among other things) switching to the **75th-percentile** latency target, which allowed the team to stop firefighting and actually fix the long-tail problems in Bigtable and the storage stack beneath it.

## Cross-book connections

- [[response-time-percentiles]] (Kleppmann) — the fullest treatment of percentiles, head-of-line blocking, tail-latency-amplification, and the "don't average percentiles" rule. Chapter 6's argument is the SRE-side restatement.
- [[tail-latency-amplification]] (Burns) — Burns's Chapter 7 arithmetic on how a backend p99 of 2 s becomes the scatter-gather system's p50 at modest fan-out. Chapter 6's "99th percentile of one backend becomes the median of your frontend" is the same observation in the single-layer case.
- [[sli-aggregation]] (SRE Ch 4) — the SLI-side treatment of histograms, percentiles vs averages, and the dangers of statistical fallacies. Chapter 6 is the instrumentation-side view; Chapter 4 is the SLI-and-SLO side.

## Related pages

- [[four-golden-signals]]
- [[response-time-percentiles]]
- [[tail-latency-amplification]]
- [[sli-aggregation]]
- [[monitoring-resolution]]
- [[site-reliability-engineering]]
