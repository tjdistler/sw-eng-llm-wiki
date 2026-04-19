# Opex vs Capex

**Summary**: The two accounting categories for technology spend. **Capex** is an up-front capital investment, amortised over years; **opex** is gradual, consumption-based, short-term. Reis and Housley argue data engineering has shifted decisively toward opex-first with the cloud, and the shift is architectural, not just accounting.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md`, `raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md`

**Last updated**: 2026-04-18

---

## The two categories

Chapter 4 splits expenses two ways (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

### Capex (capital expenses)

- Require an **up-front investment**; payment is due today.
- Before the cloud, companies purchased hardware and software up front through large acquisition contracts — often hundreds of thousands to millions of dollars.
- Treated as **assets that depreciate** slowly over time.
- **Long-term focused** — a significant capital outlay with a long-term plan to achieve positive ROI.
- Also required investment in hosting: server rooms, data centers, colocation facilities.

### Opex (operational expenses)

- **Gradual and spread out over time.**
- Pay-as-you-go or similar — allows a lot of flexibility.
- **Short-term focused.**
- Closer to a direct cost, making it easier to attribute to a data project.

## Why the cloud changed this

Chapter 4 is emphatic (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

> Until recently, opex wasn't an option for large data projects. Data systems often required multimillion-dollar contracts. This has changed with the advent of the cloud, as data platform services allow engineers to pay on a consumption-based model.

This shift has two consequences:

1. **Iterate quickly, cheaply.** Cloud-based services let data engineers try various software and technology configurations without a capital commitment.
2. **Greater choice.** Engineering teams can pick their own tools without a CFO sign-off per change.

## The opex-first recommendation

Reis and Housley's advice (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

> Data engineers need to be pragmatic about flexibility. The data landscape is changing too quickly to invest in long-term hardware that inevitably goes stale, can't easily scale, and potentially hampers a data engineer's flexibility to try new things. Given the upside for flexibility and low initial costs, we urge data engineers to take an opex-first approach centered on the cloud and flexible, pay-as-you-go technologies.

## Why this is architectural, not just accounting

Chapter 3 already made the same argument from the FinOps angle (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md): on-prem meant a fixed-capacity capital cycle every few years; the cloud made spend *dynamic*. [[finops|FinOps]] is the operational practice that makes opex manageable.

Opex-first also reinforces [[reversible-vs-irreversible-decisions|reversibility]] (Principle 7): without a multi-year capital commitment locking you in, you can switch tools when the landscape changes.

## The counter-case

Chapter 4's [[cloud-repatriation]] discussion acknowledges the opex-first rule breaks down at cloud-scale. Dropbox, Backblaze, Cloudflare, and Netflix all run workloads on their own hardware because at exabyte scale and terabit-per-second traffic, the capex model pays for itself. This is rare — the book's phrase is **"you are not Dropbox, nor are you Cloudflare."**

## Related pages

- [[total-cost-of-ownership]]
- [[total-opportunity-cost-of-ownership]]
- [[finops]]
- [[cloud]]
- [[cloud-repatriation]]
- [[principles-of-good-data-architecture]]
- [[technology-selection]]
