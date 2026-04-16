# Microservices

**Summary**: Independently deployable services modeled around a business domain, communicating over networks and owning their own data storage. A microservice architecture is an opinionated form of service-oriented architecture in which independent deployability is the central discipline.

**Sources**: `raw/monolith-to-microservices/chapter-01-just-enough-microservices.md`, `raw/monolith-to-microservices/chapter-02-planning-a-migration.md`, `raw/monolith-to-microservices/chapter-05-growing-pains.md`

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
