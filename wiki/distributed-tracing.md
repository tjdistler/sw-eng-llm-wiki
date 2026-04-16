# Distributed Tracing

**Summary**: Tools that capture per-segment timing for a chain of calls across services, so you can answer "where did the time go?" Log aggregation can show you what happened; distributed tracing shows you when and how long each part took.

**Sources**: `raw/monolith-to-microservices/chapter-05-growing-pains.md`

**Last updated**: 2026-04-16

---

## What it solves

[[log-aggregation]] gives you the ability to find all logs related to a single request via [[correlation-ids]]. That's enough to reconstruct *what* happened. It's not enough to determine *where the time was spent*. Logs are batched and forwarded on intervals — the timestamp granularity and per-process clock variation make accurate latency attribution impossible from logs alone (source: chapter-05-growing-pains.md).

Distributed tracing systems capture span-level timing data with the explicit intent of latency analysis. Each segment of the call chain — each service's processing of the request — produces a span tagged with the correlation ID, allowing the full chain to be reconstructed and visualised.

## Tooling

Newman names **Jaeger** as an open-source example (source: chapter-05-growing-pains.md). Other tools in the same space include Zipkin, AWS X-Ray, Honeycomb, and Lightstep.

## When to invest

> "The more latency sensitive your application is, the sooner I'd be looking to implement a distributed tracing tool like Jaeger." (source: chapter-05-growing-pains.md)

Specifically: distributed tracing answers questions about tail latency that other tools can't. If you're investigating p99 latency through complex call chains, you need traces. If your application doesn't care about latency, you can defer.

## The cheap-to-add prerequisite

If you've already added [[correlation-ids]] to your architecture (Newman's standing advice — do it early, regardless of tracing plans), then plugging in a tracing tool is mostly a matter of attaching span data at the same propagation points (source: chapter-05-growing-pains.md). The expensive part of distributed tracing is the propagation infrastructure, and you should have built that for log aggregation already.

A [[service-mesh]] handles inbound and outbound tracing for you automatically — covering service-to-service calls without app code changes. It can't trace what happens *inside* an individual microservice; that still requires per-app instrumentation.

## What good tracing UIs show

A typical Jaeger-style view: a horizontal time axis with each span as a coloured bar, nested to show parent-child call relationships. You can see at a glance which span is the long pole, where the gaps are (often serial calls that could parallelise), and which downstream service caused a regression after a release.

## Related pages

- [[monitoring-and-observability]]
- [[log-aggregation]]
- [[correlation-ids]]
- [[service-mesh]]
- [[response-time-percentiles]]
