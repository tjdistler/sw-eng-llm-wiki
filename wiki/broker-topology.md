# Broker Topology

**Summary**: The first of Richards and Ford's two canonical [[event-driven-architecture|event-driven architecture]] topologies. **No central mediator** — events flow peer-to-peer through a lightweight [[message-brokers|message broker]] (RabbitMQ, ActiveMQ, HornetQ) in a chain-like broadcasting fashion, with each event processor advertising what it did and other processors reacting if they are interested. Like a relay race: once a processor hands off the baton, it is done. Higher performance and extensibility than the [[mediator-topology]] at the cost of weaker error handling, no workflow control, and no recoverability. Equivalent to Newman's **choreographed [[saga]]**.

**Sources**: `raw/fundamentals-of-software-architecture/chapter-14-event-driven-architecture-style.md`

**Last updated**: 2026-04-16

---

## Structure

Four primary components (source: chapter-14-event-driven-architecture-style.md):

- **Initiating event** — the event that starts the flow (PlaceOrder, SubmitBid, ChangeJob, MaritalStatusChange).
- **Event broker** — a lightweight pub/sub-capable [[message-brokers|broker]] hosting the event channels. Usually **federated** — multiple domain-based clusters, each holding the channels for its domain.
- **Event processor** — an independent component that accepts events, does work, and advertises what it did as further processing events.
- **Processing event** — an event emitted by a processor after it has done its work, broadcast to a topic for whoever cares.

The channel is typically a **topic** (or AMQP topic exchange) rather than a queue, because the communication model is **pub/sub broadcast** — the producer does not know and does not care who is listening.

## How it works

An initiating event arrives at the event broker. A single event processor accepts it, does its piece of the work, and broadcasts a processing event describing what it did. Other processors listening to that topic react — each doing its own piece of work and broadcasting its own processing event — until no processor is interested in the final event in the chain (source: chapter-14-event-driven-architecture-style.md).

Richards and Ford's analogy: a **relay race**. Once a processor hands off the baton, it is done with the race and is free to pick up the next initiating or processing event. The baton moves through the chain until the last runner crosses the finish line.

## Worked example — retail order placement

The chapter's example (source: chapter-14-event-driven-architecture-style.md):

1. `OrderPlacement` receives `PlaceOrder` (initiating event), inserts the order, returns the order ID to the customer, then broadcasts `order-created`.
2. Three processors react to `order-created` in parallel:
   - `Notification` emails the customer, broadcasts `email-sent` (which nobody listens for — see "extensibility" below).
   - `Inventory` decrements the product inventory, broadcasts `inventory-updated` (picked up by `Warehouse` for restocking).
   - `Payment` charges the card and broadcasts either `payment-applied` or `payment-denied`. `Notification` listens for `payment-denied` to email the customer about the card problem.
3. `OrderFulfillment` listens for `payment-applied`, picks and packs, broadcasts `order-fulfilled`.
4. Both `Notification` and `Shipping` listen for `order-fulfilled` — `Notification` emails the customer, `Shipping` picks a shipping method, ships, and broadcasts `order-shipped`.
5. `Notification` listens for `order-shipped` too and sends the final status email.

No processor knows about the whole flow. Each one knows only what it listens for and what it emits.

## Extensibility is the killer feature

**Every processor should advertise what it did, even if nobody currently listens.** The chapter's `email-sent` event is broadcast but ignored — which looks wasteful until a new requirement arrives: analyse the emails sent to customers. The new analyser subscribes to the existing `email-sent` topic. No changes are needed to any existing processor or infrastructure. This is **architectural extensibility** (source: chapter-14-event-driven-architecture-style.md) and it is the broker topology's structural superpower — new functionality plugs into the existing event feed without changes to upstream producers.

The consequence: brokered event feeds are a design surface. Producers should emit events describing everything they do, not just events they currently have known consumers for.

## Strengths

- **Performance** — pure async, highly parallel. No centralised coordinator serialises anything.
- **Scalability** — each processor scales independently. Topics provide back pressure when one processor slows down.
- **Extensibility** — the five-star characteristic. New processors plug into existing event streams with no upstream changes.
- **Fault tolerance** — decoupled async processors survive each other's failures.
- **Responsiveness** — the initiating event's producer gets control back immediately.

## Weaknesses

Four structural limitations the chapter makes explicit (source: chapter-14-event-driven-architecture-style.md):

- **No workflow control** — nobody knows when the business transaction is "done" because nobody owns it. For dynamic flows with many conditional branches, this is an acceptable trade. For business transactions that must atomically succeed or fail, it is not.
- **No error handling** — if a processor crashes mid-flow, nobody notices. Other processors keep working as if everything is fine. Inventory is decremented even though payment never happened. The broker topology needs the **workflow event pattern** (see [[event-driven-architecture]]) to retrofit error handling.
- **No restart capability** — once the initiating event has been broadcast and the chain has started, re-submitting the initiating event re-runs the whole chain. No processor owns enough state to know where the flow stopped. Recoverability is not a property this topology provides.
- **No transaction integrity** — there is no saga-like coordination across processors. This is why the event-driven style rates three stars on data integrity overall, and why mixing broker-topology EDA with [[saga|sagas]] is a common real-world pattern.

## Processing events are past-tense facts

In the broker topology, processing events name **things that have happened** (`order-created`, `payment-applied`, `inventory-updated`, `email-sent`). This is a small but load-bearing difference from the [[mediator-topology]], where messages are **commands** (`place-order`, `send-email`, `apply-payment`).

Consequences of the event-as-fact framing:

- **An event can be ignored.** Not every emitted event needs a listener. Architectural extensibility depends on this.
- **Events encourage decentralised ownership.** Each processor decides which facts it cares about. No central authority decides what the flow must do.
- **Event names should describe what happened in the domain vocabulary**, not what the producer wants the rest of the system to do.

## Relationship to choreographed sagas

Newman's [[saga|choreographed saga]] is the saga-level version of the broker topology. The mechanics match:

- Both use **pub/sub events on a message broker** for inter-participant communication.
- Neither has a central coordinator. Workflow is **implicit in the event chain**.
- Both rely on a [[correlation-ids|correlation ID]] to reason about saga/flow state after the fact.
- Both have the same weakness: **saga state is distributed** and must be reconstructed from the event log if anyone needs to know whether the flow completed.
- Both loosely couple participants and scale independent team ownership.

The terminology reconciliation: Richards and Ford's **broker topology** is Newman's **choreography** applied at the top level of the architecture. See [[saga]] for the saga-level framing and [[event-driven-architecture]] for the reconciliation table.

## When to use the broker topology

- **Simple, linear event flows** — each processor is interested in a small number of upstream events.
- **High performance and responsiveness** matter more than overall workflow control.
- **Extensibility** is a first-order requirement — the set of listeners changes over time and new capabilities should plug in without upstream changes.
- **Multiple teams** own different processors and need to move independently.

## When not to use

- The flow requires **strong transactional integrity** (all-or-nothing multi-processor success). Use the [[mediator-topology]] or embed [[saga|sagas]] on top.
- **Error handling and recovery** must be explicit and owned somewhere. The broker topology does not provide this.
- The flow is **heavily conditional** — many branches depending on data or upstream state. A mediator's explicit workflow model will be easier to reason about than a web of pub/sub listeners.

## Related pages

- [[event-driven-architecture]]
- [[mediator-topology]]
- [[saga]]
- [[message-brokers]]
- [[publisher-subscriber-infrastructure]]
- [[event-streams]]
- [[correlation-ids]]
- [[event-driven-batch-pattern]]
- [[event-pipeline-pattern]]
- [[microservices]]
- [[fundamentals-of-software-architecture]]
