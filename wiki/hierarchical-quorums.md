# Hierarchical Quorums

**Summary**: A consensus quorum scheme that groups replicas into sub-groups (typically three groups of three), where a quorum requires a **majority of groups** *and* each contributing group needs a **majority of its members available**. Mitigates the flat-majority weakness that a single replica acting as a [[quorum-composition|linchpin]] between widely-separated regions can hugely increase latency on failure — in a hierarchical scheme, the local group's redundancy absorbs the failure.

**Sources**: `raw/site-reliability-engineering/chapter-23-managing-critical-state-distributed-consensus-for-reliability.md`

**Last updated**: 2026-04-17

---

## The scheme

Deploy 9 replicas in 3 groups of 3. Form a quorum as follows (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md):

1. A **majority of groups** must participate (2 out of 3).
2. Each participating group must have a **majority of its members available** (2 out of 3).

So a quorum requires 2 groups × 2 members = 4 available replicas. Contrast with a flat 9-replica majority, which requires 5.

## Why it helps

A flat 9-replica quorum is sensitive to the single most expensive-to-reach replica — any 5 must respond, so even if 4 are local and fast, the 5th response from a remote replica dominates latency.

In a hierarchical scheme, the central group can **lose one replica** without incurring a large impact on overall system performance: the central group can still participate with its remaining 2 members. The local redundancy absorbs the failure that would otherwise have forced the system to fall back to a distant quorum — which is exactly the problem on [[quorum-composition]]'s linchpin-failure page.

## The resource cost

Running 9 replicas costs more than running 5. Chapter 23's mitigation: "In a highly sharded system with a read-heavy workload that is largely fulfillable by replicas, we might mitigate this cost by using fewer consensus groups. Such a strategy means that the overall number of processes in the system may not change" (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md).

So the operational move: collapse shards (fewer groups, each with more replicas) rather than add replicas per shard. The total process count stays comparable; the per-shard resilience characteristic changes.

## When to use

Hierarchical quorums are a mitigation for the specific case where:

- Replicas span multiple distant regions with very different inter-region RTTs.
- A flat majority quorum's latency depends heavily on one or two *linchpin* replicas — see [[quorum-composition]].
- The workload can tolerate the extra replica cost or can absorb it via consolidation of shards.

For a single-region deployment, a flat 3- or 5-replica quorum is simpler and sufficient.

## Cross-book framing

- [[quorums]] (Kleppmann) — the DDIA page on w + r > n quorums in leaderless replication; same fundamental primitive, different layer. Hierarchical quorums as discussed here apply to consensus-group membership; Kleppmann's treatment applies to read/write quorums in Dynamo-style systems.
- [[partitioning]] (Kleppmann) — the "collapse shards to afford more replicas per shard" operational move is the partitioning-granularity decision, applied to consensus

## Related pages

- [[managing-critical-state]]
- [[consensus]]
- [[quorum-composition]]
- [[consensus-replica-count]]
- [[consensus-replica-placement]]
- [[quorums]]
