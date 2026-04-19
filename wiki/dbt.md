# dbt

**Summary**: Data Build Tool — a framework for expressing warehouse transformations as Git-managed, templated SQL. Compiles models into CTE-composed SQL the warehouse runs natively. The primary embodiment of the **analytics-engineering-as-code** movement and the SQL-based transformation layer Reis & Housley recommend.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md`

**Last updated**: 2026-04-18

---

## What dbt does

SQL on its own has no natural notion of libraries, reusable code, or proper version control. You can save a query as a view, or UDFs as database objects — but those aren't committed to Git without external CI/CD (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).

dbt fills the gap:

- **Models** are SQL files in a Git repo.
- **Templating** (Jinja) lets one model reference another, injects variables, and customises per-environment.
- **Compilation** turns the templated SQL into warehouse-native SQL with `CREATE TABLE AS ...` / `CREATE VIEW AS ...` / incremental merges.
- **DAG execution** — dbt figures out the dependency order between models and runs them.
- **Testing** — built-in schema and data tests (unique, not-null, relationships, custom).

## Why it matters for the data engineer

Chapter 8 frames dbt as the embodiment of two shifts (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md):

1. **Analytics as code.** SQL transformations become a first-class, version-controlled, reviewed, tested software artifact — not a collection of scripts in a filesystem or UDFs in the warehouse.
2. **Role redistribution.** Analysts and data scientists can write in-database transformations via dbt without a DBA or data engineer intervening on every change. The data engineer's role shifts: set up the repo, the CI/CD pipeline, the testing framework, and the production orchestration. Less direct ETL authorship, more platform work.

## Relationship to other primitives

- **[[common-table-expression|CTEs]].** dbt models are typically expressed as CTE-composed SQL; the templating makes CTEs more reusable than raw SQL would allow.
- **[[materialized-view|Materialization]] strategy.** Each dbt model chooses a materialization: `view`, `table`, `incremental`, `ephemeral`. Incremental models approximate live-table behaviour without warehouse-native live-table support.
- **[[orchestration]].** dbt runs the DAG; Airflow, Dagster, or Prefect invoke dbt. The compiler hands off to the warehouse for actual execution — dbt doesn't process data itself.
- **[[data-lineage]].** Every model declares its sources and refs; lineage is a by-product of the compilation.

## The analytics-engineering role

The rise of dbt coincides with the emergence of the **analytics engineer** as a distinct role — someone who lives in the intersection of data modeling (traditionally data engineer) and business logic (traditionally analyst). Chapter 8 notes this role transformation: "As data tools lower the barriers to entry and become more democratized across data teams, it will be interesting to see how the workflows of data teams change" (source: raw/fundamentals-of-data-engineering/chapter-08-queries-modeling-and-transformation.md).

## Related pages

- [[data-transformation]]
- [[common-table-expression]]
- [[materialized-view]]
- [[data-lineage]]
- [[orchestration]]
- [[software-engineering-for-data]]
- [[metrics-layer]]
- [[user-defined-function]]
