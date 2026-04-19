# Normalization Levels

**Summary**: The sequence of **normal forms** — denormalized, 1NF, 2NF, 3NF, and beyond — that formalize how a relational schema eliminates redundancy and update anomalies. Reis & Housley summarize the first three; a database is conventionally considered "normalized" when it reaches 3NF.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md`

**Last updated**: 2026-04-18

---

## Codd's four objectives

Edgar Codd introduced normalization in the early 1970s with four stated goals (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md):

1. Free the relations from undesirable insertion, update, and deletion dependencies.
2. Reduce the need for restructuring the relations as new types of data are introduced, increasing the lifespan of application programs.
3. Make the relational model more informative to users.
4. Make the relations neutral to query statistics, which change over time.

He then defined **normal forms** — sequential conditions, each incorporating the previous ones.

## The forms

| Form | Condition |
|---|---|
| **Denormalized** | No normalization. Nested and redundant data allowed. |
| **1NF** | Each column is unique and has a single value. The table has a unique primary key (simple or composite). No repeating groups or nested structures. |
| **2NF** | 1NF, plus **no partial dependencies** — a non-key column cannot depend on a subset of a composite primary key. (Only applies when the primary key is composite.) |
| **3NF** | 2NF, plus **no transitive dependencies** — a non-key column cannot depend on another non-key column. |

(source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md)

Higher forms exist (BCNF, 4NF, 5NF, 6NF in the Boyce-Codd system) but Reis & Housley call them "much less common" in practice. 3NF is the de facto ceiling for most workloads.

## Glossary

Two terms to unpack:

- **Partial dependency.** A subset of fields in a composite key determines a non-key column. Example: if `(OrderID, LineItemNumber)` is the key but `CustomerName` is determined by `OrderID` alone, that's a partial dependency — `CustomerName` belongs in an `Orders` table keyed by `OrderID`.
- **Transitive dependency.** A non-key column depends on another non-key column. Example: in an `OrderLineItem` table keyed by `(OrderID, LineItemNumber)`, if `ProductName` is determined by `SKU` (another non-key column), `ProductName` transitively depends on the key via `SKU`. Resolution: split `SKU → ProductName` into its own table.

(source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md)

## Worked example (Chapter 8 summary)

Starting from a denormalized `OrderDetail` table with a nested `OrderItems` array:

1. **→ 1NF**: Flatten the array. Each line item becomes its own row. Primary key becomes composite `(OrderID, LineItemNumber)`.
2. **→ 2NF**: Customer fields depend only on `OrderID`, not on the full composite key. Split into `Orders` (keyed by `OrderID`) and `OrderLineItem` (keyed by `(OrderID, LineItemNumber)`).
3. **→ 3NF**: In `OrderLineItem`, `ProductName` depends on `SKU`, which is a non-key. Split `SKU → ProductName` into a `Skus` table.

## When to stop

"The degree of normalization that you should apply to your data depends on your use case. No one-size-fits-all solution exists, especially in databases where some denormalization presents performance advantages" (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).

In practice:

- OLTP systems target 3NF for correctness under concurrent writes.
- OLAP systems ([[star-schema|star-schema]] / [[wide-denormalized-table|wide tables]]) deliberately **denormalize** for read performance.
- Semistructured stores ([[nested-data]], [[document-model]]) skip classical normalization entirely in favour of document locality.

## Cross-book connections

- [[normalization]] — DDIA's shorter framing of the same idea: store human-meaningful info once, reference by ID.
- [[object-relational-mismatch]] — one of the forces that pushed document stores to relax normalization.

## Related pages

- [[normalization]]
- [[relational-model]]
- [[data-modeling]]
- [[conceptual-logical-physical-models]]
- [[star-schema]]
- [[wide-denormalized-table]]
