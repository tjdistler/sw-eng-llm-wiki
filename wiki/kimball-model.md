# Kimball Model

**Summary**: Ralph Kimball's early-1990s alternative to [[inmon-model|Inmon]]: model department- or business-facing analytics directly in the data warehouse using **facts** ([[fact-table|quantitative events]]) surrounded by **dimensions** ([[dimension-table|descriptive attributes]]) in a [[star-schema]]. Bottom-up, faster to iterate, accepts duplication and denormalization as the price of accessibility.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md`

**Last updated**: 2026-04-18

---

## The shape

Two table types, one arrangement:

- **[[fact-table|Fact tables]]** — narrow and long; immutable, append-only rows representing business events (orders, clicks, sales). All numeric; foreign keys pointing to dimensions.
- **[[dimension-table|Dimension tables]]** — wide and short; descriptive attributes of the things facts refer to (customers, products, dates, stores). Denormalized, duplication permitted.

Arranged as a **[[star-schema|star schema]]**: one fact table in the centre, dimension tables radiating out. A business often has multiple stars, one per fact domain.

See [[star-schema]], [[fact-table]], [[dimension-table]], [[slowly-changing-dimensions]].

## What makes it "bottom-up"

Inmon integrates everything into a 3NF warehouse first, then projects to department marts. Kimball skips the intermediate integration tier: you model department or business analytics directly in the warehouse, one star schema per fact domain (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).

Trade-offs:

- **Faster iteration** — you don't need to design the enterprise 3NF model before delivering a report.
- **Easier for business users** — a star schema with named dimensions is immediately legible.
- **Potential looser integration** — duplicated dimension logic across stars, unless controlled via **conformed dimensions**.
- **Data redundancy** — denormalized by design.

## Conformed dimensions

A **conformed dimension** is one reused across multiple star schemas — same keys, same attributes. Conformed dimensions are what let you combine fact tables from different stars: a `dim_date` shared by `fact_sales` and `fact_web_events` lets you compare the two. Avoid replicating the same dimension table under different names — that's the path to drifting business definitions (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).

## Grain

Fact tables should be at the **lowest grain possible** — each row represents one event, not a pre-aggregation. Aggregations belong in downstream queries, marts, or views. Kimball's grain rule aligns with the general modeling rule from [[conceptual-logical-physical-models]]: you can always aggregate up but you can't recover detail you discarded.

## When Kimball fits

- Analytics workloads where business users run the queries (star schemas are legible).
- Workloads dominated by a handful of high-volume fact types (sales, web events, orders).
- Environments where the cost of duplicated dimension data is acceptable.

## When it doesn't

Kimball was designed for **batch** data. Reis & Housley explicitly say the star schema is "appropriate only for batch data and not for streaming data" — translating SCD Type 2 maintenance to a continuous stream would overwhelm the warehouse (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md). See [[streaming-data-modeling]].

## Canonical reference

- Kimball & Ross, *The Data Warehouse Toolkit* (Wiley).

## Cross-book connections

- [[data-warehousing]] — DDIA's star/snowflake schema treatment sits entirely within this tradition.
- [[stream-joins]] — DDIA describes SCD Type 2 as the standard technique for making stream-to-table joins deterministic under slowly changing lookup state.

## Related pages

- [[star-schema]]
- [[snowflake-schema]]
- [[fact-table]]
- [[dimension-table]]
- [[slowly-changing-dimensions]]
- [[inmon-model]]
- [[data-vault]]
- [[data-warehousing]]
- [[data-mart]]
