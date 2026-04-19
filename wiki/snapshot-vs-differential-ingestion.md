# Snapshot vs Differential Ingestion

**Summary**: Two ways to pull state-carrying data (typically from a database) in a batch-ingestion pipeline. A **full snapshot** grabs the entire current state of the source on each read. A **differential** or **incremental** update pulls only the rows that changed since the last read. Snapshots are simpler; differentials minimize network, compute, and storage — and are the foundation of [[query-based-cdc|query-based CDC]] and [[change-data-capture|log-based CDC]].

**Sources**: `raw/fundamentals-of-data-engineering/chapter-07-ingestion.md`

**Last updated**: 2026-04-18

---

## The choice

"Data engineers must choose whether to capture full snapshots of a source system or differential (sometimes called incremental) updates" (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md).

| | Full snapshot | Differential |
|---|---|---|
| What's read | Entire current state of the source, every run | Only rows that changed since the last read |
| Implementation | Source-side full-table scan; target-side truncate+reload or separate dated tables | Filter by `updated_at`, an autoincrementing id, or parse the DB log |
| Simplicity | Very simple; easy to reason about | More moving parts; needs a watermark or cursor |
| Network, storage, compute cost | Can be huge for large tables | Small — proportional to change volume |
| Hard-delete tracking | Implicit — missing row means deletion | Invisible unless soft-delete or log-based |
| Historical fidelity | Only "now" | Can preserve every change (with log-based, every event) |

Reis and Housley's observation: "while differential updates are ideal for minimizing network traffic and target storage usage, full snapshot reads remain extremely common because of their simplicity" (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md).

## Snapshot extraction

Full snapshots are the default in traditional batch ETL: extract the whole `customers` table every night, reload into the warehouse. This preserves only the current state at snapshot time. Intermediate changes between snapshots are lost — if a customer updated and then reverted their address between two snapshots, you will never see the intermediate address.

This is the default Reis and Housley assume when they describe the classic "run once a day, overnight during off-hours" batch-ingestion pattern (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md).

## Differential extraction

Differential updates require the engineer to know **what has changed since last time**. Three common mechanisms:

- **Timestamp-based.** The source has an `updated_at` column the ingestion system can filter against. This is the shape of [[query-based-cdc|batch-oriented CDC]] that Ch 7 describes: "we set the filter timestamp based on when we last captured changed rows from the tables. This process allows us to pull changes and differentially update a target table" (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md).
- **Autoincrement-based.** Same idea using a monotonic id column. Only works for insert-only tables or for tables where new records reflect updates.
- **Log-based.** The DB binlog / WAL is itself a differential stream; parsing it yields every change. This is log-based [[change-data-capture|CDC]].

## The "missing intermediate changes" problem

Ch 7 names the critical limitation of **batch-CDC-style differential**: while it tells you which rows changed since a point in time, it does **not** necessarily give you *all* the changes that happened in between (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md).

Their example: a bank account table with the current balance per account. If a customer withdrew money five times in the last 24 hours, a 24-hour batch CDC query returns **only the last recorded account balance** — the other four transactions are invisible. The fix: make the source [[insert-only]] (each transaction becomes a new record), so "pulling changed rows since T" returns every event rather than only the latest post-state.

Continuous log-based CDC solves the same problem differently — by treating **each write to the database as an event**, it sees every intermediate state (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md).

## Connection to CDC patterns

The snapshot vs differential choice maps directly onto how the ingestion pipeline gets data out of a database:

| Extraction pattern | Where it sits |
|---|---|
| Full snapshot reload | Full snapshot |
| Query-based CDC with `updated_at` filter | Differential (batch) |
| Log-based CDC reading the binlog/WAL | Differential (continuous) |
| Outbox-table pattern | Differential (via application-published events) |

See [[change-data-capture]], [[query-based-cdc]], [[cdc-triggers]], [[outbox-table-pattern]].

## Bootstrapping from the snapshot

Ch 7's CDC coverage implies the hybrid in practice: log-based CDC by itself does not go back to the beginning of time because the log is periodically truncated. A new pipeline typically takes one **initial snapshot** of the source table, then switches to differential ingestion from a recorded log offset onward. This is the same bootstrapping pattern DDIA and Bellemare describe in depth on [[change-data-capture]].

## Related pages

- [[data-ingestion]]
- [[change-data-capture]]
- [[query-based-cdc]]
- [[cdc-triggers]]
- [[outbox-table-pattern]]
- [[insert-only]]
- [[crud]]
- [[batch-processing]]
- [[file-based-ingestion]]
- [[data-migration]]
