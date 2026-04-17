# Domain-Driven Design

**Summary**: A modeling discipline introduced by Eric Evans (2004) for representing a problem domain inside a software system. For microservices, DDD provides the conceptual tools — chiefly the [[aggregate]] and the [[bounded-context]] — for finding service boundaries that match how the business actually works.

**Sources**: `raw/monolith-to-microservices/chapter-01-just-enough-microservices.md`, `raw/monolith-to-microservices/chapter-02-planning-a-migration.md`, `raw/building-event-driven-microservices/chapter-01-why-event-driven-microservices.md`

**Last updated**: 2026-04-17

---

## Why it matters for microservices

Modeling services around a business domain is one of the three defining properties of [[microservices]]. The question is *how* to come up with that model — and DDD is the answer Newman recommends (source: chapter-01-just-enough-microservices.md).

The desire to have programs better represent the real world they operate in is not new — Simula and other early object-oriented languages were created for this purpose. But program-language capabilities alone are not enough. Eric Evans's *Domain-Driven Design: Tackling Complexity in the Heart of Software* (Addison-Wesley, 2004) presented a series of ideas that helped systems better represent the problem domain.

## The two ideas Newman highlights

For microservice architecture, Newman calls out two DDD concepts as essential:

- **[[aggregate]]** — a representation of a real domain concept (Order, Invoice, Stock Item) with a life cycle, often implementable as a state machine. The aggregate is a self-contained unit that decides for itself whether to allow a state transition.
- **[[bounded-context]]** — a larger organizational boundary inside an organization with explicit responsibilities. A bounded context contains one or more aggregates and exposes a deliberate interface to other contexts.

Both give us units of [[cohesion]] with well-defined interfaces, so both work well as service boundaries. The recommendation is to start with services that encompass entire bounded contexts and decompose along aggregate boundaries later if needed (source: chapter-01-just-enough-microservices.md).

## Domain modelling for migration prioritisation

Chapter 2 puts a second use on the domain model: not just for finding boundaries, but for **prioritising which services to extract first** (source: chapter-02-planning-a-migration.md). A high-level [[bounded-context]] map shows the dependencies between contexts. Inbound dependencies are a rough proxy for extraction effort:

- A context with many inbound dependencies (Newman's example: Notification — many parts of the system call it) is harder to extract because every caller must change from local invocation to a service call.
- A context with no inbound dependencies (Newman's example: Invoicing) is easier — patterns like the strangler fig can intercept its outbound traffic cleanly.

Combine this with the [[why-microservices|migration's actual goal]] using the [[extraction-prioritization|two-axis effort/benefit model]].

## How much modelling is enough?

Newman explicitly pushes back on perfectionism (source: chapter-02-planning-a-migration.md). You don't need a detailed domain model of the entire system to start. You need *enough* information to make a reasonable decision about where to start decomposition. A high-level map plus deeper analysis only of the parts you're considering extracting first is fine. The model should be continuously refined as you learn — it's a living artefact, not a one-shot deliverable.

## Further reading

Newman recommends:

- Eric Evans, *Domain-Driven Design: Tackling Complexity in the Heart of Software* (Addison-Wesley, 2004) — the original.
- Vaughn Vernon, *Domain-Driven Design Distilled* (Addison-Wesley, 2014) — shorter introduction.

For the collaborative modelling technique Newman highlights for shaping these models with non-developer colleagues, see [[event-storming]].

## Bellemare's concise vocabulary

Chapter 1 of *Building Event-Driven Microservices* restates the DDD vocabulary in four crisp definitions that are useful for framing event-driven designs (source: chapter-01-why-event-driven-microservices.md):

- **Domain** — the **problem space** the business occupies, including rules, processes, ideas, and terminology. The domain exists regardless of whether the business exists.
- **Subdomain** — a component of the domain focused on a subset of responsibilities, usually reflecting some organizational structure (Warehouse, Sales, Engineering). A subdomain is itself a domain.
- **Domain model** — an **abstraction** of the domain useful for business purposes. Part of the **solution space** (domain itself is the problem space). Discernible through the business's products, customer interfaces, and internal processes.
- **[[bounded-context|Bounded context]]** — the **logical boundaries** (inputs, outputs, events, requirements, processes, data models) relevant to a subdomain. Part of the solution space. Ideally aligned with a subdomain one-to-one, but legacy systems, technical debt, and third-party integrations often create exceptions.

Two properties matter most for service design (source: chapter-01-why-event-driven-microservices.md):

- **Bounded contexts should be highly cohesive.** The vast majority of communication should happen *internally*, not cross-boundary. High cohesion keeps design scope and implementation simple. See [[cohesion]].
- **Connections between bounded contexts should be loosely coupled.** Changes inside one context should minimize or eliminate impact on neighbours. See [[coupling]].

These two together are the load-bearing DDD inputs to the [[event-driven-microservices]] style — bounded contexts become the unit of microservice ownership, and the data communication structure (durable [[event-streams]]) carries whatever crosses the boundaries.

## Related pages

- [[aggregate]]
- [[bounded-context]]
- [[event-storming]]
- [[microservices]]
- [[information-hiding]]
- [[cohesion]]
- [[extraction-prioritization]]
- [[event-driven-microservices]]
- [[communication-structures]]
- [[coupling]]
