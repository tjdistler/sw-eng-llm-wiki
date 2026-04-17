# Workflows in Event-Driven Microservices

**Summary**: How multiple [[event-driven-microservices|event-driven microservices]] work together to fulfill larger business processes. A workflow is a set of actions — including branching and compensatory actions — that composes a business process across several microservices, each within its own [[bounded-context]]. Bellemare's Chapter 8 frames two canonical patterns for stitching services together into a workflow: **choreography** and **orchestration**, and treats [[distributed-transactions]] (aka [[saga|sagas]]) as a special transactional case of either pattern.

**Sources**: `raw/building-event-driven-microservices/chapter-08-building-workflows-with-microservices.md`, `raw/building-event-driven-microservices/chapter-09-microservices-using-function-as-a-service.md`

**Last updated**: 2026-04-17

---

## What a workflow is

A workflow is a particular set of actions that compose a business process, including any logical branching and compensatory actions. Workflows commonly require multiple microservices, each with its own bounded context, performing its tasks and emitting new events to downstream consumers (source: chapter-08-building-workflows-with-microservices.md).

Bellemare's three workflow design concerns:

1. **Creating and modifying workflows** — how are the services related? Can I reorder or insert steps without breaking in-flight events, forcing changes in many services, or breaking monitoring?
2. **Monitoring workflows** — can I tell whether a specific event has completed, is stuck, or has failed? Can I see the overall health of the workflow?
3. **Implementing distributed transactions** — when many actions must succeed or fail together, how do I implement the transaction and its rollback?

## The two patterns

| Pattern | Coordinator | Message semantics | Workflow lives in | Bellemare's analogy |
|---|---|---|---|---|
| **Choreography** | None. Emergent from service relationships | Past-tense facts (events) | The *relationships* between services | A dance: each dancer knows their role and performs independently |
| **Orchestration** | A central orchestrator microservice | Imperative commands | A single orchestrator service | An orchestra: one conductor directs the musicians |

These are the same two shapes named by Richards & Ford's [[broker-topology]] / [[mediator-topology]] at the architecture-style level, and by Newman's **choreographed** / **orchestrated** [[saga]] at the business-process level. Bellemare's Chapter 8 gives them their EDM-specific treatment.

## Choreography in EDM

Choreographed (also *reactive*) architectures are highly decoupled — microservices react to input events as they arrive, without blocking or waiting, independent of upstream producers or downstream consumers (source: chapter-08-building-workflows-with-microservices.md). Communication happens strictly through input and output event streams. A producer does not know who consumes its data or why.

**Properties:**

- **Emergent workflow.** The business workflow is a form of emergent behavior: defined by the relationships between services, not by any single service. A → B → C is visible only in how the services wire up to streams.
- **Easy append.** Adding a new step at the end of a workflow is trivial — subscribe a new service to the last output stream.
- **Hard reorder.** Inserting a step into the middle or swapping two steps can be problematic. Services must be edited to consume from different streams; schemas may need to change; existing in-flight events must be fully drained before the topology is rearranged (source: chapter-08-building-workflows-with-microservices.md).
- **Monitoring is scoped to the observer.** Full end-to-end visibility requires materializing every participating event stream. Partial visibility — a customer's payment → fulfillment → shipping progress — can be built by tapping off just the streams that matter.
- **Belongs to the EDM world.** Because producers and consumers are decoupled through event streams, choreography is natural to event-driven architectures. In contrast, direct-call microservice architectures force the caller to know *which* service to call and *why* — so they are tightly coupled and fit orchestration better than choreography.

## Orchestration in EDM

An **orchestrator microservice** holds the workflow logic for the business process. It issues commands to subordinate worker microservices and awaits their responses, typically through event streams (source: chapter-08-building-workflows-with-microservices.md).

**Properties:**

- **Workflow lives in one place.** Changing the order of steps, inserting a step, or adding error handling is a single-service change.
- **State is explicit.** The orchestrator materializes the per-event progress of every in-flight workflow. Monitoring is a query against that materialized state — easy by comparison to tapping a web of streams.
- **Orchestrator bounded context must stay narrow.** Bellemare's tip: *"Ensure the orchestrator's bounded context is limited strictly to workflow logic and that it contains minimal business fulfillment logic."* The orchestrator decides *what to do next*; the workers decide *how to do it*. (source: chapter-08-building-workflows-with-microservices.md)
- **The "God service" anti-pattern.** A common failure mode: the orchestrator issues granular commands to weak minion services, spreading business logic across the orchestrator and diluting the workers' bounded contexts. This makes teams hard to scale around the workflow. Keep workers responsible for their own retry policy, error handling, and transient-failure management — the orchestrator should not micromanage these (source: chapter-08-building-workflows-with-microservices.md).
- **Retries are local.** A payment service that retries three times before giving up does so *internally*. The orchestrator learns only "succeeded" or "failed," never participates in the retry loop.

The orchestrator's control loop is straightforward — consume from the input stream and each worker's response stream, update materialized state, dispatch the next command:

```
while (true) {
  for (Event event : consumer.consume(streams)) {
    if (event.source == "Input Stream") { process; produce to Stream 1 }
    else if (event.source == "Stream 1-Response") { process; produce to Stream 2 }
    else if (event.source == "Stream 2-Response") { process; produce to Stream 3 }
    else if (event.source == "Stream 3-Response") { compose and emit final output }
  }
  consumer.commitOffsets()
}
```

(adapted from source: chapter-08-building-workflows-with-microservices.md)

## Direct-call vs event-driven orchestration

Orchestration can use either an event-driven request/response pattern (commands and responses flow on event streams) or a synchronous direct-call pattern (the orchestrator calls worker APIs and blocks on the response). The topologies look nearly identical; the trade-offs differ (source: chapter-08-building-workflows-with-microservices.md).

| | Event-driven orchestration | Direct-call orchestration |
|---|---|---|
| Speed | Slower — produce/consume overhead per step | Faster — no broker hop |
| Durability | Higher — broker isolates orchestrator from worker failures, built-in retry via stream replay | Intermittent connectivity must be handled by the orchestrator |
| Monitoring | Reuses the same lag/I-O tooling as other EDMs | Custom |
| Reuse | Other services can consume the command/response streams too | Streams do not exist |
| Best fit | Most workflows; robust against partial failures | Real-time operations with tight SLAs |

A common real-world shape is a predominantly event-driven orchestration that makes direct calls to external APIs or preexisting services at specific steps. When mixing the two, each service's failure modes must be handled explicitly.

Direct-call orchestration is also the natural shape for FaaS-based workflows — see [[functions-as-a-service]], [[faas-function-composition]], and [[event-pipeline-pattern]]. Bellemare's Chapter 9 treatment maps the event-driven variant onto FaaS's **event-driven communication pattern** (functions connected by internal event streams) and the direct-call variant onto FaaS's **direct-call pattern** (synchronous orchestrator or asynchronous choreography of function invocations) — with the critical caveat that async direct calls break ordering guarantees and risk data loss at offset-commit time (source: chapter-09-microservices-using-function-as-a-service.md).

## Transactional workflows — sagas

Distributed transactions in the EDM context are what Bellemare (following the common usage) calls **sagas**. A saga can be implemented as either a choreographed saga or an orchestrated saga; both require each participating microservice to provide an **idempotent reversal action** for its portion of the transaction. Both the regular and the reversing actions must be idempotent so that transient failures cannot leave the system inconsistent (source: chapter-08-building-workflows-with-microservices.md).

Bellemare's warning lines up with Richards & Ford's and with Newman's: **avoid distributed transactions whenever possible.** They add significant risk and complexity — synchronization, rollbacks, transient failures, network connectivity. Use them only when avoiding them would cause *more* risk and complexity (source: chapter-08-building-workflows-with-microservices.md).

See [[saga]] for the full treatment and for the Newman / Richards-and-Ford reconciliation.

### Choreographed sagas — specifics

A choreographed saga chains services in order (A → B → C) with each service's failure triggering a reverse chain (C-fail → B-reverts → A-reverts). Bellemare's observations (source: chapter-08-building-workflows-with-microservices.md):

- **The success-status and failure-status streams are different.** Successful transactions' final status comes out of the last service (C); aborted transactions' status comes out of the first service (A). A consumer that wants the full picture has to listen to both. This *is* consistent with the [[single-writer-principle]] (each service is the sole writer to its own streams), but it forces consumers to stitch multiple streams together.
- **In-flight transaction state is invisible** without materializing each participating stream, or exposing internal state via API.
- **Workflow changes carry an extra cost** compared to a nontransactional choreographed workflow — every reordering must also rework the reversal chain.
- **Best fit:** very small participant sets (pairs or trios), strict ordering, low likelihood of workflow change.

### Orchestrated sagas — specifics

An orchestrated saga's orchestrator knows the forward workflow *and* the reversal workflow. On failure from a worker it issues rollback commands to whichever services have already acted. Bellemare's observations (source: chapter-08-building-workflows-with-microservices.md):

- **Signals beyond success/failure.** The orchestrator can act on timeouts (periodically check how long a transaction has been processing) and on human inputs (cancellation instructions via a REST API). These are hard to retrofit into a choreographed saga.
- **Rollback is the orchestrator's responsibility, but *state consistency* is the worker's.** The orchestrator issues the rollback command; the worker must ensure its own state is consistent after the rollback. If a worker fails *during* a rollback, the orchestrator decides what to do next — retry, alert, terminate.
- **Single output stream for transaction status.** Because the orchestrator is the single writer, both successful and aborted transaction results flow out of the same stream — simpler than the choreographed case.
- **In-flight status can be exposed** by the orchestrator updating the transaction entity as worker responses arrive.
- **Best fit:** complex workflows, many participants, workflows subject to change, workflows requiring visibility.

### Compensation as an alternative to rollback

Not every workflow needs to be perfectly reversible. Some can complete "best-effort" and rely on a **[[compensation-workflow]]** to remedy failures after the fact — order new stock and offer a discount code rather than roll back the purchase. See [[compensation-workflow]] for the pattern and when it fits.

## Choosing between the two patterns

Bellemare's Chapter 8 summary (source: chapter-08-building-workflows-with-microservices.md):

- **Choreography** fits simple distributed transactions and simple non-transactional workflows where the microservice count is low and the order is unlikely to change. Best for loose coupling between business units and independent workflows.
- **Orchestration** fits workflows that are subject to change and contain many independent microservices, that need complex transactional behavior, or that need strong visibility and monitoring. The single-location change for workflow edits is often decisive.
- **Compensation** is the pragmatic escape hatch when neither strict transactions nor pure choreography fit the business reality — use a compensating workflow and let non-technical parts of the business solve the customer-facing issue.

This echoes Newman's team-boundary heuristic in [[saga]] — single team → orchestration is fine, multiple teams → choreography matches the team topology — and Richards & Ford's topology trade-offs in [[broker-topology]] and [[mediator-topology]].

## Related pages

- [[event-driven-microservices]]
- [[saga]]
- [[distributed-transactions]]
- [[compensation-workflow]]
- [[broker-topology]]
- [[mediator-topology]]
- [[event-driven-architecture]]
- [[business-topology]]
- [[microservice-topology]]
- [[single-writer-principle]]
- [[bounded-context]]
- [[idempotence]]
- [[effectively-once-processing]]
- [[synchronous-microservices]]
- [[correlation-ids]]
- [[functions-as-a-service]]
- [[faas-function-composition]]
