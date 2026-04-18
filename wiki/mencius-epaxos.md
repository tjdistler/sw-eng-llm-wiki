# Mencius and Egalitarian Paxos

**Summary**: Two consensus protocols that avoid the single-[[stable-leader|stable-leader]] bottleneck by either pre-assigning proposals to replicas in rotation (**Mencius**, Mao 2008) or by having every replica propose for itself with a conflict-detection scheme (**Egalitarian Paxos / EPaxos**, Moraru 2012). Chapter 23's framing: these leaderless or rotating-leader protocols can outperform stable-leader designs over wide-area networks when clients are geographically spread and replicas live near them.

**Sources**: `raw/site-reliability-engineering/chapter-23-managing-critical-state-distributed-consensus-for-reliability.md`

**Last updated**: 2026-04-17

---

## The motivation

A stable-leader protocol like [[multi-paxos|Multi-Paxos]], Zab, or Raft has three well-known performance liabilities: all writes go via the leader, the leader's outgoing bandwidth is a bottleneck, and a slow leader machine slows the whole cluster (see [[stable-leader]]). Over a wide-area network with clients spread geographically, a fixed leader adds avoidable RTT for any client not near it.

The chapter's statement: "Over a wide area network with clients spread out geographically and replicas from the consensus group located reasonably near to the clients, such leader election leads to lower perceived latency for clients because their network RTT to the nearest replica will, on average, be smaller than that to an arbitrary leader" (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md).

## Mencius: rotating leadership by slot pre-assignment

Mencius [Mao08] uses a simple scheme: each numbered consensus round is **preassigned to a replica** — typically by a modulus of the transaction ID (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md). So round 1 goes to replica A, round 2 to replica B, round 3 to replica C, round 4 to replica A again, and so on.

Benefits:

- Every replica is a leader for some fraction of rounds, so clients can always send to the local replica for their round.
- The [[multi-paxos|dueling-proposers]] problem is eliminated structurally — there is no contention for "who gets to propose" because the schedule is deterministic.
- Load is spread evenly across replicas, so the [[stable-leader|leader's bandwidth and machine-performance bottlenecks]] don't apply.

Cost: if the replica assigned a round is slow, progress on that round stalls until it acts (or times out and another replica takes over). In practice, protocols include a liveness mechanism so a stuck replica's slot can be taken over.

## Egalitarian Paxos (EPaxos): leaderless

EPaxos [Mor12a] goes further: there is no per-slot leader at all. Every replica proposes independently, and the protocol uses a **conflict-detection** mechanism to determine ordering only when proposals actually conflict. Non-conflicting operations can commit with fewer messages and no central leader.

This is particularly good for workloads where conflicts are rare — the common case avoids the full Paxos message round. Under high conflict, EPaxos degrades toward classical costs.

## When to choose rotating or leaderless protocols

Chapter 23's framing (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md):

> Over a wide area network, leaderless protocols like Mencius or Egalitarian Paxos may have a performance edge, particularly if the consistency constraints of the application mean that it is possible to execute read-only operations on any system replica without performing a consensus operation.

The decision axes:

- **Client geography** — spread out → rotating/leaderless wins
- **Replica placement** — replicas near clients → rotating/leaderless wins
- **Conflict rate** — low → EPaxos wins; high → stable leader is probably fine
- **Workload mix** — read-heavy with local reads allowed → either works; the read path is the dominant latency concern

## Contrast with stable-leader protocols

| Axis | Stable leader | Mencius | EPaxos |
|---|---|---|---|
| Dominant message cost | 1 RTT to a quorum from the leader | 1 RTT from the local replica | 1 RTT from the local replica, if no conflict |
| Batching | Easy at the leader | Per-replica | Hard |
| Best case latency | Low near leader, high elsewhere | Low everywhere | Low everywhere with no conflicts |
| Complexity | Simple | Moderate | High |

## Cross-book framing

- [[paxos]] / [[multi-paxos]] — the stable-leader baseline Mencius and EPaxos are designed to improve on
- [[fast-paxos]] — a different direction: remove the leader hop by letting clients propose directly; often loses on tail latency
- [[consensus-performance]] — the design-space summary for all these protocols

## Related pages

- [[managing-critical-state]]
- [[consensus]]
- [[paxos]]
- [[multi-paxos]]
- [[stable-leader]]
- [[consensus-performance]]
- [[fast-paxos]]
