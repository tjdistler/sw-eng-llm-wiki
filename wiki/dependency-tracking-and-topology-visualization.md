# Dependency Tracking and Topology Visualization

**Summary**: A tool that derives the full graph of microservices, event streams, and their producer/consumer relationships from [[event-stream-acls|ACLs]], overlays team ownership from [[microservice-to-team-assignment]], and renders it as an interactive [[business-topology]] map. Uses include data-source discovery, cross-team coupling metrics, business-to-implementation alignment review, and the underlying engine for [[data-lineage]].

**Sources**: `raw/building-event-driven-microservices/chapter-14-supportive-tooling.md`

**Last updated**: 2026-04-17

---

## Why ACL-derived beats self-reporting

A self-reporting system, where each service declares what it reads and writes, has an unsolvable compliance problem: some teams forget, some opt out, some deliberately don't. A partial graph is not much more useful than no graph (source: chapter-14-supportive-tooling.md).

ACL-derived graphs are **involuntarily complete**. A service that isn't in the ACL records literally cannot talk to the broker. Every change to the graph is a change to the ACLs and happens automatically. This is the structural reason Bellemare insists on building [[event-stream-acls|ACLs]] early — they are the foundation that makes every downstream visibility tool work.

## What the tool gives you

Bellemare lists five uses (source: chapter-14-supportive-tooling.md):

1. **Data lineage** — trace any event back to its producing ancestors. See [[data-lineage]].
2. **Team-boundary overlay** — color the graph by owning team; instantly see which services cross which boundaries.
3. **Data discovery** — a prospective consumer browses available streams and sees who produces and consumes each.
4. **Interconnectedness / complexity metrics** — count cross-team connections per team as a crude coupling metric. Fewer external connections per team is better.
5. **Business-function alignment** — map each microservice to the business requirement it implements, overlay teams, and ask *"does this implementation structure align with the goals of this team?"*

## The worked 25-service example

Chapter 14's Figure 14-2 shows four teams owning 25 microservices. The analysis identifies two microservices (2 and 7) that are owned by Team 2 but sit far from Team 2's other services in the graph — an "ownership island." Moving them to Teams 4 and 1 respectively, plus reassigning microservice 1 to Team 4, **net-reduces cross-team connections by three** (source: chapter-14-supportive-tooling.md).

The worked example is in service of a general point: reducing cross-boundary edges is a useful optimization target, but not the only one. Team expertise, head count, implementation complexity, and — most importantly — **business-function alignment** all matter. A team that sources external data into events will legitimately have many edges and still be well-aligned. The tool gives the business owner the data; humans make the call.

## Historical views

Because ACLs and ownership assignments are stored as event streams (see [[event-stream-acls]]), the tool can replay them to reconstruct the topology **at any past point in time** (source: chapter-14-supportive-tooling.md). Useful when auditing an incident from six months ago and needing to know what the dependency graph looked like then, not now.

## Relationship to existing wiki coverage

- **[[business-topology]]** — this tool's output *is* the business topology, made concrete and navigable.
- **[[microservice-topology]]** — the inside-a-service view the visualizer does not show.
- **[[event-stream-acls]]** — the source of truth for the dependency edges.
- **[[microservice-to-team-assignment]]** — the source of truth for the team overlay.
- **[[data-lineage]]** — a specific application of the same underlying graph.
- **[[conways-law]]** — the overlay-team-on-topology view is a direct Conway's-law diagnostic.

## Related pages

- [[edm-supportive-tooling]]
- [[business-topology]]
- [[event-stream-acls]]
- [[microservice-to-team-assignment]]
- [[data-lineage]]
- [[conways-law]]
- [[orphaned-streams]]
