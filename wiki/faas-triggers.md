# FaaS Triggers

**Summary**: The signals that cause a FaaS framework to start a function. Bellemare catalogues five categories — event-stream listener, consumer-group lag, schedule, webhook, and resource events — that between them cover every common use case for function-based event-driven microservices.

**Sources**: `raw/building-event-driven-microservices/chapter-09-microservices-using-function-as-a-service.md`

**Last updated**: 2026-04-17

---

## The five categories

Specific trigger types vary by FaaS framework but fall into one of five categories (source: chapter-09-microservices-using-function-as-a-service.md):

| Trigger | Signal | Who owns the consumer client | Order preserved |
|---|---|---|---|
| **[[event-stream-listener]]** | Event arrives in subscribed stream | The FaaS framework | Yes (if synchronous dispatch) |
| **Consumer-group lag** | Lag metric crosses threshold | The function itself | Depends on function |
| **Schedule** | Wall-clock interval or datetime | The function itself | Depends on function |
| **Webhook** | Direct HTTP invocation | N/A | N/A |
| **Resource event** | External filesystem / datastore change | The function / framework | Generally no |

## Event-stream listener

The framework consumes from the event stream and passes a batch of events into the function. This is the default EDM trigger. See [[event-stream-listener]] for the full treatment, including batch size, batch window, synchronous vs asynchronous dispatch, and the integrated-vs-external listener distinction.

## Consumer-group lag

Periodically poll the offsets of an application's consumer groups, compute the delta against the head of the stream, and report it to a monitoring framework. When lag crosses a configured threshold, the monitoring framework calls the FaaS framework to start a function (source: chapter-09-microservices-using-function-as-a-service.md).

The critical difference from the event-stream listener is that the function does **not** receive events pre-consumed. It is passed only the consumer group and stream name in its `Context`; it must establish its own event-broker client, consume events, do the work, and commit offsets itself. This makes lag-triggered functions look more like a basic producer/consumer client with a limited lifespan:

```
public int myLagConsumerfunction(Context context) {
    EventBrokerClient client = new EventBrokerClient(context.consumerGroup, ...);
    Event[] events = client.consumeBatch(context.streamName, ...);
    for (Event event : events) doWork(event);
    client.commitOffsets();
    context.success();
    return 0;
}
```

Lag can also be used to decide **how many** function instances to start: high lag spins up several, low lag a single one. You can tailor the relationship between lag quantity and function startup per microservice to meet SLAs.

## Schedule

Functions can be triggered on a cron-style interval or at specific datetimes. A scheduled function typically polls its source event streams for new events, processes them, and shuts down (source: chapter-09-microservices-using-function-as-a-service.md). Client code looks identical to the consumer-group-lag example — the function owns the broker client.

The tuning tension is standard: poll too often and you load the FaaS framework and broker; poll too rarely and SLAs slip.

## Webhook

Direct invocation via HTTP — the escape hatch for integrating with monitoring frameworks, custom schedulers, and third-party applications that don't speak the event broker's protocol (source: chapter-09-microservices-using-function-as-a-service.md). Semantically equivalent to Burns's [[event-pipeline-pattern]] edges.

## Resource events

Changes to files or database rows — creates, updates, deletes — can trigger functions. Rare in EDM because most data flows through event streams, but useful for integrating with external sources that drop files via FTP or similar (source: chapter-09-microservices-using-function-as-a-service.md).

## Choosing a trigger

The trigger determines where the boundary between "the FaaS framework" and "the function's code" falls (source: chapter-09-microservices-using-function-as-a-service.md):

- **Event-stream listener** — pushes the most responsibility into the framework. Events, consumer group, and offsets are all framework-managed. Simplest function code; tightest coupling to the framework.
- **Lag / schedule** — the function owns the broker client, offset commits, and rebalancing. More code, more portability, and more control over [[consumer-offset]] semantics.
- **Webhook / resource event** — non-EDM escape hatches.

## Rebalancing and trigger thrash

Frequent trigger firing with short-lived functions and small batch sizes can cause near-constant consumer-group rebalancing, preventing progress (source: chapter-09-microservices-using-function-as-a-service.md). Bellemare's remedies:

- Step-based scaling or hysteresis loops to dampen trigger response.
- Static partition assignments, which skip rebalancing entirely.
- Scale up or down at most once every few minutes.

## Related pages

- [[functions-as-a-service]]
- [[event-stream-listener]]
- [[faas-offset-management]]
- [[faas-batch-processing]]
- [[cold-start-warm-start]]
- [[consumer-group]]
- [[consumer-offset]]
- [[event-driven-microservices]]
