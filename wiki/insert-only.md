# Insert-Only Pattern

**Summary**: A table design where records are never updated or deleted — every change appends a new row with a timestamp, so the full history of the record is preserved in the table itself. Reis and Housley's Chapter 5 names insert-only as the direct alternative to the [[crud|CRUD]] pattern for state-bearing data, and the pattern is the application-side analogue of [[event-sourcing]] and [[change-data-capture|log-based CDC]].

**Sources**: `raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md`

**Last updated**: 2026-04-18

---

## How it works

Rather than mutating a customer-address row when the customer moves, the application **inserts a new address row** under the same customer ID with a new timestamp. The "current address" is whichever row has the most recent timestamp for that ID. To retrieve the current state you evaluate `MAX(created_timestamp)` over the rows for the key; older rows remain as history (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md).

| Record ID | Value | Timestamp |
|---|---|---|
| 1 | `123 Pine St` | 2021-09-19T00:10:23Z |
| 1 | `456 Oak Ave` | 2021-09-30T00:12:00Z |

The table is, in effect, a log of state transitions sitting inside a relational table. Reis and Housley: "the insert-only pattern maintains a database log directly in the table itself, making it especially useful if the application needs access to history" (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md).

## Two distinct uses

Chapter 5 distinguishes two variants (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md):

1. **Application-level insert-only.** The source application itself is built insert-only — for example a banking app that wants to show customer address history over time. History is a product requirement.
2. **ETL-level insert-only pattern.** The source application uses [[crud|CRUD]], but the **analytics pipeline** inserts a new row into the target analytics table every time an update lands. History is a pipeline requirement, not an application one.

Both shapes give the same query surface downstream, but (1) lives in the application's own schema and (2) lives in the warehouse or lakehouse that the data engineer controls.

## Advantages

- **History is free.** No separate audit log, no CDC connector for change events. The history *is* the table.
- **Reproducibility.** Reports can be rerun against the state of the world at any historical timestamp — the row that was current at time T is recoverable.
- **Natural CDC.** The insert stream *is* the change stream; no log parsing required.
- **Crash safety.** Since every write is an insert, there is no "lost update" risk — the pattern sidesteps a whole class of concurrency bugs.

## Disadvantages

Reis and Housley name two (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md):

- **Table growth.** Every change is a new row. Frequently-changing records multiply table size rapidly. Mitigations: purge by sunset date, keep only the last N versions per key, or roll old rows into a compressed historical partition.
- **Lookup overhead.** Retrieving the current value requires an aggregate (`MAX(created_timestamp)`) over all rows for the key. With hundreds or thousands of versions per key, the query cost becomes significant. An index on `(record_id, created_timestamp DESC)` helps; a materialized "current state" view helps more.

## Relationship to other patterns

- **[[crud|CRUD]]**. Insert-only is the inverse choice. CRUD overwrites and loses history; insert-only preserves history and never overwrites. A given application may mix the two — CRUD on high-churn operational tables, insert-only on state-bearing tables where history matters.
- **[[change-data-capture|CDC]]**. [[change-data-capture|Log-based CDC]] captures a change stream *outside* the table by reading the WAL/binlog. Insert-only produces the same change stream *inside* the table without touching logs. Insert-only is often easier to set up; CDC is easier when the application can't be modified.
- **[[event-sourcing]]**. Event sourcing stores *events* (intent — "UserMovedAddress") as the authoritative data; current state is derived. Insert-only stores *states* (facts — "address is X as of T") directly. The overlap is real but not perfect: insert-only is a lighter-weight sibling that skips the explicit event type but gets much of the auditability benefit.
- **[[soft-deletion]]**. Soft-delete is the deletion-only corner of insert-only: never `DELETE`, just mark a row as deleted with a flag and timestamp.
- **[[mvcc|Multi-version concurrency control]]**. The database-internal analogue: MVCC retains old tuple versions invisibly to make snapshot isolation possible. Insert-only exposes that same version history in the application-visible schema.

## Cross-book connections

- [[event-sourcing]] and [[change-data-capture]] (DDIA) are the DDIA-era framing of "history-preserving" data. Insert-only is the Reis & Housley formulation at the application-table level; the two patterns collapse into the same design philosophy at scale.
- [[table-stream-duality]] (Bellemare) — an insert-only table *is* a stream of entity events materialized in place. The duality is direct.

## Related pages

- [[crud]]
- [[change-data-capture]]
- [[event-sourcing]]
- [[soft-deletion]]
- [[mvcc]]
- [[table-stream-duality]]
- [[source-systems]]
- [[application-database-as-source]]
