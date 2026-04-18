# Paxos

**Summary**: Leslie Lamport's 1998 protocol for asynchronous distributed [[consensus]] — a sequence of numbered **proposals** voted on by a quorum of **acceptors**, where the strict sequence numbering plus majority-quorum overlap together guarantee safety. Paxos on its own only lets you agree on a single value once; practical systems layer [[multi-paxos|Multi-Paxos]], a [[replicated-state-machine]], and a [[stable-leader]] on top.

**Sources**: `raw/site-reliability-engineering/chapter-23-managing-critical-state-distributed-consensus-for-reliability.md`, `raw/site-reliability-engineering/chapter-24-distributed-periodic-scheduling-with-cron.md`, `raw/designing-data-intensive-applications/chapter-09-consistency-and-consensus.md`

**Last updated**: 2026-04-17

---

## The protocol at a glance

Paxos operates as a sequence of proposals. Each proposal carries a **sequence number** that imposes a strict ordering on all operations. In the first phase, a **proposer** sends a sequence number to the **acceptors**; each acceptor agrees to accept only if it hasn't seen a higher sequence number. In the second phase, if a majority agreed, the proposer sends a commit message with a value (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md).

Proposers must use unique sequence numbers — drawing from disjoint sets, or incorporating their hostname into the number, for example.

## Why it's safe

Two rules do the load-bearing work (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md):

1. **Strict sequence numbering** solves any problems relating to the ordering of messages in the system.
2. **Majority-quorum overlap** guarantees that two different values cannot be committed for the same proposal: *any two majorities overlap in at least one node*, and that overlapping node's promise prevents the second majority from committing a conflicting value.

Acceptors must **journal** every promise to persistent storage before acknowledging it, because they need to honour these guarantees after restarting. This disk write is one of the two physical bottlenecks of any Paxos system; see [[consensus-disk-access]].

## What Paxos does not give you

"Paxos on its own isn't that useful: all it lets you do is to agree on a value and proposal number once" (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md). Two limitations follow:

- **Only a quorum needs to agree**, so any individual node may not have a complete view of the set of values that have been agreed. This is a property of most distributed consensus algorithms and drives the need for state synchronisation between peers — see [[replicated-state-machine]].
- **Agreement is on one value at a time**, so practical systems use [[multi-paxos|Multi-Paxos]] or sequence of Paxos instances to agree on a sequence of values (i.e. [[total-order-broadcast]]).

## Variants

Paxos has many variations aimed at performance. Most vary in a single detail — for example, giving one process a special **leader** role to streamline the protocol (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md):

- [[multi-paxos]] — a stable leader lets subsequent operations skip Phase 1, reducing to one round trip.
- [[fast-paxos]] — clients send proposals directly to acceptors; faster on some topologies, slower on others.
- **Raft** — alternative protocol with a well-thought-out leader election process and an explicit log-consistency mechanism.
- **Zab** — ZooKeeper's protocol.
- **Mencius** — rotating leadership; see [[mencius-epaxos]].
- **Egalitarian Paxos** — leaderless; see [[mencius-epaxos]].

## The dueling proposers problem

If multiple processes try to propose at the same time with Paxos's first phase running repeatedly, they can interrupt each other indefinitely — a **livelock** (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md). Real systems address this by:

- **Electing a single proposer** that serialises all proposals (the [[multi-paxos]] approach).
- **Rotating the proposer** — each process owns specific slots (the [[mencius-epaxos|Mencius]] approach).
- **Randomised backoffs** on leader election retries to avoid synchronous re-election (the Raft approach).

See [[multi-paxos]] for Chapter 23's detailed walkthrough of the dueling-proposers figure and its mitigations.

## Cross-book framing

- [[consensus]] — Kleppmann's DDIA Chapter 9 coverage of Paxos-family algorithms is the theoretical companion; Chapter 23 is the operational one. Both converge on the same points: epoch numbering, quorum overlap, and [[safety-and-liveness|safety over liveness]] as the governing trade-off.
- [[chubby]] — Google's lock service, which uses Paxos as its consensus engine.
- [[zookeeper]] — uses Zab, a Paxos-family protocol; etcd uses Raft.
- [[total-order-broadcast]] — a sequence of Paxos rounds implements total order broadcast.

## Applied example: Google's distributed cron

Chapter 24 describes a small but production-critical Paxos deployment: Google's [[distributed-cron|distributed cron service]] uses Paxos (specifically [[fast-paxos|Fast Paxos]]) across a three-replica set to keep the "which scheduled launches have fired" state consistent (source: chapter-24-distributed-periodic-scheduling-with-cron.md). The service is a narrow example of the general Paxos machinery:

- The **leader** (Fast Paxos's internally-elected leader, reused as the cron-service leader) is the only replica that launches jobs.
- Every launch is bracketed by two **synchronous** Paxos log entries: an "about to launch" record and a "launch completed" record. This is what lets a new leader on failover resolve in-flight launches unambiguously.
- **Logs** live on local disk; **snapshots** live on local disk and on a distributed filesystem. Losing logs rewinds to the last snapshot; losing snapshots is unrecoverable, so the backup asymmetry follows naturally. See [[cron-state-storage]].

The interesting wrinkle is that Paxos alone isn't enough — the cron service additionally requires **mutual exclusion** on its downstream dependency ([[borg|Borg]]), because a stale ex-leader could otherwise still issue launch RPCs. See [[cron-leader-follower]] for the mutual-exclusion story and [[cron-partial-failure-resolution]] for the precomputed-name technique that makes it practical.

## Related pages

- [[managing-critical-state]]
- [[consensus]]
- [[multi-paxos]]
- [[fast-paxos]]
- [[mencius-epaxos]]
- [[stable-leader]]
- [[replicated-state-machine]]
- [[flp-impossibility]]
- [[safety-and-liveness]]
- [[total-order-broadcast]]
- [[consensus-disk-access]]
- [[chubby]]
- [[zookeeper]]
- [[distributed-cron]]
