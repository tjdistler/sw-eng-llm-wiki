# Query Performance Tuning

**Summary**: Reis & Housley's chapter-8 checklist for making slow queries fast. The rule of thumb: "Don't fight your database. Learn to work with its strengths and augment its weaknesses." Every technique centres on one of three ideas — scan less data, reduce join cost, or cache results.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md`

**Last updated**: 2026-04-18

---

## The levers

### 1. Scan less data (pruning)

The first rule: query only the data you need (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).

- `SELECT *` with no predicate scans the whole table. In pay-per-byte databases (BigQuery) this is directly billable.
- **Column-oriented databases**: select only the columns you need. Use **cluster keys** (Snowflake, BigQuery) to co-locate similar rows so predicate pushdown skips entire files. Use **table partitioning** (BigQuery) to restrict scans to specific partitions. Beware — inappropriate clustering and key-distribution strategies can *degrade* performance.
- **Row-oriented databases**: create **indexes** for the performance-sensitive predicates, but don't load the table with so many indexes that writes degrade.
- See also [[column-oriented-storage]], [[partitioning]], [[indexes]].

### 2. Use the right join strategy

- The optimizer chooses between [[broadcast-join]] (one small table) and [[shuffle-hash-join]] (both tables large) — your job is to make broadcast possible where you can (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).
- **Pre-filter before joining.** Filters moved early in the plan let a large table shrink to broadcastable size. Join reordering by the optimizer helps — but not every optimizer reorders predicates, so write them in an order that helps.
- **Pre-join frequently joined tables.** If analytics repeatedly join the same tables, materialise the join: relax normalisation and widen the schema, or use a [[materialized-view]] (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).
- **Complex join logic** — create a derived column for joining, or use a functional index (e.g., Postgres index on `lower(email)`) so the optimizer can still use an index when a function appears in the predicate (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).

### 3. Avoid row explosion

An "obscure but frustrating" problem: many-to-many join-key repeats cause Cartesian-product blowup. Five `this` rows in A joined to ten `this` rows in B produces 50 rows for that key alone. Enough repeats can kill the query (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).

Predicate reordering by the optimizer helps — but early-stage explosions can fail the query before a later predicate would filter the output. Watch for it in `EXPLAIN`.

### 4. Use CTEs, not nested subqueries or temp tables

[[common-table-expression|CTEs]] are more readable than nested subqueries and often more performant than intermediate-table scripts. If you must materialise an intermediate, use temporary tables (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).

### 5. Cache results

Most cloud OLAP warehouses cache query results. A cold query that takes 40 seconds may return in under a second on a rerun. Leverage the cache; it reduces database pressure and speeds up frequently-run queries (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md). [[materialized-view|Materialized views]] are another form of query caching.

### 6. Vacuum

Dead records — old row versions retained after update/delete for transaction consistency — bloat the storage layer and mislead the optimizer's statistics. **Vacuuming** removes them. Handling varies by database (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md):

- Snowflake: users don't vacuum directly — they control a **time-travel interval** that determines how long snapshots are retained.
- BigQuery: fixed seven-day history window.
- Databricks: retains indefinitely until manually vacuumed; important for S3 cost control.
- PostgreSQL / MySQL: rapid dead-record accumulation under high-transaction workloads; engineers must know the tuning knobs.

### 7. Avoid single-row inserts into columnar

Engineers coming from row-oriented systems try to `INSERT` one row at a time into a columnar warehouse. This writes many tiny files, punishes subsequent reads, and requires reclustering. Load in **micro-batches or batches** (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).

## Things to monitor

Reis & Housley list the metrics that tell you *where* a query is slow (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md):

- Disk, memory, and network utilization.
- Data loading time vs processing time.
- Query execution time, rows returned, bytes scanned, bytes shuffled.
- Competing queries that cause resource contention.
- Concurrent connections used vs available (oversubscription locks users out).

## The commit/consistency axis

Understand how your database commits. It changes what your query sees (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md):

- **PostgreSQL** — ACID transactions with row locking; not optimized for large analytical scans.
- **BigQuery** — point-in-time full-table commits; a query sees the snapshot it started with; only one write op at a time.
- **MongoDB** — variable consistency; in high-throughput modes may silently drop writes.

Know which one you're on. Unexpected results often trace to commit-model mismatch between engineer expectation and engine behaviour.

## Cross-book connections

- [[hadoop-vs-mpp-databases]] — the DDIA comparison that underlies the columnar/cluster-key discussion.
- [[query-optimizer]] — the component that actually makes these optimizations, and the one you reason about via `EXPLAIN`.

## Related pages

- [[query-optimizer]]
- [[life-of-a-query]]
- [[broadcast-join]]
- [[shuffle-hash-join]]
- [[common-table-expression]]
- [[materialized-view]]
- [[column-oriented-storage]]
- [[partitioning]]
- [[indexes]]
