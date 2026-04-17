# Running Too Many Things

**Summary**: As service count and instance count grow, deployment and configuration management techniques that worked for a monolith stop scaling. The core capability you need is [[desired-state-management]] — and the operational frame Newman recommends is "serverless-first if you can; Kubernetes when you must; don't adopt either too early".

**Sources**: `raw/monolith-to-microservices/chapter-05-growing-pains.md`, `raw/designing-distributed-systems/chapter-08-functions-and-event-driven-processing.md`

**Last updated**: 2026-04-16

---

## The problem

More services and more instances mean more processes to deploy, configure, and manage. Whatever you used for the monolith — manual SSH, scripts, traditional configuration management like Chef or Puppet — won't scale to tens or hundreds of microservices, especially when each has its own desired state (source: chapter-05-growing-pains.md).

## Symptoms

(source: chapter-05-growing-pains.md)

- Increasing percentage of time spent managing deployments and troubleshooting them.
- Manual processes producing innocent mistakes whose distributed-system consequences are hard to predict.
- Calls for more ops headcount, or delivery teams losing more time to deployment work.

## What you actually need

The capability is [[desired-state-management]]: declaratively specify the number and location of service instances, and have a platform reconcile reality with that spec.

Newman's checklist for the platform (source: chapter-05-growing-pains.md):

- High degree of automation.
- Developer self-service for provisioning deployments.
- Automated desired-state reconciliation.

## Newman's tooling preferences

### Serverless-first on public cloud

If you're already on the public cloud, default to **Function-as-a-Service** (source: chapter-05-growing-pains.md):

> "I've adopted an approach of serverless-first — try to make use of serverless technology like FaaS as a default choice, because of the reduction in operational work."

The reasoning: with FaaS, the platform handles essentially all the operational work that desired-state management exists for. Reach for container orchestration only when FaaS limits actually bite.

Burns's Chapter 8 of *Designing Distributed Systems* catalogues **where those limits actually are** (source: raw/designing-distributed-systems/chapter-08-functions-and-event-driven-processing.md): sustained high-volume request serving (pay-per-request loses to VMs), work that needs large warm in-memory state (cold starts dominate latency), long-running background jobs (runtime caps disqualify it), and workloads whose cross-function dependencies are hard to reason about (debugging is the main operational complaint). See [[functions-as-a-service]] for the full discussion and [[serverless-vs-event-driven]] for the distinction between the two axes — you can get one benefit without the other. Burns's recommendation in the same chapter for teams that have outgrown the per-request pricing of public-cloud FaaS matches Newman's other recommendation on this page: **run an open-source FaaS on a Kubernetes cluster you control**.

### Kubernetes when needed

For container-based microservices, Kubernetes is the dominant choice. Newman's caveats:

- **Vanilla Kubernetes isn't developer-friendly.** Larger orgs often adopt packaged distributions (e.g. **OpenShift**) for corporate identity/access integration and friendlier abstractions.
- **In the future, many developers running on Kubernetes won't know it.** Higher-order abstractions are being built that hide it.
- **Don't adopt early.** "Platforms like Kubernetes excel at helping you manage multiple processes, but you should wait until you have enough processes that your current approach and technology are starting to strain." (source: chapter-05-growing-pains.md)

### Don't adopt because everyone else is

The same warning he applies to microservices themselves:

> "Don't adopt a Kubernetes-based platform just because you see everyone else doing it, which can also be said for microservices!" (source: chapter-05-growing-pains.md)

If five microservices fit comfortably in your existing solution, stay there.

## Connection to other Chapter 5 pains

- **[[desired-state-management]]** — the underlying capability this section is about.
- **[[robustness-and-resiliency-at-scale]]** — automatic restarts, multiple instances, scheduling are all robustness-via-platform.
- **[[orphaned-services]]** — the runtime state the platform tracks is one input to detecting orphans.
- **[[local-developer-experience]]** — production tooling doesn't fix the developer's laptop; that needs separate investment.

## Related pages

- [[desired-state-management]]
- [[robustness-and-resiliency-at-scale]]
- [[microservices]]
- [[independent-deployability]]
- [[orphaned-services]]
- [[functions-as-a-service]]
- [[serverless-vs-event-driven]]
