# Quorums

**Summary**: A mechanism in [[leaderless-replication]] that uses overlapping sets of replicas for reads and writes to ensure at least one node in each read has the latest write — providing probabilistic recency guarantees, but not strong consistency.

**Sources**: `raw/designing-data-intensive-applications/chapter-05-replication.md`, `raw/designing-data-intensive-applications/chapter-08-the-trouble-with-distributed-systems.md`

**Last updated**: 2026-04-15

---

## The quorum condition

Given n replicas:
- A write must be acknowledged by at least **w** nodes to be considered successful.
- A read must query at least **r** nodes.

When **w + r > n**, the write set and read set must overlap in at least one node — so at least one node in any read must have the latest write. This is the quorum condition.

Typical configuration: **n = 3, w = 2, r = 2**. Tolerates one unavailable node for both reads and writes.

**Tuning for workload**:
- Read-heavy: set r = 1, w = n. Reads are fast; a single unavailable node blocks writes.
- Write-heavy: set r = n, w = 1. Writes are fast; a single unavailable node blocks reads.
- Smaller w and r (violating w + r > n): lower latency and higher availability, at the cost of more frequent stale reads.

## Fault tolerance

With n = 3, w = 2, r = 2: tolerate 1 unavailable node.
With n = 5, w = 3, r = 3: tolerate 2 unavailable nodes.

In general: the system can tolerate up to `n - w` unavailable nodes for writes, and `n - r` for reads. Normally reads and writes are sent to all n replicas in parallel; w and r determine how many acknowledgments are required before the operation is considered done.

## Sloppy quorums

A **sloppy quorum** accepts writes on nodes that are not in the usual home set for a key, when those home nodes are unreachable. This improves availability but sacrifices the overlap guarantee — the nodes serving a read may not include the node that holds the sloppy-quorum write. See [[leaderless-replication]] for details on hinted handoff.

## Limitations: quorums are not as safe as they appear

Even with w + r > n, the following edge cases can return stale data:

- **Sloppy quorums**: the w writes may be on different nodes than the r reads — no overlap guaranteed.
- **Concurrent writes**: if two writes race, and the winner is chosen by LWW (last write wins), clock skew can cause the wrong write to win. Data is silently lost.
- **Write during read**: a write that reaches only some replicas before a read may or may not be seen by the read.
- **Partial write failure**: if a write succeeds on some replicas but fails on others (reaching fewer than w), it is not rolled back on the successful replicas. Subsequent reads may return that partially-written value.
- **Failed node restored from stale backup**: if a node carrying a new value fails and is restored from an old replica, the count of up-to-date replicas can fall below w.

The conclusion: **Dynamo-style databases are optimized for use cases that can tolerate [[eventual-consistency]]**. The w and r parameters tune the *probability* of stale reads, not a binary guarantee. Stronger guarantees require transactions or consensus.

## Monitoring staleness

In leader-based systems, replication lag is measurable by comparing follower and leader log positions. In leaderless systems, there is no fixed write order, so lag is harder to quantify. Without anti-entropy, a rarely-read stale value may be arbitrarily old. Formalising staleness metrics for quorum systems is an active research area; historically not standard, though cloud vendors have since made replication-lag observability routine for their managed offerings.

## Quorums and linearizability

Intuitively, strict quorums (w + r > n) seem like they should provide [[linearizability]]. However, Chapter 9 demonstrates that this is not the case: with variable network delays, race conditions are possible where one client reads the new value while a concurrent client (starting its read later) still sees the old value. (source: designing-data-intensive-applications, chapter 9)

It is possible to make Dynamo-style quorums linearizable, but at significant cost:
- Readers must perform **synchronous read repair** before returning results.
- Writers must read the latest quorum state before sending writes.
- Even then, only linearizable reads and writes are possible -- a linearizable **compare-and-set** operation requires a full [[consensus]] algorithm. (source: designing-data-intensive-applications, chapter 9)

In practice: Riak does not perform synchronous read repair (performance penalty). Cassandra waits for read repair on quorum reads but loses linearizability with concurrent writes due to last-write-wins. **It is safest to assume leaderless systems with Dynamo-style replication do not provide linearizability.** (source: designing-data-intensive-applications, chapter 9)

## Quorums for decision-making (beyond read/write)

Chapter 8 introduces a broader use of quorums: **decision-making in distributed systems**. A node cannot trust its own judgment about the state of the system (it may be experiencing a [[process-pauses|process pause]] or [[network-faults|network fault]] without knowing it). Instead, many distributed algorithms rely on quorum voting to make decisions, including declaring nodes dead. (source: designing-data-intensive-applications, chapter 8)

If a quorum of nodes declares another node dead, it must be considered dead, even if that node still feels alive. The individual node must abide by the quorum decision and step down. Most commonly, the quorum is an **absolute majority** (more than half the nodes). A majority quorum allows the system to continue working if individual nodes fail, and it is safe because there can only be one majority -- two conflicting majorities cannot exist simultaneously. (source: designing-data-intensive-applications, chapter 8)

This principle applies to leadership, locking, and uniqueness guarantees. See [[truth-and-leadership-in-distributed-systems]] for the detailed discussion.

## Quorums in consensus algorithms

[[consensus|Consensus]] algorithms also rely on quorums, but differently: they require a majority vote for both leader election and proposal acceptance, and the two quorums must overlap. Unlike read/write quorums in leaderless systems, consensus quorums provide genuine safety guarantees because they are combined with epoch numbering and recovery protocols. (source: designing-data-intensive-applications, chapter 9)

## Related pages

- [[leaderless-replication]]
- [[replication]]
- [[write-conflicts]]
- [[eventual-consistency]]
- [[version-vectors]]
- [[linearizability]]
- [[consensus]]
- [[truth-and-leadership-in-distributed-systems]]
- [[fencing-tokens]]
