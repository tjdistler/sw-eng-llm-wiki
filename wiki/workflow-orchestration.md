# Workflow Orchestration

**Summary**: The **coordination** style for distributed workflows in which a dedicated **orchestrator (mediator)** service owns workflow state, sequences steps across participants, and handles errors centrally. One of two canonical coordination patterns named in Chapter 11 of *Software Architecture: The Hard Parts*, alongside [[workflow-choreography]]. This page covers workflow orchestration **as a distributed-architecture pattern** — the star-ish topology in which participants are domain services and the orchestrator is a neutral conductor. It is *distinct from* the [[orchestration|data-engineering orchestration]] page, which covers job-DAG schedulers like Airflow.

**Sources**: `raw/software-architecture-the-hard-parts/chapter-11-managing-distributed-workflows.md`

**Last updated**: 2026-04-19

---

## Definition

> The orchestration pattern uses an orchestrator (sometimes called a mediator) component to manage workflow state, optional behavior, error handling, notification, and a host of other workflow maintenance. (source: raw/software-architecture-the-hard-parts/chapter-11-managing-distributed-workflows.md)

The name comes from the musical orchestra analogy — a **conductor** synchronises otherwise-independent players. In a distributed architecture, the orchestrator is the conductor; domain services are the players; each owns its bounded context, data, and behaviour. The orchestrator itself **does not contain domain behaviour** outside the workflow it mediates.

Chapter 11 is explicit that in a [[microservices]] architecture, orchestration means **one orchestrator per workflow**, not a global orchestrator such as an [[orchestration-driven-soa|enterprise service bus]]. A global ESB-style mediator recreates the coupling problem microservices were designed to avoid; per-workflow orchestrators preserve the architecture's decoupling goals while still giving a given workflow a home.

## Worked example — Penultimate Electronics order

Chapter 11's running example (source: raw/software-architecture-the-hard-parts/chapter-11-managing-distributed-workflows.md):

1. `Place Order` request hits the **Order Placement Orchestrator**.
2. Orchestrator calls **Order Placement Service** (sync) — records the order, returns status.
3. Orchestrator calls **Payment Service** (sync) — payment verification needs strict timing.
4. Orchestrator calls **Fulfillment Service** (async) — no strict timing, no reason to block.
5. Orchestrator calls **Email Service** (async) — notify user of successful purchase.

The dotted lines in the book's Figure 11-4 denote async calls; the orchestrator mixes sync and async calls as each step's timing requirements dictate.

### Error scenario 1: payment rejected

Payment Service rejects the card (e.g. expired). It reports failure to the orchestrator. The orchestrator then:

- Asynchronously tells Email Service to notify the customer of the failed order.
- Updates Order Placement Service to mark the order inactive.

**No new communication paths** are required — every link used by the error handler already existed for the happy path. This is a structural property of orchestration: all participants talk to the orchestrator and only the orchestrator, so error flows route through the same spokes.

### Error scenario 2: item back-ordered

Fulfillment Service reports back order to the orchestrator mid-workflow. The orchestrator must:

- Refund the payment (this is why many online services don't charge until shipment).
- Update Order Placement Service to reflect the deferred state.

Again, **no new paths**. Contrast with [[workflow-choreography]], where each error scenario typically adds a new inter-service link.

## Advantages

Chapter 11 enumerates four (source: raw/software-architecture-the-hard-parts/chapter-11-managing-distributed-workflows.md):

- **Centralized workflow** — as workflow complexity grows, having one component that holds state and sequencing logic is where that complexity belongs.
- **Error handling** — error handling is often the majority of real workflow code. A state-owning orchestrator has an obvious home for it.
- **Recoverability** — the orchestrator can retry a step, wait out a transient outage, or resume from the failed step.
- **State management** — the workflow's state is queriable. Operational dashboards, user-facing "where is my order" screens, and cross-workflow coordination all have somewhere to ask.

## Disadvantages

Four, opposite to choreography's advantages (source: raw/software-architecture-the-hard-parts/chapter-11-managing-distributed-workflows.md):

- **Responsiveness** — every step goes through the orchestrator, which is a potential throughput bottleneck.
- **Fault tolerance** — the orchestrator is a single point of failure; redundancy mitigates but adds complexity.
- **Scalability** — coordination points cap parallelism. Choreography achieves higher scale (notably in the `Time Travel Saga(sec)` and `Anthology Saga(aec)` patterns).
- **Service coupling** — higher coupling between orchestrator and domain components than in the choreographed alternative.

## When to use

Chapter 11's rubric (source: raw/software-architecture-the-hard-parts/chapter-11-managing-distributed-workflows.md):

- The workflow has **complex error / boundary conditions**, not just a happy path.
- **State tracking** is a first-order requirement — someone wants to know "where is the workflow".
- **Recoverability** matters — failed steps should be retried or resumed.
- **Deterministic control** is required and the throughput ceiling is acceptable.

As workflow complexity rises, the utility of an orchestrator rises proportionally. The book's Figure 11-14 makes this a direct curve: complex workflows need orchestration.

## When not to use

- The workflow is **simple and linear** — an orchestrator is overhead.
- **Extreme scale / responsiveness** are first-order and error paths are rare or simple — [[workflow-choreography]] wins.
- **Multiple teams** own participants and need to extend the workflow independently — choreography's pub/sub extensibility is a better fit.

## Relationship to sagas and the mediator topology

Workflow orchestration is the coordination shape underneath several specific patterns the wiki already covers:

- **[[saga|Orchestrated sagas]]** — when the workflow has transactional consistency constraints, an orchestrated workflow becomes an orchestrated saga. The orchestrator drives participants *and* owns compensation logic on failure. Chapter 12 of the book walks the four orchestrated saga patterns: [[epic-saga|Epic Saga(sao)]], [[fairy-tale-saga|Fairy Tale Saga(seo)]], [[fantasy-fiction-saga|Fantasy Fiction Saga(aao)]], and [[parallel-saga|Parallel Saga(aeo)]] — each combining orchestration with different values on the communication and consistency axes.
- **[[mediator-topology]]** — Richards and Ford's [[event-driven-architecture]] topology in which a central event mediator coordinates the workflow via commands. Mediator-topology EDA is workflow orchestration applied at the whole-architecture-style level.
- **[[orchestrated-request-based-pattern]]** — the [[distributed-transactions|distributed-transaction]] pattern from Chapter 9 that uses synchronous orchestrated calls with compensation.

All three share the same core mechanic: a neutral coordinator knows the steps and owns error handling. They differ in scope (saga level, architecture-style level, transaction pattern level) and in transactional semantics.

## Stateless orchestrators

Chapter 11 notes in passing that some implementations use **stateless orchestrators** for higher scale — the orchestrator drives sequencing but does not persist workflow state itself, delegating persistence to participants. This weakens the centralised-state-management advantage in exchange for horizontal scalability. The trade-off recapitulates the general stateless/stateful service choice.

## Relationship to the other coordination style

[[workflow-choreography]] is the peer style — no orchestrator, participants react to events and emit their own. Chapter 11 presents them as the two values on the **coordination** axis of [[dynamic-coupling]]. See [[distributed-workflow-patterns]] for the side-by-side trade-off rubric and for why real systems usually mix the two.

## Scope note: distinct from data-engineering orchestration

The wiki's existing [[orchestration]] page covers **data-engineering orchestration** — Airflow-style DAG schedulers that coordinate batch data jobs. Both use the word "orchestration" and both involve a central coordinator, but the scope is different:

- **Data-engineering orchestration** coordinates **jobs** (batch ETL tasks, model training runs) with DAG-shaped dependencies, scheduled cadence, and long-horizon scheduling.
- **Workflow orchestration (this page)** coordinates **services** participating in a single business workflow, typically per-request, with synchronous or asynchronous cross-service calls and explicit error recovery.

An orchestration engine like Airflow or Dagster can be used to implement either, but the architectural concern here is the cross-service coordination pattern, not the scheduling infrastructure. Chapter 11 uses "orchestration" in the cross-service-coordination sense throughout.

## Related pages

- [[workflow-choreography]]
- [[distributed-workflow-patterns]]
- [[semantic-coupling]]
- [[dynamic-coupling]]
- [[saga]]
- [[mediator-topology]]
- [[broker-topology]]
- [[event-driven-architecture]]
- [[microservices]]
- [[orchestrated-request-based-pattern]]
- [[orchestration-driven-soa]]
- [[orchestration]]
- [[software-architecture-the-hard-parts]]
- [[epic-saga]]
- [[fairy-tale-saga]]
- [[fantasy-fiction-saga]]
- [[parallel-saga]]
