# Failover

**Summary**: The process of promoting a follower to leader when the current leader fails — conceptually simple, but rife with edge cases that can corrupt data or leave the system in an inconsistent state.

**Sources**: `raw/designing-data-intensive-applications/chapter-05-replication.md`, `raw/designing-data-intensive-applications/chapter-08-the-trouble-with-distributed-systems.md`, `raw/designing-data-intensive-applications/chapter-09-consistency-and-consensus.md`, `raw/designing-distributed-systems/chapter-09-ownership-election.md`

**Last updated**: 2026-04-16

---

## What failover involves

When a leader fails in [[leader-based-replication]], three things must happen:

1. **Detect the failure** — most systems use a timeout (e.g., 30 seconds without a response). There is no reliable way to distinguish a dead leader from a slow one or a network partition.
2. **Choose a new leader** — either via election (majority vote among replicas) or appointment by a controller node. The best candidate is the replica with the most up-to-date data from the old leader, to minimize data loss.
3. **Reconfigure the system** — clients must send writes to the new leader; other followers must replicate from it; the old leader (if it returns) must recognize it is now a follower.

Failover can be **manual** (an operator performs the steps) or **automatic** (the system does it). Many operations teams prefer manual failover despite its slowness, because automatic failover introduces its own failure modes.

## Things that can go wrong

**Lost writes**: in asynchronous replication, the new leader may not have received all writes the old leader acknowledged to clients. The standard resolution — discard the old leader's unreplicated writes — violates clients' durability expectations. This is especially dangerous when other systems (caches, queues, external databases) depend on those writes having occurred.

*Example from production*: GitHub promoted an out-of-date MySQL follower to leader. Its autoincrement counter had lagged, so it reused primary key values the old leader had already issued. Those keys were also used in Redis. The resulting inconsistency leaked private data to the wrong users.

**Split brain**: if the old leader comes back before realizing it has been replaced, two nodes may both believe they are the leader. If both accept writes without a conflict resolution mechanism, data is lost or corrupted. Systems use **fencing** (also called STONITH — *Shoot The Other Node In The Head*) to forcibly shut down the old leader, but if fencing is misconfigured, both nodes can be shut down.

**Timeout tuning**: a timeout that's too long means a long recovery window when the leader genuinely fails. A timeout that's too short causes spurious failovers during temporary load spikes or network hiccups — and an unnecessary failover during an already-stressed period makes things worse.

**No foolproof detection**: there is no way to definitively distinguish "the leader is dead" from "the leader is alive but I can't reach it." This ambiguity is a fundamental property of distributed systems, explored more deeply in the context of consensus in Chapter 9.

## Why failover is hard in practice

All of these issues — lost writes, split brain, false positives — stem from the same root cause: distributed systems have no single source of truth about what has happened. The nodes must agree on a new leader, but achieving that agreement under arbitrary failures is the consensus problem. Replication alone doesn't solve it; it requires coordination protocols (explored in the consensus chapter).

## Failure detection challenges from Chapter 8

Chapter 8 deepens the understanding of why failure detection -- the first step of failover -- is so hard (source: designing-data-intensive-applications, chapter 8):

- **[[unreliable-networks]]** make it impossible to distinguish a dead node from a slow one or a network partition. The only reliable mechanism is a [[timeouts|timeout]], but timeouts introduce a tradeoff between detection speed and false positives.
- **[[process-pauses]]** (GC, VM suspension, disk I/O) can make a live node appear dead for arbitrary periods. After the pause, the node resumes and doesn't realize it was "gone."
- **Premature death declarations** under load can trigger cascading failures: transferring a "dead" node's load to other nodes overloads them, causing more nodes to appear dead.
- **Adaptive timeouts** (e.g., Phi Accrual failure detectors used in Akka and Cassandra) can reduce false positives by tracking response time distributions rather than using a fixed threshold.

Even after detecting a failure, the replacement leader must be protected from the old leader resuming and issuing conflicting writes. [[fencing-tokens]] provide a mechanism for this: the resource itself rejects writes from stale leaders carrying outdated tokens.

## Consensus: the real solution

Chapter 9 makes explicit what earlier chapters foreshadowed: failover is fundamentally the [[consensus]] problem. All nodes must agree on who the new leader is, but achieving agreement under arbitrary network failures requires a consensus algorithm. (source: designing-data-intensive-applications, chapter 9)

Three approaches to handling leader failure (source: designing-data-intensive-applications, chapter 9):

1. **Wait for the leader to recover**: the system blocks. Does not satisfy the termination property of consensus. Many XA/JTA coordinators use this approach (see [[two-phase-commit]]).
2. **Manual failover**: a human chooses the new leader. Consensus by "act of God" -- correct but slow.
3. **Automatic consensus-based election**: use a proven algorithm (Raft, Zab, Paxos) via tools like [[zookeeper]] or etcd to elect a new leader safely, handling split brain and stale replicas.

Even single-leader databases that do not run consensus on every write still require consensus for leader election and leadership changes. Having a leader "kicks the can down the road" -- consensus is still needed, just less frequently. (source: designing-data-intensive-applications, chapter 9)

## Failover at the container level

Burns's *Designing Distributed Systems* Chapter 9 covers failover in the specific idiom of containerised services. His prescription has three layers (source: raw/designing-distributed-systems/chapter-09-ownership-election.md):

1. **Decide whether you need failover at all.** For many workloads, a [[singleton-pattern|singleton]] under Kubernetes already achieves three to four nines of uptime via automatic restart and machine-level rescheduling. The machinery of proper master election is warranted only when the SLA or the rollout-window constraint demands it.
2. **Outsource consensus.** Use etcd, [[zookeeper]], or Consul rather than implementing Paxos or Raft yourself. The KV store provides compare-and-swap and TTL, and the application builds locks and leases on top.
3. **Use [[renewable-leases]] for long-running ownership.** Short TTL, background refresh every `ttl/2`, terminate the process if refresh fails (and let the orchestrator restart it as a passive secondary).

Burns's named alternative to failover — the [[singleton-pattern]] — is worth surfacing because it is rarely treated as a serious option in the replication literature. The book argues explicitly that "distributed" is not always the right answer, and for background asynchronous work, a single orchestrated replica is simpler, cheaper, and probably good enough. See [[ownership-election-pattern]] for the full pattern.

## Related pages

- [[leader-based-replication]]
- [[replication]]
- [[fault-tolerance]]
- [[timeouts]]
- [[process-pauses]]
- [[unreliable-networks]]
- [[fencing-tokens]]
- [[truth-and-leadership-in-distributed-systems]]
- [[consensus]]
- [[two-phase-commit]]
- [[zookeeper]]
- [[ownership-election-pattern]]
- [[singleton-pattern]]
- [[renewable-leases]]
