# Monitoring Resolution

**Summary**: Different aspects of a system warrant different measurement granularities. The trick is to collect at high resolution on the server (via local sampling into buckets) and aggregate externally at lower frequency, getting sub-minute visibility without sub-minute collection cost.

**Sources**: `raw/site-reliability-engineering/chapter-06-monitoring-distributed-systems.md`

**Last updated**: 2026-04-17

---

## The granularity trade-off

Chapter 6 spells out three illustrative mismatches (source: chapter-06-monitoring-distributed-systems.md):

- **CPU at 1-minute resolution misses tail-latency-driving spikes.** A 15-second CPU spike won't show up in a 1-minute sample but it will drive user-visible latency.
- **Liveness probes at 1-second resolution are overkill for a 99.9% service.** 99.9% annual uptime tolerates ~9 hours of downtime — twice-a-minute success probing is sufficient.
- **Disk-fullness at 1-second resolution is wasteful for a 99.9% service.** Once every 1–2 minutes is enough.

The general point: high-resolution collection for everything is expensive to collect, store, and analyse. Match resolution to the question you're asking.

## The local-sample-then-aggregate trick

The clever Chapter 6 technique for getting sub-minute visibility without sub-minute collection cost:

1. **Record CPU utilisation every second** on the server.
2. **Bucket it** into 5%-granularity buckets, incrementing the appropriate counter each second.
3. **Aggregate every minute** externally — one scrape per minute per server, but carrying a full distribution of the 60 per-second samples.

You observe brief CPU hotspots *without* paying for 60x the scraping cost. The server does the high-frequency sampling; the monitoring system sees the distribution.

## Why this is a first-class concept

Sampling strategy interacts with every major Chapter 6 theme:

- **[[four-golden-signals]]**: saturation and latency both need distribution-aware sampling. Mean saturation hides per-node hotspots; mean latency hides the tail.
- **[[long-tail-latency]]**: exponentially-bucketed latency histograms are the same pattern applied to requests instead of server-state samples.
- **[[monitoring-simplicity]]**: this is one of the few places Chapter 6 endorses complexity, because the cost savings justify it and the pattern is reusable across metrics.

## Rule of thumb

The Chapter 6 framing:

> If your monitoring goal calls for high resolution but doesn't require extremely low latency, you can reduce these costs by performing internal sampling on the server, then configuring an external system to collect and aggregate that distribution over time or across servers.

The key phrase is "doesn't require extremely low latency": if you need to *alert* on a sub-minute event you still need sub-minute collection. But most observational questions — "was there a CPU spike last week?" — can be answered by pre-bucketed distributions at minute granularity.

## Cross-book connections

- [[unified-monitoring-interface]] (Burns) — the adapter-container realisation of server-local sampling and Prometheus-style bucketed histograms; the one-minute scrape interval of pull-based monitoring systems matches the aggregation cadence this pattern assumes.
- [[response-time-percentiles]] (Kleppmann) — Kleppmann's note that percentiles can be efficiently computed over rolling windows using approximation algorithms (forward decay, t-digest, HdrHistogram) is the same pattern scaled up.

## Related pages

- [[four-golden-signals]]
- [[long-tail-latency]]
- [[monitoring-simplicity]]
- [[unified-monitoring-interface]]
- [[site-reliability-engineering]]
