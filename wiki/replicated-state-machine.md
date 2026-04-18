# Replicated State Machine

**Summary**: A system that executes the same set of operations, in the same order, on several processes — the fundamental building block of every practical distributed-consensus-based service. An RSM sits *above* the [[consensus]] algorithm: consensus agrees on the sequence of operations; the RSM executes them. Any deterministic program can be implemented as a highly available replicated service by being implemented as an RSM.

**Sources**: `raw/site-reliability-engineering/chapter-23-managing-critical-state-distributed-consensus-for-reliability.md`

**Last updated**: 2026-04-17

---

## What an RSM is

Chapter 23's definition: "A replicated state machine (RSM) is a system that executes the same set of operations, in the same order, on several processes. RSMs are the fundamental building block of useful distributed systems components and services such as data or configuration storage, locking, and leader election" (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md).

The key theoretical result: several papers ([Agu10], [Kir08], [Sch90] in Chapter 23's bibliography) show that any deterministic program can be implemented as a highly available replicated service by being implemented as an RSM.

## The two-layer model

The architectural diagram Chapter 23 uses has the RSM as a **logical layer above the consensus algorithm** (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md):

| Layer | Responsibility |
|---|---|
| RSM | Execute operations in the agreed order; produce application state |
| Consensus algorithm | Agree on the sequence of operations |

This separation matters operationally because it means the consensus primitive is small, stable, and formally verifiable, while the RSM layer can hold arbitrary application logic as long as it is deterministic. [[zookeeper|ZooKeeper]], [[chubby|Chubby]], etcd, and Consul are all packaged RSMs — they expose a higher-level API (locks, watches, filesystem-like trees) whose implementation is an RSM on top of [[paxos|Paxos]], Zab, or Raft.

## State synchronisation between peers

Because not every member of the consensus group is necessarily a member of each consensus quorum, RSMs may need to **synchronise state from peers** after rejoining or recovering. Chapter 23 points at Kirsch and Amir's **sliding-window protocol** for reconciling state between peer processes in an RSM (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md).

The need for peer synchronisation is a direct consequence of the fact that [[paxos|Paxos]] only requires a *quorum* to agree on each value — so any given replica may have missed some decisions. See [[consensus-replica-count]] for how this interacts with the replica-count-and-recovery discussion.

## Where RSMs show up

Chapter 23 catalogues five RSM-based patterns. Each is an instance of this same machinery exposed through a different higher-level interface:

- [[reliable-replicated-datastore]] — a keyvalue or configuration store; consensus on each write
- **Highly-available processing via leader election** — one replica is elected to act; consensus is not in the critical path of its work, just of the election
- [[distributed-barrier]] — a primitive blocking a group of processes until a condition is met; see the MapReduce phase-boundary use case
- **Distributed locks** — renewable leases with timeouts; RSM entries represent lock grants
- [[reliable-distributed-queue]] — messages are ordered via consensus; atomic broadcast is equivalent to consensus per Chandra-Toueg — see [[atomic-broadcast]]

## Relationship to state-machine replication as a general principle

The broader principle — if every replica processes the same sequence of deterministic operations in the same order, they remain consistent — is catalogued on [[state-machine-replication]] (drawn from Kleppmann's DDIA treatment). This page is the Chapter-23-specific applied framing: the RSM as a *system*, as the deliberate architectural layer above consensus, with the sliding-window peer-sync detail.

## Related pages

- [[managing-critical-state]]
- [[consensus]]
- [[state-machine-replication]]
- [[paxos]]
- [[multi-paxos]]
- [[total-order-broadcast]]
- [[reliable-replicated-datastore]]
- [[distributed-barrier]]
- [[atomic-broadcast]]
- [[reliable-distributed-queue]]
- [[zookeeper]]
- [[chubby]]
