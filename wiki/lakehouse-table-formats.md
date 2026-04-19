# Lakehouse Table Formats

**Summary**: **Delta Lake, Apache Iceberg, and Apache Hudi** are the three dominant open-source **table formats** that graft warehouse-style ACID transactions, schema enforcement, and time-travel onto cheap [[object-storage]]. They are the technical substrate of the [[data-lakehouse]] — a metadata and file-management layer over Parquet (or similar) columnar files that turns an object-storage bucket into something that behaves like a transactional database.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-06-storage.md`

**Last updated**: 2026-04-18

---

## The gap they fill

Classic [[data-lake|data lakes]] stored data as Parquet or ORC files in object storage. Readers could scan them in parallel, but *writing* was brittle:

- **No atomic multi-file writes.** A query listing a directory could see half-written output.
- **No UPDATE or DELETE.** Changing a value meant rewriting whole partitions. GDPR-era deletions were operationally painful.
- **No schema enforcement.** A writer could append inconsistent schema; readers discovered it at query time.
- **No time travel.** Rolling back a bad batch meant reconstructing state from backups.

Table formats solve this with a **metadata layer** on top of the object-storage files (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md). The metadata describes which files belong to which version of the table, what the schema is, and what partitions each file covers. Readers consult the metadata, not the raw object listing.

## What they all provide

Chapter 6's framing of the lakehouse names the common feature set (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md):

- **Robust table and schema support.** Named columns, types, constraints; reads see a consistent schema regardless of which underlying file they land on.
- **Incremental updates and deletes.** Row-level merge, update, and delete operations — the DML that lake 1.0 could not efficiently express.
- **Table history and rollback.** "Accomplished by retaining old versions of files and metadata." The log of metadata changes is itself a table history.
- **ACID transactions** on object storage. A single write is either fully visible to readers or not visible at all.

Internally, each format achieves these with a combination of:

- **Parquet (or ORC)** as the row-storage format — see [[column-oriented-storage]].
- **A transaction log** (Delta's `_delta_log`, Iceberg's manifest files, Hudi's timeline) recording what files constitute each version.
- **[[mvcc|Multi-version concurrency control]]** — old file versions are retained until cleaned up, so readers at an earlier transaction see a consistent snapshot.
- **[[tombstone|Tombstones]]** for deletes — markers indicating rows/files to be ignored, cleaned up at vacuum time.

## The three implementations

Chapter 6 names all three but does not compare them in depth (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md). The field's typical positioning:

### Delta Lake

Originated at Databricks; the most prominent implementation. Promoted heavily as the reference lakehouse format. Storage is Parquet; the `_delta_log` JSON files record the sequence of commits. Strong integration with the Apache Spark ecosystem. Chapter 2 flags Delta Lake specifically for making scalable deletion transactions practical on lakes, which matters for GDPR/CCPA compliance.

### Apache Iceberg

Originated at Netflix; later donated to Apache. Emphasises **hidden partitioning** (partition strategy can change without rewriting data or rewriting queries) and **schema evolution** that does not require file rewrites. Strong read-side integration with query engines including Trino, Spark, Snowflake, BigQuery. Iceberg has become the de facto interchange format across vendor boundaries — Snowflake, AWS, GCP, and Databricks all support reading external Iceberg tables.

### Apache Hudi

Originated at Uber. Emphasises **incremental processing** — tables can be queried for only the rows changed since a timestamp, supporting incremental-ingestion pipelines. Two storage modes: **copy-on-write** (rewrite files on update — faster reads, slower writes) and **merge-on-read** (log changes, merge at read time — faster writes, slightly slower reads). Chapter 6 notes that Hudi is also cited as a hybrid serialisation format (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md).

## Relationship to commercial platforms

Reis and Housley explicitly call out that **Snowflake and BigQuery already do internally what lakehouse formats do externally** (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md):

> The architecture of the data lakehouse is similar to the architecture used by various commercial data platforms, including BigQuery and Snowflake. These systems store data in object storage and provide automated metadata management, table history, and update/delete capabilities.

The difference is **interoperability**. Snowflake's internal table format is proprietary: to read it from outside Snowflake, you export. Open table formats make the files queryable by any compatible engine — Spark, Trino, DuckDB, Snowflake (via Iceberg), Databricks (via Delta), etc. The cost of moving between tools collapses (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md).

This is why the big vendors have converged on **reading external Iceberg or Delta tables** as a feature — it preserves their query advantages while removing the "data is stuck in our silo" objection.

## What they are not

Chapter 6 is explicit: "It is important to emphasize that much of the data in a data lakehouse may not have a table structure imposed. We can impose data warehouse features where we need them in a lakehouse, leaving other data in a raw or even unstructured format" (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md). Lakehouse formats **coexist with raw files in the same bucket**. Structured tables get warehouse-like features; raw binary objects (images, video, audio, arbitrary JSON) sit alongside them in their original form.

This is the architectural win over a pure warehouse: same storage foundation for structured and unstructured data, with warehouse semantics layered on where needed.

## Related pages

- [[data-lakehouse]]
- [[object-storage]]
- [[data-lake]]
- [[data-warehousing]]
- [[column-oriented-storage]]
- [[storage-compute-separation]]
- [[schema-evolution]]
- [[mvcc]]
- [[tombstone]]
- [[acid]]
- [[data-lifecycle-management]]
