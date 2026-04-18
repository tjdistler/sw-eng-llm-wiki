# Container Management System

**Summary**: The category of purpose-built software that controls **container and VM deployment, resource allocation, and orchestration** on underlying compute resources. Kubernetes, Docker Engine, Mesos Marathon, Amazon ECS, and Nomad are the canonical examples. A CMS is one of the two largest line items in the [[microservice-tax]] for any non-trivial microservice platform.

**Sources**: `raw/building-event-driven-microservices/chapter-02-event-driven-microservice-fundamentals.md`, `raw/building-event-driven-microservices/chapter-14-supportive-tooling.md`, `raw/site-reliability-engineering/chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md`

**Last updated**: 2026-04-17

---

## What a CMS does

A CMS sits between microservice deployment units (containers or VMs) and the underlying compute (physical hosts or cloud instances). Its core responsibilities are (source: chapter-02-event-driven-microservice-fundamentals.md):

- **Deployment control.** Place, start, stop, and restart containers across a fleet of hosts.
- **Resource allocation.** Assign CPU, memory, and disk budgets; schedule placement to fit resources available.
- **Scaling.** Support both **vertical** scaling (adjusting CPU/memory/disk per instance) and **horizontal** scaling (adding or removing instances).
- **Integration with compute.** Talk to the underlying cloud provider or on-prem scheduler to acquire and release capacity.

Popular CMSes: Kubernetes, Docker Engine, Mesos Marathon, Amazon ECS, Nomad (source: chapter-02-event-driven-microservice-fundamentals.md).

## Unit of deployment

A simple microservice is often a single executable deployed in a single container. More complex services may require **multiple containers** that must be coordinated together — sidecars, data stores, migration steps. Kubernetes' [[pod]] concept is Bellemare's example of a CMS primitive that treats a group of containers as a single deployable and revertible unit (source: chapter-02-event-driven-microservice-fundamentals.md).

Kubernetes also supports single-run operations like **database migrations** alongside the main deployable, allowing operational steps to ride along with a rollout (source: chapter-02-event-driven-microservice-fundamentals.md).

## Containers vs virtual machines

Bellemare covers both container and VM approaches to isolating microservices (source: chapter-02-event-driven-microservice-fundamentals.md):

| | Containers | Virtual machines |
|---|---|---|
| Isolation | Shared OS kernel; isolates env, libs, deps | Full OS + virtual hardware per instance |
| Cost | Fast startup, low overhead | Higher overhead, slower startup |
| Security | Kernel vulnerability can affect all containers on the host | Stronger isolation; self-contained OS |
| Fit | Friendly workloads; most common microservice choice | Security-first requirements |

The line is blurring: Google's gVisor, Amazon's Firecracker, and Kata Containers aim to make VMs cheaper and more efficient for microservice workloads. Kubernetes and Docker Engine support gVisor and Kata Containers; Amazon's platform supports Firecracker (source: chapter-02-event-driven-microservice-fundamentals.md). Bellemare's advice: pick a CMS that will handle the container and VM options you actually need.

## What to expose to service teams

Bellemare recommends the CMS expose certain controls **self-serve** to microservice owners, leaving the rest to a central ops team. The question is cultural — how much DevOps sits inside product teams — but the typical split (source: chapter-14-supportive-tooling.md):

- Environment variables, per-cluster deployment targeting (testing / integration / production).
- CPU / memory / disk budgets per service.
- Manual instance-count controls.
- **Autoscaling policies** based on CPU, memory, disk, or [[consumer-lag-monitoring|consumer lag]].

Cluster bringup itself is a separate tool — see [[cluster-creation-and-management]].

## Google's internal ancestor: Borg

[[borg|Borg]] is Google's distributed cluster operating system and the direct ancestor of Kubernetes. The SRE book describes it as a cluster-level job manager similar to Apache Mesos, open-sourced as Kubernetes in 2014 (source: site-reliability-engineering, chapter 2). Borg is the internal reference system behind the CMS category — Bellemare's framing and Burns's patterns (sidecar, pod, operator) are both descended from what Borg pioneered inside Google: fluid task placement, failure-domain-aware binpacking, declarative resource budgets, automatic restart, and [[bns|BNS]]-based indirection for addressing.

## Relationship to existing wiki coverage

- **[[borg]]** — the Google-internal ancestor; Kubernetes is its open-source descendant.
- **[[pod]]** — the Kubernetes multi-container primitive Bellemare points to as a typical CMS unit.
- **[[desired-state-management]]** — Newman's name for the declarative-spec-plus-reconciliation operational pattern, which is the defining operating mode of modern CMSes like Kubernetes.
- **[[running-too-many-things]]** — Newman's observation that manual deployment doesn't scale past a certain service count; a CMS is the usual answer.
- **[[operator-pattern]]** — application-specific controllers that extend a CMS declarative API.
- **[[microservice-tax]]** — the CMS is one of the two largest line items.

## Related pages

- [[borg]]
- [[pod]]
- [[desired-state-management]]
- [[running-too-many-things]]
- [[operator-pattern]]
- [[microservice-tax]]
- [[event-driven-microservices]]
- [[microservices]]
- [[independent-deployability]]
- [[cluster-creation-and-management]]
- [[consumer-lag-monitoring]]
- [[edm-supportive-tooling]]
