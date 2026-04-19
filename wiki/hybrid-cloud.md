# Hybrid Cloud

**Summary**: Running some workloads in a public cloud and some on owned hardware. The typical mid-state of a cloud migration, but Reis and Housley note it's also a valid long-term target when certain workloads have good reasons to stay [[on-premises|on-prem]].

**Sources**: `raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md`

**Last updated**: 2026-04-18

---

## Why hybrid is so common

Chapter 4 is matter-of-fact about the prevalence of hybrid (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

> As more established businesses migrate into the cloud, the hybrid cloud model is growing in importance. Virtually no business can migrate all of its workloads overnight. The hybrid cloud model assumes that an organization will indefinitely maintain some workloads outside the cloud.

Reasons to keep some workloads on-prem indefinitely:

- **Operational excellence on existing workloads.** The application stack and its hardware work well; don't disrupt what's working.
- **Migrate only where the cloud clearly wins.** Often analytics and ephemeral Spark clusters go first because they benefit most from elasticity.

## The analytics-in-the-cloud pattern

Chapter 4 highlights an especially clean hybrid pattern (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

- **On-prem applications** generate event data.
- Event data is **pushed to the cloud** (essentially free — cloud ingress is usually not charged).
- The **bulk of data lives in the cloud**, where analytics runs.
- **Smaller amounts flow back on-prem** for model deployment to applications or [[reverse-etl]] into operational systems.

This "data flows primarily in one direction" arrangement minimises [[data-gravity|egress costs]] — the chief financial trap of cloud economics.

## Managed-hybrid offerings

Chapter 4 mentions that a new generation of managed hybrid services — AWS Outposts, Google Cloud Anthos — lets customers **locate cloud-managed servers in their own data centres** (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md). This blurs the line: you get the cloud operational model with the compliance/latency properties of on-prem.

## When not to go hybrid

Chapter 4's advice when evaluating hybrid (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

> Don't choose a complex multicloud or hybrid-cloud strategy unless there's a compelling reason.

Compelling reasons include:

- Regulatory data-residency requirements that force specific data to remain on-prem.
- Specific on-prem technology that genuinely can't be replicated in the cloud.
- An ongoing migration where hybrid is the transitional state.

If none of these apply, the single-cloud strategy is simpler and usually cheaper.

## Related pages

- [[cloud]]
- [[on-premises]]
- [[multicloud]]
- [[cloud-repatriation]]
- [[data-gravity]]
- [[reverse-etl]]
- [[technology-selection]]
- [[principles-of-good-data-architecture]]
