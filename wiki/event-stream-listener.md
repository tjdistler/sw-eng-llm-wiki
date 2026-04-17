# Event-Stream Listener

**Summary**: Bellemare's name for the canonical FaaS trigger that fires a function when new events arrive in a subscribed event stream. The listener isolates event consumption behind a predefined consumer so the developer writes only the processing code; batch size and batch window determine how events are grouped into a single function invocation.

**Sources**: `raw/building-event-driven-microservices/chapter-09-microservices-using-function-as-a-service.md`

**Last updated**: 2026-04-17

---

## Shape of the pattern

A function is registered against one or more input event streams. When a new event arrives, the FaaS framework starts the function (cold or warm), passes in a batch of events as an `Event[]` parameter, and the function processes them to completion (source: chapter-09-microservices-using-function-as-a-service.md). Each event carries a key, value, timestamp, offset, and partition id; a `Context` parameter carries metadata such as function name, stream id, and remaining lifespan.

Two sub-shapes exist depending on where the listener code lives (source: chapter-09-microservices-using-function-as-a-service.md):

- **Integrated listener** — the FaaS framework itself consumes from the event stream and invokes the function (AWS Lambda, Google Cloud Functions, Azure Functions with their proprietary brokers).
- **External listener** — a connector outside the FaaS framework (e.g., Kafka Connect) consumes events and invokes the function via the FaaS framework's API. This is how open-source brokers are bridged into proprietary FaaS and vice versa.

## Batch size and batch window

Two tunables control how events are grouped before invocation (source: chapter-09-microservices-using-function-as-a-service.md):

- **Batch size** — maximum number of events passed to a single invocation.
- **Batch window** — maximum time to wait for additional events before firing with whatever has arrived.

Both parameters spread the function's startup cost across many events and are therefore levers on both latency and cost. Small batches and short windows minimize latency but pay per-invocation overhead on every few events; large batches and long windows amortize startup but delay processing and increase the risk of timing out within the function's maximum execution time. See [[faas-batch-processing]] for the failure-handling consequences of getting this wrong.

## Synchronous vs asynchronous dispatch

The listener can dispatch events either synchronously or asynchronously (source: chapter-09-microservices-using-function-as-a-service.md):

- **Synchronous** — the listener waits for the current function invocation to complete before issuing the next batch. Processing order is preserved and parallelism is bounded by the event stream's partition count.
- **Asynchronous** — the listener fires multiple invocations concurrently without waiting. Throughput goes up but ordering is lost. Use only when the business logic does not depend on event order.

This is the EDM-level analog of the ordering-vs-parallelism trade-off that runs through all of [[consumer-group]] processing.

## Starting offset

Like any containerized EDM consumer, the listener can be configured to start consuming from the stream's earliest offsets, latest offsets, or any specific offset in between (source: chapter-09-microservices-using-function-as-a-service.md). This is the standard [[reprocessing-event-streams|reprocessing]] lever.

## Consumer group

Each function-based microservice must have its own independent [[consumer-group]], just like any non-FaaS microservice (source: chapter-09-microservices-using-function-as-a-service.md). The listener manages that consumer group on behalf of the function; the function itself does not see broker connections. This is what distinguishes the event-stream listener from the [[faas-triggers|consumer-group-lag trigger]], where the function owns the consumer client.

## Code shape

```
public int myEventfunction(Event[] events, Context context) {
    for (Event event : events) {
        // process event
    }
    context.success();   // tells FaaS framework the batch completed
    return 0;
}
```

The call to `context.success()` is what signals the framework to advance the committed offset — offsets are advanced **after** processing completes, which is the [[faas-offset-management|recommended strategy]].

## Relationship to other patterns

- **[[functions-as-a-service]]** — the broader pattern this is the canonical trigger for.
- **[[faas-triggers]]** — the full catalogue of FaaS trigger types; the event-stream listener is the one most relevant to EDM.
- **[[faas-offset-management]]** — the commit-after-processing discipline that fits cleanly into the listener model.
- **[[faas-batch-processing]]** — the batch-size / execution-time / halving-on-failure story.
- **[[consumer-group]] / [[consumer-offset]]** — what the listener is internally managing.
- **[[event-pipeline-pattern]]** — Burns's similar-shaped composition of FaaS nodes over webhooks; the listener is the event-stream counterpart when the edges are event streams instead of HTTP.

## Related pages

- [[functions-as-a-service]]
- [[faas-triggers]]
- [[faas-offset-management]]
- [[faas-batch-processing]]
- [[cold-start-warm-start]]
- [[consumer-group]]
- [[consumer-offset]]
- [[event-streams]]
- [[log-based-message-brokers]]
- [[event-driven-microservices]]
