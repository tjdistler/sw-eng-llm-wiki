# FaaS Batch Processing

**Summary**: The operational knobs for running batches of events through a function — batch size, batch window, maximum execution time, CPU/memory allocation. Mis-tuning any of these puts the function into a "fail-and-retry-and-fail-again" loop; Bellemare's escape hatches are increasing execution time, decreasing batch size, or using the automatic batch-halving feature some frameworks provide.

**Sources**: `raw/building-event-driven-microservices/chapter-09-microservices-using-function-as-a-service.md`

**Last updated**: 2026-04-17

---

## The four tunables

| Parameter | Controls |
|---|---|
| **Batch size** | Maximum events passed to a single invocation |
| **Batch window** | Maximum wait time before firing with whatever has arrived |
| **Maximum execution time** | Hard deadline — the function is killed when reached |
| **CPU / memory allocation** | Per-invocation resource budget |

Batch size and execution time are linked. Processing time per batch is roughly linear in the number of events, so a batch size that fits inside the deadline on one invocation will usually fit on the next. When the two fall out of sync, the function crosses the deadline before completing its batch and the invocation is marked failed (source: chapter-09-microservices-using-function-as-a-service.md).

## The failure loop

If a function fails its batch, the batch is retried. But with the same batch size and same deadline, the retry will usually fail for the same reason. Bellemare's two fixes (source: chapter-09-microservices-using-function-as-a-service.md):

1. **Increase the maximum execution time.** Give the function more room. Check that the ceiling doesn't violate the framework's hard limit (typically 5–10 minutes).
2. **Decrease the maximum batch size.** Less work per invocation, more invocations, more startup overhead, but the deadline is honored.

## Automatic batch halving

AWS Lambda and Azure Functions support automatic batch-halving: if a function fails, the framework halves the input batch and retries, and keeps halving until the function succeeds or each item has been tried alone (source: chapter-09-microservices-using-function-as-a-service.md). Effective when failures are size-dependent (timeouts, memory exhaustion), not when failures are data-dependent (a specific poisonous event that always fails regardless of batch size).

## Partial mid-batch commits

Functions that own their own event-broker client (the [[faas-triggers|lag-triggered]] or scheduled kind) can periodically commit offsets during processing, preserving partial progress if the function later times out. Functions receiving pre-consumed `Event[]` from an [[event-stream-listener]] cannot — they have no handle on which to commit. See [[faas-offset-management]] for the full treatment.

## Resource allocation

CPU and memory allocation is a cost lever separate from batch size (source: chapter-09-microservices-using-function-as-a-service.md):

- Over-allocation is expensive at steady-state.
- Under-allocation causes crashes or timeouts — the same failure loop as an undersized batch size.

External I/O budgets — to state stores, downstream services, or the event broker — are also part of the picture. A function that does heavy I/O per event needs a correspondingly large I/O budget even if its CPU work is trivial.

## Parallelism ceiling

For partitioned event streams where event order matters, the maximum parallelism of a FaaS deployment is bounded by partition count, same as any [[consumer-group]]. Queue-triggered functions where order doesn't matter scale unboundedly (source: chapter-09-microservices-using-function-as-a-service.md). This is the BEDM-wide ordering-vs-parallelism trade-off surfacing again at the function level.

## Related pages

- [[functions-as-a-service]]
- [[event-stream-listener]]
- [[faas-triggers]]
- [[faas-offset-management]]
- [[cold-start-warm-start]]
- [[consumer-group]]
- [[event-driven-microservices]]
