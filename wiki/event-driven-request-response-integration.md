# Event-Driven / Request-Response Integration

**Summary**: Hub page for Bellemare's Chapter 13 — the patterns that stitch [[event-driven-microservices]] together with [[synchronous-microservices|request-response]] APIs at both the producing edge (external events arriving over HTTP) and the consuming edge (serving materialized state back to users and systems). EDM cannot do everything; integration with request-response is a first-class design concern, not a grudging concession.

**Sources**: `raw/building-event-driven-microservices/chapter-13-integrating-event-driven-and-request-response-microservices.md`

**Last updated**: 2026-04-17

---

## Why integration matters

Event-driven patterns are powerful but cannot serve all business needs (source: chapter-13-integrating-event-driven-and-request-response-microservices.md). Bellemare lists five request-response-native situations: collecting metrics from external sources (mobile apps, IoT), integrating with third-party APIs, serving content in real time to users, serving dynamic requests based on real-time inputs (location, weather), and handling synchronous user interactions where latency expectations rule out waiting for event materialization.

In these cases event-driven patterns still play a large role — the integration patterns decide where the boundary sits.

For the purposes of Chapter 13, *request-response* means services that communicate directly through a synchronous API. Two services over HTTP is the canonical example.

## The integration patterns

Chapter 13 organizes the patterns into four groups:

- **Ingesting external events** — converting requests from devices or third parties into events on internal streams. See [[external-events-ingestion]] (autonomous analytical events) and [[third-party-api-integration]] (reactive events from calling out).
- **Serving state** — exposing an EDM's materialized view over a request-response API. See [[serving-state-from-edm]], [[smart-load-balancer]], and the existing [[internal-state-store]] / [[external-state-store]] pages.
- **Handling requests inside an event-driven workflow** — turning a user request into an event before processing it. See [[request-as-event]] and the [[asynchronous-ui]] patterns that make this viable.
- **Micro-frontends** — extending the microservice / bounded-context discipline through the UI layer. See [[micro-frontends]]; contrast with the UI-migration framing in [[ui-composition]].

## Two types of externally generated events

Bellemare separates external events into two kinds (source: chapter-13-integrating-event-driven-and-request-response-microservices.md):

- **Autonomous** — sent client-to-server by your products, unprompted. Measurements, sensor readings, mobile analytics. Netflix-style "what movie did you watch and how much of it" is the archetype. Covered in [[external-events-ingestion]].
- **Reactive** — generated in response to a request your service issued. Covered in [[third-party-api-integration]]. Whether to capture the response as an event is a business question: a fire-and-forget email send is usually uninteresting; a payment-processor reply with transaction IDs is critical for downstream accounting reconciliation.

Not every request needs to become an event. The test is "are these events important enough to the business that they must go into their own stream for additional processing?" — and often the answer is no.

## Two sides of "serving state"

An EDM can expose a request-response endpoint over its materialized view (source: chapter-13-integrating-event-driven-and-request-response-microservices.md). Two architectural choices:

- **[[internal-state-store|Internal state]]** served directly — the microservice instance holds a partition's data and serves requests for keys that hash to it. Requires a [[smart-load-balancer]] or an instance-to-instance redirect, because each key lives on exactly one instance.
- **[[external-state-store|External state]]** served by any instance — every instance can serve any key because all state sits behind a shared networked store. Two sub-patterns: the *all-in-one* microservice (processor + request-response API in one binary) and the *separate microservice* pattern (processor and API as separate deployables sharing a bounded context). See [[serving-state-from-edm]].

## Requests as events

The third integration direction: instead of handling a request synchronously, parse it into an event and publish it to a stream. The event becomes the canonical record and downstream services materialize off it (source: chapter-13-integrating-event-driven-and-request-response-microservices.md).

Trade-offs:

- **Durability**: every user action is a first-class event in the log.
- **Latency**: the client must wait for the event to be materialized before reads reflect the write (eventually-consistent read-after-write).
- **UI design**: needs to cue the user that processing is asynchronous — see [[asynchronous-ui]].

Bellemare's newspaper-publishing worked example (populator → editor approval → advertiser approvals → summary) shows the pattern at scale, demonstrating three benefits: a full audit-able narrative of approvals and rejections; natural splitting of a combined service into independently-scoped microservices by business bounded context; and direct materialization of state from the event streams without needing an external KV store. See [[request-as-event]].

## Micro-frontends

Chapter 13 closes with **[[micro-frontends]]** — the product-aligned frontend counterpart to microservices. Each micro-frontend owns its own UI slice and its own backing microservice(s), eliminating the monolithic-aggregation-layer problem where business logic creeps into the stitching layer. Micro-frontends pair especially well with event-driven backends because both are compositional by nature.

Distinct from [[ui-composition]] as a migration pattern: micro-frontends are a steady-state architecture choice, not just a technique for strangling a monolith.

## Related pages

- [[event-driven-microservices]]
- [[synchronous-microservices]]
- [[external-events-ingestion]]
- [[third-party-api-integration]]
- [[serving-state-from-edm]]
- [[smart-load-balancer]]
- [[request-as-event]]
- [[asynchronous-ui]]
- [[micro-frontends]]
- [[internal-state-store]]
- [[external-state-store]]
- [[materialized-state]]
- [[ui-composition]]
