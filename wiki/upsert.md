# Upsert

**Summary**: An [[update-patterns|update pattern]] that takes source records, matches them to a target table by primary key or logical condition, **updates** on match and **inserts** on no-match. **Merge** extends upsert to also delete. Reis & Housley: the most-troubled pattern when engineers move from row-based to columnar warehouses.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md`

**Last updated**: 2026-04-18

---

## The operation

```sql
MERGE INTO target AS t
USING source AS s
ON    t.id = s.id
WHEN MATCHED        THEN UPDATE SET ...
WHEN NOT MATCHED    THEN INSERT (...) VALUES (...)
-- merge also supports WHEN MATCHED THEN DELETE
```

The engineer is responsible for **managing the primary key** by running appropriate queries — most columnar systems don't enforce uniqueness. If duplicates land in the source, merge will produce unexpected behaviour.

## Why it was easy, why it isn't now

In row-based databases, update is natural: the engine looks up the row and changes it in place. Upsert/merge composes cheap primitives.

In file-based columnar systems (lakes, lakehouses, cloud warehouses), files are immutable. Every update requires rewriting files via **[[update-patterns#copy-on-write|copy-on-write (COW)]]**. A single-row update can trigger a multi-megabyte file rewrite.

This is why the early data lake community rejected updates entirely and went [[insert-only|insert-only]], leaving "current state" as a query-time problem.

## The performance shape

- **Large merge sets** are extremely performant in columnar systems — sometimes outperforming transactional databases at equivalent scale.
- **Small merge sets** are disproportionately expensive — updating five rows might rewrite a whole partition.
- **COW resolution matters.** Depending on the system, COW operates at partition / cluster / block granularity. Good partitioning and clustering strategy is what makes merges performant (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).

## The CDC-merge anti-pattern

"We've seen many engineering teams transition between database systems and try to run near real-time merges from CDC just as they did on their old system. It simply doesn't work."

Near-real-time merges from [[change-data-capture|CDC]] will bring most columnar warehouses to their knees. Every event → one merge → one file rewrite. Teams have seen systems fall weeks behind on updates (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).

Better patterns:

- **Batch the merges.** Hourly merges are usually fine where per-minute merges are catastrophic.
- **Use engine-specific near-real-time features.** BigQuery streaming inserts + deduplicating materialized views; Druid two-tier storage; similar features in Snowflake and others.
- **Combine insert-only + view.** Append every CDC event to an insert-only table, present current state via a view or materialized view.

## Cross-book connections

- [[change-data-capture]] — FoDE Ch 7 explicitly warns about the source-resource cost of continuous CDC; that warning compounds with the merge-frequency warning here on the consumer side.
- [[lakehouse-table-formats]] — Delta, Iceberg, Hudi implement efficient merge-on-read and copy-on-write so the lake can support upsert semantics without a separate warehouse.

## Related pages

- [[update-patterns]]
- [[insert-only]]
- [[change-data-capture]]
- [[lakehouse-table-formats]]
- [[materialized-view]]
- [[query-performance-tuning]]
