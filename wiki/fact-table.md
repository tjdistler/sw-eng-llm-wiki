# Fact Table

**Summary**: In a [[kimball-model|Kimball]] [[star-schema]], the central table holding **factual, quantitative, event-related data** — one row per business event (sale, click, shipment). Narrow and long, immutable and append-only, all numeric. References [[dimension-table|dimension tables]] for context.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md`, `raw/designing-data-intensive-applications/chapter-03-storage-and-retrieval.md`

**Last updated**: 2026-04-18

---

## Defining characteristics

Chapter 8's rules for fact tables (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md):

- **Immutable.** Facts relate to events, which don't change after they happen. Fact tables are **append-only**.
- **Narrow and long.** Few columns (keys + measures), many rows (billions is normal).
- **Numeric data types only.** Integers, floats, decimals. No strings — strings live in dimensions.
- **One row = one event at the grain.** Grain is whatever unit the business tracks (customer-order, line-item, click, sensor reading). Each row represents exactly that.
- **No aggregation or derivation.** Don't pre-aggregate in the fact table. Do that in a downstream query, mart table, or view.
- **No fact-to-fact references.** Fact tables reference only dimensions, never other fact tables.

## Anatomy

A typical fact table has three kinds of columns:

- **Surrogate keys** — foreign keys to dimension tables (`customer_sk`, `product_sk`, `date_key`).
- **Degenerate dimensions** — keys that identify the event but have no dimension table (e.g., `order_id` used as grain marker).
- **Measures** — the numeric quantities being counted or summed (`quantity`, `gross_amount`).

## The grain rule

"Fact tables should be at the lowest grain possible" (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md). You can always aggregate to a coarser grain; you cannot recover detail you didn't store. The grain rule is the single most consequential modeling decision for a fact table — it determines what questions the warehouse can answer.

See [[conceptual-logical-physical-models|grain discussion]] for the full argument.

## Types of fact tables (Kimball tradition)

Reis & Housley don't go deep here, but the Kimball tradition names three forms:

- **Transaction fact table** — one row per event. The default.
- **Periodic snapshot** — state at regular intervals (inventory level at end of day).
- **Accumulating snapshot** — one row per workflow instance, updated as the workflow progresses (an order going through pick → pack → ship → deliver).

## Query pattern

A typical warehouse query starts at the fact table and joins outward to dimensions (source: raw/designing-data-intensive-applications/chapter-03-storage-and-retrieval.md):

```sql
SELECT d.weekday, p.category, SUM(s.quantity)
FROM   fact_sales s
JOIN   dim_date    d ON s.date_key   = d.date_key
JOIN   dim_product p ON s.product_sk = p.product_sk
GROUP BY d.weekday, p.category
```

Because fact tables are so large and dimensions so small, this pattern pairs naturally with [[column-oriented-storage]] (scan only the fact columns you need) and [[broadcast-join]] (dimensions small enough to ship to every node).

## Cross-book connections

- [[data-warehousing]] — DDIA's standard treatment of fact/dimension tables.

## Related pages

- [[dimension-table]]
- [[star-schema]]
- [[kimball-model]]
- [[column-oriented-storage]]
- [[broadcast-join]]
