# Coupling

**Summary**: The degree to which changing one part of a system requires changing another. Newman identifies four types relevant to microservices — implementation, temporal, deployment, and domain — each with different remedies. Reducing coupling is the central design pressure that shapes service boundaries.

**Sources**: `raw/monolith-to-microservices/chapter-01-just-enough-microservices.md`, `raw/fundamentals-of-software-architecture/chapter-03-modularity.md`, `raw/building-event-driven-microservices/chapter-01-why-event-driven-microservices.md`, `raw/site-reliability-engineering/chapter-09-simplicity.md`, `raw/software-architecture-the-hard-parts/chapter-01-what-happens-when-there-are-no-best-practices.md`, `raw/software-architecture-the-hard-parts/chapter-02-discerning-coupling-in-software-architecture.md`

**Last updated**: 2026-04-19

---

## Why it matters

Coupling and [[cohesion]] together govern whether a system is stable. Constantine's law:

> "A structure is stable if cohesion is high, and coupling is low." — Larry Constantine

In a distributed system, the cost of change across service boundaries is high. Loosely coupled services with stable contracts are what make [[independent-deployability]] possible (source: chapter-01-just-enough-microservices.md). The four types below come from Newman's own taxonomy — he notes it isn't intended to be exhaustive, just useful for thinking about distributed systems. Prior taxonomies by Meyer, Yourdon, and Constantine cover the same ground in other ways.

## 1. Implementation coupling

> A is coupled to B in terms of *how* B is implemented — when B's implementation changes, A also changes (source: chapter-01-just-enough-microservices.md).

The most pernicious form Newman sees, but often the easiest to reduce. The classic example: a Recommendation service reads directly from the Order service's database. The Recommendation service is now coupled to the Order schema, the SQL dialect, and even the row layout. If Order renames a column or splits a table, Recommendation breaks.

**Remedy**: hide implementation behind an interface ([[information-hiding]]). The Recommendation service should fetch order data via an Order service API, or via a separately-published, intentionally-shaped read dataset. Either way, internal changes inside Order remain invisible to consumers. See [[information-hiding]].

## 2. Temporal coupling

A runtime concern: when sending a message and handling that message are connected in time, services are temporally coupled (source: chapter-01-just-enough-microservices.md). The classic case is a chain of synchronous HTTP calls (Warehouse → Order → Customer); for the operation to complete, *all three services must be up and contactable simultaneously*.

**Remedies**:

- **Caching** — if Order caches the Customer data it needs, the dependency on Customer being up is broken in many cases.
- **Asynchronous transports** like a [[message-brokers|message broker]] — the message is sent now, processed when the downstream service is available.

A full exploration of service-to-service communication is in Chapter 4 of *Building Microservices*.

## 3. Deployment coupling

Multiple statically-linked modules in a single process force everything to deploy together — a one-line change in one module requires redeploying the whole monolith. This is enforced deployment coupling (source: chapter-01-just-enough-microservices.md).

Deployment coupling can also be a *choice*: a "release train" deploys all changes since the last train at a fixed cadence. Newman has worked in organizations that deployed *every* service in the system as part of every release train, regardless of whether anything changed. He sees release trains as a transitional step, not a goal.

**Why it matters**: deploying carries risk. Changing only what needs to be changed reduces the surface area for things to break, and makes diagnosis easier when they do. **Smaller releases make for less risk.** This is the heart of continuous delivery. Reducing deployment coupling does not strictly require microservices — Erlang's hot code reloading is another way — but [[microservices]] are the architecture Newman pursued for this reason (source: chapter-01-just-enough-microservices.md).

## 4. Domain coupling

In any system of independent services, there must be some interaction between participants — and these interactions model the real domain. To place an order, you need to know what's in the basket. To ship a product, you need to know where to send it. This is domain coupling, and it cannot be eliminated (source: chapter-01-just-enough-microservices.md).

But it can be *minimized* by being careful about what is shared. Newman's Music Corp example: when shipping an item, sending the *full Order* to the Warehouse service is too much — it exposes pricing and credit card information the warehouse doesn't need. A new domain concept, a *Pick Instruction*, can carry only what the warehouse needs (item, quantity, address). This is [[information-hiding]] applied to inter-service messages.

A further variation: have the Order Processing service emit an event that the Warehouse consumes, flipping the dependency direction. Whether to use synchronous calls, asynchronous events, or a richer Pick Instruction depends on the wider interaction model — domain modeling helps here.

## The Structured Design axes: afferent and efferent

Newman's four types above are the distributed-systems framing. Richards and Ford's Chapter 3 goes one layer deeper, to the *code-level* measurement of coupling — the foundation that lets tooling reason about it (source: chapter-03-modularity.md).

Yourdon and Constantine's 1979 *Structured Design* defined the two base metrics:

- **Afferent coupling (Ca)** — incoming dependencies: how many things depend on this module?
- **Efferent coupling (Ce)** — outgoing dependencies: how many things does this module depend on?

On top of those, Robert Martin defined **abstractness**, **instability**, and **distance from the main sequence** — derived metrics that locate a module on a 2D plot and let architects spot the [[coupling-metrics|zones of pain and uselessness]]. See [[coupling-metrics]] for the full treatment.

## From counting to classifying: connascence

Afferent/efferent only answer *how much* coupling exists. Meilir Page-Jones's [[connascence]] framework (1996) answers *what kind* and *how hard to refactor*. Where structured programming grouped all method-call coupling as "data coupling," connascence splits it into five ordered static forms (CoN, CoT, CoM, CoP, CoA) plus four dynamic forms covering runtime concerns (execution, timing, values, identity) that structured programming never addressed (source: chapter-03-modularity.md).

The two frameworks compose: afferent/efferent counts are the inputs to architectural-scale governance (fitness functions, dependency limits); connascence is the refactoring compass when a specific dependency needs to be weakened.

## Coupling on domain data, not on APIs

Adam Bellemare's *Building Event-Driven Microservices* Chapter 1 recasts one of the central trade-offs in service-to-service integration: whether services couple on an **implementation API** (the synchronous-microservice default) or on **domain data** shared through durable [[event-streams]] (source: chapter-01-why-event-driven-microservices.md).

- **API coupling** — the caller depends on the specific signatures, error modes, and versioning strategy of the callee's implementation. Changes to the implementation force coordinated rollouts. This is the implementation coupling above, dressed up as a network interface.
- **Domain-data coupling** — the consumer depends on the **schema and semantics of an event stream**, not on any particular producer implementation. The producer owns emission; the consumer owns modeling. A producer can rewrite, re-host, or replace its implementation with no consumer-visible change as long as the event schema is preserved.

The point is not that domain-data coupling is zero — every dependency is a coupling — but that it is **weaker and more evolvable** than API coupling because the event schema is a narrow, explicitly-versioned contract, and because consumers read asynchronously from a log rather than synchronously from a live process. Bellemare calls out data schemas specifically as the mechanism that gives change-management properties APIs alone cannot match.

This is the coupling reframing behind [[event-driven-microservices]]: by pushing cross-service integration onto the data communication structure, services couple on what changes least (domain events) rather than on what changes most (each other's implementations). See [[communication-structures]] and [[synchronous-microservices]] for the structural context.

## Static vs dynamic coupling (Page-Jones, restated in *The Hard Parts*)

*Software Architecture: The Hard Parts* (Ford, Richards, Sadalage, Dehghani, 2021) opens by invoking Meilir Page-Jones's observation — from *What Every Programmer Should Know About Object-Oriented Design* — that architectural coupling splits along a fundamentally different axis than the Newman types above (source: raw/software-architecture-the-hard-parts/chapter-01-what-happens-when-there-are-no-best-practices.md):

- **Static coupling** — how architectural parts are *wired together*: dependencies, coupling degree, connection points. Measurable at compile/deploy time because it represents the static structure of the architecture. Afferent/efferent counts, import graphs, and the service-plus-database-plus-dependency bundle that defines an [[architectural-quantum]] all live here.
- **Dynamic coupling** — how architectural parts *call one another at runtime*: what kind of communication, what information is passed, strictness of contracts, synchronous vs asynchronous, request/response vs pub/sub. Dynamic coupling is invisible to a deployment diagram; it surfaces only under load and failure.

The two axes are orthogonal. Two services that are statically decoupled (each deploys independently, each has its own database, neither imports the other's code) can still be tightly dynamically coupled (one synchronously calls the other for every request and blocks until it responds). Conversely, two components statically coupled in a shared codebase can interact asynchronously with loose contracts and weak dynamic coupling.

This is the organizing distinction of *Hard Parts*: Part I ("Pulling Things Apart") treats **static coupling** — how to decompose and draw boundaries — and Part II ("Putting Things Back Together") treats **dynamic coupling** — how the pieces communicate after they're separated. The trade-off analysis method (identify coupling → analyze trade-offs → document decisions) applies to both axes.

Mapping onto the Newman types above: implementation and deployment coupling are primarily *static*; temporal coupling is primarily *dynamic*; domain coupling spans both (the dependency is static, but how it's realised is a dynamic choice).

### Chapter 2: the working definition and the three-dimensional dynamic lens

*Hard Parts* Chapter 2 — "Discerning Coupling in Software Architecture" — pins the vocabulary down for the rest of the book (source: raw/software-architecture-the-hard-parts/chapter-02-discerning-coupling-in-software-architecture.md). Its working definition is deliberately minimal:

> Two parts of a software system are coupled if a change in one might cause a change in the other.

From there, the chapter separates [[static-coupling]] from [[dynamic-coupling]] as analytical axes of the [[architectural-quantum]], and crucially refines dynamic coupling into a *three-dimensional* decision space:

1. **Communication** — synchronous vs asynchronous.
2. **Consistency** — atomic vs eventual.
3. **Coordination** — orchestrated vs [[choreography|choreographed]].

Each option has a gravitational effect on the others — transactionality is easier with synchronous + mediated workflows, while higher scale is possible with asynchronous + eventual + choreographed workflows. The 2 × 2 × 2 combinations form the pattern space Part II of the book walks through. See [[dynamic-coupling]] for the full treatment and [[static-coupling]] for the bootstrap-time counterpart.

The Chapter 2 refinement also tightens the [[architectural-quantum]] definition to *independently deployable, high functional cohesion, high static coupling, and synchronous dynamic coupling* — synchronous dynamic coupling across a quantum boundary is what silently fuses two otherwise-separate quanta into one.

## Coupling vs cohesion

Coupling and [[cohesion]] are linked — they are the two halves of Constantine's law. Tightly coupled code tends to have low cohesion (related functionality spread across boundaries); high cohesion tends to reduce coupling (related code grouped together). The microservice movement is at heart a return to modular software design — modules that communicate via networks and can be independently deployed (source: chapter-01-just-enough-microservices.md).

## Loose coupling as a simplicity pattern (SRE Ch 9)

Chapter 9 of *Site Reliability Engineering* adopts the same framing under its simplicity banner (source: chapter-09-simplicity.md):

> Loose coupling between binaries, or between binaries and configuration, is a simplicity pattern that simultaneously promotes developer agility and system stability. If a bug is discovered in one program that is a component of a larger system, that bug can be fixed and pushed to production independent of the rest of the system.

The SRE contribution is to name loose coupling as the structural enabler of **independent fixability**, not just independent deployability. When a component can be fixed and released without rebuilding the rest, the mean-time-to-repair shrinks for the whole system — the individual MTTR of each binary is decoupled from the aggregate deploy scope.

Chapter 9 also extends the framing to configuration: code-to-config coupling is coupling too. A binary that has to be rebuilt for every config change has coupled two things that should be separable. See [[configuration-management-sre]] for Google's four models for decoupling configuration from binaries.

See [[simplicity-sre]] for the full Chapter 9 treatment.

## Related pages

- [[cohesion]]
- [[coupling-metrics]]
- [[connascence]]
- [[modularity]]
- [[independent-deployability]]
- [[information-hiding]]
- [[microservices]]
- [[monolith]]
- [[message-brokers]]
- [[rpc]]
- [[fundamentals-of-software-architecture]]
- [[event-driven-microservices]]
- [[synchronous-microservices]]
- [[event-streams]]
- [[communication-structures]]
- [[simplicity-sre]]
- [[configuration-management-sre]]
- [[software-architecture-the-hard-parts]]
- [[architectural-quantum]]
- [[static-coupling]]
- [[dynamic-coupling]]
- [[choreography]]
