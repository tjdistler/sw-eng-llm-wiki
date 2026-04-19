# Metrics Layer

**Summary**: A semantic layer that encodes business logic as a library of named metrics, **independent of both transformations below and BI tools above**. Analysts and dashboards reference metrics; the layer generates queries and sends them to the warehouse. Reis & Housley name it as an emerging alternative to encoding business logic inside ETL scripts.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md`, `raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md`

**Last updated**: 2026-04-18

---

## The problem it solves

[[derived-data|Derived data]] — things like "profit after marketing costs" — traditionally lives inside ETL scripts that generate reporting tables. When the business logic changes (say, the attribution model), the change must be propagated through many ETL scripts. "ETL scripts are notorious for breaking the DRY principle" (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).

The alternative — having analysts compute the metric in each reporting query — is worse: getting analysts to consistently update their reporting queries for a business-logic change is "well-nigh impossible."

## The metrics-layer answer

Push business logic into a **metrics layer** that sits independently of the transformation layer (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md):

- Analysts reference a metric by name (`profit_after_marketing`).
- The metrics layer contains the authoritative definition.
- The layer **generates queries** from the metric definition and sends them to the warehouse.
- The warehouse does the heavy lifting.

A change to a metric definition updates every consumer at once. No ETL-script propagation problem.

## Where in the lifecycle

The metrics layer sits between [[data-transformation|transformation]] and [[data-serving|serving]]:

```
sources → ETL/ELT → warehouse tables → metrics layer → BI tool / dashboard
```

It's neither transformation (it doesn't persist new data) nor serving (it's not a user-facing interface) — it's a logical layer that shapes queries to the warehouse on behalf of consumers.

## Chapter 9 — query quality vs data quality

Chapter 9 reinforces the metrics-layer argument by separating two problems that tend to get conflated (source: raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md):

- **Data quality** — characteristics of the data itself and techniques to filter or improve bad data.
- **Query quality** — whether the query logic returns accurate answers to business questions. "Writing high-quality ETL queries and reporting is time-intensive, detailed work."

Powerful query engines don't fix bad queries — they just return bad results faster. The metrics layer is the structural fix for query quality at the organisational level: authoritative business logic in one place, referenced everywhere.

Chapter 9 calls the question the metrics layer solves "a central question in analytics that has plagued organizations since people have analyzed data: 'Are these numbers correct?'"

See also [[semantic-layer]] — Chapter 9 treats metrics layer and semantic layer as conceptually identical; *headless BI* is a closely related term.

## Reis & Housley's forecast

"While it's still early days, expect to see semantic and metrics layers becoming more popular and commonplace in data engineering and data management" (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).

The book's Chapter 11 takes this further: the metrics layer could become part of a "live data stack" where business logic, pipelines, and analytics workflows sit together on top of source systems via streaming, rather than being artificially separated into source and analytical tiers.

## Why this belongs in DataOps / data management

A metrics layer is the data-management answer to the question: *where does the authoritative business definition live?*

- Not in transformations (duplicated across ETL scripts).
- Not in BI tools (tool-specific, not reusable).
- In a dedicated layer with version control and governance.

It aligns with the [[data-governance|governance]] / [[data-catalog|catalog]] story — a metric in the layer is a governed artifact with an owner, a definition, and a lineage.

## Related pages

- [[data-transformation]]
- [[derived-data]]
- [[data-governance]]
- [[data-catalog]]
- [[dbt]]
- [[streaming-data-modeling]]
- [[semantic-layer]]
- [[data-definitions-and-logic]]
- [[trust-in-data]]
- [[data-serving]]
