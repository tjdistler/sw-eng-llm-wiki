# Asynchronous UI

**Summary**: UI design techniques for applications whose backend is event-driven — where a user's action becomes an event that is processed asynchronously rather than completed synchronously before the response returns. The UI must cue the user that processing is in flight, discourage premature retries, and decide when to push updates back to the client.

**Sources**: `raw/building-event-driven-microservices/chapter-13-integrating-event-driven-and-request-response-microservices.md`

**Last updated**: 2026-04-17

---

## Why it matters

In a synchronous system, a user clicking a button expects a success or failure response within roughly 100 ms. In an event-driven system where the [[request-as-event|request has been turned into an event]], processing may take longer — especially when a large backlog must be processed before the user's request reaches the head of the queue (source: chapter-13-integrating-event-driven-and-request-response-microservices.md).

Bellemare's recommendation: "Research and implement best practices for asynchronous UIs when handling user input as events. Proper UI design prepares the user to expect asynchronous results."

## Techniques

### Tell the user the request is in flight

Update the UI to indicate the request has been sent and is being processed. Discourage further action until it completes (source: chapter-13-integrating-event-driven-and-request-response-microservices.md). Common patterns:

- **"Please wait" spinner** that blanks the rest of the page. Airline booking and car-rental sites use this.
- **Disabling the submit button** to prevent double-submission.
- **Optimistic UI** — show the result as if it succeeded, and reconcile if it doesn't.

### Decide when to push the update back

The service is continually processing events, including non-user events arriving in parallel. You must decide:

- **When processing has progressed enough to send a UI update.**
- **When the initial catch-up from the beginning of time is "done enough"** to start showing current state — since many EDMs replay large histories on startup.

There are no hard-and-fast rules. Bellemare's guide-questions (source: chapter-13-integrating-event-driven-and-request-response-microservices.md):

- *What is the impact of the user making a decision based on stale state?*
- *What is the performance / experience impact of pushing a UI update?*

Business rules of the bounded context set the answer.

### Handle duplicates idempotently

Intermittent network failures cause retries, which introduce duplicate events. The consumer side of the async workflow must handle duplicates without double-applying the operation. See [[idempotence]] and [[effectively-once-processing]].

## Relationship to the backend patterns

This page pairs with the backend pattern [[request-as-event]] — they are two halves of the same decision. You cannot adopt request-as-event without investing in asynchronous UI techniques, or the user experience collapses.

The UI shape is also what makes [[micro-frontends]] work: because each micro-frontend handles its own async backend independently, the stitching layer has to gracefully handle components loading at different rates.

## Related pages

- [[request-as-event]]
- [[event-driven-request-response-integration]]
- [[micro-frontends]]
- [[idempotence]]
- [[effectively-once-processing]]
- [[materialized-state]]
