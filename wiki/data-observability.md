# Data Observability

**Summary**: Observability applied to data pipelines and datasets — logging, monitoring, alerting, and tracing to detect data problems (silent data corruption, schema drift, late arrivals, model drift) before they reach consumers. One of the three pillars of [[dataops|DataOps]] alongside automation and incident response. Reis and Housley cite Petrella's **Data Observability Driven Development (DODD)** as a test-driven-development-like discipline for data.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md`

**Last updated**: 2026-04-18

---

## Why data observability matters

Chapter 2's tagline: **"Data is a silent killer."** Bad data can linger in reports for months or years; executives make key decisions from it and discover the error much later. Systems creating report data stop working and the data team doesn't notice until stakeholders ask why reports are late. The long-run result is lost trust, splinter data teams, inconsistent reports, and silos (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

## What to observe

Chapter 2's list: "observability, monitoring, logging, alerting, and tracing are all critical to getting ahead of any problems along the data engineering lifecycle" (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

The specific things to watch go beyond standard application observability. At minimum (implied by Chapter 2 and elaborated in the quality chapter):

- Row counts, null rates, cardinality distributions.
- Schema drift — does the set of columns / types match expectations?
- Freshness — how recently did the dataset last update?
- Pipeline success/failure and duration.
- Model drift for ML-serving datasets.
- Data-quality rule violations.

## Statistical process control

Chapter 2 recommends incorporating **statistical process control (SPC)** to understand whether events being monitored are out of line and which incidents are worth responding to. SPC is one of the three disciplines DataOps inherits from (alongside Agile and DevOps) (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

## DODD — Data Observability Driven Development

The chapter cites **Andy Petrella's DODD** framework, drawing an analogy to test-driven development in software (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md):

> "The purpose of DODD is to give everyone involved in the data chain visibility into the data and data applications so that everyone involved in the data value chain has the ability to identify changes to the data or data applications at every step — from ingestion to transformation to analysis — to help troubleshoot or prevent data issues."

DODD makes data observability a **first-class consideration** in the lifecycle, applied from development through testing into production.

DODD is closely tied to [[data-lineage|data lineage]] — observability signals flow along the lineage graph, and lineage gives you the dependency direction to attribute defects.

## Cross-book connections

- [[monitoring-and-observability]] (SRE) — the software-system parent concept.
- [[four-golden-signals]] (SRE) — the analogous framing for services.
- [[data-validation-pipelines]] — the concrete test-at-the-boundary mechanism DODD recommends.
- [[pipeline-monitoring-problems]] (SRE Ch 25) — specific failure modes of observability in periodic batch pipelines.

## Related pages

- [[dataops]]
- [[data-quality]]
- [[data-lineage]]
- [[monitoring-and-observability]]
- [[data-validation-pipelines]]
- [[data-engineering-lifecycle]]
