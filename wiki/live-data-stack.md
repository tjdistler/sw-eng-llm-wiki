# Live Data Stack

**Summary**: Reis and Housley's name for the streaming-first successor to the [[modern-data-stack]]. The live data stack uses streaming pipelines and [[real-time-olap|real-time OLAP databases]] to fuse applications, analytics, and ML in real time — democratising the kind of data architecture currently used only at elite tech companies (TikTok, Uber, DoorDash, Google). The central prediction of Chapter 11, and the chapter's most speculative claim.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md`

**Last updated**: 2026-04-18

---

## What it is

The **live data stack** is the predicted successor to the [[modern-data-stack]]. Where the MDS is a cloud-repackaged [[data-warehousing|data warehouse]] architecture built around batch ELT, the live data stack is built around streaming ingestion, [[stream-transform-load|streaming transformation]], [[real-time-olap|real-time OLAP]], and tight integration with the applications that produce and consume the data (source: raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md).

In the chapter's words, the live data stack will "fuse real-time analytics and ML into applications by using streaming technologies, covering the full data lifecycle from application source systems to data processing to ML, and back."

## Why the MDS isn't enough

Reis and Housley applaud the [[modern-data-stack]] but call it unmodern: it's "basically a repackaging of old data warehouse practices using modern cloud and SaaS technologies" (source: raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md). Limitations:

- **Batch-oriented** — treats data as bounded; fundamentally lags the world.
- **Internal-facing** — powers BI and analytics, not live user experiences.
- **Disjointed from applications** — data is generated "with no regard for how it will be used for analytics"; lots of duct tape between stacks.

Many dashboards answer **what** and **when** questions. Reis and Housley's provocation: "If the action is repetitive, it is a candidate for automation." Why look at a report to decide to act when you can just automate the action on the event?

## What drives the shift

The live data stack exists today — at elite tech companies, as custom-built infrastructure. TikTok feels like magic because miniscule-latency ML and data processing happen behind every click. The prediction is that cloud-native, easy-to-use versions of these technologies will **democratise** this capability the way the MDS democratised cloud warehousing (source: raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md).

## Core technologies

The chapter names two foundation technologies (source: raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md):

- **Streaming pipelines** — unbounded, continuous extraction and transformation. See [[stream-processing]], [[data-pipeline]], [[stream-transform-load]].
- **[[real-time-olap|Real-time analytical databases]]** — fast ingestion, subsecond queries, enrichment against historical datasets. Named examples: Druid, ClickHouse, Rockset, Firebolt.

Surrounding ideas:

- **[[streaming-data-modeling|Streaming-friendly data modeling]]** — upstream definitions at the source application; modeling at every stage as data flows.
- **[[data-application-fusion|Application/data fusion]]** — application stacks become data stacks and vice versa.
- **ML integration** — tight feedback loops between applications and models, powered by [[feature-store|feature stores]] for ML use cases and new OLTP+OLAP hybrid databases for general use.

## What changes for the data engineer

- Batch ingestion becomes rare; Reis and Housley predict "we'll eventually look at batch ingestion the same way we now look at dial-up modems." See [[ingestion-frequency]].
- ELT becomes STL — [[stream-transform-load]].
- The [[data-engineering-lifecycle]] itself doesn't change; the time between stages collapses drastically.
- Modeling, metrics, definitions, lineage move closer to the source — "upstream definitions layer." See [[data-definitions-and-logic]] and [[semantic-layer]].
- Engineers work with managed stream processors (Kinesis Data Analytics, Dataflow) and a new generation of orchestration tools that stitch them together (source: raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md).

## What stays the same

Batch doesn't disappear. The chapter explicitly reserves it for model training, quarterly reporting, and similar ad-hoc analytical work. [[data-warehousing|Warehouses]] and [[data-lake|data lakes]] still house the "large amounts of data and perform ad hoc queries" — they just aren't the backend of the live data stack (source: raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md).

## Honest speculation

The chapter's own hedge: this paradigm shift is real but might stall. "Perhaps the trend toward real-time data will stall once again, with most companies continuing to focus on basic batch processing" (source: raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md). It's the most speculative prediction in Chapter 11 — more so than the lifecycle-survives or simplification-continues claims.

## Relation to other architectures

- **[[kappa-architecture]]** — Kreps's 2014 all-streaming alternative to Lambda. The live data stack is Kappa applied to a broader application layer, not just to analytics.
- **[[dataflow-model]]** — Google/Beam "batch as a special case of streaming." The theoretical backbone of live-data-stack transformations.
- **[[unbundling-databases]]** (DDIA Ch 12) — Kleppmann's decomposition of the database into event logs, derived indexes, and stream-processing glue. The live data stack is this vision packaged as cloud products.
- **[[event-driven-architecture]]** — the general pattern; the live data stack is EDA with real-time analytics and ML baked in.

## Related pages

- [[future-of-data-engineering]]
- [[modern-data-stack]]
- [[real-time-olap]]
- [[stream-transform-load]]
- [[data-application-fusion]]
- [[streaming-data-modeling]]
- [[stream-processing]]
- [[data-engineering-lifecycle]]
- [[ingestion-frequency]]
- [[kappa-architecture]]
- [[dataflow-model]]
- [[unbundling-databases]]
- [[event-driven-architecture]]
- [[feature-store]]
