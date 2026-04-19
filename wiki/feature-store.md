# Feature Store

**Summary**: A relatively new class of data tool at the intersection of data engineering and ML engineering. A feature store centralises **feature history and versions**, enables feature **sharing across teams**, and provides **operational and orchestration capabilities** like backfilling. Chapter 2 describes feature stores as "designed to reduce the operational burden for ML engineers" — with data engineers part of the core support team.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md`, `raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md`, `raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md`, `raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md`

**Last updated**: 2026-04-18

---

## What a feature store does

Chapter 2 names four capabilities (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md):

1. **Feature history and versioning.** A time-series store of feature values, with versioning so you can reproduce historical training runs.
2. **Feature sharing across teams.** One team's engineered feature becomes reusable by other teams — avoids the antipattern where every team independently engineers "the same" feature slightly differently.
3. **Basic operational capabilities.** Monitoring, SLAs, access controls.
4. **Orchestration capabilities** — particularly **backfilling** historical values for a newly added feature.

## Where it sits in the lifecycle

The feature store is a [[data-serving|serving]]-stage tool specifically for ML consumers, built on top of an organisation's existing [[data-transformation|transformation]] and [[data-storage-stage|storage]] infrastructure. It doesn't replace the warehouse or the lake — it sits alongside them, specialised for the ML access pattern.

## Why it straddles data engineering and ML engineering

The ownership story is deliberately fuzzy: "data engineers are part of the core support team for feature stores to support ML engineering" (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md). Feature engineering itself requires domain expertise and data-science experience, but operationalising feature pipelines — automating them, backfilling them, monitoring their freshness, serving them at low latency — is the data engineer's bread and butter.

The chapter uses this as an illustration of its broader point: "the boundaries between data engineering, ML engineering, and analytics engineering can be fuzzy," and that decision about where to draw the line is "a critical organizational decision."

## Chapter 8 — feature engineering as a transformation

Chapter 8 places feature engineering firmly inside the transformation stage. See [[feature-engineering]] for the fuller treatment. Two points Chapter 8 adds to the Chapter 2 framing (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md):

- The data engineer's role in **automating** feature pipelines, once data scientists have figured out feature shape, is the canonical example of the data-engineering / ML-engineering fuzzy boundary.
- A feature store centralizes history, sharing, operational concerns, and — critically — **backfilling**, so when a new feature is defined it can be computed over the historical window for model training.

## Chapter 9 — DE/ML collaboration surface

Chapter 9 returns to the feature store as an integration point between data engineering and ML engineering: "the data engineering lifecycle intersect[s] with the ML lifecycle" in part through whether the DE is "responsible for interfacing with or supporting ML technologies such as feature stores or ML observability" (source: raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md).

The factory-loom example: streaming data feeds feature computations; DE and ML engineers design a featurisation pipeline together; DE implements and maintains it; ML engineers automate training and deployment. The feature store is the durable artifact of that collaboration.

## Chapter 11 — substrate for the ML feedback loop

Chapter 11's [[live-data-stack]] prediction calls out feature stores as one of the key integration technologies for the coming [[data-application-fusion|data-application fusion]]: "feature stores may also play a similar role for ML use cases" alongside the mixed OLTP/OLAP databases that unify application and analytical storage (source: raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md).

In the live data stack the feature store is the durable backbone of the tight application-ML feedback loop:

- Streaming pipelines produce features continuously.
- The feature store makes features available for real-time inference.
- Applications consume inference results, produce new events, and the loop turns again.
- Training uses the same feature store (time-travelled) for reproducibility.

Chapter 11 also predicts a new **ML-focused engineer** role straddling DE and MLE (see [[titles-will-morph]]) — the feature store is a central tool for that role.

## Cross-book connections

- [[data-transformation]] — featurisation is a specific transformation mode.
- [[data-serving]] — feature stores serve features at both training-time (batch) and inference-time (online, low-latency).
- [[data-quality]] — bad-quality inputs produce bad features; quality assessment "is developed in close collaboration with teams consuming the data."

## Related pages

- [[feature-engineering]]
- [[data-serving]]
- [[data-transformation]]
- [[data-engineering-lifecycle]]
- [[data-quality]]
- [[data-catalog]]
- [[model-drift]]
- [[training-test-sets]]
- [[live-data-stack]]
- [[data-application-fusion]]
- [[titles-will-morph]]
- [[future-of-data-engineering]]
