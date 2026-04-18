# Borgmon

**Summary**: Google's monitoring program. Many Borgmon instances run in production and periodically **scrape** metrics from monitored servers, storing them in an in-memory time-series arena for alerting, historical graphing, and capacity planning. The internal ancestor of Prometheus.

**Sources**: `raw/site-reliability-engineering/chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md`, `raw/site-reliability-engineering/chapter-10-practical-alerting-from-time-series-data.md`

**Last updated**: 2026-04-17

---

## What Borgmon does

Google runs many Borgmon instances (source: chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md):

- Periodically **scrapes metrics** from monitored servers — each server exposes its own metrics on its built-in HTTP diagnostic endpoint.
- Stores the metrics for both instantaneous alerting and historical analysis.

The scrape-based pull model is the same pattern Prometheus later adopted. SRE Chapter 10 covers Borgmon in detail; that material fills out this page.

## The three uses the chapter calls out

Chapter 2 lists three distinct uses of the monitoring data (source: chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md):

1. **Alerting for acute problems** — fires pages for incidents that need human intervention.
2. **Before-and-after comparison** — did a software update make the server faster?
3. **Resource-consumption-over-time** — the trend data that feeds [[capacity-planning]].

The third point is load-bearing for the rest of the book: capacity planning depends on having historical metrics to extrapolate demand from.

## How Borgmon is built (Chapter 10)

Chapter 10 (Jamie Wilkinson) is the full treatment. Borgmon was built in 2003, shortly after [[borg]], to monitor Borg-scheduled services (source: chapter-10-practical-alerting-from-time-series-data.md). Its defining bet — Google's radical-at-the-time break from the custom-check-script model — was to make **time-series collection a first-class role of the monitoring system** and to replace ad-hoc scripts with a **rich rule language** for manipulating time-series into charts and alerts.

The internal architecture has five loosely-coupled pieces, each covered on its own page:

- **[[varz-endpoints]]** — the `/varz` HTTP exposition format. Every Google binary auto-registers metrics to a built-in HTTP server; Borgmon pulls them with one HTTP fetch.
- **[[time-series-arena]]** — fixed-size in-memory database of `(timestamp, value)` tuples, indexed by labelset. Sized for ~12 hours of data in typical datacenter/global Borgmon (~17 GB RAM for a million 1-minute series); older data archived to an external TSDB.
- **[[borgmon-rules]]** — algebraic expressions that compute new time-series from existing ones. The rule language centralises what used to live in per-target check scripts; aggregation is the cornerstone operation.
- **[[alertmanager]]** — centrally-run routing service. Borgmon fires `Alert` RPCs when rules trigger for their minimum duration; Alertmanager deduplicates, inhibits, groups, and routes to pager / ticket / dashboard.
- **[[monitoring-topology-sharding]]** — hierarchy of Borgmon (scrapers → DC aggregators → global aggregators) for scaling beyond a single instance; upper tiers pull filtered aggregated series from lower tiers over a streaming protocol.

Borgmon is paired with **[[prober]]** for the black-box monitoring piece Chapter 6 insists on — see [[black-box-vs-white-box-monitoring]].

## Collection mechanics

A Borgmon instance is configured with a list of targets, resolved through one of several service discovery mechanisms (principally BNS — see [[bns]]). The target list is typically dynamic; service discovery reduces maintenance cost and scales as services grow (source: chapter-10-practical-alerting-from-time-series-data.md).

On the scrape interval:

- Borgmon fetches `/varz` on each target.
- Results are decoded and stored in the arena.
- Scrapes are **spread across the interval** to avoid lockstep load on targets.
- Borgmon also records **synthetic variables** per target: did name resolution succeed, did the target respond, did it pass a health check, what time collection finished. These feed alerting rules that detect unavailable tasks.

The chapter notes that scraping-over-HTTP is philosophically at odds with SNMP's "continue working when most other network applications fail" design. In practice this isn't an issue: the system is already designed for network and machine failures, and scrape failure *is itself* an alertable signal.

## Counters, gauges, and rate-of-sum

Most varz are **counters** (monotonically increasing). Counters are preferred over gauges because they don't lose meaning between sampling intervals. Borgmon's `rate()` function handles counter resets from task restarts.

A key Chapter 10 rule for distributed aggregation: compute the **sum of rates**, not the **rate of sums**. Sum-of-rates defends against counter resets and missing data; rate-of-sums does not. See [[borgmon-rules]].

## Relationship to the SRE monitoring taxonomy

[[sre-monitoring-outputs]] (from Chapter 1) gives the three-way split of valid monitoring outputs: alerts, tickets, logs. Borgmon produces the time-series metrics underneath those outputs; [[alertmanager]] routes fired alerts into the correct bucket based on label severity.

Chapter 10 also closes Chapter 6's loop: Borgmon is the concrete **white-box** system ([[black-box-vs-white-box-monitoring]]), and [[prober]] is the concrete **black-box** system, and together they realise the "heavy white-box plus modest-but-critical black-box" Google mix.

## Maintainability at scale

Chapter 10 closes with the economic argument ("Ten Years On…"): the key property of the Borgmon model is that the cost of maintenance **scales sublinearly** with the size of the service (source: chapter-10-practical-alerting-from-time-series-data.md). Three mechanisms make that possible:

- **Rules separate from targets** — one rule set covers many targets; rule cost does not grow with fleet size.
- **Templated per-library rule libraries** — any user of the HTTP server library, RPC library, storage client, etc. inherits a ready-made rule template for that library's varz.
- **Templated aggregation hierarchies** — one generic rule library models the task → job → shard → datacenter → service aggregation; engineers instantiate it per service.

The rule configuration itself is **unit- and regression-tested**, packaged by a continuous integration service, and shipped to all Borgmon in production — each receiving Borgmon validates the config before accepting it. This is [[release-engineering]] applied to monitoring.

## Cross-book connections

- [[monitoring-and-observability]] (Newman / Burns) — Borgmon is the monitoring half of the pair; observability tooling for unknown-unknown debugging is a separate concern.
- [[sre-monitoring-outputs]] — the alerts/tickets/logs taxonomy.
- [[capacity-planning]] — the long-term resource-consumption use.
- [[unified-monitoring-interface]] (Burns) — at the container level, Burns's adapter-pattern realisation of exposing consistent metrics across heterogeneous apps; Google solves the same problem with every server embedding an HTTP diagnostic endpoint.
- [[prometheus-connection]] — Prometheus inherits the pull model, the exposition format idea, the rule language, Alertmanager, and federation directly from Borgmon.

## Related pages

- [[varz-endpoints]]
- [[time-series-arena]]
- [[borgmon-rules]]
- [[alertmanager]]
- [[prober]]
- [[monitoring-topology-sharding]]
- [[prometheus-connection]]
- [[sre-monitoring-outputs]]
- [[monitoring-and-observability]]
- [[capacity-planning]]
- [[black-box-vs-white-box-monitoring]]
- [[borg]]
- [[bns]]
- [[site-reliability-engineering]]
