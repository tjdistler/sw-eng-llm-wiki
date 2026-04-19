# Materialized View

**Summary**: A view whose result is **precomputed and stored**, refreshed when underlying data changes. Combines the composability of a SQL view with the query performance of a table. Reis & Housley treat materialized views as a first-class transformation primitive and a form of query caching — and note that [[query-optimizer|query optimizers]] can sometimes rewrite arbitrary queries to use them.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md`

**Last updated**: 2026-04-18

---

## View vs materialized view

A plain **view** is a saved query. When you `SELECT` from it, the engine combines the view's subquery with your query and the [[query-optimizer|optimizer]] runs the result. Every select re-executes the underlying work (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).

A **materialized view** does some or all of that work **in advance**. When source data changes, the engine updates the stored result. When a user selects from the view, they're reading the precomputed data.

## What views are good for

Reis & Housley enumerate three roles for plain views (still useful even without materialization) (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md):

1. **Security.** Expose only specific columns and filtered rows to a given role. Different views per job function.
2. **Deduplication.** On an [[insert-only]] table, a view can return the latest version per key.
3. **Common access patterns.** Pre-joined wide view over five tables that analysts can filter and aggregate on.

Materialized views extend all three with performance.

## Optimizer rewriting

Many optimizers can identify queries that "look like" a materialized view and rewrite them to select from the precomputed result — **even if the user's query doesn't reference the view directly** (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).

An analyst writing an ad-hoc filter that happens to match a materialized view's filter benefits automatically. This turns materialized views into a form of **implicit cache** that the optimizer manages on the analyst's behalf.

## Composition and live tables

Historically materialized views do **not** support composition — a materialized view cannot select from another materialized view. Tools are emerging to change that:

- **Databricks live tables** — each table updated as data arrives from sources; data flows down to subsequent tables asynchronously (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).
- **[[dbt]] incremental models** — approximate the pattern procedurally.

Live tables essentially make materialized views into a first-class DAG primitive — the transformation DAG and the materialization DAG become the same thing.

## Relationship to other primitives

- **Query caching.** Materialized views are a form of query cache where the engine refreshes based on changes to sources rather than time-to-live. Many cloud warehouses have both.
- **[[update-patterns|Upserts]].** A materialized view refresh is, under the hood, a merge against the stored result.
- **[[stream-joins|Stream-table joins]].** In DDIA's framing, a materialized view fed by CDC is equivalent to maintaining a table via stream-table join.

## Cross-book connections

- [[materialized-state]] — DDIA's general framing of precomputed views over streams.
- [[stream-joins]] — table-table joins produce materialized-view updates.
- [[derived-data]] — materialized views are one instance of derived data.

## Related pages

- [[query-optimizer]]
- [[query-performance-tuning]]
- [[update-patterns]]
- [[derived-data]]
- [[materialized-state]]
- [[federated-query]]
- [[data-virtualization]]
