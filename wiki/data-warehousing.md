# Data Warehousing

**Summary**: A data warehouse is a separate read-optimized database that holds a copy of data from all OLTP systems in an organization, enabling analysts to run expensive queries without impacting production databases.

**Sources**: `raw/designing-data-intensive-applications/chapter-03-storage-and-retrieval.md`

**Last updated**: 2026-04-15

---

## Purpose

OLTP databases serve user-facing applications that require high availability and low latency. Running ad hoc analytic queries against an OLTP database — queries that scan millions of rows — harms the performance of concurrent transactions.

A **data warehouse** is a separate database designed for analytic access patterns. It contains a read-only copy of data from all the organization's OLTP systems. Analysts can query it freely without affecting production operations.

Data warehouses exist in nearly all large enterprises. Small companies typically don't need them — their data is small enough to query in a conventional database or spreadsheet.

## ETL: Extract–Transform–Load

Data gets into a warehouse via **ETL**:
1. **Extract** — Pull data from OLTP systems via periodic dumps or a continuous stream of changes.
2. **Transform** — Clean, normalize, and reshape the data into an analysis-friendly schema.
3. **Load** — Write the prepared data into the warehouse.

## Schema patterns

Data warehouses use different schema conventions than OLTP databases. Most follow one of two related patterns.

### Star schema

The dominant pattern. At the center is a **fact table** — one row per business event (a sale, a page view, a click). Fact tables can be enormous: tens of petabytes in large enterprises.

Each fact table row has:
- **Attribute columns** — numeric measurements directly captured (price, quantity)
- **Foreign keys** to **dimension tables** — who, what, where, when, how, why of the event

Dimension tables describe the entities involved: products, customers, stores, dates, promotions. They're much smaller than fact tables (millions of rows rather than billions). They can be wide — a `dim_store` table might have dozens of columns describing each store.

The name "star" comes from the visual: fact table in the center, dimension tables radiating out like rays.

### Snowflake schema

A normalized variant of the star schema: dimensions are broken into sub-dimensions. For example, `dim_product` might reference separate `dim_brand` and `dim_category` tables rather than duplicating brand and category strings.

Snowflake schemas are more normalized; star schemas are simpler for analysts to work with. Star schemas are generally preferred in practice.

## Query patterns

A typical data warehouse query joins the fact table to one or more dimension tables and applies aggregate functions across many rows:

```sql
SELECT dim_date.weekday, dim_product.category,
       SUM(fact_sales.quantity) AS quantity_sold
FROM fact_sales
JOIN dim_date    ON fact_sales.date_key   = dim_date.date_key
JOIN dim_product ON fact_sales.product_sk = dim_product.product_sk
WHERE dim_date.year = 2013
  AND dim_product.category IN ('Fresh fruit', 'Candy')
GROUP BY dim_date.weekday, dim_product.category;
```

These queries access a small number of columns from a very large number of rows — the access pattern that motivates [[column-oriented-storage]].

## Separation of concerns

OLTP databases and data warehouses both often expose a SQL interface, but their internals are completely different. Many vendors focus on one or the other:
- OLTP: PostgreSQL, MySQL, Oracle, SQL Server
- Data warehouse: Teradata, Vertica, Amazon Redshift, Google BigQuery, Snowflake, Apache Hive, Spark SQL, Cloudera Impala, Facebook Presto

Some products (SAP HANA, Microsoft SQL Server) support both, but are increasingly treating them as separate storage and query engines behind a common SQL interface.

## Hadoop and the data lake

Hadoop has often been used for ETL: data from OLTP systems is dumped in raw form into [[distributed-filesystems|HDFS]], then [[mapreduce]] or [[dataflow-engines]] jobs clean and transform it into a relational form for loading into an MPP data warehouse. This decouples data collection from data modeling — the raw data is available immediately, and schema design happens in a separate step (source: designing-data-intensive-applications, chapter 10).

This pattern is sometimes called a **data lake** or **enterprise data hub**. It follows the "sushi principle" — raw data is better — and uses a schema-on-read approach where the consumer of data, not the producer, decides how to interpret it. See [[hadoop-vs-mpp-databases]] for how Hadoop and MPP warehouses compare (source: designing-data-intensive-applications, chapter 10).

## Related pages

- [[oltp-vs-olap]]
- [[column-oriented-storage]]
- [[storage-engines]]
- [[hadoop-vs-mpp-databases]]
- [[batch-processing]]
- [[distributed-filesystems]]
