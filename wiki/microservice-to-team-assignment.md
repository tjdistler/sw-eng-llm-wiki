# Microservice-to-Team Assignment

**Summary**: An in-house system that explicitly tracks the mapping **team ↔ microservice ↔ event stream**. Bellemare treats this as the **foundational** EDM supportive tool: almost every other self-serve tool (ACL grants, offset resets, schema notifications, topology visualization) keys off its records to decide who is allowed to do what.

**Sources**: `raw/building-event-driven-microservices/chapter-14-supportive-tooling.md`

**Last updated**: 2026-04-17

---

## What it tracks

A simple in-house microservice that records the dependencies between **people, teams, microservices, and event streams** (source: chapter-14-supportive-tooling.md). For each microservice it holds (at minimum):

- The owning team.
- The humans on that team authorized to act on its behalf.
- The microservice's input streams and output streams (derived from, or cross-referenced with, the [[event-stream-acls|ACLs]]).

Following the [[single-writer-principle]], stream ownership trivially collapses onto microservice ownership: the service that holds `WRITE` on a stream owns it (source: chapter-14-supportive-tooling.md).

## Why it must exist explicitly

When an organization has a handful of systems, tribal knowledge suffices. In the microservice world it doesn't: service counts get into the hundreds, people change teams, and teams reorganize. Without an explicit ownership record (source: chapter-14-supportive-tooling.md):

- Fine-grained DevOps permissions cannot be correctly assigned.
- Change requests have no one to route to.
- Schema and ACL change notifications have no destination.
- Orphaned streams and services cannot be distinguished from actively owned ones.

## It is the policy layer for other tools

Bellemare's tools that **consume** this system:

- **[[event-stream-acls]]** — only the owning team can grant, modify, or revoke permissions on the streams its services own.
- **[[event-stream-metadata]]** — only the owning team can tag or untag streams.
- **[[application-reset-tool]]** — only the owning team can reset a service's offsets or state.
- **[[consumer-lag-monitoring]] / autoscaling** — alerts and scale actions route to the owning team.
- **[[schema-change-notifications]]** — resolved from consumer ACLs to owning teams.
- **[[dependency-tracking-and-topology-visualization]]** — team overlays on the topology graph come from here.

This is why Bellemare recommends building this tool first.

## Relationship to existing wiki coverage

- **[[orphaned-services]]** — Newman's FT Biz Ops and System Operability Score are the same organ of assignment tracking, generalized beyond EDM.
- **[[code-ownership-models]]** — strong vs collective ownership is the organizational model this tool operationalizes.
- **[[conways-law]]** — the assignment system is the machine-readable encoding of the organization's communication structure.

## Related pages

- [[edm-supportive-tooling]]
- [[event-stream-acls]]
- [[single-writer-principle]]
- [[orphaned-services]]
- [[code-ownership-models]]
- [[conways-law]]
