# Data Virtualization

**Summary**: A query/processing engine that **doesn't store data internally** — it runs federated queries against whatever sources you point it at. Trino (Starburst) and Presto are the canonical examples. Closely related to [[federated-query]], but "virtualization" implies the engine itself is storage-less by design.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md`

**Last updated**: 2026-04-18

---

## What makes it different

A warehouse with federated-query support stores some data natively and reaches out to external sources when asked. A virtualization engine reaches out **for everything** — no native storage at all (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).

Any engine that supports external tables can serve as a virtualization engine. The term mostly captures intent: Trino, Presto, and Starburst are *built* around virtualization; Snowflake or BigQuery have it as a feature alongside native storage.

## Why organizations use it

- **Unified query across silos.** Data in MySQL, PostgreSQL, S3, and a NoSQL store, queried in one SQL statement.
- **No duplication, no pipelines.** If the source is authoritative, a virtualization engine avoids the ETL/ELT overhead of copying it into a warehouse.
- **[[data-mesh|Data mesh]] enabler.** Small teams publish their data for query without centralizing everything into a shared warehouse. Virtualization serves as the access layer (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).

## Query pushdown

The key performance optimization: push as much work as possible to the source.

- **Predicate pushdown** — move `WHERE` filters into the source query so the source returns fewer rows.
- **Projection pushdown** — move column selection down so the source returns fewer bytes.
- **Aggregation pushdown** — where supported, push `GROUP BY` into the source.

Two wins: source systems handle the work they're already good at, and less data traverses the network — the critical bottleneck for virtualization performance (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).

## What it doesn't solve

"Virtualizing a production MySQL database doesn't solve the core problem of analytics queries adversely impacting the production system — because Trino does not store data internally, it will pull from MySQL every time it runs a query" (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).

Virtualization isn't a shield for source systems; it's a query layer *over* them. If the source can't handle the analytical load, virtualization makes the problem worse, not better.

## The mixed-pattern approach

A common pattern: use Trino **once a day** at midnight (when source load is low) to pull data from production MySQL into S3. Downstream transformations and daily queries read from S3, protecting MySQL from ongoing analytics (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).

Here virtualization is used as a component in an ingestion pipeline, not as the user-facing query layer.

## Data lake / data mesh fit

Virtualization extends the data lake to many more sources by abstracting away organizational silos. An organization can store frequently-accessed transformed data in S3 and virtualize access across parts of the company — which fits the [[data-mesh]] stance of small teams preparing and sharing their own data (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).

## Related pages

- [[federated-query]]
- [[data-mesh]]
- [[data-lake]]
- [[data-sharing]]
- [[materialized-view]]
