# Stream, Transform, Load (STL)

**Summary**: Reis and Housley's proposed name for streaming-era transformation — a "back-to-the-future" return to ETL shape in a streaming context, where extraction is continuous, transformation happens in flight, and the result lands in a [[real-time-olap|real-time OLAP]] store. Positioned as the streaming successor to [[etl-vs-elt|ELT]], which only works on bounded batch data.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md`

**Last updated**: 2026-04-18

---

## The pitch

Chapter 11 predicts that the rise of the [[live-data-stack]] will trigger a "back-to-the-future moment for data transformations." The field will shift away from ELT — in-database transformations — "to something that looks more like ETL. We provisionally refer to this as stream, transform, and load (STL)" (source: raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md).

The shape:

1. **Stream** — extraction is continuous and unbounded. Not a scheduled pull; a live subscription.
2. **Transform** — transformations run in flight, on the stream, before landing.
3. **Load** — the result is written to a store that can ingest and serve live data, i.e. [[real-time-olap|real-time OLAP]].

This is structurally ETL, but the E is a stream subscription, the T runs in a stream processor, and the L targets a streaming-friendly store.

## Why not ELT

[[etl-vs-elt|ELT]] became the default in the [[modern-data-stack]] era because:

- Cloud warehouses (Snowflake, BigQuery, Redshift) could transform at massive scale using pure SQL.
- Pushing raw data into the warehouse first preserved optionality and separated responsibilities.
- Warehouse compute was cheap enough to make "just transform in-database" the right call.

But ELT assumes a **batch** warehouse — bounded data, scheduled jobs, set-theoretic SQL. It breaks when data is unbounded, continuously arriving, and latency-sensitive. You can't wait for the next 15-minute batch if the application needs to react in 500ms (source: raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md).

## What stays batch

Reis and Housley explicitly don't kill batch. Batch transformations stay useful for (source: raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md):

- Model training (point-in-time reproducibility, bulk feature computation).
- Quarterly reporting and other infrequent analytical workloads.
- Other workloads where freshness doesn't matter.

But streaming transformation becomes the norm, not the exception.

## The transform step

The transform layer of STL is built on [[stream-processing|stream processors]] (Flink, Spark Structured Streaming, Beam, Pulsar Functions, ksqlDB) and on the semantics of the [[dataflow-model|dataflow model]]. Topics around [[stream-joins|stream joins]], [[windowing]], [[late-arriving-events|late-arriving events]], and [[streaming-queries|streaming queries]] all belong to the STL's T step.

## The load step

The destination of STL is typically a [[real-time-olap|real-time OLAP database]] — Druid, ClickHouse, Rockset, Firebolt. The live data stack also often uses the destination as a feature substrate for ML, dashboards, and application backends (source: raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md).

## Modeling implications

STL forces modeling closer to the source. Chapter 11 predicts "some notion of an upstream definitions layer — including semantics, metrics, lineage, and data definitions — beginning where data is generated in the application. Modeling will also happen at every stage as data flows and evolves through the full lifecycle" (source: raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md). See [[streaming-data-modeling]], [[data-contract]], [[semantic-layer]].

## Cross-book resonance

- **[[derived-data]]** (DDIA Ch 12) — Kleppmann's framing of transformation as maintenance of derived datasets from an authoritative event log. STL is derived-data pipelines productised.
- **[[kappa-architecture]]** — Kreps's all-streaming architecture. STL is the transformation step inside Kappa.
- **[[dataflow-model]]** — Google's unification of batch and streaming. STL assumes this unification as the foundation.

## Related pages

- [[live-data-stack]]
- [[future-of-data-engineering]]
- [[etl-vs-elt]]
- [[stream-processing]]
- [[streaming-queries]]
- [[streaming-data-modeling]]
- [[real-time-olap]]
- [[windowing]]
- [[stream-joins]]
- [[late-arriving-events]]
- [[dataflow-model]]
- [[kappa-architecture]]
- [[derived-data]]
- [[data-transformation]]
