# Event-Driven Architecture Style

**Summary**: A distributed asynchronous architecture style built around **decoupled event processors** that react to events rather than serving synchronous requests. Richards and Ford position it as one of the most scalable and performant styles available — five stars on performance, scalability, elasticity, and fault tolerance — at the cost of simplicity and testability. Two canonical topologies: the **[[broker-topology]]** (peer-to-peer event chain, no central coordinator) and the **[[mediator-topology]]** (central event mediator coordinates a workflow). The style is the Part II architecture-style counterpart to the existing lower-level stream-processing and batch-pattern pages; it is also commonly embedded inside other styles (event-driven microservices, event-driven space-based, event-driven pipeline).

**Sources**: `raw/fundamentals-of-software-architecture/chapter-14-event-driven-architecture-style.md`, `raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md`

**Last updated**: 2026-04-18

---

## Request-based vs event-based

Richards and Ford frame event-driven architecture against the **request-based model** that most business applications follow (source: chapter-14-event-driven-architecture-style.md):

- **Request-based** — a request to *do* or *retrieve* something enters a request orchestrator (UI, API layer, ESB) which synchronously and deterministically routes it to request processors. Example: "retrieve my last six months of order history." The path through the system is known in advance; the call is data-driven, deterministic, and has a bounded response time.
- **Event-based** — the system *reacts* to something that happened. Example: "a bid was submitted in an online auction; compare against concurrent bids and update the high-bidder state." The path is not pre-determined; the interesting behaviour is emergent from which event processors happen to be listening.

The two models are complementary, not competitive. Richards and Ford recommend request-based for **well-structured, data-driven, deterministic** workflows and event-based for **flexible, action-based, reactive** workflows that need high responsiveness and scale (source: chapter-14-event-driven-architecture-style.md).

## What the style is made of

Event-driven architecture is made up of **decoupled event processing components** that asynchronously receive and process events (source: chapter-14-event-driven-architecture-style.md). The load-bearing vocabulary:

- **Initiating event** — the event that kicks off a flow (PlaceOrder, SubmitBid, ChangeJob).
- **Event processor** — an independent component that consumes events, does work, and (usually) emits further events.
- **Event channel** — the transport between processors: a queue or topic in a [[message-brokers|message broker]] or [[log-based-message-brokers|log-based broker]].
- **Processing event** — an event emitted by a processor after it has done its work. In the broker topology these tend to be **past-tense facts** (order-created, payment-applied); in the mediator topology they are **commands** (place-order, send-email).

Events flow through channels between processors; processors do not call each other directly. This is the mechanism behind the style's decoupling and scalability.

## Two canonical topologies

The entire chapter turns on the distinction between two topologies (source: chapter-14-event-driven-architecture-style.md):

- **[[broker-topology]]** — no central mediator. Events flow peer-to-peer through a broker; each processor advertises what it did and other processors react if they are interested. Like a relay race: once a processor hands off the baton, it is done. Simpler, higher performance, higher extensibility; no control over the overall workflow, weak error handling, no restart capability.
- **[[mediator-topology]]** — a central **event mediator** accepts the initiating event and coordinates the workflow by generating a sequence of processing commands to dedicated event channels. Event processors complete commands and acknowledge back to the mediator. Better control, error handling, and recoverability; more complex, slightly worse performance, and a scaling bottleneck on the mediator itself.

The choice is a trade-off between **workflow control and error handling** (mediator) versus **high performance and extensibility** (broker). Many real systems mix the two — a mediator for the general workflow, a broker-topology subflow for the dynamic parts.

This is the same axis Newman's [[saga]] chapter names as **orchestrated vs choreographed**. See the "Terminology reconciliation" section below.

## Event vs message

Richards and Ford touch on but do not belabour the event/message distinction. In the broker topology, processing outputs are **events** — past-tense facts (order-created). In the mediator topology, they are **commands** — imperative instructions (place-order). The broker topology is therefore choreographed by pub/sub: processors listen for events they care about and ignore the rest. The mediator topology is orchestrated by point-to-point queues: a command **must be processed** by its target, whereas an event **can be ignored** by any processor that is not interested.

## Asynchronous capabilities

The style relies **solely on asynchronous communication** for both fire-and-forget and request/reply flows (source: chapter-14-event-driven-architecture-style.md). The chapter's worked example: posting a website comment that takes 3,000ms to parse through bad-word, grammar, and context checkers. Synchronously, the user waits 3,100ms (50ms + 3,000ms + 50ms). Asynchronously, the user gets an acknowledgement in 25ms while the comment is still being processed in the background. **Responsiveness and performance are different things** — the async path addresses *responsiveness* (how soon the user is told something happened) without changing *performance* (how long the underlying work takes).

The async-only constraint is also the source of the style's biggest weakness: **error handling**. A synchronous call can return an error to the caller; an asynchronous processor that fails has no-one to tell. The chapter's **workflow event pattern** (a reactive-architecture pattern) is the named fix — see the Workflow event pattern subsection below.

### Workflow event pattern (error handling)

A **workflow delegate** is a second processor whose job is to receive errors from the primary processor, try to repair the message programmatically, and resubmit it. If it cannot repair the message, it forwards it to a **dashboard** where a human can inspect and fix it manually. The primary processor never blocks on error handling — it delegates and moves on — so responsiveness is preserved (source: chapter-14-event-driven-architecture-style.md).

The chapter's trading-firm worked example: a malformed trade order (`8756 SHARES` instead of `8756`) fails inside the Trade Placement service; the Trade Placement Error service strips the offending text, resubmits the fixed trade, and the original flow proceeds. One consequence: resubmitted messages arrive **out of order** relative to their original position in the stream. For ordering-sensitive flows (e.g. all trades within one brokerage account), the solution is to queue further messages for the affected key until the repaired one is reprocessed.

### Preventing data loss

Three places data can be lost in an event-driven flow, and the standard messaging-infrastructure fix for each (source: chapter-14-event-driven-architecture-style.md):

| Loss site | Fix |
|---|---|
| Producer → broker (broker goes down before the message is durable) | **Persistent queues** + **synchronous send** (producer blocks until broker acks the persist) |
| Broker → consumer (consumer crashes mid-process) | **Client acknowledge mode** — the message stays in the queue, pinned to the client ID, until the consumer acknowledges it |
| Consumer → database (DB write fails) | **ACID commit** + **last participant support (LPS)** — remove the message from the queue only after the DB has committed |

Together these are **guaranteed delivery** for event-driven architecture. They are off-the-shelf properties of any production-grade message broker.

### Broadcast

Producers broadcast events without knowing who, if anyone, will receive them (source: chapter-14-event-driven-architecture-style.md). This is the **highest level of decoupling** the style offers — the producer does not know the consumers; the consumers decide what, if anything, to do with the event. Broadcast is the foundation of [[eventual-consistency]] patterns and complex event processing.

### Request-reply (pseudosynchronous)

Sometimes a response is required — an order ID, a booking confirmation. Event-driven architecture implements synchronous-seeming calls as **request-reply messaging** with two queues per channel (request, reply). The chapter covers two implementations (source: chapter-14-event-driven-architecture-style.md):

- **Correlation ID** — producer sends to the request queue with a message ID, consumer replies to the reply queue with the correlation ID set to the original message ID, producer filters the reply queue by correlation ID. **Recommended for volume workloads.**
- **Temporary queue** — producer creates a throwaway reply queue per request. Simpler, but the broker's per-request queue creation slows down at scale.

## Characteristics scorecard

Richards and Ford rate event-driven architecture as follows (source: chapter-14-event-driven-architecture-style.md):

| Characteristic | Rating | Why |
|---|---|---|
| Performance | ★★★★★ | Async + highly parallel |
| Scalability | ★★★★★ | Programmatic load balancing via competing consumers |
| Fault tolerance | ★★★★★ | Decoupled async processors; eventual consistency; promises/futures |
| Elasticity | ★★★★★ | Add event processors to handle additional load |
| Evolutionary | ★★★★★ | New processors plug into existing event feeds (particularly in the broker topology) |
| Deployability | ★★★★ | Independent event processors deploy independently |
| Availability | ★★★★ | Decoupled processors survive peer failures |
| Modularity | ★★★ | Processors are the unit, but the overall workflow is implicit in the events |
| Simplicity | ★★ | Nondeterministic event flows; complex to reason about |
| Testability | ★★ | "Event tree diagrams" can generate thousands of scenarios; hard to test exhaustively |
| Cost | ★★ | Substantial infrastructure (brokers, durable queues, dead-letter flows) |

The style is **primarily technically partitioned** — any one domain is spread across multiple event processors tied together by brokers and mediators, so domain changes impact many processors (source: chapter-14-event-driven-architecture-style.md). "Event partitioning" is perhaps the more precise name.

## Architectural quantum

The number of [[architectural-quantum|quanta]] in an event-driven architecture ranges from **one to many** (source: chapter-14-event-driven-architecture-style.md). Even though communication is asynchronous, two couplings still bind processors into the same quantum:

- **Shared database** — processors sharing one DB instance are in the same quantum.
- **Request-reply synchrony** — the producer waits for the consumer's reply; if the consumer is down, the producer is blocked. That is synchronous connascence for the duration of the call, and ties the two processors into one quantum.

## Hybrid event-driven architectures

Event-driven architecture is often **embedded inside another style** rather than used standalone (source: chapter-14-event-driven-architecture-style.md). Common hybrids:

- **Event-driven microservices** — async events between microservices; see [[microservices]]. The service-to-service messaging substrate is an event-driven sub-architecture.
- **Event-driven space-based** — async data pumps feed processing units' in-memory data grids.
- **Event-driven [[microkernel-architecture|microkernel]]** — plug-ins invoked via async events rather than direct calls.
- **Event-driven [[pipeline-architecture|pipeline]]** — pipes are async event channels rather than synchronous point-to-point links.

Adding event-driven mechanics to any style **removes bottlenecks, provides back pressure, and increases responsiveness** at the cost of added complexity and infrastructure.

## When to use

- The domain is **reactive** — the system must respond to things happening rather than serve predetermined requests (auctions, trading, IoT, sensor pipelines, fraud detection).
- **High scalability / elasticity / performance / fault tolerance** are first-order characteristics.
- The workflow is **complex and dynamic** — many possible paths, many possible participants, and the set of listeners changes over the lifetime of the system.
- You need **architectural extensibility** — new processors plugging into existing event feeds without modifying upstream producers.

## When not to use

- The workflow is **request-shaped and deterministic** — use a request-based style ([[layered-architecture]], [[service-based-architecture]], [[microkernel-architecture]]).
- **Tight control** over the overall transaction is required and the mediator bottleneck is unacceptable. In that case, consider [[saga|orchestrated sagas]] inside a [[service-based-architecture|service-based]] or [[microservices]] architecture rather than full event-driven architecture.
- The team is **new to asynchronous programming** — the cost of building the error-handling, data-loss-prevention, and ordering machinery is substantial.

## Terminology reconciliation — mediator/broker ↔ orchestration/choreography

Richards and Ford's **mediator/broker** topologies are the same axis Newman's [[saga]] chapter calls **orchestration/choreography**:

| Richards & Ford (Ch 14) | Newman (M2M Ch 4) | What it is |
|---|---|---|
| **Mediator topology** | **Orchestrated saga** | A central coordinator knows the workflow, calls each participant in turn, owns error handling and recovery |
| **Broker topology** | **Choreographed saga** | No central coordinator; participants react to events and emit their own; the workflow is implicit in the event chain |

Both sources agree on the shape of the trade-off: orchestration/mediator gives **explicit workflow, easier debugging, and error-handling-with-a-home** at the cost of **centralisation, tighter coupling, and the orchestrator as bottleneck**. Choreography/broker gives **loose coupling, extensibility, and independent team ownership** at the cost of **implicit workflow, distributed saga state, and weaker error handling**.

Two differences in scope worth noting:

1. Newman treats orchestration/choreography as a **saga implementation choice inside a microservices architecture**. Richards and Ford treat mediator/broker as the **top-level topology of an event-driven architecture style** — one of two ways the whole system is organised.
2. Richards and Ford's **broker topology uses pub/sub events** (past-tense facts). Their **mediator topology uses point-to-point commands** (imperative instructions). Newman's saga chapter does not make this event-vs-command split as load-bearing, but the mechanics line up: choreographed sagas communicate via events on a broker, orchestrated sagas communicate via commands to named participants.

See [[saga]] for Newman's framing; this page and its sub-topology pages are the Richards-and-Ford architectural-style framing.

## In data architecture

Chapter 3 of *Fundamentals of Data Engineering* gives a compact treatment of event-driven architecture as one of the major architecture concepts (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md):

- Business events (new customer, new order, order update) are rarely static; an event-driven workflow creates, updates, and asynchronously moves them across lifecycle stages
- Three areas: **event production, routing, and consumption** — without tight coupling among producer, router, and consumer
- **Distributing the state of an event across multiple services** is the advantage: if a service goes offline, or a node fails in a distributed system, or multiple consumers need the same event, event-driven architecture handles it
- Anywhere you have [[loose-coupling|loosely coupled services]], event-driven architecture is a candidate

Reis and Housley treat event-driven patterns as embedded inside many of the other architecture patterns they describe — [[lambda-architecture]], [[kappa-architecture]], [[iot-architecture]], [[dataflow-model]] all lean on event-driven mechanics. The book's Chapter 5 covers event-driven streaming and messaging systems in depth.

## Relationship to existing wiki pages

Event-driven architecture at the **architecture-style level** is Richards and Ford's contribution — the top-level shape of a whole system. The wiki already has rich coverage of event-driven mechanics at **lower levels**:

- **Stream-processing level** — [[stream-processing]], [[event-streams]], [[log-based-message-brokers]], [[change-data-capture]], [[event-sourcing]]. Kleppmann's treatment of the data-flow substrate.
- **Pattern level** — [[event-driven-batch-pattern]] (Burns's workflow DAG over broker topics), [[event-pipeline-pattern]] (Burns's chained FaaS handlers), [[work-queue-pattern]]. Container-level reusable patterns.
- **Infrastructure level** — [[message-brokers]], [[publisher-subscriber-infrastructure]]. The transport.
- **Saga level** — [[saga]]. A specific coordination protocol for multi-service operations, which can be implemented in either topology.

Richards and Ford sit **above** all of these, using the same mechanics to describe the shape of an entire application. Their contribution is the style-level naming and the broker/mediator topology distinction.

## Related pages

- [[broker-topology]]
- [[mediator-topology]]
- [[monolithic-vs-distributed]]
- [[technical-vs-domain-partitioning]]
- [[architectural-quantum]]
- [[saga]]
- [[message-brokers]]
- [[log-based-message-brokers]]
- [[publisher-subscriber-infrastructure]]
- [[event-streams]]
- [[event-sourcing]]
- [[change-data-capture]]
- [[stream-processing]]
- [[event-driven-batch-pattern]]
- [[event-pipeline-pattern]]
- [[correlation-ids]]
- [[eventual-consistency]]
- [[microservices]]
- [[service-based-architecture]]
- [[layered-architecture]]
- [[pipeline-architecture]]
- [[microkernel-architecture]]
- [[fallacies-of-distributed-computing]]
- [[fundamentals-of-software-architecture]]
