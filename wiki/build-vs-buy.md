# Build vs Buy

**Summary**: The age-old technology question, framed by Reis and Housley for data engineering. **Build** when doing so provides competitive advantage to the business; **buy** the rest. The decision reduces to [[total-cost-of-ownership|TCO]], [[total-opportunity-cost-of-ownership|TOCO]], and whether you genuinely need the differentiation.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md`

**Last updated**: 2026-04-18

---

## The core question

Chapter 4 poses build-vs-buy as a competitive-advantage question (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

> The argument for building is that you have end-to-end control over the solution and are not at the mercy of a vendor or open source community. The argument supporting buying comes down to resource constraints and expertise; do you have the expertise to build a better solution than something already available?

Reis and Housley's stance is direct: invest in building and customising when doing so provides competitive advantage; otherwise, "stand on the shoulders of giants and use what's already available."

## The tire analogy

Chapter 4's signature analogy (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

> When you need new tires for your car, do you get the raw materials, build the tires from scratch, and install them yourself?

No. You buy tires and have someone install them. Building your own database — when a perfectly good open-source RDBMS would serve — is the same category of mistake. Chapter 4 cites teams that built databases from scratch where a simple OSS solution would have worked better. Low ROI on TCO, high opportunity cost.

## Four options

The "buy" side has several flavours. Chapter 4 walks through each:

### [[open-source-software|Open Source Software (OSS)]]

Software whose codebase is made available under licensing terms. Two flavours:

- **Community-managed OSS** — driven by distributed contributors. Evaluate on mindshare, maturity, troubleshooting, project management, team, community, roadmap, self-hosting cost.
- **[[commercial-oss|Commercial OSS (COSS)]]** — a vendor hosts and manages the OSS as SaaS (Databricks/Spark, Confluent/Kafka, DBT Labs/dbt). Trades self-hosting toil for vendor dependence.

### [[proprietary-walled-garden|Proprietary walled gardens]]

Closed-source products. Two sub-flavours:

- **Independent offerings** — vendor-built, not released as OSS. Evaluate on interoperability, mindshare, documentation/support, pricing, longevity.
- **Cloud platform proprietary services** — cloud-vendor-built (DynamoDB, BigQuery, Redshift). Deep integration with the cloud's other services; often best performance; creates stickiness.

## The type A / type B connection

Chapter 4 revisits Chapter 1's [[type-a-vs-type-b-data-engineers|Type A vs Type B]] distinction (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

> Whenever possible, lean toward type A behavior; avoid undifferentiated heavy lifting and embrace abstraction. Use open source frameworks, or if this is too much trouble, look at buying a suitable managed or proprietary solution.

Only go Type B ("build") where the build produces differentiated value.

## Internal operational overhead is not free

A common mistake when evaluating "buy" (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

> Don't treat internal operational overhead as a sunk cost. There's excellent value in upskilling your existing data team to build sophisticated systems on managed platforms rather than babysitting on-premises servers.

Self-hosted OSS carries real TCO: maintenance, patching, upgrades, incidents. The managed-service premium is often paying for that toil back — and the freed engineering hours can be spent on actual differentiation.

## The organisational reality

Chapter 4 notes that adoption is changing shape (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

- **Old model.** IT makes top-down software purchase decisions.
- **New model.** Bottom-up adoption driven by developers, data engineers, data scientists. Organic and continuous.

Practical advice: know **who controls the budget** and **what will get approved** before spending months evaluating a vendor. "Time kills deals." Long budget-approval cycles often kill good technology choices.

## The competitive-advantage filter

Chapter 4's test for when to build (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

> Is hand-coding a database connection between your production database and your cloud data warehouse a competitive advantage for you? Probably not. This is very much a solved problem. Pick an off-the-shelf solution (open source or managed SaaS) instead. The world doesn't need the millionth +1 database-to-cloud data warehouse connector.

Conversely: the algorithm that powers your fintech platform, the model training pipeline that's the reason customers buy — that's where building is worth it.

## Cross-book framing

- [[type-a-vs-type-b-data-engineers]] — the people-side of build-vs-buy.
- [[when-microservices-are-a-bad-idea]] (Newman) — the equivalent framing on the "don't build" side of the microservices question.
- [[service-granularity]] — deciding what to build in-house vs compose from services.
- [[total-cost-of-ownership]] / [[total-opportunity-cost-of-ownership]] — the cost frameworks the decision hinges on.

## Related pages

- [[open-source-software]]
- [[commercial-oss]]
- [[proprietary-walled-garden]]
- [[type-a-vs-type-b-data-engineers]]
- [[total-cost-of-ownership]]
- [[total-opportunity-cost-of-ownership]]
- [[principles-of-good-data-architecture]]
- [[technology-selection]]
- [[modern-data-stack]]
