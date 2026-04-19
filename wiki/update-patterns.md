# Update Patterns

**Summary**: The family of patterns for writing transformation output into persistent storage: **truncate-and-reload**, **insert-only**, **delete**, **[[upsert]]**, **merge**, **schema update**. Each has different performance characteristics in columnar warehouses than in row-based systems, and most data-engineering-team pain comes from using the wrong pattern for the engine.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md`

**Last updated**: 2026-04-18

---

## Why this exists as a concept

The original data lake "didn't really account for updating data" — and Chapter 8 says this now seems nonsensical. Updates matter because (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md):

- Rerunning significant amounts of work when a small change lands is wasteful.
- GDPR and similar require targeted deletion even from raw datasets.
- Analytical workloads naturally produce incremental outputs.

[[lakehouse-table-formats|Lakehouse table formats]] (Delta, Iceberg, Hudi) exist in part to make updates first-class over object storage.

## The pattern menu

### Truncate and reload

Wipe the target table; rerun the transformation; load fresh. "An update pattern that doesn't update anything" (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).

- **Use when** the input is small enough, or when determinism and simplicity matter more than cost.
- **Avoid when** the input has grown past the "reload everything" threshold.

### Insert-only

Append new records without changing or deleting old ones. A query or view finds the "current" record by primary key / latest timestamp.

- **Use when** you want to preserve every historical version (audit trail, time-travel).
- **Computationally expensive** at query time if you need the latest record per key on a large table.
- **Mitigation.** Combine with a [[materialized-view]] that presents the current state, or maintain a truncate-and-reload target that holds only current state for serving.

Related: [[insert-only]] source-system pattern; [[data-vault]] is insert-only at the warehouse layer.

### Delete

- **Hard delete** — row permanently removed. Needed for performance (table too big) or compliance (GDPR).
- **Soft delete** — mark the row with a deleted flag; filter it out at query time.
- **Insert deletion** — append a new record with a deleted flag rather than modifying the prior record. Preserves insert-only semantics but complicates "latest state" queries (must deduplicate *and* exclude latest-is-deleted).

In columnar systems and data lakes, deletes are more expensive than inserts — they require rewriting files via [[update-patterns#copy-on-write|copy-on-write]].

### Upsert / merge

[[upsert|Upsert]] = update if key matches, insert if it doesn't. Merge adds delete to that.

Originally designed for row-based databases, where update-in-place is natural. File-based columnar systems use **copy-on-write (COW)**: changing one record means rewriting the whole file. Hidden by the engine in modern columnar warehouses, but the cost is real.

See [[upsert]] for the detailed trade-offs.

### Scripted updates

Custom SQL scripts doing the update work. Reis & Housley recommend [[common-table-expression|CTEs]] over nested subqueries and temp tables inside these; prefer [[dbt]] or orchestrator-managed table materializations over ad-hoc scripts.

### Schema updates

Adding, deleting, or renaming columns. Columnar systems make this relatively cheap (a metadata change, with new files for new data). But the **organizational process** around schema change is the harder problem (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md):

- Will some updates be **automated** (Fivetran-style)? Convenient, but risks breaking downstream transformations.
- Is there a **review process** for adding new fields?
- Will downstream processes break? (Avoid `SELECT *` — always enumerate columns.)
- Can we create a **table fork** — a new table version specific to the requesting project?

See [[schema-evolution]].

## Copy-on-write (COW)

File-based storage doesn't support in-place file updates. Any logical update rewrites one or more files with the new state (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md):

- COW seldom rewrites the whole table — modern systems operate at partition, cluster, or block resolution.
- Merges can be extremely performant for **large update batches** and may outperform transactional databases at that scale.
- Merges are **slow for small updates** — updating a handful of rows is disproportionately expensive.

Columnar systems like Vertica have long hidden COW from users. Most modern cloud warehouses support updates and merges — but engineers should investigate update support if adopting an exotic technology.

## The merge-frequency trap

Chapter 8's biggest caveat on merges (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md):

> We've seen many engineering teams transition between database systems and try to run near real-time merges from CDC just as they did on their old system. **It simply doesn't work.** No matter how good your CDC system is, this approach will bring most columnar data warehouses to their knees.

Better: merge every hour (or similar batch window) rather than every minute, and use specialized engine features where available:

- **BigQuery**: streaming insert + specialized materialized views that present an efficient, near-real-time deduplicated view.
- **Druid**: two-tier storage with SSD-backed real-time shards.

## Related pages

- [[upsert]]
- [[insert-only]]
- [[materialized-view]]
- [[schema-evolution]]
- [[lakehouse-table-formats]]
- [[change-data-capture]]
- [[data-transformation]]
