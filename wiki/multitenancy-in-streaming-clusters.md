# Multitenancy in Streaming Clusters

**Summary**: As the number of applications on a [[stream-processing-cluster|streaming cluster]] grows, resource contention between jobs becomes a real operational risk — one replay-from-the-beginning job can starve every SLO-sensitive job running next to it. Bellemare names two mitigations: **many smaller clusters** or **namespacing within one cluster**, each with a different overhead/isolation trade-off (source: chapter-11-heavyweight-framework-microservices.md).

**Sources**: `raw/building-event-driven-microservices/chapter-11-heavyweight-framework-microservices.md`

**Last updated**: 2026-04-17

---

## The contention problem

Three variables drive multitenancy issues on a shared cluster (source: chapter-11-heavyweight-framework-microservices.md):

- **Priority of resource acquisition** — which jobs get cluster resources first.
- **Ratio of spare to committed resources** — how much headroom is kept for bursts and new jobs.
- **Rate of resource claims** — how aggressively jobs can scale up to grab capacity.

Bellemare's canonical failure mode: a new streaming application starts from the beginning of time on its input topics and requests the majority of free cluster resources to catch up. Running applications cannot acquire resources when they need them, miss their SLOs, and create downstream business problems.

## Mitigation 1: Run many smaller clusters

Each team or business unit gets its own cluster, fully isolated from other teams' (source: chapter-11-heavyweight-framework-microservices.md).

Works best when clusters can be **requisitioned programmatically** — via in-house automation or a third-party hosted service. Otherwise, the coordinator overhead (master nodes, Zookeeper, monitoring, upgrades) gets duplicated per cluster and adds up.

| Pro | Con |
|---|---|
| Strong isolation between teams | Higher aggregate financial cost |
| Simple resource accounting | Per-cluster operational overhead |
| Per-team autonomy over versioning and config | Difficult to share compute across idle/busy teams |

## Mitigation 2: Namespacing within one cluster

One cluster, divided into **namespaces with specific resource allocations.** Each team's jobs can only claim resources within their own namespace, preventing cross-team starvation (source: chapter-11-heavyweight-framework-microservices.md).

| Pro | Con |
|---|---|
| Shared coordinator/Zookeeper overhead | Idle namespace resources sit unused |
| Single operational platform | Fragmented free-capacity pool |
| Resource limits enforceable per team | Noisy-neighbor risks remain within a namespace |

The sharp edge: spare resources have to be pre-allocated to each namespace even when unused. A cluster with five namespaces might effectively waste 20% of its capacity even when most of that is idle.

## Picking a strategy

Small organizations with one team often don't need either — one cluster, one tenant. As the organization grows:

- Teams with strong SLO requirements or disparate workload profiles lean toward **separate clusters.**
- Teams comfortable sharing operational discipline and willing to trade some capacity for simpler operations lean toward **namespacing.**

The choice has the same flavor as the central-vs-per-team framing in [[microservice-tax]]: one well-operated shared thing vs several small isolated things, with the right answer depending on scale and organizational structure.

## Related pages

- [[heavyweight-framework-microservice]]
- [[stream-processing-cluster]]
- [[stream-processing-scaling-strategies]]
- [[microservice-tax]]
- [[container-management-system]]
