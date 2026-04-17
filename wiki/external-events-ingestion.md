# External Events Ingestion

**Summary**: How to turn externally-generated requests — typically analytical events from mobile apps, web clients, or IoT devices — into events on internal streams. An **event-receiver service** exposes a request-response API, validates incoming payloads against a schema, and routes each event onto the appropriate stream.

**Sources**: `raw/building-event-driven-microservices/chapter-13-integrating-event-driven-and-request-response-microservices.md`

**Last updated**: 2026-04-17

---

## The problem

External clients almost always speak request-response (source: chapter-13-integrating-event-driven-and-request-response-microservices.md). Exposing an event broker directly to outside clients is possible but largely unreasonable due to access, security, and protocol mismatches. HTTP is what the outside world uses — receive events over HTTP, then route onto streams internally.

Bellemare distinguishes two kinds of externally-generated events:

- **Autonomous** — sent client-to-server by your products without any prior request. Analytical events: what a user watched, sensor readings, session telemetry. This page focuses on these.
- **Reactive** — generated in response to a request *your* service made. See [[third-party-api-integration]].

## The event-receiver service

The pattern is a simple request-response microservice acting as an edge translator:

1. Client sends one or many analytical events to the receiver's HTTP endpoint.
2. The receiver validates each event against its schema.
3. The receiver routes each event onto the appropriate output event stream based on its type.

Bellemare's guidance: think of external event sources as a set of microservice instances, each producing schematized events via the event-receiver. Sort incoming events into their own defined streams by schema and purpose, just as you would for any other microservice's outputs (source: chapter-13-integrating-event-driven-and-request-response-microservices.md).

## Schemas at the client

**Schematize events at generation time, on the client** (source: chapter-13-integrating-event-driven-and-request-response-microservices.md). This puts the onus of populating, validating, and testing events on the producer — where the domain knowledge lives — and eliminates the need for the receiver to re-interpret plain-text or ad-hoc payloads.

Benefits:

- High-fidelity source data that reduces misinterpretation by downstream consumers.
- Detailed contract for producers: the schema tells app developers exactly what to populate.
- Version control and evolution baked in from the start.
- The receiver does not need parsing heuristics, just schema validation.

See [[data-contract]], [[explicit-vs-implicit-schemas]], and [[schema-evolution]].

## Multiple versions in flight

Mobile apps and any field-deployed client will produce multiple event versions simultaneously — you cannot realistically force every user to upgrade for every schema change (source: chapter-13-integrating-event-driven-and-request-response-microservices.md). The receiver must handle multiple concurrent versions of the same logical event without losing data or failing requests from older clients.

This is [[backward-forward-compatibility|full compatibility]] territory: new code must read old events, and old code must tolerate new events. Plan for version sprawl from day one rather than bolting it on later.

## Separate streams per event type

Bellemare is explicit: **do not dump heterogeneous events into a single stream**. Separate incoming events into their own defined streams based on their schemas and event definitions, by business purpose, just as you would for any internal EDM's outputs (source: chapter-13-integrating-event-driven-and-request-response-microservices.md). See [[singular-event-definition-per-stream]].

## Batching

Analytical events may be bundled and periodically sent in a batch, or streamed as they occur. Both work; the receiver unpacks the batch and fans out to the correct streams either way (source: chapter-13-integrating-event-driven-and-request-response-microservices.md).

## Duplicate handling

Intermittent network failures cause retries, which introduce duplicates. The Chapter-13 warning: ensure consumers of the downstream streams can handle duplicates idempotently. See [[idempotence]] and [[effectively-once-processing]].

## Related pages

- [[event-driven-request-response-integration]]
- [[third-party-api-integration]]
- [[data-contract]]
- [[explicit-vs-implicit-schemas]]
- [[schema-evolution]]
- [[singular-event-definition-per-stream]]
- [[backward-forward-compatibility]]
- [[idempotence]]
- [[basic-producer-consumer-microservice]]
