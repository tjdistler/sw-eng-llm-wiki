# Streaming Queries

**Summary**: Queries that run dynamically against in-flight data, reflecting its real-time nature. Reis & Housley contrast streaming queries (which present a current view of data) with [[data-transformation|streaming transformations]] (which persist new streams for downstream consumption). Three dominant patterns: fast-follower [[change-data-capture|CDC]], [[kappa-architecture|Kappa]], and direct query on streaming storage.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md`

**Last updated**: 2026-04-18

---

## What makes a streaming query different

A batch query is a point-in-time operation: run it, get an answer. A streaming query (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md):

- Runs continuously or on a dynamic trigger.
- Presents a *current view* of data as the stream evolves.
- Can be triggered **by the data itself** — a threshold met, a session closed, a buffer filled — rather than by an external cron or user action.

The last point is the deepest break from batch. A batch query engine is "an external observer" — something else has to tell it to run. Streaming engines can emit computations triggered directly from the data.

## Three dominant patterns

### 1. Fast-follower CDC

Use [[change-data-capture|continuous CDC]] to keep an analytics database as a fast follower of a production database. Run queries against the analytics database with minimal lag behind production (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).

- **Why not query production directly?** Because analytical scans would slow or crash the production workload.
- **Strength.** Serves real-time analytics with minimal impact on the source system.
- **Limitation.** Doesn't rethink batch query patterns — you're still running `SELECT` against a current table state; you miss the opportunity to trigger events off stream changes.

Tools that combine a streaming buffer with long-term columnar storage — Druid, BigQuery — are particularly well suited here. They resemble the [[lambda-architecture|Lambda architecture]] setup.

### 2. Kappa architecture queries

Under [[kappa-architecture]], events are stored as a stream (not a table) with long retention (months to years). Queries run directly over the streaming store, or external tools (Spark) read a time range and compute results (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).

Streaming stores like Kafka KSQL support aggregation, statistical calculations, and even sessionisation directly over the log.

### 3. Query as data-triggered computation

The most native form: set up a streaming job that emits computations when the data says so. Examples (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md):

- Emit mean and median every time N records arrive.
- Output a summary when a user session closes.
- Trigger an alert when an event rate crosses a threshold.

## Windows and triggers

Streaming queries are always tied to [[windowing|windows]]. The choice of window (tumbling / hopping / sliding / session) and trigger (time-based / count-based / session-boundary) determines what the query returns and when. See [[windowing]] and [[watermarks]].

## Joins in streaming queries

Three patterns, all covered in [[stream-joins]]:

- **Table join** with streams feeding one or both tables.
- **Enrichment** — join a stream with a lookup source (RDBMS, cache, object storage).
- **[[stream-joins|Stream-to-stream join]]** — increasingly supported natively; requires a buffer retention interval because arrival latencies differ between streams.

## Cross-book connections

- [[stream-processing]] — DDIA's treatment of streaming query engines as maintainers of materialised views.
- [[kappa-architecture]] — Reis & Housley's Chapter 3 treatment; streaming queries are the natural query pattern for a Kappa stack.
- [[table-stream-duality]] — DDIA's framing that underlies why querying a stream for a current view works at all.

## Related pages

- [[stream-processing]]
- [[windowing]]
- [[watermarks]]
- [[stream-joins]]
- [[kappa-architecture]]
- [[change-data-capture]]
- [[streaming-data-modeling]]
- [[late-arriving-events]]
