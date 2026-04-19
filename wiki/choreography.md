# Choreography

**Summary**: A coordination style for distributed workflows in which **no central coordinator** exists — participants react to events and emit their own, and the workflow emerges from the event chain. One of the two values on the **coordination** dimension of [[dynamic-coupling]] in *Software Architecture: The Hard Parts*, alongside orchestration. Matches the **[[broker-topology]]** of [[event-driven-architecture]] and the **choreographed saga** pattern from Newman.

**Sources**: `raw/software-architecture-the-hard-parts/chapter-02-discerning-coupling-in-software-architecture.md`, `raw/software-architecture-the-hard-parts/chapter-11-managing-distributed-workflows.md`

**Last updated**: 2026-04-19

---

## Definition

Chapter 2 of *The Hard Parts* names **coordination** as one of three dimensions of [[dynamic-coupling]]. The two values are (source: raw/software-architecture-the-hard-parts/chapter-02-discerning-coupling-in-software-architecture.md):

- **Orchestration** — a central orchestrator knows the workflow and directs each participant.
- **Choreography** — no central coordinator; participants react to events and emit their own.

> The two common generic patterns for microservices are orchestration and choreography, which we describe in Chapter 11. Simple workflows — a single service replying to a request — don't require special consideration from this dimension. However, as the complexity of the workflow grows, the greater the need for coordination. (source: raw/software-architecture-the-hard-parts/chapter-02-discerning-coupling-in-software-architecture.md)

Chapter 11 of the book covers choreography in depth at the **workflow-implementation grain**; [[workflow-choreography]] is the narrower page that carries the Chapter 11 worked examples and the workflow-state-management catalogue (Front Controller, stateless choreography, [[stamp-coupling]]). This page is the concept-level hub across all the book's treatments and the existing wiki vocabularies it connects to.

## The defining property: no one is in charge

In a choreographed workflow, participants don't know the workflow — they know only what they do, what events they listen for, and what events they emit. The workflow itself is **implicit in the event chain**. No component has the whole picture.

This creates the central trade-off of the style:

- **Advantage** — extreme loose coupling. New participants can be added that listen to existing events without modifying any producer. Services have no knowledge of each other, just of events. Ownership decentralises cleanly along team lines.
- **Disadvantage** — the workflow is nowhere. There's no single place to see "what happens when an order arrives"; you have to read the code of every service that reacts to `OrderPlaced` to reconstruct the flow. Error handling has no home — no-one is responsible for compensating a failed step because no-one is running the step on anyone's behalf.

## Relationship to existing wiki coverage

Choreography is already present in the wiki under other vocabularies; this page is the concept-level hub.

- **[[broker-topology]]** — Richards and Ford's name for the top-level topology of an event-driven architecture that has no central mediator. The broker topology *is* choreography at the architecture-style level.
- **[[event-driven-architecture]]** — the broker/mediator subsection contains Richards and Ford's most extensive treatment. See the "Terminology reconciliation" subsection there for the alignment between mediator/broker and orchestration/choreography.
- **[[saga]]** — Newman's framing distinguishes orchestrated sagas (a saga orchestrator drives each participant) from choreographed sagas (participants react to events without a central driver). The choreographed saga is choreography applied to a distributed transaction workflow.
- **[[event-driven-microservices]]** — a natural substrate for choreography. Bellemare's default style assumes services couple through [[event-streams]] rather than API calls, which is choreography by construction.

The book's Chapter 11 treatment elaborates the pattern for microservices specifically; this wiki cross-links those pages rather than duplicating the content here.

## The three-dimensional position

Using Chapter 2's three axes of [[dynamic-coupling]], a typical choreographed workflow sits at:

- **Communication** — asynchronous (events, not synchronous calls).
- **Consistency** — eventual (no orchestrator to drive atomic commits).
- **Coordination** — choreographed.

This corner of the cube is the *weakest* dynamic coupling possible — which is exactly why it offers the highest levels of scale and elasticity, and also why it demands the most discipline around workflow observability, error handling, and data consistency.

## When to use

Choreography fits when (drawn from the cross-referenced wiki pages and Chapter 2's framing):

- The workflow is **reactive** and the set of reactors may change over time.
- **Scale and elasticity** are first-order characteristics.
- Participants can tolerate [[eventual-consistency]].
- Teams want **independent ownership** without a cross-team coordinator.
- New event consumers need to be added without modifying producers — the event feed is the extensibility point.

## When not to use

- The workflow requires **tight control** or a single deterministic path.
- **Atomic consistency** is required across participants.
- **Debuggability** matters disproportionately — synchronous orchestrated call chains are easier to trace.
- The team is new to asynchronous programming and can't yet build the observability and compensation machinery a choreographed system needs.

In practice, many real systems mix the two: orchestration for a central workflow backbone, choreography at the leaves where extensibility matters. Chapter 2 of *The Hard Parts* treats this as a trade-off to be analysed per workflow, not a style-level commitment.

## Chapter 11's framing — every error scenario adds a link

The book's Chapter 11 adds an operational observation worth preserving here. In an orchestrated workflow, **all error-scenario communication already exists** because every participant already talks to the orchestrator. In a choreographed workflow, **each new error scenario tends to introduce new inter-service links** that didn't exist on the happy path (the "one new communication link" for a payment failure, the multi-broadcast compensation for a back-order). This is why choreography's complexity grows faster than orchestration's as error cases multiply, and why Chapter 11's choice rubric weights error-scenario complexity heavily (source: raw/software-architecture-the-hard-parts/chapter-11-managing-distributed-workflows.md). See [[distributed-workflow-patterns]] for the full side-by-side matrix and [[semantic-coupling]] for the concept Chapter 11 uses to frame *which* couplings the architect is introducing versus which are inherent to the domain.

## Related pages

- [[dynamic-coupling]]
- [[static-coupling]]
- [[broker-topology]]
- [[mediator-topology]]
- [[event-driven-architecture]]
- [[saga]]
- [[event-driven-microservices]]
- [[architectural-quantum]]
- [[eventual-consistency]]
- [[software-architecture-the-hard-parts]]
- [[coupling]]
- [[connascence]]
- [[workflow-choreography]]
- [[workflow-orchestration]]
- [[distributed-workflow-patterns]]
- [[semantic-coupling]]
- [[stamp-coupling]]
