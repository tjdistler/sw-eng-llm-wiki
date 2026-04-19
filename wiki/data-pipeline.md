# Data Pipeline

**Summary**: Reis and Housley's deliberately fluid definition: "a data pipeline is the combination of architecture, systems, and processes that move data through the stages of the [[data-engineering-lifecycle|data engineering lifecycle]]." The term covers everything from a nightly ETL job that lands a monolithic warehouse, to a cloud assemblage that pulls from 100 sources, trains five ML models, and serves them in production — because modern platforms mix every historical pattern (ETL, ELT, [[reverse-etl]], [[data-sharing]]) within a single pipeline.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-07-ingestion.md`

**Last updated**: 2026-04-18

---

## Why the definition is deliberately vague

The authors resist pinning "pipeline" to one era's technology. They note that a good deal of ceremony surrounds data-movement patterns — established ones like ETL, newer ones like ELT, and "new names for long-established practices" like [[reverse-etl]] — and that a modern pipeline typically includes *all of them*. Their framing: as the industry moves away from a monolithic processor with rigid movement rules and toward cloud services assembled "like LEGO bricks," engineers should "prioritize using the right tools to accomplish the desired outcome over adhering to a narrow philosophy of data movement" (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md).

## Where pipelines begin

"Data pipelines begin in source systems, but [[data-ingestion|ingestion]] is the stage where data engineers begin actively designing data pipeline activities" (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md). The [[source-systems]] stage exists upstream — but until the ingestion layer starts pulling or accepting data, there is nothing that counts as *the data engineer's* pipeline.

## Two canonical shapes

Reis and Housley illustrate with two end-points of the range (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md):

- **Traditional ETL pipeline.** Data is ingested from an on-premises transactional system, passed through a monolithic processor, and written into a [[data-warehousing|data warehouse]].
- **Cloud-native pipeline.** Pulls from 100 sources, combines them into 20 wide tables, trains five ML models, deploys them into production, and monitors ongoing performance.

Both are "data pipelines." The pipeline is not a technology — it is the architecture + systems + processes that move data through the lifecycle.

## Fluidity as a design property

Because the definition is intentionally open, a pipeline in practice can include:

- **Pull ingestion** (scheduled [[etl-vs-elt|ETL]] extracts) and **push ingestion** ([[change-data-capture|CDC]], [[webhooks]], event publication) in the same flow.
- [[batch-processing|Batch]] and [[stream-processing|streaming]] alongside each other — in fact Ch 7 is explicit that even streaming pipelines usually have batch components somewhere downstream.
- Both [[etl-vs-elt|ETL and ELT]] stages — extract + load for raw, transform inside the warehouse for curated.
- [[reverse-etl|Reverse ETL]] at the end — pipelines no longer terminate at the warehouse.

## Connection to orchestration

As the pipeline grows, coordinating its stages becomes a first-class problem. Ch 7 names cron jobs as acceptable at low maturity but explicitly brittle as complexity grows; [[orchestration|true orchestration]] — scheduling a **graph** of tasks rather than individual tasks — becomes necessary (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md).

## Related pages

- [[data-engineering-lifecycle]]
- [[data-ingestion]]
- [[etl-vs-elt]]
- [[reverse-etl]]
- [[data-sharing]]
- [[batch-processing]]
- [[stream-processing]]
- [[orchestration]]
- [[change-data-capture]]
- [[data-processing-pipelines]]
