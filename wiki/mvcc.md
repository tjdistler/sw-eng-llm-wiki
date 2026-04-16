# MVCC (Multi-Version Concurrency Control)

**Summary**: A technique where the database maintains multiple committed versions of each object side by side, allowing [[transactions]] at different points in time to each see a consistent snapshot without blocking concurrent writers.

**Sources**: `raw/designing-data-intensive-applications/chapter-07-transactions.md`

**Last updated**: 2026-04-15

---

## Core idea

Rather than overwriting data in place, MVCC creates a new version every time a value is changed. Multiple in-progress transactions can each see the database state at their respective start times, because older versions are preserved until no transaction needs them. (source: chapter-07-transactions.md)

MVCC is the implementation mechanism behind [[snapshot-isolation]]. If a database only needed [[read-committed]] isolation, keeping two versions (committed and uncommitted) would suffice. But storage engines that support snapshot isolation typically use MVCC for read committed as well -- the difference is that read committed uses a separate snapshot per query, while snapshot isolation uses the same snapshot for the entire transaction. (source: chapter-07-transactions.md)

## How it works (PostgreSQL model)

Each transaction receives a unique, always-increasing transaction ID (txid). Data written by a transaction is tagged with the writer's txid. (source: chapter-07-transactions.md)

Each row has two metadata fields:

- **`created_by`**: the txid of the transaction that inserted the row
- **`deleted_by`**: initially empty; set to the txid of the transaction that deletes the row

An **update** is internally translated into a delete of the old row and a create of a new row. The old row is marked with `deleted_by` and a new row is created with the updated values. (source: chapter-07-transactions.md)

A **garbage collection** process removes rows marked for deletion once no running transaction can see them. (source: chapter-07-transactions.md)

## Visibility rules

A transaction sees an object if both conditions are true:

1. The creating transaction had already committed when the reader's transaction started.
2. The object is not marked for deletion, or the deleting transaction had not yet committed when the reader started.

Writes by in-progress, aborted, or later-started transactions are invisible. This ensures each transaction sees a consistent snapshot. (source: chapter-07-transactions.md)

## MVCC and indexes

Handling indexes in a multi-version database involves trade-offs:

- **Point-to-all-versions**: The index points to every version of an object. Index queries must filter out versions not visible to the current transaction. Garbage collection removes stale index entries.
- **Append-only / copy-on-write [[b-trees]]**: Used by CouchDB, Datomic, and LMDB. Modified pages are copied rather than overwritten; each write creates a new tree root that serves as a consistent snapshot. Unmodified pages remain immutable and shared. (source: chapter-07-transactions.md)

## Role in SSI

[[serializable-snapshot-isolation]] builds on MVCC by tracking when a transaction reads data that was ignored due to MVCC visibility rules (i.e., an uncommitted write existed at read time that later commits). If the ignored write commits before the reading transaction commits, the database detects that the read was stale and may abort the transaction. (source: chapter-07-transactions.md)

## Related pages

- [[snapshot-isolation]]
- [[read-committed]]
- [[serializable-snapshot-isolation]]
- [[b-trees]]
- [[transactions]]
- [[indexes]]
