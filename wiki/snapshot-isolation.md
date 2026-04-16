# Snapshot Isolation

**Summary**: An [[isolation-levels|isolation level]] where each [[transactions|transaction]] reads from a consistent snapshot of the database taken at the start of the transaction, implemented via [[mvcc|multi-version concurrency control (MVCC)]] -- particularly valuable for long-running read-only queries like backups and analytics.

**Sources**: `raw/designing-data-intensive-applications/chapter-07-transactions.md`, `raw/designing-data-intensive-applications/chapter-09-consistency-and-consensus.md`

**Last updated**: 2026-04-15

---

## Motivation

[[read-committed|Read committed]] isolation allows an anomaly called [[read-skew]] (nonrepeatable reads): a transaction can see the database in an inconsistent state because different reads within the transaction observe data at different points in time. (source: chapter-07-transactions.md)

This is unacceptable for:

- **Backups**: A multi-hour backup process could capture some parts of the database at an older state and others at a newer state. Restoring from such a backup makes the inconsistency permanent.
- **Analytic queries and integrity checks**: Large scans over the database return nonsensical results if different parts are observed at different times. (source: chapter-07-transactions.md)

## How it works

Each transaction reads from a consistent snapshot of the database -- all data that was committed at the start of the transaction. Even if data is subsequently changed by other transactions, each transaction sees only the old data from its snapshot. (source: chapter-07-transactions.md)

A key performance principle: **readers never block writers, and writers never block readers**. This allows long-running read queries to run on a consistent snapshot while writes proceed normally, with no lock contention. (source: chapter-07-transactions.md)

## Implementation via MVCC

Snapshot isolation is implemented using [[mvcc|multi-version concurrency control]]. The database keeps multiple committed versions of each object so that different in-progress transactions can each see the state at their respective points in time. (source: chapter-07-transactions.md)

In PostgreSQL's implementation:

- Each transaction gets a unique, always-increasing transaction ID (txid).
- Each row has a `created_by` field (the txid that inserted it) and a `deleted_by` field (the txid that deleted it, initially empty).
- An update is internally a delete-and-create: the old row is marked deleted and a new row is created.
- Garbage collection removes rows that are no longer visible to any transaction. (source: chapter-07-transactions.md)

### Visibility rules

A transaction can see an object if both conditions hold:

1. The transaction that created the object had already committed when the reader's transaction started.
2. The object is not marked for deletion, or the transaction that requested deletion had not yet committed when the reader's transaction started.

Writes by transactions that are in-progress, aborted, or started after the current transaction are all invisible. (source: chapter-07-transactions.md)

## Indexes and MVCC

Several approaches exist for handling indexes in a multi-version database:

- **Filter approach**: The index points to all versions of an object; queries filter out versions not visible to the current transaction. PostgreSQL optimizes this when multiple versions fit on the same page.
- **Append-only B-trees**: Used by CouchDB, Datomic, and LMDB. Each write transaction creates a new B-tree root; a root is a consistent snapshot at the point in time it was created. Pages not affected by a write remain immutable. (source: chapter-07-transactions.md)

## Naming confusion

Snapshot isolation is not in the SQL standard (it was invented after the standard). Different databases use different names (source: chapter-07-transactions.md):

- **PostgreSQL and MySQL**: call it "repeatable read"
- **Oracle**: calls it "serializable" (even though it is weaker than true serializability)

The SQL standard defines "repeatable read" based on 1975 System R definitions, which predates snapshot isolation. This has led to widespread confusion where nobody really knows what "repeatable read" means. (source: chapter-07-transactions.md)

## Limitations

Snapshot isolation prevents [[dirty-reads-and-dirty-writes]], [[read-skew]], and phantom reads in read-only queries. However, it does **not** prevent:

- **[[lost-updates]]** -- some implementations detect these automatically (PostgreSQL, Oracle, SQL Server); MySQL/InnoDB does not
- **[[write-skew]]** -- requires [[serializability]]
- **[[phantoms]] in write transactions** -- requires predicate locks or index-range locks

## Snapshot isolation and linearizability

Snapshot isolation is **not linearizable**, by design. Reads come from a consistent snapshot that intentionally excludes writes more recent than the snapshot. This means a read may return stale data even after a more recent write has completed -- violating the recency guarantee of [[linearizability]]. (source: designing-data-intensive-applications, chapter 9)

This applies to [[serializable-snapshot-isolation]] (SSI) as well: because SSI is built on snapshot isolation, it is also not linearizable. By contrast, [[two-phase-locking]] and actual serial execution are typically linearizable. A database providing both [[serializability]] and linearizability has **strict serializability**. (source: designing-data-intensive-applications, chapter 9)

However, snapshot isolation is consistent with [[causal-consistency]]: if the snapshot contains an effect, it also contains the cause. The whole point is that it shows a consistent-with-causality view of the database at a single point in time. (source: designing-data-intensive-applications, chapter 9)

## Related pages

- [[isolation-levels]]
- [[mvcc]]
- [[read-committed]]
- [[read-skew]]
- [[serializability]]
- [[serializable-snapshot-isolation]]
- [[transactions]]
- [[linearizability]]
- [[causal-consistency]]
