# Business Analytics

**Summary**: Reis & Housley's Chapter 9 category for using **historical and current data to make strategic decisions**. Decisions tend to factor in long-term trends, with a mix of statistical analysis, domain expertise, and human judgement. Business analytics is "as much an art as a science." Splits into three common sub-activities: dashboards, reports, and ad-hoc analysis.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md`

**Last updated**: 2026-04-18

---

## What it is

Business analytics "uses historical and current data to make strategic and actionable decisions" — the classic BI use case. Long-term trends, board meetings, quarterly reviews, supply-chain investigations. Contrast with [[operational-analytics]] (immediate-action, real-time) and [[embedded-analytics]] (customer-facing) (source: raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md).

## The three sub-activities

Chapter 9 names three distinct practices that a business analyst does:

### 1. Dashboards

"A dashboard concisely shows decision makers how an organization is performing against a handful of core metrics, such as sales and customer retention." Like a car dashboard — a single readout of the critical things you need to know. Organisations typically have multiple layered dashboards (C-level overview; direct-report views; team OKR views). Tools: Tableau, Looker, Sisense, Power BI, Apache Superset/Preset (source: raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md).

Once a dashboard is relied upon, the analyst's steady-state work becomes adding metrics and investigating metric anomalies.

### 2. Reports

"The goal of a report is to use data to drive insights and action." Chapter 9's worked example: a retailer asks why women's running shorts have a high return rate; the analyst queries the warehouse, aggregates return-code data, discovers fabric quality is the cause, and publishes findings to manufacturing and QC.

Reports tend to start as ad-hoc requests. If findings are impactful, they get formalised into a recurring report or dashboard.

### 3. Ad-hoc analysis

One-off questions. The running-shorts investigation starts as an ad-hoc — "why is return rate up?" — and becomes a report only because the findings mattered.

Tools for reports and ad-hoc analysis overlap with dashboards but extend to Excel, Python, R-based notebooks, raw SQL.

## The feedback loop

Analysts feed findings back to data engineers: quality issues, reliability problems, new dataset requests. In the running-shorts example, manufacturing offered supply-chain data; data engineers ran a project to ingest it; analysts then correlated garment serial numbers with fabric suppliers and found the root cause in one specific supplier. The factory stopped using that supplier (source: raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md).

This loop is Chapter 9's archetype of how analytics produces business impact.

## How the data is served

"Business analytics is frequently served in batch mode from a [[data-warehousing|data warehouse]] or a [[data-lake|data lake]]. This varies wildly across companies." Update cadences vary from every second to once a week. Key caveat:

> The frequency of ingestion sets a ceiling on downstream frequency. If streaming applications exist for the data, it should be ingested as a stream even if some downstream processing and serving steps are handled in batches. (source: raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md)

## Backend considerations

- **Where does the BI tool process?** Some store data in their own internal layer (Tableau-style). Others push queries down to the warehouse ([[federated-query|Looker-style]], via LookML — see [[semantic-layer]] / [[metrics-layer]]).
- **Pushdown trade-offs.** Using OLAP power = full expressiveness, but cost / access-control / latency complications.

## Cross-book connections

- **[[cross-service-analytics]]** (Newman) — how to do business analytics across microservice boundaries; the warehouse is the standard destination.
- **[[oltp-vs-olap]]** — BI is the archetypal OLAP workload.

## Related pages

- [[analytics]]
- [[operational-analytics]]
- [[embedded-analytics]]
- [[data-warehousing]]
- [[data-serving]]
- [[semantic-layer]]
- [[metrics-layer]]
- [[dbt]]
