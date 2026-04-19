# User-Defined Function

**Summary**: A function written in SQL or another language (Python, JavaScript, Scala, Java) that the database executes as part of a query. UDFs extend the engine's built-in functions, but Reis & Housley treat them as a **sharp tool**: a poorly written UDF can turn a minutes-long query into an hours-long one.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md`

**Last updated**: 2026-04-18

---

## Why engineers reach for UDFs

Built-in SQL functions don't cover every business rule. A UDF encapsulates a reusable piece of logic — a custom parse, a proprietary hash, a domain-specific calculation — and lets SQL invoke it directly.

Some SQL engines also support UDFs as **database objects** that can be versioned and reused, which is one of the few reusability mechanisms SQL natively offers (alongside views and materialized views) (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).

## Deterministic vs non-deterministic

A deterministic UDF returns the same output for the same input every time. A non-deterministic one doesn't (it reads the clock, calls a service, generates a random number). Determinism matters for:

- **Result caching.** Engines cache deterministic results; non-deterministic UDFs bust the cache.
- **Materialized views.** Non-deterministic UDFs can't safely participate in materialization.
- **Optimization.** The optimizer can reason about deterministic expressions (constant-fold them, move them across joins); non-deterministic ones pin the execution plan.
- **Reproducibility.** A backfill or [[reprocessing-event-streams|replay]] that invokes a non-deterministic UDF will not produce identical output.

## Cost warnings

Reis & Housley give two concrete cautions (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md):

- **Performance.** "We've seen JavaScript UDFs increase query time from a few minutes to several hours." SQL UDFs are usually fine. Non-SQL UDFs (JavaScript, Python) cross an execution boundary and defeat many optimizer rewrites.
- **PySpark UDFs in particular.** PySpark is a wrapper around Scala Spark; a Python UDF forces data out of the JVM into Python for processing. If you need a UDF, consider rewriting it in Scala/Java, or find a Spark-native way to accomplish the same thing.

## The reusability problem SQL doesn't solve

Even with UDFs, SQL lacks a natural notion of libraries or reusable code. UDFs are stored as database objects, not committed to Git without an external CI/CD system. For cross-query reuse, [[dbt]] provides templating, and orchestrators can chain table-materializing queries that downstream queries select from (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).

## The rule of thumb

Chapter 8 (footnote): "Use UDFs responsibly."

If a built-in function or a simple SQL expression does the job, use it. Reach for a UDF only when the logic genuinely cannot be expressed in SQL, and when you've accepted the performance, caching, and cross-tool portability trade-offs.

## Related pages

- [[query-performance-tuning]]
- [[query-optimizer]]
- [[dbt]]
- [[deterministic-stream-processing]]
