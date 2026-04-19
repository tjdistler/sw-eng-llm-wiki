# Nested Data

**Summary**: Structs, arrays, and maps stored directly in a column — the semistructured-data escape hatch that modern cloud warehouses (BigQuery, Snowflake, Redshift) borrowed from document stores. Reis & Housley treat nested data as a first-class ingredient of the "wide denormalized table" pattern and the main reason rigid star-schema modeling has softened.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md`

**Last updated**: 2026-04-18

---

## Three shapes

- **Struct** — a named set of fields, addressed by dotted path (`address.zip`).
- **Array** — an ordered list; addressed by index or by `UNNEST`/`EXPLODE` to rows.
- **Map** — key-value pairs; sometimes unified with struct semantics.

A single column can hold deeply nested JSON — an array of structs of arrays — and the query engine lets SQL reach into it without flattening to tables first.

## Why it changed the modeling game

Pre-cloud-warehouse, nested data was the domain of document stores. Loading it into a warehouse meant flattening into normalized rows, losing locality, and paying the join cost on every read.

Modern cloud warehouses encode nested data as a first-class type. That breaks the old constraint and drives three patterns Chapter 8 names (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md):

1. **[[wide-denormalized-table|Wide denormalized tables]]** with nested fields replace frequently-joined entity relationships. Facts and dimensions can live in the same table.
2. **Schema evolution becomes cheaper.** In a columnar warehouse, adding a field is a metadata change — data for old rows is simply null. A nested struct absorbs new sub-fields without a rewrite.
3. **Raw-JSON-in-a-field with adjacent flattened columns** — a pattern that keeps the raw payload (from a frequently-changing document source) while exposing the frequently-accessed fields as normal columns. New fields in the JSON can be promoted into the schema over time.

## Query primitives

- `UNNEST` / `EXPLODE` — turn an array into rows. Essential for computing per-element aggregates.
- Dotted access — `SELECT order.customer.email FROM ...`.
- JSON functions — `JSON_EXTRACT`, `JSON_VALUE` for raw JSON stored in a string column.

## The CDC / streaming angle

Streaming and [[change-data-capture|CDC]] payloads are overwhelmingly semistructured. Making nested data first-class in the warehouse means CDC can land payloads without an upstream flattening pipeline. Reis & Housley note that with [[streaming-data-modeling|streaming data modeling]] still an unsettled art, **flexible schemas backed by nested columns** are the emerging answer for landing streams in analytical stores (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).

## Cross-book connections

- [[document-model]] — the DDIA framing of nested/tree-shaped data; the document model's natural locality is what nested columns inherit.
- [[schema-on-read-vs-write]] — nested-columns-plus-raw-JSON is the practical compromise between the two extremes.
- [[wide-column-database]] — different concept; a wide-column DB is a single-index KV store with many columns, not an arbitrarily nested type system.

## Related pages

- [[wide-denormalized-table]]
- [[streaming-data-modeling]]
- [[document-model]]
- [[schema-on-read-vs-write]]
- [[schema-evolution]]
