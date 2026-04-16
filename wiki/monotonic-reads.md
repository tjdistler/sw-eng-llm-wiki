# Monotonic Reads

**Summary**: A consistency guarantee that ensures a user never observes data going *backward in time* — if they have seen a value once, subsequent reads will not return an older version of that value.

**Sources**: `raw/designing-data-intensive-applications/chapter-05-replication.md`

**Last updated**: 2026-04-15

---

## The problem

In a system with asynchronous followers, a user may make two successive reads that are routed to different replicas. If the second replica is further behind than the first, the user sees data *disappear* — something visible in the first read is absent in the second. From the user's perspective, time appears to go backward.

This is one of the three anomalies caused by [[replication-lag]]. It is distinct from stale reads in general: the issue is not that the data is old, but that the *second* read is older than the *first*.

## The guarantee

Monotonic reads is a weaker guarantee than strong (linearizable) consistency, but stronger than [[eventual-consistency]]. It says:

> If a user makes several reads in sequence, they will not see older data after having seen newer data.

It does *not* guarantee that reads return the latest write — only that reads don't regress.

## Implementation

**Sticky replicas**: route each user to the same replica for all reads. The simplest implementation hashes the user ID to select a replica. This replica may still be behind the leader, but it will never appear to go backward from that user's perspective.

Caveat: if the assigned replica fails, the user's reads must be rerouted to another replica — which may itself be at a different (potentially earlier) point. The guarantee breaks at the boundary of a replica failure.

## Relationship to other guarantees

Monotonic reads, [[read-after-write-consistency]], and [[consistent-prefix-reads]] are three independent consistency properties. A system can provide any combination of them. Providing all three requires careful routing and coordination but is achievable without full transactions.

## Related pages

- [[replication-lag]]
- [[read-after-write-consistency]]
- [[consistent-prefix-reads]]
- [[eventual-consistency]]
- [[replication]]
