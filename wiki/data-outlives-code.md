---
name: Data Outlives Code
description: Database records encoded under old schemas persist long after the code that wrote them is replaced; how to handle this safely
type: reference
---

# Data Outlives Code

**Summary**: Unlike application code, database records are rarely migrated when a schema changes. A row encoded five years ago with an old schema sits in the same table as a row written today. The code is long gone; the data remains. This asymmetry has important consequences for [[backward-forward-compatibility]] in database systems.

**Sources**: `raw/designing-data-intensive-applications/chapter-04-encoding-and-evolution.md`

**Last updated**: 2026-04-15

---

## The Asymmetry

When a new version of a server-side application is deployed, the old version is replaced within minutes. But the data those old versions wrote stays in the database indefinitely — unless it is explicitly rewritten.

A single database may simultaneously contain:
- Records written with the schema from five years ago.
- Records written with last month's schema.
- Records written with today's schema.

This is "data outlives code." The corollary: **rewriting existing data into a new schema is expensive and usually avoided**.

Most relational databases support additive schema changes — adding a new column with a null default — without rewriting existing rows. The database fills in null for the new column when an old row is read. MySQL is an exception: it often rewrites the entire table even when not strictly necessary.

## Compatibility Requirements

Because old and new code access the same database rows:

- **Backward compatibility** (new code reads old data): new code must handle missing fields gracefully — treating them as null or using a default value.
- **Forward compatibility** (old code reads new data): old code must ignore fields it doesn't recognize and, critically, must not destroy them on re-write.

The second point is the subtle danger.

## The Re-Write Problem

Consider this sequence:
1. New code adds a field `billing_address` and writes it to a record.
2. Old code (still running during a rolling upgrade) reads that record, doesn't know about `billing_address`, loads it into an application model object, modifies some other field, and writes the record back.
3. If the old code's model object simply drops unknown fields during serialization, `billing_address` is silently lost.

The binary [[encoding-formats|encoding format]] can preserve unknown fields automatically (Thrift, Protocol Buffers, and Avro all do this at the encoding layer). But if the application deserializes to a language object (which has no slot for unknown fields) and then re-serializes, the encoding layer has no chance to help — the application layer must be written to preserve fields it doesn't understand.

This is not a hard problem to solve, but it requires awareness.

## Schema Evolution in Databases

Different databases handle schema evolution differently:

- **Relational databases**: schema changes via `ALTER TABLE`. Adding a column with a null default is cheap (no row rewrite). Most other changes require table rewrites. Schema migrations (e.g., via tools like Flyway or Liquibase) are executed at deployment time.
- **Document databases (schema-on-read)**: no enforced schema; old and new documents coexist naturally. The application must handle both shapes. See [[schema-on-read-vs-write]].
- **LinkedIn's Espresso**: uses [[avro]] for storage, leveraging Avro's schema evolution rules. Each record stores a schema version number; the schema registry resolves the writer's schema for decoding.

## Schema Evolution and Archival Storage

When taking a database snapshot (for backup or loading into a data warehouse), it is practical to re-encode all data in the latest schema, since the data is being copied anyway. Formats like Avro object container files are well-suited for this — the writer's schema is embedded in the file header once, and all records use it consistently. This is also an opportunity to re-encode into an analytics-friendly format like Parquet (column-oriented). See [[column-oriented-storage]].

## Related pages

- [[backward-forward-compatibility]]
- [[schema-evolution]]
- [[encoding-formats]]
- [[avro]]
- [[schema-on-read-vs-write]]
- [[column-oriented-storage]]
