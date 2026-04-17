# Request as Event

**Summary**: An integration pattern that converts an incoming synchronous request into an event published to an event stream, then processes the event asynchronously like any other EDM input. Provides a durable audit-able record of every user action and lets downstream services materialize independent views, at the cost of eventually-consistent read-after-write and an [[asynchronous-ui|asynchronous UI]]. Bellemare's newspaper-publishing approval workflow is the canonical worked example.

**Sources**: `raw/building-event-driven-microservices/chapter-13-integrating-event-driven-and-request-response-microservices.md`

**Last updated**: 2026-04-17

---

## Two ways to handle a request

When a request-response API sits in front of an event-driven workflow, there are two handling choices (source: chapter-13-integrating-event-driven-and-request-response-microservices.md):

- **Traditional** — perform the requested operation immediately, write directly to the database, return a response.
- **Event-first** — parse the request into an event, publish it to its own stream, let the event-driven workflow consume it and materialize the result.

Services often mix these: turn requests that matter to the business (and may need to be shared outside the bounded context) into events, while handling purely local requests synchronously.

## Benefits of event-first

- **Durable record.** Every request is captured as an event in the log. Any service — present or future — can materialize its own view off the stream.
- **Canonical narrative.** Sequences of events (create, approve, reject, revise) form an audit trail. You can reconstruct the history at any point in time.
- **No external state store needed in many cases.** A pure stream-processing library (Kafka Streams, Samza) can materialize state directly from the event stream whenever the application starts up, removing the need for a separate KV store.
- **Single source of truth decoupled from implementation.** Backends can be swapped out, state-store technology changed, without migrating data — the event stream remains authoritative.

## Trade-offs

- **Latency** — the service must wait for the event to be materialized before reads reflect the write (eventually-consistent read-after-write).
- **In-memory shortcut** — Bellemare suggests keeping the value in memory after producing it, so it's available immediately for application-side operations. This does not work for operations that require the data to be present in the database (e.g., [[stream-joins|joins]]).
- **UI design** — clients need to be told the operation is asynchronous. See [[asynchronous-ui]].
- **Duplicates** — request retries on intermittent failure will produce duplicate events; consumers must handle duplicates [[idempotence|idempotently]].

## Worked example: newspaper publishing approval

Bellemare's Chapter 13 example walks through a multi-stage approval workflow as a sequence of event streams (source: chapter-13-integrating-event-driven-and-request-response-microservices.md):

1. **Newspaper populator** — designers arrange articles and ads in a GUI. When ready, a PDF is compiled and a `populated newspaper` event (key = `pn_key`, value = PDF URI + page metadata) is published. The GUI interactions themselves are *not* converted into events — the bounded context only cares about the final populated-newspaper event.
2. **Editor approval** — the editor loads the populated newspaper, marks it up, approves or rejects. An `editor approval` event is published with status, comments, and optional rejected-ad list.
3. **Advertiser approval** — the advertiser reviews their PDF slice and approves or rejects. Multiple `advertiser approval` events share the same `pn_key` — the aggregate of events per newspaper is what determines full advertiser approval.

### Not all interactions need to be events

A design question the example surfaces: the populator microservice does *not* translate every human GUI interaction into an event. Only the final output (the populated newspaper) is an event. "This particular bounded context is really only concerned with producing the final populated newspaper event, but it isn't particularly important how it came to be" (source: chapter-13-integrating-event-driven-and-request-response-microservices.md). This encapsulation lets you leverage a monolithic GUI framework internally, while still participating cleanly in the EDM architecture at the boundary.

### The monolith-sync warning

When a monolith internally tracks state *and* publishes an external event, the two can get out of sync on failure. Use [[outbox-table-pattern|outbox]] or [[change-data-capture|CDC]] to atomically publish from the internal state. See [[data-liberation]].

### Splitting by bounded context

Bellemare later splits the editor approval and advertiser approval services. The editor service gates which newspapers advance to advertiser review (not all versions are forwarded automatically); the advertiser service encapsulates which advertisers are contacted and produces an **ad-approval summary** event back to the editor. The editor does not need to know which advertisers exist — the summary is enough.

This demonstrates one of the pattern's payoffs: because the shared contract is a stream of events, the two services can evolve independently with clean business boundaries.

## Aggregate events vs entity events

The advertiser-approval example has multiple events per `pn_key` — each advertiser produces their own event. This is a stream of **[[unkeyed-event|events]]** (not [[entity-event|entities]]); the aggregate across the stream for a given key represents the logical state. This is a legitimate modeling choice when the domain is fundamentally a sequence of independent decisions rather than a single mutable entity.

## Related pages

- [[event-driven-request-response-integration]]
- [[asynchronous-ui]]
- [[idempotence]]
- [[effectively-once-processing]]
- [[outbox-table-pattern]]
- [[data-liberation]]
- [[bounded-context]]
- [[entity-event]]
- [[materialized-state]]
- [[event-sourcing]]
