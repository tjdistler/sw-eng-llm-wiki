# Star Schema

**Summary**: The canonical [[kimball-model|Kimball]] arrangement — a central [[fact-table|fact table]] surrounded by [[dimension-table|dimension tables]] joined by foreign keys. Fewer joins than a normalized schema, faster queries, and legible to business users. Named for the visual: fact at the centre, dimensions radiating out.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md`, `raw/designing-data-intensive-applications/chapter-03-storage-and-retrieval.md`

**Last updated**: 2026-04-18

---

## Shape

```
         dim_customer
             |
dim_date — fact_sales — dim_product
             |
         dim_store
```

The fact table is narrow (few columns beyond keys and measures), long (billions of rows), immutable and append-only. Dimensions are wider (many descriptive columns), shorter (millions at most), and may change over time via [[slowly-changing-dimensions]].

Queries start from the fact table and join outward:

```sql
SELECT d.weekday, p.category, SUM(s.quantity)
FROM   fact_sales s
JOIN   dim_date d    ON s.date_key = d.date_key
JOIN   dim_product p ON s.product_sk = p.product_sk
WHERE  d.year = 2013
GROUP BY d.weekday, p.category
```

## Why it's fast

- **Fewer joins than 3NF.** A single fact-plus-dimensions query replaces a chain of joins through normalized reference tables.
- **Narrow fact rows.** Fact tables contain only numeric measures and keys; columnar engines scan them cheaply.
- **Dimension joins are usually [[broadcast-join|broadcast]]able.** Dimensions are small enough to ship to every node.

## What the star schema should *not* be

- **Not a report.** It should capture the business's facts and attributes and be flexible enough to answer many questions — not correspond one-to-one to a specific report. Report shaping belongs in a downstream [[data-mart|data mart]] or BI tool (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).
- **Not a streaming model.** Chapter 8 explicitly says the star schema is appropriate only for batch data — Type-2 SCD maintenance under a continuous stream is impractical.

## Multiple stars and conformed dimensions

One business → typically multiple star schemas, one per fact domain (sales, web events, support tickets). Dimensions that appear across multiple stars should be **conformed dimensions**: same table, reused. A conformed `dim_date` or `dim_customer` is what lets analysts combine fact tables across domains (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).

The warning: avoid replicating the same dimension table under different names. That's the failure mode — drifting business definitions and data integrity problems.

## Star vs snowflake

A [[snowflake-schema]] is a normalized variant: dimensions are themselves broken into sub-dimensions (`dim_product → dim_brand → dim_category`). Snowflakes save storage and enforce consistency; stars are simpler for analysts. Reis & Housley's and DDIA's verdict: **stars are preferred in practice**.

## Cross-book connections

- [[data-warehousing]] — DDIA's standard treatment of the pattern.
- [[column-oriented-storage]] — the storage layout that makes fact-table scans cheap.

## Related pages

- [[fact-table]]
- [[dimension-table]]
- [[slowly-changing-dimensions]]
- [[snowflake-schema]]
- [[kimball-model]]
- [[data-warehousing]]
- [[data-mart]]
- [[column-oriented-storage]]
