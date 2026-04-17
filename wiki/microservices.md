# Microservices

**Summary**: Independently deployable services modeled around a business domain, communicating over networks and owning their own data storage. A microservice architecture is an opinionated form of service-oriented architecture in which independent deployability is the central discipline.

**Sources**: `raw/monolith-to-microservices/chapter-01-just-enough-microservices.md`, `raw/monolith-to-microservices/chapter-02-planning-a-migration.md`, `raw/monolith-to-microservices/chapter-05-growing-pains.md`, `raw/fundamentals-of-software-architecture/chapter-07-scope-of-architecture-characteristics.md`, `raw/fundamentals-of-software-architecture/chapter-09-foundations.md`, `raw/fundamentals-of-software-architecture/chapter-17-microservices-architecture.md`

**Last updated**: 2026-04-16
---

## Definition

Microservices are independently deployable services modeled around a business domain that communicate with each other via networks (source: chapter-01-just-enough-microservices.md). They are a type of service-oriented architecture (SOA), but opinionated about two things: how service boundaries should be drawn, and that [[independent-deployability]] is key.

From a technology viewpoint, microservices expose business capabilities via one or more network endpoints. Because they communicate over networks, they are a form of distributed system. They also encapsulate data storage and retrieval, exposing data only via well-defined interfaces — databases are hidden inside the service boundary (source: chapter-01-just-enough-microservices.md).

## The three defining properties

### 1. Independently deployable

A change to one microservice can be deployed to production without deploying any other service. This is not just a capability — it is a discipline practiced for the bulk of releases (source: chapter-01-just-enough-microservices.md). To achieve this, services must be loosely coupled: explicit, well-defined, and stable contracts between services. See [[independent-deployability]].

### 2. Modeled around a business domain

Cross-process changes are expensive. By aligning service boundaries with business capabilities (rather than technical layers like UI / logic / database), changes to a single piece of business functionality stay within a single service (source: chapter-01-just-enough-microservices.md). Each service may then contain a thin slice of UI, logic, and storage as a local implementation concern. See [[bounded-context]] and [[domain-driven-design]].

### 3. Own their own data

Microservices should not share databases. If service A wants data held by service B, it asks B for it via B's interface. This lets B decide what to share and what to hide, and lets B map from changing internal implementation details to a stable public contract (source: chapter-01-just-enough-microservices.md). Sharing databases is one of the worst things you can do if you are trying to achieve [[independent-deployability]]. Related: [[information-hiding]].

## Advantages

- **Scale and robustness**: independent deployment enables new models for scaling and fault tolerance (source: chapter-01-just-enough-microservices.md).
- **Technology heterogeneity**: process isolation lets teams mix programming languages, deployment platforms, and databases.
- **Parallel development**: more developers can work on the system without getting in each other's way; each understands a smaller part.
- **Flexibility**: as James Lewis put it, "microservices buy you options" — they open up future solution paths but have a cost (source: chapter-01-just-enough-microservices.md).

## Costs

Microservices are distributed systems and inherit all the trouble that comes with that:

- Network communication has latency that varies and can fail (see [[unreliable-networks]], [[network-faults]], [[timeouts]]).
- [[transactions|Transactions]] across services are far harder than within a single process; you often must give them up for techniques with different trade-offs (see [[distributed-transactions]], [[two-phase-commit]]).
- Getting a consistent view of data across machines is difficult (see [[linearizability]], [[causal-consistency]]).
- New microservice-friendly technology can help you make mistakes faster and more expensively (source: chapter-01-just-enough-microservices.md).

Crucially, virtually all "monolithic" systems are also distributed (a single process talks to a database over a network); the difference is *the extent* to which the system is distributed (source: chapter-01-just-enough-microservices.md).

## Size

"How big should a microservice be?" is the most common question Newman gets, but he considers size one of the least interesting properties (source: chapter-01-just-enough-microservices.md). Lines of code is a poor metric — 25 lines of Java might be 10 lines of Clojure. The closest useful framing comes from Chris Richardson: the goal is "as small an interface as possible," which aligns with [[information-hiding]].

Newman urges focusing on two things instead:

1. **How many microservices can you handle?** Complexity grows with service count; this argues for incremental migration.
2. **How do you define service boundaries** to get value without creating a coupled mess?

## History

The term emerged from work by James Lewis at ThoughtWorks around 2011. He had observed companies optimizing service-oriented architectures so that services could be easily replaced — sometimes rewritten in a few days. Initially Lewis called these "micro-apps" because services were small enough that "services should be no bigger than my head." At a 2012 architectural summit, the group settled on "microservices" as a more accurate name (source: chapter-01-just-enough-microservices.md).

## Relationship to SOA

Microservices are a specific, opinionated style of [[rpc|service-oriented architecture]]. Where general SOA leaves service granularity, ownership, and data sharing open, microservices insist on independent deployability, business-domain alignment, and data ownership.

## Microservices are a means, not an end

Chapter 2 makes the point sharply: you don't "win" by having microservices. The decision to adopt them should serve a specific outcome that the existing architecture can't deliver (source: chapter-02-planning-a-migration.md). For the legitimate motivations (autonomy, time to market, scale, robustness, more developers, new technology) and the cheaper alternatives to consider for each, see [[why-microservices]]. For when *not* to adopt microservices, see [[when-microservices-are-a-bad-idea]].

For the migration approach itself — incrementally, one service at a time, evaluated against measured outcomes — see [[incremental-migration]] and [[measuring-microservice-transition]].

## The architectural-quantum view

Richards and Ford (Chapter 7 of *Fundamentals of Software Architecture*) give microservices a complementary framing: a microservices architecture is a **multi-quantum architecture**. Each service-plus-its-database satisfies the three-part definition of an [[architectural-quantum]] — independently deployable, high functional cohesion around a [[bounded-context]], and synchronous [[connascence]] contained within the service (source: chapter-07-scope-of-architecture-characteristics.md).

The consequence is that [[architecture-characteristics|architecture characteristics]] are scoped *per quantum* rather than across the whole system. The Payment microservice can have different availability, security, and scalability profiles from the Catalog microservice; both belong to the same product but neither lives under one global -ility scorecard. This is the design foundation for *hybrid* architectures.

Two practical prescriptions fall out of the quantum view:

- **Each microservice owns its database** (Newman's third defining property) is what makes the service a quantum at all. A shared database collapses the affected services into a single quantum and defeats per-service scoping of characteristics.
- **Prefer asynchronous communication between services** where operational characteristics differ. Synchronous calls between microservices create synchronous connascence for the length of the call, collapsing the operational profiles of caller and callee for that window. Event-driven or queue-based integration preserves independent characteristics.

Both prescriptions restate things Newman already argues for on different grounds — data ownership for [[independent-deployability]], asynchronous messaging for loose coupling — and converge with them cleanly.

## The distributed-architecture cost floor

Chapter 9 of *Fundamentals of Software Architecture* places microservices firmly on the distributed side of the [[monolithic-vs-distributed]] split. The practical consequence is that microservices pay the full cost structure that every distributed style pays: the [[fallacies-of-distributed-computing|eight fallacies of distributed computing]] plus the named other considerations (distributed logging, [[distributed-transactions|distributed transactions]], contract maintenance, distributed performance, distributed data access) (source: chapter-09-foundations.md).

Richards and Ford call out one fallacy as especially microservices-shaped: *the more a system relies on the network, the potentially less reliable it becomes* — and microservices rely on the network more than any other style in the book. Latency compounds at fan-out (10 chained calls at 100ms average = +1s per request); p95/p99 matter more than averages; **stamp coupling** (services returning large payloads when callers only need a fragment) silently burns bandwidth at rates that only become visible at load. The Chapter 3 cures — private endpoints, field selectors, GraphQL, [[consumer-driven-contracts]], narrow messaging events — are the microservices-era answers.

None of this invalidates the microservices case; it makes explicit the cost that [[why-microservices]]'s three-question test is really asking about.

## Growing pains as you scale

Chapter 5 catalogues the operational and organisational pains that emerge as service count grows (source: chapter-05-growing-pains.md). Newman's framing: think of microservice adoption as a dial, not a switch — as you turn it up, you get more of the benefits *and* hit different pain points. The major ones:

- **[[code-ownership-models]]** — collective ownership stops working at ~100 developers; strong ownership becomes universal.
- **[[breaking-changes]]** and **[[consumer-driven-contracts]]** — eliminate accidental contract breakages or the architecture becomes untenable.
- **[[cross-service-analytics]]** — split databases break the assumption that all data is queryable from one schema.
- **[[monitoring-and-observability]]** — monolith-era monitoring assumes binary failure; microservices need rich, queryable telemetry.
- **[[local-developer-experience]]** — running enough services on a laptop becomes impossible; need stubs, hybrid setups, or remote development.
- **[[running-too-many-things]]** and **[[desired-state-management]]** — manual deployment doesn't scale; reach for Kubernetes or serverless.
- **[[end-to-end-testing]]** — large cross-team test suites become slow, flaky, and ambiguous; shift to CDCs and progressive delivery.
- **[[global-vs-local-optimization]]** — local team decisions compose into global duplication; build cross-cutting forums without centralising.
- **[[robustness-and-resiliency-at-scale]]** — rare distributed-system failures become routine.
- **[[orphaned-services]]** — services run untouched for years until nobody knows what they do.

## The style in the catalog — Richards & Ford's Chapter 17 framing

Chapter 17 of *Fundamentals of Software Architecture* treats microservices not primarily as a migration destination (Newman's frame) or as a multi-quantum system (the Chapter 7 frame), but as **one architecture style within a catalog** of nine. The chapter's job is to slot microservices into the same star-rated scorecard every other Part II style gets, and to name the decisions that distinguish it from [[service-based-architecture]], [[orchestration-driven-soa]], and the monolithic styles (source: chapter-17-microservices-architecture.md).

### The style's driving philosophy: physical embodiment of bounded context

Richards and Ford's opening position: microservices is "the physical embodiment of the logical concepts in [[domain-driven-design]]." Each service *is* a [[bounded-context]] — not hosts-a-bounded-context but *is* one, including its classes, subcomponents, and database schema. The style takes [[technical-vs-domain-partitioning|domain partitioning]] to its extreme: every service is a domain or subdomain, full stop (source: chapter-17-microservices-architecture.md).

The philosophical move that makes this a distinct style: microservices **prefer duplication to coupling**. An `Address` class is not shared between services the way a monolith would share it. Reuse of code is explicitly traded away in exchange for decoupling. The First Law of Software Architecture is invoked by name: reuse always produces coupling; if your goal is high decoupling, you must prefer duplication (source: chapter-17-microservices-architecture.md). This is the same force [[orchestration-driven-soa]]'s canonical-`Customer` worked example shows going the other direction — SOA pursued reuse and paid the coupling cost; microservices pursues decoupling and pays the duplication cost.

### Granularity: the central architect's decision

Chapter 17 elevates **[[service-granularity|granularity]]** to the hardest single decision in the style. The quote: *"The term 'microservice' is a label, not a description"* — Martin Fowler. The name was chosen to contrast with SOA's ["gigantic services"], not as a commandment to build the smallest possible services. Too many developers hear the name and over-decompose (source: chapter-17-microservices-architecture.md).

Three guidelines Richards and Ford offer for finding the right boundary:

1. **Purpose** — each service should be extremely functionally cohesive, contributing one significant behaviour to the overall application.
2. **Transactions** — bounded contexts are business workflows, and the entities that must cooperate in a transaction typically belong together; needing a transaction across service boundaries is a smell that the split was wrong.
3. **Choreography** — if services are so fine-grained that they must communicate constantly to do useful work, the communication cost outweighs the decoupling benefit; bundle them back up.

"Don't do transactions in microservices — fix granularity instead!" is the chapter's most quotable line on this (source: chapter-17-microservices-architecture.md). See [[service-granularity]] for the full treatment and for how it plays out across the other styles (service-based is coarse, SOA failed partly on granularity, space-based sidesteps it with tuple-space caching).

### Data isolation as the structural consequence

The bounded-context-per-service rule drives a second rule: **services do not share databases**. Each service owns its schema. The Newman "own your own data" discipline is the same principle, surfaced here as the structural consequence of taking bounded contexts seriously (source: chapter-17-microservices-architecture.md).

Richards and Ford add two specific observations:

- **Entity trap avoidance** — don't model services to resemble single database entities. See [[entity-trap]] for the named anti-pattern.
- **Single-source-of-truth coordination** — with distributed data, architects must either name one service as the authority for each fact (and route reads to it) or accept the operational cost of replication and caching. There is no free relational-database unification.

The payoff: each service team picks the storage technology that fits its workload (relational, document, key-value, graph, whatever). Polyglot persistence is a natural consequence of the style, not a bolted-on feature.

### The API layer is optional

One of Chapter 17's corrections to common diagrams: the API gateway is optional, not structural. When it appears, its legitimate uses are indirection (service discovery, naming, authentication) — *not* mediation or orchestration. Putting workflow logic in an API gateway violates the style's philosophy: **all interesting logic belongs inside a bounded context**. An API layer that becomes a mediator drifts the architecture toward SOA (source: chapter-17-microservices-architecture.md).

### Operational reuse via sidecars and service mesh

Richards and Ford name the tension explicitly: microservices prefer duplication over coupling for *domain* concerns, but operational concerns (monitoring, logging, circuit breakers, service discovery) genuinely benefit from coupling. Solving this tension is what the [[sidecar-pattern]] and [[service-mesh]] are for, framed here as first-class parts of the style rather than optional infrastructure (source: chapter-17-microservices-architecture.md):

- Each service gets a common sidecar containing the cross-cutting operational concerns.
- A shared infrastructure team owns the sidecar; upgrading monitoring across the fleet is a sidecar update, not a fleet-wide code change.
- The sidecars connect via a service plane into a **service mesh**, providing unified control over logging, monitoring, and other cross-cutting operational concerns.
- **Service discovery** typically rides on the service mesh (or an API layer), providing the elasticity substrate that lets the architecture scale dynamically.

This is the style's answer to the critique that [[orchestration-driven-soa]] conflated domain and operational reuse: **keep the two concerns architecturally separate**. Domain logic lives in bounded-context services with duplication accepted; operational logic lives in sidecars with reuse encouraged.

### Communication: choreography preferred, orchestration when necessary

Chapter 17 treats the [[broker-topology|choreography]]/[[mediator-topology|orchestration]] choice the same way the [[event-driven-architecture]] chapter does — broker-topology choreography is preferred because it preserves the decoupling philosophy; orchestration is accepted for complex workflows where the coordination complexity in choreographed services (the "front controller" anti-pattern) exceeds the coupling cost of a dedicated orchestrator (source: chapter-17-microservices-architecture.md).

The chapter also names **protocol-aware heterogeneous interoperability** as the communication style:

- **Protocol-aware** — no central integration hub; each service knows how to call others (REST, messaging, gRPC). Protocols are standardised per service class.
- **Heterogeneous** — services can use different technology stacks (the "enforced heterogeneity" anecdote: a chief architect mandated different stacks per team to make accidental class-sharing impossible).
- **Interoperability** — services do call each other; the discipline is to do so without creating distributed transactions.

For transactions across services, the answer is the [[saga]] pattern — with the warning that needing many sagas means the granularity is wrong. Saga usage should be the exception, not the norm.

### Frontends: monolithic UI or microfrontends

Two user-interface patterns are catalogued (source: chapter-17-microservices-architecture.md):

- **Monolithic frontend** — a single UI (rich desktop, mobile, or web SPA) calls through the API layer. Pragmatic default for most systems.
- **Microfrontends** — each backend service emits UI components that a frontend shell coordinates. Extends the bounded-context discipline into the UI: one team owns one domain end-to-end, from UI through service through database. Implementations via React component composition or dedicated microfrontend frameworks.

The microfrontend pattern is the faithful DDD reading — the original bounded-context concept included UI — but most web applications use the monolithic UI for practical reasons.

### Characteristics star-rating

Chapter 17 closes with the star-rating scorecard. Microservices is a style of **extremes** — the highest and lowest marks on the same architecture:

| Characteristic | Rating | Why |
|---|---|---|
| **Scalability** | ★★★★★ | Independent services scale independently; "some of the most scalable systems yet written use this style" |
| **Elasticity** | ★★★★★ | Service discovery + automation enable rapid instance scaling |
| **Evolutionary** | ★★★★★ | Extreme decoupling at small deployment-unit granularity supports fast architectural change |
| **Agility** | ★★★★★ | Small deployment units, independent teams, automation-first |
| **Testability** | ★★★★★ | Small service scope + deployment independence = testable in isolation |
| **Deployability** | ★★★★★ | Independent deployability is the defining discipline |
| **Fault tolerance** | ★★★★ | Service isolation contains failures; can drop to lower under excessive interservice communication, fixed by redundancy and scaling |
| **Simplicity** | ★ | Distributed architecture, many moving parts, requires DevOps maturity |
| **Cost** | ★ | Infrastructure, operations, and engineering effort are all high |
| **Performance** | ★★ | Network calls + per-endpoint security checks + fan-out latency; mitigated by choreography over orchestration and intelligent caching |
| **Reliability** | ★★★★ | Per-service independence + patterns (circuit breakers, retries) yield high reliability under normal operation |

The shape is: **modern engineering practices maxed, operational characteristics excellent, simplicity and cost crushed**. This is the inverse of [[layered-architecture]]'s scorecard, which maxes simplicity and cost and caps operational characteristics at two stars. It is also the inverse of [[orchestration-driven-soa]], which scored high only on abstraction and crashed on almost everything else.

### Placement relative to adjacent styles

Where microservices sits in the Part II catalog:

- **vs [[service-based-architecture]]**: same distributed-style family, but service-based has 4–12 coarse-grained services sharing a database (ACID transactions preserved) while microservices has many fine-grained services each owning their own data. Service-based sacrifices peak operational characteristics for simplicity; microservices sacrifices simplicity for peak operational characteristics. No overlap in scorecard shape.
- **vs [[orchestration-driven-soa]]**: microservices is the **direct backlash**. Every SOA failure mode (central orchestration engine, shared database, technical partitioning, canonical models, distributed transactions, quantum-of-one despite distribution) has a microservices negation (choreography preferred, database-per-service, domain partitioning, bounded-context duplication, sagas used sparingly, many quanta). The relationship-to-modern-styles table on [[orchestration-driven-soa]] captures this one-for-one.
- **vs [[event-driven-architecture]]**: microservices commonly uses event-driven-architecture as its inter-service substrate. The resulting hybrid is "event-driven microservices," which combines the structural decoupling of microservices with the performance/scalability benefits of asynchronous event flow. A microservices architecture on an event-driven substrate has implicitly chosen broker-topology choreography, which is the natural match for the style anyway.
- **vs [[space-based-architecture]]**: different problem shape. SBA targets extreme variable concurrent load with replicated in-memory data grids; microservices targets general-purpose domain decomposition with independent deployment. Can compose as "event-driven space-based microservices" in extreme cases, but the two styles solve different problems.
- **vs monolithic styles ([[layered-architecture]], [[pipeline-architecture]], [[microkernel-architecture]])**: the quantum count and operational characteristics are the split. Monolithic styles buy simplicity and cost at the price of operational ceilings; microservices inverts the trade.

### The chapter's own final framing

Richards and Ford close with: *"The driving philosophy of extreme decoupling creates many headaches in this architecture but yields tremendous benefits when done well."* The chapter recommends three follow-on references: Newman's *Building Microservices*, Richards's own *Microservices vs. Service-Oriented Architecture*, and *Microservices AntiPatterns and Pitfalls*. The first of those is the source for the bulk of this wiki page's pre-Chapter-17 material; the second is the direct comparison this section now makes concrete via the adjacent-style callouts above (source: chapter-17-microservices-architecture.md).

## Related pages

- [[monolith]]
- [[modular-monolith]]
- [[independent-deployability]]
- [[bounded-context]]
- [[domain-driven-design]]
- [[information-hiding]]
- [[coupling]]
- [[cohesion]]
- [[conways-law]]
- [[service-discovery]]
- [[rpc]]
- [[message-brokers]]
- [[why-microservices]]
- [[when-microservices-are-a-bad-idea]]
- [[incremental-migration]]
- [[extraction-prioritization]]
- [[bulkhead]]
- [[architectural-quantum]]
- [[architecture-characteristics]]
- [[monolithic-vs-distributed]]
- [[fallacies-of-distributed-computing]]
- [[service-granularity]]
- [[service-based-architecture]]
- [[orchestration-driven-soa]]
- [[event-driven-architecture]]
- [[broker-topology]]
- [[mediator-topology]]
- [[sidecar-pattern]]
- [[service-mesh]]
- [[saga]]
- [[entity-trap]]
