# Bounded Context

**Summary**: A domain-driven design concept representing a larger organizational boundary inside an organization, within which explicit responsibilities are carried out and implementation details are hidden. Bounded contexts are the natural starting unit for drawing microservice boundaries.

**Sources**: `raw/monolith-to-microservices/chapter-01-just-enough-microservices.md`, `raw/monolith-to-microservices/chapter-02-planning-a-migration.md`

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

## Related pages

- [[aggregate]]
- [[domain-driven-design]]
- [[event-storming]]
- [[microservices]]
- [[information-hiding]]
- [[cohesion]]
- [[coupling]]
- [[extraction-prioritization]]
