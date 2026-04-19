# Saga

**Summary**: An algorithm for coordinating a sequence of state changes across multiple services without holding distributed locks. The original 1987 paper by Hector Garcia-Molina and Kenneth Salem proposed sagas to handle long-lived transactions; modern microservice architectures use them as the standard alternative to [[two-phase-commit|2PC]] / [[distributed-transactions]].

**Sources**: `raw/monolith-to-microservices/chapter-04-decomposing-the-database.md`, `raw/fundamentals-of-software-architecture/chapter-14-event-driven-architecture-style.md`, `raw/fundamentals-of-software-architecture/chapter-17-microservices-architecture.md`, `raw/building-event-driven-microservices/chapter-08-building-workflows-with-microservices.md`, `raw/software-architecture-the-hard-parts/chapter-01-what-happens-when-there-are-no-best-practices.md`, `raw/software-architecture-the-hard-parts/chapter-09-data-ownership-and-distributed-transactions.md`, `raw/software-architecture-the-hard-parts/chapter-11-managing-distributed-workflows.md`, `raw/software-architecture-the-hard-parts/chapter-12-transactional-sagas.md`

**Last updated**: 2026-04-19
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

## The same axis at the architecture-style level — Richards & Ford's mediator/broker

Richards and Ford's Chapter 14 on [[event-driven-architecture]] names the same orchestration/choreography distinction — but at a **different level of the architecture**. Where Newman treats orchestration and choreography as **saga implementation choices inside a microservices architecture**, Richards and Ford treat the same shapes as the **two canonical topologies of an entire event-driven architecture style**:

| Newman (M2M Ch 4) | Richards & Ford (FoSA Ch 14) | What it is |
|---|---|---|
| **Orchestrated saga** | **[[mediator-topology|Mediator topology]]** | Central coordinator knows the workflow, issues commands to participants, owns error handling and recovery |
| **Choreographed saga** | **[[broker-topology|Broker topology]]** | No central coordinator; participants react to events and emit their own; workflow is implicit in the event chain |

The trade-off lists match closely:

- Orchestration/mediator buys **explicit workflow, error handling with a home, recoverability, state visibility** at the cost of **centralisation, domain coupling in the coordinator, anaemic-participant risk, coordinator-as-bottleneck**.
- Choreography/broker buys **loose coupling, extensibility, independent team ownership, higher throughput** at the cost of **implicit workflow, distributed saga state, weaker error handling, no recoverability**.

Two differences in emphasis worth noting:

1. **Scope.** A saga is a single business process. An event-driven architecture is a whole system. Newman's orchestrator coordinates one saga; Richards and Ford's mediator coordinates every flow of a whole domain. Federated mediators (one per domain) are the structural equivalent of Newman's "different orchestrators for different flows" mitigation for coordinator anaemia.
2. **Event vs command vocabulary.** Richards and Ford load-bear the distinction: broker-topology messages are **past-tense facts** (events), mediator-topology messages are **imperative commands**. Newman's saga chapter does not make this split as explicitly, but the mechanics line up — choreographed sagas pub/sub events, orchestrated sagas send commands.

Practical consequence: a [[microservices]] architecture that uses [[event-driven-architecture]] as its inter-service substrate is **choosing the broker topology** whether it frames it that way or not. Choreographed sagas running on that architecture are the natural saga pattern; orchestrated sagas sit awkwardly inside it and typically need their own mediator infrastructure. Conversely, a system built around a central workflow mediator has effectively chosen the mediator topology and will find choreographed sagas fighting the architecture.

## Richards & Ford: "fix granularity, not transactions"

Chapter 17 of *Fundamentals of Software Architecture* treats saga as the escape hatch, not the standard tool. Richards and Ford's advice is deliberately blunt: *"The best advice for architects who want to do transactions across services is: don't! Fix the granularity components instead."* And later: *"Don't do transactions in microservices — fix granularity instead!"* (source: chapter-17-microservices-architecture.md).

The reasoning: building transactions across service boundaries violates the core decoupling principle of [[microservices|microservices architecture]] and creates the worst kind of dynamic [[connascence]] — connascence of value — across the boundary. When architects find they need a saga, the more common cause is that the [[service-granularity|granularity was wrong]]: entities that must cooperate in a transaction probably belonged in the same service to begin with.

Chapter 17 does accept exceptions. When two services legitimately need different architecture characteristics but still must coordinate transactionally, the saga pattern is the recognised pattern, with the caveat: *"the best advice for architects is to use the saga pattern sparingly. A few transactions across services is sometimes necessary; if it's the dominant feature of the architecture, mistakes were made!"* (source: chapter-17-microservices-architecture.md).

Chapter 17 also names the two concrete implementations of the compensating-transaction framework that sit under any orchestrated saga:

1. **Pending-state coordination** — each mediator request leaves its target in a pending state until overall saga success is confirmed. Operationally simpler, but becomes complex when async requests must be juggled or new requests arrive that depend on pending state. Heavy network coordination traffic.
2. **Explicit do-and-undo pairs** — each potentially transactional operation has a paired undo operation. Less coordination during the happy path, but the undo operations are usually significantly more complex than the do operations, more than doubling the design, implementation, and debugging work.

Both match Newman's backward-vs-forward-recovery framing above; Richards and Ford's contribution is flagging the design-cost asymmetry of the undo-pair style — the undo is typically *much* harder than the do, and the complexity multiplier should be part of the saga-vs-re-draw-the-boundary decision.

## Bellemare's EDM framing

Bellemare's Chapter 8 treats sagas as the transactional special case of [[workflows-in-edm|EDM workflows]]. The top-level framing echoes Newman and Richards & Ford, but two EDM-specific observations are worth pulling out (source: chapter-08-building-workflows-with-microservices.md):

### Idempotence is load-bearing for both actions

Bellemare emphasizes that both the forward action and the reversing action of each participant must be **idempotent**. This is a stronger statement than the 1987 paper's requirement — in an EDM context, transient failures cause events to be replayed, and a non-idempotent reversal that fires twice can leave the system in a worse state than the original failure. See [[idempotence]] and [[effectively-once-processing]].

### The single-writer asymmetry in choreographed sagas

A choreographed saga has a structural asymmetry Bellemare flags clearly: successful transactions finalize in the *last* service's output stream, but aborted transactions finalize in the *first* service's output stream (since the first service is the one that decides what to do with the failed result). A consumer that wants the complete picture has to listen to both streams. This is consistent with the [[single-writer-principle]] but makes end-to-end monitoring harder than in an orchestrated saga, where the single orchestrator can emit both success and failure results to one output stream (source: chapter-08-building-workflows-with-microservices.md).

### Orchestrated sagas admit more signals

Because the orchestrator materializes workflow state, it can act on signals beyond success/failure from its workers — **timeouts** (how long has this transaction been in flight?) and **human inputs** (cancellation via a REST API). A choreographed saga has no natural home for either. Orchestrated sagas are therefore the natural choice when workflows may involve manual approvals, interrupts, or timeout-based abort policies (source: chapter-08-building-workflows-with-microservices.md).

### Compensation vs strict rollback

Bellemare also names a third option that sits alongside both saga styles: the **[[compensation-workflow]]**. Instead of reversing a failed transaction, complete what can be completed and remediate the rest via a business-level policy (ticketing overbooking, inventory shortfall). This is the operational-pragmatism escape hatch when neither choreographed nor orchestrated strict rollback is appropriate.

## Hard Parts Ch 9: saga vocabulary is introduced before the full treatment

Chapter 9 of *The Hard Parts* introduces the **vocabulary** the book's saga chapter (Chapter 12) depends on — without pre-emptively covering the full saga catalogue. The chapter's contribution:

- Names **[[compensating-update|compensating updates]]** as the fundamental building block of sagas (source: raw/software-architecture-the-hard-parts/chapter-09-data-ownership-and-distributed-transactions.md).
- Introduces the **[[orchestrated-request-based-pattern]]** as a synchronous orchestrated-saga shape that performs compensation on partial failure.
- Introduces the **[[event-based-consistency-pattern]]** as the choreographed-saga shape — services publishing/subscribing to events and applying compensations in reverse.
- Names the nastiest saga failure mode — **compensation of compensation fails** — and observes that human intervention is often the only realistic answer.

Chapter 12's deeper treatment then generalises these shapes into the eight-pattern saga catalogue (characterised by coupling, communication style, and consistency). Chapter 9's job is to make sure the [[data-ownership]] and [[distributed-transactions]] discussion uses saga vocabulary correctly once it arrives.

## Hard Parts Ch 11: sagas are the consistency-flavoured instance of distributed-workflow coordination

Chapter 11 of *The Hard Parts* ([[distributed-workflow-patterns]]) is the book's treatment of coordination at the workflow-implementation grain — [[workflow-orchestration]] vs [[workflow-choreography]]. Chapter 12 then adds consistency constraints to that axis to produce the eight saga patterns. Seen this way, sagas are simply the **transactional flavour** of distributed-workflow patterns: take Chapter 11's orchestration/choreography choice and overlay Chapter 2's atomic/eventual consistency axis (source: raw/software-architecture-the-hard-parts/chapter-11-managing-distributed-workflows.md).

The Chapter 11 rubric for choosing orchestration vs choreography applies directly to saga implementation choice:

- **Complex error / compensation scenarios** — prefer orchestrated sagas. Compensation in a choreographed saga adds new cross-service links per failure case; an orchestrator already has links to everyone.
- **High throughput / scale** — prefer choreographed sagas. Chapter 11 specifically names `Time Travel Saga(sec)` and `Anthology Saga(aec)` (both choreographed) as the patterns that achieve the highest scale.
- **Workflow state visibility** — orchestrated sagas give it for free; choreographed sagas need a [[correlation-ids|correlation ID]] + state-projection service.

The eight saga patterns split cleanly across Chapter 11's axis:

- **Orchestrated**: `Epic Saga(sao)`, `Fairy Tale Saga(seo)`, `Fantasy Fiction Saga(aao)`, `Parallel Saga(aeo)`
- **Choreographed**: `Phone Tag Saga(sac)`, `Time Travel Saga(sec)`, `Anthology Saga(aec)`
- **The cautionary edge case**: `Horror Story(aac)` — asynchronous + atomic + choreographed — which Chapter 11 flags as the combination that tends to produce genuinely painful implementations.

Practical consequence: when a workflow has both transactional-consistency requirements *and* [[semantic-coupling|high semantic coupling]] in the domain, the saga discussion starts from the orchestrated side of the table. When the workflow is a simple linear chain with rare compensation, choreographed sagas stay close to the domain's semantic floor.

## Hard Parts Ch 12: the eight-pattern saga taxonomy

Chapter 12 of *The Hard Parts* is the **deep treatment** of transactional sagas. It names the full 2×2×2 combination space along the three axes of [[dynamic-coupling]] (source: raw/software-architecture-the-hard-parts/chapter-12-transactional-sagas.md):

- **Communication**: synchronous vs asynchronous
- **Consistency**: atomic vs eventual
- **Coordination**: orchestrated vs choreographed

Each combination gets a whimsical Greek- or story-themed name plus a superscript encoding the three axes in alphabetical order (communication, consistency, coordination). The superscript is the pragmatic lookup key; the name is the mnemonic.

### The eight patterns at a glance

| Pattern | Axes | Superscript | One-line |
|---|---|---|---|
| [[epic-saga|Epic Saga]] | sync / atomic / orchestrated | **sao** | "Traditional" distributed transaction; most coupled of all; rarely advisable |
| [[phone-tag-saga|Phone Tag Saga]] | sync / atomic / choreographed | **sac** | Chain-of-responsibility with compensations; rare combination; usually worse than Epic |
| [[fairy-tale-saga|Fairy Tale Saga]] | sync / eventual / orchestrated | **seo** | Common real-world choice; orchestrator + per-service transactions |
| [[time-travel-saga|Time Travel Saga]] | sync / eventual / choreographed | **sec** | Fire-and-forget pipelines; Chain of Responsibility / Pipes and Filters |
| [[fantasy-fiction-saga|Fantasy Fiction Saga]] | async / atomic / orchestrated | **aao** | Mostly implausible; usually an Epic Saga that "needs to be faster"; prefer Parallel |
| [[horror-story-saga|Horror Story]] | async / atomic / choreographed | **aac** | Worst combination; the cautionary tale; avoid |
| [[parallel-saga|Parallel Saga]] | async / eventual / orchestrated | **aeo** | Strong default for complex workflows needing scale |
| [[anthology-saga|Anthology Saga]] | async / eventual / choreographed | **aec** | Exact opposite of Epic; least coupled; EDA's default saga |

The exact ratings tables (Tables 12-2 through 12-9) live on each variant's page. The book ranks each pattern on four characteristics:

- **Coupling** — how tightly the participants are bound by the combination of axes.
- **Complexity** — design, implementation, debugging, and operational complexity combined.
- **Responsiveness / availability** — how the pattern behaves under normal load and participant failure.
- **Scale / elasticity** — throughput ceiling and how well participants scale independently.

### The two ends of the spectrum

- **[[epic-saga|Epic Saga(sao)]]** — **most coupled** pattern. Sync + atomic + orchestrated maximises every axis. Mimics monolithic behaviour in a distributed architecture; architects reach for it reflexively, usually to their cost.
- **[[anthology-saga|Anthology Saga(aec)]]** — **least coupled** pattern. Async + eventual + choreographed. The natural saga for [[broker-topology|broker-topology]] / [[event-driven-architecture|event-driven]] systems. Highest scale and responsiveness; correspondingly hard for complex workflows.

These two sit at opposite corners of the 2×2×2 cube; the remaining six are each one, two, or three axis-swaps away.

### The axis-substitution intuition

The patterns are easiest to remember as axis-substitutions:

- Start from [[epic-saga|Epic Saga(sao)]] and relax consistency → [[fairy-tale-saga|Fairy Tale(seo)]].
- Relax consistency and communication → [[parallel-saga|Parallel(aeo)]].
- Relax all three → [[anthology-saga|Anthology(aec)]].

The book's advice typically tracks exactly this chain: if performance is inadequate, relax the most-expensive axis first (usually consistency), then communication, then coordination. Relaxing axes **in the wrong order** produces the bad patterns — swap communication while keeping atomicity and orchestration and you get [[fantasy-fiction-saga|Fantasy Fiction(aao)]]; swap both communication and coordination while keeping atomicity and you land in [[horror-story-saga|Horror Story(aac)]].

### Pick a pattern per workflow, not per system

Chapter 12's pedagogical point: **there is no single right saga for a system**. Different workflows in the same architecture legitimately want different patterns. A ticket-completion workflow may be a [[fairy-tale-saga]]; an analytics ingestion pipeline in the same system may be an [[anthology-saga]]. Architects do the trade-off analysis **per workflow**.

### Compensating updates are the universal failure primitive

All eight patterns use [[compensating-update|compensating updates]] when they reach for failure recovery inside an atomic workflow, or for data-correction in an eventual-consistency workflow. Chapter 12 reinforces Chapter 9's warning: compensation of a compensation failure is the nastiest known saga error mode and often requires human intervention. The [[compensating-update]] page covers the semantics, prerequisites, and failure modes.

### Saga state machines and state management

Chapter 12 introduces an alternative to compensating updates for [[eventual-consistency|eventual]] sagas: **saga state machines**. The orchestrator (or, in choreographed sagas, the set of participants) models the workflow as an explicit finite state machine with named states (`START`, `CREATED`, `ASSIGNED`, `COMPLETED`, `NO_SURVEY`, `CLOSED`) and transition actions. Instead of issuing a compensating update on partial failure, the saga transitions to an **error state** (e.g. `NO_SURVEY`) and the orchestrator retries or escalates asynchronously (source: raw/software-architecture-the-hard-parts/chapter-12-transactional-sagas.md).

The state-machine approach dominates compensating updates when:

- The end user should not be blocked by transient failures.
- The error path is resolvable by retry or manual intervention, not rollback.
- Cross-service atomicity is not a business requirement.

It's the preferred mechanism inside a [[fairy-tale-saga|Fairy Tale(seo)]] or [[parallel-saga|Parallel(aeo)]].

### Managing sagas with annotations / custom attributes

Chapter 12 offers a concrete code-level technique: capture the set of sagas an application participates in as a language-level construct (Java `@Saga` annotation with a `Transaction` enum; C# custom attribute). Each `@ServiceEntrypoint` class declares which sagas it participates in. A simple code-walking CLI tool can then list all services involved in a named saga (source: raw/software-architecture-the-hard-parts/chapter-12-transactional-sagas.md):

```
$ ./sagatool.sh NEW_TICKET -services
-> Ticket Service
-> Assignment Service
-> Routing Service
-> Survey Service
```

This gives the team a real inventory of saga membership for test-scope analysis and change-impact review. The annotations themselves do nothing at runtime; they exist to be grepped.

### The decision matrix

Chapter 12's closing contribution is a combined ratings matrix covering all eight patterns along coupling, complexity, responsiveness, and scale — the condensed form of Tables 12-2 through 12-9. The matrix is the book's final artefact for saga selection: consult it per workflow, pick the least-worst combination.

## The Oxford etymology (*Hard Parts* Ch 1)

*Software Architecture: The Hard Parts* opens its Sysops Squad introduction with the Oxford English Dictionary definition: *a saga is "a long story of heroic achievement"* (source: raw/software-architecture-the-hard-parts/chapter-01-what-happens-when-there-are-no-best-practices.md). The authors note that architects have co-opted the term to describe transactional behaviour in distributed architectures — the coordination pattern documented on this page — but the literary sense survives in the book's recurring *Sysops Squad* pedagogical example, which itself is framed as a "saga" about one fictional ticketing system's journey out of a distributed monolith. The transactional saga chapter sits much later in the book (Chapter 12); Chapter 1 only points at it.

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
- [[event-driven-architecture]]
- [[broker-topology]]
- [[mediator-topology]]
- [[service-granularity]]
- [[microservices]]
- [[connascence]]
- [[workflows-in-edm]]
- [[compensation-workflow]]
- [[idempotence]]
- [[effectively-once-processing]]
- [[single-writer-principle]]
- [[software-architecture-the-hard-parts]]
- [[data-ownership]]
- [[base-properties]]
- [[compensating-update]]
- [[orchestrated-request-based-pattern]]
- [[event-based-consistency-pattern]]
- [[distributed-workflow-patterns]]
- [[workflow-orchestration]]
- [[workflow-choreography]]
- [[semantic-coupling]]
- [[dynamic-coupling]]
- [[epic-saga]]
- [[phone-tag-saga]]
- [[fairy-tale-saga]]
- [[time-travel-saga]]
- [[fantasy-fiction-saga]]
- [[horror-story-saga]]
- [[parallel-saga]]
- [[anthology-saga]]
