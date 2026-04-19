# Multicloud

**Summary**: Deploying workloads across multiple public clouds. Offers best-of-breed access and customer proximity but introduces significant complexity — cross-cloud networking, egress costs, and security coordination. Reis and Housley urge "don't unless you have to."

**Sources**: `raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md`

**Last updated**: 2026-04-18

---

## What it is

Chapter 4's definition (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

> Multicloud simply refers to deploying workloads to multiple public clouds.

Any mix of provider services is possible in principle; the practical question is what you get and what you pay for it.

## Motivations

Chapter 4 lists the common reasons (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

- **Customer proximity for SaaS.** Snowflake and Databricks offer their SaaS across multiple clouds so data-intensive customers can run the SaaS close to their existing workloads, avoiding network latency and egress costs.
- **Best-of-breed per cloud.** Google Ads and Analytics in GCP, Microsoft workloads in Azure, best-in-class services (Lambda, Kubernetes) in AWS. Use each cloud for what it does best.
- **Negotiating leverage / risk diversification.** Not explicit in Chapter 4 but implied by the "intense competition among the major cloud providers" framing.

## Disadvantages

Chapter 4 is blunt (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

- **[[data-gravity|Data egress costs]] and networking bottlenecks are critical.** Cloud providers charge to move data out; multicloud means you're doing that a lot.
- **Significant complexity.** Managing a "dizzying array of services across several clouds." Cross-cloud integration and security present considerable challenges.
- **Multicloud networking can be diabolically complicated.**

## "Cloud of clouds"

Chapter 4 names an emerging category that aims to reduce multicloud complexity (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

> A new generation of "cloud of clouds" services aims to facilitate multicloud with reduced complexity by offering services across clouds and seamlessly replicating data between clouds or managing workloads on several clouds through a single pane of glass.

**Snowflake** is the book's cited example — a single account runs in one cloud region, but customers can spin up other accounts in other clouds and replicate between them on a schedule. The UI is identical across clouds, eliminating the training burden of switching between cloud-native data services.

## Chapter 4's advice

> Don't choose a complex multicloud or hybrid-cloud strategy unless there's a compelling reason. (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md)

Compelling reasons named:

- Serving data near customers on multiple clouds.
- Industry regulations require certain data to reside in your data centres.
- A compelling technology need for specific services on two different clouds.

If none apply, choose **single-cloud**. "The decision space will look very different in five to ten years" — Chapter 4 explicitly advises against trying to architect around every possible multicloud future.

## Related pages

- [[cloud]]
- [[hybrid-cloud]]
- [[on-premises]]
- [[data-gravity]]
- [[technology-selection]]
- [[principles-of-good-data-architecture]]
