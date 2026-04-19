# Model Drift

**Summary**: ML models degrade over time as the statistical properties of real-world data shift away from what the model was trained on. Chapter 9 lists **monitoring model drift** as one of the ML fundamentals a data engineer should understand — because the data engineer typically owns the pipelines and observability that make drift detection possible.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md`

**Last updated**: 2026-04-18

---

## Why it happens

A model is trained on historical data. The world keeps moving. Over time:

- **Input distributions shift** (feature drift / data drift) — customer behaviour changes, new product lines appear, seasonality patterns evolve.
- **Target distributions shift** (concept drift) — what "good" or "fraud" or "conversion" looks like changes.
- **Label quality changes** — upstream labelling processes change.

The model's predictions become increasingly less accurate without any code changing.

## Chapter 9's framing

Chapter 9 lists "monitoring model drift" among the ML basics a data engineer should be familiar with, alongside feature engineering, feature stores, training/test set management, and hyperparameter handling (source: raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md).

The point isn't that data engineers *own* drift detection — ML engineers typically do that — but that the data engineer's infrastructure choices (pipelines, observability, feature stores) make drift detection feasible or painful. Chapter 9 also names **ML observability** as a tooling category data engineers may interface with.

## What drift detection looks like

The typical instrumented pipeline compares live-inference input distributions and prediction distributions against a baseline (training data, or a rolling window). Statistics monitored include:

- Feature means, variances, quantiles per-feature.
- Prediction distribution (for classifiers, class-probability histograms).
- Input-feature correlations.
- Downstream outcome metrics (conversion, click-through, fraud-catch rate) vs model-predicted values.

Triggers: statistical distance thresholds (KL divergence, population stability index), drop in downstream business metric, alert when outcome lag catches up.

## Data engineer's role

- **Logged inference data.** The data engineer makes sure live inputs and outputs are captured at a volume and schema compatible with drift analysis.
- **Training-serving parity.** Features used in production should be identical to features used at training time — the core [[feature-store|feature store]] promise.
- **Observability plumbing.** The same [[data-observability]] tooling watches for drift as watches for data quality.

## The feedback loop

Chapter 9 notes the broader lifecycle observation: "a data engineer should be aware of feedback loops between the data engineering lifecycle and the broader use of data once it's in the hands of stakeholders." Drift is one of those loops — a signal that upstream reality has changed and the model (or its inputs) must respond (source: raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md).

## Cross-book connections

- **[[data-observability]]** — DODD extended from data quality to model quality; same discipline, different predicate.
- **[[dataops]]** — "data/model drift detection" is explicitly called out in Chapter 2 as a DataOps-automation dimension.
- **[[feature-store]]** — a feature store's versioning and training-serving consistency is a prerequisite for meaningful drift analysis.

## Related pages

- [[feature-store]]
- [[feature-engineering]]
- [[training-test-sets]]
- [[data-observability]]
- [[dataops]]
- [[data-quality]]
- [[data-serving]]
