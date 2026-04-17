# Cluster Creation and Management

**Summary**: Self-serve tooling for bringing up new [[event-broker]] clusters, new compute/container clusters, and the supporting tooling *on* those clusters. Larger EDM organizations end up with multiple clusters for isolation, data residency, disaster recovery, and scale; the platform must make cluster lifecycle a button-press, not a month-long project.

**Sources**: `raw/building-event-driven-microservices/chapter-14-supportive-tooling.md`

**Last updated**: 2026-04-17

---

## Why multiple clusters appear

A small-to-medium organization can run EDM on a single event broker cluster. Larger organizations hit several forcing functions (source: chapter-14-supportive-tooling.md):

- **Data residency** — international regulation (GDPR and similar) requires some data to stay in-country.
- **Data size** — even horizontally-scalable brokers have practical single-cluster ceilings.
- **Business-unit isolation** — separate clusters for separate lines of business.
- **Disaster recovery** — cross-region replication via a second cluster.

Bellemare explicitly flags multicluster management as "a complex topic that could very well fill its own book" — Capital One, as a bank, maintains significant custom Kafka tooling specifically to avoid losing financial events during cluster outages (source: chapter-14-supportive-tooling.md).

## Programmatic bringup of event brokers

Hosted options now cover most common brokers — Amazon's managed Kafka (MSK, from late 2018) joined a number of other cloud-provider offerings. The goal regardless of hosting model: **any team can create a broker cluster on demand** via a tool that the organization owns, rather than filing a ticket with a platform team (source: chapter-14-supportive-tooling.md).

## Programmatic bringup of compute

Cloud-managed Kubernetes (GKE, EKS) is the usual substrate. The same residency/redundancy/cost considerations apply to compute as to brokers: distribute across AZs for fault tolerance, keep processing local to data for latency, shift compute-heavy workloads to cheaper providers when possible (source: chapter-14-supportive-tooling.md).

One constraint that binds the two together: compute must have access to the event data it processes, generally by being **colocated** with the broker in the same region or AZ. Cross-region broker access works but is expensive and slow.

## Programmatic bringup of tooling

The crucial second-order point (source: chapter-14-supportive-tooling.md): when a new cluster comes up, the **supportive tooling itself** should come up with it. Benefits:

- **Tooling gets exercised more often** — bugs and missing features surface earlier.
- **Lower barrier to entry** — users encounter the same interfaces on every cluster.
- **Clean teardown** — when the cluster is decommissioned, tooling tears down with it; no external state left behind needing a cleanup job.

The tooling uses only the event broker for durable storage (where applicable), so there are no external dependencies to point at the new cluster.

## Relationship to existing wiki coverage

- **[[container-management-system]]** — the CMS is the underlying compute orchestrator that this tooling provisions.
- **[[cross-cluster-replication]]** — the data-level partner to cluster lifecycle.
- **[[stream-processing-cluster]]** — a specific kind of compute cluster that this tooling stands up (Spark, Flink, etc.).
- **[[microservice-tax]]** — cluster management is part of the tax; centralizing it into a self-serve tool is how large orgs keep the tax bounded.

## Related pages

- [[edm-supportive-tooling]]
- [[event-broker]]
- [[container-management-system]]
- [[cross-cluster-replication]]
- [[stream-processing-cluster]]
- [[microservice-tax]]
