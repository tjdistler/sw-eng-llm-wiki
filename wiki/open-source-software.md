# Open Source Software (OSS)

**Summary**: A software distribution model in which the code is made available for general use, typically with licenses that require open redistribution of derived software. Reis and Housley split OSS into **community-managed** and **[[commercial-oss|commercial (COSS)]]** and give specific evaluation criteria for each.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md`

**Last updated**: 2026-04-18

---

## Definition

Chapter 4 (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

> Open source software (OSS) is a software distribution model in which software, and the underlying codebase, is made available for general use, typically under specific licensing terms. Often OSS is created and maintained by a distributed team of collaborators. OSS is free to use, change, and distribute most of the time, but with specific caveats. For example, many licenses require that the source code of open source-derived software be included when the software is distributed.

Origins vary: sometimes OSS springs from an individual or small team releasing their work to the public; sometimes a company releases a specific tool under an OSS license.

## Two flavours

Chapter 4 draws the central distinction:

### Community-managed OSS

Driven by a distributed community of contributors. Success depends on a **strong community and vibrant user base** — the "virtuous cycle" of strong adoption (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md).

Evaluation factors Chapter 4 names:

- **Mindshare.** GitHub stars, forks, commit volume and recency. Community activity on chat groups and forums.
- **Maturity.** How long has the project existed? How active is it today? Is it used in production?
- **Troubleshooting.** Are you on your own, or can the community help?
- **Project management.** How are Git issues addressed? Are they resolved quickly?
- **Team.** Who are the core contributors? Is a company sponsoring?
- **Developer relations and community management.** Vibrant Slack community? Support forums?
- **Contributing.** Does the project encourage and accept pull requests?
- **Roadmap.** Is there one? Is it transparent?
- **Self-hosting and maintenance.** Do you have resources to host/maintain? What's the [[total-cost-of-ownership|TCO]] vs buying managed?
- **Giving back.** If you like the project and use it actively, consider contributing code, fixes, or donations. OSS maintainers often run projects as unpaid labour of love.

### [[commercial-oss|Commercial OSS (COSS)]]

A vendor hosts and manages the OSS for you, typically as a cloud SaaS offering. Examples: **Databricks** (Spark), **Confluent** (Kafka), **DBT Labs** (dbt). A vendor is often affiliated with the underlying community project — the maintainers spin out a company to commercialise. See [[commercial-oss]] for details.

## Why Chapter 4 favours OSS by default

Chapter 4's advice (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

> In general, we favor OSS and COSS by default, which frees you to focus on improving those areas where these options are insufficient.

Benefits of the OSS-first posture:

- **Lower lock-in.** Even if the vendor or OSS project dies, you can keep running the code. Much lower [[total-opportunity-cost-of-ownership|TOCO]] than [[proprietary-walled-garden|proprietary walled gardens]].
- **Transparency.** You can read the code, understand the system, and predict its behaviour.
- **Community support.** Strong projects have communities that answer questions and fix bugs faster than many paid vendors do.
- **Budget velocity.** Getting started often doesn't require a contract or budget approval.

## The caveat

Chapter 4 is careful to note that OSS "may be trivial or extremely complicated and cumbersome" to self-host, depending on the application (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md). Commercial OSS exists precisely because many organisations find self-hosting Kafka or Spark too painful to justify the savings.

The full-OSS route makes the most sense when:

- Your team has the operational skill.
- The project is mature and the community is strong.
- Self-hosting gives you capabilities the managed version would restrict.

Otherwise, COSS is usually the better trade.

## Cloud-vendor OSS

Chapter 4 also names the cloud-provider angle (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

> Note also that clouds offer their own managed open source products. If a cloud vendor sees traction with a particular product or project, expect that vendor to offer its version. This can range from simple examples (open source Linux offered on VMs) to extremely complex managed services (fully managed Kafka).

The motivation is simple: clouds make their money through consumption. More offerings mean more stickiness.

## Cross-book framing

- [[modern-data-stack]] is largely OSS and COSS components stitched together.
- [[orchestration]] — Apache Airflow is Chapter 2's canonical community-OSS example; managed Airflow (via Astronomer, GCP, AWS) is the COSS form.
- [[event-driven-microservices]] and the Kafka ecosystem are a textbook OSS/COSS ecosystem.

## Related pages

- [[build-vs-buy]]
- [[commercial-oss]]
- [[proprietary-walled-garden]]
- [[technology-selection]]
- [[modern-data-stack]]
- [[total-cost-of-ownership]]
- [[total-opportunity-cost-of-ownership]]
- [[principles-of-good-data-architecture]]
