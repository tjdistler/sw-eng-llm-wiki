# Cron State Storage

**Summary**: Chapter 24's treatment of how the distributed cron service persists its Paxos log and periodic snapshots. Logs and snapshots live on **local disk** of each replica (three copies by default); **snapshots are additionally backed up to a distributed filesystem** because losing all three copies of the snapshot is unrecoverable, while losing recent log entries just rewinds the service to the last snapshot. Logs are intentionally **not** stored on the distributed filesystem — the small-write latency penalty isn't worth it given that simultaneous loss of all three replicas' local disk is unlikely.

**Sources**: `raw/site-reliability-engineering/chapter-24-distributed-periodic-scheduling-with-cron.md`

**Last updated**: 2026-04-17

---

## The two storage problems

Paxos is fundamentally a **log of state changes** appended synchronously. That has two practical consequences (source: chapter-24-distributed-periodic-scheduling-with-cron.md):

1. **The log grows without bound.** It must be compacted so the system doesn't eventually run out of disk and so new replicas don't have to replay years of history on startup.
2. **The log itself must live somewhere.** Writing it somewhere durable and fast enough is the engineering problem.

## Compaction via snapshots

The standard technique: periodically take a **snapshot** of the current state. The snapshot subsumes all log entries up to the snapshot point, so those entries can be discarded (source: chapter-24-distributed-periodic-scheduling-with-cron.md). Chapter 24's illustration: if the log contains a thousand "increment counter by 1" records, a single snapshot "counter = 1000" replaces them all.

After a snapshot:

- The log is truncated to cover just the interval since the snapshot.
- Losing the log loses only state changes since the last snapshot.
- Losing the snapshot, however, means reconstructing state from zero (or from an even older snapshot if the system keeps a chain).

So **snapshots are the most critical state** in the cron service — much more so than the per-operation log entries that feed them.

## The three-tier storage layout

Chapter 24's actual mechanism (source: chapter-24-distributed-periodic-scheduling-with-cron.md):

1. **Paxos logs on local disk** of each replica. With three replicas (the default) there are three copies.
2. **Snapshots on local disk** of each replica. Same three-copy redundancy.
3. **Snapshot backups on a distributed filesystem** ([[colossus|Colossus]]). One more copy, survives simultaneous local-disk loss.

Notably, logs are **not** backed up to the distributed filesystem. This is a deliberate trade-off.

## Why logs don't go to DFS

Two reasons Chapter 24 states explicitly (source: chapter-24-distributed-periodic-scheduling-with-cron.md):

1. **Storing logs on a distributed filesystem can entail a substantial performance penalty caused by frequent small writes.** Distributed filesystems like GFS / [[colossus|Colossus]] are optimised for large sequential writes; a Paxos log's small synchronous appends hit their worst case.
2. **Simultaneous loss of all three replicas is unlikely.** If it does occur, the system automatically restores from the most recent snapshot and loses only the logs since that snapshot — a bounded loss in time, not in principle.

The trade-off Chapter 24 makes: a small risk of bounded state loss in exchange for substantially better steady-state latency.

## Why snapshots do go to DFS

Symmetrically, Chapter 24 is pointed that snapshots must survive the all-three-replicas-gone case (source: chapter-24-distributed-periodic-scheduling-with-cron.md):

> Snapshots are in fact our most critical state — if we lose our snapshots, we essentially have to start from zero again because we've lost our internal state. Losing logs, on the other hand, just causes a bounded loss of state and sends the cron system back in time to the point when the latest snapshot was taken.

Snapshots are infrequent and large — the write pattern suits DFS. The cost of storing them there is acceptable even if the per-write latency is worse than local disk.

## Replica startup and state transfer

Chapter 24 notes an additional benefit of the separate-snapshot-backup layout: **a freshly-started replica can fetch the state snapshot and all logs from an already running replica over the network** (source: chapter-24-distributed-periodic-scheduling-with-cron.md). This makes replica startup independent of local-disk state — a replica rescheduled to a different machine by [[borg|Borg]] doesn't need any existing data to come online.

The consequence for operations: rescheduling a cron replica because its machine died or needs updates is effectively a non-event for the reliability of the service. Local-disk state is a performance optimisation, not a correctness requirement.

## Why in-service state rather than external

Chapter 24 also justifies the higher-level choice — why the cron service keeps its own state rather than delegating to an external store (source: chapter-24-distributed-periodic-scheduling-with-cron.md):

- **Distributed filesystems cater to large files**, and the cron state is small — small writes there are expensive and high-latency.
- **Base services with wide blast radius should have few dependencies.** If parts of the datacenter degrade, cron should still function. Delegating state to an external service couples cron's uptime to that service's uptime.

This is the same dependency-minimisation argument [[managing-critical-state]] makes for consensus systems generally. Cron is a control-plane service; its dependencies should be minimal.

## Comparison to a reliable replicated datastore

Structurally, the cron service *is* a [[reliable-replicated-datastore]] specialised for scheduling state. The Paxos-plus-snapshots-plus-local-log layout is the generic shape of any Paxos-backed service. What makes cron's treatment interesting is the explicit honesty about what can be lost — logs can be lost; snapshots cannot — and the engineering choices that follow.

## The snapshot-interval trade-off

Chapter 24 mentions that snapshots are taken on "configurable intervals" (source: chapter-24-distributed-periodic-scheduling-with-cron.md). Implicit trade-offs:

- **Frequent snapshots** → short log tails → less state lost if all three replicas fail simultaneously, but more DFS write cost.
- **Infrequent snapshots** → long log tails → more potential state loss but cheaper steady state.

The right interval is workload-dependent. Small scheduler state and cheap snapshot writes mean this is not a hard operational decision for cron.

## Related pages

- [[distributed-cron]]
- [[cron-leader-follower]]
- [[cron-partial-failure-resolution]]
- [[paxos]]
- [[consensus-disk-access]]
- [[reliable-replicated-datastore]]
- [[replicated-state-machine]]
- [[colossus]]
