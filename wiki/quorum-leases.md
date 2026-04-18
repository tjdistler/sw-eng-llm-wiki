# Quorum Leases

**Summary**: A consensus performance optimisation (Moraru, Andersen, Kaminsky 2014) that grants a **read lease** on some subset of replicated state to a **quorum of replicas** for a brief period, enabling those replicas to serve strongly-consistent reads locally — at the cost of any state-changing operation now needing acknowledgement from all replicas in the read quorum during the lease. Particularly useful for read-heavy workloads where reads cluster in one geographic region.

**Sources**: `raw/site-reliability-engineering/chapter-23-managing-critical-state-distributed-consensus-for-reliability.md`

**Last updated**: 2026-04-17

---

## The problem it solves

Most consensus protocols require either a **distributed consensus operation** (read from a quorum of replicas) or a **stable leader replica** to serve a strongly-consistent read. In many systems, read operations vastly outnumber writes, so this reliance on either a distributed operation or a single replica harms both latency and throughput (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md).

[[stable-leader|Leader reads]] solve the latency problem for clients near the leader but not for clients elsewhere. [[consensus-read-optimisations|Read-only consensus operations]] work anywhere but pay the full consensus cost.

## How quorum leases work

Chapter 23's description (source: chapter-23-managing-critical-state-distributed-consensus-for-reliability.md):

> The quorum leasing technique simply grants a read lease on some subset of the replicated datastore's state to a quorum of replicas. The lease is for a specific (usually brief) period of time. Any operation that changes the state of that data must be acknowledged by all replicas in the read quorum. If any of these replicas becomes unavailable, the data cannot be modified until the lease expires.

The trade-off is explicit: faster reads at the lease-holding replicas, slower writes (because every write must wait for all lease-holding replicas), and a failure-mode penalty (lease-holding-replica failure freezes writes on that data until the lease expires).

## When they pay off

Quorum leases are particularly useful when:

- **Read-heavy workload** — the read win dominates the write cost.
- **Reads are concentrated in a geographic region** — leases can be granted to the replicas in that region, so local reads are strongly consistent without cross-region consensus.
- **The write rate on leased data is low** — so the all-replicas-acknowledge requirement does not dominate the write latency budget.

When reads are geographically spread or writes are frequent, quorum leases lose to a plain stable leader.

## Relationship to other read optimisations

[[consensus-read-optimisations]] lays out the four options for strongly-consistent reads:

1. Read-only consensus operation — works anywhere, full cost.
2. Leader read — single-replica up-to-date property; fast near the leader.
3. **Quorum lease** — this page; local strongly-consistent reads at a quorum of replicas.
4. Stale read from replica — not strongly consistent; when "stale data means extra work, not wrong answers" (Photon).

Quorum leases are option 3: the only strongly-consistent read path that tolerates geographic distance *and* keeps reads at replicas rather than forcing them to a leader.

## Relationship to [[renewable-leases]] and distributed locking

The lease mechanism is the same primitive Burns's ownership-election derivations use for distributed locking — a TTL plus renewal plus compare-and-swap. What differs is the semantic: here the lease grants *read authority*; in Burns's world it grants *write authority*. Both sit on the same consensus foundation.

## Related pages

- [[managing-critical-state]]
- [[consensus]]
- [[consensus-performance]]
- [[consensus-read-optimisations]]
- [[stable-leader]]
- [[reliable-replicated-datastore]]
- [[renewable-leases]]
- [[linearizability]]
