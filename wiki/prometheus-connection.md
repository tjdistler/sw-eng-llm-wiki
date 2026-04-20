# Prometheus Connection

**Summary**: Chapter 10's explicit acknowledgement that the pre-Prometheus time-series monitoring ideas are now freely available outside Google through open-source tools — Prometheus most directly, plus Riemann, Heka, and Bosun. The design principles — variable collection, centralised rule evaluation, a unified time-series arena — carry across all of them.

**Sources**: `raw/site-reliability-engineering/chapter-10-practical-alerting-from-time-series-data.md`

**Last updated**: 2026-04-19

---

## The genealogy

Chapter 10 opens with a paragraph explicitly aimed at non-Googlers (source: chapter-10-practical-alerting-from-time-series-data.md):

> In recent years, monitoring has undergone a Cambrian Explosion: Riemann, Heka, Bosun, and Prometheus have emerged as open source tools that are very similar to Borgmon's time-series–based alerting. In particular, Prometheus shares many similarities with Borgmon, especially when you compare the two rule languages. The principles of variable collection and rule evaluation remain the same across all these tools and provide an environment with which you can experiment, and hopefully launch into production, the ideas inspired by this chapter.

Prometheus was founded by former Google engineers and explicitly modelled on the pre-Prometheus internal system. The footprint shows up throughout:

## What carries over

### The pull model with scraped metrics endpoints

Both systems **scrape** targets on a schedule, pulling metrics from an HTTP endpoint the target exposes. Prometheus's convention is `/metrics`; the internal precursor used `/varz`. Prometheus's format is more structured (type hints, labels, `#` comments) — but the paradigm is identical.

### The time-series arena + TSDB split

Prometheus's in-memory head block plus on-disk chunked blocks mirror the precursor's in-memory arena plus externally-archived TSDB. Both systems hold a horizon of recent data in RAM for fast queries and persist older data to cheaper storage.

### The rule language

The similarity Chapter 10 calls out explicitly. PromQL's operators are one-to-one descendants of the precursor's algebraic rule language: `rate(x[10m])`, `sum by (code)`, `sum without (instance)`, recording rules that produce named time-series, alerting rules with a `for 2m` minimum-duration clause. The design discipline — counters over gauges, sum-of-rates rather than rate-of-sums, the `task:http_requests:rate10m` naming convention — survives the port.

### Alertmanager — the name and the design

Prometheus's Alertmanager carries the name over unchanged. The responsibilities are the same: receive alert RPCs from one or more rule evaluators, deduplicate, group/fan-in by labelset, inhibit lower-priority alerts when higher-priority ones fire, and route to pagers / tickets / chat / email. See [[alertmanager]].

### Hierarchical federation

Prometheus federation — a higher-level Prometheus scraping aggregated series from lower-level Prometheus instances — implements exactly the topology-sharding pattern Chapter 10 documents (see [[monitoring-topology-sharding]]). Scraper-tier shards, DC aggregators, global aggregators: the shape Chapter 10 documents is the shape federated Prometheus deployments adopt in practice.

### Black-box monitoring as a companion

Just as the internal stack pairs a white-box scraper with a protocol prober (see [[prober]]), Prometheus ships with `blackbox_exporter` for the same purpose.

## What doesn't cleanly carry over

A few features of the pre-Prometheus system do not carry over (either because they're Google-specific, or because the Prometheus ecosystem solves them differently):

- **Service discovery from an internal naming service** — the precursor used Google's naming service to find targets dynamically. Prometheus uses its own SD integrations (Kubernetes, Consul, EC2, file-based, etc.) for the equivalent.
- **Automatic metrics-endpoint registration in every binary** — a Google-language-library feature, not an ecosystem convention. The Prometheus client libraries are opt-in per language.
- **Streaming protocol between instances** — Prometheus federation uses HTTP scrape of aggregated series rather than a dedicated streaming protocol. Newer remote-write protocols close some of the gap.
- **Internal CI pipeline for rule configuration** — Google's rule-test / package / ship / validate flow is an internal release-engineering service. Prometheus users build equivalent pipelines themselves (e.g. `promtool test rules`, GitOps deployment).

## What the chapter wants non-Googlers to take away

Chapter 10 explicitly names its audience:

> The principles of variable collection and rule evaluation remain the same across all these tools and provide an environment with which you can experiment, and hopefully launch into production, the ideas inspired by this chapter.

Put differently: the Chapter 10 material isn't archaeology. It's a practical guide to operating any modern time-series monitoring stack, because the core ideas survived the transition to open source essentially unchanged.

## Cross-book connections

- [[monitoring-and-observability]] (Newman) — Newman lists Prometheus (implicitly via metrics) as one of the monitoring toolbox pieces; this page is the deeper why.
- [[unified-monitoring-interface]] (Burns) — Burns's canonical worked example is a Prometheus exporter as an adapter container; that's the containerised realisation of the universal metrics-endpoint convention.
- [[adapter-pattern]] (Burns) — adapter containers bridge heterogeneous apps to the Prometheus scrape standard; Google's internal approach solved the same problem inside every binary.
- [[sre-monitoring-outputs]] — the three-output taxonomy is what Prometheus + Alertmanager routes into by default.

## Related pages

- [[alertmanager]]
- [[prober]]
- [[monitoring-topology-sharding]]
- [[monitoring-and-observability]]
- [[site-reliability-engineering]]
