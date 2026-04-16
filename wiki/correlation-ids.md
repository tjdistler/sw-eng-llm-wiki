# Correlation IDs

**Summary**: A single identifier generated when a request enters the system and propagated through every downstream call it triggers. Lets you reconstruct the full path of a request across services from log aggregation, and is the prerequisite hook that distributed tracing plugs into later.

**Sources**: `raw/monolith-to-microservices/chapter-05-growing-pains.md`

**Last updated**: 2026-04-16

---

## How they work

When a call enters the system — typically at an API gateway or [[service-mesh]] — a correlation ID is generated. As that call fans out into downstream microservices, the correlation ID is passed along: in an HTTP header, a message field, or whatever transport mechanism the call uses. Each service logs in conjunction with that ID (source: chapter-05-growing-pains.md).

If your log aggregation puts the correlation ID in a standard place in the log format, you can then query across all services for "everything that happened on request X".

## Newman's worked example

(source: chapter-05-growing-pains.md)

The Invoice service receives a call and is given a correlation ID. When Invoice calls the Notification service, it passes the correlation ID along — say, via an HTTP header. Notification logs information about its work in conjunction with that ID. From the log aggregation system you can now retrieve the full chain of events for that originating request.

## Where they're generated

Newman recommends generating the correlation ID at an **edge component** — an API gateway or service mesh — so that every inbound request gets one and individual services don't have to remember to generate them. The same edge component can also handle the cross-service propagation.

## Other uses besides log search

- **Saga coordination** — correlation IDs are how a saga orchestrator follows the steps of a long-running multi-service operation. See [[saga]].
- **Distributed tracing** — once correlation IDs are propagated everywhere, plugging in [[distributed-tracing]] is mostly a matter of attaching span timing to the same identifier.

## Why introduce them early

Newman's strong advice (source: chapter-05-growing-pains.md): **add correlation-ID generation and propagation well before you need a distributed tracing tool.** They're cheap to add to a small architecture and become extremely expensive to backfill across a large one. When the day comes that you do need tracing, the hooks are already in place.

## Related pages

- [[monitoring-and-observability]]
- [[log-aggregation]]
- [[distributed-tracing]]
- [[service-mesh]]
- [[saga]]
