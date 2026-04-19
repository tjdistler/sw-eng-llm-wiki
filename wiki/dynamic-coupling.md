# Dynamic Coupling

**Summary**: How [[architectural-quantum|architecture quanta]] **call one another at runtime** to form workflows — the runtime behaviour that no deployment diagram can show. In *Software Architecture: The Hard Parts*, dynamic coupling is a three-dimensional decision space: **communication** (synchronous / asynchronous) × **consistency** (atomic / eventual) × **coordination** (orchestrated / choreographed). These three axes are interlocking, not independent, and together they generate the pattern space Part II of the book walks through.

**Sources**: `raw/software-architecture-the-hard-parts/chapter-02-discerning-coupling-in-software-architecture.md`

**Last updated**: 2026-04-19

---

## Definition

> Dynamic coupling represents how quanta communicate at runtime, either synchronously or asynchronously. Thus, fitness functions for these characteristics must be continuous, typically utilizing monitors. (source: raw/software-architecture-the-hard-parts/chapter-02-discerning-coupling-in-software-architecture.md)

The core distinction in *The Hard Parts* (source: raw/software-architecture-the-hard-parts/chapter-02-discerning-coupling-in-software-architecture.md):

- **[[static-coupling]]** — how services are *wired together* (dependencies, contracts, topology). Visible on a deployment diagram. Measurable at build/deploy time.
- **Dynamic coupling** — how services *call one another at runtime* to satisfy a workflow. Invisible until load and failure expose it.

Two services can be statically decoupled (each deploys independently, each owns its data, neither imports the other's code) and still be tightly *dynamically* coupled (one synchronously calls the other on every request and blocks until it responds). The reverse also holds: components that share code can still interact asynchronously with loose contracts.

Because dynamic coupling is only visible under load, monitors and [[architecture-fitness-function|continuous fitness functions]] are the natural governance tool — static analysis can't see whether a call chain times out under pressure.

## The three dimensions

Chapter 2's pivotal contribution is reframing dynamic coupling as a *three-dimensional* decision space. Each runtime call has three interlocking forces, and architects cannot decide one in isolation — each pulls on the others (source: raw/software-architecture-the-hard-parts/chapter-02-discerning-coupling-in-software-architecture.md):

### 1. Communication — synchronous vs asynchronous

*What kind of connection synchronicity is used.*

- **Synchronous**: the caller blocks until the callee returns. Protocols: gRPC, HTTP/REST with blocking clients, direct method calls within a quantum. The caller and callee's operational characteristics (scalability, availability, performance) fuse for the duration of the call.
- **Asynchronous**: the caller posts a message (typically via a [[message-brokers|message queue]]) and continues working. If a response is required, the callee uses a reply queue to notify the caller later. Buffers absorb operational mismatches between the two sides.

See [[synchronous-microservices]] for the synchronous-default trade-offs and [[event-driven-architecture]] for the async style.

### 2. Consistency — atomic vs eventual

*Strictness of transactional integrity during the call.*

- **Atomic** — all-or-nothing transactions that require consistency during request processing. Expensive across service boundaries; discussed in Chapters 6, 9, 10, and 12 of the book.
- **Eventual** — different degrees of [[eventual-consistency]] on the other end of the spectrum. Participants converge over time rather than committing together.

The general advice in the book: *avoid cross-service atomic transactions wherever possible.* Transactionality — multiple services in a single all-or-nothing commit — is one of the hardest problems to model in distributed architectures (source: raw/software-architecture-the-hard-parts/chapter-02-discerning-coupling-in-software-architecture.md). See [[saga]] for the canonical replacement.

### 3. Coordination — orchestrated vs choreographed

*How the workflow's steps are conducted.*

- **Orchestrated** — a central [[orchestration-driven-soa|orchestrator / mediator]] knows the workflow and directs each participant.
- **Choreographed** — no central coordinator; participants react to events and emit their own, and the workflow emerges from the event chain.

Simple workflows (one service replying to one request) don't need dedicated coordination. As complexity grows, the need for coordination grows with it. Chapter 11 of the book covers orchestration vs choreography in depth — see [[distributed-workflow-patterns]] for the side-by-side rubric, [[workflow-orchestration]] and [[workflow-choreography]] for the two values at the workflow-implementation grain, and [[semantic-coupling]] for the domain-level coupling force the chapter introduces. See [[event-driven-architecture]]'s mediator/broker topology discussion for the structural reconciliation with Richards and Ford's *Fundamentals* treatment, and [[saga]] for Newman's orchestrated/choreographed saga framing.

## The dimensions interact

The three axes are not independent. Ford, Richards, Sadalage, and Dehghani are explicit: **each option has a gravitational effect on the others** (source: raw/software-architecture-the-hard-parts/chapter-02-discerning-coupling-in-software-architecture.md):

- Transactionality is **easier in synchronous architectures with mediation** — a single orchestrator holding the transaction scope can drive all participants to commit or roll back.
- Higher levels of **scale** are possible with **eventually consistent asynchronous choreographed systems** — no orchestrator bottleneck, no synchronous blocking, no cross-service atomicity requirement.

The three dimensions together form a cube: 2 × 2 × 2 = 8 possible combinations. Chapter 2's Table 2-1 catalogues these eight as a framework for identifying fundamental distributed-workflow pattern names; the rest of the book (especially Chapters 11-13) walks through them.

[[saga|Chapter 12]] names each of the eight corners of the cube with a mnemonic pattern name plus a superscript encoding the three axes in alphabetical order: [[epic-saga|Epic Saga(sao)]], [[phone-tag-saga|Phone Tag(sac)]], [[fairy-tale-saga|Fairy Tale(seo)]], [[time-travel-saga|Time Travel(sec)]], [[fantasy-fiction-saga|Fantasy Fiction(aao)]], [[horror-story-saga|Horror Story(aac)]], [[parallel-saga|Parallel(aeo)]], [[anthology-saga|Anthology(aec)]]. Chapter 12 is the canonical worked example of how the three-axis dynamic-coupling model produces a design space architects can actually reason about.

## Why three dimensions matter

The multidimensional framing solves a practical problem: architects repeatedly struggle with distributed-architecture decisions because the forces are entangled. Debating "should we use synchronous or asynchronous?" in isolation leaves the consistency and coordination questions implicit — and they're load-bearing.

The three-dimensional lens forces each decision to be made explicitly and alongside the other two. It is also what makes *trade-off analysis* tractable at the workflow level: once you name the three positions, you can enumerate the consequences on each axis and pick the least-worst combination for the scenario at hand. This is the method [[software-architecture-the-hard-parts|the book]] teaches generalised down to the workflow-call grain.

## Direction and strength

Dynamic coupling also has a **direction**: when service A calls service B, the coupling runs A → B. A depends on B at runtime; B does not depend on A (though B's failure cascades back to A through the call's error path). **Strength** varies by the combination of the three dimensions — synchronous + atomic + orchestrated is the strongest possible dynamic coupling (A's operational characteristics fuse with B's for the duration of the call, A cannot commit without B, and the orchestrator sequences them). Asynchronous + eventual + choreographed is the weakest (A emits an event, B may or may not react, neither knows about the other's transactional state).

Architects read dynamic-coupling diagrams with the directional arrow *and* the axis position on each dimension in mind. Two arrows between the same pair of services can represent wildly different runtime couplings.

## Dynamic coupling and the architectural quantum

Chapter 2 tightens the [[architectural-quantum]] definition using dynamic coupling:

> An architecture quantum is an independently deployable artifact with high functional cohesion, high static coupling, and **synchronous dynamic coupling**. (source: raw/software-architecture-the-hard-parts/chapter-02-discerning-coupling-in-software-architecture.md)

Synchronous dynamic coupling is what fuses two otherwise-separate services into the same quantum. A microservice that synchronously calls another microservice on every request has — for the duration of those calls — merged its operational characteristics with the callee's. Architects who want genuinely independent quanta (each with its own scalability, availability, security profile) must avoid synchronous dynamic coupling across quantum boundaries. This is the Chapter 7 *Fundamentals* point restated with the fuller static/dynamic vocabulary: inside a quantum, synchronous calls are fine; across quanta, prefer asynchronous.

## The reuse-pattern lens

Chapter 8's [[shared-service-pattern]] is the paradigmatic example of deliberately *introducing* dynamic coupling between services for the sake of reuse (source: raw/software-architecture-the-hard-parts/chapter-08-reuse-patterns.md). Every operational trade-off on that page — performance (network + security latency), scalability (the shared service must scale with callers), fault tolerance (unavailability cascades) — is a dynamic-coupling trade-off. Versioning (API endpoint versioning, multi-protocol coordination) is a dynamic-coupling governance problem; in a [[shared-library-pattern|shared library]] the equivalent concern is handled at compile time.

The chapter's framing makes explicit what the static/dynamic split implies: **moving code from a library to a service converts static coupling into dynamic coupling**, and the operational characteristics of every consumer now depend on the shared service at runtime. This is also why the [[sidecar-pattern]] / [[service-mesh]] option is structurally different from the other reuse patterns — the sidecar doesn't produce cross-service dynamic coupling at all; it bundles orthogonal behaviour into each pod's local deployment unit.

## Relation to Page-Jones dynamic connascence

Page-Jones's original 1996 [[connascence]] framework named four forms of dynamic connascence — execution, timing, values, identity — all visible only at runtime. The book's dynamic coupling is the *architectural-scale* counterpart: it asks the same question (what couplings exist only at runtime?) at the granularity of service-to-service calls rather than class-to-class method invocations. The three dimensions above sit above Page-Jones's four in the layered framework — a cross-service synchronous call is architecturally synchronous *and* contains dynamic connascence of execution and timing.

## Part II of the book

Chapter 2 is the introduction; the rest of Part II ("Putting Things Back Together") decomposes each of the three dimensions in turn, then re-entangles them:

- Communication — synchronous vs asynchronous in depth.
- Consistency — atomic transactions, eventual consistency, [[saga|sagas]].
- Coordination — [[orchestration-driven-soa|orchestration]] vs choreography.
- Contract design (Chapter 13).
- Dynamic-coupling trade-offs across the 8-combination matrix (Chapter 12).

The individual chapters exist because each dimension is already hard; understanding the interactions requires understanding each axis first.

## Related pages

- [[static-coupling]]
- [[architectural-quantum]]
- [[coupling]]
- [[connascence]]
- [[synchronous-microservices]]
- [[event-driven-architecture]]
- [[saga]]
- [[eventual-consistency]]
- [[message-brokers]]
- [[software-architecture-the-hard-parts]]
- [[architecture-fitness-function]]
- [[choreography]]
- [[reuse-patterns]]
- [[shared-service-pattern]]
- [[distributed-workflow-patterns]]
- [[workflow-orchestration]]
- [[workflow-choreography]]
- [[semantic-coupling]]
- [[epic-saga]]
- [[phone-tag-saga]]
- [[fairy-tale-saga]]
- [[time-travel-saga]]
- [[fantasy-fiction-saga]]
- [[horror-story-saga]]
- [[parallel-saga]]
- [[anthology-saga]]
