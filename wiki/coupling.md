# Coupling

**Summary**: The degree to which changing one part of a system requires changing another. Newman identifies four types relevant to microservices — implementation, temporal, deployment, and domain — each with different remedies. Reducing coupling is the central design pressure that shapes service boundaries.

**Sources**: `raw/monolith-to-microservices/chapter-01-just-enough-microservices.md`

**Last updated**: 2026-04-16

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

## Coupling vs cohesion

Coupling and [[cohesion]] are linked — they are the two halves of Constantine's law. Tightly coupled code tends to have low cohesion (related functionality spread across boundaries); high cohesion tends to reduce coupling (related code grouped together). The microservice movement is at heart a return to modular software design — modules that communicate via networks and can be independently deployed (source: chapter-01-just-enough-microservices.md).

## Related pages

- [[cohesion]]
- [[independent-deployability]]
- [[information-hiding]]
- [[microservices]]
- [[monolith]]
- [[message-brokers]]
- [[rpc]]
