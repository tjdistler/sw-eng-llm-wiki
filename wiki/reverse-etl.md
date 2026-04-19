# Reverse ETL

**Summary**: Taking processed data from the output side of the [[data-engineering-lifecycle|data engineering lifecycle]] and feeding it back **into source and SaaS systems**. Chapter 2 frames reverse ETL as "a practical reality long viewed as an antipattern" that has become legitimate, essential, and increasingly productised. One of the three main consumption modes of [[data-serving]].

**Sources**: `raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md`, `raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md`

**Last updated**: 2026-04-18

---

## What reverse ETL is

Reverse ETL pushes processed data — analytics results, scored ML models, computed customer segments — from the warehouse **back into production or SaaS systems**. Chapter 2's canonical examples (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md):

- A marketing analyst calculates advertising bids in Excel from warehouse data, then uploads the bids back to Google Ads.
- A company pushes specific metrics from the warehouse to a customer data platform (CDP) or CRM.

## Why it was seen as an antipattern

The traditional data flow goes source → ingestion → warehouse → consumer (analyst). Reverse ETL **inverts** that: the warehouse becomes a source for the operational system. Historically this was often "entirely manual and primitive" — spreadsheets, ad-hoc scripts — and it was the kind of pipeline nobody wanted to claim (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

## Why it's now legitimate

Chapter 2 argues it's "beneficial and often necessary." The shift is driven by (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md):

- The rise of SaaS and external platforms that businesses rely on operationally.
- Vendors embracing the pattern and productising it — **Hightouch, Census** are named.
- The general recognition that transformed data has value *inside operational systems*, not only in the warehouse.

## The future: stream-based reverse ETL?

Some engineers argue reverse ETL can be eliminated by handling data transformations directly in an **event stream** and sending those events back to source systems as they are produced. Chapter 2's view: widespread adoption of that pattern is another matter, and "realizing widespread adoption of this pattern across businesses is another matter."

Regardless of implementation: "transformed data will need to be returned to source systems in some manner, ideally with the correct lineage and business process associated with the source system" (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

## Chapter 9 — the lead-scoring example

Chapter 9 makes the use case concrete (source: raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md):

1. Pull customers and orders from a CRM into the warehouse.
2. Train a lead-scoring model on warehouse data.
3. Return scored leads to the sales team.

The sales team does its work inside the CRM. Emailing Excel files of scored leads or giving them a dashboard loses the context. Loading the scores **back into the CRM** puts the data where the user already is — the lowest-friction path.

## "Bidirectional Load and Transform"

Chapter 9's half-joking proposal: the term should be *bidirectional load and transform (BLT)*, not reverse ETL, since "the term reverse ETL doesn't quite accurately describe what's happening." The term has stuck in the industry regardless, so the authors use it throughout the book (source: raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md).

## Ways to serve with reverse ETL

Chapter 9 is pragmatic: roll your own or (recommended) use an off-the-shelf commercial or OSS option. Warning: "the reverse ETL space is changing extremely quickly. No clear winners have emerged, and many reverse ETL products will be absorbed by major clouds or other data product vendors. Choose carefully" (source: raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md).

## The feedback-loop hazard

The distinctive Chapter 9 caveat: **reverse ETL creates feedback loops**, and bad ones can burn a lot of money fast.

Chapter 9's worked warning: download Google Ads data, use a model to compute new bids, load bids back into Google Ads, collect the new data, retrain, repeat. If the bid model has a bug that trends bids upward, each iteration amplifies the error — "you can quickly waste massive amounts of money." Monitoring and guardrails are mandatory (source: raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md).

The same shape appears for any closed-loop reverse-ETL system: pricing models that feed their own outputs, recommendation engines that amplify their biases, budget optimisers that lock into bad local optima.

## Cross-book connections

Reverse ETL maps onto several patterns from other books:

- **[[serving-state-from-edm]]** / **[[materialized-state]]** (Bellemare) — the event-driven analogue: each consuming service derives its own view from the producer's event stream, which doubles as a mechanism for "serving back" into operations.
- **[[data-liberation]]** (Bellemare) — producing event streams from a monolith's internal data is the forward direction; reverse ETL is the *return path* from warehouse back to operational stores. Together they close the loop.
- **[[event-sinking]]** (Bellemare) — sinking an event stream back into a consumer's database is essentially streaming reverse ETL for the event-driven case.

## Related pages

- [[data-serving]]
- [[data-engineering-lifecycle]]
- [[etl-vs-elt]]
- [[data-warehousing]]
- [[serving-state-from-edm]]
- [[event-sinking]]
- [[data-lineage]]
