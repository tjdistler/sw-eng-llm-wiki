# Event Stream ACLs

**Summary**: Per-microservice permissions (`READ` / `WRITE` / `CREATE` / `DELETE` / `MODIFY` / `DESCRIBE`) on event streams, enforced by the [[event-broker]]. ACLs are how the [[single-writer-principle]] is made into a hard boundary, how [[bounded-context|bounded contexts]] stay sealed, and how the [[dependency-tracking-and-topology-visualization|topology graph]] and [[data-lineage]] can be reconstructed without voluntary self-reporting.

**Sources**: `raw/building-event-driven-microservices/chapter-14-supportive-tooling.md`

**Last updated**: 2026-04-17

---

## The permission model

Most [[event-broker|event brokers]] offer some subset of (source: chapter-14-supportive-tooling.md):

- **READ** — consume events.
- **WRITE** — produce events.
- **CREATE / DELETE / MODIFY** — stream lifecycle.
- **DESCRIBE** — read metadata without reading events.

The typical allocation for a microservice (source: chapter-14-supportive-tooling.md):

| Component | Permissions for the owning microservice |
|---|---|
| Input event streams | `READ` |
| Output event streams | `CREATE`, `WRITE` (and `READ` if used internally) |
| Internal & [[changelog-stream|changelog]] streams | `CREATE`, `WRITE`, `READ` |

Only the owning microservice has `WRITE` on an output stream — this is the [[single-writer-principle]] made mechanical. No other service may ever write to that stream.

## Identity is a day-one decision

> "ACLs rely on individual identification for each consumer and producer. Ensure that you enable and enforce identification for your event broker and services as soon as possible, preferably from day one. Adding identification after the fact is extremely painful, as it requires updating and reviewing every single service that connects to the event broker." (source: chapter-14-supportive-tooling.md)

A corollary that does not get said enough: retrofitting ACLs onto an unauthenticated broker is usually the single most expensive piece of platform work an EDM-using org will ever do.

## Self-serve request/grant workflow

The chapter describes two styles of self-serve ACL grants (source: chapter-14-supportive-tooling.md):

- **Owner-decides** — the owning team receives access requests from consumer teams and grants or denies. Minimal central bottleneck.
- **Centralized review** — requests for sensitive streams (PII, financial — see [[event-stream-metadata]]) are routed through a security team first.

Both styles use the [[microservice-to-team-assignment]] system to map requestor identity onto a team.

## ACL changes as an event stream

The granting and revoking of permissions can itself be stored as a stream of events (source: chapter-14-supportive-tooling.md). This produces a durable, immutable audit record: *who had what access on what date, and why was it granted or revoked?* It also provides the historical record that lets the [[data-lineage]] tool reconstruct the topology **at any point in the past**.

## ACLs as the dependency graph source of truth

Because every microservice must register its ACL needs to function at all, the ACL set is the **involuntarily-complete** map of consumer→stream→producer relationships (source: chapter-14-supportive-tooling.md). This is why Bellemare favors ACLs over self-reporting for [[dependency-tracking-and-topology-visualization|topology tooling]]:

- A service cannot "forget" to report — without its ACL it does not function.
- Any change to dependencies is reflected automatically.
- The graph includes every service, not just the compliant ones.

## Orphan detection

Cross-referencing ACLs against live streams and microservices surfaces **orphans** (source: chapter-14-supportive-tooling.md). See [[orphaned-streams]].

## Relationship to existing wiki coverage

- **[[single-writer-principle]]** — ACLs are its enforcement point.
- **[[bounded-context]]** — ACLs keep contexts sealed: a service may not read another's internal or [[changelog-stream|changelog]] streams.
- **[[service-discovery]]** — addresses the "where is it" question; ACLs address the orthogonal "who may talk to it" question.

## Related pages

- [[edm-supportive-tooling]]
- [[single-writer-principle]]
- [[event-broker]]
- [[event-stream-metadata]]
- [[microservice-to-team-assignment]]
- [[dependency-tracking-and-topology-visualization]]
- [[data-lineage]]
- [[orphaned-streams]]
- [[bounded-context]]
