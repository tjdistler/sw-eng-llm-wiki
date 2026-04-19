# Data Warehousing

**Summary**: A data warehouse is a separate read-optimized database that holds a copy of data from all OLTP systems in an organization, enabling analysts to run expensive queries without impacting production databases. Reis and Housley give it pride of place among data architecture patterns — "among the oldest and most well-established" — and distinguish its **organisational** architecture (business structure around the warehouse) from its **technical** architecture (MPP, columnar, cloud).

**Sources**: `raw/designing-data-intensive-applications/chapter-03-storage-and-retrieval.md`, `raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md`, `raw/fundamentals-of-data-engineering/chapter-06-storage.md`

**Last updated**: 2026-04-18

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

## Chapter 3: Inmon's original definition

Chapter 3 of *Fundamentals of Data Engineering* traces the warehouse to Bill Inmon's 1990 definition (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md):

> A subject-oriented, integrated, nonvolatile, and time-variant collection of data in support of management's decisions.

Reis and Housley argue this definition has held up despite decades of technical evolution. What has changed is affordability: on-prem warehouses used to cost millions and require dedicated teams; cloud pay-as-you-go made the pattern accessible to tiny companies.

## Chapter 3: organisational vs technical architecture

Chapter 3 draws a distinction the DDIA treatment does not (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md):

- **Organisational data warehouse architecture** — how data is organised around business team structures and processes. Two defining properties: (1) analytics (OLAP) separated from production (OLTP); (2) data centralised and organised, traditionally via ETL into tightly-modelled form. DBA and ETL developer teams implement business leaders' direction so that reporting corresponds to business processes.
- **Technical data warehouse architecture** — MPP, columnar, cloud-specific implementation details. A company can have a warehouse without MPP, or run an MPP system that isn't organised as a warehouse. In practice the two have existed in a virtuous cycle.

## Chapter 3: the cloud data warehouse

Chapter 3 treats cloud warehouses as a **significant evolution** (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md):

- **Amazon Redshift** kicked off the cloud data warehouse revolution — on-demand clusters, no multimillion-dollar upfront contract
- **Google BigQuery and Snowflake** popularised **separating compute from storage**: data lives in object storage (virtually limitless), compute spins up on demand
- Cloud warehouses now process petabytes in a single query, store tens of megabytes of raw text per row, and handle rich JSON
- The line between warehouse and [[data-lake|lake]] is **blurring**; see the [[data-lakehouse]]

Chapter 3 goes as far as suggesting the term "data warehouse" itself might be jettisoned as these services evolve into broader **data platforms**.

## Chapter 3: ELT and ELT-on-lake

Chapter 3 adds two flavour notes on the [[etl-vs-elt|ETL/ELT]] distinction (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md):

- **ELT in a cloud warehouse**: data moves more or less directly from production into a **staging area** (raw form), then transforms happen directly in the warehouse using its computational power. Popular in streaming arrangements — CDC-sourced events land in staging, then transform inside the warehouse.
- **Transform-on-read ELT** — popularised during the Hadoop era; the [[data-lake]]'s native pattern. Chapter 3 distinguishes it from warehouse-side ELT.

## Chapter 3: MPP

Chapter 3 sketches the technical trajectory (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md):

- First **MPP (massively parallel processing)** systems emerged in the late 1970s, popular in the 1980s
- Same SQL semantics as relational application databases, but optimised to scan massive data in parallel for aggregation and statistics
- MPPs have shifted from row-based to **[[column-oriented-storage|columnar]]** architecture in recent years, especially in cloud warehouses
- MPPs are indispensable for performant queries as enterprise data and reporting grow

## Ch 6 — the warehouse as storage abstraction

Chapter 6 frames the data warehouse as one of four **data-engineering storage abstractions** alongside [[data-lake]], [[data-lakehouse]], and [[data-platform|data platform]] (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md). The trajectory stated plainly:

> We've evolved from building data warehouses atop conventional transactional databases, row-based MPP systems (e.g., Teradata and IBM Netezza), and columnar MPP systems (e.g., Vertica and Teradata Columnar) to cloud data warehouses and data platforms.

Two practical Chapter 6 points worth noting:

- **Cloud DWs as lake-host.** "Cloud data warehouses are often used to organize data into a data lake." They can store massive raw text and complex JSON, but not true unstructured data (images, video, audio) — those belong in [[object-storage]]. A common pattern is **warehouse + object storage** as a coupled solution.
- **Convergence with lakes.** "The popularity of separating storage from compute means the lines between OLAP databases and data lakes are increasingly blurring. Major cloud data warehouses and data lakes are on a collision course. In the future, the differences between these two may be in name only since they might functionally and technically be very similar under the hood" (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md). See [[storage-compute-separation]] and [[data-lakehouse]].

## Ch 6 — micro-partitioning (Snowflake)

Chapter 6 calls out **Snowflake's micro-partitioning** as a representative evolution of columnar storage (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md):

- Rows are grouped into **micro-partitions of 50–500 MB uncompressed**.
- Snowflake algorithmically clusters similar rows together rather than partitioning on a single designated field.
- A metadata database stores per-micro-partition statistics (row count, value ranges per field).
- At query time, Snowflake **prunes** micro-partitions whose value ranges don't match the predicate — e.g. a `WHERE created_date='2017-01-02'` query skips every micro-partition whose date range excludes that value.
- Snowflake calls this **hybrid columnar storage** — storage is columnar, but rows are grouped into small units; the metadata plays the role of an index in a traditional RDBMS.

See [[partitioning]] for the broader context of analytics partitioning and clustering.

## Data marts

See [[data-mart]]. Chapter 3 introduces the mart as the refined subset of a warehouse tailored to a single department — providing accessibility for analysts and a second transformation stage for performance on complex joins and aggregations.

## Related pages

- [[oltp-vs-olap]]
- [[column-oriented-storage]]
- [[storage-engines]]
- [[hadoop-vs-mpp-databases]]
- [[batch-processing]]
- [[distributed-filesystems]]
- [[data-lake]]
- [[data-lakehouse]]
- [[data-platform]]
- [[data-mart]]
- [[modern-data-stack]]
- [[etl-vs-elt]]
- [[data-architecture]]
- [[storage-compute-separation]]
- [[object-storage]]
- [[partitioning]]
