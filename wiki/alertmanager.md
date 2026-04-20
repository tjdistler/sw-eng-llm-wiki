# Alertmanager

**Summary**: A centrally-run service that receives `Alert` RPCs from the time-series monitoring system when rules fire, then routes, deduplicates, inhibits, and fans-in/out alerts toward the correct destination (pager, ticket queue, dashboard). The concept and name carried over into Prometheus's Alertmanager essentially unchanged.

**Sources**: `raw/site-reliability-engineering/chapter-10-practical-alerting-from-time-series-data.md`, `raw/site-reliability-engineering/chapter-16-tracking-outages.md`

**Last updated**: 2026-04-19

---

## Role

When an alerting rule evaluates to true for at least its minimum duration (the `for` clause), the monitoring system emits an **Alert RPC** to Alertmanager. The RPC fires twice: once when the rule first triggers (pending), and again when the alert is considered firing (source: chapter-10-practical-alerting-from-time-series-data.md).

Alertmanager is responsible for routing the alert notification to the correct destination. It is one centralised service shared by many monitoring instances, which is what enables the cross-source logic below.

## What Alertmanager adds

Chapter 10 lists three capabilities (source: chapter-10-practical-alerting-from-time-series-data.md):

- **Inhibit certain alerts when others are active** — a datacenter-down alert should suppress the hundreds of per-service alerts it would otherwise generate. Inhibition is the "higher-priority cause has already fired" mechanism.
- **Deduplicate alerts** — when multiple monitoring instances (e.g. two global replicas) evaluate the same rule on the same data, they fire the same alert. Deduplication by labelset collapses these to one notification.
- **Fan-in or fan-out by labelset** — alerts that share labels can be grouped (one page for "500 machines in us-west-1 are down", not 500 pages), or split apart when they have distinct ownership.

## Routing to the three monitoring outputs

Chapter 10 closes the loop with the Chapter 6 / Chapter 1 taxonomy (source: chapter-10-practical-alerting-from-time-series-data.md):

> Teams send their page-worthy alerts to their on-call rotation and their important but subcritical alerts to their ticket queues. All other alerts should be retained as informational data for status dashboards.

This is the [[sre-monitoring-outputs]] taxonomy realised in Alertmanager's routing config: page / ticket / log (dashboard). The alert's `labels` (e.g. `severity=page`) is what Alertmanager keys on to pick the destination.

## Why centralise

The alternative is per-instance notification logic. Centralisation wins on three counts:

- **Cross-instance deduplication** is only possible if one service sees all notifications. Global + datacenter replicas (see [[monitoring-topology-sharding]]) all fire overlapping alerts; without Alertmanager, every team would have to write deduplication rules inside each monitoring instance's rule file.
- **Inhibition across concerns** — a network team's "datacenter unreachable" alert can suppress downstream service alerts only if the systems see each other's alerts.
- **Uniform routing policy** — severity-to-destination mappings (page vs ticket vs dashboard) stay consistent across teams.

## Relationship to the time-series monitoring system

The monitoring system's job is detection: evaluate rules against the time-series arena and fire when thresholds are met. Alertmanager's job is action: take the fired alerts from all monitoring instances and get them to the right humans with the right urgency. The split keeps each piece simple (see [[monitoring-simplicity]]) and lets each scale independently.

## The paging-path neighbours: ack tracking and outage archival

Chapter 16 names two more pieces of the same real-time-plus-archival stack (source: chapter-16-tracking-outages.md):

- An **ack-tracking and auto-escalation** service. Alertmanager routes the page; the ack tracker tracks whether a human grabs it, and escalates to secondary / manager / further if nobody does.
- An **outage-level archive** for annotation, grouping, and analysis. It ingests the notification stream and is the long-term record.

Alertmanager's **real-time** concerns (inhibition, deduplication, grouping) have post-hoc counterparts in the archive: [[incident-aggregation|grouping multiple alerts into one incident]] after the fact, [[incident-tagging|tagging `bogus` on false positives]] so they're visible but excluded from actionable counts. The two axes — real-time noise control and archival data quality — are complementary; both are needed for the data to be useful weeks later.

Chapter 16 also notes a **dummy-ack-tracker** pattern: route notifications through the stack to the archive with no human pager destination, as a way to use the archive as a **system of record** for auditable events (privileged role-account access, non-idempotent periodic jobs). Alertmanager isn't the right tool for this use — its value is in real-time routing — but the overall architecture accommodates it because the pipeline is composable.

## Cross-book connections

- [[sre-monitoring-outputs]] — Alertmanager is the piece that physically routes alerts into the three valid outputs.
- [[alert-philosophy]] — Alertmanager's inhibition + deduplication + grouping are all noise-reduction mechanisms serving the "every page should require intelligence" rule.
- [[prometheus-connection]] — Prometheus's Alertmanager inherits the design (and the name).
- [[change-management-sre]] — fast, accurate detection is one of the three change-management practices; Alertmanager is the hop between detection and response.
- [[monitoring-simplicity]] — the centralised router is one example of Chapter 6's "keep monitoring/profiling/log-analysis as distinct loosely-coupled systems" rule applied inside monitoring.

## Related pages

- [[sre-monitoring-outputs]]
- [[alert-philosophy]]
- [[prober]]
- [[prometheus-connection]]
- [[outage-tracking]]
- [[site-reliability-engineering]]
