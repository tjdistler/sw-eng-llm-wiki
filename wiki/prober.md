# Prober

**Summary**: Google's black-box monitoring tool. Runs a protocol check against a target and reports success or failure; can send alerts directly to [[alertmanager]] or expose its own metrics endpoint for the pull-based time-series monitoring system to scrape. Fills the coverage gap that white-box monitoring leaves: failures invisible to the server itself (DNS errors, load-balancer misroutes, crashed instances).

**Sources**: `raw/site-reliability-engineering/chapter-10-practical-alerting-from-time-series-data.md`, `raw/site-reliability-engineering/chapter-17-testing-for-reliability.md`

**Last updated**: 2026-04-17

---

## Why white-box isn't enough

The internal time-series monitoring system is pure white-box: it scrapes the target's internal state. That gives enormous power to identify *what* is failing, *which* queues are full, and *where* bottlenecks are — but it has a structural blind spot (source: chapter-10-practical-alerting-from-time-series-data.md):

> You only see the queries that arrive at the target; the queries that never make it due to a DNS error are invisible, while queries lost due to a server crash never make a sound. You can only alert on the failures that you expected.

Prober closes that gap. By probing from outside the service, it catches failures that the service itself cannot report, because the service isn't there to report them.

## What Prober does

Prober runs a protocol check against a target and reports success or failure (source: chapter-10-practical-alerting-from-time-series-data.md). It is a hybrid of the classic check-and-test model with richer variable extraction:

- **Protocol checks** — send an HTTP request, make a DNS query, open a TCP connection.
- **Response validation** — inspect the payload (e.g. the HTML of an HTTP response) and confirm it matches expectations.
- **Variable extraction** — pull values out of responses and export them as time-series. Teams often use Prober to export histograms of response times broken down by operation and payload size.
- **Two output paths** — send alerts directly to Alertmanager, or expose its own metrics endpoint for the monitoring system to scrape. The second path is usually preferred because it feeds the full aggregation-rule language.

## Before-the-LB and behind-the-LB

A Prober can be pointed at either the frontend domain or behind the load balancer. Both together give a locality signal (source: chapter-10-practical-alerting-from-time-series-data.md):

- Monitoring `www.google.com` (the load-balanced frontend) and each datacenter's webservers behind the LB independently.
- If frontend probes succeed but a datacenter probe fails, traffic is still being served — no user-visible harm.
- If frontend probes fail, the problem is global or at the edge.

This lets the probing configuration "suppress alerts" that are known to be absorbed by load-balanced redundancy, and "quickly isolate an edge" where failure is happening.

## How it fits the monitoring mix

Chapter 10 uses Prober as the concrete worked example for Chapter 6's [[black-box-vs-white-box-monitoring]] guidance. The combined Borgmon + Prober deployment is the full Google recipe:

- **Heavy white-box** — every Google binary exposes `/varz`; Borgmon scrapes all of them; most debugging and most alerting use this.
- **Modest but critical black-box** — Prober probes the user-critical paths externally; the backstop that ensures you only page when something is actually user-visible.

Prober's detection latency is often slower than Borgmon's (probes run at longer intervals than scrapes), but Prober alerts are higher-signal: if a probe fails, a user would see the same failure.

## Probes as release-test continuation (Chapter 17)

Chapter 17 reframes production probes as the natural continuation of the release-test pipeline (source: chapter-17-testing-for-reliability.md). The same bank of known-good and known-bad requests that integration tests use can be replayed against production as probes. Because the frontend and backend typically have **independent release cycles**, probes exercise version combinations that the release tests never did — which is why they catch things release tests cannot.

Chapter 17's sharpening of Chapter 10's probe story: probes are **also a rollout gate**. If a probe fails on a newly-started instance, the updater can pause the rollout indefinitely until engineers diagnose the mismatch. See [[production-probes]].

## Cross-book connections

- [[synthetic-transactions]] (Newman) — synthetic transactions and Prober are the same idea. Newman's framing emphasises scripted end-to-end journeys; Chapter 10's Prober emphasises single-protocol probes and payload validation. Both are end-to-end black-box checks against the live system.
- [[health-check-adapter]] (Burns) — the container-orchestrator's per-pod version of what Prober does centrally; rich application-specific black-box checks.
- [[health-probes]] (Burns) — Kubernetes liveness/readiness; coarser than Prober but with the same intent.
- [[alert-philosophy]] — Chapter 6's point that once an alert is urgent/actionable/user-visible/novel, it doesn't matter whether white-box or black-box fired it. Prober is the mechanism that makes black-box alerts practical.

## Related pages

- [[black-box-vs-white-box-monitoring]]
- [[alertmanager]]
- [[synthetic-transactions]]
- [[four-golden-signals]]
- [[site-reliability-engineering]]
- [[production-probes]]
- [[testing-for-reliability]]
