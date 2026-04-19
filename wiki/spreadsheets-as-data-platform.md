# Spreadsheets as a Data Platform

**Summary**: Reis and Housley's whimsical-but-serious closing prediction in Chapter 11. The most widely used data platform in the world — 700 million to 2 billion users — is the humble spreadsheet. Spreadsheets are the "dark matter" of the data world: interactive data applications that support complex analytics, accessible to a wider spectrum of users than any BI tool. The prediction: a new class of tool will combine spreadsheet interactivity with the backend power of cloud [[real-time-olap|OLAP]] systems.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md`

**Last updated**: 2026-04-18

---

## The "dark matter" framing

Chapter 11 takes a deliberate left turn near the end (source: raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md):

> This section might seem odd, but we need to address something that's widely ignored in today's data world, especially by engineers. What's the most widely used data platform? It's the humble spreadsheet.

Depending on the estimate, 700M–2B people use spreadsheets. Huge volumes of real analytics — financial reporting, supply-chain analytics, even CRM in many organisations — run in spreadsheets and never make it into the "sophisticated data systems" this book describes.

Engineers tend to dismiss spreadsheets. Reis and Housley argue that's a mistake: spreadsheets are the proof that accessibility beats sophistication for most users.

## What spreadsheets actually are

Chapter 11 reframes the spreadsheet as "an interactive data application that supports complex analytics" (source: raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md). Unlike code-based tools like [[dbt]], pandas, or SQL, spreadsheets span a whole spectrum of users:

- Casual users who just open files and look at results.
- Power users who write sophisticated procedural data processing (macros, lambda functions, linked sheets).
- Everything in between.

BI tools have never matched this range. They tend to offer slicing and dicing within tight guardrails, not general-purpose programmable analytics.

## The prediction

A new product category will emerge that fuses (source: raw/fundamentals-of-data-engineering/chapter-11-the-future-of-data-engineering.md):

- The **interactive analytics capabilities** of a spreadsheet — open, flexible, directly manipulable, accessible to non-engineers.
- The **backend power of cloud OLAP systems** — the scale and latency of a [[real-time-olap|real-time OLAP database]] or [[data-warehousing|cloud warehouse]].

Candidates are already appearing. The winner may keep a spreadsheet-like paradigm or invent a new interaction idiom entirely.

## Where it fits in the chapter's argument

This is Reis and Housley's reminder that the future of data engineering isn't only about streaming and real-time — it's also about the **serving** and **user experience** layer. [[self-service-analytics]] has been mostly aspirational; spreadsheets are the existing proof that accessible data tools can succeed at massive scale. A spreadsheet-shaped front end on a cloud-OLAP backend could be the next big serving idiom.

See [[data-serving]] and [[self-service-analytics]].

## Caveats

The chapter doesn't predict this will replace BI tools outright or dominate the way the [[live-data-stack]] might. It's framed as a plausible near-future category, not a certainty. But the underlying observation — that engineers systematically undercount spreadsheet usage — is hard to argue with.

## Related pages

- [[future-of-data-engineering]]
- [[data-serving]]
- [[self-service-analytics]]
- [[real-time-olap]]
- [[data-warehousing]]
- [[embedded-analytics]]
- [[business-analytics]]
- [[data-wrangling]]
