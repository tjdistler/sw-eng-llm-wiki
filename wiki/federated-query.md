# Federated Query

**Summary**: A database feature that lets an OLAP engine select from an **external data source** — object storage, another RDBMS — as if it were a local table. The query engine talks to the remote source at query time, combines the result with local data, and returns a unified answer. Cousin to [[data-virtualization]] and [[materialized-view|materialized views]] over external data.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md`

**Last updated**: 2026-04-18

---

## What it does

A federated query lets the warehouse combine data across object storage and various external databases without staging it first. You issue one query; the engine fans out to the external sources, pulls what it needs, and joins locally.

Example from Chapter 8: combining data across object storage plus tables in MySQL and PostgreSQL — the warehouse issues a federated query to all three and returns the combined result (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).

## Snowflake external tables (a representative implementation)

Snowflake supports external tables defined on S3 buckets. The table definition specifies an S3 location and a file format, but no data is ingested. When the external table is queried, Snowflake reads from S3 and processes the data with the stored format parameters. External-table data can be joined to internal warehouse tables (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).

This is what makes cloud warehouses compatible with a data-lake environment: the warehouse becomes a query layer over lake-resident data.

## Federated query → materialized view

Some OLAP systems can convert a federated query into a [[materialized-view]]. This gives you table-like performance without manually ingesting, and the view refreshes when the external source changes — a middle ground between "always live" (federated) and "fully ingested" (loaded into native tables) (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).

## When to use

- You need occasional joins between warehouse data and lake / external data.
- You don't want the pipeline complexity of loading everything into native tables.
- The external data changes infrequently (or you can live with the freshness semantics).

## When to avoid

- **Hot external sources.** Querying a production MySQL via federation every time gives you analytics-query load on production — the exact problem the warehouse was supposed to solve. Use federated queries as a **scheduled extraction** primitive (once a day at midnight) rather than an online read path.
- **High query volume.** Federated reads don't cache the external data; the external source pays the read cost every time.

## Relationship to data virtualization

[[data-virtualization]] is the more general pattern: a query engine that doesn't store data internally at all, only federates. Trino/Presto are the canonical examples. Federated query features in warehouses are a middle ground — the warehouse stores some data natively and federates for the rest.

## Related pages

- [[data-virtualization]]
- [[materialized-view]]
- [[data-lake]]
- [[data-lakehouse]]
- [[query-performance-tuning]]
