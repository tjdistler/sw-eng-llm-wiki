# Shared Responsibility Model

**Summary**: AWS's formal division of security responsibility between cloud provider and customer: the provider is responsible for *security of the cloud*; the customer is responsible for *security in the cloud*. Reis and Housley cite it alongside [[zero-trust-security]] as one of the two ideas at the core of their [[principles-of-good-data-architecture|security principle]].

**Sources**: `raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md`, `raw/fundamentals-of-data-engineering/chapter-10-security-and-privacy.md`

**Last updated**: 2026-04-18

---

## The division

Chapter 3 quotes the AWS framing directly (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md):

**AWS is responsible for the security *of* the cloud**:
> AWS is responsible for protecting the infrastructure that runs AWS services in the AWS Cloud. AWS also provides you with services that you can use securely.

**The customer is responsible for security *in* the cloud**:
> Your responsibility is determined by the AWS service that you use. You are also responsible for other factors including the sensitivity of your data, your organization's requirements, and applicable laws and regulations.

The exact boundary moves depending on the service — managed databases, serverless functions, and IaaS VMs have different splits — but the principle is constant. All cloud providers operate on a variant of this model.

## Why it matters for the data engineer

The shared responsibility model explicitly **pushes security responsibility out to application engineers**. The cloud provider guarantees a secure platform *if the customer configures it correctly*. Misconfigurations are the customer's problem (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md).

This is the organisational context for Reis and Housley's assertion that **all data engineers should consider themselves security engineers**. The command-and-control model — a central security team owns everything — does not work once an engineer with `s3:PutBucketPolicy` can accidentally leak petabytes of customer data.

Chapter 3 cites S3 bucket misconfigurations as the canonical case: numerous breaches have resulted from the simple error of making buckets public.

## Chapter 10 — the end-user breach statistic

Chapter 10 reinforces the framing with a blunt empirical claim (source: raw/fundamentals-of-data-engineering/chapter-10-security-and-privacy.md):

> Most cloud security breaches continue to be caused by end users, not the cloud. Breaches occur because of unintended misconfigurations, mistakes, oversights, and sloppiness.

This is the shared responsibility model's bill coming due. The cloud provider has largely held up its side — its infrastructure is, by revealed preference, more secure than most enterprises could build themselves. The remaining breach surface is overwhelmingly on the customer side: IAM role sprawl, public buckets, checked-in credentials, unpatched VMs. Those are all covered by [[least-privilege]], [[secrets-management]], [[network-access-security]], and [[security-monitoring]] — the engineer-owned half of the model.

## Relationship to [[zero-trust-security]]

Zero-trust and the shared responsibility model are complementary, not alternatives:

- **Zero-trust** is about *architecture* — don't assume network location confers trust
- **Shared responsibility** is about *organisation* — the customer is accountable for everything above the provider's floor, so engineers become security engineers

Both reflect the cloud's dissolution of the traditional perimeter — technical in one case, organisational in the other.

## Related pages

- [[data-security]]
- [[zero-trust-security]]
- [[principles-of-good-data-architecture]]
- [[least-privilege]]
- [[data-architect]]
