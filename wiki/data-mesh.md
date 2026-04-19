# Data Mesh

**Summary**: A decentralised data architecture proposed by Zhamak Dehghani (2019) as a response to sprawling, monolithic data lakes and warehouses. Applies domain-driven design principles to data: domain teams own and serve their own data products, a central platform provides self-serve infrastructure, and computational governance is federated rather than centralised.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md`, `raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md`

**Last updated**: 2026-04-18

---

## The problem it reacts to

Reis and Housley frame the data mesh as a response to two specific pain points in traditional data architecture (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md):

- **Sprawling monolithic data platforms** — centralised [[data-lake|data lakes]] and [[data-warehousing|data warehouses]] that try to be the single owner of all data
- **The "great divide of data"** — the landscape split between operational data (owned by the product teams that generate it) and analytical data (owned by a central data team)

Chapter 3 quotes Dehghani:

> In order to decentralize the monolithic data platform, we need to reverse how we think about data, its locality, and ownership. Instead of flowing the data from domains into a centrally owned data lake or platform, domains need to host and serve their domain datasets in an easily consumable way.

The thesis: apply [[domain-driven-design]] — which has become the default in software architecture — to data architecture.

## The four principles

Dehghani identified four key components of the data mesh (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md):

1. **Domain-oriented decentralized data ownership and architecture** — each domain (sales, inventory, fulfilment, etc.) owns its analytical data just as it owns its operational data. No central data team acts as a middleman between data producers and data consumers.
2. **Data as a product** — domain teams treat their published data as a [[data-as-a-product|first-class product]] with consumers, SLAs, documentation, versioning, and a product manager. Not a byproduct of operations.
3. **Self-serve data infrastructure as a platform** — a central platform team provides the storage, pipelines, cataloguing, access control, and observability primitives so that **domain teams don't have to build their own**. The platform is domain-agnostic; the data is not.
4. **Federated computational governance** — global rules (schemas, interoperability, access policies, compliance) are agreed across domains and enforced computationally, not by a central committee reviewing every change.

## Chapter 9 — data mesh as a serving model

Chapter 9 returns to the mesh specifically as a **serving architecture**. It "fundamentally changes the way data is served" (source: raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md):

- Instead of siloed data teams serving their internal constituents, **every domain team takes on serving responsibilities** for its own data.
- Teams prepare their own data for consumption by other teams — ready for data apps, dashboards, analytics, BI tools across the organisation.
- Each team potentially runs its own dashboards and analytics for self-service.
- Domains consume data from other domains and may embed that data into their own software via user-facing analytics or ML features.

The effect on the engineer's job is structural: "this dramatically changes the details and structure of serving." Adopting a data mesh "dramatically reorganizes team responsibilities, and every domain team takes on aspects of serving. For a data mesh to be successful, each team must work effectively on its data serving responsibilities, and teams must also effectively collaborate to ensure organizational success" (source: raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md).

## Why Chapter 3 highlights it

The data mesh gets its own section because it is the direct counterpoint to the centralised patterns earlier in the chapter — [[data-warehousing]], [[data-lake]], [[data-lakehouse]], [[modern-data-stack]] (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md). Chapter 3 does not fully evaluate it but tells the reader to be aware of it; the canonical treatment is Dehghani's book *Data Mesh* (O'Reilly, 2022).

## Relationship to other principles

- **[[principles-of-good-data-architecture|Principle 6 (loose coupling)]]** — decentralised domain ownership is loose coupling applied to data ownership
- **[[principles-of-good-data-architecture|Principle 4 (architecture is leadership)]]** — federated governance replaces architect-as-dictator with architect-as-platform-builder
- **[[microservices]]** — the data mesh is the data-architecture analogue of microservices; the tension between global coherence and local autonomy is the same

## Cross-book connections

- [[domain-driven-design]] (from *Fundamentals of Software Architecture* and elsewhere) — the conceptual parent that data mesh borrows from
- [[bounded-context]] — the natural unit of a data-mesh domain
- [[event-driven-microservices]] and [[data-liberation]] (Bellemare) — an operational-side pattern where domains publish their data as event streams shares the same spirit as data mesh
- [[data-contract]] — the inter-domain interface in a data mesh

## Related pages

- [[data-as-a-product]]
- [[data-architecture]]
- [[principles-of-good-data-architecture]]
- [[domain-driven-design]]
- [[bounded-context]]
- [[data-warehousing]]
- [[data-lake]]
- [[data-lakehouse]]
- [[data-governance]]
- [[data-contract]]
- [[data-liberation]]
