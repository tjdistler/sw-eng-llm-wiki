# Desired State Management

**Summary**: Specifying the number and location of service instances you require, and having the platform continuously maintain that state. Manual or script-based deployment doesn't scale to tens or hundreds of services with different desired states; Kubernetes and serverless platforms exist largely to solve this.

**Sources**: `raw/monolith-to-microservices/chapter-05-growing-pains.md`

**Last updated**: 2026-04-16

---

## Definition

Desired state management is the ability to declaratively say "I want N instances of service X running in locations Y" and have the platform make that true and *keep* it true (source: chapter-05-growing-pains.md). If an instance dies, the platform restarts it. If demand requires more, the platform scales up. If you change the spec, the platform reconciles.

It is the operational counterpart to the architectural shift to many small services. A monolith with one or a handful of instances can be managed manually. A microservice estate with tens or hundreds of services, each with its own desired count, redundancy, and placement requirements, cannot.

## Why this becomes a Chapter 5 pain

Symptoms (source: chapter-05-growing-pains.md):

- Increasing percentage of time spent managing deployments and troubleshooting them.
- Manual processes producing innocent mistakes with hard-to-predict distributed-system effects.
- Calls for more operations headcount, or delivery teams spending more time on deployment than on delivery.

The point at which manual processes break is roughly the point at which the number of services and the variety of their desired states exceed what humans can keep in their head. Tools like Chef and Puppet — designed for traditional configuration management — also start to struggle.

## What good tools provide

Newman's checklist (source: chapter-05-growing-pains.md):

- High degree of automation.
- Developer self-service for provisioning deployments.
- Automated desired-state reconciliation (restart on crash, scale on load).

## Kubernetes

For container-based microservices, Kubernetes has emerged as the tool of choice (source: chapter-05-growing-pains.md). It requires containerisation, but in exchange handles deployment placement across machines, scaling for robustness and load, and continuous reconciliation.

Newman's caveats:

- **Vanilla Kubernetes is not developer-friendly.** Higher-order abstractions are still being built. Larger organisations often adopt packaged distributions like **OpenShift** for corporate identity/access integration and friendlier developer abstractions.
- **Don't reach for Kubernetes too early.** It is "a bit too early" a default for many teams. If your existing solutions handle your five services fine, don't switch.

## Serverless / Function-as-a-Service

For teams already on the public cloud, Newman recommends a **serverless-first** posture (source: chapter-05-growing-pains.md):

> "I've adopted an approach of serverless-first — try to make use of serverless technology like FaaS as a default choice, because of the reduction in operational work. If your problem doesn't fit the limitations of the serverless products available to you, then look for other options."

The reasoning: with FaaS, the platform handles essentially all operational work — including most of what desired-state management is for. You only fall back to container-orchestration platforms when the FaaS limits actually bite.

## Don't adopt because everyone else is

Newman closes the section with the same warning he applies to microservices themselves:

> "Don't adopt a Kubernetes-based platform just because you see everyone else doing it, which can also be said for microservices!" (source: chapter-05-growing-pains.md)

Wait until your existing approach is genuinely straining. Adopting Kubernetes "for the future" before you have the present problem it solves is a way to inherit operational complexity you didn't need.

## Connection to other Chapter 5 pains

- **[[robustness-and-resiliency-at-scale]]**: desired-state management directly contributes to robustness — automatic restarts, multiple copies, replacement of failed instances.
- **[[orphaned-services]]**: a service registry (which a desired-state platform inherently maintains) helps surface orphans because *something* is keeping a list of what's running.
- **[[local-developer-experience]]**: orchestration platforms ease production but not the developer's laptop — see Telepresence and similar tools.

## Related pages

- [[robustness-and-resiliency-at-scale]]
- [[orphaned-services]]
- [[fault-tolerance]]
- [[microservices]]
- [[independent-deployability]]
- [[service-discovery]]
