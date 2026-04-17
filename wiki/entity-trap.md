# Entity Trap

**Summary**: The standing anti-pattern in [[components|component]] identification: one `*Manager` component per database entity. Richards and Ford name this the **entity trap** and treat it as the tell-tale sign that the architect has skipped workflow analysis and built an object-relational mapping in architectural clothing. If all you need is database-entity CRUD, download an ORM or scaffolding framework — don't design an architecture.

**Sources**: `raw/fundamentals-of-software-architecture/chapter-08-component-based-thinking.md`

**Last updated**: 2026-04-16

---

## The pattern

> The architect has basically taken each entity identified in the requirements and made a Manager component based on that entity. This isn't an architecture; it's an object-relational mapping (ORM) of a framework to a database. (source: chapter-08-component-based-thinking.md)

The symptom is a component diagram that reads like a list of database tables: `CustomerManager`, `OrderManager`, `ProductManager`, `PaymentManager`, `InvoiceManager`... each responsible for CRUD on one entity. No workflows, no roles, no cross-entity processes. Every component has the same verbs (create / read / update / delete) and differs only in the noun.

## Why it's a trap

The entity trap treats database relationships as if they were the application's workflows. In real systems, they almost never are. A realistic workflow — "check out a shopping cart" — spans many entities (`Customer`, `Cart`, `Inventory`, `Order`, `Payment`, `Shipment`), and it is the **workflow** that represents the domain, not any individual entity. Components built from entities leave the workflows implicit and distributed across wherever happens to call whom (source: chapter-08-component-based-thinking.md).

The secondary problems Chapter 8 flags:

- **Components end up too coarse-grained.** An `OrderManager` that owns everything order-shaped accumulates responsibilities until it's a mini-monolith.
- **No guidance to developers.** Below the component line, the package structure has to be invented from scratch because the component itself is just a CRUD bucket.
- **Workflow knowledge lives nowhere.** The actual business logic — when does an order become an invoice? who triggers payment capture? — is not represented as a first-class element in the architecture.

## The test: is it actually just CRUD?

Richards and Ford are direct: if the application genuinely is a thin UI over database entities, a full-blown architecture is overkill. Use a framework (source: chapter-08-component-based-thinking.md):

- **Naked Objects** / **Apache Isis** — frameworks that generate a UI directly from database entity definitions.
- **Ruby on Rails scaffolding** — the same idea in another ecosystem.

These tools solve the entity-CRUD-UI problem well, and the decision to use one is a legitimate architectural choice. The entity trap is when the architect *designs* something that does no more than these frameworks but calls it an architecture.

## The correct response

The entity trap is almost always a sign of missing workflow analysis. The remedies Chapter 8 offers map to the three discovery techniques on [[components]]:

- **Actor/actions** — name the actors and the actions they perform; components emerge from action clusters, not entity tables.
- **[[event-storming]]** — name the domain events; components emerge around event handlers.
- **Workflow analysis** — trace the end-to-end workflows; components emerge around workflow segments.

All three move the design away from entities and toward **behaviour**. That is the shift the entity trap fails to make.

## Related pages

- [[components]]
- [[component-identification-cycle]]
- [[technical-vs-domain-partitioning]]
- [[event-storming]]
- [[domain-driven-design]]
- [[bounded-context]]
- [[object-relational-mismatch]]
- [[fundamentals-of-software-architecture]]
