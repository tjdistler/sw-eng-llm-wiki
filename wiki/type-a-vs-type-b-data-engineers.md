# Type A vs Type B Data Engineers

**Summary**: A two-way split of the [[data-engineer]] role: **Type A** (abstraction) engineers avoid undifferentiated heavy lifting by composing off-the-shelf tools and managed services; **Type B** (build) engineers build custom tools and systems where the company's competitive advantage demands them. Borrowed by analogy from the Type A / Type B data scientist distinction (analysis vs building).

**Sources**: `raw/fundamentals-of-data-engineering/chapter-01-data-engineering-described.md`, `raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md`

**Last updated**: 2026-04-18

---

## The distinction

Job descriptions paint the data engineer as a unicorn with every skill imaginable. Reis and Housley push back with a simpler framing borrowed from the data-science world:

- **Type A data scientist** — *Analysis*; extracts insights from data.
- **Type B data scientist** — *Build*; builds systems that make data science work in production.

They apply the same split to data engineers (source: raw/fundamentals-of-data-engineering/chapter-01-data-engineering-described.md):

### Type A — Abstraction

Avoids undifferentiated heavy lifting. Keeps architecture as abstract and straightforward as possible. Doesn't reinvent the wheel. Manages the [[data-engineering-lifecycle]] primarily with off-the-shelf products, managed services, and SaaS.

Found at companies across industries and at every stage of [[data-maturity]].

### Type B — Build

Builds custom data tools and systems that scale and leverage the company's core competency and competitive advantage.

Most common in Stage 2 ([[data-maturity|scaling with data]]) and Stage 3 ([[data-maturity|leading with data]]) companies, or in early-stage companies whose initial data use case is so unique that existing tools don't cover it.

## How the two interact

The roles are not exclusive (source: raw/fundamentals-of-data-engineering/chapter-01-data-engineering-described.md):

- Type A and Type B engineers can work at the same company.
- A single engineer may play both roles at once.
- A common hiring pattern: **Type A first** (to lay the foundation using managed tools), then **Type B** (either through internal growth or new hires) as the need for custom builds emerges.

## Why the distinction matters

Two practical consequences:

1. **Don't hire for the unicorn.** Expecting every data engineer to be equally good at gluing managed services together *and* at building bespoke framework-level software is unrealistic. Pick which kind of work the role needs and hire for that.
2. **Match the engineer to the maturity stage.** A Stage 1 company trying to hire a Type B engineer will likely watch them build custom infrastructure that nobody needs; a late-Stage-3 company trying to get by with Type A engineers will plateau on off-the-shelf capability.

The chapter explicitly connects this split back to [[data-maturity]]: maturity shapes which blend of Type A and Type B the organisation needs (source: raw/fundamentals-of-data-engineering/chapter-01-data-engineering-described.md).

## In [[build-vs-buy|build-vs-buy]] selection (Chapter 4)

Chapter 4 revives the Type A / Type B split as a decision rule for technology selection (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

> Whenever possible, lean toward type A behavior; avoid undifferentiated heavy lifting and embrace abstraction. Use open source frameworks, or if this is too much trouble, look at buying a suitable managed or proprietary solution.

The practical implication: default to "buy" ([[open-source-software|OSS]] or [[commercial-oss|COSS]] or [[proprietary-walled-garden|proprietary]]) and reserve the Type B "build" work for areas of genuine competitive advantage. Chapter 4's tire analogy — "when you need new tires for your car, do you get the raw materials, build the tires from scratch, and install them yourself?" — is the same argument as the Chapter 1 split, just applied at the tool-choice level.

## Related pages

- [[data-engineer]]
- [[data-maturity]]
- [[data-engineering-lifecycle]]
- [[data-engineering-history]]
- [[fundamentals-of-data-engineering]]
- [[build-vs-buy]]
- [[technology-selection]]
