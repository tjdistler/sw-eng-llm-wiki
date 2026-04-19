# Proprietary Walled Gardens

**Summary**: Closed-source products — either from independent vendors or cloud-platform services — chosen for features or integration rather than transparency. Reis and Housley place them alongside [[open-source-software|OSS]] and [[commercial-oss|COSS]] as one of the [[build-vs-buy|buy]] options, with the key warning that walled gardens carry the strongest lock-in.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md`

**Last updated**: 2026-04-18

---

## Definition

Chapter 4 (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

> While OSS is ubiquitous, a big market also exists for non-OSS technologies. Some of the biggest companies in the data industry sell closed source products.

Two subtypes:

## Independent offerings

VC-funded independent companies that sell proprietary tools — often as fully-managed cloud services. Because they skip the OSS step, they don't get community-driven credibility, but they can still produce excellent products (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md).

Evaluation factors Chapter 4 names:

- **[[interoperability|Interoperability]].** Does the tool play nicely with your other choices (OSS, other independents, cloud offerings)? Try before you buy.
- **Mindshare and market share.** Is the solution popular? Positive customer reviews?
- **Documentation and support.** Clear how to solve problems — documentation or support?
- **Pricing.** Map low/medium/high usage scenarios with respective costs. Can you negotiate a discount? What flexibility do you lose by signing a contract? Contractual commitments on future pricing?
- **Longevity.** Will the company survive long enough for you to get value? Check funding (Crunchbase), user reviews, word of mouth.

## Cloud platform proprietary service offerings

Services built and sold by cloud vendors — often internal tools that outgrew their original use and became products (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

- **Amazon DynamoDB** — built internally to handle Amazon.com scale when relational databases couldn't; later offered on AWS as a top-rated service.
- **Google BigQuery, AWS Redshift, Azure Synapse** — cloud-native OLAP services.
- Many more.

Cloud vendors bundle proprietary services to work well together — each cloud creates stickiness with its user base by offering a strongly integrated ecosystem. **This is intentional.**

Evaluation factors for proprietary cloud offerings:

- **Performance vs price.** Is the cloud offering substantially better than an independent or OSS alternative? What's the total TCO?
- **Purchase considerations.** On-demand pricing is expensive. Can you lower cost with reserved capacity or a long-term commitment? What's the flexibility trade-off?

## Why walled gardens carry the strongest lock-in

Chapter 4's general pattern:

- With community OSS, you can self-host forever.
- With COSS, the community OSS underneath is your fallback.
- With a **walled garden**, there is **no fallback** — if the vendor raises prices, deprecates the product, or shuts down, you are rebuilding on something else from scratch.

The [[total-opportunity-cost-of-ownership|TOCO]] for walled gardens is therefore higher than for OSS/COSS, all else being equal. Chapter 4's advice is not "avoid walled gardens" but "weigh this explicitly." Sometimes the integration or capability advantage genuinely outweighs the lock-in — DynamoDB or BigQuery for a company all-in on AWS or GCP is usually a reasonable call.

## Cross-cloud competition

Chapter 4 observes that cloud competition drives stronger proprietary offerings (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

> Given the intense competition among the major cloud providers, expect them to offer more best-of-breed services, making multicloud more compelling.

This is partly what feeds the [[multicloud]] "best-of-breed per cloud" argument — each cloud pushes proprietary differentiators, and teams want to use each cloud's best service.

## Related pages

- [[open-source-software]]
- [[commercial-oss]]
- [[build-vs-buy]]
- [[cloud]]
- [[multicloud]]
- [[total-opportunity-cost-of-ownership]]
- [[interoperability]]
- [[technology-selection]]
