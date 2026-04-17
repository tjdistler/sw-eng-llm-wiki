# FaaS Offset Management

**Summary**: When a function-based microservice commits [[consumer-offset|consumer offsets]] — before or after processing — determines whether events can be lost on failure. Bellemare's rule: commit offsets **only after processing has completed**. Committing before is a common framework default that trades data-loss risk for simpler retry logic.

**Sources**: `raw/building-event-driven-microservices/chapter-09-microservices-using-function-as-a-service.md`

**Last updated**: 2026-04-17

---

## The two choices

A FaaS framework commits offsets for a batch of events at one of two times (source: chapter-09-microservices-using-function-as-a-service.md):

| When | Semantics | Risk |
|---|---|---|
| **After processing completes** | At-least-once, equivalent to non-FaaS microservices | None beyond normal reprocessing on failure |
| **When the function starts** | Fire-and-forget with framework-level retries | Data loss if retries exhaust — events go to a DLQ or are discarded |

## Committing after processing (the default for EDM)

This aligns FaaS with every other microservice style — basic producer/consumer clients and [[stream-processing]] frameworks alike commit offsets only after the work for the batch has finished. It gives the standard **at-least-once** guarantee: no event is dropped, but some may be processed more than once on failure. Combined with [[idempotence|idempotent]] processing, this is the path to [[effectively-once-processing|effectively-once]] semantics (source: chapter-09-microservices-using-function-as-a-service.md).

In the [[event-stream-listener]] model the signal that processing has completed is the call to `context.success()`. For lag-triggered or scheduled functions that own their own broker client, it is the explicit `client.commitOffsets()`.

## Committing when the function starts

Some FaaS frameworks commit offsets as soon as the batch has been dispatched to the function. The rationale is operational simplicity: the framework's own retry and alerting machinery is supposed to catch failures (source: chapter-09-microservices-using-function-as-a-service.md).

The risk is real: if all retries fail, the event is typically shunted to a dead-letter queue or simply dropped. For any workflow sensitive to data loss, this is the wrong default.

Bellemare notes that functions using choreographed direct-call composition (see [[faas-function-composition]]) often rely on this early-commit strategy because it simplifies progress tracking across chained invocations — at the cost of exactly this data-loss risk at the edges.

## Partial commits within a batch

Functions that establish their own broker connections can commit offsets periodically **during** execution, so partial progress survives a mid-batch failure (source: chapter-09-microservices-using-function-as-a-service.md). This is not available to functions that receive the pre-consumed `Event[]` from the event-stream listener — the function has no handle on which to commit.

This is one of the main reasons to prefer the lag or schedule triggers over the event-stream listener for workloads where batches are large and individual events are expensive.

## Consequence for failure handling

Because committing-after-processing is at-least-once, the correct design discipline is to make processing idempotent — via deduplication IDs, idempotent writes to external state, or upstream transactionality. The BEDM treatment of this lives at [[effectively-once-processing]] and [[idempotence]]; FaaS inherits it unchanged.

When a function fails to complete its batch within its allocated execution time, the batch must be processed again from the last committed offset. [[faas-batch-processing]] covers the parameter-tuning side of making sure this loop eventually succeeds.

## Related pages

- [[functions-as-a-service]]
- [[event-stream-listener]]
- [[faas-triggers]]
- [[faas-batch-processing]]
- [[faas-function-composition]]
- [[consumer-offset]]
- [[consumer-group]]
- [[effectively-once-processing]]
- [[idempotence]]
- [[event-driven-microservices]]
