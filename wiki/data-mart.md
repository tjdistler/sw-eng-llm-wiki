# Data Mart

**Summary**: A refined subset of a [[data-warehousing|data warehouse]] designed to serve analytics and reporting for a single suborganisation, department, or line of business — typically with its own additional stage of transformation tuned for that audience.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md`

**Last updated**: 2026-04-18

---

## Why data marts exist

Chapter 3 gives two reasons (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md):

1. **Accessibility for analysts and report developers** — the data is pre-shaped for the audience's questions
2. **A second transformation stage beyond initial ETL/ELT** — complex joins and aggregations can be materialised ahead of queries, improving live-query performance when raw data is large

Each department has its own mart tuned to its needs: Marketing's mart, Finance's mart, Product's mart. The enterprise warehouse remains the source of truth; the mart is the performance-and-usability layer.

## Relationship to the warehouse

Chapter 3 situates the mart as the downstream companion of the warehouse in the ETL/ELT → warehouse → mart flow (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md). The same chapter introduces [[etl-vs-elt|ELT]] as the transformation pattern that increasingly supplants ETL; in either case, the mart is populated downstream of the warehouse.

Modeling for data marts is the subject of Chapter 8 (Queries, Modeling, and Transformation); see [[data-modeling]] for the Kimball / Inmon / Data Vault framing.

## Related pages

- [[data-warehousing]]
- [[etl-vs-elt]]
- [[data-modeling]]
- [[analytics]]
- [[data-serving]]
- [[data-architecture]]
