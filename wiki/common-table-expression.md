# Common Table Expression

**Summary**: A SQL feature (`WITH ... AS`) that names an intermediate query result and composes it into a larger query. Reis & Housley prescribe CTEs over nested subqueries and temp tables as a first-line readability and performance improvement.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md`

**Last updated**: 2026-04-18

---

## What a CTE is

A Common Table Expression (CTE) is a SQL construct that names an intermediate result in a query and lets you reference it later. Syntactically it's the `WITH name AS (SELECT ...)` clause that precedes a `SELECT` statement.

## Why Reis & Housley prefer it

Chapter 8 prescribes CTEs instead of nested subqueries or temporary tables for three reasons (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md):

1. **Readability.** Composing complex queries with named intermediate results reads top-to-bottom rather than inside-out. "The importance of readability for complex queries cannot be understated."
2. **Performance vs scripts.** In many cases, CTEs deliver better performance than a script that materialises intermediate tables. If you *must* materialise, prefer temporary tables over permanent ones.
3. **DAG composition in SQL.** SQL is often dismissed for not being procedural — but CTEs plus SQL scripts or an orchestrator let you build complex DAGs of data transformations entirely in declarative SQL. The [[query-optimizer|optimizer]] sees the whole DAG at once.

## In the transformation layer

CTEs are a primitive inside tools like [[dbt]], which compile Jinja-templated SQL with CTEs into warehouse-native DAGs. The metrics-layer / semantic-layer tooling Reis & Housley mention in the undercurrents leans heavily on CTE-based composition.

## Related pages

- [[query-performance-tuning]]
- [[query-optimizer]]
- [[declarative-vs-imperative-queries]]
- [[dbt]]
