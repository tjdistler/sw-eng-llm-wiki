# Multi-Paxos

**Summary**: A performance-oriented variant of [[paxos|Paxos]] that elects a stable leader whose presence reduces the steady-state cost of consensus to a single round trip from proposer to a quorum of acceptors. The canonical shape for most production consensus systems, including [[chubby|Chubby]] and similar variants of Zab and Raft. The payoff is bounded by three well-known problems: dueling proposers on re-election, the leader's outgoing bandwidth as a bottleneck, and the leader's machine becoming a single performance point of failure.

**Sources**: `raw/site-reliability-engineering/chapter-23-managing-critical-state-distributed-consensus-for-reliability.md`

**Last updated**: 2026-04-17

---

## Why Multi-Paxos

Classic [[paxos|Paxos]] requires two phases (Prepare/Promise, Accept/Accepted) per value agreed. For a sequence of values that cost is wasteful. Multi-Paxos's insight: once a proposer has executed Phase 1 successfully, it has established a **numbered view** (also called a leader term), and for as long as that view remains stable, subsequent proposals can skip Phase 1 and go straight to Accept, reaching consensus in one round trip once a quorum of acceptors responds (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md).

This is the minimum message cost any consensus protocol can achieve in the common case and is typical of most consensus protocols in production.

## Message flow

Using a strong leader (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md):

1. **Initial state** — a new proposer executes Prepare/Promise (Phase 1), establishing a new view.
2. **Subsequent operations within the view** — the proposer sends Accept messages; consensus is reached once a quorum of responses (including the proposer itself) is received.
3. **View change** — another process in the group may assume the proposer role, but must execute Phase 1 again, incurring the extra round trip.

For the disk-write overlay of this flow see [[consensus-disk-access]]; the proposer writes before sending Accept and acceptors write before sending Accepted.

## Dueling proposers

When two processes simultaneously try to become the proposer, their Prepare phases interrupt each other repeatedly and no proposals can be accepted. This is a livelock: it can continue indefinitely (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md).

Practical systems avoid this by:

- **Electing a single proposer** explicitly (the classical Multi-Paxos pattern).
- **Using a rotating proposer** that assigns each process specific slots — the [[mencius-epaxos|Mencius]] approach.
- **Randomised backoffs** on leader election retries — the Raft approach, which Chapter 23 singles out as "a well-thought-out method of approaching the leader election process."

The trade-off with a leader-elected system: leader-election timeouts must be tuned carefully to balance **system unavailability when no leader is present** against **dueling-proposers risk during re-election**. Randomness is the best defence in either direction.

## The three performance costs of a stable leader

Chapter 23 lists three specific problems that come with the leader design (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md):

1. **Network latency for non-local clients.** All state-changing operations must go via the leader, which adds RTT for clients not near it.
2. **Outgoing bandwidth as a bottleneck.** The leader's Accept message contains all the proposal's data; replies contain only acknowledgements. Outgoing bandwidth at the leader's datacenter is the serialising resource. Chapter 23 cites this as a real operational concern for highly-sharded consensus systems.
3. **Leader-machine performance dominates the cluster.** If the leader's machine has problems, the throughput of the whole system is reduced.

## Read-only operation via the leader

A stable leader has the most up-to-date state, so read-only operations can be served directly by the leader to provide linearizable reads. This is a cheap performance win that [[quorum-leases|quorum leases]] later generalise to the quorum level for read-heavy workloads concentrated in a region. See [[consensus-read-optimisations]].

## Where it sits in the family

- [[paxos]] is the one-value-at-a-time base protocol.
- Multi-Paxos extends it to a sequence of values with a stable leader.
- Zab (ZooKeeper) and Raft are Multi-Paxos-shaped protocols with different details; Chapter 23 treats all three as instances of the same design pattern (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md).
- [[fast-paxos]] is the variant that *drops* the stable leader to save one message hop — sometimes faster, sometimes slower.
- [[mencius-epaxos|Mencius and EPaxos]] are leaderless/rotating-leader variants designed to remove the leader bottleneck.

## Related pages

- [[managing-critical-state]]
- [[consensus]]
- [[paxos]]
- [[fast-paxos]]
- [[stable-leader]]
- [[mencius-epaxos]]
- [[consensus-disk-access]]
- [[consensus-read-optimisations]]
- [[quorum-leases]]
- [[consensus-performance]]
