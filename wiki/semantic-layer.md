# Semantic Layer

**Summary**: A layer that consolidates business definitions and logic in a reusable fashion — "write once, use anywhere." Chapter 9 describes it as an object-oriented approach applied to metrics, calculations, and logic; *headless BI* is a closely related term. Conceptually extremely similar to a [[metrics-layer|metrics layer]]; Chapter 9 treats "semantic layer" and "metrics layer" as nearly synonymous.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md`, `raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md`

**Last updated**: 2026-04-18

---

## The problem

Business logic that computes "profit after marketing costs," "churn," or "customer lifetime value" tends to live in multiple places simultaneously: ETL scripts, BI calculated fields, analyst SQL. Every place has a slightly different version, and the definitions drift until nobody can tell which report is "right." See [[data-definitions-and-logic]] and [[trust-in-data]] for why that drift is catastrophic (source: raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md).

## The semantic-layer answer

Consolidate logic into a single layer (source: raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md):

- Authoritative definitions live in one place.
- Consumers (reports, dashboards, ad-hoc queries) reference definitions by name.
- The layer compiles references into SQL (or similar) and runs them against the warehouse.
- A change to the definition propagates to every consumer at once.

Chapter 9's framing: this is "an object-oriented approach to metrics, calculations, and logic."

## Two concrete examples

Chapter 9 names two tools in the space (source: raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md):

- **Looker (LookML).** Users define virtual, complex business logic in LookML. Reports point to the LookML definition; Looker generates SQL queries from the definition, pushes them down to the warehouse, and caches results in the Looker server or the database for large result sets.
- **[[dbt|dbt]].** Defines SQL data flows and standard metric definitions similarly, but runs exclusively in the transform layer. dbt can be orchestrated like a data pipeline — it's a broader analytics-engineering tool than a pure semantic layer.

## Query quality vs data quality

Chapter 9 draws a distinction the semantic layer operationalises (source: raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md):

- **Data quality** — characteristics of the data itself; how to filter or improve bad data. See [[data-quality]].
- **Query quality** — whether the query logic is correct; whether it returns accurate answers to business questions.

The semantic layer tackles query quality at the organisational level: even if every analyst is skilled, they won't produce identical SQL for "net profit" without a shared definition to bind to.

## "Are these numbers correct?"

Chapter 9's framing of the problem the layer solves: *the* central question that has plagued analytics forever — "are these numbers correct?" The semantic layer's long-term payoff is making that question answerable by pointing at a canonical definition, not by re-deriving the logic every time (source: raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md).

## Relationship to metrics-layer

Chapter 9: "Fundamentally, a metrics layer is a tool for maintaining and computing business logic. (A semantic layer is extremely similar conceptually, and headless BI is another closely related term.)"

For wiki purposes:

- **[[semantic-layer]]** (this page) — the broader umbrella: all business semantics, definitions, and derivation logic in one reusable place.
- **[[metrics-layer]]** — a narrower instance focused on metrics specifically.

In practice the two terms are used interchangeably.

## Reis & Housley's forecast

Chapter 8's forecast (carried into Chapter 9): "expect to see semantic and metrics layers becoming more popular and commonplace in data engineering and data management" — and the authors expect these layers to move "upstream toward the application" over time (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).

## Related pages

- [[metrics-layer]]
- [[dbt]]
- [[data-definitions-and-logic]]
- [[trust-in-data]]
- [[data-quality]]
- [[data-governance]]
- [[data-serving]]
- [[business-analytics]]
