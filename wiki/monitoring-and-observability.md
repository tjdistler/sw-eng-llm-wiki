# Monitoring and Observability

**Summary**: Monolithic-era monitoring assumed a small number of long-lived processes with binary up/down failure modes. Microservices break that assumption: failures are partial, processes are short-lived, and "is everything OK?" stops being a simple question. Newman frames the shift as moving from monitoring (known causes) to observability (open-ended questions).

**Sources**: `raw/monolith-to-microservices/chapter-05-growing-pains.md`

**Last updated**: 2026-04-16

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

## Related pages

- [[log-aggregation]]
- [[correlation-ids]]
- [[distributed-tracing]]
- [[synthetic-transactions]]
- [[response-time-percentiles]]
- [[fault-tolerance]]
- [[service-mesh]]
- [[end-to-end-testing]]
