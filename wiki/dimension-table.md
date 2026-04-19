# Dimension Table

**Summary**: In a [[kimball-model|Kimball]] [[star-schema]], the reference tables that provide **attributes, descriptions, and context** for events in a [[fact-table]]. Smaller than fact tables, wider, short. Denormalized — duplication permitted. Tracking changes over time uses [[slowly-changing-dimensions|Slowly Changing Dimension (SCD)]] patterns.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md`, `raw/designing-data-intensive-applications/chapter-03-storage-and-retrieval.md`

**Last updated**: 2026-04-18

---

## Purpose

Where the [[fact-table]] captures the *what happened*, dimensions capture the *who / what / where / when / how / why* (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).

Common dimensions: `dim_customer`, `dim_product`, `dim_date`, `dim_store`, `dim_promotion`, `dim_employee`.

## Shape

- **Wide.** Many descriptive attributes per row (dozens of columns is normal).
- **Short.** Millions of rows typical, not billions.
- **Denormalized.** Attributes that could live in separate reference tables often stay flat — brand name, category name, region name inline in the product dimension. Duplication is OK in the Kimball tradition.
- **Surrogate key.** A meaningless integer (`customer_sk`) is the primary key; the source system's natural key (`customer_id`) is just another attribute. Surrogate keys decouple the warehouse from source-system ID changes and enable SCD versioning.

## The date dimension special case

A `dim_date` has one row per calendar date and any attributes you care to attach: day-of-week, is-holiday, fiscal-quarter, ISO week number, Black-Friday-flag. With `dim_date` you can answer "how many more customers shop on Tuesday than Wednesday?" with a trivial join (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).

## Conformed dimensions

A **conformed dimension** is one reused across multiple star schemas. A single `dim_date` or `dim_customer` joined to both `fact_sales` and `fact_web_events` lets you combine those domains. Conformed dimensions are the integration glue of a Kimball warehouse (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).

Avoid the anti-pattern of replicating the same dimension under different names in different stars — that's how business definitions drift.

## Changes over time: SCD

Dimension attributes change: customers move, products get renamed, employees change departments. The family of [[slowly-changing-dimensions|Slowly Changing Dimension (SCD) patterns]] answers the question "how do we want historical facts to see historical dimension state?"

Reis & Housley cover Type 1 (overwrite — history lost), Type 2 (new row per change — full history, effective-start/end dates), and Type 3 (new column per change). Type 2 is most common in practice.

## Cross-book connections

- [[stream-joins]] — DDIA notes SCD Type 2 as the standard way to make stream-to-table joins deterministic under slowly changing lookup data; giving each dimension version its own key makes replay reproducible.

## Related pages

- [[fact-table]]
- [[star-schema]]
- [[slowly-changing-dimensions]]
- [[kimball-model]]
- [[data-warehousing]]
