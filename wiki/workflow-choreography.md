# Workflow Choreography

**Summary**: The peer counterpart to [[workflow-orchestration]] — a coordination style for distributed workflows where **no central coordinator exists**. Services communicate peer-to-peer via events or commands, each reacting to upstream signals and emitting its own. Chapter 11 of *Software Architecture: The Hard Parts* analyses choreography at the **workflow-implementation grain** — what works, what doesn't, and how to manage workflow state when nobody owns it. This page is the Chapter 11 workflow-grain treatment; see [[choreography]] for the concept-level hub across all coverage in the wiki.

**Sources**: `raw/software-architecture-the-hard-parts/chapter-11-managing-distributed-workflows.md`

**Last updated**: 2026-04-19

---

## Definition

> Instead [of a conductor], each service participates with the others, similar to dance partners. It isn't an ad hoc performance — the moves were planned beforehand by the choreographer/architect but executed without a central coordinator. (source: raw/software-architecture-the-hard-parts/chapter-11-managing-distributed-workflows.md)

The workflow itself is **implicit in the event chain**. Each service knows only which events or messages it listens for and what it emits in response. No component has the whole workflow; no component is "the boss."

## Worked example — Penultimate Electronics order

The same order-placement workflow the book's Chapter 11 uses to illustrate [[workflow-orchestration]], reshaped as choreography (source: raw/software-architecture-the-hard-parts/chapter-11-managing-distributed-workflows.md):

1. Request hits **Order Placement Service** — records the order, sends a message.
2. **Payment Service** receives the message — applies payment, emits its own message.
3. **Fulfillment Service** receives the payment message — plans delivery, emits a message.
4. **Email Service** receives the fulfillment message — notifies the customer.

At first glance this looks *simpler* than the orchestrated version: fewer components (no orchestrator), a simple chain of commands. The book is blunt that this surface-level simplicity is misleading — difficulties lie in **boundary and error conditions**, not the happy path.

### Error scenario 1: payment rejected

Payment Service, upon failure, must now send messages in **two** new directions: to Email Service (notify customer) *and* back to Order Placement Service (update order status). One extra communication link was added to express the error flow.

### Error scenario 2: item back-ordered

This is where choreography's cost shows up. Many services have already committed local state by the time Fulfillment discovers the out-of-stock condition. Each must issue **compensating messages** to undo its part. Fulfillment emits broadcast messages subscribed to by Email, Payment, *and* Order Placement services. This is the `Anthology Saga(aec)` pattern — asynchronous, eventual-consistency, choreographed (source: raw/software-architecture-the-hard-parts/chapter-11-managing-distributed-workflows.md).

> Every error scenario forces domain services to interact with each other, adding communication links that weren't necessary for the happy path. (source: raw/software-architecture-the-hard-parts/chapter-11-managing-distributed-workflows.md)

This is the structural difference from [[workflow-orchestration]]. Orchestration's error links are already drawn — the orchestrator was already talking to everyone. Choreography's error links are new. As error-scenario count grows, so does the communication-link count.

## Advantages

Chapter 11's list (source: raw/software-architecture-the-hard-parts/chapter-11-managing-distributed-workflows.md):

- **Responsiveness** — fewer choke points, more opportunities for parallelism.
- **Scalability** — no orchestrator-shaped coordination point; each service scales independently.
- **Fault tolerance** — no single coordinator to fail; multiple instances easily deployed.
- **Service decoupling** — no coordinator means less structural coupling between participants.

## Disadvantages

Opposite numbers to orchestration's advantages (source: raw/software-architecture-the-hard-parts/chapter-11-managing-distributed-workflows.md):

- **Distributed workflow** — no workflow owner makes error management and boundary conditions harder.
- **State management** — no centralized state holder; knowing "which workflows are in flight and at which step" is non-trivial.
- **Error handling** — harder without an orchestrator, because each domain service must carry workflow knowledge about what to do on failure.
- **Recoverability** — no central driver to retry or resume.

## Workflow state management

Somebody has to track which workflows are in flight, which steps have run, and what the current status is. Orchestration gives this job to the orchestrator. Choreography has **no obvious owner**. Chapter 11 names three common solutions (source: raw/software-architecture-the-hard-parts/chapter-11-managing-distributed-workflows.md):

### 1. Front Controller pattern

The first service in the chain of responsibility (Order Placement Service in the example) owns workflow state **in addition to** its domain behaviour. Downstream services communicate back to it to update order state. This pattern:

- Simplifies the workflow's state ownership (one place to ask).
- **Increases communication overhead** — every state-updating service now has an extra call back to the front controller.
- **Complicates the front controller** — it now carries both domain logic and workflow logic.

Chapter 11's Figure 11-13 is the reference diagram.

### 2. Stateless choreography

**No transient workflow state at all.** The current state is rebuilt by querying each participant in real time. This:

- Is the maximally decoupled form — nobody carries workflow state.
- **Trades performance for control** — reconstructing state is chatty. A customer asking "where is my order?" triggers queries to every service in the chain.
- Scales well on write paths, poorly on query paths.

### 3. Stamp coupling in the message contract

Workflow state rides along in the **message itself**. Each service updates its portion of the shared state and passes the augmented message to the next. See [[stamp-coupling]] for the general concept and Chapter 13's "Stamp Coupling for Workflow Management" discussion for the trade-offs.

- Partial solution — still no single place to query, but any message carries complete history of the workflow so far.
- Keeps participants decoupled from each other while still propagating state.
- Cost: larger messages, coupling on the shared contract shape.

## When to use

Chapter 11's rubric (source: raw/software-architecture-the-hard-parts/chapter-11-managing-distributed-workflows.md):

- **Responsiveness and scalability** are first-order characteristics.
- Error scenarios are **simple, infrequent, or absent**.
- The workflow is mostly linear — not many conditional branches or compensations.
- Multiple teams own different participants and value independent evolution.

The book's phrase: *the sweet spot for choreography lies with workflows that need responsiveness and scalability, and either don't have complex error scenarios or they are infrequent.*

## When not to use

- **Complex error / boundary conditions** dominate the workflow. Each error scenario adds new communication links; choreography degrades faster than orchestration as error complexity grows.
- **Operational visibility** of workflow state is a hard requirement.
- **Strong recoverability** is needed — no central driver means no natural retry home.
- The workflow is a [[saga]] with many participants and rich compensation requirements — orchestrated sagas are structurally easier at that complexity level.

Chapter 11 specifically calls out the `Horror Story(aac)` pattern as what happens when choreography is forced onto workflows with too many other constraints (atomic consistency + async + choreography).

## Relationship to the broker topology and choreographed sagas

Workflow choreography maps onto several specific patterns already in the wiki:

- **[[broker-topology]]** — Richards and Ford's whole-architecture-style counterpart; a broker-topology EDA is workflow choreography applied at the style level.
- **[[saga|Choreographed sagas]]** — when the workflow requires compensation semantics, a choreographed workflow becomes a choreographed saga. Chapter 12's choreographed variants are [[phone-tag-saga|Phone Tag Saga(sac)]], [[time-travel-saga|Time Travel Saga(sec)]], [[horror-story-saga|Horror Story(aac)]] (cautionary), and [[anthology-saga|Anthology Saga(aec)]].
- **[[event-based-consistency-pattern]]** — the eventual-consistency [[distributed-transactions|data-sync]] pattern from Chapter 9; a choreographed-workflow shape for transactional consistency.

## Relationship to the hub page

The wiki's [[choreography]] page is the concept-level hub — it reconciles this pattern with Newman's sagas, Richards and Ford's broker topology, and the coordination axis of [[dynamic-coupling]]. This page is the narrower **Chapter 11 workflow-grain treatment**: worked examples, state-management tactics, and the trade-off rubric at the single-workflow grain.

## Related pages

- [[choreography]]
- [[workflow-orchestration]]
- [[distributed-workflow-patterns]]
- [[semantic-coupling]]
- [[dynamic-coupling]]
- [[saga]]
- [[broker-topology]]
- [[mediator-topology]]
- [[event-driven-architecture]]
- [[event-based-consistency-pattern]]
- [[microservices]]
- [[stamp-coupling]]
- [[software-architecture-the-hard-parts]]
- [[phone-tag-saga]]
- [[time-travel-saga]]
- [[horror-story-saga]]
- [[anthology-saga]]
