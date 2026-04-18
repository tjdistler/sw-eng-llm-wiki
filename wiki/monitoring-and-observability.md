# Monitoring and Observability

**Summary**: Monolithic-era monitoring assumed a small number of long-lived processes with binary up/down failure modes. Microservices break that assumption: failures are partial, processes are short-lived, and "is everything OK?" stops being a simple question. Newman frames the shift as moving from monitoring (known causes) to observability (open-ended questions).

**Sources**: `raw/monolith-to-microservices/chapter-05-growing-pains.md`, `raw/designing-distributed-systems/chapter-04-adapters.md`, `raw/site-reliability-engineering/chapter-01-introduction.md`, `raw/site-reliability-engineering/chapter-06-monitoring-distributed-systems.md`, `raw/site-reliability-engineering/chapter-10-practical-alerting-from-time-series-data.md`

**Last updated**: 2026-04-17

---

## The shift

> "We replaced our monolith with microservices so that every outage could be more like a murder mystery." — Honest Status Page (source: chapter-05-growing-pains.md)

A monolith is mostly all-up or all-down. CPU stuck at 100% is unambiguously a problem. A microservice architecture has tens or hundreds of processes; failure is now per-instance, per-service-type, or per-call-chain. Should you wake someone up at 3 a.m. for one process at 100% CPU? It depends — and answering depends on context the monolith-era monitoring stack doesn't capture (source: chapter-05-growing-pains.md).

## When this hits

Newman finds this hard to predict. Could be at two services or twenty. Symptoms (source: chapter-05-growing-pains.md):

- Production issues you can't explain or understand.
- Alerts firing while the system seems healthy.
- "Is everything OK?" becomes hard to answer.

His pragmatic recommendation: implement basic improvements *ahead* of when you'd otherwise need them.

## Monitoring vs observability

The Chapter 5 distinction (source: chapter-05-growing-pains.md):

- **Traditional monitoring and alerting** = *known* failure modes. You think about what might go wrong, instrument for it, alert on it. Disk full, instance unresponsive, latency spike.
- **Observability** = *unknown* failure modes. The system is complex enough that you cannot enumerate all the ways it might fail. You need to be able to ask open-ended questions of your system after the fact, using data you didn't know you'd need.

The observability shift requires:

1. Gathering rich data — logs, traces, metrics — without prejudging which questions you'll ask.
2. Tooling that supports **ad hoc querying** of that data.
3. A team disposition: "we *will* be surprised; let's get good at asking questions" rather than "we know what's broken — let's check our dashboard".

Newman's recommended depth read: Cindy Sridharan's *Distributed Systems Observability* (O'Reilly, 2018).

## The toolbox

Newman lists a non-exhaustive toolkit, in roughly increasing complexity (source: chapter-05-growing-pains.md):

### [[log-aggregation]]

The first thing to do — even before adopting microservices. Forward all logs to a central queryable place. Newman: if your organisation can't get this in place, microservices are likely a step too far. Tools: ELK (Elasticsearch / Logstash or Fluentd / Kibana), Humio (his personal favourite).

### [[correlation-ids]]

A single identifier propagated through the chain of calls triggered by an inbound request. Lets log aggregation answer "what happened on this user's request, across all the services it touched?" Typically generated at the API gateway or service mesh and passed via HTTP header or message field.

### [[distributed-tracing]]

Goes further than correlation IDs in log aggregation: captures timing for each segment of a call chain. Required when log batching latency makes "where did the time go?" impossible to answer from logs. Tools: Jaeger (open source). The more latency-sensitive the application, the sooner to invest.

### Metrics

Numeric time-series — CPU, request rate, error rate, p50/p95/p99 latency. The traditional monitoring substrate. Combine with distributed tracing for outliers and with logs for context.

### [[synthetic-transactions]] (test in production)

Inject fake user behaviour — synthetic transactions — that exercise end-to-end behaviour against the live system. Faster signal than waiting for a real user to hit the bug. Newman's Atomist example is in [[synthetic-transactions]].

## A sequencing rule of thumb

Roughly:

1. **Log aggregation first.** Easiest, most useful, also a litmus test of organisational readiness.
2. **Correlation IDs early** — well before you need distributed tracing. Adding correlation-ID generation to existing services is a small change and creates the hooks distributed tracing later plugs into.
3. **Distributed tracing when latency matters.** If you're chasing tail-latency problems through call chains, this is what you need. A [[service-mesh]] gives you inbound/outbound tracing for free; intra-service instrumentation still requires app-level work.
4. **Synthetic transactions as a continuous safety net** for behaviours your end-to-end test suite used to cover.

## Why this is a Chapter 5 pain

The transition from "monitoring works" to "monitoring doesn't work" is mostly silent. There's no error at the moment the dashboard becomes uninformative. You discover it the next time a real production incident happens and the team can't tell what's going on. Newman's prescription is to invest *ahead* of that moment.

## The container-level mechanism: adapters

Newman's chapter makes the operational case; Brendan Burns's [[adapter-pattern]] is the container-level mechanism for satisfying it in a heterogeneous fleet. A single monitoring tool can only aggregate metrics if every application exposes the same interface — but real fleets include first-party code, vendor binaries, and off-the-shelf open source with many incompatible native interfaces (source: raw/designing-distributed-systems/chapter-04-adapters.md). Rather than fork each image to embed standard metrics, run an adapter container alongside that translates whatever the application emits into the fleet-standard shape. The Chapter 4 worked examples cover the three pieces of the toolbox above:

- **Metrics** — [[unified-monitoring-interface]]: a Prometheus exporter running alongside Redis presents the fleet-standard pull endpoint without modifying the Redis image.
- **Logs** — [[log-normalization]]: a fluentd adapter normalises and restructures heterogeneous log streams before they reach the aggregator.
- **Deep health** — [[health-check-adapter]]: a custom adapter runs workload-representative queries and exposes an HTTP probe the orchestrator can consume.

A [[service-mesh]] supplies the cross-cutting HTTP/gRPC telemetry for free; adapter containers fill in the application-specific gaps.

## The SRE taxonomy: alerts, tickets, logs

Google SRE's Chapter 1 adds a sharper taxonomy for the *output* side of a monitoring system (source: raw/site-reliability-engineering/chapter-01-introduction.md). There are only three valid monitoring outputs:

- **Alerts** — a human must act *now*.
- **Tickets** — a human must act, but not immediately.
- **Logs** — nobody needs to read this unless something else prompts them to.

The named anti-pattern is the email alert that requires a human to interpret whether action is needed. *Software should do the interpreting, and humans should be notified only when they need to take action.* The full page is [[sre-monitoring-outputs]]; it slots neatly inside Newman's *monitoring* half of the monitoring-vs-observability split.

## The SRE monitoring chapter: what to measure and what to page on

Chapter 6 of the SRE book (Rob Ewaschuk) is the full treatment of monitoring philosophy (source: raw/site-reliability-engineering/chapter-06-monitoring-distributed-systems.md). Where Chapter 1 established *what outputs monitoring should have*, Chapter 6 fills in *what to measure* and *when to page*. The resulting pages all slot inside Newman's monitoring half:

- [[four-golden-signals]] — latency, traffic, errors, saturation: if you can only measure four things, measure these
- [[symptoms-vs-causes]] — the single most important distinction for signal-vs-noise; page on symptoms, debug with causes
- [[black-box-vs-white-box-monitoring]] — heavy white-box + modest critical black-box; Google's mix
- [[alert-philosophy]] — urgent, actionable, user-visible, novel; the four principles for page criteria
- [[long-tail-latency]] — why histograms beat means, especially under fan-out
- [[monitoring-resolution]] — matching measurement granularity to the question; server-local sampling
- [[monitoring-simplicity]] — the complexity trap and the three pruning rules; keep the paging path robust

These concepts supply the *"what makes a good monitoring signal"* answer that Newman's chapter leaves implicit. The two views are complementary: Newman focuses on the monitoring-vs-observability split and the toolbox sequencing; SRE Chapter 6 focuses on paging discipline and measurement hygiene.

## The SRE monitoring-system architecture (Chapter 10)

Chapter 10 of the SRE book (Jamie Wilkinson) is the architecture deep-dive behind the philosophy of Chapter 6 (source: raw/site-reliability-engineering/chapter-10-practical-alerting-from-time-series-data.md). It describes [[borgmon]] — Google's internal monitoring system and the explicit ancestor of Prometheus — in enough detail that the design choices carry over to any modern time-series monitoring stack:

- [[varz-endpoints]] — the `/varz` HTTP metrics exposition format; every Google binary auto-registers metrics. The pull-with-text-format convention Prometheus inherited.
- [[time-series-arena]] — in-memory store for ~12 hours of labelled `(timestamp, value)` tuples; older data archived to an external TSDB.
- [[borgmon-rules]] — the centralised rule language for computing new time-series from existing ones; aggregation-via-sum-of-rates as the cornerstone; the direct ancestor of PromQL.
- [[alertmanager]] — centrally-run service that deduplicates, inhibits, groups, and routes fired alerts to pager / ticket / dashboard; the Prometheus Alertmanager inherits the design and the name.
- [[prober]] — the concrete black-box monitoring tool that complements Borgmon's white-box approach; Newman's [[synthetic-transactions]] in Google vocabulary.
- [[monitoring-topology-sharding]] — the scraper / DC aggregator / global aggregator hierarchy that scales Borgmon past a single instance's capacity; Prometheus federation implements the same pattern.
- [[prometheus-connection]] — the explicit genealogy, naming what transferred intact from Borgmon to the open-source ecosystem.

Chapter 10's central claim — that treating time-series as the first-class data source and centralising rule evaluation makes monitoring **scale sublinearly with service size** — is the operational argument behind the Newman/Burns observability-toolbox recommendations.

## Related pages

- [[sre-monitoring-outputs]]
- [[four-golden-signals]]
- [[symptoms-vs-causes]]
- [[black-box-vs-white-box-monitoring]]
- [[alert-philosophy]]
- [[long-tail-latency]]
- [[monitoring-resolution]]
- [[monitoring-simplicity]]
- [[log-aggregation]]
- [[correlation-ids]]
- [[distributed-tracing]]
- [[synthetic-transactions]]
- [[response-time-percentiles]]
- [[fault-tolerance]]
- [[service-mesh]]
- [[end-to-end-testing]]
- [[adapter-pattern]]
- [[unified-monitoring-interface]]
- [[health-check-adapter]]
- [[borgmon]]
- [[varz-endpoints]]
- [[time-series-arena]]
- [[borgmon-rules]]
- [[alertmanager]]
- [[prober]]
- [[monitoring-topology-sharding]]
- [[prometheus-connection]]
