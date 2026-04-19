# Wide Denormalized Table

**Summary**: A modeling style for columnar cloud warehouses: one very wide table (hundreds to thousands of columns, often with [[nested-data|nested fields]]) that encodes facts and dimensions together. Removes joins at query time. Enabled by cheap cloud storage and columnar storage's cheap handling of null cells and schema evolution.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md`

**Last updated**: 2026-04-18

---

## The shape

A wide denormalized table is what it sounds like:

- **Many columns** — often thousands.
- **Highly denormalized** — no separate dimension tables to join; descriptive attributes are inline.
- **Sparse** — the vast majority of entries in any given column may be null. That's fine in a columnar store (nulls take essentially zero space).
- **Nested fields allowed** — a column may hold a struct or an array; see [[nested-data]].
- **Organized along one or more keys** closely tied to the grain.

## Why this is now reasonable

In an RDBMS, a wide table is expensive. Each row allocates space for every column whether populated or not, and reads traverse that entire allocation. Schema evolution is slow and resource-heavy.

In a [[column-oriented-storage|columnar database]], the economics flip (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md):

- **Selective reads.** A query reads only the columns it references, so wide doesn't mean slow.
- **Null cells are free.** No storage allocated for empty values.
- **Schema evolution is a metadata change.** Adding a column touches the metadata, not existing files. New data gets files for the new column.

Combined with cheap cloud storage, this means the traditional cost model for denormalization — duplicated data = wasted disk, wasted scan time — no longer applies.

## The analytics argument

"Analytics queries on wide tables often run faster than equivalent queries on highly normalized data requiring many joins. Removing joins can have a huge impact on scan performance" (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).

For reporting and dashboards over moderately sized data, a wide table is often simpler *and* faster than a [[star-schema|Kimball star]].

## The criticisms

- **Business logic gets lost.** When facts and dimensions are blended, the explicit modeling of the business is gone. What does "customer" mean? Without a `dim_customer`, the definition is implicit in the column set.
- **Updates to nested elements are painful.** Changing one element inside an array field typically requires rewriting the whole row (the [[update-patterns|copy-on-write]] cost, multiplied by array size).
- **Schema evolution becomes its own problem.** Wide tables typically arise through schema evolution over time; without governance, the column set drifts toward incoherence.

## When to use

Reis & Housley's guidance (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md):

> Use a wide table when you don't care about data modeling, or when you have a lot of data that needs more flexibility than traditional data-modeling rigor provides.

Particularly relevant for:

- **High-volume transactional or event data** that arrives in nested formats (web events, IoT, mobile telemetry).
- **[[streaming-data-modeling|Streaming data modeling]]**, where schemas change on a whim and the rigid Kimball approach doesn't fit.
- **Rapid prototyping** of analytics where modeling rigour would slow delivery.

See also [[one-big-table]] (the OBT modeling approach that takes this pattern to its logical extreme).

## Related pages

- [[one-big-table]]
- [[nested-data]]
- [[column-oriented-storage]]
- [[star-schema]]
- [[streaming-data-modeling]]
- [[schema-evolution]]
- [[data-modeling]]
