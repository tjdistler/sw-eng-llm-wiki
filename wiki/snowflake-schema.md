# Snowflake Schema

**Summary**: A normalized variant of the [[star-schema]]: dimension tables reference further sub-dimension tables rather than storing denormalized attribute text. More storage-efficient and consistency-preserving than a star, but harder for analysts to navigate. Generally not preferred in practice.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md`, `raw/designing-data-intensive-applications/chapter-03-storage-and-retrieval.md`

**Last updated**: 2026-04-18

---

## Shape

Instead of a `dim_product` table with brand and category columns:

```
dim_product (
  product_sk,
  name,
  brand_sk       -- FK to dim_brand
  category_sk,   -- FK to dim_category
  ...
)
```

Dimensions normalize into sub-dimensions, and the join graph now branches.

## Trade-offs vs star

| Axis | Snowflake | Star |
|---|---|---|
| Storage | Smaller (no duplication of brand/category text) | Larger |
| Join cost | More joins per query | Fewer joins |
| Consistency | Single source for each attribute | Duplication may drift |
| Analyst usability | Harder — more tables to navigate | Simpler — one hop from fact to attribute |
| Schema evolution | Localized change | Ripple through denormalized rows |

## Why stars win in practice

Modern columnar warehouses make the "duplication" concern cheap: storage is inexpensive and column compression collapses repeated values. The *analyst usability* gap persists, and is the deciding factor for most teams (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).

Snowflake schemas still appear in environments where:

- Dimensions are extremely wide and the brand/category pattern matters for storage.
- Consistency enforcement is required (single source for a reference table).
- The warehouse is strongly [[inmon-model|Inmon]]-style — integration via normalization is already the governing principle.

## Not to be confused with

**Snowflake** the company (a cloud data warehouse) is unrelated to the snowflake schema. Different snowflake.

## Related pages

- [[star-schema]]
- [[fact-table]]
- [[dimension-table]]
- [[kimball-model]]
- [[normalization-levels]]
- [[data-warehousing]]
