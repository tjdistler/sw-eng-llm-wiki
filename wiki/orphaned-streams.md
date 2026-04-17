# Orphaned Streams

**Summary**: Event streams that have no active consumers, and microservices that produce only to streams no one consumes. In an EDM organization these are discoverable **automatically** by cross-referencing the [[event-stream-acls|ACL]] records against the set of live streams and services — the operational counterpart to Newman's [[orphaned-services]].

**Sources**: `raw/building-event-driven-microservices/chapter-14-supportive-tooling.md`

**Last updated**: 2026-04-17

---

## Two kinds of orphans

Bellemare's cleanup pass (source: chapter-14-supportive-tooling.md):

- **An orphaned stream** — a stream with `WRITE` permissions granted to some producer but zero outstanding `READ` grants held by any consumer. Candidate for deletion.
- **An orphaned microservice** — a producer whose only output streams are themselves orphaned. Candidate for decommission.

Detection is a straightforward graph query against the dependency graph built by [[dependency-tracking-and-topology-visualization]].

## Why this is strictly easier than the general orphan problem

Newman's [[orphaned-services]] problem — services quietly running for years with no owner — is harder because ownership information is often absent or stale. In an EDM organization with [[microservice-to-team-assignment]] and [[event-stream-acls|ACLs]] in place, the graph is **complete by construction**:

- A service cannot produce to or consume from a stream without registered ACLs.
- Every ACL record maps to an owning microservice which maps to an owning team.

The "no one in the company is taking ownership" failure mode Newman describes cannot arise here unless the ownership record itself falls out of date — which is visible and fixable, not invisible.

## Relationship to existing wiki coverage

- **[[orphaned-services]]** — Newman's more general framing (FT Biz Ops, System Operability Score). The EDM-specific mechanism complements rather than replaces it.
- **[[event-stream-acls]]** — the source of truth.
- **[[event-stream-metadata]]** — the **deprecation** tag is the graceful-decomm workflow for orphaning a stream intentionally.
- **[[dependency-tracking-and-topology-visualization]]** — the tool that surfaces orphans visually.

## Related pages

- [[edm-supportive-tooling]]
- [[orphaned-services]]
- [[event-stream-acls]]
- [[event-stream-metadata]]
- [[dependency-tracking-and-topology-visualization]]
