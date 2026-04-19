# Query Optimizer

**Summary**: The component of a database engine that translates a declarative SQL query into an efficient execution plan. Reis & Housley frame the optimizer as the thing you don't directly work with but absolutely must understand if you want performant queries — every database's optimizer is different, and writing good SQL is largely a conversation with the one in front of you.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md`

**Last updated**: 2026-04-18

---

## What the optimizer does

A query optimizer's job is to optimize query performance and minimize costs by breaking the query into appropriate steps in an efficient order. It assesses joins, indexes, data scan size, and other factors, and attempts to execute the query in the least expensive manner (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).

The optimizer is fundamental to how a query will perform. Every database executes queries in ways that are obviously and subtly different from each other. You won't directly write code against the optimizer, but understanding some of its functionality will help you write more performant queries (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).

## Where it fits in query execution

In [[life-of-a-query|the life of a SQL query]], the optimizer runs after parsing and bytecode conversion, before physical execution. It reorders and refactors steps to use available resources as efficiently as possible (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).

## Key optimizations

Reis & Housley call out a handful of optimizations the modern cloud-warehouse optimizer handles for you:

- **Predicate reordering.** Pushing filters before joins dramatically reduces rows entering expensive join stages. Some databases reorder joins and predicates; others don't — which is why a [[query-performance-tuning|row-explosion]] in an early stage can kill the query even when a later predicate would have filtered the result (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).
- **Join strategy selection.** The optimizer chooses between [[broadcast-join|broadcast]] and [[shuffle-hash-join|shuffle hash]] based on estimated table sizes. A filtered "large" table that becomes small enough to broadcast can switch strategies mid-plan (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).
- **Index and cluster-key use.** The optimizer decides whether a given index or cluster key applies to the predicate. Some optimizers can match functional indexes (e.g., Postgres's index on `lower(x)` — the optimizer matches `WHERE lower(x) = ...`) (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).
- **Materialized view matching.** Many optimizers can identify queries that "look like" a [[materialized-view]] and rewrite the query to select from the precomputed result, even if the query doesn't reference the view directly (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).

## EXPLAIN

The optimizer's **explain plan** shows how it determined the lowest-cost query — the database objects used (tables, indexes, cache), the sequence of steps, and resource consumption statistics per stage. Some databases expose this visually; others via the `EXPLAIN` SQL command (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).

`EXPLAIN` is the first tool to reach for when a query is slow — before throwing more compute at it.

## The Spark exception

SQL engines hand you optimization for free. Code-heavy processing frameworks like Spark push optimization back onto the engineer — you're responsible for filter placement, join reordering, and avoiding [[user-defined-function|UDFs]] that prevent the Catalyst optimizer from reasoning about your code. Intermixing SQL inside Spark jobs lets Catalyst optimize the SQL portion even when the surrounding code is native Spark (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).

## Cross-book connections

- [[declarative-vs-imperative-queries]] — DDIA's framing of why declarative languages give the database room to optimize.
- [[relational-model]] — DDIA's observation that the relational model's durability owes partly to the query optimizer being written once and reused by every application.

## Related pages

- [[life-of-a-query]]
- [[query-performance-tuning]]
- [[broadcast-join]]
- [[shuffle-hash-join]]
- [[materialized-view]]
- [[declarative-vs-imperative-queries]]
- [[user-defined-function]]
