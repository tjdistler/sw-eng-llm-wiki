# Data Lakehouse

**Summary**: A convergent storage pattern that grafts warehouse-like guarantees (schema, ACID transactions, governance, SQL) onto a [[data-lake|data lake's]] cheap object-storage foundation. Reis and Housley list the lakehouse alongside warehouse, lake, database, and object storage as one of the major storage-technology categories the data engineer chooses between.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md`, `raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md`, `raw/fundamentals-of-data-engineering/chapter-06-storage.md`

**Last updated**: 2026-04-18

---

## The motivation

Classic [[data-lake|data lakes]] had two major weaknesses:

1. **No transactional guarantees.** Deletion, update, and concurrent writes were fragile — which made GDPR compliance painful and schema evolution risky (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).
2. **Schema drift and data swamps.** Without governance, raw lakes degenerated. See [[data-modeling]] on the WORN (write once, read never) antipattern.

Classic [[data-warehousing|warehouses]] had the opposite problem: strong transactional and schema guarantees, but rigid, expensive storage tied to the query engine, with limited ability to hold raw/unstructured data.

The lakehouse stance: keep the lake's cheap object-storage foundation, but add warehouse-like transactional tables on top.

## What Chapter 2 says

Chapter 2 names the lakehouse directly in the storage-evaluation question list: "Is this storage solution compatible with the architecture's required write and read speeds? ... when choosing a storage system for a data warehouse, data lakehouse, database, or object storage" (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md). The book treats the lakehouse as a first-class storage category alongside the other three.

Chapter 2 doesn't go deep on the lakehouse architecture itself — Chapter 6 (Storage) is signposted for that. But the mention of **Delta Lake** in [[data-lifecycle-management]] as a tool that "allows easy management of deletion transactions at scale" on a lake-like store is pointing at one of the major lakehouse implementations (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

## The main implementations

Not all named in Chapter 2, but the field's typical landscape:

- **Delta Lake** (Databricks) — transactional table format over Parquet on object storage; explicitly called out in Chapter 2 for enabling deletion at scale on a lake.
- **Apache Iceberg** — table format with hidden partitioning, schema evolution, and time travel.
- **Apache Hudi** — incremental-processing-oriented table format.

Each provides: ACID transactions on object storage, schema evolution, time travel, and efficient updates/deletes — the warehouse-like guarantees missing from classic lakes.

## Chapter 3: the convergence narrative

Chapter 3 frames the lakehouse as the central move in a broader **convergence** story (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md):

> The lakehouse incorporates the controls, data management, and data structures found in a data warehouse while still housing data in object storage and supporting a variety of query and transformation engines. In particular, the data lakehouse supports atomicity, consistency, isolation, and durability (ACID) transactions, a big departure from the original data lake.

The broader trajectory Chapter 3 describes:

- [[data-lake|Data lake 1.0]] failed to deliver on management, governance, and deletion
- Databricks coined **lakehouse** as the response
- Cloud warehouses (BigQuery, Snowflake) evolved *toward* the lake: compute-storage separation, petabyte queries, unstructured/JSON support, Spark/Beam integration
- The result is **converged data platforms** — AWS, Azure, Google Cloud, Snowflake, Databricks as class leaders, each offering a tightly integrated tool constellation running from relational through unstructured

Chapter 3's conclusion: lake and warehouse will remain distinct as architectures, but in day-to-day work "few users will notice a boundary between them." Future data engineers will choose converged data platforms rather than picking between lake and warehouse.

See [[modern-data-stack]] for the plug-and-play ecosystem that typically sits on top of a lakehouse/converged platform.

## Ch 6 — the architecture in detail

Chapter 6 gives the most concrete description of what a lakehouse *is* as a system (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md):

> As it is generally conceived, the lakehouse stores data in object storage just like a lake. However, the lakehouse adds to this arrangement features designed to streamline data management and create an engineering experience similar to a data warehouse.

The feature set, stated explicitly:

- **Robust table and schema support.**
- **Features for managing incremental updates and deletes.**
- **Table history and rollback** — accomplished by retaining old versions of files and metadata.
- **ACID transactions** over object-storage files — a fundamental departure from classic data lakes.

Chapter 6's one-line architectural definition: "A lakehouse system is a metadata and file-management layer deployed with data management and transformation tools" (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md). The heavy lifting lives in the metadata, not the files themselves. See [[lakehouse-table-formats]] for the three reference implementations (Delta Lake, Iceberg, Hudi) and the specific mechanisms each uses.

## Ch 6 — interoperability as the real advantage

Reis and Housley explicitly name **interoperability** as the lakehouse's core advantage over proprietary data platforms (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md):

> It's much easier to exchange data between tools when stored in an open file format. Reserializing data from a proprietary database format incurs overhead in processing, time, and cost. In a data lakehouse architecture, various tools can connect to the metadata layer and read data directly from object storage.

Snowflake and BigQuery provide equivalent warehouse-like guarantees — ACID, table history, update/delete — but in proprietary formats. Migrating data *out* of them is expensive. A lakehouse stores the same data as Parquet files governed by an open table format, so Spark, Trino, DuckDB, or even Snowflake (via external Iceberg reads) can query the same files. The lock-in drops to the catalog and metadata layer, which is substantially lower.

## Ch 6 — hybrid, not uniform

A point Chapter 6 is careful to make (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md):

> It is important to emphasize that much of the data in a data lakehouse may not have a table structure imposed. We can impose data warehouse features where we need them in a lakehouse, leaving other data in a raw or even unstructured format.

The lakehouse is **not a forced schema-on-write world**. Structured business tables get the warehouse-like guarantees; raw logs, images, audio, and video sit alongside as plain objects. A single storage foundation serves both. This is the capability a classical warehouse cannot match.

## Related pages

- [[data-storage-stage]]
- [[data-lake]]
- [[data-warehousing]]
- [[lakehouse-table-formats]]
- [[object-storage]]
- [[storage-compute-separation]]
- [[data-platform]]
- [[modern-data-stack]]
- [[data-architecture]]
- [[data-lifecycle-management]]
- [[column-oriented-storage]]
- [[schema-evolution]]
- [[acid]]
- [[mvcc]]
- [[tombstone]]
- [[data-engineering-lifecycle]]
