# Communication Structures

**Summary**: Adam Bellemare's three-part framework for how information flows through an organization — the **business**, **implementation**, and **data** communication structures. The framework reframes [[conways-law|Conway's law]] by naming the piece most organizations neglect (the data communication structure) and showing how overloading the implementation communication structure to fill that gap produces the classic pathologies of monolith sprawl and point-to-point microservice coupling.

**Sources**: `raw/building-event-driven-microservices/chapter-01-why-event-driven-microservices.md`, `raw/building-event-driven-microservices/chapter-17-conclusion.md`

**Last updated**: 2026-04-17

---

## The three structures

An organization's teams, systems, and people must communicate to fulfill their goals. Those communications form an interconnected topology of dependencies Bellemare calls a **communication structure**. There are three, and each affects how the business operates (source: chapter-01-why-event-driven-microservices.md).

### 1. Business communication structure

Communication between teams and departments — Engineering produces software, Sales sells, Support handles customers. The organization of teams, the provisioning of their goals, and the reporting lines from major business units down to individual contributors all fall under this structure (source: chapter-01-why-event-driven-microservices.md).

Business communication structures change over time: teams split, merge, and are reassigned responsibilities. These changes put pressure on the other two structures, especially the implementation communication structure.

### 2. Implementation communication structure

The data and logic of the subdomain model as dictated by the organization — where business processes, data structures, and system design are formalized in code (source: chapter-01-why-event-driven-microservices.md). The classic example is a monolithic database-backed application whose modules communicate through function calls and shared in-process state.

The implementation communication structure trades flexibility for speed: once business rules are encoded in a monolith's schema and code, the schema and code become authoritative, and changing them requires rewrites. Those rewrites are usually iterative — a reflection of the evolution of the business, not a one-shot event.

### 3. Data communication structure

How data is communicated **across the business**, particularly **between implementations** (source: chapter-01-why-event-driven-microservices.md). For humans this structure is dense and well-understood — email, chat, meetings, documents. For software implementations it has historically been **neglected**: fulfilled ad hoc, system to system, with the implementation communication structure often playing double duty.

This is the structure Bellemare's book is organized around. Most of the pain he diagnoses traces back to its absence or weakness.

## Conway's law through the communication-structure lens

[[conways-law|Conway's law]] — "organizations which design systems are constrained to produce designs which are copies of the communication structures of these organizations" — applies to all three structures, not just the business one (source: chapter-01-why-event-driven-microservices.md).

Bellemare's refinement: because the data communication structure is usually weak, the implementation communication structure ends up doing its job. Two design pressures result:

1. **Discouraging new products.** Getting domain data out of an existing implementation is hard, so teams hesitate to create logically separate products that would need it.
2. **Expanding existing products.** Existing domain data is easy to reach *inside* the implementation, so new requirements accrete onto whatever service already owns the data.

The second pressure is the Conway's-law mechanism behind monolith sprawl: every new requirement with a nearby data-gravity well grows the monolith rather than spawning a properly-bounded new service.

## Why overloaded implementation structures go wrong

Chapter 1's worked team scenario illustrates the dynamics (source: chapter-01-why-event-driven-microservices.md). The typical fixes organizations reach for — when they try to make the implementation communication structure carry cross-team data traffic — all have well-known failure modes:

| Fix | Why it hurts |
|---|---|
| **Shared database** | Promotes anti-patterns (see [[shared-database-antipattern]]); cannot scale to all performance requirements; exposes internal schemas. |
| **Read-only replicas** | Still exposes inner data models to readers; schema changes become coordination events. |
| **Batch file dumps** | Stale data, multiple sources of truth, brittle pipelines. |
| **Direct point-to-point copy** | Tight coupling between teams; sync jobs saturate source systems; copies drift; copy-of-a-copy propagates errors. |

All of these "harden the architecture into direct point-to-point relationships" (source: chapter-01-why-event-driven-microservices.md). They are symptoms of the same underlying problem: trying to solve a data-communication problem inside the wrong structure.

## The caution

Bellemare's explicit diagnostic cue (source: chapter-01-why-event-driven-microservices.md):

> If you find that it is too hard to access data in your organization or that your products are scope-creeping because all the data is located in a single implementation, you're likely experiencing the effects of poor data communication structures.

This problem magnifies as the organization grows, develops new products, and increasingly needs access to commonly used domain data.

## The event-driven fix

Event-driven architectures formalize the data communication structure as a set of durable [[event-streams]]. All shareable data is published to these streams; they become the canonical single source of truth for the organization. Production and ownership of data become **decoupled from access to it**: producers publish to their streams, and any consumer — present or future — can read (source: chapter-01-why-event-driven-microservices.md).

Two consequences of the inversion:

- **Applications can access data that was previously laborious to obtain**, without depending on point-to-point connections with any other service. New services can acquire history from the event streams, build their own models, and start producing business value without explicit coordination with producing teams.
- **Core domain events remain available across organizational change**. Teams restructure and products come and go, but the central data keeps flowing. This gives the business flexibility that no implementation-structure-based access can match (source: chapter-01-why-event-driven-microservices.md).

This is the structural thesis of [[event-driven-microservices]]: fix the weak third structure, and the overload symptoms on the other two go away.

## The Chapter 17 one-liner

Bellemare's conclusion restates the thesis of the book as a crisp definition of the mature data communication layer: it **decouples the ownership and production of data from the access and consumption of it** (source: chapter-17-conclusion.md). Producers focus on emitting well-defined events; consumers pull from the broker and model the data to their own needs. Neither has to negotiate with the other beyond the data contract on the stream. That one-sentence framing is the compact version of everything on this page.

## Relationship to adjacent wiki framings

- **[[conways-law]]** — Conway's law describes the pull; Bellemare names the three substructures where the pull operates.
- **[[technical-vs-domain-partitioning]]** — Richards & Ford's axis describes *which* logical partitioning the implementation communication structure adopts. Domain partitioning maps cleanly onto bounded contexts; technical partitioning smears business changes across the implementation.
- **[[reorganizing-teams]]** — Newman's treatment of the business-side half of the same question: when you want a different implementation communication structure, you usually have to change the business communication structure too.
- **[[event-streams]] / [[log-based-message-brokers]]** — the substrate that realizes the data communication structure in EDM architectures.

## Related pages

- [[event-driven-microservices]]
- [[conways-law]]
- [[event-streams]]
- [[log-based-message-brokers]]
- [[event-sourcing]]
- [[shared-database-antipattern]]
- [[bounded-context]]
- [[domain-driven-design]]
- [[coupling]]
- [[cohesion]]
- [[technical-vs-domain-partitioning]]
- [[reorganizing-teams]]
