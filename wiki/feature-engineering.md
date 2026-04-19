# Feature Engineering

**Summary**: The transformation activity that produces **features** — model-ready inputs — from raw data for ML training and inference. Reis & Housley frame it as combining domain expertise with data-science experience: the data scientist figures out the shape, the data engineer automates the pipeline.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md`, `raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md`

**Last updated**: 2026-04-18

---

## What feature engineering is

A **feature** is an input to a machine-learning model — typically a number or a categorical encoding. Feature engineering is the transformation step that converts raw data (orders, clicks, sensor readings, text) into features the model can consume.

It's one of the lifecycle's specialisations of [[data-transformation|transformation]] — distinct from standard ETL because the target is not a reporting schema but a training / inference-ready feature matrix.

## Chapter 2's framing

Chapter 2 calls feature engineering "a dark art" (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md): it requires domain expertise *and* data-science experience. The data engineer's contribution is to **automate** the featurisation pipelines once data scientists have figured out the shape of each feature.

That division of labour is the clearest statement in the book of where data engineering ends and ML engineering begins. It's also the reason the [[feature-store]] exists.

## Typical feature-engineering operations

- **Parsing and type conversion** — raw strings into numbers, timestamps, durations.
- **Normalization / scaling** — zero-mean / unit-variance, min-max, robust scaling.
- **Encoding** — one-hot, target encoding, hashing, embedding lookup.
- **Aggregation** — user-level rolling counts, sums, rates over a window.
- **Joining** — enrich an event with profile attributes, product attributes, external reference data.
- **Time-series features** — lags, rolling statistics, seasonality indicators.
- **Text / image features** — tokenization, tf-idf, embedding extraction.

Many of these operations are just [[data-transformation|transformations]] with a particular target audience.

## Why a dedicated store exists

Reis & Housley treat feature engineering and the [[feature-store|feature store]] together:

- **Feature history and versioning** — reproduce training runs.
- **Sharing across teams** — prevent every team from engineering "the same" feature slightly differently.
- **Backfilling** — compute a new feature for historical events so models can train on it.
- **Low-latency online serving** — the same feature used at training time is available at inference time.

See [[feature-store]].

## The data engineer's role

Chapter 2 and Chapter 8 (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md) both stress the data engineer's contribution:

- **Pipeline automation.** Get features computed reliably, on schedule, with lineage.
- **Quality.** Features are only as good as their inputs; the [[data-quality]] mandate applies.
- **Backfill orchestration.** When a new feature is defined, compute it over the historical window so models can use it.
- **Low-latency serving path.** The same computation, reusable at inference time with tight SLOs.

The book's organizing statement: "the boundaries between data engineering, ML engineering, and analytics engineering can be fuzzy" — feature engineering is the canonical example.

## Cross-book connections

- [[derived-data]] — DDIA's general framing; features are derived data.
- [[stream-processing]] — streaming feature computation (user-level rolling aggregates) is an important sub-case.

## Related pages

- [[feature-store]]
- [[data-transformation]]
- [[derived-data]]
- [[data-quality]]
- [[stream-processing]]
- [[data-serving]]
