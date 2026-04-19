# Containers

**Summary**: Lightweight virtualization units that package an isolated user space (filesystem, processes) on a shared host kernel, giving dependency and code isolation without full-VM overhead. Reis and Housley treat containers as the middle path between raw [[serverless-vs-servers|servers and serverless]], and as a concrete mitigation for the [[distributed-monolith]] problem.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md`

**Last updated**: 2026-04-18

---

## What a container is

Chapter 4's compact framing (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

> Containers are often referred to as lightweight virtual machines. Whereas a traditional VM wraps up an entire operating system, a container packages an isolated user space (such as a filesystem and a few processes); many such containers can coexist on a single host operating system.

You get the principal benefits of virtualisation — dependency and code isolation — without the overhead of a full OS kernel per instance. One hardware node can host many containers with fine-grained resource allocation.

## Kubernetes and managed container platforms

Chapter 4 notes Kubernetes's role (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

- Kubernetes is a kind of **serverless environment** — developers deploy microservices without managing underlying machines.
- Kubernetes is widely available as a managed service (GKE, AKS, EKS).
- Serverless environments typically run on containers behind the scenes.

### Hybrid container-serverless products

- **Containerised function platforms** — run containers as ephemeral units triggered by events. Lambda-like convenience with container-level flexibility (not stuck on Lambda's restricted runtime). Examples: OpenFaaS, Knative, Google Cloud Run.
- **AWS Fargate, Google App Engine** — run containers without managing a cluster. Also fully isolate containers, avoiding the multitenancy security concerns below.

## The security warning

Chapter 4 is explicit (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

> Container clusters do not provide the same security and isolation that full VMs offer. Container escape — broadly, a class of exploits whereby code in a container gains privileges outside the container at the OS level — is common enough to be considered a risk for multitenancy.

Amazon EC2 is a truly multitenant environment: VMs from many customers share hardware. A Kubernetes cluster should host code only **within an environment of mutual trust** (inside one company). Code review and vulnerability scanning are critical — a developer introducing a security hole can compromise the cluster.

## Role in the distributed-monolith escape

Chapter 4 explicitly names containers as the "proper decomposition" answer for the [[distributed-monolith]] anti-pattern (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

- The Hadoop-style distributed monolith shares one dependency set across all jobs.
- Containers let each job carry **its own isolated dependencies**.
- Hadoop itself now supports containers for exactly this reason.

## Relationship to the cloud stack

Chapter 4's summary:

> Abstraction will continue working its way across the data stack. Consider the impact of Kubernetes on cluster management. While you can manage your Kubernetes cluster — and many engineering teams do so — even Kubernetes is widely available as a managed service.

The abstraction ladder: **bare servers → VMs → containers on VMs → managed Kubernetes → serverless**. Each rung offloads more operational burden to the provider.

## Cross-book framing

- [[container-management-system]] — Burns/Google's Borg/Kubernetes lineage of orchestrators.
- [[pod]] — the Kubernetes multi-container unit.
- [[serverless-vs-servers]] — Chapter 4's high-level debate; containers are the middle option.
- [[serverless-vs-event-driven]] — Burns's two-axis framing of the serverless question.
- [[single-purpose-events|modular reusable containers]] and Burns's Chapter 2 — the single-node container design patterns.

## Related pages

- [[serverless-vs-servers]]
- [[container-management-system]]
- [[pod]]
- [[distributed-monolith]]
- [[functions-as-a-service]]
- [[infrastructure-as-code]]
- [[monolith-vs-modular-data]]
- [[technology-selection]]
