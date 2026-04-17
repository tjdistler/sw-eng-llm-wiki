# Technical vs Domain Partitioning

**Summary**: The first top-level decision an architect makes when identifying [[components]]: organise them by **technical capability** (presentation / business / persistence layers) or by **business domain** (Catalog / Checkout / Payment). Richards and Ford treat this as *the* foundational choice — it determines the architecture style on offer and the shape of every change that follows. Industry trend over the last several years has been toward domain partitioning, but neither is "correct"; the First Law applies.

**Sources**: `raw/fundamentals-of-software-architecture/chapter-08-component-based-thinking.md`

**Last updated**: 2026-04-16

---

## The two axes

> Organizing architecture based on technical capabilities like the layered monolith represents *technical top-level partitioning*. ... The other architectural variation represents *domain partitioning*, inspired by the Eric Evans book *Domain-Driven Design*. (source: chapter-08-component-based-thinking.md)

| | Technical partitioning | Domain partitioning |
|---|---|---|
| Top-level components | presentation, business rules, services, persistence | Catalog, Checkout, ManageInventory, Delivery |
| Canonical style | layered monolith, MVC | [[modular-monolith]], [[microservices]] |
| Organising principle | separation of *technical* concerns | separation of *domain* concerns |
| Team alignment ([[conways-law]]) | tech-skill silos (DBAs, frontend, backend) | cross-functional product teams |

Both use components; the difference is what the *top-level* components are. A technically-partitioned architecture still has domain code *inside* each layer; a domain-partitioned architecture still has persistence and UI code *inside* each domain component. The choice is about which axis is the dominant outer boundary.

## The Catalog-Checkout change-smear problem

The most concrete argument against technical partitioning: a realistic business workflow cuts across every technical layer. Chapter 8's example is `CatalogCheckout` — adding or modifying the checkout workflow touches the presentation layer, business-rules layer, service layer, and persistence layer all at once. The domain is **smeared across the technical layers** (source: chapter-08-component-based-thinking.md).

In a domain-partitioned system the same change lands inside a single `Checkout` component. [[cohesion|Cohesion]] of business functionality is high; [[coupling|coupling]] across the change is low. That's the logic behind the industry drift: most change requests are business-domain shaped, so the architecture that localises domain changes wins on change cost.

## Trade-offs (the First Law applies)

### Domain partitioning

**Advantages** (source: chapter-08-component-based-thinking.md):
- Models how the business actually works, not an implementation detail.
- Makes the **Inverse Conway Maneuver** easy — cross-functional teams map onto domain components.
- Aligns with modular-monolith and microservices styles.
- Message flow matches the problem domain.
- Easy to migrate data and components to a distributed architecture later.

**Disadvantage**:
- Customization / cross-cutting code appears in multiple places. (In the *Silicon Sandwiches* kata, the common-vs-local customization code has to live in every domain component that needs it.)

### Technical partitioning

**Advantages** (source: chapter-08-component-based-thinking.md):
- Clearly separates cross-cutting code (the *Silicon Sandwiches* alternative isolates Common and Local into their own top-level components).
- Aligns with the layered architecture pattern and with the traditional MVC separation — familiar to most developers.
- Matches legacy team structures (separate UI / backend / DBA teams).

**Disadvantages**:
- Higher **global coupling** — changes to a shared layer ripple through every domain using it.
- Developers end up duplicating domain concepts across layers.
- Typically higher coupling at the data level — one shared database becomes the default, which makes a later migration to distributed architectures expensive (it's hard to untangle the data relationships). See [[database-decomposition]] for what that migration looks like in practice.

## Conway's law and the Inverse Conway Maneuver

Technical partitioning is natural when the org is split by technical competency (DBA team, backend team, frontend team) — [[conways-law]] predicts exactly that outcome. Domain partitioning requires cross-functional product teams, which most traditional organisations don't have.

Jonny Leroy's **Inverse Conway Maneuver** (ThoughtWorks) is the counter-move: deliberately evolve team structure in the direction of the architecture you want, rather than accepting the architecture that falls out of the current org (source: chapter-08-component-based-thinking.md). This is why adopting a domain-partitioned architecture is usually also an org-design exercise — Newman's [[reorganizing-teams]] chapter is the microservices-side treatment of the same move.

## Which should you pick?

Richards and Ford's honest answer: it depends, and naming the trade-offs is the point of the exercise (source: chapter-08-component-based-thinking.md). That said:

- The industry trend over the last several years is toward domain partitioning — for both monolithic and distributed systems.
- Domain partitioning is a prerequisite for any eventual microservices extraction; technical partitioning actively works against it.
- Technical partitioning is still legitimate when the customization dimension genuinely dominates the domain dimension (the *Silicon Sandwiches* customization-heavy variant), or when the organisation cannot support cross-functional teams.

## Relationship to Newman's bounded contexts

Newman's *Monolith to Microservices* arrives at the same decision from the opposite direction: starting from the microservice target and asking how to find service boundaries. The [[bounded-context]] technique (and [[event-storming]] as a way to discover them) is the DDD-side vocabulary for the same underlying move: **partition by domain, not by technical layer**. The two framings converge.

## Related pages

- [[components]]
- [[component-identification-cycle]]
- [[entity-trap]]
- [[modular-monolith]]
- [[microservices]]
- [[monolith]]
- [[conways-law]]
- [[bounded-context]]
- [[domain-driven-design]]
- [[cohesion]]
- [[coupling]]
- [[fundamentals-of-software-architecture]]
