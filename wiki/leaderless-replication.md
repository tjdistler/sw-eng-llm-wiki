# Leaderless Replication

**Summary**: A replication architecture where any replica can directly accept writes from clients, with no designated leader and no failover — popularized by Amazon's internal Dynamo system and used in Riak, Cassandra, and Voldemort.

**Sources**: `raw/designing-data-intensive-applications/chapter-05-replication.md`, `raw/designing-data-intensive-applications/chapter-09-consistency-and-consensus.md`

**Last updated**: 2026-04-15

---

## How it works

The client (or a coordinator node on its behalf) sends writes to *all* n replicas in parallel. The write is considered successful once w replicas acknowledge it. Reads are similarly sent to r replicas in parallel; the client uses version numbers to pick the most recent value.

Unlike [[leader-based-replication]], there is no failover: if a node is down, the client simply ignores that node's absence and writes to the remaining nodes. When the node comes back, it may have missed writes and will serve stale data — which is corrected through repair mechanisms.

This architecture was used in some of the earliest distributed systems, fell out of fashion during the relational database era, and was revived by Amazon Dynamo. Open-source implementations include Riak, Cassandra, and Voldemort ("Dynamo-style" databases).

## Repair mechanisms

Two mechanisms ensure that nodes eventually catch up after being unavailable:

**Read repair**: when a client reads from multiple replicas in parallel and detects a stale value on one, it writes the newer value back to the stale replica. Works well for frequently-read values; values that are rarely read may stay stale for a long time.

**Anti-entropy**: a background process continuously compares data between replicas and copies missing data from one to another. Unlike leader-based replication logs, anti-entropy does not copy writes in any particular order and may introduce significant delay. Not all systems implement it (Voldemort, notably, does not).

Without anti-entropy, rarely-read values may be durably missing from some replicas.

## Quorum reads and writes

With n replicas, w write acknowledgments required, and r replicas queried per read:

- As long as **w + r > n**, at least one of the r nodes you read from must have the latest write (the write set and read set must overlap).
- Common configuration: n = 3, w = 2, r = 2 (tolerates one unavailable node).
- Read-heavy workloads: set w = n, r = 1. Writes fail if any node is down; reads are always fresh and fast.

See [[quorums]] for detail on the math and the many edge cases where quorums fail to provide the expected guarantees.

## Sloppy quorums and hinted handoff

When a network interruption cuts a client off from the n designated home nodes for a key, the client faces a choice: return an error, or write to *any* w available nodes — even if they are not in the normal home set. Writing to non-home nodes is called a **sloppy quorum**.

The nodes that temporarily accept writes on behalf of the home nodes later forward those writes to the home nodes during **hinted handoff** — once the network is restored.

Sloppy quorums improve write availability: as long as *any* w nodes are reachable, writes succeed. But they break the quorum overlap guarantee: the r nodes you read from may not include the node that has the most recent sloppy-quorum write. A sloppy quorum is thus not a true quorum — it is a durability guarantee (the data is *somewhere*), not a recency guarantee.

Sloppy quorums are enabled by default in Riak, disabled by default in Cassandra and Voldemort.

## Concurrent writes

Dynamo-style databases allow multiple clients to write to the same key concurrently, even with strict quorums. Conflicts arise, and must be resolved — the same problem as [[write-conflicts]] in multi-leader systems. [[version-vectors]] are the mechanism for detecting whether two writes are concurrent or whether one supersedes the other.

## Multi-datacenter leaderless

Cassandra and Voldemort extend the leaderless model across datacenters: n includes replicas in all datacenters, and writes are sent to all replicas regardless of datacenter, but the client only waits for a quorum from its local datacenter. Cross-datacenter replication happens asynchronously.

Riak takes a different approach: n is scoped to one datacenter, and cross-datacenter replication uses an asynchronous process similar to [[multi-leader-replication]].

## Linearizability: probably not

Despite claims that quorum reads and writes (w + r > n) provide "strong consistency," leaderless replication is **probably not linearizable**. Chapter 9 demonstrates that variable network delays allow race conditions even with strict quorums: one client can read the new value while another (starting later) still sees the old value. (source: designing-data-intensive-applications, chapter 9)

Specific problems:
- **Last-write-wins** conflict resolution using timestamps (e.g., Cassandra) is almost certainly nonlinearizable due to clock skew.
- **Sloppy quorums** destroy any chance of linearizability.
- Even with strict quorums, synchronous read repair (before returning results) and writer-side quorum reads would be needed -- and compare-and-set still requires [[consensus]].

It is safest to assume leaderless systems do not provide [[linearizability]]. See [[quorums]] for the detailed analysis. Leaderless and multi-leader systems typically operate without global [[consensus]], and the conflicts that result are a consequence of this design choice. (source: designing-data-intensive-applications, chapter 9)

## Related pages

- [[replication]]
- [[quorums]]
- [[write-conflicts]]
- [[version-vectors]]
- [[multi-leader-replication]]
- [[eventual-consistency]]
- [[fault-tolerance]]
- [[linearizability]]
- [[consensus]]
