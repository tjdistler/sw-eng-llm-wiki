# FaaS Function Composition

**Summary**: How multiple functions cooperate to deliver a bounded context. Bellemare catalogues two patterns — **event-driven communication** (functions produce to event streams that other functions consume) and **direct call** (functions invoke other functions directly). Both can be used for either [[workflows-in-edm|choreography or orchestration]], but their failure modes and ordering guarantees differ sharply.

**Sources**: `raw/building-event-driven-microservices/chapter-09-microservices-using-function-as-a-service.md`

**Last updated**: 2026-04-17

---

## The two patterns

| Pattern | Connection | Failure recovery | Order | Coupling |
|---|---|---|---|---|
| **Event-driven communication** | Internal event streams between functions | Durable log → replay | Preserved per partition | Minimal (via schemas) |
| **Direct call (async)** | Function A invokes function B inline | Must be handled by caller; DLQs on failure | Not preserved | Function A knows B's name |
| **Direct call (sync)** | Function A invokes function B and awaits | Failures propagate up; caller orchestrates | Preserved if enforced by caller | Function A knows B's name |

## Event-driven communication

Each function is wired into its own input and output event streams. Function A emits events; function B subscribes; function C subscribes to B's output (source: chapter-09-microservices-using-function-as-a-service.md). Internal event streams are strictly scoped to the bounded context — any stream the owners do not intend for external consumption should be access-restricted.

Benefits (source: chapter-09-microservices-using-function-as-a-service.md):

- Each function manages its own [[consumer-offset|consumer offsets]] independently.
- No coordination is required outside the event stream mechanics.
- Failures never lose data — events are durably stored and get reprocessed by the next function instance.
- Defaults to choreography (each function reacts autonomously), but orchestration can be layered on by routing all intermediate work through an orchestrator function.

This is the FaaS-specific realization of the [[broker-topology]] and of Newman's choreographed [[saga]], down to the same "emergent workflow" property that makes it easy to append and hard to reorder.

## Direct-call pattern (asynchronous)

Function A invokes function B from its own code, fire-and-forget: no return value, no result awaited (source: chapter-09-microservices-using-function-as-a-service.md).

```
public int functionA(Event[] events, Context context) {
    for (Event event : events) {
        // Function A's work
        asyncfunctionB(event);   // does not wait
    }
    context.success();
    return 0;
}
```

This is a choreography-style composition. It has two failure modes Bellemare calls out explicitly (source: chapter-09-microservices-using-function-as-a-service.md):

- **Offset commits can race the work.** Function A's `context.success()` advances its offset regardless of whether any B invocation eventually succeeds. If B fails and retries exhaust, data is lost — unless the workflow tolerates loss.
- **Out-of-order processing.** Multiple B instances run in parallel and may finish in any order. If B's work depends on B-instance-k having seen B-instance-(k-1)'s output (e.g., writing to a shared external store), the workflow produces nondeterministic results.

Bellemare's caveat: restructuring the loop to batch-call B once at the end of A does **not** fix ordering — A's per-event work still executes for the whole batch before any B invocation, which is equally bad when B depends on A's per-event output.

## Direct-call pattern (synchronous / orchestration)

Function A (now an orchestrator) invokes function B, awaits the result, invokes C, awaits, composes an output, and moves to the next event (source: chapter-09-microservices-using-function-as-a-service.md):

```
public int orchestrationFunction(Event[] events, Context context) {
    for (Event event : events) {
        Result a = invokeFunctionA(event);
        Result b = invokeFunctionB(event, a);
        Output output = composeOutputEvent(a, b);
        producer.produce("Output Stream", output);
    }
    context.success();
    return 0;
}
```

Each event is fully processed — through A, through B, through the output producer — before the next event starts. That is the only pattern that preserves ordering when multiple functions share downstream state (source: chapter-09-microservices-using-function-as-a-service.md). This is the FaaS realization of the [[mediator-topology]] and of the orchestrated [[saga]].

For queue-triggered workloads where commits are per-event, the orchestrator simply runs once per event, confirming each item back to the queue on success.

## Choosing a composition

The decision rule (source: chapter-09-microservices-using-function-as-a-service.md):

- **Event-driven communication** is the default for EDM — durable, decoupled, and loss-free. Use unless you have a specific reason not to.
- **Synchronous direct calls** are the right shape when you need strict ordering of multiple steps per event and the steps are light enough to complete within one function's lifetime.
- **Asynchronous direct calls** are a last resort — faster to write but opaque about success, lossy, and order-breaking. Use only when data loss is tolerable and ordering doesn't matter.

## Bounded context discipline

Regardless of composition, Bellemare's strict rule: every function in the composition must belong to one clearly identified [[bounded-context]], and internal event streams must be access-restricted to functions inside it (source: chapter-09-microservices-using-function-as-a-service.md). The "reusable function across many services" trap is called out as a specific anti-pattern — it fragments ownership, makes change risk opaque, and forces versioning overhead that quickly rivals the cost of just duplicating the function. His rule of thumb: **fewer functions are better than many granular ones**.

## Related pages

- [[functions-as-a-service]]
- [[event-stream-listener]]
- [[faas-triggers]]
- [[faas-offset-management]]
- [[workflows-in-edm]]
- [[compensation-workflow]]
- [[saga]]
- [[broker-topology]]
- [[mediator-topology]]
- [[bounded-context]]
- [[event-driven-microservices]]
