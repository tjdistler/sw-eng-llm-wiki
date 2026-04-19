# Embedded Analytics

**Summary**: Customer-facing analytics embedded *into a product*, not shown to internal users. The SaaS-era trend where an application includes dashboards and metrics for the product's own customers — a smart thermostat showing power consumption, an e-commerce seller portal showing real-time sales. Chapter 9 flags three performance dimensions that make embedded analytics materially harder than internal BI: **low data latency, fast query performance, and high query concurrency**.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md`, `raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md`

**Last updated**: 2026-04-18

---

## What it is

Where [[business-analytics]] and [[operational-analytics]] are internally focused, embedded analytics is "externalor user-facing" — analytics delivered *to end users of the product* (source: raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md).

Chapter 9's examples:

- A smart thermostat app showing real-time temperature and power consumption, letting the user build an energy-efficient schedule.
- A third-party e-commerce platform showing sellers real-time sales, inventory, and returns — so the seller can offer near-real-time customer deals.

These are "data applications" — applications whose value is primarily analytics delivered to their end user.

## The three hard requirements

Chapter 9 pulls out three performance problems that internal BI rarely faces (source: raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md):

1. **Low data latency.** "App users are not as tolerant of infrequent batch processing as internal company analysts; users of a recruiting SaaS platform may expect to see a change in their statistics as soon as they upload a new resume."
2. **Fast query performance.** When users adjust a parameter, they expect refreshed results in seconds.
3. **High query concurrency.** "Data apps must often support extremely high query rates across many dashboards and numerous customers."

All three stress the serving database in a way the classic warehouse was never designed for.

## Scaling arc

Chapter 9's observed pattern:

- Google and early major players developed **exotic technologies** to cope.
- New startups **default to conventional transactional databases** for data apps — which works until customer base grows.
- They **outgrow that architecture** and migrate to a newer generation of databases that combine fast queries, high concurrency, and near-real-time updates with SQL ease-of-use.

The latter category — operational analytics databases, some of the newer cloud warehouses — is the emerging home for embedded analytics at scale (source: raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md).

## The multitenancy problem

Chapter 2 emphasises the security dimension Chapter 9 doesn't repeat in detail: embedded analytics is almost always **multitenant**. Every customer must see their data and only their data. A leak is catastrophic — a public breach, not an internal procedural review (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

Cloud data platforms support multitenancy via logical views, row-level security, and filters — and "data engineers must understand the minutiae of multitenancy in the systems they deploy to ensure absolute data security and isolation" (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

## The data engineer's role

Chapter 9 notes that data engineers typically don't build the embedded analytics **frontend** — that's the application developer's job. But data engineers own the databases behind the frontend and must understand speed / latency / concurrency requirements. The "Software Engineering" undercurrent of Chapter 9: data engineers ensure application developers get correctly-shaped payloads quickly and cost-effectively (source: raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md).

## Cross-book connections

- **[[abusive-client-behavior]]** / **[[handling-overload]]** (SRE) — embedded analytics faces an adversarial concurrency pattern; rate limiting and quota systems become critical.
- **[[multitenancy-in-streaming-clusters]]** (Bellemare) — the streaming analogue of embedded analytics' shared-infrastructure problem.

## Related pages

- [[analytics]]
- [[business-analytics]]
- [[operational-analytics]]
- [[data-security]]
- [[data-serving]]
- [[data-product]]
- [[streaming-queries]]
