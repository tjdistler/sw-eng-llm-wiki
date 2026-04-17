# Bounded Context

**Summary**: A domain-driven design concept representing a larger organizational boundary inside an organization, within which explicit responsibilities are carried out and implementation details are hidden. Bounded contexts are the natural starting unit for drawing microservice boundaries.

**Sources**: `raw/monolith-to-microservices/chapter-01-just-enough-microservices.md`, `raw/monolith-to-microservices/chapter-02-planning-a-migration.md`, `raw/fundamentals-of-software-architecture/chapter-07-scope-of-architecture-characteristics.md`

**Last updated**: 2026-04-16
---

## The concept

A bounded context typically represents a larger organizational boundary inside an organization. Within the scope of that boundary, explicit responsibilities need to be carried out (source: chapter-01-just-enough-microservices.md).

Newman's example: at the fictional Music Corp, the *warehouse* and the *finance department* are distinct bounded contexts. The warehouse manages shipping orders, taking delivery of stock, "having forklift truck races." Finance handles payroll and paying for shipments. Each context has internal concerns (the type of forklift used) that are of no interest to anyone outside it.

## Hiding implementation detail

Bounded contexts hide implementation detail. Internal concerns should be hidden from the outside world — outsiders don't need to know, nor should they care (source: chapter-01-just-enough-microservices.md). This is the same principle as [[information-hiding]], applied at the level of an organizational boundary rather than a single module.

A bounded context exposes a deliberate, explicit interface to other contexts. Inside it sits one or more [[aggregate|aggregates]]; some are exposed externally, others are kept internal.

## Mapping to microservices

Both [[aggregate|aggregates]] and bounded contexts give us units of cohesion with well-defined interfaces, so both can serve as service boundaries. Newman's recommendation (source: chapter-01-just-enough-microservices.md):

- **Start coarse-grained**: target services that encompass entire bounded contexts. This keeps the service count manageable while you build operational maturity.
- **Split later if needed**: as you find your feet, decompose along [[aggregate]] boundaries inside a context.
- **Hide the split**: even if you internally decompose a bounded-context service into smaller services, you can present a coarser-grained API to consumers. The decomposition is then an implementation decision you can hide.

## Why this matters for microservices

Aligning services with bounded contexts gives [[cohesion|high cohesion]] of business functionality — the code that changes together stays together, because changes to a business capability are contained inside one context. This minimizes [[coupling|cross-service change]], which is the most expensive kind of change in a distributed system.

## Bounded contexts as units of prioritization

Chapter 2 adds a second use: each bounded context is a candidate **unit of decomposition** for the migration. The relationships between contexts (visible on a domain-model diagram) help estimate which contexts are easier or harder to extract — see [[extraction-prioritization]] (source: chapter-02-planning-a-migration.md).

Newman cautions that the logical model is not the same as the code structure. A bounded context that looks easy to extract logically may turn out to be entangled in shared code or — worse — a shared database. Use the model as a starting point for the conversation, then dig into the code to confirm.

## Bounded context and the architectural quantum

Richards and Ford (Chapter 7 of *Fundamentals of Software Architecture*) connect the DDD bounded context to their [[architectural-quantum]] unit. The bounded context is a *logical* boundary that localises a domain model; the architecture quantum is a *physical* boundary that includes the deployable and its dependent components (source: chapter-07-scope-of-architecture-characteristics.md).

In a well-designed microservice architecture the two align: **one bounded context, one quantum, one service + its own database**. The bounded context gives the quantum its high functional cohesion (the module does one business-meaningful thing), and the service-owns-its-data discipline gives it the independent-deployability requirement.

Richards and Ford credit DDD as "deeply influential on modern architectural thinking" for exactly this reason: before DDD, teams sought holistic reuse across a shared Customer class (or Product, or Order) — which caused coupling, coordination cost, and complexity. The bounded context recognises that each entity works best inside a localised context, and reconciling differences at integration points is cheaper than enforcing a global shared model (source: chapter-07-scope-of-architecture-characteristics.md). The architecture quantum inherits that principle and adds the physical-deployment requirement on top.

The alignment is not automatic. A bounded context that depends synchronously on a database owned by another context isn't a quantum — the shared database collapses both contexts into a single deployable unit regardless of their logical separation. This is why Newman's "own your own data" rule for microservices matters: it's what lets the logical boundary become a physical one.

## Related pages

- [[aggregate]]
- [[domain-driven-design]]
- [[event-storming]]
- [[microservices]]
- [[information-hiding]]
- [[cohesion]]
- [[coupling]]
- [[extraction-prioritization]]
- [[architectural-quantum]]
- [[architecture-characteristics]]
