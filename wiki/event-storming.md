# Event Storming

**Summary**: A collaborative domain-modelling exercise created by Alberto Brandolini in which technical and non-technical stakeholders together define a shared model by starting from domain events, grouping them into [[aggregate|aggregates]], and grouping aggregates into [[bounded-context|bounded contexts]].

**Sources**: `raw/monolith-to-microservices/chapter-02-planning-a-migration.md`

**Last updated**: 2026-04-16

---

## How it works

Event Storming works **bottom-up** (source: chapter-02-planning-a-migration.md):

1. Participants brainstorm **domain events** — things that happen in the system (e.g., "Order Placed", "Invoice Sent", "Payment Received"). These are facts that stakeholders care about.
2. Events are grouped into **[[aggregate|aggregates]]** — the domain entities responsible for them.
3. Aggregates are grouped into **[[bounded-context|bounded contexts]]** — the larger organisational boundaries inside the business.

The end product is a domain model that maps cleanly to the candidate microservice boundaries Newman recommends as starting points.

## Logical events, not implementation events

A common confusion: Event Storming does **not** mean you must build an event-driven system (source: chapter-02-planning-a-migration.md). It identifies the *logical* events that matter to the business. Those events might be implemented as messages on a broker, as state transitions in a relational schema, as records in a [[change-data-capture|CDC]] stream — or as nothing at all, if the model only needs to inform the decomposition.

## The point is shared understanding

Brandolini's emphasis is on the **collective** producing the model. The output isn't just the diagram; it's the shared understanding of the domain across roles (source: chapter-02-planning-a-migration.md).

For this to work, the right stakeholders need to be in the room — and that, Newman notes, is often the biggest challenge. The technique only works when business and technical participants are both present.

## Why it's useful for microservice migration

Event Storming produces exactly the artefacts Newman wants for [[extraction-prioritization|prioritising decomposition]]:

- A list of [[bounded-context|bounded contexts]] — candidate service boundaries.
- A view of relationships between them — useful for assessing extraction effort.
- A shared vocabulary across the team — useful for the conversations the migration will require.

It is one of the techniques Newman recommends for the up-front [[domain-driven-design|domain modelling]] step in a migration. Further reading: Brandolini's *Introducing EventStorming*.

## Related pages

- [[domain-driven-design]]
- [[bounded-context]]
- [[aggregate]]
- [[extraction-prioritization]]
- [[event-sourcing]]
- [[event-streams]]
