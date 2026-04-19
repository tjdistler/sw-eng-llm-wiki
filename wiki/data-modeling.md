# Data Modeling

**Summary**: The process of converting raw data into a usable form for business analytics and data science. A facet of [[data-management]] and a recurring activity across the [[data-engineering-lifecycle]] — especially during [[data-transformation|transformation]]. Chapter 2 insists that despite modern tooling making it tempting to skip modeling, doing so produces **write-once read-never (WORN)** data swamps. Chapter 8 is the deep dive, walking through [[conceptual-logical-physical-models|conceptual/logical/physical]] models, [[normalization-levels|normal forms]], and the three paradigms — [[inmon-model|Inmon]], [[kimball-model|Kimball]], [[data-vault]] — plus the emerging [[wide-denormalized-table|wide-table]] and [[streaming-data-modeling|streaming]] alternatives.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md`, `raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md`

**Last updated**: 2026-04-18

---

## What data modeling is

To derive business insights from data via analytics and data science, data must be in a usable form. The process of converting it into a usable form is data modeling and design (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

Historically thought of as the purview of DBAs and ETL developers, modeling now **happens almost anywhere** in an organisation:

- A firmware engineer designing the record format for an IoT device,
- A web application developer designing the JSON response to an API call,
- A web developer designing a MySQL table schema —

all are doing data modeling (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

## Why it's harder now

Modeling is more challenging because of the variety of new data sources and use cases. Strict normalisation doesn't work well with event data, for example.

A new generation of tools increases the flexibility of data models while retaining logical separations of **measures, dimensions, attributes, and hierarchies**. Cloud warehouses support ingestion of denormalised and semistructured data while still accommodating common patterns like **Kimball, Inmon, and data vault** modeling. Data-processing frameworks like Spark can ingest a full spectrum, from flat relational records to raw unstructured text (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

## The WORN trap

Chapter 2's warning: with the variety of data engineers must handle, there's a temptation to give up on modeling. This is a "terrible idea with harrowing consequences," made evident when people start muttering about the **write once, read never (WORN)** access pattern or a **data swamp**. Data engineers must understand modeling best practices and develop the flexibility to apply the appropriate level and type of modeling to the source and use case (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

## Chapter 8 — what a data model is

A data model represents the way data relates to the real world. It reflects how data must be structured and standardized to best reflect the organization's processes, definitions, workflows, and logic. A **good data model** captures how communication and work naturally flow within the organization; a poor or nonexistent one is haphazard, confusing, and incoherent (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).

Reis & Housley insist on one discipline above all: **translate the model to business outcomes**. A term like "customer" means different things in different departments — someone who bought in the last 30 days? The last six months? Ever? Carefully defining and modeling this has massive downstream impact on churn models and reporting.

## Chapter 8 — conceptual / logical / physical

Modeling moves from abstract to concrete along a three-level continuum — see [[conceptual-logical-physical-models]]:

- **Conceptual** — business logic, rules, entities, relationships. Visualized in ER diagrams.
- **Logical** — field types, primary and foreign keys, cardinalities.
- **Physical** — specific databases, schemas, tables, configuration.

Successful modeling involves business stakeholders **at the inception** of the process. Modeling is "a full-contact sport," not a solo DBA activity.

## Chapter 8 — grain

The **grain** of the data is the resolution at which it's stored and queried — typically at the level of a primary key (customer ID, order ID, product ID), often accompanied by a timestamp (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).

**The grain rule:** model at the lowest level of grain possible. Aggregating upward is trivial; recovering detail you've aggregated away is generally impossible. Chapter 8's worked example: responding to a "daily customer order totals" report request by still modeling the full customer-order-line detail, so the next report (with a different aggregation shape) doesn't require starting over.

See [[conceptual-logical-physical-models#grain]].

## Chapter 8 — the three batch-modeling paradigms

Three dominant approaches to modeling for data warehouses and data lakes — the book's "must-reads" are listed in each page:

- **[[inmon-model]]** — top-down, 3NF integration in the warehouse, department-specific [[data-mart|marts]] downstream. "Integration is the most important" attribute.
- **[[kimball-model]]** — bottom-up, [[fact-table|facts]] + [[dimension-table|dimensions]] in [[star-schema|star schemas]] modeled directly for business consumption. Denormalization accepted; duplication is OK.
- **[[data-vault]]** — Linstedt's insert-only, schema-stable approach using [[data-vault|hubs, links, and satellites]]. Business logic interpreted at query time, not baked into the schema.

In practice, some teams combine them — data vault as landing zone, Kimball star schema for analytics consumption.

## Chapter 8 — the "don't model" alternatives

Modern columnar warehouses and cheap cloud storage soften the rigor-or-bust choice:

- **[[wide-denormalized-table]]** — one very wide table (thousands of columns, [[nested-data|nested fields]]) replacing many joined tables. Works because columnar storage reads only selected columns and nulls are free.
- **[[one-big-table]]** — the no-modeling extreme. Query sources directly or shove everything into one table. Fast to start; Reis & Housley warn you'll eventually gravitate back to stricter modeling.

## Chapter 8 — streaming is the unsettled frontier

Batch modeling approaches don't translate to streams. See [[streaming-data-modeling]]. The emerging practice: flexible schemas, nested columns, trust source-system definitions, react to changes rather than report on them.

## Cross-book connections

- [[data-warehousing]] (DDIA) covers the **star schema / snowflake schema** patterns that dominate warehouse modeling — the most widely used of the Kimball family.
- [[data-models]] (DDIA) is the higher-level framing of relational vs document vs graph models at the storage-engine level.
- [[schema-evolution]] and [[schema-on-read-vs-write]] name the schema-change axis of modeling.
- [[domain-driven-design]] provides the service-boundary analogue in microservice decomposition.
- [[stream-joins]] (DDIA) — SCD Type 2 as the determinism technique for stream-table joins.

## Related pages

- [[conceptual-logical-physical-models]]
- [[normalization-levels]]
- [[inmon-model]]
- [[kimball-model]]
- [[data-vault]]
- [[star-schema]]
- [[wide-denormalized-table]]
- [[one-big-table]]
- [[streaming-data-modeling]]
- [[slowly-changing-dimensions]]
- [[data-transformation]]
- [[data-management]]
- [[data-warehousing]]
- [[data-models]]
- [[schema-on-read-vs-write]]
- [[schema-evolution]]
- [[normalization]]
- [[oltp-vs-olap]]
