# Saga

**Summary**: An algorithm for coordinating a sequence of state changes across multiple services without holding distributed locks. The original 1987 paper by Hector Garcia-Molina and Kenneth Salem proposed sagas to handle long-lived transactions; modern microservice architectures use them as the standard alternative to [[two-phase-commit|2PC]] / [[distributed-transactions]].

**Sources**: `raw/monolith-to-microservices/chapter-04-decomposing-the-database.md`

**Last updated**: 2026-04-16

---

## What a saga is

A saga is a single business process modelled as a sequence of **independent transactions**, each of which can be carried out and committed by a different service. Instead of locking resources across the whole flow (as 2PC would), each step does its work in a local ACID transaction and the saga as a whole reasons about progress and failure. (source: chapter-04-decomposing-the-database.md)

The original framing came from Hector Garcia-Molina and Kenneth Salem's 1987 paper "Sagas," which addressed **long-lived transactions** (LLTs) — operations that take minutes, hours, or days. Mapping an LLT to one DB transaction would lock data for the duration; instead, decompose it into shorter sub-transactions whose locks are short-lived. (source: chapter-04-decomposing-the-database.md)

Sagas extend naturally from one-database-many-LLTs to multiple-services-one-business-process.

## What a saga does NOT give you

A saga does **not give you ACID atomicity at the saga level.** Each step is atomic locally; the saga as a whole is not. What it gives you is *enough information to reason about which state the saga is in*. You then handle the implications. (source: chapter-04-decomposing-the-database.md)

This is the central trade-off: you give up the all-or-nothing illusion, and you get back the ability to coordinate change across services without the pathologies of [[distributed-transactions]].

## Failure recovery: backward and forward

The saga paper describes two recovery modes (source: chapter-04-decomposing-the-database.md):

- **Backward recovery** (rollback) — undo the steps that already committed by running **compensating actions**. You explicitly define an undo operation for each step of the saga.
- **Forward recovery** — pick up from the failure point and keep going. Requires the system to persist enough state to retry.

Real sagas mix the two. After payment is taken and an item is packaged, "we can't dispatch" is more naturally a forward-recovery problem (retry, then escalate to a human) than a wholesale rollback.

### Compensating actions are not rollbacks

Database rollback erases the transaction as if it never happened. A saga compensating action is a *new* transaction that semantically reverses a previous one — but the previous one really did happen. Newman calls these **semantic rollbacks**.

If a step sent an email, you can't unsend it. The compensation is a *second* email saying the order was cancelled. (source: chapter-04-decomposing-the-database.md)

It is appropriate — even valuable — to keep records of failed/aborted sagas in the system. The history matters.

### Reorder steps to reduce rollbacks

If a step is failure-prone, **move it earlier** in the saga; if a step is hard to compensate, **move it later** (or after the failure-prone steps).

Newman's example: award loyalty points only after the order is dispatched, not before. Then if packaging or dispatch fails, there's no points-awarded transaction to compensate. (source: chapter-04-decomposing-the-database.md)

## Two implementation styles

Sagas can be implemented in two opposing styles, and the trade-off recapitulates many themes of microservices architecture.

### Orchestrated sagas

A central **orchestrator** coordinates the saga: knows the steps, calls each service in turn, decides what to do on failure. Typically heavy on request/response calls. (source: chapter-04-decomposing-the-database.md)

**Pros:**
- The business process is **explicitly modelled** in one place. Onboarding new developers is easier; debugging is easier.
- Failure handling has an obvious home.

**Cons:**
- **Domain coupling** is concentrated — the orchestrator must know about all participating services.
- **Anaemic services** — logic that should live in services drifts into the orchestrator. ("If logic has a place where it can be centralized, it will become centralized.")

Mitigation: have *different* orchestrators for different flows (Order Processor for placement, Returns for refunds, Goods Receiving for incoming stock), each calling shared services like Warehouse. (source: chapter-04-decomposing-the-database.md)

### Choreographed sagas

No central coordinator. Each service reacts to events and emits its own. Heavy use of pub/sub via a [[message-brokers|message broker]]. (source: chapter-04-decomposing-the-database.md)

**Pros:**
- **Loose coupling** — no service knows about all the others; each just knows what to do when an event arrives.
- No risk of logic centralisation.
- Easier to distribute responsibility across teams.

**Cons:**
- **No explicit business process model** — the flow is implicit in the events. Building a mental model requires reading every service.
- **Saga state is distributed** — knowing whether a saga is mid-flight or completed is not directly visible anywhere.

The state-visibility problem has a standard fix: a **correlation ID** attached to every event in the saga, plus a service that aggregates events by correlation ID and projects the saga's current state. (source: chapter-04-decomposing-the-database.md)

### Mixing styles

Newman explicitly endorses mixing. A choreographed top-level saga can have orchestrated sub-sagas inside individual services (e.g. Warehouse's internal "package and dispatch" flow). Just keep visibility of overall progress so failure modes remain debuggable. (source: chapter-04-decomposing-the-database.md)

## Choreography or orchestration: when to choose what

Newman's heuristic (source: chapter-04-decomposing-the-database.md):

- **Single team owns the whole saga** → orchestration is fine. The coupling is internal to the team.
- **Multiple teams own different participants** → choreography. Distributing responsibility matches the team boundaries; loose coupling lets teams move independently.

His personal preference leans choreography, accepting the extra complexity of tracking saga state in exchange for the architectural decoupling.

## A note on BPM tools

Business process modelling tools (e.g. older enterprise platforms) are often pitched for orchestrated sagas. Newman's experience: the central conceit — that nondevelopers will define business processes — almost never holds. Developers end up using GUI-based tools that are hard to version-control and test. (source: chapter-04-decomposing-the-database.md)

He'd rather see business processes implemented in code, with visualisations *projected from* the code. He notes Camunda and Zeebe as more developer-friendly modern alternatives if you really want orchestration tooling.

## Sagas vs distributed transactions

Pat Helland on distributed transactions: "When flying an airplane that needs all of its engines to work, adding an engine reduces the availability of the airplane." (Helland, "Life Beyond Distributed Transactions") (source: chapter-04-decomposing-the-database.md)

In Newman's experience, modelling business processes as sagas avoids most of the operational pitfalls of distributed transactions and has a side benefit: it makes the core business processes of the system **explicit and first-class**, where they were previously implicit and scattered. (source: chapter-04-decomposing-the-database.md)

See [[distributed-transactions]] for the operational problems sagas avoid, and [[two-phase-commit]] for why "just say no."

## Related pages

- [[database-decomposition]]
- [[two-phase-commit]]
- [[distributed-transactions]]
- [[transactions]]
- [[acid]]
- [[message-brokers]]
- [[event-streams]]
- [[change-data-capture]]
- [[event-sourcing]]
- [[eventual-consistency]]
- [[coupling]]
- [[bounded-context]]
