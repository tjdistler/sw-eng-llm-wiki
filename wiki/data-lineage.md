# Data Lineage

**Summary**: The ability to trace, for any piece of data, **every upstream service and stream it passed through** to get to its current form. In an event-driven microservice organization, data lineage falls out of the [[dependency-tracking-and-topology-visualization|topology graph]] built from [[event-stream-acls|ACLs]] — no separate instrumentation required.

**Sources**: `raw/building-event-driven-microservices/chapter-14-supportive-tooling.md`

**Last updated**: 2026-04-17

---

## Why data engineers and scientists need it

A recurring data-team problem: a number in a dashboard looks wrong, or a model is misbehaving, and the investigator needs to know **where this data came from**. What stream? Produced by which service? Derived from which upstream streams? Which previous transformation introduced the defect? (source: chapter-14-supportive-tooling.md)

Without lineage, each investigation starts from scratch — reading code, interviewing teams, guessing.

## How it falls out of ACLs for free

The full ACL-derived dependency graph is a directed graph: producer microservice → output stream → consumer microservices (some of which are themselves producers of downstream streams) → ... By walking *backwards* from any stream, you get every ancestor service and stream — the full lineage (source: chapter-14-supportive-tooling.md).

This is the same graph [[dependency-tracking-and-topology-visualization|topology visualization]] uses; lineage is just the ancestor-subgraph query.

## Historical lineage

Because the ACL changes and [[microservice-to-team-assignment|team-assignment]] changes are themselves stored as event streams, you can reconstruct the topology at any past point in time. A lineage query against old data answers *"what was the graph like when this data was produced?"* rather than *"what is the graph like now?"* (source: chapter-14-supportive-tooling.md) — which is usually the question you actually want answered when auditing six-month-old records.

## Lineage vs distributed tracing

The two are complementary (not overlapping):

| | Distributed tracing | Data lineage |
|---|---|---|
| Scope | Per-request | Per-dataset / per-stream |
| Granularity | Single call chain | Architectural-graph level |
| Source | Span instrumentation inside services | ACL and ownership records outside services |
| Answer shape | "What did *this request* do?" | "Where did *this data* come from?" |

See [[distributed-tracing]] for the request-oriented companion.

## Relationship to existing wiki coverage

- **[[dependency-tracking-and-topology-visualization]]** — the tool from which lineage is derived.
- **[[event-stream-acls]]** — the raw source of lineage edges.
- **[[event-streams]]** — the "stream as single source of truth" framing is what makes lineage queries meaningful.
- **[[distributed-tracing]]** — the per-request companion.

## Related pages

- [[edm-supportive-tooling]]
- [[dependency-tracking-and-topology-visualization]]
- [[event-stream-acls]]
- [[event-streams]]
- [[distributed-tracing]]
- [[change-data-capture]]
