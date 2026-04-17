# Mediator Topology

**Summary**: The second of Richards and Ford's two canonical [[event-driven-architecture|event-driven architecture]] topologies. A **central event mediator** accepts the initiating event and coordinates the workflow by generating a sequence of processing **commands** to dedicated event channels (usually point-to-point queues); event processors complete their assigned commands and acknowledge back to the mediator. Addresses the [[broker-topology]]'s weak points — **workflow control, error handling, and recoverability** — at the cost of **more complexity, lower peak performance, and the mediator itself as a scaling bottleneck**. Equivalent to Newman's **orchestrated [[saga]]**.

**Sources**: `raw/fundamentals-of-software-architecture/chapter-14-event-driven-architecture-style.md`

**Last updated**: 2026-04-16

---

## Structure

Five primary components (source: chapter-14-event-driven-architecture-style.md):

- **Initiating event** — same as in the [[broker-topology]]: the event that starts the flow.
- **Event queue** — the initial queue that the mediator listens on.
- **Event mediator** — the central coordinator. Knows the steps of the workflow; generates processing events (commands) for each step; tracks state; handles errors; owns recoverability.
- **Event channels** — dedicated queues for each step's commands. Usually **point-to-point queues** rather than pub/sub topics, because each command has exactly one intended consumer.
- **Event processors** — independent workers, each subscribed to its own dedicated channel. Unlike the broker topology, processors here **do not advertise what they did to the rest of the system** — they reply privately to the mediator.

The mediator is typically **not a single instance**. Most implementations use **multiple mediators** scoped to a domain (customer-events mediator, order-events mediator, billing-events mediator) to reduce the single-point-of-failure risk and improve throughput (source: chapter-14-event-driven-architecture-style.md).

## How it works

An initiating event arrives at the initiating-event queue. The mediator picks it up, generates a processing command for step 1 of the workflow, sends it to the dedicated queue for the step-1 processor, and waits for the acknowledgement. On acknowledgement it proceeds to step 2, which may fan out to multiple processors in parallel. The mediator waits for all parallel acknowledgements before proceeding to step 3, and so on until the workflow is complete. The mediator then clears the flow's state (source: chapter-14-event-driven-architecture-style.md).

## Mediator implementations

The chapter catalogues three classes of implementation, selected by the complexity of the workflow (source: chapter-14-event-driven-architecture-style.md):

| Complexity | Mediator technology | Notes |
|---|---|---|
| Simple error handling and orchestration | **Apache Camel, Mule ESB, Spring Integration** | Message routes custom-written in Java or C# |
| Lots of conditional processing, multiple dynamic paths, complex error handling | **Apache ODE, Oracle BPEL Process Manager** | BPEL (Business Process Execution Language) — XML-like, powerful, hard to learn, usually authored via a graphical BPEL engine suite |
| Long-running transactions with human intervention (approvals, holds, manual intervention) | **jBPM** | BPM engine — workflow can suspend indefinitely and resume on human action |

### Mediator delegation

Because it is **rare for all events in a system to be of one complexity class**, the chapter recommends a **delegation model**: every event flows through a **simple mediator** (Apache Camel / Mule) which inspects a classification (simple / hard / complex) on the incoming event and forwards it to the appropriate specialised mediator (BPEL or BPM). The simple mediator handles simple events itself and forwards the harder ones. This avoids the wrong-tool-for-the-job anti-pattern on both ends: using a BPM engine for a simple two-step flow takes months of wasted effort, and using Apache Camel for a multi-day human-approval flow is extremely difficult to write and maintain (source: chapter-14-event-driven-architecture-style.md).

## Worked example — retail order placement

The chapter walks through the same order-placement example as the broker topology, using a mediator instead (source: chapter-14-event-driven-architecture-style.md):

1. `PlaceOrder` arrives on `customer-event-queue`. The **Customer mediator** picks it up.
2. **Step 1** — mediator sends `create-order` to `order-placement-queue`. `OrderPlacement` processor validates and creates the order, replies with an acknowledgement and the order ID.
3. **Step 2** (parallel) — mediator sends three concurrent commands: `email-customer`, `apply-payment`, `adjust-inventory`. Mediator waits for all three acknowledgements before moving on.
4. **Step 3** (parallel) — mediator sends `fulfill-order` and `order-stock`. Both must acknowledge.
5. **Step 4** — mediator sends `email-customer` (ready-to-ship content) and `ship-order`.
6. **Step 5** — mediator sends final `email-customer` (shipped content). Marks the flow complete. Clears state.

The mediator **always knows which step the flow is in**. This is the structural property the broker topology lacks.

## Processing events are commands

In the mediator topology, messages from the mediator are **commands** — imperative instructions naming what the receiving processor must do (`place-order`, `send-email`, `apply-payment`, `fulfill-order`). This contrasts with the [[broker-topology]]'s **past-tense facts** (`order-created`, `payment-applied`).

Consequences of the command framing:

- **A command must be processed** by its target processor. It cannot be ignored (unlike an event in the broker topology).
- **The mediator owns the vocabulary** — it chooses which commands exist, in which order, to which processors. Processors do not advertise capabilities to each other.
- **Point-to-point queues** are the natural transport, not pub/sub topics.

## Error handling, state, and recovery

The mediator's knowledge of the workflow is what enables three properties the broker topology cannot offer (source: chapter-14-event-driven-architecture-style.md):

- **Error handling has a home.** When a processor in step 2 fails (e.g. the card is expired), the mediator receives the failure, knows step 3 cannot proceed, stops the workflow, and records state to its own persistent data store. When the problem is fixed, the flow resumes from the failed step.
- **State is explicit.** At any moment the mediator knows which initiating events are mid-flight and which step each is on. Operational dashboards can report this directly rather than reconstructing it from a log.
- **Recoverability** is native. A flow stopped by a processor failure can be resumed from the failed step rather than replayed from the initiating event.

The chapter's worked example: `apply-payment` fails because the card is expired. The mediator stops the flow, waits for the customer to update their card, and resumes from step 3 when the new payment succeeds. No compensating action is needed because `create-order` completed cleanly and the flow never advanced past step 2 for the database state the failure affected.

## Strengths

- **Workflow control** — the flow is explicit and centralised. Easy to reason about, easy to document, easy to debug.
- **Error handling** — has an owner. The mediator can retry, roll back, suspend, or escalate.
- **Recoverability** — flows can resume from the failed step.
- **State visibility** — the mediator is the authoritative source of in-flight flow state.

## Weaknesses

Four structural limitations the chapter makes explicit (source: chapter-14-event-driven-architecture-style.md):

- **Hard to model dynamic flows declaratively.** Complex branching and exception handling are painful to express in BPEL or Java routes. Real systems often use a **hybrid** — the mediator handles the general workflow, but a [[broker-topology]] sub-flow handles the dynamic parts (out-of-stock, fraud-hold, unusual error conditions).
- **Mediator scaling bottleneck.** Event processors scale independently just as in the broker topology, but the mediator itself must scale too — and is often a throughput ceiling. Per-domain mediator federation mitigates but does not eliminate this.
- **Tighter coupling** than the broker topology. Processors are bound to the mediator's command vocabulary.
- **Lower performance than broker topology.** The mediator adds a routing hop per step, serialises step transitions, and maintains persistent state — all of which cost latency and throughput.

## Relationship to orchestrated sagas

Newman's [[saga|orchestrated saga]] is the saga-level version of the mediator topology. The mechanics match:

- Both have a **central coordinator** that knows all the steps.
- Both use **point-to-point commands** (or request/response calls) to named participants.
- Both concentrate **domain coupling** in the coordinator.
- Both have the same risk: **anaemic participants** — logic that should live in participants drifts into the coordinator because the coordinator is the only place it can be centralised.
- Both handle **error handling and recovery** as first-class concerns — the coordinator owns them.

Newman's mitigation for coordinator-centric anaemia — **have different orchestrators for different flows** (Order Processor for placement, Returns for refunds, Goods Receiving for incoming stock, all calling a shared Warehouse service) — is the same shape as Richards and Ford's **federated mediators** (one per domain, each handling its own event class).

The terminology reconciliation: Richards and Ford's **mediator topology** is Newman's **orchestration** applied at the top level of the architecture. See [[saga]] for the saga-level framing and [[event-driven-architecture]] for the reconciliation table.

## When to use the mediator topology

- **Transactional integrity** across multiple processors matters. A flow that must atomically succeed or fail benefits from the mediator's ownership of state and error handling.
- **Complex, conditional workflows** with many branches. The mediator gives the workflow a declarative home.
- **Long-running flows with human intervention** — BPM engines can suspend for days or weeks while waiting for an approval.
- **Recoverability is a hard requirement.** The mediator's persisted state is what makes resumption possible.
- **Operational visibility** of in-flight flows is required — dashboards, audits, SLA tracking.

## When not to use

- **High-volume throughput** is the dominant characteristic and the mediator would be a bottleneck. Consider [[broker-topology]] or a hybrid.
- **Extensibility matters more than coordination** — new processors plugging into existing event feeds is harder when the mediator owns the command vocabulary.
- The flow is **genuinely simple and linear** — the mediator is overhead.

## Hybrid mediator + broker

Richards and Ford explicitly recommend **mixing the two topologies** when complex event processing has both predictable and dynamic parts (source: chapter-14-event-driven-architecture-style.md). The mediator handles the main workflow; dynamic or exceptional cases are handed off to a broker-topology sub-flow where pub/sub extensibility is more appropriate. The hybrid is also the answer to "how do I get the mediator's control over the happy path with the broker's extensibility for ad-hoc analytics listeners?" — expose an event feed from within the mediator-controlled flow for downstream consumers to subscribe to without interfering with the core workflow.

## Related pages

- [[event-driven-architecture]]
- [[broker-topology]]
- [[saga]]
- [[message-brokers]]
- [[correlation-ids]]
- [[eventual-consistency]]
- [[microservices]]
- [[service-based-architecture]]
- [[fundamentals-of-software-architecture]]
