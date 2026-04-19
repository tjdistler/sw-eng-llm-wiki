# Distributed Workflow Patterns

**Summary**: The side-by-side hub for the two **coordination patterns** named in Chapter 11 of *Software Architecture: The Hard Parts* — [[workflow-orchestration]] and [[workflow-choreography]]. This page holds the trade-off rubric that decides between them at the single-workflow grain: complexity of error scenarios, need for state tracking, scale requirements, and how much [[semantic-coupling]] the domain already imposes. Chapter 11 is the coordination axis of [[dynamic-coupling]] viewed at the workflow implementation level, and this page is the cross-reference.

**Sources**: `raw/software-architecture-the-hard-parts/chapter-11-managing-distributed-workflows.md`

**Last updated**: 2026-04-19

---

## The two patterns

Chapter 11 names exactly two fundamental coordination patterns in distributed architectures (source: raw/software-architecture-the-hard-parts/chapter-11-managing-distributed-workflows.md):

- **[[workflow-orchestration|Orchestration]]** — a neutral **orchestrator** (mediator) component owns workflow state, sequences participants, and handles errors. Star-ish topology.
- **[[workflow-choreography|Choreography]]** — no central coordinator. Participants communicate peer-to-peer (events, commands) and the workflow is implicit in the chain.

The whole of Chapter 11 is the trade-off between these two; Chapter 12 then refines the trade-off under consistency constraints to produce the eight-pattern saga catalogue.

## The trade-off matrix

Each row is opposite-valued — the two patterns trade characteristics cleanly (source: raw/software-architecture-the-hard-parts/chapter-11-managing-distributed-workflows.md):

| Concern | Orchestration | Choreography |
|---|---|---|
| Workflow state | Centralized in orchestrator | Distributed / must choose a pattern (front controller, stateless, stamp coupling) |
| Error handling | Has a natural home | Must be woven into every participant |
| Recoverability | Native | Difficult — no central retry driver |
| Boundary conditions | Existing links handle them | Each error case adds new links |
| Responsiveness | Lower — all calls through orchestrator | Higher — no choke point |
| Scalability | Capped by orchestrator | Higher ceiling, more parallelism |
| Fault tolerance | Orchestrator is SPOF (unless redundant) | No single coordinator to fail |
| Service coupling | Higher — to orchestrator | Lower — decoupled participants |

## The choice rubric

Four forces determine the right pattern for a given workflow (source: raw/software-architecture-the-hard-parts/chapter-11-managing-distributed-workflows.md):

### 1. How complex are the error scenarios?

This is the dominant force. Every choreographed error scenario typically **adds new inter-service communication links** that the happy path did not need. Orchestrated error scenarios reuse links that the orchestrator already has. As error-scenario count grows, choreography's complexity grows faster than orchestration's.

### 2. How much state needs to be tracked?

Orchestration gives state a home. Choreography has three options ([[workflow-choreography#workflow-state-management|front controller, stateless, stamp coupling]]) each with its own trade-off. If the workflow is long-lived, if operational dashboards need real-time status, or if users ask "where is my order?", orchestration is structurally easier.

### 3. What are the scale requirements?

Choreography's sweet spot is scale + responsiveness — no coordinator bottleneck, no serialised step transitions. The book's cited examples are the `Time Travel Saga(sec)` and `Anthology Saga(aec)` patterns, both choreographed precisely for their scale characteristics.

### 4. How much semantic coupling does the domain already impose?

High [[semantic-coupling]] — many domain relationships between participants, rich cross-references, mandatory sequencing — makes orchestration's centralised model a natural fit because the domain already demands something that looks like an orchestrator. Low semantic coupling (a simple linear chain with independent steps) gives choreography room to stay near the [[semantic-coupling|semantic floor]].

## Workflow complexity vs orchestration utility

Chapter 11's Figure 11-14 shows a direct relationship: as workflow complexity rises, the utility of an orchestrator rises proportionally. The practical consequence: architects should default to orchestration above a complexity threshold and choreography below it, not treat either as a style-level commitment. Many real systems **mix the two** — orchestration for the complex transactional backbone, choreography at the leaves where extensibility matters.

## Which patterns sit where

The book's eight saga patterns are the distributed-workflow patterns under explicit consistency constraints; Chapter 12 catalogues them. The coordination axis of those patterns uses this chapter's orchestration/choreography distinction:

### Orchestrated patterns

- [[epic-saga|Epic Saga(sao)]]
- [[fairy-tale-saga|Fairy Tale Saga(seo)]]
- [[fantasy-fiction-saga|Fantasy Fiction Saga(aao)]]
- [[parallel-saga|Parallel Saga(aeo)]]

See [[saga]] and [[orchestrated-request-based-pattern]].

### Choreographed patterns

- [[phone-tag-saga|Phone Tag Saga(sac)]]
- [[time-travel-saga|Time Travel Saga(sec)]]
- [[anthology-saga|Anthology Saga(aec)]]

See [[saga]] and [[event-based-consistency-pattern]]. The [[horror-story-saga|Horror Story(aac)]] is Chapter 11's named cautionary pattern — asynchronous + atomic consistency + choreographed — which combines forces that fight each other.

## Relation to architecture-style topologies

Chapter 11 works at the **workflow-implementation grain**: one workflow inside a larger architecture. Richards and Ford's [[event-driven-architecture]] chapter makes the *same* distinction at the **whole-architecture-style grain**:

- [[mediator-topology]] = whole-architecture orchestration
- [[broker-topology]] = whole-architecture choreography

A system can choose orchestration at the style level (mediator EDA) and still have individual workflows that choreograph inside sub-domains. The forces are fractal: the same rubric applies at both grains.

## Sysops Squad example

Chapter 11 closes by modeling the Sysops Squad ticket-assignment workflow both ways — once as choreography (Figure 11-15) and once as orchestration (Figure 11-16). The book works through the trade-off iteratively (Tables 11-6, 11-7, 11-8) and shows that either coordination style can implement the workflow. The choice comes down to which set of trade-offs the team prefers to accept, which is Chapter 11's intended pedagogical point: **these are genuinely trade-offs, not a right answer hiding behind surface complexity**.

## Foreshadowing Chapter 12

Chapter 11 is the coordination axis in isolation. Chapter 12 re-entangles it with the **consistency** axis of [[dynamic-coupling]] to produce the eight-pattern saga catalogue — each pattern is a specific combination of (sync/async, atomic/eventual, orchestrated/choreographed). The [[saga]] page summarises those patterns; this page is the single-axis rubric underneath them.

## Related pages

- [[workflow-orchestration]]
- [[workflow-choreography]]
- [[semantic-coupling]]
- [[dynamic-coupling]]
- [[saga]]
- [[mediator-topology]]
- [[broker-topology]]
- [[event-driven-architecture]]
- [[choreography]]
- [[orchestrated-request-based-pattern]]
- [[event-based-consistency-pattern]]
- [[microservices]]
- [[software-architecture-the-hard-parts]]
- [[epic-saga]]
- [[phone-tag-saga]]
- [[fairy-tale-saga]]
- [[time-travel-saga]]
- [[fantasy-fiction-saga]]
- [[horror-story-saga]]
- [[parallel-saga]]
- [[anthology-saga]]
