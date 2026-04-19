# Analytics

**Summary**: The core of most data serving — generating reports, dashboards, and ad-hoc analysis. Reis & Housley split analytics into three varieties that differ sharply in audience, request rate, and access-control complexity: **business intelligence (BI)**, **operational analytics**, and **embedded / customer-facing analytics**. This page is the hub; each sub-variety has its own deeper page.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md`, `raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md`

**Last updated**: 2026-04-18

---

## The first question: use case and user

Chapter 9 sharpens the Chapter 2 taxonomy by insisting the engineer identify the end use case before choosing a serving mechanism: is the user looking at historical trends, watching for anomalies in real time, or consuming a dashboard on a mobile application? Each maps to a different category below and has different serving requirements (source: raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md).

## Business intelligence

BI "marshals collected data to describe a business's past and current state." It requires **business logic** to process raw data into reportable form (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md). Chapter 9 adds the sub-activity breakdown — dashboards, reports, and ad-hoc analysis — worked through the running-shorts quality-investigation example. See [[business-analytics]] for the full Chapter 9 treatment.

Chapter 2 flags a shift in **where** that business logic lives: historically applied in the [[data-transformation|transformation]] stage, increasingly applied on-read via a BI tool's [[semantic-layer|semantic layer]]. In **logic-on-read**, data is stored clean but fairly raw; the BI system maintains a repository of business logic and definitions that reports and dashboards query through.

### Self-service analytics

As data maturity grows, BI moves from ad-hoc analysis toward **[[self-service-analytics|self-service analytics]]** — democratised data access for business users without needing IT. Simple in theory, "tough to pull off in practice." The three main blockers (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md):

1. Poor data quality.
2. Organisational silos.
3. Lack of adequate data skills across the business.

Chapter 9 adds the audience analysis: self-service succeeds only with the right audience — typically executives or analysts with genuine data fluency; it fails when applied to everyone. See [[self-service-analytics]].

## Operational analytics

Operational analytics focuses on **fine-grained details of operations** — insights the report consumer can act on immediately. Live inventory, real-time dashboards of website health. Data is consumed in real time, directly from source systems or streaming pipelines.

The defining difference from BI: operational analytics is focused on **the present**, not historical trends (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md). Chapter 9's slogan: "operational analytics versus business analytics = immediate action versus actionable insights." See [[operational-analytics]] for the full treatment, including Chapter 9's 10-year forecast that streaming will supplant batch.

## Embedded / customer-facing analytics

Analytics exposed to the SaaS platform's own customers rather than internal users. Called out separately from BI because the requirements are materially different (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md):

| | Internal BI | Embedded / customer-facing |
|---|---|---|
| Audience | Limited (a company's employees) | Thousands or more external customers |
| Request rate | Modest | Much higher — one report per customer, many customers |
| Access control | Handful of roles | Significantly more complicated; per-tenant isolation critical |
| Blast radius of a leak | Internal procedural review | Massive breach of trust, likely public, loss of customers |

Chapter 2's recommendation: **minimise blast radius**. Apply tenant- or data-level security in storage and anywhere data can leak. Chapter 9 names three dimensions where embedded analytics is materially harder than internal BI: **low data latency**, **fast query performance**, and **high query concurrency** — see [[embedded-analytics]] for the full Chapter 9 treatment.

## Multi-tenancy is the enabler and the risk

Many storage and analytics systems support multi-tenancy — a unified internal view (useful for analytics and ML across customers) with **logical views, controls, and filters** that separate customer-facing data. Data engineers must understand the minutiae of multi-tenancy in the systems they deploy to ensure absolute data security and isolation (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

## Cross-book connections

- [[oltp-vs-olap]] — analytics is the quintessential OLAP workload.
- [[data-warehousing]] — the traditional home for BI.
- [[cross-service-analytics]] (Newman) — how to do analytics across microservice boundaries.

## Related pages

- [[data-serving]]
- [[business-analytics]]
- [[operational-analytics]]
- [[embedded-analytics]]
- [[self-service-analytics]]
- [[data-warehousing]]
- [[oltp-vs-olap]]
- [[data-security]]
- [[data-engineering-lifecycle]]
- [[cross-service-analytics]]
- [[semantic-layer]]
- [[metrics-layer]]
