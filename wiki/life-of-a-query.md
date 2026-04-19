# Life of a Query

**Summary**: Reis & Housley's four-phase narrative for what happens when you press Execute on a SQL statement: parse, compile to bytecode, optimize, execute. Running a query "might seem simple — write code, run it, get results — [but] a lot is going on under the hood."

**Sources**: `raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md`

**Last updated**: 2026-04-18

---

## The four phases

When you execute a SQL query, this is roughly what a database does (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md):

1. **Parse and validate.** The engine compiles the SQL, parsing the code to check semantics, verify that referenced database objects exist, and confirm the current user has access to them.
2. **Compile to bytecode.** The SQL is converted into an efficient, machine-readable format that expresses the steps the engine must execute.
3. **Optimize.** The [[query-optimizer]] analyzes the bytecode to determine how to execute the query, reordering and refactoring steps to use available resources as efficiently as possible.
4. **Execute.** The engine runs the chosen plan and produces results.

## Why this matters for the data engineer

You won't reach into any of these phases directly — but understanding what the engine is doing clarifies what can and can't be fixed from the SQL side:

- **Parsing errors** come from syntax or permission issues. See [[data-security]]: access-control errors show up here as "object does not exist."
- **Bytecode-level inefficiencies** are mostly invisible.
- **Optimizer decisions** are the big lever. `EXPLAIN` shows the plan the optimizer chose; rewriting the query or adding indexes/cluster keys changes the plan.
- **Execution-time bottlenecks** show up in the metrics you monitor: disk/memory/network, rows scanned, bytes shuffled, concurrent connections.

See [[query-performance-tuning]] for the lever set.

## Related languages around the query

Reis & Housley take the opportunity to re-enumerate the SQL sublanguages that sit around query execution (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md):

- **DDL (Data Definition Language)** — `CREATE`, `DROP`, `ALTER`. Defines the state of database objects.
- **DML (Data Manipulation Language)** — `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `COPY`, `MERGE`. Adds and alters data inside those objects.
- **DCL (Data Control Language)** — `GRANT`, `DENY`, `REVOKE`. Controls access to objects.
- **TCL (Transaction Control Language)** — `COMMIT`, `ROLLBACK`. Controls transaction boundaries.

A query is a DML operation. The life-of-a-query story is about what happens when a DML `SELECT` (or `INSERT`/`UPDATE`/etc.) runs.

## Related pages

- [[query-optimizer]]
- [[query-performance-tuning]]
- [[crud]]
- [[declarative-vs-imperative-queries]]
- [[transactions]]
