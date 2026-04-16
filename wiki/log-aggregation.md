# Log Aggregation

**Summary**: Forwarding log output from many short-lived processes to a central queryable store. Newman's "first thing to do" when adopting microservices — both because it's immediately useful and because organisations that can't manage it probably aren't ready for microservices.

**Sources**: `raw/monolith-to-microservices/chapter-05-growing-pains.md`

**Last updated**: 2026-04-16

---

## Why it matters in microservices

With a few long-lived machines, debugging meant SSH-ing in and tailing the file. Microservice processes are numerous, often containerised, and frequently short-lived. By the time you go looking for the log, the container may not exist (source: chapter-05-growing-pains.md).

Log aggregation captures every process's logs and forwards them to a central system that supports search and (sometimes) alerting. It's the floor of [[monitoring-and-observability]] — without it, the rest of the toolbox is barely usable.

## Newman's "do this first" framing

Newman explicitly recommends implementing log aggregation **before** implementing a microservice architecture (source: chapter-05-growing-pains.md). Two reasons:

1. **It pays off immediately.** Even with a small number of services, cross-process search is an order-of-magnitude productivity gain.
2. **It's an organisational test.** The work to ship a log-aggregation pipeline is straightforward. If your organisation can't manage that, microservices are probably out of reach — they require much more operational sophistication.

> "If your organization struggles to implement a suitable log aggregation system, you might want to reconsider whether you're ready for microservices." (source: chapter-05-growing-pains.md)

## Tools Newman names

(source: chapter-05-growing-pains.md)

- **ELK stack** — Elasticsearch + Logstash (or Fluentd) + Kibana. Open source, widely deployed.
- **Humio** — Newman's personal favourite.

The market has many alternatives (Splunk, Datadog Logs, Loki, OpenSearch, etc.); Newman doesn't survey them.

## What good log aggregation enables

- Cross-service search for a single request via [[correlation-ids]].
- Alert generation from log patterns.
- Forensic timelines after incidents — what each service was doing minute-by-minute around an outage.
- Trend analysis across releases — "did this error rate go up after yesterday's deploy?"

## Where log aggregation isn't enough

Logs are batched and shipped on intervals. That makes them a coarse instrument for **timing** questions — "where did the latency go in this call chain?" For that, you need [[distributed-tracing]], which captures span-level timing data with synchronised intent.

## Related pages

- [[monitoring-and-observability]]
- [[correlation-ids]]
- [[distributed-tracing]]
- [[microservices]]
