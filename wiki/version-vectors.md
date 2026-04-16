# Version Vectors

**Summary**: A data structure that tracks, per-replica, which writes have been seen — enabling a distributed system to distinguish between an overwrite (one write supersedes another) and a conflict (two writes are concurrent and must be merged).

**Sources**: `raw/designing-data-intensive-applications/chapter-05-replication.md`, `raw/designing-data-intensive-applications/chapter-09-consistency-and-consensus.md`

**Last updated**: 2026-04-15

---

## The happens-before relationship

Two operations can be in one of three states:
- **A happened before B**: B knows about A, depends on A, or builds upon A.
- **B happened before A**: the reverse.
- **A and B are concurrent**: neither knew about the other when it was performed.

Concurrency is not about *physical time* — two events are concurrent if they were both *unaware of each other*, regardless of when they actually occurred. Network delays mean that even events well-separated in time can be concurrent if communication was interrupted.

This insight is fundamental: causality, not clocks, defines concurrency in distributed systems.

## Single-replica version numbers

On a single replica, version numbers are sufficient to track the happens-before relationship. The algorithm:

1. The server keeps a version number per key, incrementing it on every write.
2. On a read, the server returns all un-overwritten values and the current version number.
3. On a write, the client includes the version number from its most recent read, plus a merged value that incorporates everything it received in that read.
4. The server overwrites values at or below the sent version number (they've been merged) and keeps values at higher version numbers (they are concurrent siblings).

A write sent without a version number is concurrent with all existing values and becomes a sibling.

## Multiple replicas: version vectors

With multiple replicas all accepting writes, a single version number per key is insufficient — it doesn't say *which replica* has seen which writes. The solution: a **version number per replica per key**.

Each replica increments its *own* version number when it processes a write, and tracks the version numbers it has seen from each other replica. The collection of these per-replica version numbers is the **version vector** (sometimes called *vector clock*, though they are slightly different — version vectors are the correct structure for comparing replica state).

Version vectors are sent to clients when values are read and must be sent back when values are written. This allows the database to determine, when it receives a write, which existing values are superseded and which are concurrent siblings.

## Siblings and merging

When two concurrent writes produce siblings (divergent values), the client or application must merge them. Strategies:

- **For sets**: take the union. Use **tombstones** to record deletions, so that a deleted item isn't resurrected when merging with a version that kept it.
- **CRDTs**: data structures designed to merge automatically without data loss (see [[write-conflicts]]).
- **Last write wins**: pick one based on timestamp; simple but lossy.

Riak calls concurrent values *siblings* and uses dotted version vectors (Riak 2.0) to encode causal context.

## Version vectors vs vector clocks

Version vectors are sometimes called vector clocks, but they are not quite the same. The difference is subtle and relates to what the numbers are tracking (state vs. events). For the purpose of comparing replica state and determining what to merge, version vectors are the right data structure.

## Version vectors vs Lamport timestamps

Chapter 9 draws an important distinction between version vectors and [[lamport-timestamps]] (source: designing-data-intensive-applications, chapter 9):

| Property | Version vectors | [[lamport-timestamps]] |
|---|---|---|
| Order type | Partial order | Total order |
| Can detect concurrency | Yes -- incomparable vectors mean concurrent operations | No -- every pair is ordered, concurrent operations are indistinguishable |
| Size | One counter per replica (grows with replicas) | Compact: one counter + node ID |
| Purpose | Detect concurrent writes to merge or resolve conflicts | Provide a causal total ordering for sequencing operations |

Version vectors are the right tool when you need to know whether two writes conflict (concurrent) or whether one supersedes the other. Lamport timestamps are the right tool when you need a total ordering consistent with causality but do not need to identify concurrency.

Version vectors can be generalized beyond single-key conflict detection to track [[causal-consistency]] across the entire database. The database must know which version of data was read by each operation, so that it can determine causal ordering. (source: designing-data-intensive-applications, chapter 9)

## Related pages

- [[leaderless-replication]]
- [[write-conflicts]]
- [[multi-leader-replication]]
- [[consistent-prefix-reads]]
- [[replication]]
- [[lamport-timestamps]]
- [[causal-consistency]]
