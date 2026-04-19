# Immutable vs Transitory Technologies

**Summary**: Reis and Housley's fifth [[technology-selection|selection criterion]]. **Immutable** technologies are durable foundations that have stood the test of time — object storage, SQL, bash, the C programming language. **Transitory** technologies come and go with hype cycles. Build on the immutable; swap transitory tools around them every few years.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md`

**Last updated**: 2026-04-18

---

## The distinction

Chapter 4 names two classes of tool for any selection decision (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

### Immutable technologies

Components that **underpin the cloud or languages and paradigms that have stood the test of time**. In the cloud, examples are:

- **Object storage** — Amazon S3, Azure Blob Storage. "Will be around from today until the end of the decade, and probably much longer."
- **Networking, servers, security.**

For languages, **SQL** and **bash** "have been around for many decades, and we don't see them disappearing anytime soon."

### Transitory technologies

Those that come and go. The typical trajectory: "a lot of hype, followed by meteoric growth in popularity, then a slow descent into obscurity."

Chapter 4's illustrative example is the JavaScript frontend landscape: Backbone.js, Ember.js, Knockout (early 2010s), AngularJS (mid-2010s), React and Vue.js (now). "What's the popular frontend framework three years from now? Who knows."

In data, Hive is the canonical example — rapid uptake in the early 2010s, now primarily legacy deployments. Presto and peers superseded it.

## The Lindy effect

Reis and Housley's litmus test (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

> Immutable technologies benefit from the Lindy effect: the longer a technology has been established, the longer it will be used.

Examples: the power grid, relational databases, the C programming language, the x86 processor architecture. Age is evidence of fitness — if a technology has survived decades of alternatives, it probably will survive more.

## The two-year re-evaluation rule

Chapter 4's practical recommendation (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

- Evaluate your tools **every two years**.
- Find the **immutable technologies along the data engineering lifecycle** and use those as your base.
- **Build transitory tools around the immutables.**
- Know the barriers to leaving each tool. Go in eyes-open: the project may be abandoned, the company may not be viable, the fit may erode.

## Why this matters

Given the hundreds of tools in Matt Turck's MAD (ML, AI, data) landscape, even relatively successful technologies fade into obscurity quickly. VCs making large bets expect most of them to fail. A data architecture built entirely on transitory tools will need to be rebuilt, piece by piece, every cycle.

The pattern reduces [[total-opportunity-cost-of-ownership|TOCO]]: immutable foundations are stable anchors, transitory tools are swappable heads — the whole stack doesn't need to be ripped out together.

## Cross-book framing

- [[cost-of-change]] (Richards and Ford / Booch) — immutable technology choices have a low cost-of-change because they're stable; transitory tool choices must be made so they stay cheap to change.
- [[reversible-vs-irreversible-decisions|Principle 7]] (reversible decisions) — the immutable/transitory split is how you operationalise "make reversible decisions" in data engineering.
- [[modern-data-stack]] — the modern-data-stack *is* the modular ecosystem of transitory-on-top-of-immutable.

## Related pages

- [[technology-selection]]
- [[total-opportunity-cost-of-ownership]]
- [[reversible-vs-irreversible-decisions]]
- [[cost-of-change]]
- [[modern-data-stack]]
- [[principles-of-good-data-architecture]]
- [[speed-to-market]]
- [[brownfield-vs-greenfield]]
