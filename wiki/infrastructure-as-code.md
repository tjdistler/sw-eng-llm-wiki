# Infrastructure as Code

**Summary**: The practice of applying software-engineering methods (version control, review, automated deployment) to infrastructure configuration. A software-engineering sub-topic of the [[data-engineering-lifecycle]] and a core enabler of [[dataops|DataOps]]. Chapter 2 frames IaC as a maturity marker: as managed services absorb low-level provisioning, the remaining infra work happens through IaC frameworks rather than manual instance spin-ups.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md`

**Last updated**: 2026-04-18

---

## What IaC is

Infrastructure as code (IaC) "applies software engineering practices to the configuration and management of infrastructure" (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md). Rather than an engineer clicking through a cloud console to spin up instances and install software, the desired state of infrastructure is expressed as declarative code in a repository, reviewed like any other code change, and applied automatically.

## Why IaC matters for data engineers

Chapter 2 notes a trend: the infrastructure-management burden of the big-data era has **decreased** as companies moved to managed systems (Databricks, Amazon EMR, cloud data warehouses). Where engineers still must manage cloud infrastructure themselves, they increasingly do so through IaC frameworks rather than manual clicks (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

## Frameworks

Several categories of IaC tool exist (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md):

- **General-purpose** — Terraform, Pulumi.
- **Cloud-platform-specific** — AWS CloudFormation, Azure Resource Manager, GCP Deployment Manager.
- **Container/Kubernetes** — Helm charts, Kustomize; the container-level analogue of IaC.

Many of these frameworks manage cloud services as well as raw infrastructure.

## Why it's a DevOps/DataOps primitive

IaC gives **version control and repeatability of deployments** — both prerequisites for treating infrastructure as a software artefact. Repeatable deployments enable testing, review, rollback, and auditability. These properties transfer directly into [[dataops|DataOps]] practices across the data engineering lifecycle (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

## Cross-book connections

- [[continuous-integration-delivery-deployment]] — IaC is typically applied through a CI/CD pipeline.
- [[dataops]] — IaC is one of the core techniques behind DataOps automation.
- [[operator-pattern]] (Burns) — the Kubernetes-native way to encode domain-specific operational knowledge in code.

## Related pages

- [[software-engineering-for-data]]
- [[dataops]]
- [[data-engineering-lifecycle]]
- [[continuous-integration-delivery-deployment]]
- [[operator-pattern]]
