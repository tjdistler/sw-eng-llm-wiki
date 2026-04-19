# Data Definitions and Logic

**Summary**: The correctness of data goes beyond faithful reproduction of source values — it must also encode consistent **meanings** (who is a "customer"?) and consistent **derivation rules** (how is "net profit" calculated?). Chapter 9 warns that when definitions and logic become tribal knowledge, anecdote replaces insight and trust evaporates.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md`

**Last updated**: 2026-04-18

---

## Two halves

Chapter 9 separates what everyone often conflates (source: raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md):

- **Data definition** — the meaning of a term across the organisation. *Customer* must have a single precise meaning; when it varies across departments, those variants must be documented and discoverable.
- **Data logic** — the formulas for deriving metrics. Churn, gross sales, customer lifetime value, net profit — each is a computation with a specific set of inputs, filters, and exclusions. Logic encodes definitions and the statistical-calculation details.

Both must be baked into the pipeline, not left as oral tradition.

## The tribal-knowledge failure mode

"Frequently, we see data definitions and logic taken for granted, often passed around the organization in the form of tribal knowledge. Tribal knowledge takes on a life of its own, often at the expense of anecdotes replacing data-driven insights, decisions, and actions" (source: raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md).

Signals you're living in this failure:

- Two dashboards claim different numbers for the same metric and nobody can say which is correct.
- A new hire keeps producing "wrong" answers until someone pulls them aside and explains the unwritten exclusion rule.
- A metric's definition was set by an analyst who has since left.

## Where to encode them

Chapter 9 names two locations (source: raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md):

1. **A [[data-catalog|data catalog]]** — the discoverable, governed, documented home for the *definitions*.
2. **Systems of the data engineering lifecycle** — the pipelines, warehouses, BI tools, and (increasingly) [[metrics-layer|metrics layers]] where the *logic* is expressed as code.

Definitions are served implicitly every time a query or dashboard runs against the data — correct logic is what makes the numbers right without the consumer having to re-derive them.

## The semantic-layer answer

Chapter 9 points directly to the [[semantic-layer|semantic layer]] (and [[metrics-layer|metrics layer]]) as the best tool for consolidating business definitions and logic reusably: "write once, use anywhere." This is an object-oriented approach applied to metrics, calculations, and logic (source: raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md).

Without it, definitions and logic end up duplicated across ETL scripts, BI tool-specific calculated fields, and ad-hoc analyst SQL — the classic DRY violation that breaks down the moment a definition changes.

## Relationship to data modeling

Chapter 9 calls out [[data-modeling]] (Chapter 8) as "incredibly useful to capture data definitions and logic in a way that's understandable and usable by multiple end users." A [[star-schema]] or [[kimball-model|Kimball-style]] model is in part a physical representation of the business's shared definitions.

## Cross-book connections

- **[[master-data-management]]** — the formal discipline for maintaining golden records across the organisation; the organisational counterpart to data definitions.
- **[[bounded-context]]** — DDD's idea that the same term can mean different things in different contexts; the exception that proves Chapter 9's rule. Where definitions genuinely differ, the catalog must make those distinctions explicit.

## Related pages

- [[trust-in-data]]
- [[semantic-layer]]
- [[metrics-layer]]
- [[data-catalog]]
- [[data-modeling]]
- [[data-governance]]
- [[master-data-management]]
- [[data-serving]]
