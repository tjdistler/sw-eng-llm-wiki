# FinOps

**Summary**: A cultural and operational practice that brings engineering, finance, technology, and business teams together to make data-driven decisions about cloud spending. The ninth of Reis and Housley's [[principles-of-good-data-architecture|principles of good data architecture]] — cost is now an architectural characteristic, not an afterthought.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md`, `raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md`

**Last updated**: 2026-04-18

---

## Definitions

Chapter 3 cites two definitions (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md):

**FinOps Foundation**:
> FinOps is an evolving cloud financial management discipline and cultural practice that enables organizations to get maximum business value by helping engineering, finance, technology, and business teams to collaborate on data-driven spending decisions.

**Sorment and Fuller, *Cloud FinOps* (O'Reilly)**:
> The term "FinOps" typically refers to the emerging professional movement that advocates a collaborative working relationship between DevOps and Finance, resulting in an iterative, data-driven management of infrastructure spending (i.e., lowering the unit economics of cloud) while simultaneously increasing the cost efficiency and, ultimately, the profitability of the cloud environment.

The FinOps Foundation was founded only in 2019 — this is a young discipline.

## Why cloud changed the cost story

In an on-prem world, data systems were a **capital expenditure** cycle: buy a system sized for the next several years, balance budget against compute and storage capacity, and live with the sizing until the next refresh (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md).

- **Overbuying** → wasted money
- **Underbuying** → hampered projects; personnel time burned managing load; faster refresh cycles

In the cloud, systems are **pay-as-you-go** and readily scalable. Cost per query, per processing-second, per byte stored. Scale up for high performance, scale down to save money. More efficient *on average* — but spending becomes **dynamic** rather than fixed.

## The new challenge: dynamic spend management

The old engineering discipline was **performance engineering**: maximise performance on a fixed resource budget. The FinOps mindset is different (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md):

- What is the right mix of AWS spot vs on-demand vs reserved instances for a distributed cluster?
- What is the most cost-effective approach for a sizable daily job?
- When should the company switch from pay-per-query to reserved capacity?

Monitoring extends from CPU and latency to **spend**. Serverless function cost, per-query cost, spend spikes — all become alertable signals.

## Graceful failure modes for cost

Just as systems are designed to fail gracefully under excess traffic, they should fail gracefully under excess *spending* (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md). Hard spending limits with graceful shutoff are a legitimate architectural tool.

## Cost attacks

A DDoS blocks access to a web server. A **cost attack** runs up a spending bill to threaten the company's solvency. Chapter 3's canonical example: **excessive downloads from S3 buckets** have driven small startups toward bankruptcy (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md).

Defences when sharing data publicly:

- **Requester-pays** policies (the downloader pays egress, not the bucket owner)
- Monitoring for excessive data access spending, with automatic revocation above a threshold

## FinOps in technology selection (Chapter 4)

Chapter 4 revisits FinOps in the context of [[technology-selection|choosing data technologies]] and sharpens one point (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

> If it seems that FinOps is about saving money, then think again. FinOps is about making money. Cloud spend can drive more revenue, signal customer base growth, enable more product and feature release velocity, or even help shut down a data center.

Chapter 4 also positions FinOps alongside two cost lenses specific to technology selection:

- **[[total-cost-of-ownership|Total Cost of Ownership (TCO)]]** — direct and indirect costs, capex vs opex. Chapter 4 recommends an [[opex-vs-capex|opex-first]] posture centred on the cloud.
- **[[total-opportunity-cost-of-ownership|Total Opportunity Cost of Ownership (TOCO)]]** — what choosing this technology costs you in lost options. Often ignored; Chapter 4 treats it as a "massive blind spot."

All three compose: TCO tells you what you'll pay, TOCO tells you what you'll give up, FinOps operationalises both day-to-day.

## Relationship to other principles

- [[principles-of-good-data-architecture|Principle 3 (architect for scalability)]] — scale-to-zero is FinOps made operational
- [[principles-of-good-data-architecture|Principle 1 (choose common components wisely)]] — common components get FinOps attention because their cost aggregates across the organisation

## Related pages

- [[principles-of-good-data-architecture]]
- [[data-architecture]]
- [[well-architected-framework]]
- [[scalability]]
- [[elasticity]]
- [[data-temperature]]
- [[dataops]]
- [[total-cost-of-ownership]]
- [[total-opportunity-cost-of-ownership]]
- [[opex-vs-capex]]
- [[technology-selection]]
