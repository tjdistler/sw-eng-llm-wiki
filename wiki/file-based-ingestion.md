# File-Based Ingestion

**Summary**: A push-style [[data-ingestion|ingestion]] pattern where the source system serializes data into files (CSV, Parquet, Avro, JSON, etc.) and delivers them to a consumer via object storage, SFTP, EDI, SCP, or a similar transport. Ch 7 presents it as a security- and control-friendly alternative to direct database connections — the source decides what gets exported and how, and the consumer never touches the backend.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-07-ingestion.md`

**Last updated**: 2026-04-18

---

## The pattern

"Data is quite often moved between databases and systems using files. Data is serialized into files in an exchangeable format, and these files are provided to an ingestion system" (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md).

Ch 7 classifies file-based export as [[push-vs-pull-vs-poll|push-based]]: "data export and preparation work is done on the source system side."

Typical delivery transports:

- **[[object-storage|Object storage]]** (S3, GCS, Azure Blob). Ch 7 calls out object storage as "the most optimal and secure way to handle file exchange" — multitenant, high-performance, arbitrary file types and sizes, with signed-URL short-term access.
- **SFTP / SCP.** Older but still widespread, especially between partner businesses unwilling to adopt other standards.
- **[[edi|EDI]].** Archaic but persistent — email, flash drives, and other "any data movement method" categories.

## Why it beats direct DB connection

Ch 7 lists two main advantages (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md):

- **Security.** "It is often undesirable to allow direct access to backend systems for security reasons." With file-based ingestion, the source decides what to expose and runs its own export process; the consumer never opens a connection into the production database.
- **Source-side control.** "Export processes are run on the data-source side, giving source system engineers complete control over what data gets exported and how the data is preprocessed." The source can filter, anonymize, transform, or format before writing the file.

## File formats matter

Ch 7 walks through the format landscape (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md):

### CSV is everywhere and error-prone

"CSV is by no means a uniform format." Engineers must stipulate delimiter, quote characters, and escaping to handle string data correctly. CSV does not natively encode schema or support nested structures. Autodetection is a convenience but "inappropriate for production ingestion." Best practice: record CSV encoding and schema details in file metadata.

### Modern formats are strictly better — when supported

More robust options: **Parquet, Avro, Arrow, ORC, JSON** (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md):

- Natively encode schema.
- Handle arbitrary string data without escaping hazards.
- Most handle nested structures natively (JSON fields stored as internal nested data rather than escaped strings).
- Columnar formats (Parquet, Arrow, ORC) allow direct transcoding between columnar databases — no row-oriented round-trip.
- Arrow is designed to map directly into processing-engine memory, yielding high performance in data-lake environments.

The catch: many source systems still don't support these natively. "Data engineers are often forced to work with CSV data and then build robust exception handling and error detection to ensure data quality on ingestion" (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md).

See [[encoding-formats]] for the cross-book treatment of each format.

## Databases as first-class file exporters

Modern cloud data warehouses — Snowflake, BigQuery, Redshift — "are highly optimized for direct file export" to object storage in various formats (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md). This is the opposite end of the era where the only way out of a database was JDBC: bulk export is now often the fastest path, and it bypasses the row-by-row JDBC/ODBC bottleneck.

On the load side of the database, bulk export into object storage is "often an excellent intermediate stage for transferring data" for [[data-migration|data migrations]] and [[snapshot-vs-differential-ingestion|snapshot-style batch ingestion]].

## Managing export load on the source

Ch 7's operational caveat for transactional sources: "export involves large data scans that significantly load the database for many transactional systems." Source engineers must pick when to run them without hurting application performance, or apply one of the mitigations (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md):

- Break a single large export into **smaller exports by key range or partition**.
- Run the export against a **read replica** rather than the primary.

Read replicas are "especially appropriate if exports happen many times a day and coincide with a high source system load."

## Chunking large files

For genuinely large payloads, Ch 7 recommends splitting into chunks: smaller files are easier to transmit over a network (especially compressed) and reassembled after arrival (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md). See [[ingestion-payload]].

## Related pages

- [[data-ingestion]]
- [[push-vs-pull-vs-poll]]
- [[object-storage]]
- [[encoding-formats]]
- [[compression-algorithms]]
- [[ingestion-payload]]
- [[snapshot-vs-differential-ingestion]]
- [[data-migration]]
- [[edi]]
- [[file-sources]]
- [[data-warehousing]]
