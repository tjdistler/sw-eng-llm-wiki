# Training and Test Sets

**Summary**: The canonical partition of labelled data for machine learning: the **training set** is used to fit a model; the **test set** is held out and used only to estimate real-world performance. Chapter 9 names training/test sets among the ML basics a data engineer should understand because DE infrastructure — pipelines, [[feature-store|feature stores]], and data governance — determines whether these splits can be built correctly and reproducibly.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md`

**Last updated**: 2026-04-18

---

## What they are

The standard ML split:

- **Training set** — the data the model learns from. The model adjusts its parameters to minimise error on this set.
- **Test set** — the held-out data the model never sees during training. Evaluated on the test set once per model version to estimate real-world generalisation.
- **Validation set** (a third partition, often between) — used for hyperparameter tuning and model selection without contaminating the test set.

## Why the DE cares

Chapter 9 lists training/test set handling among the ML fundamentals a DE should know, alongside [[feature-engineering]], [[feature-store|feature stores]], [[model-drift]] monitoring, and hyperparameter management (source: raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md).

The data engineer typically owns infrastructure that *makes* correct train/test splits possible:

- **Time-consistent features.** A feature at training time must be identical to the same feature at inference time — point-in-time correctness. The [[feature-store]] exists in part to guarantee this.
- **No leakage across splits.** Data from "the future" must not leak into training. Time-based splits require pipelines that can reconstruct feature values as of a past timestamp.
- **Reproducibility.** Versioned feature pipelines and versioned datasets so a model trained six months ago can be retrained identically.
- **Scale.** Large training sets may require distributed storage and compute; the DE sets up the pipelines.

## The leakage trap

The most common (and most damaging) failure mode: training on data that contains information the model wouldn't have at inference time. Causes:

- A feature derived from a post-outcome field (e.g., "number of refunds" used to predict churn, but refunds happen after churn).
- Not partitioning by time when the real-world inference is on future data.
- Applying normalisation/scaling parameters computed over the full dataset before splitting.
- Oversampling or upsampling before splitting.

Chapter 9 doesn't enumerate these, but all of them sit at the data-engineering / ML-engineering boundary Chapter 9 repeatedly highlights.

## Batch vs online learning

Chapter 9 notes the difference between batch and online learning (source: raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md):

- **Batch training** fits with offline fit-once-evaluate-once workflows using static train/test splits.
- **Online training** updates the model continuously with streaming data — the "train/test" concept blurs into ongoing evaluation and rolling windows.

Streaming features from the [[feature-store]] are the bridge.

## Cross-book connections

- **[[feature-store]]** — point-in-time feature correctness is the feature-store's core value proposition for training.
- **[[model-drift]]** — drift analysis compares live inference to a held-out reference distribution; the same discipline applied continuously.

## Related pages

- [[feature-store]]
- [[feature-engineering]]
- [[model-drift]]
- [[data-serving]]
- [[data-quality]]
- [[data-observability]]
