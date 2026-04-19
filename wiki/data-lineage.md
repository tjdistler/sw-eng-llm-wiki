# Data Lineage

**Summary**: The ability to trace, for any piece of data, **every upstream service and stream it passed through** to get to its current form. In an event-driven microservice organization, data lineage falls out of the [[dependency-tracking-and-topology-visualization|topology graph]] built from [[event-stream-acls|ACLs]] — no separate instrumentation required. In the [[data-engineering-lifecycle|FoDE]] framing, lineage is a form of **technical [[metadata]]** that records an audit trail of data through its lifecycle and is one of the enabling pillars of [[dataops|DataOps]]'s observability pillar.

**Sources**: `raw/building-event-driven-microservices/chapter-14-supportive-tooling.md`, `raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md`

**Last updated**: 2026-04-18

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

## FoDE perspective — lineage as an audit trail across the lifecycle

Reis and Housley's Chapter 2 puts data lineage squarely inside the **[[data-management]]** undercurrent and specifically under the **technical [[metadata]]** category (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md):

> As data moves through its lifecycle, how do you know what system affected the data or what the data is composed of as it gets passed around and transformed? Data lineage describes the recording of an audit trail of data through its lifecycle, tracking both the systems that process the data and the upstream data it depends on.

Their named use cases line up with the Bellemare/EDM ones above plus two explicit additional ones (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md):

- **Error tracking and debugging** — given a bad number, walk back to where it went wrong.
- **Accountability** — knowing who owns each upstream step.
- **Audit trail for compliance** — e.g., a GDPR "right to be forgotten" request: lineage tells you where the user's data is stored and what depends on it. This is the bridge between lineage and [[data-lifecycle-management]].

Chapter 2 notes that lineage historically was a large-company, compliance-driven concern but is now "more widely adopted in smaller companies as data management becomes mainstream" (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

### Data Observability Driven Development (DODD)

Chapter 2 cites Andy Petrella's **DODD** as closely related to lineage: DODD "observes data all along its lineage" during development, testing, and production to deliver quality and conformity to expectations. Lineage gives DODD its dependency direction — observability signals propagate along the lineage graph. See [[data-observability]] (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

### Lineage as infrastructure for destruction

Chapter 2 also notes that new generations of metadata-management, lineage, and cataloguing tools "will streamline the end of the data engineering lifecycle" — because you cannot destroy data you cannot locate, and you cannot destroy it safely without knowing who depends on it. See [[data-lifecycle-management]] (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

## Related pages

- [[edm-supportive-tooling]]
- [[dependency-tracking-and-topology-visualization]]
- [[event-stream-acls]]
- [[event-streams]]
- [[distributed-tracing]]
- [[change-data-capture]]
- [[metadata]]
- [[data-governance]]
- [[data-management]]
- [[data-observability]]
- [[data-lifecycle-management]]
- [[data-catalog]]
