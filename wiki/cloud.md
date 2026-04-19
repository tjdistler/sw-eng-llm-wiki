# Cloud

**Summary**: Renting hardware and managed services from a provider (AWS, Azure, GCP) rather than owning them. Reis and Housley's Chapter 4 argues cloud is the default deployment target for new data workloads, but "Cloud ≠ On Premises" — naive lift-and-shift produces horrifying bills.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md`

**Last updated**: 2026-04-18

---

## The cloud flips the model

Chapter 4's summary (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

> Instead of purchasing hardware, you simply rent hardware and managed services from a cloud provider. These resources can often be reserved on an extremely short-term basis; VMs spin up in less than a minute, and subsequent usage is billed in per-second increments.

For data engineers: quickly launch projects, experiment without long hardware lead times, run servers as soon as code is ready. Extremely appealing to startups tight on budget and time. For established enterprises, the COVID-19 era (2020) was a major driver — the need to rapidly scale data processes for highly uncertain business conditions.

## The three layers of cloud service

Chapter 4 maps the conventional IaaS/PaaS/SaaS stack onto data engineering (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

- **IaaS (Infrastructure as a Service)** — the early-cloud default. VMs and virtual disks; rented slices of hardware. Amazon EC2.
- **PaaS (Platform as a Service)** — IaaS plus managed application support. Examples: Amazon RDS, Google Cloud SQL (managed databases); Amazon Kinesis, SQS (managed streaming); GKE, AKS (managed Kubernetes). Engineers ignore individual-machine operations.
- **SaaS (Software as a Service)** — fully functioning enterprise software. Salesforce, Google Workspace, Microsoft 365, Zoom, Fivetran.

Chapter 4 observes the industry trajectory: PaaS and SaaS keep growing at the expense of raw IaaS. The book calls out **[[serverless-vs-servers|serverless]]** as increasingly important in PaaS and SaaS — automated scaling from zero to extreme, pay-as-you-go billing, no operational awareness of underlying servers.

## Cloud economics: how clouds make money

Chapter 4 has a lengthy sidebar on cloud pricing. Key points (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

### Cloud services as financial derivatives

Cloud providers don't just sell hardware; they slice it into tiers of risk and performance. Each disk in a storage cluster has three assets: **capacity, IOPs, bandwidth**. Any one of them can be the bottleneck. So providers sell:

- Cheap storage with expensive access (archival class storage — GCP archival runs on the same clusters as standard but costs ~1/17 per GB per month).
- Expensive storage with cheap access.
- Various points in between.

Cloud vendors monetise **durability, reliability, longevity, and predictability** — not just CPU cores and memory. Spot and ephemeral instances discount workloads that can be interrupted.

### Cloud ≠ On Premises

Chapter 4's most emphasised warning:

> Moving on-premises servers one by one to VMs in the cloud — known as simple lift and shift — is a perfectly reasonable strategy for the initial phase of cloud migration... However, companies that leave their cloud assets in this initial state are in for a rude shock. On a direct comparison basis, long-running servers in the cloud are significantly more expensive than their on-premises counterparts.

The cognitive error Chapter 4 calls the **"curse of familiarity"** — cloud services are designed to look like familiar things (a VM is a VM, right?) but have subtleties that users must learn to identify, accommodate, and optimise.

Keys to cloud value (Chapter 4):

- **Autoscaling** — scale down when load is light, up during peaks. Don't size for peak year-round.
- **Reserved or spot instances** — discount the durability or predictability you don't need.
- **Serverless functions** in place of long-running servers.
- **Create new value** — do things impossible on-prem (spin up massive ephemeral clusters for specific jobs).

### [[data-gravity|Data gravity]]

Cloud vendors want to lock you in. Getting data onto a platform is cheap or free; getting data *out* via **egress fees** can be extremely expensive. "Data gravity is real: once data lands in a cloud, the cost to extract it and migrate processes can be very high." See [[data-gravity]].

## Deployment options

Chapter 4 names the four principal places to run your stack (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

- [[on-premises]] — you own the hardware.
- **Cloud** — single public cloud.
- [[hybrid-cloud]] — some workloads in cloud, some on-prem. The most common migration state.
- [[multicloud]] — workloads spread across multiple public clouds.

Decentralised computing (blockchain, Web 3.0, edge) is briefly mentioned as a possible long-term disruption but has not yet had meaningful impact in the data space.

## Chapter 4's advice

"Choose technologies for the present, but look toward the future" (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

- **Plan for the present.** Don't try to architect around every possible five-to-ten-year future — analysis paralysis kills projects.
- **Default to single-cloud.** Unless you have a compelling reason (customer proximity, regulatory data residency, specific tech needs), don't pay the complexity tax of multicloud or hybrid-cloud.
- **Have an escape plan.** Every technology has lock-in; single-cloud especially. Prepare the plan even if you never use it.

## Relationship to the nine principles

The cloud is the operational substrate that makes several of Chapter 3's [[principles-of-good-data-architecture|principles]] practical:

- Principle 3 (scalability) — elasticity and autoscaling are cloud-native.
- Principle 7 (reversible decisions) — opex-first, short-term commitments.
- Principle 9 (FinOps) — cloud made cost dynamic, which forced [[finops|FinOps]] as a discipline.

## Related pages

- [[on-premises]]
- [[hybrid-cloud]]
- [[multicloud]]
- [[cloud-repatriation]]
- [[data-gravity]]
- [[cloud-native-principles]]
- [[shared-responsibility-model]]
- [[finops]]
- [[opex-vs-capex]]
- [[serverless-vs-servers]]
- [[elasticity]]
- [[technology-selection]]
- [[principles-of-good-data-architecture]]
