# EDM Supportive Tooling

**Summary**: Adam Bellemare's hub framing for the **self-serve DevOps tools** that make event-driven microservices manageable at scale. As service and stream counts grow, tribal knowledge and admin-only CLIs stop working — every major operation (ownership assignment, ACL grants, stream creation, offset resets, cluster bringup) needs a first-class, team-facing tool so that the organization scales elastically with its [[event-driven-microservices|EDM]] investment.

**Sources**: `raw/building-event-driven-microservices/chapter-14-supportive-tooling.md`

**Last updated**: 2026-04-17

---

## Why supportive tooling is a distinct category

Many of the tools in this chapter are things an administrator could do by hand with a CLI or a shell script. The point Bellemare makes is that manual tooling does not scale past a small number of services: teams get blocked on an ops bottleneck, tribal knowledge accumulates, and the [[microservice-tax]] becomes paid per-team-per-task rather than once centrally (source: chapter-14-supportive-tooling.md). Self-serve tools move the tax from recurring manual effort into a one-time platform build.

"Unfortunately, there is a dearth of freely available open source tooling for managing event-driven microservices" — Bellemare notes that organizations often write these tools in-house, and encourages contributing back when possible (source: chapter-14-supportive-tooling.md).

## The tooling catalog

| Area | Page |
|---|---|
| Ownership tracking | [[microservice-to-team-assignment]] |
| Stream creation, modification, metadata | [[event-stream-metadata]] |
| Throughput protection | [[event-broker-quotas]] |
| Schema management | [[schema-registry]], [[schema-change-notifications]] |
| Access control | [[event-stream-acls]] |
| Offsets and state | [[application-reset-tool]] |
| Autoscaling signal | [[consumer-lag-monitoring]] |
| Repo scaffolding | [[microservice-creation-workflow]] |
| Compute orchestration | [[container-management-system]] |
| Cluster lifecycle | [[cluster-creation-and-management]] |
| Cross-cluster data | [[cross-cluster-replication]] |
| Dependency graph | [[dependency-tracking-and-topology-visualization]] |
| Data provenance | [[data-lineage]] |
| Orphan cleanup | [[orphaned-streams]] |

## The two foundational tools

Two tools recur as dependencies of all the others:

1. **[[microservice-to-team-assignment]]** — maps teams ↔ microservices ↔ streams. Every other tool's permission model depends on it.
2. **[[event-stream-acls]]** — the [[single-writer-principle|single-writer]] enforcement point and the input to dependency tracking, lineage, and orphan detection.

Build these first; almost every other tool in the chapter consumes one or both.

## Programmatic bringup

A corollary theme: when a new cluster is brought up, the **tooling itself** should come up with it, not just the broker (source: chapter-14-supportive-tooling.md). Benefits: the tools get exercised often enough to reveal bugs, users see the same interfaces on every cluster, and teardown is clean because no external state needs cleanup. See [[cluster-creation-and-management]].

## Related pages

- [[event-driven-microservices]]
- [[microservice-tax]]
- [[event-broker]]
- [[single-writer-principle]]
- [[business-topology]]
