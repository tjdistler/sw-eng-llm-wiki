# Replication

**Summary**: Keeping a copy of the same data on multiple machines, connected via a network. The simple goal — same data everywhere — turns out to be extraordinarily difficult in the presence of change.

**Sources**: `raw/designing-data-intensive-applications/chapter-05-replication.md`, `raw/designing-data-intensive-applications/chapter-11-stream-processing.md`, `raw/site-reliability-engineering/chapter-26-data-integrity-what-you-read-is-what-you-wrote.md`

**Last updated**: 2026-04-17

---

## Why replicate?

Three motivations drive replication:

- **Latency** — place data geographically close to users
- **Availability** — keep the system running if some parts fail
- **Read throughput** — distribute read load across multiple machines

If data never changed, replication would be trivial: copy once, done. All the difficulty lies in *handling changes* to replicated data.

## Three architectures

Almost all distributed databases use one of three replication approaches:

| Architecture | Who accepts writes | Conflict risk |
|---|---|---|
| [[leader-based-replication]] | One leader node | None (single writer) |
| [[multi-leader-replication]] | Any of several leaders | Yes — must be resolved |
| [[leaderless-replication]] | Any replica (Dynamo-style) | Yes — must be resolved |

Each has its own tradeoff profile around availability, consistency, and operational complexity.

## The fundamental tension

Every replication system must choose between **synchronous** and **asynchronous** replication:

- **Synchronous**: the leader waits for the follower to confirm before reporting success. Guarantees the follower is up-to-date; blocks writes if the follower is slow or down.
- **Asynchronous**: the leader sends the change and moves on. Writes are not blocked; followers may lag.

In practice, fully synchronous setups are impractical — any single node outage halts all writes. Most systems use asynchronous replication, which introduces [[replication-lag]] and its associated consistency anomalies.

## Consistency guarantees layered on top of replication

When using asynchronous followers, applications must decide which guarantees they need:

- [[read-after-write-consistency]] — users see their own writes
- [[monotonic-reads]] — reads don't appear to go backward in time
- [[consistent-prefix-reads]] — causally related writes appear in order
- [[eventual-consistency]] — the weakest guarantee: replicas will converge, eventually

Stronger guarantees ([[linearizability]], [[serializability]]) require transactions or [[consensus]] protocols, not just replication. Chapter 9 explores how different replication architectures relate to linearizability: single-leader is potentially linearizable, multi-leader is not, and leaderless is probably not. (source: designing-data-intensive-applications, chapter 9)

## Concurrency and conflicts

Multi-leader and leaderless systems introduce [[write-conflicts]] because multiple nodes accept writes simultaneously. Resolving conflicts requires understanding causality — whether two writes *knew about each other* at the time they were made. [[version-vectors]] are the tool for tracking this.

## Relationship to partitioning

[[partitioning|Partitioning]] is almost always combined with replication so that copies of each partition are stored on multiple nodes for fault tolerance. A node may store more than one partition and may be the leader for some partitions and a follower for others. The choice of partitioning scheme is mostly independent of the replication scheme (source: chapter-06-partitioning.md).

## Replication logs as event streams

A replication log is fundamentally a stream of database write events. The leader produces this stream as it processes transactions; followers consume it and apply the same writes to stay in sync. This is an instance of the [[state-machine-replication]] principle: same events, same order, same final state (source: chapter-11-stream-processing.md).

This insight connects databases to [[stream-processing]] in a deep way:

- **[[change-data-capture]]** (CDC) extracts the replication log and makes it available as a stream for consumption by heterogeneous derived systems (search indexes, caches, data warehouses). The source database becomes the leader; derived systems become followers.
- **[[log-based-message-brokers]]** (Kafka, Kinesis) use the same append-only log structure as replication logs but generalize it for arbitrary event streams. Consumer offsets in Kafka are directly analogous to log sequence numbers in database replication -- both track a follower's position in the leader's log (source: chapter-11-stream-processing.md).
- **[[event-sourcing]]** applies the same idea at the application level: store all state changes as an immutable event log, and derive current state by replaying the log.

## Replication is not recoverability (SRE Ch 26)

A classic but flawed response to "do you have a backup?" is "we have something even better than a backup — replication!" SRE Chapter 26 rejects this directly (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md):

> Replication provides many benefits, including locality of data and protection from a site-specific disaster, but it can't protect you from many sources of data loss. Datastores that automatically sync multiple replicas guarantee that a corrupt database row or errant delete are pushed to all of your copies, likely before you can isolate the problem.

Replication protects against the failure modes replication was designed for — machine loss, rack loss, datacenter loss. It **does not** protect against:

- **User or admin error** — an errant `DELETE` propagates to every replica, usually within seconds.
- **Application bugs** — a deletion pipeline with a race condition (see [[google-music-runaway-deletion]]) corrupts every replica simultaneously.
- **Zero-day vulnerabilities in low-level components** — a bug in the filesystem or device driver affects every disk-backed replica at the same time.

Chapter 26's prescription: keep **non-serving copies on diverse components** — different media (disk and tape), different stack layers, different storage technologies. This is exactly the [[tiered-backup-strategy|multi-tier backup]] architecture. Replication is useful *within* each tier but cannot substitute *for* any tier. See [[defense-in-depth-data]] and [[data-integrity-sre]] for the broader framing.

The 2011 [[gmail-gtape-restore|Gmail incident]] is the canonical worked example: Gmail's internal replication and online backups both failed; only the offsite tape layer (media diverse from disks) still worked.

## Replication in distributed filesystems

[[distributed-filesystems|HDFS]] replicates file blocks across multiple machines for fault tolerance, using the same core idea as database replication but applied to immutable file blocks rather than mutable records. Two approaches are used: full replication (multiple identical copies) and erasure coding (e.g., Reed-Solomon codes) which allows recovery with lower storage overhead. The techniques are similar to RAID but operate across machines over a conventional datacenter network (source: designing-data-intensive-applications, chapter 10).

## Related pages

- [[leader-based-replication]]
- [[multi-leader-replication]]
- [[leaderless-replication]]
- [[replication-lag]]
- [[write-conflicts]]
- [[quorums]]
- [[eventual-consistency]]
- [[fault-tolerance]]
- [[scalability]]
- [[partitioning]]
- [[distributed-filesystems]]
- [[linearizability]]
- [[consensus]]
- [[cap-theorem]]
- [[total-order-broadcast]]
- [[change-data-capture]]
- [[event-sourcing]]
- [[log-based-message-brokers]]
- [[stream-processing]]
- [[data-integrity-sre]]
- [[defense-in-depth-data]]
- [[tiered-backup-strategy]]
- [[gmail-gtape-restore]]
- [[google-music-runaway-deletion]]
