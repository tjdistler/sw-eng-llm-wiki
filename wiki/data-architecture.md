# Data Architecture

**Summary**: The fourth [[data-engineering-lifecycle|lifecycle]] **undercurrent** — the current and future state of data systems that support an organisation's long-term data needs and strategy. Chapter 2 names the undercurrent; **Chapter 3 defines the discipline**: data architecture is a subset of enterprise architecture, its job is to design systems that support the evolving data needs of the enterprise through flexible, reversible decisions and careful trade-off analysis.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md`, `raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md`, `raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md`, `raw/software-architecture-the-hard-parts/chapter-14-managing-analytical-data.md`

**Last updated**: 2026-04-19

---

## What Chapter 2 says

"A data architecture reflects the current and future state of data systems that support an organization's long-term data needs and strategy. Because an organization's data requirements will likely change rapidly, and new tools and practices seem to arrive on a near-daily basis, data engineers must understand good data architecture." Chapter 3 covers architecture in depth; Chapter 2 simply highlights that it is an undercurrent (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

The data engineer's workflow:

1. **Understand the needs of the business** and gather requirements for new use cases.
2. **Translate those requirements into designs** for capturing and serving data, balanced for cost and operational simplicity.
3. **Know the trade-offs** across design patterns, technologies, and tools at every lifecycle stage — source systems, ingestion, storage, transformation, serving.

## Data engineer ≠ data architect

Chapter 2 is explicit that the data engineer is not the same as the data architect — usually these are two roles. When a data engineer works alongside a data architect, the engineer should be able to **deliver on the architect's designs and provide architectural feedback** (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

## Chapter 3: the working definition

Reis and Housley synthesise TOGAF, DAMA, and their own experience into this definition (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md):

> **Data architecture is the design of systems to support the evolving data needs of an enterprise, achieved by flexible and reversible decisions reached through a careful evaluation of trade-offs.**

This parallels their definition of enterprise architecture, substituting "data needs" for "systems to support change." Data architecture is a **subset of enterprise architecture** — it inherits the parent discipline's properties (processes, strategy, change management, technology) and applies them specifically to data (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md).

**Data engineering architecture** is a further subset: the systems and frameworks that make up the key sections of the [[data-engineering-lifecycle]]. Chapter 3 uses *data architecture* and *data engineering architecture* interchangeably.

## Operational vs technical

Chapter 3 splits data architecture into two dimensions (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md):

- **Operational architecture** — the functional requirements around people, processes, and technology. *What* business processes does the data serve? How is [[data-quality]] managed? What is the latency requirement from production to query?
- **Technical architecture** — *how* data is ingested, stored, transformed, and served along the lifecycle. For instance, how to move 10 TB/hour from a source database to the data lake.

Operational says *what needs to be done*; technical says *how it happens*. Both matter.

## "Good" data architecture

Richards and Ford's "[[architecture-characteristics|never shoot for the best architecture, but rather the least worst architecture]]" is quoted directly (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md). Reis and Housley's gloss:

> Good data architecture serves business requirements with a common, widely reusable set of building blocks while maintaining flexibility and making appropriate trade-offs. Bad architecture is authoritarian and tries to cram a bunch of one-size-fits-all decisions into a big ball of mud.

Grady Booch's formulation is also cited: "architecture represents the significant design decisions that shape a system, where significant is measured by cost of change" — connecting directly to [[cost-of-change]] and [[reversible-vs-irreversible-decisions]] (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md).

Good data architecture is:

- **Agile** — acknowledging the world is fluid; evolves with business and technology change
- **Flexible and maintainable** — reversibility is the core property (see [[reversible-vs-irreversible-decisions]])
- **Loosely coupled** — not tightly coupled, rigid, or overly centralised
- **Using the right tools for the job** — not a single hammer applied to every nail
- **Living** — never finished; change and evolution are central to the meaning of the discipline

This is [[evolutionary-architecture]] applied to data.

## Architecture vs tools (Chapter 4)

Chapter 4 opens by separating architecture from technology (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

> Architecture is the top-level design, roadmap, and blueprint of data systems that satisfy the strategic aims for the business. Architecture is the what, why, and when. Tools are used to make the architecture a reality; tools are the how.

Teams that pick tools before architecture build "Dr. Seuss fantasy machines." The corrective: **architecture first, technology second.** See [[technology-selection]] for the tactical framework Chapter 4 provides for the second step.

The architecture/tools split also names the scope of architectural decisions: [[principles-of-good-data-architecture|the nine principles]] govern architecture; Chapter 4's ten criteria govern tool choice within that architecture.

## Hard Parts Ch 14 — analytical data in distributed architectures

*Software Architecture: The Hard Parts* Ch 14 frames analytical data as a **cross-cutting concern every decomposed architecture has to solve** (source: raw/software-architecture-the-hard-parts/chapter-14-managing-analytical-data.md). It walks the historical progression — [[data-warehousing|data warehouse]] → [[data-lake|data lake]] → [[data-mesh]] — through an architect's lens, focusing on how each pattern handles domain partitioning.

Ch 14's architectural verdict:

- **Warehouse and lake partition technically** (ingest / transform / load / serve), which works against the domain partitioning modern distributed architectures (microservices) depend on.
- **Data mesh preserves domain partitioning** by putting the analytical interface — the [[data-product-quantum]] — inside the domain boundary, alongside the operational service.

This adds a specifically architectural take on the patterns Reis & Housley's Chapter 3 introduces, and makes explicit the link between microservices-style domain decomposition and the data-mesh approach to analytics.

## What Chapter 3 covers (index)

- [[principles-of-good-data-architecture]] — the nine principles, borrowing from AWS Well-Architected and Google Cloud's five cloud-native principles
- [[well-architected-framework]] — the AWS six-pillar framework
- [[cloud-native-principles]] — Google Cloud's five cloud-native principles
- [[data-architect]] — the role and its relationship to the data engineer
- Architecture patterns covered in depth: [[data-warehousing]], [[data-lake]], [[data-lakehouse]], [[modern-data-stack]], [[lambda-architecture]], [[kappa-architecture]], [[dataflow-model]], [[iot-architecture]], [[data-mesh]]

## Related pages

- [[data-engineering-lifecycle]]
- [[data-engineer]]
- [[data-architect]]
- [[principles-of-good-data-architecture]]
- [[reversible-vs-irreversible-decisions]]
- [[trade-off-analysis]]
- [[evolutionary-architecture]]
- [[lambda-architecture]]
- [[unbundling-databases]]
- [[fundamentals-of-software-architecture]]
- [[architecture-characteristics]]
- [[technology-selection]]
- [[data-mesh]]
- [[data-product-quantum]]
- [[software-architecture-the-hard-parts]]
