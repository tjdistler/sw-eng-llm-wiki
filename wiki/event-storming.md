# Event Storming

**Summary**: A collaborative domain-modelling exercise created by Alberto Brandolini in which technical and non-technical stakeholders together define a shared model by starting from domain events, grouping them into [[aggregate|aggregates]], and grouping aggregates into [[bounded-context|bounded contexts]].

**Sources**: `raw/monolith-to-microservices/chapter-02-planning-a-migration.md`, `raw/fundamentals-of-software-architecture/chapter-08-component-based-thinking.md`, `raw/fundamentals-of-software-architecture/chapter-20-analyzing-architecture-risk.md`

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

## As a component-identification technique (Richards & Ford)

Chapter 8 of *Fundamentals of Software Architecture* positions event storming under a different lens: not as a migration tool but as one of three general techniques for **discovering [[components]]** on a new system (source: chapter-08-component-based-thinking.md). The technique still starts from domain events, but the output is a component breakdown rather than a migration ranking.

The Richards & Ford framing:

> In event storming, the architect assumes the project will use messages and/or events to communicate between the various components. To that end, the team tries to determine which events occur in the system based on requirements and identified roles, and build components around those event and message handlers. (source: chapter-08-component-based-thinking.md)

Where Newman positions event storming alongside other DDD techniques for finding [[bounded-context|bounded contexts]], Richards and Ford position it alongside two alternatives for finding components:

- **Actor/actions** — the generic default (works on any style).
- **Event storming** — the DDD-and-messaging default (works best for microservices and event-driven styles).
- **Workflow analysis** — the middle ground (workflow-shaped components without the message-driven assumption).

The key Chapter 8 caveat: event storming "works well in distributed architectures like microservices that use events and messages, because it helps architects define the messages used in the eventual system" (source: chapter-08-component-based-thinking.md). In a system that genuinely isn't message-driven, the workflow approach or actor/actions is a better fit — event storming's explicit messaging assumption becomes noise.

## Two lenses, same technique

The Newman (migration) and Richards-Ford (component discovery) framings don't contradict each other; they use the same technique for adjacent problems:

| Framing | Starting point | Output |
|---|---|---|
| Newman | Existing monolith to decompose | Bounded contexts ranked for extraction |
| Richards & Ford | New system to design | Top-level components built around event handlers |

Both converge on the same underlying insight: **events and aggregates reveal the domain structure in a way that entity-first thinking does not**. Compare [[entity-trap]] for the anti-pattern event storming is designed to avoid.

## The same rhythm, different output: risk storming

Chapter 20 of *Fundamentals of Software Architecture* introduces **[[risk-storming]]**, a collaborative session for identifying architectural risk that shares event storming's structural shape almost exactly (source: chapter-20-analyzing-architecture-risk.md):

1. An asynchronous individual phase — participants walk the artefact (a diagram rather than a requirements list) *alone*, one to two days in advance, producing their own annotations.
2. A collaborative consensus phase — everyone arrives together, annotations are pooled on the shared artefact, and discussion reconciles disagreements.
3. An action phase — mitigation in risk storming; aggregate-and-bounded-context grouping in event storming.

Both rely on the same behavioural insight: premature discussion converges the group on the first-stated opinion and loses the diverse viewpoints the exercise was designed to capture. The silent individual phase is load-bearing in both techniques.

The difference is what the technique produces. Event storming maps the domain; risk storming maps the places the architecture is likely to fail. The same group of people can run both — event storming during early design or migration planning, risk storming continuously through the life of the system.

## Related pages

- [[domain-driven-design]]
- [[bounded-context]]
- [[aggregate]]
- [[extraction-prioritization]]
- [[event-sourcing]]
- [[event-streams]]
- [[components]]
- [[component-identification-cycle]]
- [[entity-trap]]
- [[risk-storming]]
- [[architecture-risk-matrix]]
- [[fundamentals-of-software-architecture]]
