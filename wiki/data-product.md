# Data Product

**Summary**: DJ Patil's definition — "a product that facilitates an end goal through the use of data." Chapter 9 frames data-product thinking as a full-contact sport mixing product, business, and engineering concerns. A good data product has positive feedback loops, identified users with "jobs to be done," and clear ROI. This page is the *product-design* view; see [[data-as-a-product]] for the organisational stance that treats datasets as first-class products in a [[data-mesh|data mesh]].

**Sources**: `raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md`

**Last updated**: 2026-04-18

---

## Patil's definition

Chapter 9 opens the section with DJ Patil's line: "A good definition of a data product is a product that facilitates an end goal through the use of data" (source: raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md).

The point is the *end goal* — not the dashboard, not the model, the thing the user is trying to accomplish.

## Jobs to be done

Chapter 9 borrows Clayton Christensen's "jobs to be done" framing: a user hires a product to do a job. Before building, the engineer has to know *what job the user is hiring the product for*.

The classic failure mode: "a classic engineering mistake is simply building without understanding the requirements, needs of the end user, or product/market fit" — the data product that nobody wants to use (source: raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md).

## Positive feedback loops

"A good data product has positive feedback loops. More usage of a data product generates more useful data, which is used to improve the data product. Rinse and repeat." Chapter 9's pithy model of compound product value (source: raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md).

The flywheel only spins when the product is good enough that usage is a tailwind, not a chore.

## The three questions

Chapter 9 lists the three questions to ask at build time (source: raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md):

1. **What do they hope to accomplish?** The JTBD question.
2. **Internal or external user?** Internal- vs external-facing data engineering have materially different reliability, latency, and access-control requirements. See [[embedded-analytics]] for the external case.
3. **What's the ROI?** The loss of [[trust-in-data|trust]] from an unwanted or low-quality product is a big negative ROI.

## Use-case-driven engineering

Chapter 9's broader argument: "Data engineers love to obsess over the technical implementation details of the systems they build while ignoring the basic question of purpose." The fix is working backward from the use case (source: raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md):

- Who will use the data, and how?
- What do stakeholders expect?
- What action will the data trigger, and can it be automated?
- Where's the highest-ROI use case?

## Relationship to data-as-a-product

- **This page (data-product)** — Chapter 9's product-design framing for a specific user-facing artifact (a dashboard, a lead-scoring model, a CRM enrichment).
- **[[data-as-a-product]]** — Dehghani's [[data-mesh]] stance that every *dataset* a domain publishes is a first-class product with consumers, SLAs, and an owner.

The two ideas are compatible; the data-mesh stance operationalises the product-design stance at the dataset level.

## Related pages

- [[data-as-a-product]]
- [[trust-in-data]]
- [[data-serving]]
- [[self-service-analytics]]
- [[embedded-analytics]]
- [[data-mesh]]
- [[dataops]]
- [[data-product-quantum]]
