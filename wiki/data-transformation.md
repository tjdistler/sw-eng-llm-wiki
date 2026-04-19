# Data Transformation

**Summary**: The fourth stage of the [[data-engineering-lifecycle|data engineering lifecycle]] — changing data from its original form into something useful downstream. Transformation is where data begins to create value; without it, data "sits inert." In practice transformation is entangled with ingestion, storage, and serving rather than cleanly isolated. Chapter 8 is the deep dive: [[update-patterns]], [[mapreduce|MapReduce]] and post-MapReduce, SQL-based frameworks like [[dbt]], [[materialized-view|materialized views]], [[federated-query|federation]], [[data-virtualization]], streaming transformations, and [[feature-engineering]] for ML.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md`, `raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md`

**Last updated**: 2026-04-18

---

## What transformation does

Immediately after ingestion, basic transformations convert data into correct types (string to number, string to date), apply standard formats, and drop bad records. Later stages apply schema changes, normalisation, large-scale aggregation for reporting, or featurisation for ML (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

The chapter treats **data preparation, data wrangling, and cleaning** as the low-hanging-fruit transformations that immediately add value for consumers.

## Key engineering considerations

Questions to ask when designing a transformation (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md):

- **Cost and ROI** of the transformation; what business value does it deliver?
- **Simplicity** — is the transformation as simple and self-isolated as possible?
- **Business rules** the transformation encodes.
- **Data movement minimisation** between transformation and storage — computation should live near data where possible.

## Batch vs streaming transformation

Transformation can run in batch or in-flight on a stream. Chapter 2 reiterates the *all data is stream* framing from [[data-ingestion]]: batch is a specialised way of processing a stream. Batch transformations are still overwhelmingly popular, but streaming transformations are growing rapidly with the rise of stream-processing platforms — and may "entirely replace batch processing in certain domains" (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

## Transformations are entangled

Although the lifecycle treats transformation as its own stage, in practice transformations appear everywhere (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md):

- In **[[source-systems|source systems]]** — a service may add an event timestamp before emitting.
- In **[[data-ingestion|ingestion]]** — a streaming pipeline may enrich a record with additional fields and calculations before it reaches the warehouse.
- In **[[data-serving|serving]]** — BI semantic layers apply business logic at query time under a "logic-on-read" pattern.

## Business logic as the primary driver

Business logic is the main force driving transformation, often via [[data-modeling|data modelling]]. Chapter 2's example: a raw retail transaction (`"somebody bought 12 picture frames from me for $30 each, or $360 in total"`) needs accounting rules on top to become a number the CFO can use. A standard approach to implementing business logic across transformations is a core responsibility of the data engineer (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

## Feature engineering for ML

Featurisation is a specific flavour of transformation: extracting and enhancing data features for model training. The chapter calls feature engineering "a dark art" that combines domain expertise with data-science experience; the data engineer's role is to **automate** the featurisation pipelines once data scientists have figured out the shape. See [[feature-store]] (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

## Chapter 8 — query vs transformation

A [[life-of-a-query|query]] retrieves data based on filter and join logic. A transformation **persists the results** for consumption by additional transformations or queries (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md):

- **Persistence** — results saved ephemerally or permanently, not just returned to a user.
- **Complexity** — complex pipelines combine data from multiple sources and reuse intermediate results for multiple final outputs.

While you can build complex dataflows inside single queries using [[common-table-expression|CTEs]], scripts, or DAGs, this quickly becomes unwieldy. Enter transformations — which is why transformations critically rely on [[orchestration]].

## Chapter 8 — batch transformations

The bulk of Chapter 8 treats batch transformations:

- **Distributed joins** — the optimizer picks between [[broadcast-join]] (one side small) and [[shuffle-hash-join]] (both sides large). Same primitive across MapReduce, BigQuery, Snowflake, Spark.
- **ETL vs ELT vs transform-on-read** — Chapter 8's verdict: "the line between ETL and ELT can become somewhat blurry in a data lakehouse environment," especially with [[data-virtualization|virtualization]] and live tables. Apply these terms at the micro (pipeline) level, not the organizational macro level.
- **SQL-based transformation frameworks** — [[dbt]] as the primary embodiment. Analytics engineering as code.
- **Native Spark vs Spark SQL** — ask four questions: how difficult would this be in SQL? How readable? Should it be pushed into a library for reuse? Chapter 8 recommends intermixing SQL inside Spark for Catalyst-optimizable portions.
- **MapReduce and post-MapReduce** — see [[mapreduce]]. Post-MapReduce engines (Spark, BigQuery, Flink) relax the "write-to-disk-between-stages" rigidity by allowing in-memory caching.

## Chapter 8 — update patterns

The family of patterns for writing transformation output: **truncate-and-reload**, **insert-only**, **delete (hard / soft / insert-deletion)**, **[[upsert|upsert/merge]]**, **scripted updates**, **schema updates**. See [[update-patterns]].

Key warnings:

- Don't use single-row inserts against columnar warehouses; load micro-batches.
- Don't run near-real-time merges from CDC against columnar warehouses — you'll bring them to their knees. Batch at hourly (or similar) cadence instead.
- File-based systems use **copy-on-write** internally; small updates are disproportionately expensive.

## Chapter 8 — views, materialization, federation

Three techniques that virtualize query results as table-like objects (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md):

- **[[materialized-view|Materialized views]]** — precomputed query results that refresh on source change. Can be transparently rewritten into by the optimizer.
- **[[federated-query|Federated queries]]** — query external data sources (object storage, other RDBMS) as if they were local tables.
- **[[data-virtualization]]** — engines like Trino/Presto that don't store data at all; query everything via federation. Critical to push predicates down to the source.

## Chapter 8 — business logic and derived data

Classic example: "profit after marketing costs." Business rules are full of edge cases (fraud cancellations, marketing attribution models). This type of reporting data is quintessential **[[derived-data]]** — data computed from other data stored in the system.

Updating complex ETL scripts to reflect business-logic changes is labor-intensive but necessary. The emerging alternative: a **[[metrics-layer]]** that encodes business logic independently of transformations and generates queries to the warehouse.

## Chapter 8 — streaming transformations

Distinct from [[streaming-queries]]: streaming queries present a current view; streaming transformations **prepare data for downstream consumption**. Key patterns (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md):

- **Enrichment** — join a stream against a lookup source; emit enriched events to another stream.
- **[[stream-joins|Stream-stream joins]]** — requires a buffer retention interval because streams arrive with different latencies.
- **Streaming DAGs** — Pulsar's native handling of multi-stream, multi-stage topologies.
- **Micro-batch vs true streaming** — Spark Streaming vs Beam/Flink. No universal answer; pick by latency requirements and team expertise, and distrust vendor benchmarks.

## Chapter 8 — feature engineering

See [[feature-engineering]]. Chapter 8 revisits the Chapter 2 framing: the data scientist designs features; the data engineer automates, backfills, and serves them. A [[feature-store]] centralizes history, sharing, and operational concerns.

## Chapter 8 — data wrangling

See [[data-wrangling]]. Reis & Housley's case for data-wrangling tools as "IDEs for malformed data," pushing back against engineers' dismissal of no-code tools.

## Cross-book connections

- [[batch-processing]], [[mapreduce]], [[dataflow-engines]] — the algorithmic machinery for transformation in batch.
- [[stream-processing]], [[windowing]], [[stream-joins]] — the streaming machinery.
- [[data-modeling]] and [[data-warehousing]] star/snowflake schemas — the shapes transformation targets.
- [[etl-vs-elt]] — whether to transform before or after loading into the warehouse.

## Related pages

- [[data-engineering-lifecycle]]
- [[data-ingestion]]
- [[data-serving]]
- [[data-modeling]]
- [[etl-vs-elt]]
- [[update-patterns]]
- [[upsert]]
- [[materialized-view]]
- [[federated-query]]
- [[data-virtualization]]
- [[dbt]]
- [[feature-engineering]]
- [[data-wrangling]]
- [[metrics-layer]]
- [[streaming-queries]]
- [[query-performance-tuning]]
- [[broadcast-join]]
- [[shuffle-hash-join]]
- [[batch-processing]]
- [[stream-processing]]
- [[windowing]]
- [[feature-store]]
- [[dataflow-engines]]
- [[mapreduce]]
