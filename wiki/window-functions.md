# Window Functions

**Summary**: SQL operators that compute a value for each row based on a **window** of related rows — rank, running total, lead/lag — without collapsing the rows into a group. Reis & Housley list them alongside CTEs, subqueries, and UDFs as one of the core query patterns every data engineer should have at hand.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md`

**Last updated**: 2026-04-18

---

## What they do

A window function computes a value for each row using a window — a set of rows related to the current row. Unlike `GROUP BY` aggregations, which collapse the rows, a window function preserves every row and attaches the computed value to it.

Typical uses: running totals, moving averages, rank within a partition, percentile, first/last/lead/lag values within a session.

Syntax is `function(...) OVER (PARTITION BY ... ORDER BY ... ROWS BETWEEN ...)`.

## Why they matter in analytics

Reis & Housley treat window functions as one of the **query patterns** a data engineer should know well (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md). Their value: a great deal of analytics logic — sessionisation, cohort statistics, top-N-per-group, change-over-time, YoY — can be expressed in a single declarative query instead of a multi-stage procedural script.

Because window logic is declarative, the [[query-optimizer]] can reason about it and push work into the engine's native parallel-processing primitives. Re-implementing the same logic with `JOIN`s or procedural Python is usually slower and less readable.

## Relationship to streaming windows

The word "window" is overloaded. A SQL window function operates on a row-aware partition inside a single query, at query time. A [[windowing|streaming window]] (tumbling, sliding, session) is a completeness boundary for aggregation over an unbounded event stream. Both answer "compute something relative to a set of related rows" but the machinery is entirely different.

## Related pages

- [[query-performance-tuning]]
- [[query-optimizer]]
- [[common-table-expression]]
- [[windowing]]
- [[declarative-vs-imperative-queries]]
