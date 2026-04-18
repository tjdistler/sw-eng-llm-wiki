# Consensus Read Optimisations

**Summary**: Chapter 23's four-option menu for serving reads against a consensus-backed datastore under different latency, availability, and consistency requirements: read-only consensus operation, leader read, quorum lease, and stale replica read. The choice is per-workload: Photon happily reads stale because stale means extra work, not wrong answers; a financial ledger cannot.

**Sources**: `raw/site-reliability-engineering/chapter-23-managing-critical-state-distributed-consensus-for-reliability.md`

**Last updated**: 2026-04-17

---

## Why this matters

Many workloads are read-heavy. Replicated datastores have the data available in multiple places, so if strong consistency is not required for all reads, data can be read from any replica. Chapter 23 gives Google's Photon as the canonical example: it uses an atomic compare-and-set for state modification (inspired by atomic registers) that must be absolutely consistent, but "read operations may be served from any replica, because stale data results in extra work being performed but not incorrect results" (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md). The trade-off is worthwhile for that workload.

## The four options for strongly-consistent reads

Chapter 23 enumerates the options when the read must be strongly consistent — that is, guaranteed to reflect all writes performed before the read started (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md):

| Option | Mechanism | Latency | Where it wins |
|---|---|---|---|
| Read-only consensus op | Full consensus round on read | Consensus RTT | Works anywhere; last resort |
| Leader read | [[stable-leader\|Stable leader]] has latest state | LAN RTT if client is near the leader | Stable-leader systems; local clients |
| [[quorum-leases\|Quorum lease]] | Lease grants read quorum the right to serve local reads | Local replica read | Geographic read clustering; read-heavy |
| Stale replica read | Read any replica; accept staleness | Local replica read | Workloads where stale = extra work only |

The first three are strongly consistent; the fourth is not. The Chapter 23 list above excludes option 4 — it is mentioned separately as the Photon approach.

## Picking an option

The decision axes Chapter 23 surfaces:

- **Does stale data produce wrong answers or just extra work?** If the latter, option 4 is often the right answer.
- **Are clients concentrated near the leader?** If so, option 2 is the simplest strong option.
- **Are reads concentrated in a region away from the leader?** That's the quorum-lease case (option 3).
- **Do reads need to be serviceable anywhere with strong consistency?** That's option 1, accepting the latency cost.

## Relationship to linearizability

"Strongly consistent" here is [[linearizability|linearizability]] — every read reflects every write that completed before it started, as visible to any client. Options 2 and 3 preserve linearizability via the "has-seen-all-recent-state-changes" property of the serving replica. Option 4 provides [[eventual-consistency]] rather than linearizability.

## Cross-book framing

- [[linearizability]] — the consistency model being served
- [[leader-based-replication]] (Kleppmann) — read-from-follower-or-leader is the DDIA replication-level analogue, without the consensus substrate
- [[replication-lag]] (Kleppmann) — the mechanism that makes replica reads potentially stale
- [[eventual-consistency]] — what you get from option 4
- [[coordination-avoidance]] (Kleppmann) — the broader principle: you don't always need coordination for correctness

## Related pages

- [[managing-critical-state]]
- [[consensus]]
- [[quorum-leases]]
- [[stable-leader]]
- [[consensus-performance]]
- [[linearizability]]
- [[reliable-replicated-datastore]]
